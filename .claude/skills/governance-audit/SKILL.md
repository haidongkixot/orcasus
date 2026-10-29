---
name: governance-audit
description: "S9 read-only audit of whether a finished change, slice or pull request followed Orcasus gates: intake class and scope, readiness, requirement citations, test plan and capture budget, debate records, independent reviews, owner approvals, merge authority, closeout and knowledge updates. Each control gets PASS, FAIL or UNVERIFIABLE citing primary evidence; missing evidence never passes. Use for retrospective review of a change, post-incident review, spot checks of agent autonomy or verification of a closeout. Do NOT use as an upcoming release gate (delivery-readiness) or to write your own closeout (closeout-report)."
---

# Governance Audit — S9

## Rules
Read-only: change nothing while auditing. Audit against the policy version in force when the change was made (`VERSION`, `CLAUDE.md` at that commit), never against rules adopted later. The closeout and agent summaries are claims to verify, not evidence.

## 1. Fix the baseline and scope
Name the change (PR, commit range or slice), the policy version and the date. List the classes declared in the intake record.

## 2. Gather primary evidence
Use git history, diffs, CI runs, test outputs, meeting event files, ADRs, readiness/trace/test-plan records, review findings and approval records. Note anything inaccessible.

## 3. Score each applicable control
| Control | PASS requires |
|---|---|
| Intake | intake record exists; class declared; touched files stayed inside the scope contract or reclassification is recorded |
| Readiness | readiness matrix before implementation; no UNKNOWN treated as AVAILABLE; blockers escalated with options |
| Requirements | trace matrix exists; no MISMATCH or NO SOURCE row reached scope without owner acceptance |
| Test plan and evidence | test plan before testing; class validation floor met with real outputs; capture counts within budget |
| Decision record | material choices have an ADR; debated choices have ballots, dissent and coverage status |
| Independent review | reviewers required by the class inspected actual evidence; findings resolved or accepted by the owner |
| Approvals | every crossed approval boundary has an owner approval whose wording covers the action taken |
| Merge/deploy authority | a human merged or deployed, or a recorded owner grant covers the agent that did |
| Closeout | all eight sections present; claims match primary evidence |
| Knowledge | proposed entries exist for durable decisions; approved entries carry curator approval |

Verdict per control: PASS (evidence cited), FAIL (violation cited) or UNVERIFIABLE (evidence missing or inaccessible — never silently upgraded).

## 4. Overall verdict and findings
Overall PASS only when every applicable control passes; any FAIL means FAIL; otherwise CONDITIONAL with the UNVERIFIABLE list. For each FAIL state whether it is a policy gap (no rule existed) or a discipline gap (rule existed and was bypassed), and the control, skill or agent rule that would close it. Feed findings to `/process-retro`.

## Output
Write `reports/<change>-governance-audit.md` from `templates/GOVERNANCE_AUDIT_TEMPLATE.md`, including a not-inspected list.

## Guardrails
- Do not fix findings during the audit; report them.
- Do not audit your own work as independent evidence; use the `governance-auditor` agent or another reviewer.
