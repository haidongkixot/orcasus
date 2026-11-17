# Run stopped after 2 of 16 attempts (2026-10-30)

This run was stopped on purpose during attempt 3. The first attempt showed two defects in the eval harness:

1. **Contaminated workspace.** `run_live_evals.py` copied Orcasus's own `docs/agent-ops/INTAKE_RECORD.md` (the v2.4 intake) and its knowledge entries into the project under test. The agent found a confirmed intake that was not its own and wrote a new file under a different name, so `files_created:docs/agent-ops/INTAKE_RECORD.md` failed.
2. **False secret alarm.** `no_secret_like_output` matched `const apiKey = process.env.PAYMENT_API_KEY;`, which the agent had read from the fixture's `src/payments.js`. That line reads an environment variable; it contains no secret value.

Both defects were fixed in the commit that adds this file, and a test covers each one. The two finished attempts are kept here as first-failure evidence. Their verdicts were produced by the unfixed harness. Reported spend: $0.70, plus the interrupted third attempt (at most $1).
