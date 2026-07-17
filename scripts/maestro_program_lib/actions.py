from maestro_program_lib.core import *  # noqa: F403
from maestro_program_lib.model import *  # noqa: F403
from maestro_program_lib.receipts import *  # noqa: F403
from maestro_program_lib.plan import *  # noqa: F403


def prepare_receipt(
    files: ProgramFiles,
    mandate: dict[str, Any],
    backlog: dict[str, Any],
    findings: dict[str, Any],
    task_id: str,
    repo_id: str,
    repo_root: Path,
    acceptance_command: str,
    evidence_paths: list[str],
    gates: list[str],
) -> dict[str, Any]:
    tasks = program_task_map(backlog, findings)
    if task_id not in tasks:
        raise ContractError("UNKNOWN_TASK")
    task = tasks[task_id]
    if repo_id not in task.get("repositories", []):
        raise ContractError("TASK_REPOSITORY_MISMATCH")
    if not git_available(repo_root):
        raise ContractError("REPOSITORY_NOT_GIT")
    baseline = git_ref(repo_root, "HEAD")
    change_result = validate_change(mandate, repo_root, baseline, "WORKTREE", repo_id)
    if not change_result["valid"]:
        raise ContractError(*change_result["reasons"])
    implicit = [receipt_path(task_id)]
    for changed in change_result["changed_paths"]:
        if not allowed_match(changed, task.get("paths", []), implicit):
            raise ContractError(f"TASK_PATH_OUTSIDE_OWNERSHIP:{changed}")
    for evidence_path in evidence_paths:
        if not (repo_root / normalize_path(evidence_path)).is_file():
            raise ContractError(f"TASK_EVIDENCE_MISSING:{evidence_path}")
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "program_id": mandate.get("program_id"),
        "task_id": task_id,
        "repository": repo_id,
        "commit_binding": "SELF",
        "prepared_at": utc_now(),
        "acceptance": {"command": acceptance_command, "result": "pass"},
        "gates": [{"name": gate, "result": "pass"} for gate in gates],
        "evidence_paths": sorted(normalize_path(path) for path in evidence_paths),
        "changed_paths": change_result["changed_paths"],
    }
    target = repo_root / receipt_path(task_id)
    atomic_write_json(target, receipt)
    return receipt


def register_finding(
    backlog: dict[str, Any],
    state: dict[str, Any],
    findings: dict[str, Any],
    payload: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    finding_id = payload.get("id")
    task_payload = payload.get("correction_task")
    if not isinstance(finding_id, str) or not isinstance(task_payload, dict) or not isinstance(task_payload.get("id"), str):
        raise ContractError("FINDING_AND_CORRECTION_TASK_REQUIRED")
    if payload.get("material_human_consequence") is True:
        raise ContractError("HUMAN_CONSEQUENCE_REQUIRES_ORCHESTRATOR")
    if not task_payload.get("reversible", True):
        raise ContractError("CORRECTION_TASK_MUST_BE_REVERSIBLE")
    existing_findings = finding_list(findings)
    if any(item["id"] == finding_id for item in existing_findings):
        raise ContractError("DUPLICATE_FINDING_ID")
    tasks = program_task_map(backlog, findings)
    if task_payload["id"] in tasks:
        raise ContractError("DUPLICATE_TASK_ID")
    finding = {
        "id": finding_id,
        "severity": payload.get("severity", "P2"),
        "state": "open",
        "actionable": True,
        "summary": payload.get("summary", "technical finding"),
        "source_task_id": payload.get("source_task_id"),
        "correction_task_id": task_payload["id"],
        "correction_task": task_payload,
        "evidence": payload.get("evidence", []),
        "registered_at": utc_now(),
    }
    backlog = json.loads(json.dumps(backlog))
    findings = json.loads(json.dumps(findings))
    state = json.loads(json.dumps(state))
    findings["findings"].append(finding)
    state.setdefault("history", []).append(
        {"event": "finding_registered", "finding_id": finding_id, "task_id": task_payload["id"], "observed_at": utc_now()}
    )
    return backlog, state, findings
