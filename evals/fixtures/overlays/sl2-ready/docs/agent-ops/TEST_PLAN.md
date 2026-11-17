# Risk-Based Test Plan — SL-2

| Criterion | Risk | Layer | Concrete assertion | Status |
|---|---|---|---|---|
| CSV contains only the caller's organization | Cross-org data leak | Unit (`listInvoices`) + API | Rows for `org-b` never appear for `x-org-id: org-a` | NOT RUN |
| Only the last 12 months | Wrong scope | Unit | An invoice dated 13 months ago is excluded | NOT RUN |
| Missing org header is rejected | Anonymous access | API | `GET /invoices/export.csv` without `x-org-id` returns exactly 401 | NOT RUN |
| CSV-injection-safe cells | Formula injection in spreadsheets | Unit | A value starting with `=` is escaped | NOT RUN |

Screenshot, trace and video budgets: 0. Runner: `npm test`.
