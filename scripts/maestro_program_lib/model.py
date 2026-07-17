from maestro_program_lib.core import *  # noqa: F403


def task_map(backlog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    tasks = backlog.get("tasks")
    if not isinstance(tasks, list):
        raise ContractError("TASK_LIST_REQUIRED")
    result: dict[str, dict[str, Any]] = {}
    for task in tasks:
        if not isinstance(task, dict) or not isinstance(task.get("id"), str):
            raise ContractError("TASK_ID_REQUIRED")
        if task["id"] in result:
            raise ContractError(f"DUPLICATE_TASK_ID:{task['id']}")
        result[task["id"]] = task
    return result


def program_task_map(backlog: dict[str, Any], findings: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result = task_map(backlog)
    for finding in finding_list(findings):
        correction = finding.get("correction_task")
        if correction is None:
            continue
        if not isinstance(correction, dict) or not isinstance(correction.get("id"), str):
            raise ContractError(f"INVALID_DYNAMIC_CORRECTION_TASK:{finding['id']}")
        if correction["id"] in result:
            raise ContractError(f"DUPLICATE_TASK_ID:{correction['id']}")
        result[correction["id"]] = correction
    return result


def work_package_ids(backlog: dict[str, Any]) -> set[str]:
    packages = backlog.get("work_packages")
    if not isinstance(packages, list):
        raise ContractError("WORK_PACKAGE_LIST_REQUIRED")
    result: set[str] = set()
    for package in packages:
        if not isinstance(package, dict) or not isinstance(package.get("id"), str):
            raise ContractError("WORK_PACKAGE_ID_REQUIRED")
        if package["id"] in result:
            raise ContractError(f"DUPLICATE_WORK_PACKAGE:{package['id']}")
        result.add(package["id"])
    return result


def state_overrides(state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    overrides = state.get("task_overrides", {})
    if not isinstance(overrides, dict):
        raise ContractError("TASK_OVERRIDES_OBJECT_REQUIRED")
    return overrides


def finding_list(findings: dict[str, Any]) -> list[dict[str, Any]]:
    values = findings.get("findings")
    if not isinstance(values, list):
        raise ContractError("FINDINGS_LIST_REQUIRED")
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for finding in values:
        if not isinstance(finding, dict) or not isinstance(finding.get("id"), str):
            raise ContractError("FINDING_ID_REQUIRED")
        if finding["id"] in seen:
            raise ContractError(f"DUPLICATE_FINDING_ID:{finding['id']}")
        seen.add(finding["id"])
        result.append(finding)
    return result


def detect_cycle(tasks: dict[str, dict[str, Any]]) -> bool:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(task_id: str) -> bool:
        if task_id in visiting:
            return True
        if task_id in visited:
            return False
        visiting.add(task_id)
        for dependency in tasks[task_id].get("dependencies", []):
            if dependency in tasks and visit(dependency):
                return True
        visiting.remove(task_id)
        visited.add(task_id)
        return False

    return any(visit(task_id) for task_id in tasks)


def program_hashes(mandate: dict[str, Any], backlog: dict[str, Any], state: dict[str, Any], findings: dict[str, Any]) -> dict[str, str]:
    return {
        "mandate": sha256_bytes(canonical_json_bytes(mandate)),
        "backlog": sha256_bytes(canonical_json_bytes(backlog)),
        "state": sha256_bytes(canonical_json_bytes(state)),
        "findings": sha256_bytes(canonical_json_bytes(findings)),
    }


def validate_program(
    files: ProgramFiles,
    mandate: dict[str, Any],
    backlog: dict[str, Any],
    state: dict[str, Any],
    findings: dict[str, Any],
    repo_map: dict[str, Path],
    check_queue: bool = True,
) -> list[str]:
    reasons: list[str] = []
    payloads = [mandate, backlog, state, findings]
    if any(payload.get("schema_version") != SCHEMA_VERSION for payload in payloads):
        reasons.append("SCHEMA_VERSION_MISMATCH")
    program_ids = {payload.get("program_id") for payload in payloads}
    if len(program_ids) != 1 or None in program_ids:
        reasons.append("PROGRAM_ID_MISMATCH")
    try:
        tasks = program_task_map(backlog, findings)
        packages = work_package_ids(backlog)
        overrides = state_overrides(state)
        all_findings = finding_list(findings)
    except ContractError as error:
        return reasons + error.reasons

    required_packages = set(mandate.get("required_work_packages", []))
    if not required_packages.issubset(packages):
        reasons.append("REQUIRED_WORK_PACKAGE_MISSING")
    objectives = backlog.get("objectives", {})
    required_objectives = set(mandate.get("required_objectives", []))
    if not isinstance(objectives, dict) or not required_objectives.issubset(set(objectives)):
        reasons.append("REQUIRED_OBJECTIVE_MISSING")
    if isinstance(objectives, dict):
        for objective in required_objectives:
            mapped = objectives.get(objective)
            if not isinstance(mapped, list) or not mapped or any(item not in packages for item in mapped):
                reasons.append(f"OBJECTIVE_COVERAGE_INVALID:{objective}")

    for task_id, task in tasks.items():
        if task.get("work_package") not in packages:
            reasons.append(f"UNKNOWN_TASK_WORK_PACKAGE:{task_id}")
        dependencies = task.get("dependencies", [])
        if not isinstance(dependencies, list) or any(dep not in tasks for dep in dependencies):
            reasons.append(f"UNKNOWN_DEPENDENCY:{task_id}")
        repositories = task.get("repositories")
        if not isinstance(repositories, list) or not repositories:
            reasons.append(f"TASK_REPOSITORY_REQUIRED:{task_id}")
        elif any(repo_id not in repo_map for repo_id in repositories):
            reasons.append(f"TASK_REPOSITORY_UNMAPPED:{task_id}")
        paths = task.get("paths")
        if not isinstance(paths, list) or not paths:
            reasons.append(f"TASK_PATHS_REQUIRED:{task_id}")
        if "status" in task:
            reasons.append(f"BACKLOG_STATUS_FORBIDDEN:{task_id}")
    if detect_cycle(tasks):
        reasons.append("TASK_DEPENDENCY_CYCLE")

    for task_id, override in overrides.items():
        if task_id not in tasks:
            reasons.append(f"STATE_UNKNOWN_TASK:{task_id}")
            continue
        if not isinstance(override, dict) or override.get("state") not in OVERRIDE_STATES:
            reasons.append(f"INVALID_TASK_OVERRIDE:{task_id}")
            continue
        if override.get("state") == "accepted" and not (override.get("commit") or override.get("commits")):
            reasons.append(f"ACCEPTED_TASK_COMMIT_REQUIRED:{task_id}")
        if override.get("state") == "accepted" and not override.get("review"):
            reasons.append(f"ACCEPTED_TASK_REVIEW_REQUIRED:{task_id}")
    gates = state.get("human_gates", [])
    if not isinstance(gates, list):
        reasons.append("HUMAN_GATES_LIST_REQUIRED")

    for finding in all_findings:
        state_name = finding.get("state")
        if state_name not in {"open", "resolved", "accepted_risk", "superseded"}:
            reasons.append(f"INVALID_FINDING_STATE:{finding['id']}")
        if state_name == "open" and finding.get("actionable", True):
            correction = finding.get("correction_task_id")
            if not isinstance(correction, str) or correction not in tasks:
                reasons.append(f"OPEN_FINDING_WITHOUT_CORRECTION_TASK:{finding['id']}")

    protected_root = mandate.get("protected_paths", {})
    by_repository = protected_root.get("by_repository", {}) if isinstance(protected_root, dict) else {}
    protected_sets = by_repository if isinstance(by_repository, dict) and by_repository else {"coordinator": protected_root}
    for protected_repo_id, protected in protected_sets.items():
        if not isinstance(protected, dict):
            reasons.append(f"PROTECTED_CONFIG_INVALID:{protected_repo_id}")
            continue
        inventory = protected.get("inventory", {})
        if not isinstance(inventory, dict):
            reasons.append(f"PROTECTED_INVENTORY_REQUIRED:{protected_repo_id}")
            continue
        protected_repo_root = repo_map.get(protected_repo_id)
        if protected_repo_root is None:
            reasons.append(f"PROTECTED_REPOSITORY_UNMAPPED:{protected_repo_id}")
            continue
        for path, expected_hash in inventory.items():
            target = protected_repo_root / normalize_path(path)
            if not target.is_file():
                reasons.append(f"PROTECTED_FILE_MISSING:{protected_repo_id}:{path}")
            elif not isinstance(expected_hash, str) or sha256_file(target) != expected_hash:
                reasons.append(f"PROTECTED_FILE_DRIFT:{protected_repo_id}:{path}")
        prefixes = [normalize_path(value) for value in protected.get("prefixes", []) if isinstance(value, str)]
        for prefix in prefixes:
            prefix_root = protected_repo_root / prefix
            if prefix_root.is_dir():
                actual = {
                    normalize_path(str(path.relative_to(protected_repo_root)))
                    for path in prefix_root.rglob("*")
                    if path.is_file() and "__pycache__" not in path.parts
                }
                expected = {normalize_path(path) for path in inventory if path_contains(prefix, path)}
                unexpected = actual - expected
                if unexpected:
                    reasons.append(f"PROTECTED_INVENTORY_UNTRACKED:{protected_repo_id}:{sorted(unexpected)[0]}")

    if check_queue and files.queue.is_file():
        try:
            queue = read_json(files.queue)
            expected_hashes = program_hashes(mandate, backlog, state, findings)
            if queue.get("source_hashes") != expected_hashes:
                reasons.append("DERIVED_QUEUE_STALE")
        except ContractError as error:
            reasons.extend(error.reasons)
    return sorted(set(reasons))
