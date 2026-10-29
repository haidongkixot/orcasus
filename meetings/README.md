# Meeting Records

The CURRENT_MEETING.json manifest identifies the one active debate in this workspace. Before a material debate, create a unique meeting ID and set active=true. After the Secretary reconciles events, minutes, ballots, decisions and actions and all teammates have stopped, set active=false.

Session records live in sessions/<meeting-id>/. Hook event payloads are stored in events/. Messages outside an active meeting go into unassigned/ for later reconciliation, not silently discarded.

A logger hook is best-effort. Its presence in settings does not prove it executes in each teammate session. Test with actual messages from at least two teammates and compare source messages to event files.

Never store hidden chain-of-thought or raw secret values. Redaction is best-effort; inspect event payloads before sharing logs. Use a separate worktree for concurrent meetings because only one active meeting is supported per workspace.
