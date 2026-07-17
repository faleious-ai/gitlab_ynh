#!/usr/bin/env python3
"""Deterministic planner and gate validator for the MAESTRO program queue."""

from __future__ import annotations

import argparse
import datetime as datetime_module
import json
import sys
from pathlib import Path
from typing import Any


SUCCESS_STATES = {
    "accepted",
    "completed",
    "machine_green_awaiting_review",
    "remote_verified",
    "task_remote_verified",
}
HUMAN_GATE_CLASSES = {
    "credential_required",
    "external_authorization",
    "financial_cost",
    "legal_or_ethical_decision",
    "product_consequence",
    "irreversible_operation",
    "destructive_production_action",
}
UNSAFE_OPERATION_CLASSES = {
    "credential",
    "deploy",
    "destructive",
    "irreversible",
    "promotion",
    "production_credential",
    "release",
}


class ContractError(Exception):
    """A user-facing contract failure that must be emitted as JSON."""

    def __init__(self, *reasons: str) -> None:
        self.reasons = list(reasons)
        super().__init__(", ".join(self.reasons))


def read_json(path: str) -> dict[str, Any]:
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ContractError("INVALID_JSON_INPUT") from error
    if not isinstance(payload, dict):
        raise ContractError("JSON_OBJECT_REQUIRED")
    return payload


def task_list(queue: dict[str, Any]) -> list[dict[str, Any]]:
    tasks = queue.get("tasks")
    if not isinstance(tasks, list):
        raise ContractError("TASK_LIST_REQUIRED")
    result: list[dict[str, Any]] = []
    ids: set[str] = set()
    for task in tasks:
        if not isinstance(task, dict) or not isinstance(task.get("id"), str):
            raise ContractError("TASK_ID_REQUIRED")
        if task["id"] in ids:
            raise ContractError("DUPLICATE_TASK_ID")
        ids.add(task["id"])
        result.append(task)
    return result


def dependency_satisfied(task: dict[str, Any], by_id: dict[str, dict[str, Any]]) -> bool:
    dependencies = task.get("dependencies", [])
    if not isinstance(dependencies, list):
        return False
    return all(
        dependency in by_id and by_id[dependency].get("status") in SUCCESS_STATES
        for dependency in dependencies
    )


def blocked_reason(task: dict[str, Any], by_id: dict[str, dict[str, Any]]) -> str:
    status = task.get("status")
    if status == "blocked_environment":
        return "ENVIRONMENT_BLOCKED"
    if status == "blocked_human":
        return "HUMAN_GATE_REQUIRED"
    if status in SUCCESS_STATES:
        return "AWAITING_REVIEW"
    if not dependency_satisfied(task, by_id):
        return "DEPENDENCY_NOT_SATISFIED"
    if task.get("requires_orchestrator_acceptance"):
        return "ORCHESTRATOR_ACCEPTANCE_REQUIRED"
    if not task.get("reversible", True):
        return "IRREVERSIBLE_OPERATION"
    if task.get("operation_class") in UNSAFE_OPERATION_CLASSES:
        return "HUMAN_GATE_REQUIRED"
    if status != "ready":
        return "TASK_NOT_READY"
    return "TASK_BLOCKED"


def paths_for(task: dict[str, Any]) -> set[str]:
    paths = task.get("paths", [])
    return {path for path in paths if isinstance(path, str)} if isinstance(paths, list) else set()


def build_lanes(eligible: list[dict[str, Any]], state: dict[str, Any]) -> list[dict[str, Any]]:
    baseline = state.get("baseline_head", "unresolved")
    lanes: list[dict[str, Any]] = []
    for index, task in enumerate(eligible, start=1):
        lanes.append(
            {
                "lane_id": f"LANE-{index:02d}-{task['id']}",
                "task_ids": [task["id"]],
                "ownership": task.get("owner") or task.get("work_package") or "unassigned",
                "paths": sorted(paths_for(task)),
                "baseline": baseline,
                "output": task.get("output", "task output pending"),
            }
        )
    return lanes


def build_plan(mandate: dict[str, Any], queue: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
    tasks = task_list(queue)
    by_id = {task["id"]: task for task in tasks}
    eligible: list[dict[str, Any]] = []
    blocked: list[dict[str, str]] = []
    for task in tasks:
        status = task.get("status")
        ready = (
            status == "ready"
            and dependency_satisfied(task, by_id)
            and not task.get("requires_orchestrator_acceptance", False)
            and task.get("reversible", True)
            and task.get("operation_class") not in UNSAFE_OPERATION_CLASSES
        )
        if ready:
            eligible.append(task)
        else:
            blocked.append({"task_id": task["id"], "reason": blocked_reason(task, by_id)})

    eligible.sort(key=lambda task: (-int(task.get("priority", 0)), task["id"]))
    lanes = build_lanes(eligible, state)
    separable = False
    for index, left in enumerate(eligible):
        for right in eligible[index + 1 :]:
            if paths_for(left).isdisjoint(paths_for(right)):
                separable = True
                break
        if separable:
            break
    parallelism_required = len(eligible) >= 2 and separable
    stop_allowed = not eligible
    if eligible:
        stop_reason = "ELIGIBLE_WORK_REMAINS"
    elif blocked:
        stop_reason = "NO_ELIGIBLE_WORK_PENDING_GATE_OR_BLOCK"
    else:
        stop_reason = "QUEUE_COMPLETE"
    return {
        "eligible_tasks": [task["id"] for task in eligible],
        "blocked_tasks": blocked,
        "lanes": lanes,
        "integration_order": [task["id"] for task in eligible],
        "parallelism_required": parallelism_required,
        "commit_mode": "serial",
        "stop_allowed": stop_allowed,
        "stop_reason": stop_reason,
        "protected_paths": mandate.get("protected_paths", []),
    }


def parse_timestamp(value: Any) -> datetime_module.datetime:
    if not isinstance(value, str):
        raise ValueError
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime_module.datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError
    return parsed


def validate_wave(plan: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    plan_lane_ids = {lane.get("lane_id") for lane in plan.get("lanes", []) if isinstance(lane, dict)}
    supplied = [lane for lane in evidence.get("lanes", []) if isinstance(lane, dict)]
    lanes = [lane for lane in supplied if lane.get("lane_id") in plan_lane_ids]
    reasons: list[str] = []
    intervals: list[tuple[datetime_module.datetime, datetime_module.datetime]] = []
    for lane in lanes:
        try:
            started = parse_timestamp(lane.get("started_at"))
            finished = parse_timestamp(lane.get("finished_at"))
        except (TypeError, ValueError):
            reasons.append("INVALID_LANE_INTERVAL")
            continue
        if finished <= started:
            reasons.append("INVALID_LANE_INTERVAL")
            continue
        intervals.append((started, finished))
    if len(intervals) < 2:
        reasons.append("AT_LEAST_TWO_LANES_REQUIRED")
    overlap = False
    for index, (_, finish) in enumerate(intervals):
        for start, _ in intervals[index + 1 :]:
            if start < finish:
                overlap = True
                break
        if overlap:
            break
    if len(intervals) >= 2 and not overlap:
        reasons.append("PARALLELISM_NOT_DEMONSTRATED")
    valid = not reasons
    return {"valid": valid, "reasons": reasons, "parallelism_demonstrated": overlap}


def validate_gate(mandate: dict[str, Any], queue: dict[str, Any], state: dict[str, Any], gate: dict[str, Any]) -> dict[str, Any]:
    plan = build_plan(mandate, queue, state)
    reasons: list[str] = []
    allowed = set(mandate.get("human_gate_classes", HUMAN_GATE_CLASSES))
    reason_class = gate.get("reason_class")
    if reason_class not in allowed or reason_class not in HUMAN_GATE_CLASSES:
        reasons.append("INVALID_HUMAN_GATE_CLASS")
    if plan["eligible_tasks"]:
        reasons.append("INDEPENDENT_WORK_REMAINS")
    blocked_task = gate.get("blocked_task")
    tasks = {task["id"]: task for task in task_list(queue)}
    if blocked_task not in tasks or tasks[blocked_task].get("status") != "blocked_human":
        reasons.append("BLOCKED_HUMAN_TASK_REQUIRED")
    if gate.get("external_authority") is not True:
        reasons.append("EXTERNAL_AUTHORITY_REQUIRED")
    for field in ("condition", "evidence", "fallbacks_attempted", "requested_human_action", "safe_state", "resume"):
        value = gate.get(field)
        if not value:
            reasons.append(f"{field.upper()}_REQUIRED")
    return {
        "valid": not reasons,
        "reasons": reasons,
        "stop_allowed": not reasons,
        "eligible_tasks": plan["eligible_tasks"],
    }


def validate_change(mandate: dict[str, Any], actor: str, paths: list[str]) -> dict[str, Any]:
    protected = [path for path in mandate.get("protected_paths", []) if isinstance(path, str)]
    matched = [path for path in paths if path in protected]
    valid = actor != "executor" or not matched
    return {
        "valid": valid,
        "reasons": [] if valid else ["ORCHESTRATOR_OWNED_PATH"],
        "protected_paths": matched,
    }


def emit(payload: dict[str, Any], exit_code: int = 0) -> int:
    print(json.dumps(payload, ensure_ascii=True, sort_keys=True))
    return exit_code


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    plan = commands.add_parser("plan")
    plan.add_argument("--mandate", required=True)
    plan.add_argument("--queue", required=True)
    plan.add_argument("--state", required=True)

    gate = commands.add_parser("validate-gate")
    gate.add_argument("--mandate", required=True)
    gate.add_argument("--queue", required=True)
    gate.add_argument("--state", required=True)
    gate.add_argument("--gate", required=True)

    wave = commands.add_parser("validate-wave")
    wave.add_argument("--plan", required=True)
    wave.add_argument("--evidence", required=True)

    change = commands.add_parser("validate-change")
    change.add_argument("--mandate", required=True)
    change.add_argument("--actor", required=True)
    change.add_argument("--paths", nargs="+", required=True)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "plan":
            return emit(build_plan(read_json(args.mandate), read_json(args.queue), read_json(args.state)))
        if args.command == "validate-gate":
            result = validate_gate(
                read_json(args.mandate),
                read_json(args.queue),
                read_json(args.state),
                read_json(args.gate),
            )
            return emit(result, 0 if result["valid"] else 2)
        if args.command == "validate-wave":
            result = validate_wave(read_json(args.plan), read_json(args.evidence))
            return emit(result, 0 if result["valid"] else 2)
        if args.command == "validate-change":
            result = validate_change(read_json(args.mandate), args.actor, args.paths)
            return emit(result, 0 if result["valid"] else 2)
        raise ContractError("UNKNOWN_COMMAND")
    except ContractError as error:
        return emit({"valid": False, "reasons": error.reasons}, 2)


if __name__ == "__main__":
    sys.exit(main())
