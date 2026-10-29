# Discovery and Testing Principles — v1.3.0

This guide defines the gates for web/mobile work using Orcasus with Claude Code.

## Required sequence

1. Inspect the actual repository and current work.
2. Inventory existing assets/licences, components, integrations, permissions/scopes, credential availability, environments, test tools and budget.
3. Complete an evidence-backed readiness matrix.
4. Escalate blockers and material trade-offs to the owner; never silently invent a workaround.
5. Compare feasible solution options and record significant decisions.
6. Map acceptance criteria to a risk-based test plan before implementation.
7. Implement small, testable slices using approved resources.
8. Execute the cheapest reliable tests first and broaden only when risk/release criteria justify it.
9. Report actual evidence and clearly mark unverified areas.

## Mandatory anti-patterns

- Starting architecture/implementation while a material prerequisite is UNKNOWN.
- Delegating coding tasks before the orchestrator consolidates discovery.
- Pretending a credential, permission, asset, API or environment is available.
- Replacing a required production integration with a fake implementation without approval.
- Generating images to serve as screenshots or evidence that the real app works.
- Creating screenshots for every page, state, test, viewport or run by default.
- Enabling screenshot/trace/video capture globally without a named question and artifact budget.
- Adding new test frameworks/dependencies before inspecting existing project capabilities.
- Re-running broad suites without diagnosing the first failure.
- Marking blocked, untested or assumed behavior as passed.

## Owner-decision protocol

Ask the owner only for decisions not resolvable from the repository or reliable evidence. For each blocker/material trade-off, present feasible options, cost/time impact, quality/security/data-fidelity implications, reversibility and a recommendation. Continue independent, reversible work that does not encode the unresolved choice.

## Screenshot/trace/video policy

Default budgets are:
- Screenshots: 0.
- Videos: 0.
- Traces: 0.

Use semantic/behavioral assertions, API outcomes, DOM state, accessibility queries, console/network logs and layout geometry first. For actual visual-regression needs, use the real application render and an approved baseline—not AI-generated imagery.

Before any non-zero capture, record the exact question, representative test/page/state, viewport/device/theme matrix, maximum artifact count, output path, retention/cleanup and approval or approved project policy. Count screenshots embedded in trace archives as visual artifacts. Do not capture all combinations by default.

If Playwright is already used, keep screenshot, trace and video explicitly off in routine fast-feedback runs. Enable a narrow diagnostic configuration only if the question and artifact budget have been approved. Verify the installed Playwright version and existing config before changing settings.

## Testing economics

- Prefer static/unit/API/component tests when they reliably prove the acceptance criterion.
- Keep browser/mobile E2E coverage to critical end-to-end journeys and platform risks.
- Do not duplicate assertions across layers unless they catch distinct failure modes.
- Run targeted tests during development; run broader regression tests at agreed release gates.
- Diagnose failure causes before retrying; record retries and flakiness.
- Report runtime and artifact count when available so the team can improve confidence per cost.

## Status vocabulary

- PASS: execution evidence verifies the criterion.
- FAIL: a confirmed criterion did not pass.
- BLOCKED: a required resource or decision is unavailable.
- NOT RUN: no verification was executed.
- SKIPPED: intentionally not executed under a documented policy.

Never report NOT RUN, BLOCKED or assumed behavior as PASS.

## References

- Claude Code Skills: https://code.claude.com/docs/en/skills
- Claude Code Permissions: https://code.claude.com/docs/en/permissions
- Claude Code Hooks: https://code.claude.com/docs/en/hooks
- Playwright test options and capture behavior: https://playwright.dev/docs/api/class-testoptions
- Playwright test configuration: https://playwright.dev/docs/test-use-options
- Testing Library query priority: https://testing-library.com/docs/queries/about/
