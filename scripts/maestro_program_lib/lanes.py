from maestro_program_lib.core import *  # noqa: F403


def parse_timestamp(value: Any) -> dt.datetime:
    if not isinstance(value, str):
        raise ValueError
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = dt.datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError
    return parsed


def journal_events(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    events: list[dict[str, Any]] = []
    previous_hash = "GENESIS"
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        event = json.loads(raw)
        supplied_hash = event.pop("event_hash", None)
        if event.get("previous_hash") != previous_hash:
            raise ContractError("LANE_JOURNAL_HASH_CHAIN_INVALID")
        expected_hash = sha256_bytes(canonical_json_bytes(event))
        if supplied_hash != expected_hash:
            raise ContractError("LANE_JOURNAL_EVENT_HASH_INVALID")
        event["event_hash"] = supplied_hash
        events.append(event)
        previous_hash = supplied_hash
    return events


def append_journal_event(path: Path, event: dict[str, Any]) -> dict[str, Any]:
    events = journal_events(path)
    event["previous_hash"] = events[-1]["event_hash"] if events else "GENESIS"
    event["event_hash"] = sha256_bytes(canonical_json_bytes(event))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    return event


def lane_start(journal: Path, task_id: str, lane_id: str, worker_id: str, baseline: str, paths: list[str]) -> dict[str, Any]:
    events = journal_events(journal)
    if any(event.get("lane_id") == lane_id and event.get("event") == "start" for event in events):
        raise ContractError("LANE_ALREADY_STARTED")
    return append_journal_event(
        journal,
        {
            "event": "start",
            "event_id": str(uuid.uuid4()),
            "lane_id": lane_id,
            "task_id": task_id,
            "worker_id": worker_id,
            "baseline": baseline,
            "paths": sorted(normalize_path(path) for path in paths),
            "started_at": utc_now(),
        },
    )


def lane_finish(journal: Path, lane_id: str, worker_id: str, artifacts: list[str], log_path: str, result: str) -> dict[str, Any]:
    events = journal_events(journal)
    starts = [event for event in events if event.get("event") == "start" and event.get("lane_id") == lane_id]
    if len(starts) != 1:
        raise ContractError("LANE_START_REQUIRED")
    if starts[0].get("worker_id") != worker_id:
        raise ContractError("LANE_WORKER_MISMATCH")
    if any(event.get("event") == "finish" and event.get("lane_id") == lane_id for event in events):
        raise ContractError("LANE_ALREADY_FINISHED")
    artifact_records: list[dict[str, Any]] = []
    for raw in artifacts:
        path = Path(raw).resolve()
        if not path.is_file() or path.stat().st_size == 0:
            raise ContractError(f"LANE_ARTIFACT_INVALID:{raw}")
        artifact_records.append({"path": str(path), "sha256": sha256_file(path), "size": path.stat().st_size})
    log = Path(log_path).resolve()
    if not log.is_file() or log.stat().st_size == 0:
        raise ContractError("LANE_COMMAND_LOG_REQUIRED")
    return append_journal_event(
        journal,
        {
            "event": "finish",
            "event_id": str(uuid.uuid4()),
            "lane_id": lane_id,
            "worker_id": worker_id,
            "finished_at": utc_now(),
            "artifacts": artifact_records,
            "command_log": {"path": str(log), "sha256": sha256_file(log), "size": log.stat().st_size},
            "result": result,
        },
    )


def validate_wave(plan: dict[str, Any], journal: Path) -> dict[str, Any]:
    try:
        events = journal_events(journal)
    except (ContractError, json.JSONDecodeError) as error:
        reasons = error.reasons if isinstance(error, ContractError) else ["LANE_JOURNAL_INVALID_JSON"]
        return {"valid": False, "reasons": reasons, "parallelism_demonstrated": False}
    plan_lanes = {lane["lane_id"]: lane for lane in plan.get("lanes", []) if isinstance(lane, dict) and lane.get("lane_id")}
    starts = {event["lane_id"]: event for event in events if event.get("event") == "start"}
    finishes = {event["lane_id"]: event for event in events if event.get("event") == "finish"}
    reasons: list[str] = []
    intervals: list[tuple[str, str, dt.datetime, dt.datetime]] = []
    for lane_id, lane in plan_lanes.items():
        if lane_id not in starts or lane_id not in finishes:
            continue
        start = starts[lane_id]
        finish = finishes[lane_id]
        if start.get("worker_id") != finish.get("worker_id"):
            reasons.append(f"LANE_WORKER_MISMATCH:{lane_id}")
            continue
        try:
            started_at = parse_timestamp(start.get("started_at"))
            finished_at = parse_timestamp(finish.get("finished_at"))
        except ValueError:
            reasons.append(f"INVALID_LANE_INTERVAL:{lane_id}")
            continue
        if finished_at <= started_at:
            reasons.append(f"INVALID_LANE_INTERVAL:{lane_id}")
            continue
        if sorted(normalize_path(path) for path in start.get("paths", [])) != sorted(normalize_path(path) for path in lane.get("paths", [])):
            reasons.append(f"LANE_PATH_OWNERSHIP_MISMATCH:{lane_id}")
        for artifact in finish.get("artifacts", []):
            path = Path(str(artifact.get("path", "")))
            if not path.is_file() or sha256_file(path) != artifact.get("sha256") or path.stat().st_size == 0:
                reasons.append(f"LANE_ARTIFACT_HASH_INVALID:{lane_id}")
        log = finish.get("command_log", {})
        log_path = Path(str(log.get("path", "")))
        if not log_path.is_file() or sha256_file(log_path) != log.get("sha256") or log_path.stat().st_size == 0:
            reasons.append(f"LANE_COMMAND_LOG_INVALID:{lane_id}")
        intervals.append((lane_id, str(start.get("worker_id")), started_at, finished_at))
    overlap = False
    for index, left in enumerate(intervals):
        for right in intervals[index + 1 :]:
            if left[1] == right[1]:
                continue
            if left[2] < right[3] and right[2] < left[3]:
                overlap = True
                break
        if overlap:
            break
    if plan.get("parallelism_required"):
        if len(intervals) < 2:
            reasons.append("AT_LEAST_TWO_COMPLETED_LANES_REQUIRED")
        if len({item[1] for item in intervals}) < 2:
            reasons.append("DISTINCT_WORKERS_REQUIRED")
        if not overlap:
            reasons.append("SUBSTANTIVE_PARALLELISM_NOT_DEMONSTRATED")
    return {"valid": not reasons, "reasons": sorted(set(reasons)), "parallelism_demonstrated": overlap}
