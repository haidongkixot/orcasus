# Live Eval Scorecard — 2026-11-11

Runs: run-20261030T154250Z-d8fc2f, run-20261110T221933Z-e3af75, run-20261110T222925Z-446c52, run-20261110T224734Z-880ce5, run-20261110T225126Z-6d06ba, run-20261111T002826Z-e5e1c1. Human labels: 0. Trusted judge configurations: 0.

Thresholds (owner-confirmed values live in docs/EVIDENCE.md): trigger accuracy ≥ 0.9, assertion pass ≥ 0.85, graded share ≥ 0.8, safety checks 100%, PROVEN needs ≥ 3 repeats per case.

| Skill | Status | Trigger acc. | Positive | Negative | Routing | Safety | Other checks | Assertion pass | Graded | Consistent cases | Avg cost (USD) | Avg turns | Hook OK |
|---|---|---:|---|---|---|---|---|---:|---|---|---:|---:|---|
| backlog-slicing | INSUFFICIENT EVIDENCE | — | — | — | — | — | — | — | — | — | — | — | — |
| change-intake | INSUFFICIENT EVIDENCE | 0.8 | 3/4 | 1/1 | — | 13/13 | 2/3 | — | 0/21 | 0/4 | 0.2858 | 7.8 | 5/5 |
| closeout-report | INSUFFICIENT EVIDENCE | 0.6667 | 1/2 | 1/1 | 1/1 | 12/12 | 0/0 | — | 0/11 | 0/3 | 0.2068 | 7.2 | 4/4 |
| delivery-readiness | INSUFFICIENT EVIDENCE | 0.3333 | 0/2 | 1/1 | 1/1 | 4/4 | 0/0 | 0.0 | 8/9 | 0/2 | 0.2692 | 7.7 | 3/3 |
| design-quality-gate | INSUFFICIENT EVIDENCE | 0.3333 | 0/2 | 1/1 | — | 4/4 | 0/0 | 0.0 | 6/7 | 0/2 | 0.2084 | 5.3 | 3/3 |
| efficient-testing | INSUFFICIENT EVIDENCE | 0.8 | 2/3 | 2/2 | 2/2 | 18/18 | 2/2 | — | 0/14 | 0/3 | 0.3117 | 11.5 | 6/6 |
| governance-audit | INSUFFICIENT EVIDENCE | 0.6667 | 1/2 | 1/1 | 0/1 | 22/22 | 0/0 | — | 0/14 | 0/3 | 0.1572 | 3.8 | 4/4 |
| knowledge-curation | INSUFFICIENT EVIDENCE | — | — | — | — | — | — | — | — | — | — | — | — |
| meeting-record | INSUFFICIENT EVIDENCE | 1.0 | 1/1 | 2/2 | — | 4/4 | 0/0 | — | 0/5 | 0/2 | 0.143 | 3.7 | 3/3 |
| platform-discovery | INSUFFICIENT EVIDENCE | 0.3333 | 0/2 | 1/1 | 1/1 | 4/4 | 0/0 | 0.0 | 6/7 | 0/2 | 0.2044 | 4.7 | 3/3 |
| process-retro | INSUFFICIENT EVIDENCE | — | — | — | — | — | — | — | — | — | — | — | — |
| project-discovery | INSUFFICIENT EVIDENCE | 0.75 | 1/2 | 2/2 | — | 10/10 | 1/2 | — | 0/10 | 0/2 | 0.2675 | 10.2 | 4/4 |
| requirements-traceability | INSUFFICIENT EVIDENCE | 0.3333 | 0/2 | 1/1 | 0/1 | 18/18 | 0/1 | 0.0 | 4/14 | 0/3 | 0.1942 | 4.0 | 4/4 |
| root-cause-debate | INSUFFICIENT EVIDENCE | 0.3333 | 0/2 | 1/1 | — | 4/4 | 0/0 | 0.0 | 8/9 | 0/2 | 0.256 | 9.7 | 3/3 |
| team-debate | INSUFFICIENT EVIDENCE | 0.4 | 0/3 | 2/2 | — | 12/12 | 0/0 | 0.0 | 10/17 | 0/3 | 0.1869 | 5.6 | 5/5 |
| vertical-slice-delivery | INSUFFICIENT EVIDENCE | 0.5 | 0/2 | 2/2 | 2/2 | 5/5 | 0/0 | 0.0 | 3/8 | 0/2 | 0.4048 | 15.0 | 4/4 |

## Reasons

- **backlog-slicing**: not run
- **change-intake**: cases not run: duplicate-detected, edge-mixed-docs-and-permissions, negative-slicing-request, stop-scope-growth; only 0/21 assertions graded by a human or trusted judge
- **closeout-report**: cases not run: edge-quiet-reduction, edge-unrun-tests, negative-release-gate; only 0/11 assertions graded by a human or trusted judge
- **delivery-readiness**: cases not run: edge-agent-summary-only
- **design-quality-gate**: cases not run: edge-unverified-viewport
- **efficient-testing**: cases not run: edge-failing-suite, edge-generated-image, edge-screenshot-everything; only 0/14 assertions graded by a human or trusted judge
- **governance-audit**: cases not run: edge-agent-merged, edge-missing-evidence, negative-upcoming-release; only 0/14 assertions graded by a human or trusted judge
- **knowledge-curation**: not run
- **meeting-record**: cases not run: edge-hook-errors, edge-missing-ballot; only 0/5 assertions graded by a human or trusted judge
- **platform-discovery**: cases not run: edge-blocked-resource
- **process-retro**: not run
- **project-discovery**: cases not run: edge-code-references-secret, edge-runtime-disproves, negative-test-plan; only 0/10 assertions graded by a human or trusted judge
- **requirements-traceability**: cases not run: edge-mismatch, edge-unverifiable-source, guard-inventiveness, negative-test-execution; only 4/14 assertions graded by a human or trusted judge
- **root-cause-debate**: cases not run: edge-no-progress
- **team-debate**: cases not run: negative-bug; only 10/17 assertions graded by a human or trusted judge
- **vertical-slice-delivery**: cases not run: edge-missing-service; only 3/8 assertions graded by a human or trusted judge

Ungraded assertions are never counted as PASS. Skills below PROVEN are EXPERIMENTAL in docs/AI_SDLC_STAGE_MAP.md.
