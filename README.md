# Orcasus — Agent Skills Library

Reusable Claude Code skills for disciplined web/mobile product engineering.

## Core skills

| Skill | Purpose |
|---|---|
| [Project Discovery](skills/project-discovery/SKILL.md) | Mandatory resource, asset, integration, environment and permission discovery before architecture or implementation. |
| [Efficient Testing](skills/efficient-testing/SKILL.md) | Risk-based testing with a strict screenshot budget and an evidence-based report. |

## Adoption guide

See [Discovery and Testing Principles](docs/discovery-and-testing-principles.md) for the recommended sequence, gates, and owner-decision rules.

For stronger enforcement inside a real product repository, also adopt the [Agent Operating Contract](docs/agent-operating-contract.md) in that repository's root `CLAUDE.md`, and start from the [Readiness Matrix template](templates/READINESS_MATRIX_TEMPLATE.md) and [Test Plan template](templates/TEST_PLAN_TEMPLATE.md). Skill installation alone does not guarantee every agent invokes the skills on every task; project-level orchestration instructions should make the discovery and test-planning gates explicit.

## Install in a project

Copy the chosen skill folder into the target project's `.claude/skills/` directory, for example:

```text
your-project/
└── .claude/
    └── skills/
        ├── project-discovery/
        │   └── SKILL.md
        └── efficient-testing/
            └── SKILL.md
```

Then invoke the skill using `/project-discovery` or `/efficient-testing`, or let Claude Code select it based on the description. Confirm the current [Claude Code Skills documentation](https://code.claude.com/docs/en/skills) if your installed version uses different configuration conventions.

## Design principles

- Inspect actual repository resources and constraints before selecting a solution.
- Surface blockers and owner decisions; never silently replace unavailable resources with inferior workarounds.
- Prefer behavioral tests at the cheapest reliable layer.
- Screenshots are not the default test oracle; capture only for justified visual checks or failures.
- Report evidence and executed commands. Never mark untested behavior as passed.
