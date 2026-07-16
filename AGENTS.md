# AGENTS.md

## Mission

Maintain the YunoHost GitLab packaging safely and coordinate the related GitLab Runner packaging, upstream mirrors, and GitLab MCP initiative.

## Operating rules

1. Read this file, `continuity/HANDOFF_CURRENT.md`, `continuity/STATUS.md`, and `docs/planning/GITLAB_MCP_AND_AUTOUPDATE_PLAN.md` before changing code.
2. Treat repository files as the source of truth; chat context is not authoritative.
3. Do not update GitLab directly to an arbitrary latest release. Respect GitLab required upgrade stops and supported upgrade paths.
4. Pin download URLs and SHA256 values in released packaging. Dynamic discovery may generate a pull request, but installation must remain reproducible.
5. Keep CE/EE, Debian release, architecture, and upgrade-source matrices explicit.
6. Never commit credentials, runner tokens, personal access tokens, OAuth secrets, or instance backups.
7. Use small, auditable work packages with persisted evidence and handoff updates.
8. Destructive GitLab API operations require explicit authorization, narrow scope, and test namespaces.
9. Every MCP capability must declare authentication scope, pagination behavior, mutability, idempotency, risk class, edition/version availability, and audit fields.
10. Stop only at a genuine human or environmental blocker; record it precisely in the handoff.

## Required validation

For packaging changes, validate the relevant subset of clean install, upgrade, backup, restore, change URL, configuration, removal, and architecture/source integrity. For MCP changes, validate schema contracts, pagination, authorization failures, rate limits, retries, idempotency, and destructive-operation isolation.
