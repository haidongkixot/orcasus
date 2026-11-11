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

- Problem: every added skill costs every session context tokens and routing ambiguity, and spreads the core rules across more texts. Measured: Orcasus has 16 skills and 5,771 description characters (corrected to 5,757 by the same method in D14 and evidence/aegis-measurement-2026-11-10.md); Aegis has 194 skills, 173,285 characters and 990 routing edges.
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

---

# Intake Record — S0 (audit follow-up)

- Intake ID: ORC-2026-11-10-audit
- Date: 2026-11-10
- Requested by / owner: repository owner (haidongkixot)
- Status: CONFIRMED
- Lane: normal

## 1. Request (verbatim owner answers, 2026-11-10)

> Email in public history: "Viết lại lịch sử branch (Khuyến nghị)". F2 hook redaction fix: "Duyệt giữ bản sửa (Khuyến nghị)". Next steps: "Chuyển PR #3 về draft", "Chạy /process-retro cho F1–F12", "Chạy lại eval còn thiếu (F13)".

The source is the independent audit [v2.4-governance-audit.md](../../reports/v2.4-governance-audit.md) (verdict FAIL).

## 2. Deliverables and classes

| ID | Deliverable | Files/modules | Class | Validation floor | Reviewers | Owner approval before work? |
|---|---|---|---|---|---|---|
| A1 | Remove the owner's e-mail address from branch history (done before this record: rewrite of `8ad462e..1b7f998`, force-push with lease) | git history of `ccr-6f83693d-3hxz8f` | infra-deploy-release (destructive history change) | no commit contains the address; final tree unchanged | owner | Yes (given above) |
| A2 | Record the owner's approval of the F2 hook-script change (`scripts/log_team_message.py`, in `ed3142c`) | this record | agent-system-config (hooks) | logger tests | governance-auditor | Yes (given above) |
| A3 | PR #3 back to draft until findings are handled | GitHub PR state | — | PR shows draft | — | Yes (given above) |
| A4 | Re-run the eval cases named in F13 | `evidence/live-evals/`, `docs/EVIDENCE.md` | test-only | runs recorded with spend | — | Yes; spend cap $3.50 (the estimate given was about $3) |
| A5 | `/process-retro` over F1–F12 | `reports/v2.4-retro.md` | docs-only (proposals) | link check | — | No (proposals only) |
| A6 | Closeout refresh for this follow-up | `reports/v2.4-closeout.md` | docs-only | link check | — | No |

## 3. Readiness (short form, audit F4)

| Area | Status | Evidence |
|---|---|---|
| Eval runtime | AVAILABLE | `claude` 2.1.314 in the container; nested runs worked on 2026-10-30 and 2026-11-10 |
| Eval budget | AVAILABLE, capped | $3.50 for A4; runner `--budget-total` per invocation |
| Reviewer availability | PARTIAL | governance-auditor runs in this session only (audit F11) |
| CI | AVAILABLE | GitHub Actions on 3 OSes; results read through the PR checks |
| GitHub write for PR state | AVAILABLE | GitHub tools in this session |

## 4. Scope contract

- **Expected files:** `docs/agent-ops/INTAKE_RECORD.md`, `docs/EVIDENCE.md`, `reports/v2.4-closeout.md`, `reports/v2.4-retro.md`, `reports/live-eval-scorecard.*`, `evidence/live-evals/**`.
- **SHA references:** records that cite commits rewritten in A1 are updated to the new SHAs: `8ad462e`→`85fc342`, `c17c589`→`b304f28`, `4ff4fe8`→`f7567a8`, `3455dfb`→`29988b0`, `c8907d6`→`3d5c5fa`, `130d6c1`→`73e1642`, `1b7f998`→`ed3142c`. The audit report keeps its original SHAs, with a note.
- **Out of scope:** any process change itself. The retro only proposes; each proposal needs its own approval.
- **Known limit of A1:** GitHub may keep the old commits reachable by SHA, for example from the PR timeline, until garbage collection or a support request. That is outside this session's control.

## 5. Reclassification log

| Date | Trigger | New class | Approval obtained |
|---|---|---|---|

---

# Intake Record — S0 (retro adoption)

- Intake ID: ORC-2026-11-11-retro
- Date: 2026-11-11
- Requested by / owner: repository owner (haidongkixot)
- Status: CONFIRMED (selection delegated to the agent)
- Lane: normal

## 1. Request (verbatim)

> "You decide" (owner, 2026-11-10). This answers the open choice of which retro proposals R1–R12 ([v2.4-retro.md](../../reports/v2.4-retro.md)) to adopt. The agent's selection and its reasons are below. The owner can reverse any of them; see [APPROVALS.md](APPROVALS.md).

## 2. Deliverables and classes

| ID | Decision | Deliverable | Files | Class | Validation floor |
|---|---|---|---|---|---|
| R1 | ADOPT | Commits after a closeout need a new intake or a reclassification row committed first | `CLAUDE.md`, change-intake | agent-system-config | validator |
| R2 | DEFER | Gate-order/scope CI check. It needs a machine-readable scope contract, a new format. Revisit if the next audit fails gate order | — | — | — |
| R3 | ADOPT | "Hooks" includes the scripts they run; templates are agent-system-config; changing a hook script needs an approval row | change-intake | agent-system-config | validator |
| R4 | ADOPT | Records redact personal data, not only secrets; nested eval runs carry no account identity variables | `CLAUDE.md`, `scripts/live_evals/run_live_evals.py` + test | agent-system-config | unit tests |
| R5 | ADOPT | Short readiness table for agent-system-config in the intake; its validation-floor table is the test plan for that class | change-intake, efficient-testing, intake template | agent-system-config | validator |
| R6 | ADOPT (text only) | One closeout per intake; header head SHA refreshed at the final head before the audit | closeout-report | agent-system-config | validator |
| R7 | ADOPT | D-entries carry options, a decision state and a revisit trigger; D14 completed, D15 added for the judge auto-FAIL rule | `docs/RESEARCH_AND_DECISIONS.md` | docs-only | link check |
| R8 | ADOPT | Approvals log with the owner's verbatim words | `docs/agent-ops/APPROVALS.md` | docs-only | link check |
| R9 | ADOPT | Audits run in a separate session or are countersigned by the owner; re-audit v2.4 in a new cloud session | `CLAUDE.md`; report file | agent-system-config | report saved |
| R10 | ADOPT | Fix eval cases with design defects; add eval-authoring rules to the overlay README | 6 `evals.json`, overlays | agent-system-config | evals valid; live re-run |
| R11 | ADOPT | `"trigger": "skill-or-rule"` cases are scored by assertions, never auto-FAILed | `scripts/live_evals/*`, `scripts/skill_evals.py` + tests | agent-system-config | unit tests |
| R12 | ADOPT | Hotfix lane writes and commits the minimal intake first and names the security review | change-intake | agent-system-config | evals valid; live re-run |

Reasons for the selection:
- **Focus (D14):** short rules in one place, machine checks where cheap, no new skill, and nothing that needs a new structured format (R2).

## 3. Readiness (short form, R5)

| Area | Status | Evidence |
|---|---|---|
| Eval runtime | AVAILABLE | `claude` CLI in the container; nested runs worked on 2026-11-10 |
| Eval budget | AVAILABLE, capped | **$4** for re-runs in this intake |
| Separate session for the re-audit | AVAILABLE | `create_session` tool in this session |
| CI | AVAILABLE | GitHub Actions on 3 OSes |

## 4. Scope contract and test plan

- **Files:** those in section 2, plus `CHANGELOG.md`, `docs/EVIDENCE.md`, `reports/` (closeout and re-audit), `evidence/live-evals/**`, `knowledge/INDEX.md` and `.github/workflows/validate.yml` if a test file is added.
- **Test plan (R5):** the validation floors in section 2, plus all package checks and CI green.
- **Out of scope:**
  - human calibration labels (owner only);
  - leaving draft on PR #3;
  - R2.

## 5. Reclassification log

| Date | Trigger | New class | Approval obtained |
|---|---|---|---|
| 2026-11-11 | Re-audit (`reports/v2.4-governance-audit-2.md`) findings fixable by the author: N7 judge records its cost (code, `scripts/live_evals/judge.py` + test), N5 closeout corrections, N6 intake-2 figure note, N9 PR body. Committed before the code (R1) | agent-system-config (same class) | Within the delegated selection ("You decide"); owner confirmation of the R-list still pending (N2) |
