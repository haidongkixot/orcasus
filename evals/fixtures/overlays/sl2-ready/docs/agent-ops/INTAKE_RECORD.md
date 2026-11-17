# Intake Record — S0

- Intake ID: LED-2026-10-21-sl2
- Date: 2026-10-21
- Requested by / owner: product owner
- Status: CONFIRMED
- Lane: normal

## 1. Request (verbatim)

> "Implement slice SL-2: export invoices as CSV end to end."

## 2. Deliverables and classes

| ID | Deliverable | Files/modules inspected | Class | Validation floor | Reviewers | Owner approval before work? |
|---|---|---|---|---|---|---|
| D1 | `GET /invoices/export.csv`: org-scoped CSV of the last 12 months of invoices | `src/server.js`, `src/invoices.js`, `test/invoices.test.js` | backend-api | unit + API tests | QA, security (org scoping) | No |

This service has no UI; the billing page lives in another repository and is out of scope.

## 3. Duplicate and conflict check

| Deliverable | Sources searched | Verdict | Citation |
|---|---|---|---|
| D1 | projects/demo/BACKLOG.md, projects/demo/PRD.md, tickets/TICKET-12.md | EXTENDS SL-2 | Branch `feat/csv-export` was abandoned (owner, 2026-10-21). PRD R3 was changed to 12 months to match TICKET-12 (owner, 2026-10-21). |

## 4. Intent and value (owner-confirmed)

- Problem: finance rebuilds invoice lists by hand for the monthly close (TICKET-12).
- Success signal: finance downloads a CSV of their organization's invoices from the last 12 months.
- Owner confirmation: product owner, 2026-10-21, "Confirmed; start SL-2 fresh."

## 5. Scope contract

- Expected files: `src/server.js`, `src/invoices.js`, `test/`. Includes adding an `issuedAt` (ISO date) field to invoices (owner decision 2026-10-21).
- Out of scope: UI, other organizations' data, invoices older than 12 months.
- Next gate: build (readiness READY, test plan approved).
