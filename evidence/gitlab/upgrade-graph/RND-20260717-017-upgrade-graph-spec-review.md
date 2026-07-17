# Spec review — T-GITLAB-UPGRADE-GRAPH-001

Verdict: PASS, pending independent Orchestrator acceptance.

- The graph is sourced from GitLab's official upgrade-path and version-notes documentation.
- It separates exact historical conditional stops from the scheduled x.2/x.5/x.8/x.11 policy.
- Positive cross-major and same-major paths and a downgrade negative case are recorded.
- The validator rejects duplicate, malformed or out-of-major stops and does not mutate a manifest.
