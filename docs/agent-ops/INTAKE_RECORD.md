# Intake Record — S0

> Completed with `/change-intake` before any change to the Orcasus system files for v2.4.0.

- Intake ID: ORC-2026-10-30-v2.4
- Date: 2026-10-30
- Requested by / owner: repository owner (haidongkixot)
- Status: CONFIRMED

## 1. Request (verbatim)

> "tiếp tục kế hoạch cải tiến Orcasus" (owner, 2026-10-30). The owner approved the v2.4 plan (P1–P9) in the session's plan approval the same day.

The plan turns the tbagri-web pilot retro proposals into rules and checks: [pilot evidence](../../evidence/pilots/tbagri-web-2026-10-29.md). The full retro is reports/sl-1-retro.md in the private tbagri-web repository.

## 2. Deliverables and classes

| ID | Deliverable | Files/modules inspected | Class | Validation floor | Reviewers | Owner approval before work? |
|---|---|---|---|---|---|---|
| P1 | Only the owner may set ASSUMPTION-ACCEPTED; the checker fails rows without an owner name and date | `.claude/skills/requirements-traceability/SKILL.md`, `templates/TRACE_MATRIX_TEMPLATE.md`, `scripts/check_knowledge_links.py` | agent-system-config | evals + validator; checker unit tests | governance-auditor | Yes (given 2026-10-30) |
| P2 | Subagent-mode debate when Agent Teams are unavailable | `team-debate` skill, `docs/DEBATE_PROTOCOL.md`, `docs/ADR_TEMPLATE.md` | agent-system-config | evals + validator | governance-auditor | Yes (given) |
| P3 | Intake enumerates domain values from code before a policy question | `change-intake` skill | agent-system-config | evals + validator | governance-auditor | Yes (given) |
| P4 | Records committed before code; security review saved; closeout before audit; gate-order audit control; dangling record-path warning | `CLAUDE.md`, `governance-audit` and `closeout-report` skills, checker | agent-system-config | evals + validator; checker unit tests | governance-auditor | Yes (given) |
| P5 | Evidence pack for the security reviewer (no new tool grant) | `.claude/agents/security-reviewer.md`, `vertical-slice-delivery` skill | agent-system-config | validator | governance-auditor | Yes (given) |
| P6 | Discovery takes env var names from code (no permission change) | `project-discovery` skill, readiness template | agent-system-config | evals + validator | governance-auditor | Yes (given) |
| P7 | Allowed-path tests assert exact statuses | `efficient-testing` skill, test plan template | agent-system-config | evals + validator | governance-auditor | Yes (given) |
| P8 | Draft PR before review and audit | `docs/USER_GUIDE_VI.md`, `docs/TEAM_OPERATING_MODEL.md` | docs-only | link check | — | No |
| P9 | Hotfix lane: same gates, different completion order | `CLAUDE.md`, `change-intake` skill, `docs/AI_SDLC_STAGE_MAP.md` | agent-system-config | evals + validator | governance-auditor | Yes (given) |

- Governing class (highest risk): agent-system-config. No permission, hook or tool grant changes: the retro's P5 (Bash for the reviewer) and P6 (allow reading `.env.example`) were replaced by process changes, so no grant widens.
- Suggestions recorded but NOT in scope: live eval runs (owner's machine), Agent Teams runtime acceptance, any change in tbagri-web.

## 3. Duplicate and conflict check

| Deliverable | Sources searched | Verdict | Citation |
|---|---|---|---|
| P1–P9 | knowledge/INDEX.md (empty), decisions/ (empty), projects/ (empty), reports/ (empty), docs/, open PRs | EXTENDS | v2.3.0 in open PR #3 (https://github.com/haidongkixot/orcasus/pull/3); the pilot record lists P1–P8 as PROPOSED |
| P5, P6 | `.claude/settings.json`, security-reviewer agent | CONFLICTS with the retro wording, resolved in the approved plan | Deny rules win over allow, and Bash cannot be limited to read-only, so both became process changes |

## 4. Intent and value (owner-confirmed)

- Problem: the pilot's governance audit failed because key rules existed only in prose, gate order could not be proven, and debates without Agent Teams had no protocol.
- Who is affected: the owner and any reviewer relying on Orcasus records.
- Expected value: the failures seen in the pilot are caught by a check or have a written procedure.
- Success signal: the new checker flags the pilot's two record errors (self-accepted assumption, dangling closeout path) when they are reproduced; package checks and CI stay green.
- Urgency / deadline: none stated.
- Non-goals: new gates without pilot evidence; permission or tool-grant changes.
- Owner confirmation: plan approved 2026-10-30, then "tiếp tục kế hoạch cải tiến Orcasus".

## 5. Scope contract

- Expected files/modules: the files listed in section 2, their `evals/evals.json`, `scripts/test_knowledge_links.py`, `VERSION`, `CHANGELOG.md`, `docs/EVIDENCE.md`, this record and `reports/v2.4-closeout.md`.
- Out of scope: `.claude/settings.json`, hooks, agent tool lists, tbagri-web.
- Approval path: owner reviews and merges PR #3; v2.4 rides on the same branch because this session can push only there.
- Next gate: implementation in this order: records, checker, skills and docs, closeout. Readiness for this change: the package checks run locally, and CI runs on Ubuntu, macOS and Windows.

## 6. Reclassification log

| Date | Trigger (file/layer/behavior outside contract) | New class | Approval obtained |
|---|---|---|---|
| 2026-10-30 | Version titles (README, INITIALIZE_AGENTS, DEFINITION_OF_DONE), D13 in RESEARCH_AND_DECISIONS, STATIC_VALIDATION_RESULTS, knowledge/README, the pilot record, and the intake and audit templates were edited to carry the same P1–P9 text | docs-only (lower than the governing class) | Covered by the approved plan; no new class |

---

# Intake Record — S0 (focus rule)

- Intake ID: ORC-2026-11-10-focus
- Date: 2026-11-10
- Requested by / owner: repository owner (haidongkixot)
- Status: CONFIRMED
- Lane: normal

## 1. Request (verbatim)

> "Theo quan điểm của tôi, số lượng skill tăng lên sẽ làm giảm sức mạnh của sự tập trung của triết lý" (owner, 2026-11-10). Asked whether to make it a rule with validator checks, the owner chose "Có, thêm luật", then approved the plan.

## 2. Deliverables and classes

| ID | Deliverable | Files/modules inspected | Class | Validation floor | Reviewers | Owner approval before work? |
|---|---|---|---|---|---|---|
| F1 | "Skill admission and focus" rule | `CLAUDE.md` | agent-system-config | validator | governance-auditor | Yes (given 2026-11-10) |
| F2 | Validator checks: core skill cap, description budget, stage-map entry, "Do NOT use" boundary | `scripts/validate_bundle.py`, `scripts/skill_evals.py` | agent-system-config | unit tests + validator | governance-auditor | Yes (given) |
| F3 | Boundary clause added to the 9 skill descriptions that lack one; `root-cause-debate` added to the stage map | 9 `SKILL.md` and 2 mirrors, `docs/AI_SDLC_STAGE_MAP.md` | agent-system-config | evals valid + validator; live evals required by the regression rule | governance-auditor | Yes (given) |
| F4 | Decision D14, user guide, README, changelog, closeout | docs | docs-only | link check | — | No |

- Governing class: agent-system-config. No permission, hook or tool grant changes.
- Suggestions NOT in scope: creating optional skill packs; removing or merging any current skill.

## 3. Duplicate and conflict check

| Deliverable | Sources searched | Verdict | Citation |
|---|---|---|---|
| F1–F4 | knowledge/INDEX.md (K-0001, K-0002), decisions/ (empty), docs/RESEARCH_AND_DECISIONS.md (D1–D13), open PR #3 | NEW | No existing rule caps core skills or requires boundary clauses; `validate_bundle.py` checks only the exact skill set and the 1024-character limit per description |

## 4. Intent and value (owner-confirmed)

- Problem: every added skill costs every session context tokens and routing ambiguity, and spreads the core rules across more texts. Measured: Orcasus has 16 skills and 5,771 description characters; Aegis has 194 skills, 173,285 characters and 990 routing edges.
- Expected value: the core stays small and each skill has a clear boundary, so routing and the core rules stay sharp.
- Success signal: the validator fails a bundle that exceeds the cap or budget, or that has a skill without a stage-map entry or a boundary clause.
- Urgency: none stated. Non-goals: shrinking the current set.
- Owner confirmation: answer "Có, thêm luật (Khuyến nghị)" and plan approval, 2026-11-10.

## 5. Scope contract

- Expected files: those in section 2, `scripts/test_skill_focus.py`, `.github/workflows/validate.yml` (to run the new test), `docs/RESEARCH_AND_DECISIONS.md`, `docs/USER_GUIDE_VI.md`, `README.md`, `CHANGELOG.md`, `reports/v2.4-closeout.md`.
- Out of scope: settings, hooks, agent tool lists, live eval runs (they cost money above the approved cap; recorded as NOT RUN).
- Next gate: implementation. Changed descriptions require live evals before merge, under the regression rule.

## 6. Reclassification log

| Date | Trigger | New class | Approval obtained |
|---|---|---|---|
| 2026-11-10 | Owner agreed to fix the smoke-run eval findings and run the pending live evals: live-eval harness (overlays, per-case budget, harness note) and three eval cases | agent-system-config (same class) | Owner "Đồng ý", 2026-11-10; live eval spend capped at $6 |
