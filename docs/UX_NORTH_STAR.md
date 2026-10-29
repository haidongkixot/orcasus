# UX North Star — Clear, Fast, Trustworthy

Aim for a polished product experience informed by strong work-management software without copying proprietary UI, branding, code or assets.

## Experience qualities
- Clear hierarchy and predictable navigation.
- High information density without visual clutter.
- Common tasks require few, obvious actions.
- Progressive disclosure for advanced configuration.
- Consistent design tokens, typography, spacing, icons and component behavior.
- Clear loading, empty, error, success, disabled, validation and permission-denied states.
- Responsive layouts adapted to mobile interaction, not merely shrunk desktop screens.
- Semantic structure, keyboard support, visible focus, accessible names, contrast and reduced-motion support.
- Helpful undo/recovery and clear impact warnings for destructive operations.
- Fast-feeling transitions with no unnecessary animation or misleading static controls.

## Before design
Inspect actual design system, available assets and licenses, component library, localization, responsive requirements and accessibility constraints. Do not create or substitute branded assets without approval. Designers must make assumptions and missing resources explicit.

## Visual verification policy
Visual polish is not achieved by generating thousands of screenshots. Default screenshot/trace/video budgets are zero. Start with semantic DOM checks, interaction tests, accessibility queries and geometry where appropriate. Only conduct a visual comparison when it answers a specific question that cannot be sufficiently answered by cheaper checks. Record target pages/states, viewport/theme, maximum artifact count and retention policy before capture.

## Acceptance signals
- Users can complete primary workflows without unexplained dead ends.
- Navigation and status language stay consistent.
- Errors explain cause and recovery where known.
- Forms have correct validation, focus and accessibility behavior.
- Layouts support agreed viewports with no known critical overflow/clipping.
- Claims of user research, device coverage or visual review are supported by actual evidence.
