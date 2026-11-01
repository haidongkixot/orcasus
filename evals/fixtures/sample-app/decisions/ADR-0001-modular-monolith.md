# ADR-0001: Modular monolith

- Status: DECIDED
- Date: 2026-09-01
- Decision owner: Product owner

## Decision
Ledgerly stays a single Node service with modules per domain (invoices, payments) until load or team size justifies separation.

## Rejected
Microservices per domain: operational cost not justified for one small team.
