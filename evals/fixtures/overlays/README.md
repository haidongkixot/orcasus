# Eval fixture overlays

A case in `.claude/skills/<skill>/evals/evals.json` can set `"setup": {"overlay": "<name>"}`. The live runner copies `overlays/<name>/` over the sample-app fixture before the baseline commit. Use an overlay when a skill is only reachable after an earlier gate: for example, a confirmed intake record so that discovery or delivery is the next step. Without one, the agent correctly stops at intake.

| Overlay | Puts the workspace in this state |
|---|---|
| `stripe-intake-confirmed` | Intake for Stripe card payments CONFIRMED by the owner; the PRD moves payments into this phase. Discovery is the next gate. |
| `sl2-ready` | SL-2 (CSV export API) has a confirmed intake, a READY readiness matrix, a test plan and resolved requirements. Building the slice is the next step. Also used by the team-debate positive case so its export question does not hit the SL-2 conflicts. |
| `settings-page` | Adds a small settings page (`public/settings.html`, `public/settings.css`) with real accessibility defects, so the design-quality-gate case has a UI to review. |
| `rca-intake-confirmed` | Confirmed intake for an intermittent cross-organization invoice in `GET /invoices`; the next gate is root-cause-debate. |
| `platform-intake-confirmed` | Confirmed intake for a new work-management platform; the next gate is platform-discovery. |
| `storage-intake-confirmed` | Confirmed intake for the invoice storage decision; the next gate is team-debate. |

## Writing an eval case (retro R10)

1. Every artefact the prompt names must exist in the fixture or in the case's overlay. "Milestone 3", "the settings page" and "orders" did not exist, and agents correctly refused.
2. A case for a skill that comes after an earlier gate (discovery, debate, delivery, root-cause) needs an overlay holding that gate's confirmed record. Without one, the agent stops at intake as CLAUDE.md requires.
3. If CLAUDE.md states the behavior as a rule, mark the case `"trigger": "skill-or-rule"`. It is then scored by its assertions, not by whether the skill was invoked.
4. Avoid prompts that ask an agent to reveal hidden reasoning. The model provider may block them before the agent acts.
5. After a change, run the case once before relying on it. Two of the 2026-11-10 rewrites collided with fixture traps.
