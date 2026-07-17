from maestro_program_lib.core import *  # noqa: F403
from maestro_program_lib.model import *  # noqa: F403
from maestro_program_lib.receipts import *  # noqa: F403


def build_lanes(eligible_tasks: list[dict[str, Any]], state: dict[str, Any]) -> list[dict[str, Any]]:
    lanes: list[dict[str, Any]] = []
    baseline = state.get("baseline_heads", {})
    for index, task in enumerate(eligible_tasks, start=1):
        lanes.append(
            {
                "lane_id": f"LANE-{index:02d}-{task['id']}",
                "task_ids": [task["id"]],
                "repositories": task.get("repositories", []),
                "paths": sorted(normalize_path(path) for path in task.get("paths", [])),
                "baseline_heads": {repo: baseline.get(repo, "resolve-at-start") for repo in task.get("repositories", [])},
                "required_output": task.get("output", "task artifact and command log"),
            }
        )
    return lanes


def actionable_findings(findings: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        finding
        for finding in finding_list(findings)
        if finding.get("state") == "open" and finding.get("actionable", True)
    ]


def build_plan(
    mandate: dict[str, Any],
    backlog: dict[str, Any],
    state: dict[str, Any],
    findings: dict[str, Any],
    repo_map: dict[str, Path],
    validation_reasons: list[str] | None = None,
) -> dict[str, Any]:
    tasks = program_task_map(backlog, findings)
    effective, receipt_errors, receipt_commits = effective_task_states(mandate, backlog, state, findings, repo_map)
    eligible: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []
    unsafe_classes = set(mandate.get("unsafe_operation_classes", []))
    for task_id, task in tasks.items():
        task_state = effective[task_id]
        auto_activate = task.get("auto_activate", True)
        ready = task_state in {"ready", "planned"} and auto_activate and dependency_satisfied(task, effective)
        safe = task.get("reversible", True) and task.get("operation_class") not in unsafe_classes
        if ready and safe and not task.get("requires_orchestrator_acceptance", False):
            item = dict(task)
            item["effective_state"] = "ready"
            eligible.append(item)
        else:
            if task_state in TERMINAL_STATES:
                reason = "TERMINAL"
            elif task_state == "task_remote_verified":
                reason = "ORCHESTRATOR_REVIEW_REQUIRED"
            elif task_state == "blocked_human":
                reason = "VALID_HUMAN_GATE" if valid_human_gate(task_id, state, mandate) else "INVALID_HUMAN_GATE"
            elif task_state == "blocked_environment":
                reason = "ENVIRONMENT_BLOCK_EXHAUSTED" if environment_block_exhausted(task_id, state) else "ENVIRONMENT_BLOCK_INCOMPLETE"
            elif task_state in {"failed", "correction_required"}:
                reason = "CORRECTION_TASK_REQUIRED"
            elif not dependency_satisfied(task, effective):
                reason = "DEPENDENCY_NOT_SATISFIED"
            elif not safe or task.get("requires_orchestrator_acceptance", False):
                reason = "HUMAN_GATE_DECLARATION_REQUIRED"
            else:
                reason = "TASK_NOT_ACTIVATED"
            blocked.append({"task_id": task_id, "state": task_state, "reason": reason})
    eligible.sort(key=lambda item: (-int(item.get("priority", 0)), item["id"]))
    lanes = build_lanes(eligible, state)
    parallelism_required = any(
        set(left.get("repositories", [])).isdisjoint(set(right.get("repositories", [])))
        or not any_path_conflict(left.get("paths", []), right.get("paths", []))
        for index, left in enumerate(eligible)
        for right in eligible[index + 1 :]
    )
    open_findings = actionable_findings(findings)
    invalid = sorted(set(validation_reasons or []))
    all_terminal = all(value in TERMINAL_STATES for value in effective.values())
    only_valid_human = bool(blocked) and all(item["reason"] in {"TERMINAL", "VALID_HUMAN_GATE"} for item in blocked)
    environment_only = bool(blocked) and all(
        item["reason"] in {"TERMINAL", "ENVIRONMENT_BLOCK_EXHAUSTED", "ORCHESTRATOR_REVIEW_REQUIRED"}
        for item in blocked
    )
    if invalid:
        stop_allowed = False
        checkpoint_allowed = False
        stop_reason = "PROGRAM_INVALID"
    elif eligible:
        stop_allowed = False
        checkpoint_allowed = False
        stop_reason = "ELIGIBLE_WORK_REMAINS"
    elif open_findings:
        stop_allowed = False
        checkpoint_allowed = False
        stop_reason = "OPEN_ACTIONABLE_FINDINGS"
    elif all_terminal:
        stop_allowed = True
        checkpoint_allowed = True
        stop_reason = "PROGRAM_COMPLETE"
    elif only_valid_human:
        stop_allowed = True
        checkpoint_allowed = True
        stop_reason = "VALID_HUMAN_GATE_ONLY"
    elif environment_only:
        stop_allowed = False
        checkpoint_allowed = True
        stop_reason = "ORCHESTRATOR_OR_ENVIRONMENT_CHECKPOINT"
    else:
        stop_allowed = False
        checkpoint_allowed = False
        stop_reason = "BACKLOG_NOT_EXHAUSTED_OR_BLOCK_INVALID"
    return {
        "valid": not invalid,
        "validation_reasons": invalid,
        "effective_states": effective,
        "eligible_tasks": [task["id"] for task in eligible],
        "blocked_tasks": blocked,
        "receipt_errors": receipt_errors,
        "receipt_commits": receipt_commits,
        "open_actionable_findings": [finding["id"] for finding in open_findings],
        "lanes": lanes,
        "integration_order": [task["id"] for task in eligible],
        "parallelism_required": parallelism_required and len(eligible) >= 2,
        "commit_mode": "serial-per-task-per-repository",
        "stop_allowed": stop_allowed,
        "checkpoint_allowed": checkpoint_allowed,
        "stop_reason": stop_reason,
        "program_complete": all_terminal,
    }


def queue_snapshot(
    mandate: dict[str, Any], backlog: dict[str, Any], state: dict[str, Any], findings: dict[str, Any], plan: dict[str, Any]
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "program_id": mandate.get("program_id"),
        "derived": True,
        "source_hashes": program_hashes(mandate, backlog, state, findings),
        "eligible_tasks": plan["eligible_tasks"],
        "blocked_tasks": plan["blocked_tasks"],
        "lanes": plan["lanes"],
        "integration_order": plan["integration_order"],
        "parallelism_required": plan["parallelism_required"],
        "stop_allowed": plan["stop_allowed"],
        "checkpoint_allowed": plan["checkpoint_allowed"],
        "stop_reason": plan["stop_reason"],
    }


def validate_change(mandate: dict[str, Any], repo_root: Path, base: str, head: str | None, repo_id: str = "coordinator") -> dict[str, Any]:
    entries = git_changed_paths(repo_root, base, head)
    violations: list[dict[str, str]] = []
    changed: set[str] = set()
    for status, old, new in entries:
        for path in [old, new]:
            if not path:
                continue
            changed.add(path)
            if protected_match(path, mandate, repo_id):
                violations.append({"status": status, "path": path})
    return {
        "valid": not violations,
        "reasons": [] if not violations else ["ORCHESTRATOR_OWNED_PATH_CHANGED"],
        "changed_paths": sorted(changed),
        "protected_violations": violations,
    }
