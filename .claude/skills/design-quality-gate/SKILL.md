---
name: design-quality-gate
description: Assess a web/mobile design system and implemented UI against usability, accessibility, responsiveness, consistency, and interaction-state criteria.
---

# Design Quality Gate

1. Read product requirements and UX North Star.
2. Inspect actual design system, assets, fonts, icons, licence constraints and existing components.
3. Check hierarchy, navigation, information density, task efficiency, responsive layout, accessibility, keyboard flow, focus, contrast, reduced motion and copy clarity.
4. Verify loading, empty, error, success, disabled, validation and permission-denied states.
5. Prefer DOM/accessibility assertions and interaction checks.
6. Do not generate screenshots as test evidence. Real screenshots are not the default; if visual review is material, follow Efficient Testing and its zero-by-default artifact budget.
7. Record issues with severity, actual evidence, affected workflow, expected behavior and recommended fix.
8. Do not report viewport/device inspection that did not occur.

Deliver prioritized UX/UI report and testable acceptance criteria for fixes.
