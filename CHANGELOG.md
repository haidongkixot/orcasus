# Changelog

## 2.4.0 — Pilot-driven process checks
Changes from the tbagri-web pilot retro (P1–P9). Dispositions are in docs/EVIDENCE.md.
- Only the owner may set ASSUMPTION-ACCEPTED; check_knowledge_links.py fails a trace-matrix row without `accepted by owner: <name> YYYY-MM-DD` or with an agent's name (P1).
- team-debate subagent mode when Agent Teams are unavailable: at least 4 voters including devil-advocate, voter-scored matrix, one rebuttal round, verbatim ballots in decisions/, capture NOT VERIFIED (P2).
- change-intake lists every domain value (roles, statuses, tenants) from code before a policy question (P3).
- Intake and readiness records are committed before code; reviews are saved in reports/; the closeout exists before the audit; governance-audit has a gate-order control; the checker warns about record paths that do not exist (P4).
- security-reviewer receives an evidence pack instead of a shell grant (P5). project-discovery takes env var names from code; the .env deny rules are unchanged (P6).
- efficient-testing requires exact results on allowed paths; "not 401/403" is called out as vacuous (P7).
- Pull requests open as drafts until reviews, closeout and audit exist (P8).
- Owner-confirmed hotfix lane: same gates, records completed before the pull request leaves draft or merges (P9).
- 6 new eval cases and 1 rewritten (16 skills, 78 cases); 2 new checker tests.
- Live evals: the first smoke run on the 8 changed skills (evidence in docs/EVIDENCE.md). Harness fixes: Orcasus's own records are kept out of the eval workspace; env references and redaction markers are not secrets; the judge loads no user-level settings. The judge no longer calls the model for assertions of attempts whose trigger check failed: they are marked FAIL as `auto:trigger-fail` and are never sampled for calibration.

### Live evidence tooling (shipped in the same pull request)
- Added a live skill eval pipeline run locally with `claude -p`: sample-app fixture with deliberate traps, deterministic checks per case (`checks` in evals.json), LLM judge whose PASS must quote real evidence, calibration against human labels (trusted only at ≥ 80% agreement, ≤ 5% false-PASS), and a per-skill scorecard. Tests use a fake `claude`, so CI makes no model calls.
- Added a headless SendMessage hook probe, the Agent Teams runtime acceptance runbook and an evidence collector that computes capture coverage.
- Added docs/EVIDENCE.md (what real runs have proven; all skills EXPERIMENTAL until PROVEN) and a pull request template with the skill-eval regression rule.

## 2.3.0 — Full S0–S10 Lifecycle Coverage, Skill CI and Portable Hooks
- Added 7 skills: change-intake (S0), requirements-traceability (S3), backlog-slicing (S5), closeout-report, governance-audit and process-retro (S9), knowledge-curation (S10). The package now has 16 skills.
- Added 2 agents: governance-auditor (independent, read-only) and knowledge-steward (prepares entries, never approves). The package now has 17 agents.
- Added templates for intake records, trace matrices, backlogs, closeouts, governance audits and retros, plus a curated knowledge/INDEX.md with human curator approval.
- Added docs/AI_SDLC_STAGE_MAP.md mapping each stage to its owning skill, agents, fence, human decision and evidence.
- Added eval cases for all 16 skills, scripts/skill_evals.py (validation and live grading sheet), scripts/check_knowledge_links.py (knowledge index, trace-matrix citations, documentation links) and a GitHub Actions workflow running all checks on Ubuntu and macOS.
- Fixed silent meeting-logger failure on machines without a `python` command: hooks now run through scripts/hooks/run_python.sh, a SessionStart hook reports the runtime, and launch failures go to meetings/HOOK_ERRORS.log, which caps meeting capture at PARTIAL.
- Added .gitattributes forcing LF line endings so the hook launcher and skill frontmatter survive Windows checkouts; CI now also runs on Windows (Git Bash) with an end-to-end logger run through the launcher on all three OSes.
- validate_bundle.py now checks exact skill and agent sets, name/file matches, description length, eval files and hook portability instead of fixed counts.
- Updated CLAUDE.md, the operating model, Definition of Done, acceptance tests, meeting protocol, product/QA/secretary agents and the user guides.

## 2.2.0 — Whole-System Integration
- Integrated the full Agent Team runtime: 15 agents, 9 skills, settings, hooks, meeting logger, templates, scripts and setup documentation.
- Applied mandatory preflight discovery and zero screenshot/trace/video defaults across roles, skills, orchestration and QA.
- Added explicit owner decision gates for missing resources, permissions and material trade-offs.
- Added whole-system initialization and runtime acceptance tests.

## 1.3.0 — Discovery and Efficient Testing
- Added orchestrator-owned readiness checks, owner escalation for blockers, risk-based tests and zero-capture defaults.
