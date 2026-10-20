# Changelog

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
- Prohibited generated images as evidence of the real application working.
- Added evidence-based test reports and truthful PASS/FAIL/BLOCKED/NOT RUN distinctions.
