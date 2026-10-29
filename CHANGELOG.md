# Changelog

## 1.3.0 — Mandatory Preflight and Zero-Capture Testing Defaults
- Strengthened Project Discovery into an explicit orchestrator-owned gate: parallel work before readiness is read-only discovery, and implementation delegation waits for consolidated evidence.
- Added a stricter owner-decision protocol for missing permissions, credentials, licensed assets, integration access, environments and material quality/cost trade-offs.
- Prohibited silent substitute integrations, degraded workarounds and requirement weakening without approval.
- Set screenshot, trace and video budgets to zero by default; non-zero capture requires a named visual/diagnostic question, bounded artifact plan and owner approval or pre-approved project policy.
- Clarified that Playwright traces may embed screenshots/screencasts and DOM snapshots, so they count toward the artifact budget.
- Strengthened test-layer selection, targeted retries, failure diagnosis and reporting of actual execution evidence.
- Updated Agent Operating Contract, principles, templates, user guide and README to align with the new gates.

## 1.2.1 — Documentation and Adoption Guide
- Rewrote README to describe the library's scope, limitations, core skills, installation and recommended reading order.
- Added a Vietnamese end-to-end user guide with platform-specific copy commands, workflow, blocker handling, testing layers, screenshot policy and acceptance checklist.
- Clarified project artifact paths and updated the Agent Operating Contract to use consistent docs/agent-ops/ paths.
- Kept the distinction between skill guidance and actual runtime/permission enforcement explicit.

## 1.2.0 — Stronger Project Adoption Gates
- Added an Agent Operating Contract to enforce discovery and test planning in each consuming project.
- Added a reusable readiness matrix template for assets, integrations, permissions, runtime and budget.
- Added a risk-based test plan template with an explicit default-zero screenshot budget and artifact retention controls.
- Clarified that installing a skill alone does not guarantee automatic invocation; consuming projects should include orchestration rules.

## 1.1.0 — Discovery and Efficient Testing
- Added mandatory pre-planning discovery of repository, assets, access, permissions, integrations, runtime and test resources.
- Added readiness matrix and explicit owner decision protocol for blockers/high-risk gaps.
- Added efficient layered testing, with unit/API/component checks preferred over costly browser/visual tests where appropriate.
- Set screenshots off for successful tests by default and require explicit rationale, count budget and retention for visual artifacts.
- Prohibited generated images as evidence of the real app working.
- Added evidence-based test reports and truthful PASS/FAIL/BLOCKED/NOT RUN distinctions.
