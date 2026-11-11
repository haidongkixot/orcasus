# Project Readiness Matrix — v2.2.0

Complete discovery before architecture or implementation. Record current evidence, not assumptions.

| Area | Requirement/capability | Resource/permission | Status (AVAILABLE/MISSING/UNKNOWN/BLOCKED/NOT NEEDED) | Evidence/path/source | Impact if missing | Feasible options/trade-offs | Recommendation | Owner decision? |
|---|---|---|---|---|---|---|---|---|
| Product | User goal and acceptance criteria | Product brief/owner decisions | UNKNOWN | | | | | Yes/No |
| Repo and stack | Framework, runtime, scripts, git status | Existing repository | UNKNOWN | | | | | Yes/No |
| UX/assets | Components, tokens, fonts, logo, icons, licences | Files/source/usage rights | UNKNOWN | | | | | Yes/No |
| Integrations | APIs, SSO, database, payments, email, analytics | Account, endpoint, scopes, network | UNKNOWN | | | | | Yes/No |
| Secrets | Required env var presence | Secret manager/local env | UNKNOWN | Record names/status only; never record values. Names come from code (file:line), not from `.env*` files | | | | Yes/No |
| Permissions | Tool/MCP/API operations | Current session and granted scopes | UNKNOWN | | | | | Yes/No |
| Environments | Local, preview, staging, production separation | URLs/configuration/access | UNKNOWN | | | | | Yes/No |
| Data | Fixtures, seed data, schema, migrations, rollback | Approved test data/access | UNKNOWN | | | | | Yes/No |
| Testing | Runner, scripts, CI, fixtures | Installed tools and CI access | UNKNOWN | | | | | Yes/No |
| Browser/mobile | Browsers, devices, emulators, signing | Runtime/device access | UNKNOWN | | | | | Yes/No |
| Security | Roles, tenant boundaries, sensitive data | Requirements/test cases | UNKNOWN | | | | | Yes/No |
| Performance | Latency/load/bundle budgets | Metrics and approved test resources | UNKNOWN | | | | | Yes/No |
| Capture artifacts | Screenshot/trace/video requirement | Named question, bounded budget, approval | NOT NEEDED | All budgets default to zero | | | | Yes/No |
| Cost | Paid services, CI, device farms, storage | Budget/approval | UNKNOWN | | | | | Yes/No |
| Delivery | Release target, approval, rollback | Deployment access and owner approval | UNKNOWN | | | | | Yes/No |

## Readiness decision
- READY: no unresolved material blocker in scope.
- READY WITH ACCEPTED RISKS: high-risk gaps and owner acceptance are recorded.
- PARTIAL: safe independent work may continue; dependent work is blocked.
- BLOCKED: a required resource or decision prevents delivery.

## Owner decisions
| ID | Blocker/unknown | Evidence | Option A | Option B | Option C | Recommendation | Decision owner | Decision/date |
|---|---|---|---|---|---|---|---|---|

## Gate before implementation
- [ ] Current repository, git diff, existing components and resources inspected.
- [ ] Assets, sources and licenses checked.
- [ ] Integrations, credentials availability and permission scopes verified.
- [ ] Runtime, test runner, fixtures and target platforms checked.
- [ ] UNKNOWN items are not misclassified as AVAILABLE.
- [ ] Material trade-offs/options presented to owner.
- [ ] No unapproved workaround or degraded acceptance criteria.
- [ ] Architecture decision, acceptance criteria and test plan recorded.
- [ ] Screenshot/trace/video budgets remain zero unless a justified exception is approved.
