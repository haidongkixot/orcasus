---
name: platform-discovery
description: Turn an ambitious web/mobile platform idea into a validated product brief, capability map, domain model, architecture options, and phased vertical-slice roadmap.
---

# Platform Discovery Workflow

1. Invoke project-discovery first for repository, asset, permission, integration, runtime and test-resource readiness.
2. Do not assume greenfield; inspect existing code, docs and decisions.
3. Define user segments, jobs-to-be-done, workflows, constraints, platforms, data sensitivity, integrations and success metrics.
4. Map capability domains only as required: identity/orgs, tenancy, policies, modules, metadata, workflow, notifications, audit/history, search, reporting, imports/exports, integrations, mobile sync and administration.
5. Separate platform primitives from business modules and differentiators.
6. Use team-debate for material choices, with independent proposals and documented trade-offs.
7. Produce PRD, capability map, ADRs, dependency plan and testable acceptance criteria.
8. Pick one end-to-end vertical slice that validates the riskiest product/architecture assumptions.
9. Define MVP non-goals and unknowns. Do not paper over blocked resources.

Outputs: projects/<slug>/PRD.md, CAPABILITY_MAP.md, ROADMAP.md, ADRs, risk register, success metrics and owner decisions.
