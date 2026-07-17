# Learning ledger

## BP-RND-20260717-015-001

- Round-ID: `RND-20260717-015`
- Task-ID: `T-GOV-01-program-engine`
- Classification: `IMPLEMENTATION_BUG`
- Pattern: CLI error propagation
- Symptom: `validate-gate` emitted `valid=false` for an invalid gate but exited with status 0, so the public acceptance seam could not distinguish rejection from success.
- Root cause: the command dispatcher used a constant success exit code for the gate result instead of mapping the result validity to the process status.
- Contract amendment: none; the public contract already requires nonzero exit for contract rejection.
- RED: `PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.acceptance.test_autonomous_program_execution -v` — 6 passed, 1 failed on expected return code 2.
- GREEN: same command after the dispatcher fix — all 7 tests passed.
- Affected path: `scripts/maestro_program.py`.
- Broader systemic amendment: not indicated; all four JSON CLI subcommands now map invalid results to nonzero status.
