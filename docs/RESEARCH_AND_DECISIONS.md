# Research and Design Decisions — Orcasus v2.4.0

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

### D13 — Pilot retro becomes checks, not grants (v2.4.0)
Rationale: the first real pilot (tbagri-web, 2026-10-29) failed its governance audit because rules existed only in prose. v2.4.0 adds machine checks where a check is possible (owner-only ASSUMPTION-ACCEPTED, dangling record paths) and written procedures elsewhere (subagent-mode debate, records before code, closeout before audit, hotfix lane). Two retro proposals asked for wider permissions: Bash for the security reviewer and reading `.env.example`. Both were replaced. Claude Code cannot restrict Bash to read-only commands, and deny rules win over allow rules, so an exception for `.env.example` needs a narrower deny glob that could expose other env files. Reviewers get an evidence pack instead, and discovery takes env var names from code. Evidence: [pilot record](../evidence/pilots/tbagri-web-2026-10-29.md), [EVIDENCE.md](EVIDENCE.md).

### D14 — Focus over breadth (v2.4.0)
- Decision state: DECIDED (owner, 2026-11-10; [approvals](agent-ops/APPROVALS.md)).
- Options considered:
  - (a) a formal admission rule with validator checks (chosen);
  - (b) a written principle only;
  - (c) no change.
- Rationale:
  - The owner holds that adding skills weakens the focus of the philosophy.
  - The measured cost agrees. Every skill description loads into every session.
  - Orcasus: 16 skills, 5,757 description characters before this change (about 1,400 tokens).
  - Aegis: 194 skills and 173,103 characters (about 43,000 tokens), a 990-edge routing graph, and a "Do NOT use" clause in 177 of the 194 descriptions ([measurement](../evidence/aegis-measurement-2026-11-10.md)).
- Decision:
  - Orcasus caps its core at 20 skills and 9,000 description characters.
  - Each skill needs a stage-map entry and a boundary clause.
  - Domain skills go in optional packs.
- Limits: a cap does not make a skill good; evals and the live scorecard still decide that.
- Revisit when a needed skill cannot fit without removing one, or when live evals show routing errors that the caps do not explain.
- Evidence: [intake record](agent-ops/INTAKE_RECORD.md), `scripts/skill_focus.py`.

### D15 — Judge auto-FAIL for trigger-failed attempts (v2.4.0)
- Decision state: DECIDED, then adjusted (owner, 2026-11-01: "dùng option 3"; adjusted 2026-11-11 by retro R11).
- Options considered:
  - (1) a cheaper judge model, which needs recalibration;
  - (2) one judge call per attempt, with a new rubric;
  - (3) no model call when the deterministic trigger check failed (chosen).
- Rationale: it saved about 40% of judge calls in the 2026-10-30 run.
- Known cost:
  - It can only lower scores.
  - It hid correct rule-following when the rules live in CLAUDE.md (run `run-20261110T224734Z-880ce5`).
  - Therefore cases marked `"trigger": "skill-or-rule"` are never auto-FAILed (R11).
- Revisit when calibration shows the judge is trusted on a cheaper model (option 1), or when auto-FAIL marks more than 10% of a run's assertions on cases whose behavior a human labels PASS.

### D12 — Attribution
The S0 classification gate, task slicing, closeout structure, governance audit controls and memory write/trust rules were adapted in Orcasus's own words from ideas in Project Aegis (https://github.com/ModernNomad-98/Project-Aegis, Apache License 2.0; reference copy haidongkixot/aegis-ref). No Aegis text or code was copied.

## Validation boundary
Static validation can confirm required files, metadata shape, settings JSON and policy text. It cannot prove actual teammate creation, peer messages, hook firing in every session, permission enforcement, application UX quality, cost or production readiness. See docs/ACCEPTANCE_TESTS.md.
