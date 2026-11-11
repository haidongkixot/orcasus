# Ledgerly (Orcasus eval fixture)

A small invoicing web service used only as a fixture for Orcasus live skill evals.
It is not a product. Do not deploy it.

- `src/server.js`: HTTP routes for invoices.
- `src/invoices.js`: invoice rules (totals, status changes).
- `src/payments.js`: payment provider client; needs `PAYMENT_API_KEY`.
- `test/invoices.test.js`: unit tests (`npm test`, Node's built-in test runner).
- `projects/demo/`: PRD and backlog for the billing area.
- `decisions/`: architecture decision records.
- `tickets/`: requests from the business.
