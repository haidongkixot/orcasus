# Meeting Recording Protocol

## Scope
Record observable team communications and explicit records: proposals, stated rationale, evidence, questions, challenges, rebuttals, ballots, decisions, dissent and action items. Do not request, capture or claim to capture hidden chain-of-thought or unexpressed private reasoning.

## Lifecycle
1. Create a unique meeting ID and activate meetings/CURRENT_MEETING.json before substantive debate.
2. Start team-secretary first; declare participants, voting roster, decision criteria and privacy boundary.
3. Confirm hooks in .claude/settings.json point to scripts/log_team_message.py. This is a static check only.
4. Participants send a copy of key proposals, critiques, rebuttals and FINAL_BALLOT directly to secretary as a backup to hooks.
5. Reconcile observable event files with direct records. Distinguish captured, manually recorded, redacted, missing and unverified content.
6. Produce MINUTES.md, DISCUSSION_LOG.md, VOTE_REGISTER.md, DECISION_SUMMARY.md, ACTION_ITEMS.md and COVERAGE_REPORT.md.
7. Close only after teammates have stopped; set the manifest inactive after reconciliation.

## Capture statuses
- CAPTURE VERIFIED: at least two actual teammates exchanged messages; event files contain sender, recipient and sufficient message content; no unexplained material gaps remain.
- PARTIAL: some events/records exist but coverage is incomplete.
- NOT VERIFIED: hook was not runtime-tested, peers/tools unavailable, or no sufficient evidence exists.

Never infer ballots from silence or idle state. Secretary is neutral/non-voting by default. Redact secrets; secret redaction is best effort and must be disclosed as such. Hook failure must not block a team message. One active meeting per workspace is supported; use separate worktrees for concurrent meetings.
