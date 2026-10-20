# Discovery and Testing Principles

This guide defines the mandatory working order for web/mobile changes using Claude Code agents.

## Required sequence
1. Inspect repository, instructions, stack, assets, integrations, permissions, test infrastructure and in-progress changes.
2. Complete `docs/discovery/READINESS_MATRIX.md` or an equivalent project-approved matrix.
3. Surface blockers, unknowns and high-risk choices with real alternatives; request owner decisions where necessary.
4. Compare feasible architectures and record significant decisions in an ADR.
5. Implement in small, testable slices using already-approved resources.
6. Apply the test pyramid and justify any visual testing/screenshot artifacts.
7. Run targeted tests first; broaden only when risk/release criteria warrant it.
8. Report commands, actual results, retained artifacts and unverified areas.

## Mandatory anti-patterns
- Generating screenshots for every screen, component state or test by default.
- Using generated imagery as proof that a real app works.
- Adding new test frameworks or major dependencies before reviewing existing project capabilities.
- Faking a required asset, account, integration or runtime resource and presenting it as production-ready.
- Silently choosing a degraded workaround because permissions, assets or credentials are missing.
- Repeatedly rerunning a failed suite without diagnosis.
- Marking blocked, untested or assumed behavior as passed.

## Owner-decision protocol
Ask for owner input when required credentials/scopes, third-party accounts, paid services, licensed assets, deployment environments, device platforms, destructive migrations or material quality/cost trade-offs are missing or unknown. Explain options, consequences and a recommendation. Continue safe independent work while waiting, but do not cross the blocked decision.

## Suggested Playwright default
If Playwright is already present and the project has no contrary policy, disable success screenshots and capture only failures:

```ts
use: {
  screenshot: 'only-on-failure',
  trace: 'on-first-retry',
  video: 'off'
}
```

Confirm the supported options in the installed Playwright version and current project config before applying. The snippet is a suggested default, not a requirement to add Playwright to every project.

## References
- Claude Code Skills: https://code.claude.com/docs/en/skills
- Claude Code Permissions: https://code.claude.com/docs/en/permissions
- Claude Code Hooks: https://code.claude.com/docs/en/hooks
- Playwright test options: https://playwright.dev/docs/api/class-testoptions
- Testing Library query priority: https://testing-library.com/docs/queries/about/
