# Spec review — T-GOV-ARCHITECTURE-V2-READONLY-CONSUMER

Reviewer role: independent specification review by the Executor; acceptance remains with the Orchestrator.

Verdict: `PASS` for the correction contract.

- `scripts/program_consumer.py` creates a context-managed `TemporaryDirectory`.
- The same explicit `--queue` path is passed to `refresh-queue`, `doctor` and `plan`.
- The behavioral test creates a byte sentinel in the tracked queue, records every engine invocation, verifies the command order and confirms the sentinel is unchanged.
- The consumer remains in the protected inventory; the updated SHA-256 is recorded in `PROGRAM_MANDATE.json`.
- No queue placeholder, staging file or protection weakening was introduced.

Scope note: the pre-existing full Runner suite mismatch is assigned to `T-RUN-CI-REPAIR-001` and is not used as acceptance evidence for this correction.
