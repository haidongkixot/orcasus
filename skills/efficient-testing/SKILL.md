---
name: efficient-testing
description: Mandatory risk-based testing for web/mobile changes. Prefer the lowest-cost reliable behavioral test; screenshot, trace and video artifacts default to zero unless a named question, bounded budget and approval exist.
---

# Efficient Testing — Zero-Capture Defaults v1.3.0

## Hard defaults
- Screenshot budget = 0.
- Trace budget = 0.
- Video budget = 0.
- Do not use image-generation tools to synthesize screenshots or prove app behavior.
- Do not capture every page, route, component, state, viewport, theme or run.
- Do not add a browser framework, device farm, visual-regression package or major dependency until existing resources are inspected and a documented gap justifies it.
- Any non-zero capture budget requires a named diagnostic/visual question, bounded artifact count, destination, retention/cleanup and owner approval or a pre-approved project CI policy.

## Inspect before designing tests
Read requirements/acceptance criteria, changed files, current test runner/config/version, package scripts, fixtures, CI, prior failures and existing artifact paths. Verify browser/device access, API, database, test data, preview/staging, network and budget. Reuse existing tools.

## Test pyramid
Map each acceptance criterion to the cheapest reliable layer:
1. Static — format/lint/type/schema/config.
2. Unit — rules, validation, permissions, calculation, state.
3. API/integration — contracts, persistence, auth, migrations, service failures.
4. Component — interactive states, keyboard, semantics/accessibility.
5. Small critical browser/mobile E2E set.
6. Visual regression only when explicit visual requirements or a high-risk layout change justify it.

Prefer semantic role/name/label assertions, API responses, DOM state, accessibility, console/network errors and geometry where appropriate. Avoid brittle selectors and screenshots when behavioral assertions prove the requirement more cheaply. Don't duplicate identical assertions across layers unless they cover distinct failure modes.

## Capture policy
Default to no image/video/trace capture. Traces can contain screenshots, screencasts and DOM snapshots; count them as artifacts. Start with assertions and concise text logs. For an approved visual check, record exact question, representative states/pages, viewport/device/theme, maximum screenshot/trace/video counts, output directory, cleanup/retention, and expected cost. Use real running application captures or approved baselines, never AI-generated screenshots as evidence.

If Playwright is already in use, keep use.screenshot, use.trace and use.video explicitly set to off for routine development. Inspect existing config/version first. Do not install Playwright merely because it is mentioned here. For narrow diagnostics, enable only the necessary capture with a bounded selection and plan.

## Run incrementally
Run focused tests for changed logic, relevant lint/typecheck/build, focused API/integration/component tests, and then only critical E2E required by risk. Expand to full regression/release suites at agreed gates, not after every edit.

## Failure policy
Preserve first failure and minimal evidence. Classify cause (code, test assumption, fixture, permission, service, environment, browser/device, flake, resource exhaustion) before retrying. Run targeted retry. Never weaken assertions, skip failures, or update snapshots only to get green. If access/resource is missing, mark BLOCKED or NOT RUN and return to Project Discovery/owner decision. Stop repeated no-progress retries and report blocker.

## Team coordination and report
Orchestrator approves test strategy/capture budget before expensive UI work. QA explains why each higher-cost test is necessary. Developer cannot independently add screenshots to prove a feature works. Reviewer checks actual test outputs, capture counts and coverage gaps. Secretary records approved deviations.

Report criteria tested, actual commands/exit codes/durations, PASS/FAIL/SKIPPED/BLOCKED/NOT RUN counts, artifact counts/retention/reasons, root causes/retries, unverified resources/platforms, new dependencies and deviations. Never call unrun tests PASS.
