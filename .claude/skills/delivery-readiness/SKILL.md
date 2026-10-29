---
name: delivery-readiness
description: Run a multidisciplinary release gate for complex web/mobile changes, covering requirements, tests, UX/accessibility, security, reliability, migrations, and documentation.
---

# Delivery Readiness Gate

1. Read PRD, ADRs, acceptance criteria, readiness record, test plan and change summary.
2. Verify every acceptance criterion as PASS, FAIL, BLOCKED or NOT CHECKED.
3. Inspect actual commands and outputs; never infer success from a code diff or agent summary.
4. Review migration/backfill/rollback and backward compatibility.
5. Request targeted independent reviews: QA, security, UX/accessibility, performance and mobile when affected.
6. Confirm no unapproved workaround, dependency, permission expansion or quality downgrade.
7. Check screenshot/trace/video counts against approved test plan; default budget is zero.
8. Block release recommendation if authorization/tenant isolation, data integrity or critical user journeys fail.
9. Save report to reports/<milestone>-readiness.md.

Verdicts: READY FOR REVIEW, NOT READY, INSUFFICIENT EVIDENCE. This skill cannot approve deployment for the owner.
