# Research and Design Decisions — Orcasus v2.3.0

## Research basis
This package combines the Agent Team architecture from the v2.1.0 distribution with the v1.3.0 discovery/testing gates. Core claims were checked against the official documentation linked below on 2026-10-29.

## Important official documentation
- Agent Teams: https://code.claude.com/docs/en/agent-teams
- Subagents: https://code.claude.com/docs/en/sub-agents
- Skills: https://code.claude.com/docs/en/skills
- Hooks: https://code.claude.com/docs/en/hooks
- Permissions: https://code.claude.com/docs/en/permissions
- Playwright TestOptions: https://playwright.dev/docs/api/class-testoptions
- Playwright test configuration: https://playwright.dev/docs/test-use-options

## Decisions
### D1 — Orcasus is a complete runtime package, not a skills-only library
Rationale: the reported problems originate from orchestration, agent prompts, test strategy, permissions, hooks, and documentation. Rules need consistent adoption across settings, the root operating constitution, role agents, skills, scripts and templates.

### D2 — Agent Teams enabled explicitly, but still treated as experimental
Rationale: this system is team-first and needs peer discussion, shared task coordination and direct messaging. Team size remains task-dependent because more teammates increase token and coordination cost. Runtime support must be verified in the selected Claude Code harness.

### D3 — Orchestrator-owned discovery gate
Rationale: agents should verify repository/assets/licences/integrations/access/environment/test resources before architecture or coding. Parallel discovery is read-only; implementation waits for consolidated readiness and owner decisions on material blockers.

### D4 — Screenshot, trace and video defaults are all zero
Rationale: screenshots are not a test oracle for behavior. Unit/API/component and semantic UI assertions are usually cheaper. Trace archives can themselves include screenshot and DOM snapshots. Captures require a named question, bounded budget, storage/retention and approval or pre-approved CI policy.

### D5 — Team Secretary records expressed evidence, not hidden reasoning
Rationale: observable messages, stated rationale, sources, objections, ballots and decisions form an auditable decision trail. Hidden chain-of-thought is neither requested nor recorded. Hook capture remains best-effort until runtime verified.

### D6 — Durable records survive interrupted team sessions
Keep PRD, readiness matrix, test plan, ADR, evidence, minutes, ballot register, action items and coverage report in the repository. In-memory chat and task state are not treated as durable source of truth.

### D7 — The system is an engineering scaffold, not a delivered ERP or mobile product
Use a modular architecture reference and premium UX bar as review standards, then build thin vertical slices. Do not start with overbuilt microservices or disconnected mock screens.

### D8 — Cover every AI SDLC stage, S0–S10 (v2.3.0)
Rationale: a stage-by-stage comparison against the 11-stage AI SDLC lifecycle showed gaps at S0 (classification, duplicate check), S3 (citation checks), S5 (slicing and prioritization), S9 (closeout, governance audit, retro) and S10 (knowledge linking, curator approval). v2.3.0 adds one skill per gap and maps every stage in [AI_SDLC_STAGE_MAP.md](AI_SDLC_STAGE_MAP.md). Each skill states what AI does, the fence and the human decision, so it prepares decisions without taking them.

### D9 — Citations and knowledge links are checked mechanically, content by people
Rationale: a script can prove that a cited file, line, meeting or commit exists and that statuses use the agreed vocabulary; it cannot prove the source supports the claim. `scripts/check_knowledge_links.py` runs in CI for the first part; the citation-check step in `requirements-traceability` and the human curator cover the second.

### D10 — Skill contracts and evals in CI
Rationale: the skill set grew to 16; without checks, names, descriptions, eval cases and the agent roster drift silently. Every skill carries trigger and behavior cases in `evals/evals.json`. CI validates their structure; live behavior is graded with the exported sheet from `scripts/skill_evals.py` because CI cannot run a model.

### D11 — Hooks never call a bare interpreter
Rationale: hooks called `python`. macOS and many Linux systems ship only `python3`, Windows may resolve a Store alias stub, and hook failures are non-blocking by design, so the meeting logger could fail without anyone noticing. All hooks now go through `scripts/hooks/run_python.sh`, which probes `$ORCASUS_PYTHON`, `python3`, `python` and `py -3` by running them. A SessionStart check reports the runtime, and a launch failure is written to `meetings/HOOK_ERRORS.log` and to stderr. Team messaging is still never blocked by the logger.

### D12 — Attribution
The S0 classification gate, task slicing, closeout structure, governance audit controls and memory write/trust rules were adapted in Orcasus's own words from ideas in Project Aegis (https://github.com/ModernNomad-98/Project-Aegis, Apache License 2.0; reference copy haidongkixot/aegis-ref). No Aegis text or code was copied.

## Validation boundary
Static validation can confirm required files, metadata shape, settings JSON and policy text. It cannot prove actual teammate creation, peer messages, hook firing in every session, permission enforcement, application UX quality, cost or production readiness. See docs/ACCEPTANCE_TESTS.md.
