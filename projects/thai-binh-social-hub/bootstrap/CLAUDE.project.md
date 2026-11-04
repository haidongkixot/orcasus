

---

# Project: Thai Binh Social Hub (tb-social-hub)

The Orcasus constitution above governs every task in this repository. This section adds project facts. Where the two conflict, the Orcasus gates win, and the conflict goes to the owner.

## Start of every session
1. Read `projects/thai-binh-social-hub/PLAN.md` (approved plan) and `projects/thai-binh-social-hub/HANDOFF_LOCAL.md` (current status and owner actions).
2. Read the readiness and test records in `docs/agent-ops/`, plus the ADRs in `decisions/` once they exist.
3. Check `git status` and the latest commits before changing anything.

## Product in one line
A mobile-first web app where 1000+ Thai Binh Corp employees sign in with Facebook, are approved as employees, browse the company's Facebook Pages and Instagram posts, engage with them, and earn points, badges and leaderboard places.

## Owner decisions (already made; record them as ADRs in Phase 0)
- **Engagement = hub + deep link + webhook attribution.**
  - Meta's API cannot comment, react or share as a user. Comment/React open the post in the FB/IG app.
  - Page/IG webhooks on Thai Binh's own accounts credit points.
  - Shares are self-reported and unverified.
  - Never build or claim an "in-app comment as the employee" feature.
- **Identity = Facebook Login (`public_profile`) + employee profile + admin approval.** Accounts are bound by a one-time code that the employee comments on a pinned verification post.
- **Rewards = recognition + small prizes for breadth of participation**, after legal review. No pay-per-like, no scripted comments.
- **Stack:** Next.js (App Router, TypeScript strict), Vercel, Neon Postgres, Drizzle ORM, Auth.js. UI: Tailwind generated from the design-system tokens, Radix primitives, Lucide icons (a flagged substitute for the brand's 3D icons), `motion`, `canvas-confetti`. Each new dependency needs an ADR.
- **Language:** Vietnamese-first UI, with English secondary.

## Design system
- **Source of truth:** https://claude.ai/artifact/DWNMgAxFRgSUc4PWrAo1C1. Offline snapshot: `projects/thai-binh-social-hub/design-system/` (read `SOURCE.md`).
- **Brand rules to respect:**
  - Montserrat everywhere
  - navy/red palette with exact hexes from `tokens.json`
  - no emoji in UI chrome
  - `sky` only at ≥32px
  - white on `red-signal` only at ≥17px medium
  - one sector accent per surface
  - never recolour or redraw logos or the 3 Décadas ring art
- **New layer:** the App & Gamification layer (mobile type scale, motion tokens, Level Ring, Points Pop, Podium, Mission Card and so on) is new. It needs brand-owner approval before it's treated as part of the brand.

## Code conventions
- **Modules** live in `src/modules/<module>/{domain,application,infrastructure,ui}`:
  - `identity`, `social`, `gamification`, `rewards`, `admin`, `platform`
  - cross-module imports go only through each module's `index.ts`, enforced by ESLint boundary rules
  - `src/app` holds routes only
- **Validation:** Zod at every boundary (HTTP, webhooks, env, forms).
- **Ledger:** points live in an append-only `point_ledger`. Corrections are compensating entries, never updates.
- **Webhooks:** verify `X-Hub-Signature-256` and store raw events idempotently before processing.
- **Commits:** Conventional Commits.
- **Secrets:** never in code or docs. `.env*` is git-ignored and unreadable to Claude under the Orcasus deny rules. Record secret **names** only.

## Testing (per /efficient-testing)
- Use Vitest (unit, component and integration against a Neon branch) and Playwright (3–5 critical flows).
- Screenshot, trace and video budgets are **0**.
- Recorded real Meta webhook payloads are fixtures only. They never stand in for the live integration.

## Approval-gated actions
These need explicit owner approval:
- production deploys
- paid plans (Vercel Pro, Neon paid tier)
- publishing to the shared design-system artifact
- Meta App Review submission
- any external communication

## Current status
Phase 0 (discovery, decisions, design) has **not started**. The owner actions in `HANDOFF_LOCAL.md` §7 are open.
