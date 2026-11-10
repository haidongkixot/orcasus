# Project Readiness Matrix — SL-2

| Area | Requirement/capability | Resource/permission | Status | Evidence/path/source | Impact if missing | Feasible options/trade-offs | Recommendation | Owner decision? |
|---|---|---|---|---|---|---|---|---|
| Repo and stack | Node 20 HTTP service, ES modules | Repository | AVAILABLE | `package.json`, `src/server.js` | — | — | — | No |
| Data | In-memory invoices; `orgId` on every invoice | Code | AVAILABLE | `src/invoices.js`, `src/server.js` | — | — | — | No |
| Testing | `node --test` | Installed Node | AVAILABLE | `package.json` script `test` | — | — | — | No |
| Security | Org scoping from the `x-org-id` header | Code | AVAILABLE | `src/server.js` | Cross-org leak | — | Reuse `listInvoices` | No |
| Capture artifacts | Screenshot/trace/video | — | NOT NEEDED | All budgets zero | — | — | — | No |

## Readiness decision

READY (2026-10-21).
