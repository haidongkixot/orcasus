# Initialize Orcasus v2.3.0

## Before starting
1. Open this repository root in VS Code and select the Claude harness.
2. Install/authenticate Claude Code using https://code.claude.com/docs/en/setup.
3. Read CLAUDE.md, .claude/settings.json, and docs/TEAM_OPERATING_MODEL.md.
4. Run the package checks with Python 3.8+ (`python3` on macOS/Linux, `py -3` on Windows):
   - `python3 scripts/validate_bundle.py`
   - `python3 scripts/test_meeting_logger.py`, `python3 scripts/test_hook_launcher.py`, `python3 scripts/test_knowledge_links.py`
   - `python3 scripts/check_knowledge_links.py`
   - `sh scripts/hooks/run_python.sh --check` (Windows: run in Git Bash)
5. Start a new interactive Claude Code session. Confirm the SessionStart line reads "Orcasus hook runtime: OK" and whether Agent Teams and peer messaging actually work in this environment.

## Initialization prompt

Initialize this workspace as the complete Orcasus Agent Team System v2.3.0. Do not implement a feature yet. Read CLAUDE.md, README.md, the AI SDLC stage map, the team operating model, debate protocol, meeting recording protocol, platform reference architecture, UX North Star, and acceptance tests. Inspect every configured agent, skill, permission rule, and hook. Run the validation scripts and report actual exit codes. Distinguish static configuration from runtime proof. Check Team Secretary capture with two or more real teammates if the runtime supports teams. Do not claim a hook worked merely because it is configured. Explain the intake gate, the mandatory discovery gate, requirement citation checks, backlog slicing, owner decision process, debate/voting, zero-capture test policy, release readiness gate, closeout/audit/retro and knowledge curation. Report any gaps, then stop before implementation.

## First exercise

Run a non-production discovery and architecture debate for a future enterprise work-management platform with possible ERP and mobile capabilities. Start Team Secretary and 4–5 relevant teammates. Complete readiness matrix and discovery summary before deciding architecture. Have participants make independent proposals, challenge one another, rebut with evidence, score options, and send explicit final ballots. Keep screenshot/trace/video budgets at zero. Save PRD, capability map, roadmap, ADR, meeting minutes, vote register, action list and coverage report. Do not install packages or connect paid services. If Agent Teams or messaging is unavailable, report that limitation rather than simulating a successful team.

## Build prompt (only after owner review)

Implement only the approved vertical slice from the backlog. Complete the intake record, Project Discovery and the test plan first, and stay inside the intake scope contract. Keep screenshot, trace and video capture disabled unless a named visual/diagnostic question, bounded artifact count, retention policy and approval exist. Use real approved assets and integrations; if access or resources are missing, stop dependent work and ask the owner with feasible options. Assign explicit file/module ownership, run focused tests, request independent reviews, report actual results and write the closeout report. Do not deploy or publish.
