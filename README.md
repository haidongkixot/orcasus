# Orcasus — Complete Claude Code Agent Team System v2.2.0

Orcasus is a complete, repository-integrated Agent Team System for complex web/mobile platform development. It is not just a collection of two skills. The package brings together runtime configuration, role agents, workflow skills, debate/voting, Team Secretary, hook-based event logging, discovery/test gates, templates, validation and setup documentation.

## What is included

| Layer | Contents |
|---|---|
| Runtime and governance | Root CLAUDE.md, .claude/settings.json, Agent Teams switch, permissions and logging hooks |
| Agent roles | 15 roles: product manager/analyst, domain architect, product designer, UX researcher, frontend/backend/mobile/integration/data engineers, QA, security reviewer, performance reviewer, devil's advocate and team secretary |
| Workflow skills | 9 skills: project discovery, efficient testing, team debate, meeting record, platform discovery, root-cause debate, vertical-slice delivery, design quality gate and delivery readiness |
| Recording | Meeting manifest, event logger, task lifecycle records, minutes, ballots, decisions, actions and coverage status |
| Quality resources | Readiness matrix, test plan, ADR, PRD, minutes and definition-of-done templates |
| Validation and documentation | Logger unit tests, bundle validator, acceptance tests, Vietnamese user guide, platform architecture, UX north star and research decisions |

## v2.2.0 operating principles

- For non-trivial tasks, the orchestrator must consolidate evidence from Project Discovery before delegating implementation. Parallel discovery is read-only until material readiness is known.
- Missing resources, assets, licences, permissions, integrations or owner decisions trigger a blocker and options—not a silent workaround.
- Screenshot, trace and video budgets default to zero. Non-zero capture requires a named question, bounded artifact count, destination/retention and owner approval or pre-approved CI policy.
- Use the lowest-cost reliable test layer, then a small critical E2E suite where justified.
- Material debate uses independent proposals, peer challenges, rebuttals, weighted comparison, explicit ballots and a durable ADR.
- Team Secretary records observable messages and expressed rationale; it does not request or record hidden chain-of-thought.
- Deployment, publishing, destructive production operations, paid infrastructure and external commitments remain approval-gated.

## Setup in VS Code

1. Open this repository root in VS Code and select the Claude harness/session target.
2. Install/authenticate Claude Code: https://code.claude.com/docs/en/setup
3. Review CLAUDE.md and .claude/settings.json. Agent Teams are experimental and explicitly enabled in this package.
4. Ensure Python 3 is available.
5. Run python scripts/test_meeting_logger.py and python scripts/validate_bundle.py.
6. Start a fresh interactive Claude Code session and follow INITIALIZE_AGENTS.md.
7. Run docs/ACCEPTANCE_TESTS.md in a non-production environment before relying on runtime hooks or automation.

Do not overlay this package blindly on an existing app repository. Merge settings carefully and preserve existing instructions, changes, assets and configured integrations.

## Recommended workflow

1. /project-discovery — readiness matrix and discovery summary.
2. /team-debate — only when material choices have competing viable options.
3. /efficient-testing — acceptance criteria mapped to the lowest-cost reliable test layer.
4. /vertical-slice-delivery — build one coherent end-to-end product slice.
5. /design-quality-gate and independent QA/security/performance reviews.
6. /delivery-readiness — evidence-based handoff and residual-risk report.

## Repository map

- CLAUDE.md: system-wide operating constitution.
- .claude/settings.json: team enablement, permissions and event hooks.
- .claude/agents/: all role definitions.
- .claude/skills/: all 9 runtime skills.
- skills/: root mirrors of the two reusable core library skills.
- scripts/: event logger, logger tests and complete bundle validator.
- meetings/: active meeting manifest and durable session folders.
- docs/: operating model, debate/recording policies, reference architecture, UX standards, acceptance tests, setup guide and research decisions.
- templates/: readiness matrix, test plan, ADR, PRD and minutes templates.
- decisions/, evidence/, projects/, reports/: durable project outputs.

## Important limitations

- Agent Teams are experimental, consume more tokens than a single session and have known coordination/resume/shutdown limitations.
- Configured hooks are not proof that hooks execute in every teammate session. Run the actual multi-teammate recording acceptance test.
- Permission rules and instructions reduce risk but are not a complete sandbox.
- This system is an engineering scaffold, not a prebuilt ERP or mobile application. Start with a thin vertical slice.
- Static validation cannot prove runtime team behavior, permission enforcement, UX quality, costs or production readiness.

## Documentation and sources

- Initialization: INITIALIZE_AGENTS.md
- Vietnamese user guide: docs/USER_GUIDE_VI.md
- Team operating model: docs/TEAM_OPERATING_MODEL.md
- Debate protocol: docs/DEBATE_PROTOCOL.md
- Meeting recording protocol: docs/MEETING_RECORDING_PROTOCOL.md
- Platform reference architecture: docs/PLATFORM_REFERENCE_ARCHITECTURE.md
- UX north star: docs/UX_NORTH_STAR.md
- Acceptance tests: docs/ACCEPTANCE_TESTS.md
- Static verification record: docs/STATIC_VALIDATION_RESULTS.md
- Official Agent Teams: https://code.claude.com/docs/en/agent-teams
- Official Skills: https://code.claude.com/docs/en/skills
- Official Hooks: https://code.claude.com/docs/en/hooks
- Official Permissions: https://code.claude.com/docs/en/permissions
- Playwright capture options: https://playwright.dev/docs/api/class-testoptions
