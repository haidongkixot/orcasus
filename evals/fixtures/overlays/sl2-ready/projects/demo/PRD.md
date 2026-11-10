# PRD: Billing area

## Problem
Finance staff rebuild invoice lists by hand in spreadsheets every month.

## Users
Finance staff and organization admins.

## Requirements
- R1: Users can see all invoices of their own organization, never another organization's.
- R2: Only admins can void an invoice.
- R3: Exports include the organization's invoices from the last 12 months (changed by the product owner on 2026-10-21 to match TICKET-12).
- R4: Invoice totals are shown in the organization's currency.

## Non-goals
- Payments collection in this phase.
