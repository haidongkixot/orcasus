# Discovery and Testing Principles

This guide defines the required working order for web/mobile changes using Claude Code skills.

For a complete Vietnamese installation and operating walkthrough, see [USER_GUIDE_VI.md](USER_GUIDE_VI.md). To apply the rules consistently in a consuming project, use the [Agent Operating Contract](agent-operating-contract.md).

## Required sequence
1. Inspect repository, instructions, stack, assets, integrations, permissions, test infrastructure and in-progress changes.
2. Complete a readiness matrix with evidence.
3. Surface blockers, unknowns and high-risk choices with feasible options; request owner decisions where necessary.
4. Compare viable architectures and record significant decisions in an ADR.
5. Define acceptance criteria and a risk-based test plan before implementation.
6. Implement in small, testable slices using approved resources.
7. Choose the lowest-cost reliable test layer; justify any browser/device/visual testing.
8. Report commands, actual results, retained artifacts and unverified areas.

## Mandatory anti-patterns
- Generating screenshots for every screen, component state or test by default.
- Using generated imagery as proof that the real app works.
- Adding new test frameworks or major dependencies before reviewing existing project capabilities.
- Faking a required asset, account, integration or runtime resource and presenting it as production-ready.
- Silently choosing a degraded workaround because permissions, assets or credentials are missing.
- Repeatedly rerunning a failed suite without diagnosis.
- Marking blocked, untested or assumed behavior as passed.

## Owner-decision protocol
Ask the owner when required credentials/scopes, third-party accounts, paid services, licensed assets, deployment environments, device platforms, destructive migrations or material quality/cost trade-offs are missing or unknown. Explain options, consequences and a recommendation. Continue safe independent work while waiting, but do not cross the blocked decision.

## Screenshot policy
Default screenshot budget is zero. Use semantic/behavioral assertions, API responses, DOM state, logs and network checks first. Capture real application screenshots only to answer a named visual question or to verify an approved visual regression baseline. Set a count budget, retention policy and representative viewport matrix before running. Do not use AI-generated images as test evidence.

If Playwright is already present and the project has no contrary policy, a suitable starting point may be:

    use: {
      screenshot: 'only-on-failure',
      trace: 'on-first-retry',
      video: 'off'
    }

Confirm the installed version and current project configuration before applying. This is an option, not a requirement to add Playwright.

## Test status vocabulary
- **PASS:** criterion verified by execution/evidence.
- **FAIL:** criterion did not pass.
- **BLOCKED:** required resource or decision is unavailable.
- **NOT RUN:** no verification was executed.
- **SKIPPED:** deliberately not executed under a documented policy.

Never report NOT RUN, BLOCKED or assumed behavior as PASS.

## References
- Claude Code Skills: https://code.claude.com/docs/en/skills
- Claude Code Permissions: https://code.claude.com/docs/en/permissions
- Claude Code Hooks: https://code.claude.com/docs/en/hooks
- Playwright test options: https://playwright.dev/docs/api/class-testoptions
- Testing Library query priority: https://testing-library.com/docs/queries/about/
