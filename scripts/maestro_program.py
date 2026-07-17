#!/usr/bin/env python3
"""Executable governance engine for the MAESTRO continuous program backlog."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from maestro_program_lib.actions import *  # noqa: F403
from maestro_program_lib.core import *  # noqa: F403
from maestro_program_lib.lanes import *  # noqa: F403
from maestro_program_lib.model import *  # noqa: F403
from maestro_program_lib.plan import *  # noqa: F403
from maestro_program_lib.receipts import *  # noqa: F403


def emit(payload: dict[str, Any], exit_code: int = 0) -> int:
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return exit_code


def add_program_paths(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", default=".")
    parser.add_argument("--mandate", default=DEFAULT_FILES["mandate"])
    parser.add_argument("--backlog", default=DEFAULT_FILES["backlog"])
    parser.add_argument("--state", default=DEFAULT_FILES["state"])
    parser.add_argument("--findings", default=DEFAULT_FILES["findings"])
    parser.add_argument("--queue", default=DEFAULT_FILES["queue"])
    parser.add_argument("--repo", action="append", default=[], help="repository mapping ID=PATH")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    for name in ("doctor", "plan", "refresh-queue"):
        child = commands.add_parser(name)
        add_program_paths(child)

    change = commands.add_parser("validate-change")
    change.add_argument("--root", default=".")
    change.add_argument("--mandate", default=DEFAULT_FILES["mandate"])
    change.add_argument("--repo-root", required=True)
    change.add_argument("--repo-id", default="coordinator")
    change.add_argument("--base", required=True)
    change.add_argument("--head", default="WORKTREE")

    wave = commands.add_parser("validate-wave")
    wave.add_argument("--plan", required=True)
    wave.add_argument("--journal", required=True)

    start = commands.add_parser("lane-start")
    start.add_argument("--journal", required=True)
    start.add_argument("--task-id", required=True)
    start.add_argument("--lane-id", required=True)
    start.add_argument("--worker-id", required=True)
    start.add_argument("--workspace", required=True)
    start.add_argument("--baseline", required=True)
    start.add_argument("--path", action="append", default=[])

    finish = commands.add_parser("lane-finish")
    finish.add_argument("--journal", required=True)
    finish.add_argument("--lane-id", required=True)
    finish.add_argument("--worker-id", required=True)
    finish.add_argument("--artifact", action="append", default=[])
    finish.add_argument("--log", required=True)
    finish.add_argument("--result", required=True)

    receipt = commands.add_parser("prepare-receipt")
    add_program_paths(receipt)
    receipt.add_argument("--task-id", required=True)
    receipt.add_argument("--repo-id", required=True)
    receipt.add_argument("--repo-root", required=True)
    receipt.add_argument("--acceptance-command", required=True)
    receipt.add_argument("--evidence", action="append", default=[])
    receipt.add_argument("--gate", action="append", default=[])

    finding = commands.add_parser("register-finding")
    add_program_paths(finding)
    finding.add_argument("--payload", required=True)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "validate-wave":
            result = validate_wave(read_json(Path(args.plan)), Path(args.journal).resolve())
            return emit(result, 0 if result["valid"] else 2)
        if args.command == "lane-start":
            return emit(lane_start(Path(args.journal).resolve(), args.task_id, args.lane_id, args.worker_id, args.baseline, args.path, args.workspace))
        if args.command == "lane-finish":
            return emit(lane_finish(Path(args.journal).resolve(), args.lane_id, args.worker_id, args.artifact, args.log, args.result))
        files = resolve_files(args.root, args)
        mandate, backlog, state, findings = load_program(files)
        repo_map = parse_repo_map(getattr(args, "repo", []), files.root, mandate)
        if args.command == "validate-change":
            result = validate_change(mandate, Path(args.repo_root).resolve(), args.base, args.head, args.repo_id)
            return emit(result, 0 if result["valid"] else 2)
        reasons = validate_program(files, mandate, backlog, state, findings, repo_map, check_queue=args.command != "refresh-queue")
        if args.command == "doctor":
            result = {"valid": not reasons, "reasons": reasons, "source_hashes": program_hashes(mandate, backlog, state, findings)}
            return emit(result, 0 if result["valid"] else 2)
        if args.command in {"plan", "refresh-queue"}:
            plan_result = build_plan(mandate, backlog, state, findings, repo_map, reasons)
            if args.command == "refresh-queue":
                snapshot = queue_snapshot(mandate, backlog, state, findings, plan_result)
                atomic_write_json(files.queue, snapshot)
                return emit(snapshot, 0 if plan_result["valid"] else 2)
            return emit(plan_result, 0 if plan_result["valid"] else 2)
        if args.command == "prepare-receipt":
            receipt = prepare_receipt(files, mandate, backlog, findings, args.task_id, args.repo_id, Path(args.repo_root).resolve(), args.acceptance_command, args.evidence, args.gate)
            return emit(receipt)
        if args.command == "register-finding":
            payload = read_json(Path(args.payload).resolve())
            _new_backlog, new_state, new_findings = register_finding(backlog, state, findings, payload)
            atomic_write_json(files.state, new_state)
            atomic_write_json(files.findings, new_findings)
            return emit({"valid": True, "finding_id": payload["id"], "correction_task_id": payload["correction_task"]["id"]})
        raise ContractError("UNKNOWN_COMMAND")
    except ContractError as error:
        return emit({"valid": False, "reasons": error.reasons}, 2)


if __name__ == "__main__":
    raise SystemExit(main())
