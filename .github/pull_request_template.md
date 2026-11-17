## Summary

<!-- What changed and why. Link the intake record if one exists. -->

## Checks

- [ ] `python3 scripts/validate_bundle.py`, the `scripts/test_*.py` tests and `python3 scripts/check_knowledge_links.py` pass locally
- [ ] If any `.claude/skills/*/SKILL.md` or `evals.json` changed: live evals for each changed skill were rerun locally (`python3 scripts/live_evals/run_live_evals.py --skill <name>`), and the evidence path is listed below
- [ ] If hooks, `.claude/settings.json` or `scripts/hooks/` changed: the runtime runbook (`docs/RUNTIME_ACCEPTANCE_RUNBOOK.md`) was rerun on at least one OS, or this PR says why not
- [ ] `docs/EVIDENCE.md` updated if new evidence was produced

## Evidence

<!-- Paths under evidence/ or reports/, CI links, and anything NOT RUN with the reason. -->

## Intentionally not done

<!-- Write "None." if empty. -->
