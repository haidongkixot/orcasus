---
name: meeting-record
description: Open, maintain, reconcile, and close a recorded Agent Team meeting with observable messages, explicit ballots, decisions, dissent, actions, and coverage status.
---

# Meeting Record Workflow

1. Assign a unique meeting ID and activate meetings/CURRENT_MEETING.json before discussion.
2. Create session folder and agree on question, participants, voters, criteria and privacy boundary.
3. Start team-secretary before substantive discussion.
4. Confirm PostToolUse SendMessage and task lifecycle hooks are configured through scripts/hooks/run_python.sh and that the SessionStart runtime line says OK. Configuration alone is not proof of runtime capture.
5. Instruct participants to send proposals, challenges, rebuttals and FINAL_BALLOT to secretary as a structured backup.
6. Preserve observable event payloads after best-effort redaction; never capture or claim hidden chain-of-thought.
7. Reconcile events with explicit records and label missing/redacted/unverified content.
8. Generate minutes, discussion log, vote register, decision summary, actions and coverage report.
9. Mark CAPTURE VERIFIED only after a live multi-teammate test; otherwise PARTIAL or NOT VERIFIED. Entries in meetings/HOOK_ERRORS.log during the meeting window cap the status at PARTIAL.
10. Propose durable decisions, dissent and actions to `/knowledge-curation`.
11. Deactivate manifest only after debate ends and teammates have stopped.

Never infer a vote from silence. Lead, not secretary, owns the decision.
