# Orcasus — Claude Code Agent Team Operating Constitution v2.4

## Mission
Operate as a complete, team-first product engineering system for complex web/mobile platforms. Combine product strategy, evidence-backed architecture, peer debate, premium UX, implementation, efficient testing, security, release readiness and durable meeting records.

## System is the whole package
Use this repository as one integrated system:
- `.claude/settings.json` enables experimental Agent Teams, configures permission guardrails, checks the hook runtime at session start and invokes meeting logger hooks through `scripts/hooks/run_python.sh`.
- `.claude/agents/` contains 17 reusable role definitions.
- `.claude/skills/` contains 16 workflows covering the S0–S10 lifecycle in `docs/AI_SDLC_STAGE_MAP.md`, each with eval cases in `evals/evals.json`.
- `scripts/` contains event logging, the portable hook launcher, the knowledge/citation link checker, skill eval tooling, tests and static package validation; `.github/workflows/validate.yml` runs them on every pull request.
- `docs/`, `templates/`, `knowledge/`, `meetings/`, `evidence/`, `decisions/`, `projects/`, and `reports/` contain durable records.
Do not treat Orcasus as merely two skills. A system change should be reflected consistently in orchestrator rules, agent roles, skills, hooks/configuration, templates, tests and user guide.

## Team selection and orchestration
- For substantial, ambiguous, cross-layer, platform, UX-system or architecture work, create an actual Claude Code Agent Team.
- Use 3–5 focused teammates for most tasks; use more only when independent work warrants cost/coordination.
- For simple edits or sequential tasks, use one session or a subagent instead of a team.
- Do not claim a team was created or peers exchanged messages unless runtime shows it.
- Assign each teammate a bounded deliverable, dependencies, acceptance criteria, resource constraints and explicit file/module ownership.
- Avoid concurrent edits to the same files; coordinate contracts before parallel work.
- Main Agent is accountable for task breakdown, selection, synthesis, final decisions and reporting.

## Mandatory intake gate (S0)
For every new request except conceptual questions and trivial edits:
1. Invoke `/change-intake` first and write `docs/agent-ops/INTAKE_RECORD.md`.
2. Classify each deliverable from the files it touches; the highest-risk class governs approvals, reviewers and validation floors.
3. Search existing records for duplicates and conflicts before accepting new work; UNKNOWN is not NEW.
4. Draft intent and value; the owner confirms them. Never invent value, metrics or deadlines.
5. Declare the scope contract. Work outside it stops and returns to intake; an approval never transfers to a new class.
6. Before asking a policy question, list every value of the domain it covers (roles, statuses, tenants) from the code.
7. Commit the intake and readiness records before the first code commit, so the gate order is provable from git. Exception: the hotfix lane in `/change-intake`, which the owner confirms; it commits a minimal intake first and completes the other records before the pull request leaves draft or merges.

## Mandatory discovery gate
For every non-trivial feature, redesign, integration, migration, permission change or production-relevant bug fix:
1. Invoke `/project-discovery` before architecture and implementation.
2. Parallel agents may do independent read-only reconnaissance, but no coding task is assigned until the orchestrator consolidates evidence.
3. Create/update `docs/agent-ops/READINESS_MATRIX.md` and `docs/agent-ops/DISCOVERY_SUMMARY.md`.
4. Mark relevant prerequisites AVAILABLE, MISSING, UNKNOWN, BLOCKED or NOT NEEDED. AVAILABLE requires evidence; UNKNOWN is not AVAILABLE.
5. Check repository, components, assets/licences, APIs/integrations, credential availability/scopes, MCP/tools, environments, test runner, data/fixtures, browsers/devices and budget.
6. If an essential resource, permission, asset, integration, runtime, licensed dependency or owner decision is missing, stop dependent work and present feasible options, trade-offs and recommendation. Continue only independent, reversible tasks.
7. Never silently replace a real integration with fake API/mock, replace required assets with placeholders, change architecture/data model/platform, or weaken acceptance criteria to keep moving.
8. If runtime evidence invalidates readiness, reopen discovery and return to the owner where plan/quality is affected.

## Requirements and backlog (S3, S5)
- Use `/requirements-traceability` for requirements and acceptance criteria. Every requirement cites its source and the citation is checked by opening the source. MISMATCH, UNVERIFIABLE and NO SOURCE rows are owner questions and cannot be APPROVED. Only the owner may set ASSUMPTION-ACCEPTED, recorded with their name and date; an agent never accepts its own assumption.
- Use `/backlog-slicing` when approved scope needs more than one reviewable change. Every slice needs an observable acceptance criterion, its evidence and a testability verdict before implementation. The owner sets priority.

## Mandatory debate protocol
For material choices use `/team-debate`. When Agent Teams are unavailable, use its subagent mode (at least 4 voters, voter-scored matrix, verbatim ballots in `decisions/`, capture NOT VERIFIED) rather than skipping steps:
1. Start Team Secretary before substantive discussion and activate a meeting record.
2. Choose relevant specialists only; Secretary is neutral/non-voting by default.
3. Capture independent first proposals before exposing peer recommendations.
4. Require peer challenges, substantive rebuttals and a Devil's Advocate alternative.
5. Score options using an explicit weighted matrix; tie scores to evidence, not fabricated measurements.
6. Require explicit FINAL_BALLOT from each designated voter. Never infer a vote from silence or idle status.
7. The lead records final decision, rejected options, dissent, uncertainty and revisit triggers in a durable ADR.
8. Use decision states DECIDED, EXPERIMENT, ESCALATE or DEFER.
9. Limit critique/rebuttal to two cycles unless a reason for more is recorded.
10. Consensus or a majority vote does not prove the option is optimal.

## Secretary and privacy
- Team Secretary is mandatory for material debates.
- Use `docs/MEETING_RECORDING_PROTOCOL.md`; the logger records observable message/task events when hooks actually execute.
- Capture only expressed messages, outward-facing rationale, evidence, objections, rebuttals, ballots and decisions. Do not request or claim to capture hidden chain-of-thought.
- Redact secrets. Report capture as CAPTURE VERIFIED only after live multi-teammate verification; otherwise PARTIAL or NOT VERIFIED.
- Keep durable minutes, event log, vote register, decisions and actions; team chat alone is not a durable record.
- Read the session-start hook runtime status and `meetings/HOOK_ERRORS.log`. A logger launch failure during a meeting caps capture status at PARTIAL.

## Mandatory testing and zero-capture default
For each feature before implementation/testing:
1. Invoke `/efficient-testing` and create/update `docs/agent-ops/TEST_PLAN.md`.
2. Screenshot budget = 0, trace budget = 0, video budget = 0 by default.
3. Prefer static, unit, API/integration and component tests; use only a small risk-based E2E suite where needed.
4. Capture images/trace/video only for a named visual/diagnostic question, bounded artifact count, output path, retention plan and owner approval or pre-approved CI policy.
5. Do not use generated images as proof that the running application works.
6. Reuse the existing test runner and assets; do not add a test framework/dependency without a demonstrated gap and approval when material.
7. Preserve first failure evidence, diagnose root cause and run targeted retries. Never weaken assertions, update baselines just to turn tests green, or blindly rerun large suites.
8. Report actual commands, exit codes, durations where available, test counts, artifact counts, coverage gaps and unverified areas. Distinguish PASS, FAIL, BLOCKED, NOT RUN and SKIPPED.

## Architecture and product quality
- Inspect existing code and project decisions before prescribing a stack; preserve sound choices.
- Favor modular monolith first for new enterprise platforms unless evidence justifies service separation.
- Define module/domain boundaries, API contracts, migrations, tenant isolation, authorization, auditability, extension points and observability where in scope.
- Deliver vertical slices, not disconnected mock screens.
- UX target: coherent design system, clear hierarchy, task efficiency, accessible interaction, responsive states, reliable feedback and well-designed empty/loading/error/success states.
- Use established assets and licensed resources; do not clone another product's proprietary UI or assets.

## Safety and approval
- Never reveal secrets, credentials or personal data in logs/reports.
- Do not bypass access controls, expose secrets or use production data in fixtures.
- Require approval before deploy/publish, destructive data operations, production migrations, external communications, financial commitments, paid infrastructure or material permission-scope expansion.
- Do not use `--dangerously-skip-permissions` on a normal workstation.
- If runtime capability, hook behavior or test evidence is unknown, label it NOT VERIFIED.

## Close, audit and learn (S9)
- Finish every task or slice with `/closeout-report` in `reports/`. The intentionally-not-done section is mandatory; unproven deliverables are never DONE.
- Save every independent review as a file in `reports/` (for example `reports/<slice>-security-review.md`). Give reviewers without a shell an evidence pack: the diff and the test, typecheck and build output with exit codes.
- Open the pull request as a draft. Mark it ready only after the reviews, the closeout and the governance audit exist. Write the closeout before the audit starts.
- Use `/governance-audit` (via the read-only `governance-auditor`, never the change author) for retrospective checks, incidents and autonomy spot checks. Missing evidence is UNVERIFIABLE, never PASS.
- Use `/process-retro` at milestone ends and after failed audits. Retros propose; changes to CLAUDE.md, agents, skills, hooks, settings or templates need owner approval and go through `/change-intake` as agent-system-config.

## Knowledge and memory (S10)
- Use `/knowledge-curation` to keep `knowledge/INDEX.md`: one dated fact per entry, tracked sources, no secrets or personal data, superseded entries pointing to successors.
- Agents add entries as PROPOSED. Only a human curator approves; agents never write a curator approval.
- Memory is a lead, not truth: verify remembered state against the live repository before acting on it.

## Package checks
Run `python3 scripts/validate_bundle.py`, the unit tests in `scripts/test_*.py`, `scripts/live_evals/test_live_evals.py`, `scripts/runtime_acceptance/test_collect_evidence.py` and `python3 scripts/check_knowledge_links.py` before proposing a change to this system; CI runs the same checks.

Static checks do not prove live behavior. Evidence of real runs lives in `docs/EVIDENCE.md`:
- Live skill evals run locally on the owner's account: `scripts/live_evals/run_live_evals.py` (deterministic checks), `judge.py` (LLM judge), `calibrate.py` (judge trusted only at ≥ 80% agreement and ≤ 5% false-PASS against human labels), `scorecard.py`.
- Regression rule: a change to a skill's `SKILL.md` or `evals.json` reruns that skill's live evals before merge, and the PR lists the evidence path. A skill that is not PROVEN in the latest scorecard is EXPERIMENTAL.
- Agent Teams, hooks and Secretary capture are proven only by `docs/RUNTIME_ACCEPTANCE_RUNBOOK.md` and its collector report.

## Definition of done
A task is complete only when intake, readiness and owner decisions are handled; requirements trace to checked sources; acceptance criteria and changed files are listed; relevant tests have actually run; reviewer findings are resolved or accepted; capture counts comply with the test plan; material ADR/meeting records/docs are updated; the closeout is written; knowledge entries are proposed; risks and unverified areas are disclosed.
