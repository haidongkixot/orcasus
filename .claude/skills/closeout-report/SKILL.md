---
name: closeout-report
description: "S9 closeout for a finished or stopped task, slice or milestone: what changed, a mandatory intentionally-not-done section, files touched from git, validation actually run with real results, a per-deliverable trace from request item to files, check and evidence, risks, skipped validation and next action. Scope reductions are disclosed, never silent. Use when finishing a task or slice, handing off work, opening a pull request or answering what was actually done. Do NOT use to judge whether someone else's change followed the rules (governance-audit) or as a release gate (delivery-readiness)."
---

# Closeout Report — S9

## Gate
A task is not reported complete until its closeout exists and every deliverable is either proven by evidence or listed as not done.

## Steps
1. Re-read the intake record, trace matrix, backlog slice and the original request. List every explicit deliverable.
2. Mark each deliverable DONE, PARTIAL, NOT DONE or NOT APPLICABLE.
3. Put everything not fully done in **Intentionally not done / omitted** with the reason, including quiet reductions (asked for ten, delivered six). Write "None." explicitly when empty.
4. List files touched from `git diff --name-only <base>...HEAD` and `git status`, not from memory. Compare them with the intake scope contract; any file outside it is a finding.
5. Record validation with the exact commands, exit codes, durations where available and PASS/FAIL/SKIPPED/BLOCKED/NOT RUN counts. Copy failures verbatim. Include screenshot/trace/video counts against the approved budget.
6. Build the trace: request item → files → check → evidence (command + exit code, CI run link or report path) at a named commit SHA. A deliverable without a proving check is "not verified" and also appears under Skipped validation; it is never DONE.
7. State risks, known gaps, unverified integrations/platforms and owner decisions still open.
8. Recommend the next action. When a milestone is merged, add a completion anchor: "<work> is complete; do not treat as pending", pinned to the merged PR/commit SHA and date.
9. Propose knowledge entries (decisions, constraints, lessons) for `/knowledge-curation`; do not approve them yourself.

## Output
Write `reports/<task-or-slice>-closeout.md` from `templates/CLOSEOUT_TEMPLATE.md` with all eight sections in order: Summary; Intentionally not done / omitted; Files touched; Tests and validation run; Evidence trace; Risks and known gaps; Skipped validation; Next actions and handoff.

## Order
Write and commit the closeout before `/governance-audit` starts. An audit run against a missing closeout fails the closeout control.

## Guardrails
- Never write "complete" or "verified" while a recorded gap is open; qualify the claim and name the gap.
- Never mark NOT RUN or BLOCKED as PASS.
- The closeout is a claim sheet; `/governance-audit` verifies it against primary evidence.
