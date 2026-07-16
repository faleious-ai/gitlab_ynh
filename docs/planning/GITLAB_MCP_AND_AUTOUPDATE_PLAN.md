# GitLab MCP and YunoHost Safe Autoupdate Plan

Status: planning baseline
Date: 2026-07-16

## Confirmed baseline

- `faleious-ai/gitlab_ynh` exists and is administered by the owner account.
- `faleious-ai/gitlab-runner_ynh` exists and is administered by the owner account.
- `gitlab_ynh` currently declares `19.1.0~ynh1` and pins package URLs and SHA256 values across CE/EE, Debian releases, and amd64/arm64.
- `gitlab-runner_ynh` currently declares `18.6.2~ynh1`; its proposed autoupdate block is commented, and the helper-images package lacks an automated update strategy.
- The current GIT Asimov connector exposes only a narrow subset of GitLab API capabilities. This project is intended to expand that surface substantially.

## Program goals

1. Keep both YunoHost packages current through reproducible, reviewed automation.
2. Mirror `gitlab-org/gitlab` and `gitlab-org/gitlab-runner` into GitHub for analysis and continuity.
3. Build a GitLab MCP whose practical coverage approaches the breadth of the GitHub connector while respecting GitLab edition, version, permissions, and safety constraints.
4. Persist architecture, API coverage, decisions, tests, evidence, status, and handoff in repositories.

## Non-negotiable safety constraint

“Always point to the latest version” must mean “automatically discover the newest eligible version and prepare a validated update.” It must not mean downloading an unpinned artifact during installation or skipping GitLab required upgrade stops. Released manifests remain immutable and hash-pinned.

## Work packages

### WP-01 — Packaging inventory

Audit manifests, scripts, helpers, tests, configuration panels, backup/restore behavior, upgrade logic, source matrices, and differences from YunoHost upstream for both repositories.

### WP-02 — GitLab package updater

Build a generator that discovers stable releases, resolves CE/EE packages for supported Debian releases and architectures, calculates hashes, updates the manifest, and opens a reviewable change. Add an upgrade-path resolver that emits every required intermediate stop.

### WP-03 — Runner package updater

Automate release discovery for the runner package and helper images as one atomic version set. Validate amd64, arm64, and armhf assets, hashes, installation, registration, Docker execution, upgrade, and removal.

### WP-04 — Upstream GitLab-to-GitHub mirrors

Create GitHub mirror repositories for the GitLab and Runner upstreams. Synchronize branches and tags using a scheduled runner job or authorized local workflow. Record upstream URL, mirrored commit, timestamp, and sync result. Treat these as mirrors, not native GitHub forks.

### WP-05 — GitLab API coverage catalog

Create a machine-readable inventory covering REST and GraphQL operations across projects, groups, namespaces, users, members, repositories, commits, branches, tags, issues, work items, epics, merge requests, reviews, pipelines, jobs, logs, artifacts, schedules, variables, runners, releases, packages, registries, wikis, snippets, pages, environments, deployments, feature flags, webhooks, integrations, keys, tokens, protected resources, audit events, settings, migrations, imports/exports, and search.

Each operation must record endpoint or GraphQL field, method, minimum scope, pagination, request and response schema, mutability, idempotency, risk class, CE/EE availability, version availability, and proposed MCP tool mapping.

### WP-06 — MCP architecture

Implement a version-aware GitLab REST/GraphQL client, generated operation catalog, high-level workflow tools, a controlled residual API tool, explicit pagination, normalized resource references, risk-based policy gates, narrow instance/project allowlists, secret redaction, trace IDs, and auditable mutations.

### WP-07 — GitHub parity matrix

Compare capabilities rather than tool names: repository discovery, files, trees, blobs, commits, refs, issues/work items, discussions, merge requests/reviews, CI/CD, artifacts, releases, packages, search, identity, administration, batch mutations, and continuity. Classify gaps as implementable, API-limited, edition-limited, security-limited, or deliberately out of scope.

### WP-08 — Assurance harness

Add contract tests against an isolated GitLab instance; schema and pagination golden tests; negative authorization tests; retry, rate-limit, idempotency, and partial-failure tests; and destructive tests restricted to ephemeral namespaces. Compare the exposed MCP catalog against the API surface available in the target GitLab version.

### WP-09 — Continuity structure

The future coordinator repository should contain:

- `AGENTS.md`
- `CONTEXT.md`
- `docs/architecture/ARCHITECTURE.md`
- `docs/api/API_COVERAGE_MATRIX.md`
- `docs/api/GITHUB_PARITY_MATRIX.md`
- `docs/security/THREAT_MODEL.md`
- `docs/security/AUTHORIZATION_POLICY.md`
- `docs/ynh/UPSTREAM_UPDATE_POLICY.md`
- `docs/ynh/UPGRADE_PATH_POLICY.md`
- `continuity/STATUS.md`
- `continuity/HANDOFF_CURRENT.md`
- `continuity/DECISIONS.md`
- `continuity/EXECUTION_PLAN.md`
- `evidence/EVIDENCE_INDEX.md`

## Delivery order

1. Create the coordinator repository, provisionally `faleious-ai/gitlab-mcp`.
2. Create and synchronize both upstream mirrors.
3. Complete both packaging inventories.
4. Implement Runner autoupdate first because its source matrix and upgrade semantics are smaller.
5. Implement GitLab autoupdate with mandatory upgrade-path enforcement.
6. Generate the API catalog and GitHub parity matrix.
7. Deliver the MCP in waves: read-only discovery; collaboration; repository mutations; CI/CD and artifacts; packages and releases; administration.
8. Close each wave only with contract-test evidence and updated handoff.

## Current blockers

- The available GitHub connector in this conversation does not expose repository creation or cross-host fork/mirror creation.
- The Asimov MCP Gateway command path is unavailable in this conversation, so the runner cannot currently execute `git clone --mirror` and `git push --mirror`.
- The current GIT Asimov connector does not expose enough repository and administration operations to bootstrap the full project from GitLab itself.

## Next executable action

From Codex or another session with the Asimov MCP Gateway command runner available:

1. create `faleious-ai/gitlab-mcp`;
2. create GitHub repositories for the two upstream mirrors;
3. run authenticated mirror synchronization;
4. add the continuity structure above;
5. inventory both YunoHost repositories and persist findings before code changes.
