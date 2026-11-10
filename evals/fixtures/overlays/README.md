# Eval fixture overlays

A case in `.claude/skills/<skill>/evals/evals.json` can set `"setup": {"overlay": "<name>"}`. The live runner copies `overlays/<name>/` over the sample-app fixture before the baseline commit. Use an overlay when a skill is only reachable after an earlier gate: for example, a confirmed intake record so that discovery or delivery is the next step. Without one, the agent correctly stops at intake.

| Overlay | Puts the workspace in this state |
|---|---|
| `stripe-intake-confirmed` | Intake for Stripe card payments CONFIRMED by the owner; the PRD moves payments into this phase. Discovery is the next gate. |
| `sl2-ready` | SL-2 (CSV export API) has a confirmed intake, a READY readiness matrix, a test plan and resolved requirements. Building the slice is the next step. |
