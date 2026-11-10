# PRD: Billing area

## Problem
Finance staff rebuild invoice lists by hand in spreadsheets every month.

## Users
Finance staff and organization admins.

## Requirements
- R1: Users can see all invoices of their own organization, never another organization's.
- R2: Only admins can void an invoice.
- R3: Exports include all historical invoices for the organization.
- R4: Invoice totals are shown in the organization's currency.
- R5: Customers can pay an open invoice by card (Stripe). Added by the product owner on 2026-10-20.

## Non-goals
- Refunds and subscriptions in this phase.
