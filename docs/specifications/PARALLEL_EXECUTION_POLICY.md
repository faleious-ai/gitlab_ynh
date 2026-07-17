# Substantive parallel execution contract

Task paths are normalized and compared by ancestry. Parent and descendant paths conflict.

A lane start record contains the planner lane ID, task ID, baseline, owned paths, worker identity and an isolated workspace. A lane finish record contains at least one nonempty artifact and one nonempty command log inside that workspace, with hashes and sizes. Wave validation confirms task, baseline, path ownership, distinct workers, distinct workspaces and real overlap.

Lane outputs are preparation artifacts. Canonical integration, acceptance, receipt creation and publication remain serial per task and repository.
