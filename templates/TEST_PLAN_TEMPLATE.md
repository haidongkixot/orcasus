# Risk-Based Test Plan — v2.2.0

Default budgets: screenshots 0, traces 0, videos 0. Non-zero capture requires a named question, bounded count, output path, retention policy and owner approval or pre-approved project CI policy.

## 1. Scope and acceptance criteria
- Feature/change:
- Owner:
- Risk: LOW / MEDIUM / HIGH / CRITICAL
- Primary user journeys:
- Supported browser/device/platform:
- Non-goals:
- Existing runner/config/version:
- Existing test runtime/artifact baseline:

## 2. Test selection matrix
| Criterion | Risk | Lowest-cost reliable layer | Concrete assertion | Existing fixture/service | Higher-cost test needed? Why? | Expected runtime | Status |
|---|---|---|---|---|---|---|---|
| | | Static / Unit / API / Integration / Component / E2E / Visual | | | | | NOT RUN |

Prefer static, unit, API/integration and component tests where they reliably prove the criterion. Use a small E2E set for journeys with cross-layer risk. Visual regression is an exception, not a default. Avoid duplicating identical assertions across layers unless they catch distinct defects.

## 3. Resource and permission readiness
| Resource | Required? | Status | Evidence | Impact if missing | Owner action/options |
|---|---|---|---|---|---|
| Browser/device/emulator | | UNKNOWN | | | |
| Credentials/scopes (never record secret values) | | UNKNOWN | | | |
| API/database/external service | | UNKNOWN | | | |
| Test data/fixtures | | UNKNOWN | | | |
| CI/preview/staging/network | | UNKNOWN | | | |
| Licensed assets/fonts/icons | | UNKNOWN | | | |
| Paid service/device farm/storage | | UNKNOWN | | | |

If required resource is missing or UNKNOWN, dependent tests are BLOCKED or NOT RUN. Do not replace it with an unapproved workaround that changes what is being validated.

## 4. Screenshot/trace/video authorization — all default zero
- Is capture necessary? YES / NO
- Exact visual/diagnostic question:
- Why assertions, API/DOM state, accessibility queries, logs or geometry are insufficient:
- Real app/page/state and criterion:
- Representative pages/states only:
- Viewports/devices/themes and reason:
- Maximum screenshot count:
- Maximum trace archive count; whether snapshots/screenshots are included:
- Maximum video count:
- Capture policy: NONE / TARGETED FAILURE / APPROVED VISUAL BASELINE
- Output directory:
- Retention and cleanup:
- Owner approval or approved CI policy:
- Expected runtime/storage impact:

If no named question and approved/non-zero budget exist, keep capture disabled. Do not generate fake screenshots. Trace archives may include visual snapshots and count toward the same artifact budget.

## 5. Execution order
1. Inspect existing test configuration and preserve user changes.
2. Run focused static checks.
3. Run tests for changed logic.
4. Run focused API/integration/component tests.
5. Run critical E2E journeys only where needed.
6. Run approved visual/regression checks only at the justified gate.
7. Record actual commands, exit codes and duration where available.

Do not run broad E2E/visual suites after every edit without evidence. Do not add a new test framework without a documented gap.

## 6. Failure and retry
- Preserve the first failure and minimal useful evidence.
- Diagnose code, test assumption, fixture, permission, service, environment, browser/device or flakiness before retry.
- Use a targeted retry and explain why.
- Do not weaken assertions, skip failures or update snapshots only to turn tests green.
- Stop repeated no-progress retries and report blocker/root cause.

## 7. Results
| Command/test | Exit code | Duration | PASS | FAIL | SKIPPED | BLOCKED | NOT RUN | Artifacts retained + reason/approval |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| | | | | | | | | |

## 8. Final report
- Criteria verified:
- Defects found/fixed:
- Unresolved defects:
- Actual commands and outcomes:
- Screenshot/trace/video counts, paths, reasons and approvals:
- Dependencies/config changes and justification:
- Coverage gaps/unverified resources:
- Plan deviations and approval:
- Verdict: PASS / FAIL / BLOCKED / NOT READY
