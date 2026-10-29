# Static Validation Results — Orcasus v2.3.0

Validation date: 2026-10-29
Environment: Linux container, Python 3.13.17, local checkout of the v2.3.0 working tree (base commit `db4a8eb`).

## Commands executed

| Command | Exit code | Result |
|---|---:|---|
| `python3 scripts/validate_bundle.py` | 0 | 115 passed, 0 failed |
| `python3 scripts/skill_evals.py validate` | 0 | 16 skills, 72 eval cases, 0 failed |
| `python3 scripts/test_meeting_logger.py` | 0 | 5 tests OK |
| `python3 scripts/test_hook_launcher.py` | 0 | 7 tests OK |
| `python3 scripts/test_knowledge_links.py` | 0 | 8 tests OK |
| `python3 scripts/check_knowledge_links.py` | 0 | 3 passed, 0 warnings, 0 failed |
| `sh scripts/hooks/run_python.sh --check` | 0 | "Orcasus hook runtime: OK (python3, Python 3.13.17)" |

The v2.2.0 scripts, which were not executed when v2.2.0 was published, were also run before the upgrade on the v2.2.0 tree: `test_meeting_logger.py` 5 tests OK, `validate_bundle.py` 58 passed, 0 failed.

## What these checks establish

- Exactly the 17 expected agents and 16 expected skills exist; each name matches its file or directory; skill descriptions are within 1024 characters.
- Every skill has a structurally valid `evals/evals.json` with trigger and non-trigger cases.
- Every hook in `.claude/settings.json` calls Python through `scripts/hooks/run_python.sh`; a SessionStart hook runs the runtime check.
- The launcher runs the logger with `python3`, falls back to `python`, skips a non-Python stub, honors `ORCASUS_PYTHON`, and without an interpreter exits 1, warns on stderr and writes `meetings/HOOK_ERRORS.log`.
- The knowledge index and trace-matrix rules reject broken links, out-of-range line anchors, unknown meeting IDs, missing sources, secret-like values, missing curator approvals and uncited approved requirements.
- Root library copies of `project-discovery` and `efficient-testing` still match their runtime copies.

## Runtime observation

In the Claude Code session that built v2.3.0, the configured SessionStart hook fired on session resume and printed "Orcasus hook runtime: OK (python3, Python 3.13.17). Meeting logger hooks can run." This confirms the shell-form launcher command and `${CLAUDE_PROJECT_DIR}` expansion on Linux. It was not observed on macOS or Windows.

## Not run / not proven

- The GitHub Actions workflow had not run when this record was written; check the `validate` workflow result on the pull request.
- Agent Teams creation, peer messaging, logger hooks firing inside real teammate sessions and meeting coverage reconciliation were not tested at runtime.
- Live skill behavior (whether agents pick the right skill and meet the eval assertions) was not measured; use `python3 scripts/skill_evals.py sheet`.
- Windows behavior of the launcher (Git Bash) was not tested.
- Permission enforcement, product UX, performance, cost and production readiness are not proven by static validation.

## Required runtime checks

Use INITIALIZE_AGENTS.md and docs/ACCEPTANCE_TESTS.md, including section H (hook runtime portability) and the live multi-teammate logger test before reporting CAPTURE VERIFIED.
