#!/usr/bin/env python3
"""Executable governance engine for the MAESTRO continuous program backlog.

The engine treats the backlog as the complete authorized program, derives task
state from orchestrator decisions and remotely published task receipts, protects
acceptance contracts from the real Git diff, validates substantive parallel
lanes, and distinguishes program completion from a review/environment checkpoint.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import uuid
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

SCHEMA_VERSION = 2
DEFAULT_FILES = {
    "mandate": "continuity/PROGRAM_MANDATE.json",
    "backlog": "continuity/PROGRAM_BACKLOG.json",
    "state": "continuity/PROGRAM_STATE.json",
    "findings": "continuity/PROGRAM_FINDINGS.json",
    "queue": "continuity/PROGRAM_QUEUE.json",
}
DERIVED_SUCCESS_STATES = {"task_remote_verified", "accepted"}
DEPENDENCY_SUCCESS_STATES = {"task_remote_verified", "accepted", "superseded"}
TERMINAL_STATES = {"accepted", "superseded"}
HUMAN_GATE_STATES = {"blocked_human"}
ENVIRONMENT_GATE_STATES = {"blocked_environment"}
OVERRIDE_STATES = {
    "accepted",
    "blocked_environment",
    "blocked_human",
    "correction_required",
    "failed",
    "in_progress",
    "ready",
    "superseded",
}


class ContractError(Exception):
    def __init__(self, *reasons: str) -> None:
        self.reasons = list(reasons)
        super().__init__(", ".join(self.reasons))


@dataclass(frozen=True)
class ProgramFiles:
    root: Path
    mandate: Path
    backlog: Path
    state: Path
    findings: Path
    queue: Path


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_path(value: str) -> str:
    value = value.replace("\\", "/").strip()
    while value.startswith("./"):
        value = value[2:]
    path = str(PurePosixPath(value))
    return "" if path == "." else path.rstrip("/")


def path_contains(parent: str, child: str) -> bool:
    parent_n = normalize_path(parent)
    child_n = normalize_path(child)
    return bool(parent_n) and (child_n == parent_n or child_n.startswith(parent_n + "/"))


def paths_conflict(left: str, right: str) -> bool:
    return path_contains(left, right) or path_contains(right, left)


def any_path_conflict(left: Iterable[str], right: Iterable[str]) -> bool:
    return any(paths_conflict(a, b) for a in left for b in right)


def canonical_json_bytes(payload: Any) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def atomic_write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", dir=path.parent, prefix=f".{path.name}.", delete=False
        ) as handle:
            temporary = handle.name
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)


def read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ContractError(f"INVALID_JSON:{path.as_posix()}") from error
    if not isinstance(payload, dict):
        raise ContractError(f"JSON_OBJECT_REQUIRED:{path.as_posix()}")
    return payload


def resolve_files(root: str, args: argparse.Namespace) -> ProgramFiles:
    root_path = Path(root).resolve()
    return ProgramFiles(
        root=root_path,
        mandate=(root_path / getattr(args, "mandate", DEFAULT_FILES["mandate"])).resolve(),
        backlog=(root_path / getattr(args, "backlog", DEFAULT_FILES["backlog"])).resolve(),
        state=(root_path / getattr(args, "state", DEFAULT_FILES["state"])).resolve(),
        findings=(root_path / getattr(args, "findings", DEFAULT_FILES["findings"])).resolve(),
        queue=(root_path / getattr(args, "queue", DEFAULT_FILES["queue"])).resolve(),
    )


def load_program(files: ProgramFiles) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    return read_json(files.mandate), read_json(files.backlog), read_json(files.state), read_json(files.findings)


def parse_repo_map(values: list[str] | None, root: Path, mandate: dict[str, Any]) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for repo in mandate.get("repositories", []):
        if not isinstance(repo, dict) or not isinstance(repo.get("id"), str):
            continue
        relative = repo.get("relative_path")
        if isinstance(relative, str):
            result[repo["id"]] = (root / relative).resolve()
    for value in values or []:
        if "=" not in value:
            raise ContractError("REPO_MAPPING_MUST_BE_ID_EQUALS_PATH")
        repo_id, raw_path = value.split("=", 1)
        result[repo_id.strip()] = Path(raw_path).resolve()
    return result


def run_git(repo_root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if check and completed.returncode != 0:
        raise ContractError(f"GIT_COMMAND_FAILED:{' '.join(args)}")
    return completed


def git_available(repo_root: Path) -> bool:
    return run_git(repo_root, "rev-parse", "--is-inside-work-tree", check=False).returncode == 0


def git_ref(repo_root: Path, ref: str) -> str:
    return run_git(repo_root, "rev-parse", ref).stdout.strip()


def git_subject(repo_root: Path, commit: str) -> str:
    return run_git(repo_root, "show", "-s", "--format=%s", commit).stdout.strip()


def git_commit_exists(repo_root: Path, commit: str) -> bool:
    return run_git(repo_root, "cat-file", "-e", f"{commit}^{{commit}}", check=False).returncode == 0


def git_is_ancestor(repo_root: Path, ancestor: str, descendant: str) -> bool:
    return run_git(repo_root, "merge-base", "--is-ancestor", ancestor, descendant, check=False).returncode == 0


def git_file_exists(repo_root: Path, commit: str, path: str) -> bool:
    return run_git(repo_root, "cat-file", "-e", f"{commit}:{normalize_path(path)}", check=False).returncode == 0


def git_changed_paths(repo_root: Path, base: str, head: str | None) -> list[tuple[str, str, str | None]]:
    command = ["diff", "--name-status", "--find-renames", base]
    if head and head != "WORKTREE":
        command.append(head)
    completed = run_git(repo_root, *command)
    entries: list[tuple[str, str, str | None]] = []
    for raw in completed.stdout.splitlines():
        parts = raw.split("\t")
        if not parts:
            continue
        status = parts[0]
        if status.startswith(("R", "C")) and len(parts) >= 3:
            entries.append((status, normalize_path(parts[1]), normalize_path(parts[2])))
        elif len(parts) >= 2:
            entries.append((status, normalize_path(parts[1]), None))
    if not head or head == "WORKTREE":
        untracked = run_git(repo_root, "ls-files", "--others", "--exclude-standard").stdout.splitlines()
        entries.extend(("A?", normalize_path(path), None) for path in untracked if path.strip())
    return entries


def commit_changed_paths(repo_root: Path, commit: str) -> list[str]:
    completed = run_git(repo_root, "diff-tree", "--no-commit-id", "--name-only", "-r", commit)
    return [normalize_path(path) for path in completed.stdout.splitlines() if path.strip()]


def protected_config(mandate: dict[str, Any], repo_id: str) -> dict[str, Any]:
    protected = mandate.get("protected_paths", {})
    by_repository = protected.get("by_repository", {}) if isinstance(protected, dict) else {}
    if isinstance(by_repository, dict) and isinstance(by_repository.get(repo_id), dict):
        return by_repository[repo_id]
    return protected if isinstance(protected, dict) else {}


def protected_match(path: str, mandate: dict[str, Any], repo_id: str = "coordinator") -> bool:
    protected = protected_config(mandate, repo_id)
    exact = {normalize_path(item) for item in protected.get("exact", []) if isinstance(item, str)}
    prefixes = [normalize_path(item) for item in protected.get("prefixes", []) if isinstance(item, str)]
    normalized = normalize_path(path)
    return normalized in exact or any(path_contains(prefix, normalized) for prefix in prefixes)


def allowed_match(path: str, allowed_paths: Iterable[str], implicit: Iterable[str] = ()) -> bool:
    normalized = normalize_path(path)
    candidates = [normalize_path(item) for item in [*allowed_paths, *implicit] if normalize_path(item)]
    return any(path_contains(candidate, normalized) for candidate in candidates)
