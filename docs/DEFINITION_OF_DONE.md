# Definition of Done — Orcasus v2.2.0

A feature/slice is done only when applicable gates have evidence.

## Readiness and product
- Requirements, user journey, non-goals and acceptance criteria documented.
- Current repository, in-progress work, components, assets/licences, integrations/access, environments and test resources inspected.
- Readiness record uses evidence; UNKNOWN is not AVAILABLE.
- Owner resolves blockers/material trade-offs.
- No unapproved fake integration, placeholder asset, local-only substitute or weakened requirement.

## Design and engineering
- Architecture/API/data/UI contracts and file ownership agreed.
- Significant decisions and rejected alternatives recorded in ADR.
- Authorization, data boundaries, validation, error states and migrations handled where relevant.
- Responsive behavior, accessibility, and loading/empty/error/success/permission-denied states considered.
- New dependencies have a documented reason and needed approval.

## Testing
- Test plan maps criteria to a justified test layer.
- Lowest-cost reliable tests used; broad E2E only where risk requires.
- Screenshot/trace/video budgets default to zero; every nonzero capture is planned and authorized.
- Actual commands and results recorded.
- Failures diagnosed before targeted retries; assertions are not weakened to obtain green results.
- BLOCKED, NOT RUN, SKIPPED and unverified areas are disclosed.

## Review and delivery
- Independent QA and relevant security/UX/performance/mobile review completed.
- Findings resolved or explicitly accepted by owner with rationale.
- Meeting Secretary status is accurate after a material debate.
- Docs/ADR/PRD updated where material.
- Final handoff summarizes deliverables, tests, findings, risks and next actions.
- Deployment/publishing is separately authorized; this checklist grants no deployment permission.
