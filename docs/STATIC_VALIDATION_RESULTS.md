# Static Validation Results — Orcasus v2.2.0

Validation date: 2026-10-29

## Static checks verified by reading the committed GitHub tree and file contents

- Main branch points to commit 629664e66ec743d2e3983503c2bd0b109055892c at the time of this check.
- The committed tree contains the complete runtime layout, 15 agent definition files, 9 skill files, settings, meeting logger and tests, documentation, templates and output folders.
- The JSON in .claude/settings.json parses successfully.
- All 15 agent files were fetched and each has a YAML frontmatter start/end, name, description and non-empty role instructions.
- All 9 skill files were fetched and each has a YAML frontmatter start/end, name, description and non-empty workflow instructions.
- Root library copies of skills/project-discovery/SKILL.md and skills/efficient-testing/SKILL.md are byte-equivalent at the GitHub blob level to their .claude/skills runtime copies.
- Efficient Testing declares screenshot, trace and video budgets as zero by default and prohibits generated images as app-test evidence.
- The readiness and test-plan templates include explicit resources/access checks and capture-budget controls.
- The meeting manifest starts inactive.
- Hook settings include PostToolUse filtered to SendMessage and task lifecycle events that reference scripts/log_team_message.py.

## Not run / not proven

- The Python scripts were not executed against a local checkout during this validation. Network access in the execution container did not resolve github.com, so clone-based local execution was unavailable.
- Agent Teams creation, peer messaging, shared task behavior, hooks firing inside real teammate sessions and meeting coverage reconciliation were not tested at runtime.
- Permission enforcement, product UX, performance, cost and production readiness are not proven by static validation.

## Required runtime checks

Use the instructions in INITIALIZE_AGENTS.md and docs/ACCEPTANCE_TESTS.md. Run python scripts/test_meeting_logger.py and python scripts/validate_bundle.py locally; then conduct the live multi-teammate logger test before reporting CAPTURE VERIFIED.
