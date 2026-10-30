# Evidence Status

What has been proven by running Orcasus for real, and what has not. Each row links to the evidence; a row without evidence is NOT RUN. Update this page whenever new evidence lands, and rerun before each release and at least monthly.

Last updated: 2026-10-30 (first live smoke run on the 8 skills changed in v2.4.0).

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
| Smoke run, 8 skills changed in v2.4.0 (16 attempts, Linux cloud container, Claude Code 2.1.314, default model) | RAN 2026-10-30: trigger 12/16; deterministic checks 38/40, both failures `files_created` on a trigger FAIL; safety checks 36/36; judge (uncalibrated) 18 PASS / 22 FAIL of 40 assertions; spend $3.97 run + $1.67 judge | [run](../evidence/live-evals/run-20261030T154250Z-d8fc2f/run.json), [scorecard](../reports/live-eval-scorecard.md), [findings](../reports/v2.4-closeout.md#live-eval-smoke-run-2026-10-30) |
| First smoke attempt (stopped after 2 attempts) | STOPPED: harness copied Orcasus's own records into the workspace and flagged an env reference as a secret; both fixed in `f27550e` | [stopped run](../evidence/live-evals/run-20261030T154015Z-752394/STOPPED.md) |
| Smoke run, other 8 skills | NOT RUN | `python3 scripts/live_evals/run_live_evals.py --smoke --budget-total <USD>` |
| Full run (78 cases × 3) | NOT RUN | owner decides after the smoke run's measured cost |
| Judge calibration (≥ 30, target 60 human labels) | WAITING FOR OWNER: 40 items sampled, human labels empty | [labels sheet](../evidence/live-evals/calibration/2026-10-30-labels.csv), then `calibrate.py score` |
| Scorecard | RAN 2026-10-30: every skill INSUFFICIENT EVIDENCE (1 attempt per case, judge not calibrated, 0 human labels) | [scorecard](../reports/live-eval-scorecard.md) |
| SendMessage hook in headless mode | NOT RUN | `python3 scripts/live_evals/hook_probe.py` |

Until a skill reaches PROVEN in the scorecard, treat it as **EXPERIMENTAL**. Today that is all 16 skills.

v2.4.0 changed the `SKILL.md` or `evals.json` of 8 skills: change-intake, closeout-report, efficient-testing, governance-audit, project-discovery, requirements-traceability, team-debate and vertical-slice-delivery, plus the security-reviewer agent. Under the regression rule their live evals must run before merge. The smoke run on 2026-10-30 covered one trigger and one non-trigger case per skill. It did **not** reach the new v2.4 cases (P1, P2, P3, P4, P7, P9), because smoke takes the first cases of each file. Those cases still need a targeted run (`--case <id>`).

## Agent Teams runtime (interactive)

| OS | Status | Evidence |
|---|---|---|
| macOS | NOT RUN | [RUNTIME_ACCEPTANCE_RUNBOOK.md](RUNTIME_ACCEPTANCE_RUNBOOK.md) |
| Windows (Git Bash) | NOT RUN | same |
| Linux | NOT RUN | same |

## Pilot (real project, S0–S10)

| Project | Status | Evidence |
|---|---|---|
| tbagri-web (security hotfix, production) | RAN 2026-10-29: 11/11 stage records; 31 tests; independent security review APPROVE WITH CHANGES; governance audit **FAIL** (record fixes applied); PR open, not merged or deployed | [evidence/pilots/tbagri-web-2026-10-29.md](../evidence/pilots/tbagri-web-2026-10-29.md) |

## Retro dispositions (tbagri-web pilot, v2.4.0)

Owner approved the plan on 2026-10-30. "Checked" means a machine check exists; "written" means a rule or procedure with an eval case, not yet proven by a live run.

| ID | Retro proposal | Disposition | Enforcement | Evidence |
|---|---|---|---|---|
| P1 | Only the owner sets ASSUMPTION-ACCEPTED | ADOPTED | Checked: `check_knowledge_links.py` fails rows without `accepted by owner: <name> date` or with an agent's name | `test_assumption_accepted_needs_human_owner`; pilot reproduction fails R6 |
| P2 | Subagent-mode debate | ADOPTED | Written: team-debate, DEBATE_PROTOCOL, ADR template | eval `team-debate/edge-no-agent-teams` |
| P3 | List domain values before policy questions | ADOPTED | Written: change-intake, intake template | eval `change-intake/edge-policy-question-lists-domain-values` |
| P4 | Records before code; saved reviews; closeout before audit | ADOPTED | Partly checked: missing record paths warn (`test_dangling_record_path_warns`); gate order is an audit control read from git | evals `governance-audit/edge-gate-order-and-missing-closeout`, `closeout-report/edge-closeout-before-audit` |
| P5 | Read-only Bash for security-reviewer | REPLACED: evidence pack, no tool grant | Written: security-reviewer agent, vertical-slice-delivery | Bash cannot be limited to read-only (D13) |
| P6 | Allow reading `.env.example` | REPLACED: env var names from code; deny rules unchanged | Written: project-discovery, readiness template | Deny wins over allow (D13) |
| P7 | Exact statuses on allowed paths | ADOPTED | Written: efficient-testing, test plan template | eval `efficient-testing/edge-vacuous-allowed-path` |
| P8 | Draft PR before review | ADOPTED | Written: user guide, operating model, CLAUDE.md | — |
| P9 | Hotfix lane (from the post-pilot evaluation) | ADOPTED | Written: change-intake, CLAUDE.md, stage map; audit gate-order control | eval `change-intake/edge-hotfix-lane` |

## Not proven by any of the above

- That a resolving citation supports its claim (people check content).
- Permission enforcement beyond Claude Code's own behavior, product UX quality, cost and production readiness.
