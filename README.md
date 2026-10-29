# Orcasus — Complete Claude Code Agent Team System v2.3.0

Orcasus is a complete, repository-integrated Agent Team System for complex web/mobile platform development. It is not just a collection of two skills. The package brings together runtime configuration, role agents, workflow skills, debate/voting, Team Secretary, hook-based event logging, discovery/test gates, templates, validation and setup documentation.

## What is included

| Layer | Contents |
|---|---|
| Runtime and governance | Root CLAUDE.md, .claude/settings.json, Agent Teams switch, permissions, logging hooks through a portable Python launcher and a session-start runtime check |
| Agent roles | 17 roles: product manager/analyst, domain architect, product designer, UX researcher, frontend/backend/mobile/integration/data engineers, QA, security reviewer, performance reviewer, devil's advocate, team secretary, governance auditor and knowledge steward |
| Workflow skills | 16 skills covering S0–S10: change intake, project discovery, platform discovery, requirements traceability, team debate, meeting record, backlog slicing, efficient testing, vertical-slice delivery, root-cause debate, design quality gate, delivery readiness, closeout report, governance audit, process retro and knowledge curation — each with eval cases |
| Recording | Meeting manifest, event logger, task lifecycle records, minutes, ballots, decisions, actions and coverage status |
| Quality resources | Intake record, readiness matrix, trace matrix, backlog, test plan, ADR, PRD, minutes, closeout, governance audit, retro and definition-of-done templates; curated knowledge index |
| Validation and documentation | Bundle validator, skill eval validation and grading sheet, knowledge/citation link checker, logger/launcher/link-checker tests, GitHub Actions CI, AI SDLC stage map, acceptance tests, Vietnamese user guide, platform architecture, UX north star and research decisions |

## v2.3.0 operating principles

- Every new request starts with intake: change class, duplicate/conflict check, owner-confirmed intent and value, and a scope contract that forces reclassification when work grows.
- For non-trivial tasks, the orchestrator must consolidate evidence from Project Discovery before delegating implementation. Parallel discovery is read-only until material readiness is known.
- Missing resources, assets, licences, permissions, integrations or owner decisions trigger a blocker and options—not a silent workaround.
- Screenshot, trace and video budgets default to zero. Non-zero capture requires a named question, bounded artifact count, destination/retention and owner approval or pre-approved CI policy.
- Use the lowest-cost reliable test layer, then a small critical E2E suite where justified.
- Material debate uses independent proposals, peer challenges, rebuttals, weighted comparison, explicit ballots and a durable ADR.
- Team Secretary records observable messages and expressed rationale; it does not request or record hidden chain-of-thought.
- Requirements cite their sources and each citation is checked; uncited or mismatched requirements are owner questions.
- Every slice is testable before it is built; the owner sets priority.
- Every task ends with a closeout; independent governance audits and retros propose process changes for owner approval.
- Durable knowledge is linked, dated and secret-free, and only a human curator approves it.
- Deployment, publishing, destructive production operations, paid infrastructure and external commitments remain approval-gated.

## Setup in VS Code

1. Open this repository root in VS Code and select the Claude harness/session target.
2. Install/authenticate Claude Code: https://code.claude.com/docs/en/setup
3. Review CLAUDE.md and .claude/settings.json. Agent Teams are experimental and explicitly enabled in this package.
4. Ensure Python 3.8+ is available (`python3`, `python` or `py -3`). If it lives elsewhere, set `ORCASUS_PYTHON` to its path. On Windows, hooks need Git Bash.
5. Run `python3 scripts/validate_bundle.py`, the tests in `scripts/test_*.py` and `python3 scripts/check_knowledge_links.py`. CI runs the same checks on every pull request.
6. Start a fresh interactive Claude Code session, check that the session-start line reads "Orcasus hook runtime: OK", and follow INITIALIZE_AGENTS.md.
7. Run docs/ACCEPTANCE_TESTS.md in a non-production environment before relying on runtime hooks or automation.

Do not overlay this package blindly on an existing app repository. Merge settings carefully and preserve existing instructions, changes, assets and configured integrations.

## Recommended workflow

Full stage map: [docs/AI_SDLC_STAGE_MAP.md](docs/AI_SDLC_STAGE_MAP.md).

1. /change-intake — classify, check duplicates, confirm intent and value, declare scope (S0).
2. /project-discovery — readiness matrix and discovery summary (S1).
3. /platform-discovery and /requirements-traceability — brief, cited requirements, checked citations (S2–S3).
4. /team-debate — only when material choices have competing viable options (S4).
5. /backlog-slicing — testable slices and a prioritization proposal for the owner (S5).
6. /efficient-testing — acceptance criteria mapped to the lowest-cost reliable test layer (S6–S8).
7. /vertical-slice-delivery — build one coherent end-to-end product slice (S7).
8. /design-quality-gate, independent QA/security/performance reviews and /delivery-readiness (S8).
9. /closeout-report, /governance-audit and /process-retro (S9).
10. /knowledge-curation — linked knowledge approved by a human curator (S10).

## Repository map

- CLAUDE.md: system-wide operating constitution.
- .claude/settings.json: team enablement, permissions, session-start runtime check and event hooks.
- .claude/agents/: all role definitions.
- .claude/skills/: all 16 runtime skills, each with evals/evals.json.
- skills/: root mirrors of the two reusable core library skills.
- scripts/: event logger, portable hook launcher (scripts/hooks/run_python.sh), knowledge/citation link checker, skill eval tooling, unit tests and complete bundle validator.
- .github/workflows/validate.yml: CI for all package checks on Ubuntu and macOS.
- knowledge/: curated knowledge index with tracked sources and curator approval.
- meetings/: active meeting manifest and durable session folders.
- docs/: operating model, debate/recording policies, reference architecture, UX standards, acceptance tests, setup guide and research decisions.
- templates/: intake, readiness, trace matrix, backlog, test plan, closeout, governance audit and retro templates (ADR, PRD and minutes templates live in docs/).
- decisions/, evidence/, projects/, reports/: durable project outputs.

## Important limitations

- Agent Teams are experimental, consume more tokens than a single session and have known coordination/resume/shutdown limitations.
- Configured hooks are not proof that hooks execute in every teammate session. Run the actual multi-teammate recording acceptance test.
- CI checks file contracts, eval structure, links and scripts; it does not run a model. Live skill evals run locally with `scripts/live_evals/` (see docs/EVIDENCE.md); until a skill is PROVEN there, treat it as experimental.
- A resolving citation proves the source exists, not that it supports the claim; people check content.
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
- AI SDLC stage map: docs/AI_SDLC_STAGE_MAP.md
- Evidence status (what real runs have proven): docs/EVIDENCE.md
- Runtime acceptance runbook: docs/RUNTIME_ACCEPTANCE_RUNBOOK.md
- Research decisions and attribution: docs/RESEARCH_AND_DECISIONS.md
- Official Agent Teams: https://code.claude.com/docs/en/agent-teams
- Official Skills: https://code.claude.com/docs/en/skills
- Official Hooks: https://code.claude.com/docs/en/hooks
- Official Permissions: https://code.claude.com/docs/en/permissions
- Playwright capture options: https://playwright.dev/docs/api/class-testoptions
