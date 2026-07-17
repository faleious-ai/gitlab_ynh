from maestro_program_lib.core import *  # noqa: F403
from maestro_program_lib.model import *  # noqa: F403


def receipt_path(task_id: str) -> str:
    return f"continuity/task_receipts/{task_id}.json"


def find_receipt_commit(repo_root: Path, task_id: str) -> str | None:
    path = receipt_path(task_id)
    completed = run_git(repo_root, "log", "--format=%H", "--diff-filter=A", "--", path, check=False)
    commits = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
    return commits[0] if commits else None


def verify_receipt(task: dict[str, Any], repo_id: str, repo_root: Path, remote_ref: str) -> tuple[bool, list[str], str | None]:
    reasons: list[str] = []
    if not git_available(repo_root):
        return False, [f"REPOSITORY_NOT_GIT:{repo_id}"], None
    commit = find_receipt_commit(repo_root, task["id"])
    if not commit:
        return False, [f"TASK_RECEIPT_MISSING:{repo_id}"], None
    if not git_commit_exists(repo_root, commit):
        return False, [f"TASK_RECEIPT_COMMIT_MISSING:{repo_id}"], commit
    remote = run_git(repo_root, "rev-parse", remote_ref, check=False)
    if remote.returncode != 0:
        return False, [f"REMOTE_REF_UNAVAILABLE:{repo_id}"], commit
    remote_commit = remote.stdout.strip()
    if not git_is_ancestor(repo_root, commit, remote_commit):
        reasons.append(f"TASK_COMMIT_NOT_REMOTE:{repo_id}")
    if task["id"] not in git_subject(repo_root, commit):
        reasons.append(f"TASK_ID_NOT_IN_COMMIT_SUBJECT:{repo_id}")
    raw = run_git(repo_root, "show", f"{commit}:{receipt_path(task['id'])}", check=False)
    if raw.returncode != 0:
        reasons.append(f"TASK_RECEIPT_NOT_IN_COMMIT:{repo_id}")
        return False, reasons, commit
    try:
        receipt = json.loads(raw.stdout)
    except json.JSONDecodeError:
        reasons.append(f"TASK_RECEIPT_INVALID_JSON:{repo_id}")
        return False, reasons, commit
    if receipt.get("task_id") != task["id"] or receipt.get("commit_binding") != "SELF":
        reasons.append(f"TASK_RECEIPT_IDENTITY_INVALID:{repo_id}")
    acceptance = receipt.get("acceptance", {})
    if not isinstance(acceptance, dict) or acceptance.get("result") != "pass":
        reasons.append(f"TASK_ACCEPTANCE_NOT_PASS:{repo_id}")
    gates = receipt.get("gates", [])
    if not isinstance(gates, list) or any(not isinstance(gate, dict) or gate.get("result") != "pass" for gate in gates):
        reasons.append(f"TASK_GATE_NOT_PASS:{repo_id}")
    evidence_paths = receipt.get("evidence_paths", [])
    if not isinstance(evidence_paths, list) or not evidence_paths:
        reasons.append(f"TASK_EVIDENCE_REQUIRED:{repo_id}")
    else:
        for path in evidence_paths:
            if not isinstance(path, str) or not git_file_exists(repo_root, commit, path):
                reasons.append(f"TASK_EVIDENCE_NOT_IN_COMMIT:{repo_id}:{path}")
    allowed = task.get("paths", [])
    implicit = [receipt_path(task["id"])]
    for changed in commit_changed_paths(repo_root, commit):
        if not allowed_match(changed, allowed, implicit):
            reasons.append(f"TASK_PATH_OUTSIDE_OWNERSHIP:{repo_id}:{changed}")
    if receipt.get("repository") != repo_id:
        reasons.append(f"TASK_RECEIPT_REPOSITORY_MISMATCH:{repo_id}")
    return not reasons, reasons, commit


def effective_task_states(
    mandate: dict[str, Any],
    backlog: dict[str, Any],
    state: dict[str, Any],
    findings: dict[str, Any],
    repo_map: dict[str, Path],
) -> tuple[dict[str, str], dict[str, list[str]], dict[str, dict[str, str]]]:
    tasks = program_task_map(backlog, findings)
    overrides = state_overrides(state)
    effective: dict[str, str] = {}
    receipt_errors: dict[str, list[str]] = {}
    receipt_commits: dict[str, dict[str, str]] = {}
    remote_refs = {
        repo.get("id"): repo.get("remote_ref", "origin/master")
        for repo in mandate.get("repositories", [])
        if isinstance(repo, dict)
    }
    for task_id, task in tasks.items():
        override = overrides.get(task_id, {})
        override_state = override.get("state") if isinstance(override, dict) else None
        if override_state in {"accepted", "blocked_human", "blocked_environment", "correction_required", "failed", "superseded"}:
            effective[task_id] = override_state
            continue
        errors: list[str] = []
        commits: dict[str, str] = {}
        verified = True
        for repo_id in task.get("repositories", []):
            root = repo_map.get(repo_id)
            if root is None:
                verified = False
                errors.append(f"TASK_REPOSITORY_UNMAPPED:{repo_id}")
                continue
            valid, repo_errors, commit = verify_receipt(task, repo_id, root, str(remote_refs.get(repo_id, "origin/master")))
            verified = verified and valid
            errors.extend(repo_errors)
            if commit:
                commits[repo_id] = commit
        if verified and task.get("repositories"):
            effective[task_id] = "task_remote_verified"
            receipt_commits[task_id] = commits
        elif override_state in {"ready", "in_progress"}:
            effective[task_id] = override_state
            receipt_errors[task_id] = errors
        else:
            effective[task_id] = "planned"
            if errors:
                receipt_errors[task_id] = errors
    return effective, receipt_errors, receipt_commits


def dependency_satisfied(task: dict[str, Any], effective: dict[str, str]) -> bool:
    return all(effective.get(dep) in DEPENDENCY_SUCCESS_STATES for dep in task.get("dependencies", []))


def valid_human_gate(task_id: str, state: dict[str, Any], mandate: dict[str, Any]) -> bool:
    allowed = set(mandate.get("human_gate_classes", []))
    required_fields = {
        "reason_class",
        "condition",
        "evidence",
        "fallbacks_attempted",
        "requested_human_action",
        "safe_state",
        "resume",
    }
    for gate in state.get("human_gates", []):
        if not isinstance(gate, dict) or gate.get("task_id") != task_id or gate.get("state") != "open":
            continue
        if gate.get("reason_class") not in allowed:
            return False
        if gate.get("external_authority") is not True:
            return False
        if any(not gate.get(field) for field in required_fields):
            return False
        return True
    return False


def environment_block_exhausted(task_id: str, state: dict[str, Any]) -> bool:
    for block in state.get("environment_blocks", []):
        if not isinstance(block, dict) or block.get("task_id") != task_id or block.get("state") != "open":
            continue
        required = ("condition", "evidence", "fallbacks_attempted", "safe_state", "resume")
        return all(block.get(field) for field in required)
    return False
