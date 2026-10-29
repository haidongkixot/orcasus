# Risk-Based Test Plan — v1.3.0

> Default screenshot budget: 0. Default trace budget: 0. Default video budget: 0. Non-zero capture requires a named question, bounded budget and owner approval or pre-approved project policy.

## 1. Change and acceptance criteria

- Feature/change:
- Owner:
- Risk level: LOW / MEDIUM / HIGH / CRITICAL
- Primary user journeys:
- In-scope browsers/devices/platforms:
- Out of scope:
- Existing test runner/config/version:
- Current artifact count and runtime baseline, if available:

## 2. Test selection matrix

| Requirement / acceptance criterion | Risk | Lowest-cost reliable layer | Concrete assertion | Existing fixture/service | Higher-cost layer necessary? Why? | Expected runtime | Result |
|---|---|---|---|---|---|---|---|
| | | Static / Unit / API / Integration / Component / E2E / Visual | | | | | NOT RUN |

Choose the cheapest layer that credibly proves each criterion. Avoid repeating identical assertions across layers unless they cover distinct failure modes.

## 3. Resource and permission readiness

| Resource | Needed? | Status: AVAILABLE / MISSING / UNKNOWN / BLOCKED / NOT NEEDED | Evidence | Impact if missing | Owner action/options |
|---|---|---|---|---|---|
| Browser/device/emulator | | | | | |
| Credentials/scopes (never record secret values) | | | | | |
| API/database/third-party service | | | | | |
| Test data/fixtures | | | | | |
| CI/preview/staging/network | | | | | |
| Licensed assets/fonts/icons | | | | | |
| Paid service/device farm/artifact storage | | | | | |

If a required resource is missing or UNKNOWN, mark dependent tests BLOCKED or NOT RUN. Do not replace it with an unapproved mock/workaround that changes what is validated.

## 4. Screenshot/trace/video authorization — all default to zero

- Is visual or capture-based diagnosis necessary? YES / NO
- Exact question to answer:
- Why assertions, API/DOM state, accessibility queries, logs or geometry checks are insufficient:
- Real application/page and acceptance criterion:
- Representative pages/states only:
- Required viewports/devices/themes and reason:
- Maximum screenshots:
- Maximum trace archives and whether traces include screenshots/snapshots:
- Maximum videos:
- Capture policy: NONE / TARGETED FAILURE / APPROVED VISUAL BASELINE
- Output directory:
- Retention and cleanup:
- Approval or existing project policy:
- Expected runtime/storage cost:

If there is no named question and approved/non-zero budget, do not enable capture. Never use an image-generation model to create test screenshots or to prove app behavior. A screenshot used for visual verification must come from the real running application or an explicitly approved baseline workflow.

## 5. Execution sequence

1. Inspect existing test config and preserve the current user changes.
2. Run static checks relevant to the changed files.
3. Run unit tests for changed logic.
4. Run focused API/integration/component tests.
5. Run critical E2E journeys only where required.
6. Run visual/extended regression only if the approved plan justifies it.
7. Record commands, exit codes, duration and actual results.

Do not run full browser or visual suites after every edit by default. Do not install another test runner without documented need and required approval.

## 6. Failure and retry policy

- Preserve the first failure and minimal useful evidence.
- Diagnose code, test assumptions, fixtures, permissions, environment, service or flakiness before retry.
- Use a targeted retry; explain why it was necessary.
- Never blindly rerun broad suites, soften assertions, skip failures or update snapshots solely to obtain a green result.
- Stop after repeated targeted failures and report the blocker/root cause.

## 7. Results

| Command/test | Exit code | Duration | PASS | FAIL | SKIPPED | BLOCKED | NOT RUN | Artifacts retained + justification |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| | | | | | | | | |

## 8. Final report

- Acceptance criteria verified:
- Defects found/fixed:
- Unresolved defects:
- Commands and actual outcomes:
- Screenshot/trace/video counts, paths, reason and approval:
- Dependencies/config changes and justification:
- Coverage gaps and unverified permissions/integrations:
- Deviations from plan and authorization:
- Release recommendation: PASS / FAIL / BLOCKED / NOT READY
