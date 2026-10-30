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
