---
name: efficient-testing
description: Mandatory risk-based test planning for web/mobile changes. Inspect the existing runner and resources first, prefer the lowest-cost reliable behavioral test, and keep screenshot, trace and video artifacts disabled unless a named visual/diagnostic question has an approved budget.
---

# Efficient Testing — Cost and Evidence Gate (v1.3.0)

## Goal

Maximize defect detection and confidence per unit of runtime, token use, artifact storage and maintenance. Tests prove acceptance criteria; screenshots are not the default test oracle.

## 1. Hard defaults

- Default screenshot budget: ZERO.
- Default video budget: ZERO.
- Default trace budget: ZERO.
- Do not call image-generation tools/models to create synthetic screenshots, fake UI evidence or pictures to stand in for a real application test.
- Do not create screenshots for every screen, route, component, state, viewport, theme, test or iteration.
- Do not add a browser framework, mobile emulator, device farm, visual-regression package or new dependency until existing project resources have been inspected and a documented gap justifies the change.
- Do not enable screenshot, trace or video capture globally just because a browser test is being run.
- A test report must distinguish PASS, FAIL, BLOCKED, NOT RUN and SKIPPED. Creating a test or image is not proof that the feature works.

Any non-zero screenshot, trace or video budget must be stated in the test plan before execution. If no relevant visual/diagnostic question and budget are documented, keep capture disabled.

## 2. Inspect before designing tests

Read the current repository instructions, changed files, acceptance criteria, package manifest/scripts, installed test runner and versions, test configuration, fixtures, CI, past test failures and existing artifact paths. Reuse what exists unless a specific limitation is demonstrated.

Check readiness for required browsers/emulators, credentials and scopes, APIs, database, seed data, staging/preview, network, CI, licenses and paid services. Use Project Discovery when a prerequisite is missing or uncertain. Never expose secret values.

## 3. Map each acceptance criterion to the cheapest reliable test

Create or update docs/agent-ops/TEST_PLAN.md using the project template. For each criterion, record:
- Risk/impact and the failure mode to detect.
- The lowest-cost reliable test layer.
- The concrete assertion and fixture/service required.
- Why any more expensive layer is necessary and what additional failure mode it covers.
- Browser/device/platform coverage required by the supported-product scope.
- Expected runtime and artifact budget when available.

Prefer this sequence where it fits the architecture:

1. Static checks — formatting, lint, typecheck, schema/config validation.
2. Unit tests — business logic, validation, calculations, permission decisions and pure functions.
3. API/integration tests — contracts, authentication, persistence, migrations, service boundaries and error handling.
4. Component tests — states, keyboard interactions, accessible semantics and forms.
5. A small set of critical browser/mobile end-to-end journeys.
6. Visual regression only when explicit visual requirements or high-value layout changes justify it.

Do not duplicate the same assertion at several layers unless each catches a distinct class of defect. Prioritize authentication/authorization, data integrity, money/calculations, destructive actions, critical business flows and integrations by risk rather than visual prominence.

For UI behavior, prefer semantic assertions such as role/name/label, state, DOM content, API outcomes, keyboard behavior, accessibility checks, console/network errors and layout geometry where appropriate. Avoid brittle selectors and screenshot comparisons when behavioral assertions prove the requirement more cheaply.

## 4. Screenshot, trace and video rules

### 4.1 Default: capture nothing

Do not create or retain screenshot files for successful tests by default. Do not use generated images as test evidence. If a test only needs to prove that a button works, a record is saved, a permission is enforced or an API returns the correct result, use assertions—not a screenshot.

### 4.2 Allowed exceptions

A non-zero capture budget is allowed only when:
- a specific visual question is recorded (for example, clipping/overlap at a supported breakpoint, font loading, contrast, responsive layout or approved visual regression);
- semantic/behavioral assertions, API/DOM state, logs or geometry checks cannot adequately answer that question;
- the test plan lists representative pages/states, viewport/device/theme matrix, maximum artifact count, output path, retention/cleanup and reason for each artifact; and
- the owner or an existing project-approved CI policy authorizes that budget.

Failure diagnostics are not blanket permission to screenshot every failing case. First use error messages, assertion diffs, console/network logs and a focused reproduction. Only then request/consume a small, explicitly bounded screenshot/trace budget if images materially help.

A screenshot used for visual validation must come from the real running application or an explicitly authorized visual baseline capture. AI-generated mockups and image assets may be used for design exploration when separately requested, but never as proof that a real app renders or behaves correctly.

### 4.3 Playwright guidance, only if already installed

Playwright documents screenshot, trace and video capture as off by default. Keep them off for routine fast feedback, and verify the installed version and existing project config before changing anything.

For an existing Playwright project, the explicit baseline is:

    use: {
      screenshot: 'off',
      trace: 'off',
      video: 'off'
    }

For a focused, authorized diagnostic run only, selectively enable the minimum necessary evidence. Do not enable traces globally: traces can contain screenshots/screencasts and DOM snapshots for many actions. Count traces that embed visual snapshots against the artifact budget. Avoid recording every run.

Do not add Playwright if the project uses another supported test system. Do not edit test configuration blindly; first inspect current settings and explain material behavior changes in the test plan.

### 4.4 Artifact limits and retention

- Prefer no artifacts, then text logs/assertions, then a narrowly selected trace or screenshot only if the test plan justifies it.
- Bound the visual matrix to representative high-risk pages/states × supported breakpoints/themes; do not multiply every combination.
- Give each artifact run an output directory, maximum count, retention period and cleanup owner.
- Keep transient reports out of source control unless they are approved baselines.
- Never accept snapshots just to turn a failing test green; review the diff and record why it is correct.

## 5. Execute in small, risk-based slices

During implementation:
1. Run the smallest relevant test for the changed logic.
2. Run relevant lint/typecheck/build checks.
3. Run focused API/integration/component tests.
4. Run only critical E2E journeys required by feature risk.
5. Expand to broader regression/release checks at the agreed quality gate.
6. Record exact commands, exit codes, counts and duration if available.

Do not launch the full E2E or visual suite after every edit. Do not generate screenshots as progress updates. Use existing configuration; do not create duplicate test runners.

## 6. Diagnose before retrying

- Preserve the first failing assertion/log and only minimum necessary evidence.
- Classify the cause: code, test assumption, flaky timing, fixture/data, credential/scope, external service, browser/device, environment or resource exhaustion.
- Change one relevant cause at a time and run a targeted test.
- Do not repeatedly rerun the whole suite without diagnosis.
- Do not skip a test, loosen an assertion, update a snapshot or change requirements merely to get a green result.
- If essential access/environment is missing, mark the affected test BLOCKED or NOT RUN and return to Project Discovery and the owner-decision gate.
- Stop after repeated targeted failures and report the blocker instead of looping indefinitely.

## 7. Team coordination

The orchestrator must approve the test strategy and artifact budget before assigning expensive UI/visual test work. Delegate test-plan design before test execution. QA must explain why each browser/device/visual test is necessary. Developer must not independently add screenshot generation to prove implementation. Reviewer verifies test evidence, artifact counts and coverage gaps. Team Secretary records approved budget changes and reasons.

If a newly discovered constraint changes the selected test strategy, stop the affected activity, update the plan and ask the owner when the change affects cost, quality, supported platforms or confidence.

## 8. Evidence-based report

Report:
- Acceptance criteria tested and test layer used.
- Commands actually executed, exit codes and duration where available.
- PASS / FAIL / SKIPPED / BLOCKED / NOT RUN counts.
- Screenshot, trace, video and other artifact counts; retention path; reason and approval/budget for each non-zero class.
- First failures, root-cause analysis, targeted retries and remaining defects.
- Browser/device/integration/permission coverage and anything unverified.
- New dependency/configuration changes and why they were necessary.
- Deviations from the approved plan and who approved them.

Never claim a test passed unless execution evidence confirms it. Never call screenshot generation itself a test pass. Never represent a blocked or untested integration as working.
