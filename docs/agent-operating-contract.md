# Agent Operating Contract: Mandatory Discovery and Efficient Testing

Copy and adapt this contract into the target project's root CLAUDE.md. Installing skills alone does not guarantee that every agent invokes them; the orchestrator must enforce the gates in each task plan and delegation prompt.

Use these project artifacts:
- docs/agent-ops/READINESS_MATRIX.md
- docs/agent-ops/DISCOVERY_SUMMARY.md
- docs/agent-ops/TEST_PLAN.md
- docs/agent-ops/adr/ for significant architecture decisions

## Required workflow

For every non-trivial feature, redesign, integration, migration or production-relevant bug fix:

1. **Discovery before design.** Invoke /project-discovery. The orchestrator may delegate parallel read-only investigation, but must not assign implementation until discovery evidence is consolidated.
2. **Readiness evidence.** Create/update docs/agent-ops/READINESS_MATRIX.md and docs/agent-ops/DISCOVERY_SUMMARY.md. AVAILABLE requires evidence; UNKNOWN is not AVAILABLE.
3. **Owner decision gate.** For missing essential resources/permissions/assets, unresolved product decisions or material quality/cost/security trade-offs, stop dependent work. Present feasible options, consequences and a recommendation. Do not silently replace the intended solution with a workaround.
4. **Architecture and scope.** Compare feasible options and record significant choices/rejected alternatives in an ADR. Define acceptance criteria, ownership, dependencies and resource constraints.
5. **Test plan before implementation.** Invoke /efficient-testing and write docs/agent-ops/TEST_PLAN.md before adding tests or starting browser/device/visual work.
6. **Zero-capture default.** Screenshot, trace and video budgets are all zero unless a named visual/diagnostic question, bounded artifact count, output path, retention policy and owner approval or pre-approved project policy exist. Never use AI-generated imagery as test evidence.
7. **Use the lowest-cost reliable test.** Prefer static, unit, API/integration and component tests before a small risk-based E2E suite. Do not run full E2E/visual regression after every edit without a reason.
8. **Diagnose before retrying.** Preserve first failure evidence, diagnose root cause, then run targeted retries. Do not loop blindly, skip tests, soften assertions or update snapshots merely to get green.
9. **Re-open discovery on runtime surprises.** If access, assets, integration or environment differs from the readiness record, stop dependent work, update the record and ask the owner when a workaround changes quality or requirements.
10. **Truthful report.** Record actual commands/results, exit codes, durations where available, artifact counts, coverage gaps and unverified areas. Use PASS, FAIL, BLOCKED, NOT RUN and SKIPPED distinctly.

## Role-specific expectations

- Orchestrator: owns discovery gate, test plan and approval of scope/budget; embeds them in prompts to teammates.
- Architect/Designer: cannot finalize an option based on unverified assets, integrations, permissions or platform assumptions.
- Developer: cannot substitute mocks, placeholders, local-only implementations or degraded behavior for a required production capability without approval.
- QA: selects the lowest-cost reliable test, justifies higher-cost layers and respects artifact budget.
- Reviewer: checks readiness evidence, test assertions, execution logs, artifact counts and coverage gaps—not just code style.
- Team Secretary: records blockers, owner decisions, accepted risks, approved deviations and test/artifact budgets.

## Stop conditions

Pause only the affected work and request owner input if a required credential/scope, licensed asset, third-party account, runtime/device, paid service or product decision is unavailable; if requirements conflict; if a workaround changes product behavior/data fidelity/security/supported platforms; or if requested screenshot/trace/video capture has no approved question and budget.

Continue unrelated safe and reversible work that does not depend on the blocker. Do not expose secret values or perform unauthorized deployments, destructive migrations or financial commitments.
