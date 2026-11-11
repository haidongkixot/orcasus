# Intake Record — S0

- Intake ID: LED-2026-10-22-crossorg
- Date: 2026-10-22
- Requested by / owner: product owner
- Status: CONFIRMED
- Lane: normal (owner: "not exploitable on demand; investigate first")

## 1. Request (verbatim)

> "Users occasionally see another organization's invoice in the invoice list in production, and nobody can reproduce it."

## 2. Deliverables and classes

| ID | Deliverable | Files/modules inspected | Class | Validation floor | Reviewers | Owner approval before work? |
|---|---|---|---|---|---|---|
| D1 | Find the root cause of the intermittent cross-organization invoice in `GET /invoices`, then fix it | `src/server.js`, `src/invoices.js`, `test/invoices.test.js` | auth-permission-security | failing case reproduced, negative authorization tests, security review | security, QA | Yes (given 2026-10-22) |

## 4. Intent and value (owner-confirmed)

- Problem: tenant isolation (PRD R1) is broken intermittently; no reliable reproduction.
- Owner confirmation: product owner, 2026-10-22, "Confirmed. Investigate with competing hypotheses; no production changes without my approval."

## 5. Scope contract

- Expected files: `src/server.js`, `src/invoices.js`, tests.
- Out of scope: production data access, changes to production infrastructure.
- Next gate: /root-cause-debate (cause unknown and not reproducible).
