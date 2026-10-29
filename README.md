# Orcasus — Claude Code Skills for Disciplined Web/Mobile Engineering

Orcasus is a reusable skills library that helps Claude Code teams discover project resources and permissions before choosing a solution, and test features efficiently with explicit evidence and artifact budgets.

## Version 1.3.0

This release strengthens two core skills:
- **Project Discovery**: a mandatory preflight gate. The orchestrator consolidates evidence about repository, assets/licences, integrations, credentials/scopes, tools, environments, test resources and budget before assigning implementation.
- **Efficient Testing**: screenshot, trace and video budgets default to zero. Capture remains disabled unless a named visual/diagnostic question, bounded budget and owner approval or pre-approved project policy exist.

Orcasus is a skills and workflow library, not a standalone agent runtime or a technical permission-enforcement sandbox. Apply the Agent Operating Contract to each consuming project's CLAUDE.md and validate behavior in that project.

## What this is designed to prevent

- Coding starts before assets, permissions, integrations and environments have been checked.
- Agents silently substitute fake integrations, placeholder assets, local-only behavior or degraded workarounds.
- Tests create screenshots for each screen/state/run or use AI-generated images instead of behavioral assertions.
- Broad suites are rerun without diagnosing initial failures.
- Reports claim success without execution evidence or hide untested areas.

## Core skills

| Skill | Use it for | Required outputs |
|---|---|---|
| [Project Discovery](skills/project-discovery/SKILL.md) | New projects/features, integrations, redesigns, migrations and material bug fixes | Evidence-backed readiness matrix, discovery summary, blockers/options and owner decisions |
| [Efficient Testing](skills/efficient-testing/SKILL.md) | Test planning and execution | Acceptance-criterion test matrix, lowest-cost reliable test layers, capture budget and evidence report |

## Recommended reading order

1. [Vietnamese User Guide](docs/USER_GUIDE_VI.md)
2. [Discovery and Testing Principles](docs/discovery-and-testing-principles.md)
3. [Agent Operating Contract](docs/agent-operating-contract.md)
4. [Readiness Matrix template](templates/READINESS_MATRIX_TEMPLATE.md)
5. [Risk-Based Test Plan template](templates/TEST_PLAN_TEMPLATE.md)

## Quick install

Copy both skill folders into the target project's .claude/skills/ directory, copy templates into docs/agent-ops/templates/, and merge the Agent Operating Contract into the existing CLAUDE.md without overwriting project-specific instructions.

Once installed, invoke /project-discovery and /efficient-testing at the start of material work. The orchestrator must include the gates in prompts to teammates; installing a skill alone does not guarantee every agent invokes it.

See [docs/USER_GUIDE_VI.md](docs/USER_GUIDE_VI.md) for Windows PowerShell and macOS/Linux instructions and the full workflow.

## Non-negotiable principles

- Verify evidence; UNKNOWN is not AVAILABLE.
- No implementation before the readiness gate for material tasks.
- No silent workaround that changes required quality or behavior.
- Screenshot, trace and video budgets default to zero.
- AI-generated imagery is not evidence that a real application works.
- Prefer the cheapest reliable test layer and diagnose failure before retries.
- Report PASS, FAIL, BLOCKED, NOT RUN and SKIPPED truthfully.

## Version and references

Current version: **1.3.0**. See CHANGELOG.md.

- Claude Code Skills: https://code.claude.com/docs/en/skills
- Claude Code Permissions: https://code.claude.com/docs/en/permissions
- Claude Code Hooks: https://code.claude.com/docs/en/hooks
- Playwright test options: https://playwright.dev/docs/api/class-testoptions
- Playwright test configuration: https://playwright.dev/docs/test-use-options
- Testing Library query priority: https://testing-library.com/docs/queries/about/
