# Assurance report — RND-20260717-015

Task: `T-ASSURANCE-01-maintenance`

Scope: repeat the proportional gates after the published implementation and record limitations without changing protected oracles.

## Acceptance results

| Pack | Result | Claim |
|---|---|---|
| Autonomous program | `tests.acceptance.test_autonomous_program_execution`: 7/7 passed | `LOCAL_VERIFIED` |
| GitLab updater | `tests.acceptance.test_gitlab_autoupdate_objective`: 3/3 passed | `LOCAL_VERIFIED` |
| GitLab MCP fixture | `GITLAB_MCP_ROOT=evidence/mcp/gitlab-mcp`; foundation acceptance: 5/5 passed | `LOCAL_VERIFIED` |
| Runner Docker default | `tests.acceptance.test_supported_docker_default`: 2/2 passed | `LOCAL_VERIFIED` |

The protected packs therefore produced 17/17 passing tests in this assurance run. No protected specification or acceptance test was modified.

## Required gates

- Updater dry-run generated a fixed `19.2.4` candidate, reported `promoted=false`, and left the input manifest unchanged.
- Runner `manifest.toml` remained at `18.6.2~ynh1`.
- Bash syntax validation with the installed Git Bash executable passed for `_common.sh`, `config`, `backup`, `restore`, `install`, `upgrade` and `remove`.
- JSON/TOML parsing passed for 5/3 files in the coordinator and 11/3 files in the Runner, excluding generated cache directories.
- Runner `scripts/secret_scan.py` reported `secret scan: clean`; the coordinator acceptance pack's current-tree secret test also passed.

## Limitations

The Runner full local suite reported 34/38 passing, 3 failures and 1 error under the Windows execution environment. The failures are the Bash controller path and POSIX file-mode lifecycle harnesses; the error is the missing-GPG negative test's network key fetch timing out during the local TLS handshake. These are classified `ENVIRONMENTAL_LIMIT`, not converted into product success. The focused Runner acceptance remains GREEN.

The published Runner SHA `b3f752f4c5b8ace5a224263454eb9fc6220b71a1` has a remote GitHub Actions run `29582869706`; job `87892565898` completed with `failure` at `Run unit and negative tests`. Detailed logs were not available to this executor, so remote success remains `UNVERIFIED` and the observation remains `FAILED` for CI.

The final-continuity test still expects the round to be closed; it is intentionally deferred to `T-GOV-03-final-continuity` after this assurance record is published.
