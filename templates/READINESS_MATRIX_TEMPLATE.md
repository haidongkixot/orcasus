# Project Readiness Matrix — v1.3.0

> Complete discovery before selecting architecture or starting implementation. Record evidence, not assumptions. Duplicate rows as needed.

| Area | Requirement / capability | Resource / permission required | Status (AVAILABLE / MISSING / UNKNOWN / BLOCKED / NOT NEEDED) | Evidence / path / source | Impact if missing | Feasible options and trade-offs | Recommended action | Owner decision required? |
|---|---|---|---|---|---|---|---|---|
| Product | Requirements and acceptance criteria | Product brief / owner decisions | UNKNOWN | | | | | Yes/No |
| Repo & stack | Framework, runtime, package manager, scripts | Local repository | UNKNOWN | | | | | Yes/No |
| UX / assets | Design system, fonts, logos, icons, licensed assets | Files, source, usage rights | UNKNOWN | | | | | Yes/No |
| Integrations | API, database, SSO, email, payments, analytics | Endpoint, account, scopes | UNKNOWN | | | | | Yes/No |
| Secrets | Required environment variables | Secret manager / local env | UNKNOWN | Record presence only; never paste values | | | | Yes/No |
| Permissions | Tool/MCP/API operations available to this session | Granted scopes / policy | UNKNOWN | | | | | Yes/No |
| Environments | Local, preview, staging, production separation | URLs, access, configuration | UNKNOWN | | | | | Yes/No |
| Data | Fixtures, seed data, schema, migrations, rollback | Approved test data and backups | UNKNOWN | | | | | Yes/No |
| Testing | Existing test runner, scripts, fixtures, CI | Dependencies and CI access | UNKNOWN | | | | | Yes/No |
| Browser/mobile | Supported browsers, devices, emulators | Runtime/device access | UNKNOWN | | | | | Yes/No |
| Observability | Logs, error tracking, network inspection | Local tools/authorized services | UNKNOWN | | | | | Yes/No |
| Security | Roles, authorization boundaries, sensitive data | Requirements and test cases | UNKNOWN | | | | | Yes/No |
| Performance | Target latency, concurrency, bundle size | Acceptance thresholds and measurement tools | UNKNOWN | | | | | Yes/No |
| Budget | Paid services, CI minutes, device farms, artifact storage | Budget and approval | UNKNOWN | | | | | Yes/No |
| Visual evidence | Need for screenshots, traces or videos | Named visual question, bounded budget and retention | UNKNOWN | Default capture budgets are zero until a justified need is reviewed | | | | Yes/No |
| Delivery | Release target, approvals, rollback | Deployment access and owner approval | UNKNOWN | | | | | Yes/No |

## Readiness decision

- **READY:** no unresolved material blocker for the proposed scope.
- **READY WITH ACCEPTED RISKS:** high-risk gaps and owner acceptance are documented.
- **BLOCKED:** a required resource or owner decision prevents safe delivery.
- **PARTIAL:** independent work can proceed, but listed dependent tasks remain blocked.

## Blockers and decisions

| ID | Blocker / unknown | Evidence | Option A | Option B | Option C | Recommendation | Decision owner | Decision / date |
|---|---|---|---|---|---|---|---|---|

## Gate before implementation

- [ ] Existing resources, components, assets and licences inspected.
- [ ] Permissions, scopes and integrations checked using available evidence.
- [ ] Runtime, test environment, test runner and fixtures verified.
- [ ] Missing resources and unknowns remain explicitly labelled.
- [ ] Alternatives and material trade-offs presented to owner.
- [ ] No workaround silently changes required behavior or quality.
- [ ] Architecture decision and acceptance criteria recorded.
- [ ] Test plan and screenshot/trace/video budgets reviewed (default zero).
