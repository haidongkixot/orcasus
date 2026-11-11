# Project Readiness Matrix — SL-2

| Area | Requirement/capability | Resource/permission | Status | Evidence/path/source | Impact if missing | Feasible options/trade-offs | Recommendation | Owner decision? |
|---|---|---|---|---|---|---|---|---|
| Repo and stack | Node 20 HTTP service, ES modules | Repository | AVAILABLE | `package.json`, `src/server.js` | — | — | — | No |
| Data | In-memory invoices; `orgId` on every invoice | Code | AVAILABLE | `src/invoices.js`, `src/server.js` | — | — | — | No |
| Data | An issue date for the 12-month filter | Data model | MISSING, owner decided | Invoices have no date field | 12-month scope cannot be applied | Add `issuedAt` (ISO date) to invoices | Add `issuedAt`; approved by the product owner on 2026-10-21 and part of this slice | Yes (decided) |
| Testing | `node --test` | Installed Node | AVAILABLE | `package.json` script `test` | — | — | — | No |
| Security | Org scoping from the `x-org-id` header | Code | AVAILABLE | `src/server.js` | Cross-org leak | — | Reuse `listInvoices` | No |
| Capture artifacts | Screenshot/trace/video | — | NOT NEEDED | All budgets zero | — | — | — | No |

## Readiness decision

READY (2026-10-21).
