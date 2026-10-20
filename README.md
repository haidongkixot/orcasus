# Orcasus — Claude Code Skills for Disciplined Web/Mobile Engineering

Orcasus is a reusable skills library for Claude Code. It helps teams discover project constraints **before** choosing a solution and plan efficient, evidence-based tests **before** implementation/testing.

It is not a standalone agent framework and does not, by itself, enforce permissions or guarantee that every agent invokes a skill. For consistent adoption, copy the Agent Operating Contract into the target project's root CLAUDE.md.

## What it solves

- Agents start implementation before checking assets, permissions, integrations or test infrastructure.
- Missing resources are silently replaced by inferior workarounds.
- Browser tests generate too many screenshots or use images instead of behavior assertions.
- Teams rerun broad suites repeatedly without diagnosing the first failure.
- Reports claim success without execution evidence or hide untested areas.

## Core skills

| Skill | Use it for | Main output |
|---|---|---|
| [Project Discovery](skills/project-discovery/SKILL.md) | New projects/features, redesigns, integrations, migrations, significant bug fixes | Readiness matrix, discovery summary, owner decisions, feasible options |
| [Efficient Testing](skills/efficient-testing/SKILL.md) | Test planning and execution for changed web/mobile behavior | Risk-based test plan, minimal test set, artifact budget, evidence-based report |

## Recommended reading order

1. [Vietnamese user guide](docs/USER_GUIDE_VI.md) — installation and end-to-end usage.
2. [Discovery and Testing Principles](docs/discovery-and-testing-principles.md) — required sequence and anti-patterns.
3. [Agent Operating Contract](docs/agent-operating-contract.md) — copy/adapt into the consuming project's CLAUDE.md.
4. [Readiness Matrix template](templates/READINESS_MATRIX_TEMPLATE.md).
5. [Risk-Based Test Plan template](templates/TEST_PLAN_TEMPLATE.md).

## Quick install

Copy the two skill folders to the target project's .claude/skills/ directory:

    target-project/
    ├── CLAUDE.md
    └── .claude/
        └── skills/
            ├── project-discovery/SKILL.md
            └── efficient-testing/SKILL.md

Also copy the templates into docs/agent-ops/templates/ and merge the Agent Operating Contract into the existing CLAUDE.md — do not overwrite project-specific instructions. See the [user guide](docs/USER_GUIDE_VI.md) for PowerShell/macOS/Linux commands and the full workflow.

Once installed, invoke /project-discovery and /efficient-testing or let Claude Code select them when appropriate. Confirm the current [Claude Code Skills documentation](https://code.claude.com/docs/en/skills) if the installed version behaves differently.

## Non-negotiable principles

- Inspect the actual repository, assets, integrations, permissions, environments and test resources before selecting an implementation.
- Do not infer that a credential/scope is available just because code references it.
- Treat UNKNOWN as unknown, not AVAILABLE.
- Escalate blockers and material trade-offs to the owner rather than silently adopting a degraded workaround.
- Prefer assertions and low-cost reliable test layers; screenshot budget is zero by default.
- AI-generated imagery is not evidence that a real application works.
- Report commands and actual outcomes; never mark untested behavior as passed.

## Version

Current documentation version: **1.2.1**. See [CHANGELOG.md](CHANGELOG.md).

## References

- Claude Code Skills: https://code.claude.com/docs/en/skills
- Claude Code Permissions: https://code.claude.com/docs/en/permissions
- Claude Code Hooks: https://code.claude.com/docs/en/hooks
- Playwright test options: https://playwright.dev/docs/api/class-testoptions
- Testing Library query priority: https://testing-library.com/docs/queries/about/
