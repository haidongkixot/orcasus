# Requirements Trace Matrix — S3 (Orcasus v2.4.0)

> Written with `/requirements-traceability` on 2026-11-17, after the fact, to close audit findings F7 and N6. Every citation was opened on that date by Claude (author session). Citation status values: VERIFIED, PARAPHRASE-OK, MISMATCH, UNVERIFIABLE, NO SOURCE. Requirement status values: PROPOSED, APPROVED, REJECTED, ASSUMPTION-ACCEPTED. Only the owner sets ASSUMPTION-ACCEPTED.

- Scope: retro rules P1–P9 (intake ORC-2026-10-30-v2.4) and the skill focus rule (intake ORC-2026-11-10-focus)
- Intake record: [INTAKE_RECORD.md](INTAKE_RECORD.md)
- Owner: repository owner

All ten requirements are already implemented on the branch. Rows marked PROPOSED are implemented **without** a source that states them; they stay PROPOSED until the owner answers the questions below.

## Sources

| Source ID | Type | Location | Accessible? | Quote or summary with date |
|---|---|---|---|---|
| S1 | Pilot record (in repo) | [tbagri-web pilot](../../evidence/pilots/tbagri-web-2026-10-29.md#L26-L33) | Yes | The eight retro proposals, 2026-10-29 |
| S2 | Full retro (private repo) | reports/sl-1-retro.md in haidongkixot/tbagri-web | No (not in this repository) | P1–P8 in full |
| S3 | Owner approvals log | [APPROVALS.md](APPROVALS.md#L7) | Yes, agent-transcribed | "tiếp tục kế hoạch cải tiến Orcasus" + plan approval, 2026-10-30 |
| S4 | Owner approvals log | [APPROVALS.md](APPROVALS.md#L10) | Yes, agent-transcribed | "Có, thêm luật (Khuyến nghị)" + plan approval, 2026-11-10 |
| S5 | Decision record | [D13](../RESEARCH_AND_DECISIONS.md#L49), [D14](../RESEARCH_AND_DECISIONS.md#L52) | Yes | Why P5/P6 were replaced; the focus rule |
| S6 | The approved v2.4 plan | session plan file, not saved in the repository | No | Listed P1–P9 with the P5/P6 replacements and P9 |

## Requirements

| Req ID | Requirement (as written) | Priority | Source citation | Citation status | Checked by / date | Acceptance criteria | Test layer / test | Evidence | Requirement status | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| P1 | Only the owner may set ASSUMPTION-ACCEPTED; the checker fails rows without an owner name and date | High | [pilot item 1](../../evidence/pilots/tbagri-web-2026-10-29.md#L26); [approval](APPROVALS.md#L7) | VERIFIED | Claude 2026-11-17 | A row marked ASSUMPTION-ACCEPTED without `accepted by owner: <name> date`, or naming an agent, fails the checker | Unit: `test_assumption_accepted_needs_human_owner`; live case `edge-agent-self-accepts-assumption` | `scripts/test_knowledge_links.py`; run `e5e1c1` (4/4) | APPROVED | — |
| P2 | Subagent-mode debate with verbatim ballots and a voter-scored matrix when Agent Teams are unavailable | High | [pilot item 2](../../evidence/pilots/tbagri-web-2026-10-29.md#L27); [approval](APPROVALS.md#L7) | VERIFIED | Claude 2026-11-17 | At least 4 voters, voters score, ballots saved verbatim, capture NOT VERIFIED | Live case `team-debate/edge-no-agent-teams` | run `b9d145` (5/5) | APPROVED | — |
| P3 | Intake lists every domain value (roles, statuses) from code before a policy question | Medium | [pilot item 3](../../evidence/pilots/tbagri-web-2026-10-29.md#L28); [approval](APPROVALS.md#L7) | VERIFIED | Claude 2026-11-17 | The question to the owner lists all values with file:line | Live case `edge-policy-question-lists-domain-values` | run `446c52` (4/4) | APPROVED | — |
| P4 | Intake and readiness records are committed before code; reviews are saved in `reports/`; the closeout exists before the audit | High | [pilot item 4](../../evidence/pilots/tbagri-web-2026-10-29.md#L29) | MISMATCH | Claude 2026-11-17 | Gate order readable from git; saved review file; closeout precedes audit | Audit control "Gate order"; live cases P4 ×2 | runs `880ce5`, `e5e1c1` | PROPOSED | The source says "S0–S5 records before code". The rule as written covers only intake and readiness (trace, ADR, backlog and test plan may follow). Narrowed by the agent; see owner question Q1 |
| P5 | Reviewers without a shell get an evidence pack (diff, test/typecheck/build output with exit codes); no Bash grant | Medium | [pilot item 5](../../evidence/pilots/tbagri-web-2026-10-29.md#L30); [D13](../RESEARCH_AND_DECISIONS.md#L49) | MISMATCH | Claude 2026-11-17 | The security-reviewer tool list is unchanged; the agent file asks for an evidence pack | Validator (agent roster, tool grants unchanged) | `validate_bundle.py` | PROPOSED | The source asks for read-only Bash. Replaced because Bash cannot be limited to read-only (D13). The replacement was in the approved plan (S6, not in the repository); see Q2 |
| P6 | Discovery takes env var names from code; the `.env*` deny rules stay unchanged | Medium | [pilot item 6](../../evidence/pilots/tbagri-web-2026-10-29.md#L31); [D13](../RESEARCH_AND_DECISIONS.md#L49) | MISMATCH | Claude 2026-11-17 | `.claude/settings.json` deny rules unchanged; project-discovery names code as the source | Validator (hook and settings checks) | `validate_bundle.py` | PROPOSED | The source asks to allow reading `.env.example`. Replaced because deny wins over allow (D13); see Q2 |
| P7 | Tests on allowed paths assert the exact expected status | Medium | [pilot item 7](../../evidence/pilots/tbagri-web-2026-10-29.md#L32); [approval](APPROVALS.md#L7) | VERIFIED | Claude 2026-11-17 | A test asserts the exact result, not only "no permission error" | Live case `edge-vacuous-allowed-path` | runs `880ce5` (3/3), `e5e1c1` (2/3) | APPROVED | — |
| P8 | Open the pull request as a draft; mark it ready only after the reviews, the closeout and the audit exist | Medium | [pilot item 8](../../evidence/pilots/tbagri-web-2026-10-29.md#L33) | MISMATCH | Claude 2026-11-17 | PR is draft until reviews, closeout and audit exist | PR state on GitHub | PR #3 is draft since 2026-11-10 | PROPOSED | The source says "document the conflict between stop hooks and review-before-push". The rule goes further and requires a draft PR; see Q3 |
| P9 | Hotfix lane: minimal intake first, fix with negative tests on a draft PR, security review, remaining records before the PR leaves draft | Medium | — | NO SOURCE | Claude 2026-11-17 | The intake is written and committed before code in a hotfix; lane recorded with owner confirmation | Live case `change-intake/edge-hotfix-lane` | runs `880ce5`, `e5e1c1` (2/5 each) | PROPOSED | Proposed by the agent in its post-pilot evaluation (chat) and listed in the approved plan (S6). Neither is in the repository; see Q4 |
| F1 | The core holds at most 20 skills and 9,000 description characters; each skill has a stage-map entry and a "Do NOT use" boundary | High | [approval](APPROVALS.md#L10); [D14](../RESEARCH_AND_DECISIONS.md#L52) | PARAPHRASE-OK | Claude 2026-11-17 | The validator fails a bundle over either limit or with a skill lacking a stage or a boundary | Unit: `scripts/test_skill_focus.py`; validator | 4/4 tests; 133 passed | APPROVED | The owner stated the principle and chose "add the rule"; the two numbers were the agent's proposal in the plan the owner approved. The approval row is agent-transcribed (audit F12) |

Citation format: repo-relative link with a line anchor, `meeting:<meeting-id>`, commit SHA, ticket link or full URL.

## Owner questions

| Req ID | Status needing a decision | Question | Recommendation | Owner decision / date |
|---|---|---|---|---|
| P4 (Q1) | MISMATCH | The retro said "commit S0–S5 records before code". The rule requires only the intake and readiness records first. Keep the narrower rule, or require all S0–S5 records first? | Keep the narrower rule: trace, ADR and test plan often depend on discovery results, and the hotfix lane already orders the rest before merge | Open |
| P5, P6 (Q2) | MISMATCH | The retro asked for a Bash grant and an `.env.example` read exception. Both were replaced by process changes (evidence pack; env names from code). Confirm the replacements? | Confirm: neither grant can be scoped safely (D13) | Open |
| P8 (Q3) | MISMATCH | The retro asked only to document the stop-hook conflict. The rule requires a draft PR until reviews, closeout and audit exist. Keep the stronger rule? | Keep: it is what made the audit findings visible before merge | Open |
| P9 (Q4) | NO SOURCE | The hotfix lane has no written source in this repository. Accept it as a requirement, change it, or remove it? | Accept; record it as ASSUMPTION-ACCEPTED with your name and date, or state the source | Open |
