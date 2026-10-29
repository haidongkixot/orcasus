---
name: project-discovery
description: Mandatory preflight gate for non-trivial web/mobile work. Inventory repository, assets/licences, tools and permissions, integrations, credential availability, runtime, environments, test resources and budget before architecture or implementation.
---

# Project Discovery — Mandatory Preflight Gate v1.3.0

## Gate
For non-trivial features, integrations, redesigns, migrations, permission changes and production-relevant bug fixes, the orchestrator must consolidate discovery evidence before selecting architecture or assigning implementation. Parallel agents may perform read-only discovery; they must not invent substitutes, add dependencies or begin implementation while material readiness is UNKNOWN.

Reuse a current, evidence-backed readiness record rather than duplicating it.

## Inspect actual evidence
Inspect instructions, git status/diff, in-progress work, manifests/lockfiles, versions/scripts, architecture, routes/state/APIs/schemas/migrations, reusable UI, design tokens, fonts/logos/icons/images and licences. Inventory auth/SSO, database, storage, email, payments, analytics, external APIs, tool/MCP availability and actual operation scopes. Check environment-variable names and presence only; never print secrets. Check local/preview/staging/production separation, browsers/devices, CI, fixtures, test runner, observability, budget, accessibility, localization, performance and release/rollback requirements.

Do not overwrite uncommitted changes. Do not infer a credential, account, scope, asset or runtime exists just because code references it.

## Readiness record
Write/update docs/agent-ops/READINESS_MATRIX.md and docs/agent-ops/DISCOVERY_SUMMARY.md.

Use statuses:
- AVAILABLE — verified with current evidence.
- MISSING — known unavailable.
- UNKNOWN — not verified; never treat as available.
- BLOCKED — prevents a dependent requirement/task.
- NOT NEEDED — justified as irrelevant.

Record requirement, resource/permission, status, evidence, impact, feasible options, cost/time/security/quality trade-offs, recommendation and owner decision needed.

## Decision gate
Classify READY, READY WITH ACCEPTED RISKS, PARTIAL or BLOCKED. Before implementation, verify assets/licences, service contracts, permission scopes, environment and test resources; compare options; record significant decision/rejected alternatives in an ADR; define acceptance criteria, owner/dependencies and a test plan.

If a required resource, licensed asset, integration, permission or product decision is missing—or a workaround would reduce functionality, security, fidelity, UX, performance or maintainability—stop dependent work. Present 2–3 viable options, consequences and recommendation to the owner. Continue only independent, reversible work that does not encode the unresolved choice.

Never silently replace a real integration with fake API/mock/local-only behavior, replace required assets with placeholders/generated assets, change architecture/data model/platform or weaken acceptance criteria to keep work moving. Mocks are allowed only for isolated tests and must not hide production gaps.

If runtime disproves an assumption, stop affected work, preserve minimal evidence, update readiness record and return to owner when the plan/quality changes. Discovery completion is not runtime validation.

## Output
Readiness matrix, discovery summary, blockers/unknowns, owner decisions, evidence-backed options, ADR and acceptance/test-plan handoff. Never record secret values.
