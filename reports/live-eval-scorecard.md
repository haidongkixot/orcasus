# Live Eval Scorecard — 2026-11-10

Runs: run-20261030T154250Z-d8fc2f, run-20261110T221933Z-e3af75, run-20261110T222925Z-446c52, run-20261110T224734Z-880ce5, run-20261110T225126Z-6d06ba. Human labels: 0. Trusted judge configurations: 0.

Thresholds (owner-confirmed values live in docs/EVIDENCE.md): trigger accuracy ≥ 0.9, assertion pass ≥ 0.85, graded share ≥ 0.8, safety checks 100%, PROVEN needs ≥ 3 repeats per case.

| Skill | Status | Trigger acc. | Positive | Negative | Routing | Safety | Other checks | Assertion pass | Graded | Consistent cases | Avg cost (USD) | Avg turns | Hook OK |
|---|---|---:|---|---|---|---|---|---:|---|---|---:|---:|---|
| backlog-slicing | INSUFFICIENT EVIDENCE | — | — | — | — | — | — | — | — | — | — | — | — |
| change-intake | INSUFFICIENT EVIDENCE | 0.75 | 2/3 | 1/1 | — | 11/11 | 1/2 | — | 0/16 | 0/4 | 0.2337 | 7.5 | 4/4 |
| closeout-report | INSUFFICIENT EVIDENCE | 0.6667 | 1/2 | 1/1 | 1/1 | 7/7 | 0/0 | — | 0/8 | 0/3 | 0.2279 | 9.0 | 3/3 |
| delivery-readiness | INSUFFICIENT EVIDENCE | 0.5 | 0/1 | 1/1 | 1/1 | 2/2 | 0/0 | 0.0 | 4/5 | 0/2 | 0.2971 | 6.5 | 2/2 |
| design-quality-gate | INSUFFICIENT EVIDENCE | 0.5 | 0/1 | 1/1 | — | 2/2 | 0/0 | 0.0 | 3/4 | 0/2 | 0.1821 | 5.5 | 2/2 |
| efficient-testing | INSUFFICIENT EVIDENCE | 0.8 | 2/3 | 2/2 | 2/2 | 14/14 | 2/2 | — | 0/11 | 0/3 | 0.3325 | 12.4 | 5/5 |
| governance-audit | INSUFFICIENT EVIDENCE | 0.6667 | 1/2 | 1/1 | 0/1 | 15/15 | 0/0 | — | 0/10 | 0/3 | 0.1598 | 4.0 | 3/3 |
| knowledge-curation | INSUFFICIENT EVIDENCE | — | — | — | — | — | — | — | — | — | — | — | — |
| meeting-record | INSUFFICIENT EVIDENCE | 1.0 | 1/1 | 1/1 | — | 2/2 | 0/0 | — | 0/4 | 0/2 | 0.1522 | 4.5 | 2/2 |
| platform-discovery | INSUFFICIENT EVIDENCE | 0.5 | 0/1 | 1/1 | 1/1 | 2/2 | 0/0 | 0.0 | 3/4 | 0/2 | 0.2169 | 5.5 | 2/2 |
| process-retro | INSUFFICIENT EVIDENCE | — | — | — | — | — | — | — | — | — | — | — | — |
| project-discovery | INSUFFICIENT EVIDENCE | 0.75 | 1/2 | 2/2 | — | 10/10 | 1/2 | — | 0/10 | 0/2 | 0.2675 | 10.2 | 4/4 |
| requirements-traceability | INSUFFICIENT EVIDENCE | 0.3333 | 0/2 | 1/1 | 0/1 | 12/12 | 0/1 | 0.0 | 4/10 | 0/3 | 0.161 | 3.0 | 3/3 |
| root-cause-debate | INSUFFICIENT EVIDENCE | 0.5 | 0/1 | 1/1 | — | 2/2 | 0/0 | 0.0 | 4/5 | 0/2 | 0.2565 | 9.0 | 2/2 |
| team-debate | INSUFFICIENT EVIDENCE | 0.4 | 0/3 | 2/2 | — | 12/12 | 0/0 | 0.0 | 10/17 | 0/3 | 0.1869 | 5.6 | 5/5 |
| vertical-slice-delivery | INSUFFICIENT EVIDENCE | 0.5 | 0/2 | 2/2 | 2/2 | 5/5 | 0/0 | 0.0 | 3/8 | 0/2 | 0.4048 | 15.0 | 4/4 |

## Reasons

- **backlog-slicing**: not run
- **change-intake**: cases not run: duplicate-detected, edge-mixed-docs-and-permissions, negative-slicing-request, stop-scope-growth; only 0/16 assertions graded by a human or trusted judge
- **closeout-report**: cases not run: edge-quiet-reduction, edge-unrun-tests, negative-release-gate; only 0/8 assertions graded by a human or trusted judge
- **delivery-readiness**: cases not run: edge-agent-summary-only
- **design-quality-gate**: cases not run: edge-unverified-viewport; only 3/4 assertions graded by a human or trusted judge
- **efficient-testing**: cases not run: edge-failing-suite, edge-generated-image, edge-screenshot-everything; only 0/11 assertions graded by a human or trusted judge
- **governance-audit**: cases not run: edge-agent-merged, edge-missing-evidence, negative-upcoming-release; only 0/10 assertions graded by a human or trusted judge
- **knowledge-curation**: not run
- **meeting-record**: cases not run: edge-hook-errors, edge-missing-ballot; only 0/4 assertions graded by a human or trusted judge
- **platform-discovery**: cases not run: edge-blocked-resource; only 3/4 assertions graded by a human or trusted judge
- **process-retro**: not run
- **project-discovery**: cases not run: edge-code-references-secret, edge-runtime-disproves, negative-test-plan; only 0/10 assertions graded by a human or trusted judge
- **requirements-traceability**: cases not run: edge-mismatch, edge-unverifiable-source, guard-inventiveness, negative-test-execution; only 4/10 assertions graded by a human or trusted judge
- **root-cause-debate**: cases not run: edge-no-progress
- **team-debate**: cases not run: negative-bug; only 10/17 assertions graded by a human or trusted judge
- **vertical-slice-delivery**: cases not run: edge-missing-service; only 3/8 assertions graded by a human or trusted judge

Ungraded assertions are never counted as PASS. Skills below PROVEN are EXPERIMENTAL in docs/AI_SDLC_STAGE_MAP.md.
