# Intake Record — S0

- Intake ID: LED-2026-10-25-export-design
- Date: 2026-10-25
- Requested by / owner: product owner
- Status: CONFIRMED
- Lane: normal

## 1. Request (verbatim)

> "How should invoice export run: a synchronous CSV download, or a background job that emails a download link? Get the team to decide."

## 2. Deliverables and classes

| ID | Deliverable | Files/modules inspected | Class | Validation floor | Reviewers | Owner approval before work? |
|---|---|---|---|---|---|---|
| D1 | A decision on how SL-2 delivers the export, recorded in an ADR. No code in this intake | `src/server.js`, `src/invoices.js`, `projects/demo/PRD.md`, `tickets/TICKET-12.md` | backend-api (decision only) | ADR with a debate record | architecture, security | Yes (given 2026-10-25) |

## 3. Duplicate and conflict check

| Deliverable | Sources searched | Verdict | Citation |
|---|---|---|---|
| D1 | projects/demo/BACKLOG.md, projects/demo/PRD.md, tickets/TICKET-12.md, decisions/ | NEW decision inside SL-2 | The old branch `feat/csv-export` was abandoned (owner, 2026-10-25). PRD R3 now says 12 months, matching TICKET-12. No ADR covers the delivery mode; ADR-0001 only fixes a single Node service. |

## 4. Intent and value (owner-confirmed)

- Problem: finance needs the export for the monthly close (TICKET-12). The delivery mode is undecided, and SL-2 is blocked on it.
- Facts the owner gave: the largest organization has about 40,000 invoices in 12 months; the others have a few hundred. No e-mail provider is set up for this service yet. No job queue exists.
- Owner confirmation: product owner, 2026-10-25, "Confirmed. Both options are open. Run the team debate; I decide after the ADR."

## 5. Scope contract

- Out of scope: implementing either option.
- Next gate: /team-debate.
