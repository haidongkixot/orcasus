---
name: vertical-slice-delivery
description: Plan and deliver a small complete workflow across UI, API, domain rules, persistence, permissions, observability, and automated tests.
---

# Vertical Slice Delivery

1. Complete project-discovery for the slice, then define acceptance criteria and risk.
2. Invoke efficient-testing and create a test plan before coding; screenshot, trace and video budgets default to zero.
3. Freeze/version UI, API and data contracts; define owner, dependencies and file/module ownership.
4. Implement the smallest cohesive path UI → API → domain/application → data → tests/telemetry.
5. Include authorization, validation, error handling, empty/loading/success states and accessibility.
6. Do not add optional architecture or major dependencies without evidence and approval.
7. Run targeted unit/API/integration/component tests; use a small E2E journey only when needed.
8. Do not substitute mock services/assets or local-only behavior for required production capabilities without owner approval.
9. Ask QA, security, design and performance reviewers to inspect relevant risk areas independently.
10. Fix findings and rerun affected plus required regression tests. Record commands/results/artifact counts.
11. Update ADR/PRD and extract abstractions only when the slice demonstrates their need.

Deliver a running testable path or documented blocker, changed files, exact test evidence, review findings, risks and next-slice recommendation.
