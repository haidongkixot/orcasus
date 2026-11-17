# Intake Record — S0

- Intake ID: LED-2026-10-24-storage
- Date: 2026-10-24
- Requested by / owner: product owner
- Status: CONFIRMED
- Lane: normal

## 1. Request (verbatim)

> "Invoices are lost on every restart. Decide how invoices are stored: keep the in-memory array, move to SQLite, or move to PostgreSQL."

## 2. Deliverables and classes

| ID | Deliverable | Files/modules inspected | Class | Validation floor | Reviewers | Owner approval before work? |
|---|---|---|---|---|---|---|
| D1 | Storage decision for invoices, recorded in an ADR (implementation is a later slice) | `src/server.js`, `src/invoices.js`, `decisions/ADR-0001-modular-monolith.md` | data-schema-migration (decision only) | ADR with debate record | data, security | Yes (given 2026-10-24) |

## 4. Intent and value (owner-confirmed)

- Problem: `src/server.js` keeps invoices in an in-memory array; a restart loses them.
- Constraints: one small team; a single Node service (ADR-0001); hosting not yet chosen.
- Owner confirmation: product owner, 2026-10-24, "Confirmed. Run the team debate; I decide after the ADR."

## 5. Scope contract

- Next gate: /team-debate. No code change.
