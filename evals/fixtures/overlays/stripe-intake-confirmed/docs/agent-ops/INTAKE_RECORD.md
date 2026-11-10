# Intake Record — S0

- Intake ID: LED-2026-10-20-stripe
- Date: 2026-10-20
- Requested by / owner: product owner
- Status: CONFIRMED
- Lane: normal

## 1. Request (verbatim)

> "Add Stripe payments to the checkout."

## 2. Deliverables and classes

| ID | Deliverable | Files/modules inspected | Class | Validation floor | Reviewers | Owner approval before work? |
|---|---|---|---|---|---|---|
| D1 | Customers pay an open invoice by card through Stripe on a new pay-invoice route (the "checkout") | `src/payments.js`, `src/server.js`, `projects/demo/PRD.md` | integration | contract tests + failure-path tests; real account/scope verified | integration, security | Yes (given 2026-10-20) |

- Governing class: integration (payment provider, keys, webhooks).

## 3. Duplicate and conflict check

| Deliverable | Sources searched | Verdict | Citation |
|---|---|---|---|
| D1 | knowledge/INDEX.md, projects/demo/, decisions/, tickets/ | EXTENDS | `src/payments.js` holds a stub `chargeInvoice`. The PRD non-goal "Payments collection" was removed by the owner on 2026-10-20 (PRD R5). |

## 4. Intent and value (owner-confirmed)

- Problem: customers pay invoices by bank transfer, and finance matches payments by hand.
- Expected value: card payment of open invoices; finance sees paid status without manual matching.
- Success signal: an open invoice can be paid by card in test mode and its status becomes `paid`.
- Owner confirmation: product owner, 2026-10-20, "Confirmed, card payments are in scope for this phase."

## 5. Scope contract

- Expected files/modules: `src/payments.js`, `src/server.js`, `src/invoices.js`, tests.
- Out of scope: refunds, subscriptions, stored cards.
- Next gate: /project-discovery.
