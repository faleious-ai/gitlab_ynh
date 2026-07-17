# GitLab MCP foundation package

This package is the publication-ready test-mode foundation for `faleious-ai/gitlab-mcp` while a separate remote repository cannot be created by the current executor environment.

The server is fixture-only when exercised by the acceptance pack. It uses newline-delimited JSON-RPC 2.0 on stdio, exposes capability and paginated project-read tools, and rejects destructive project deletion before any transport with `CONFIRMATION_REQUIRED`.

Validation command from the coordinator repository:

```text
$env:GITLAB_MCP_ROOT = (Resolve-Path evidence/mcp/gitlab-mcp).Path
PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.acceptance.test_gitlab_mcp_foundation -v
```

This package does not contain credentials, network clients, release metadata or destructive operations.
