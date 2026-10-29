# Evidence Status

What has been proven by running Orcasus for real, and what has not. Each row links to the evidence; a row without evidence is NOT RUN. Update this page whenever new evidence lands, and rerun before each release and at least monthly.

Last updated: 2026-10-29.

## Package checks (CI, no model calls)

| Check | Status | Evidence |
|---|---|---|
| Validator, skill eval files, logger, launcher and link-checker tests on Ubuntu, macOS, Windows (Git Bash) | PASS on PR #3 (2026-10-29) | GitHub Actions `validate` workflow on https://github.com/haidongkixot/orcasus/pull/3 |
| Hook launcher picks a working interpreter and the logger records an event end to end | PASS on Linux (python3 3.13), macOS, Windows (python3 3.12.10 via Git Bash) | same workflow, steps "Hook runtime check" and "End-to-end logger run" |
| SessionStart hook fires in a real Claude Code session | OBSERVED on Linux (2026-10-29) | [STATIC_VALIDATION_RESULTS.md](STATIC_VALIDATION_RESULTS.md) |

## Live skill behavior (local runs with `claude -p`)

Proposed thresholds, to be confirmed by the owner: trigger accuracy ≥ 0.90, assertion pass ≥ 0.85, safety checks 100%, at least 80% of assertions graded by a human or a trusted judge; PROVEN needs 3 repeats per case.

| Item | Status | Evidence |
|---|---|---|
| Smoke run (32 attempts) | NOT RUN | `python3 scripts/live_evals/run_live_evals.py --smoke --budget-total <USD>` |
| Full run (72 cases × 3) | NOT RUN | owner decides after the smoke run's measured cost |
| Judge calibration (≥ 30, target 60 human labels) | NOT RUN | `scripts/live_evals/calibrate.py` |
| Scorecard | NOT RUN | `reports/live-eval-scorecard.md` |
| SendMessage hook in headless mode | NOT RUN | `python3 scripts/live_evals/hook_probe.py` |

Until a skill reaches PROVEN in the scorecard, treat it as **EXPERIMENTAL**. Today that is all 16 skills.

## Agent Teams runtime (interactive)

| OS | Status | Evidence |
|---|---|---|
| macOS | NOT RUN | [RUNTIME_ACCEPTANCE_RUNBOOK.md](RUNTIME_ACCEPTANCE_RUNBOOK.md) |
| Windows (Git Bash) | NOT RUN | same |
| Linux | NOT RUN | same |

## Pilot (real project, S0–S10)

| Project | Status | Evidence |
|---|---|---|
| tbagri-web | NOT STARTED: owner to pick one small, low-risk feature | `evidence/pilots/tbagri-web-<date>.md` |

## Not proven by any of the above

- That a resolving citation supports its claim (people check content).
- Permission enforcement beyond Claude Code's own behavior, product UX quality, cost and production readiness.
