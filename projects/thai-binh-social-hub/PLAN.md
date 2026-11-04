# Plan — Thai Binh Social Hub (employee social-advocacy + gamification platform)

## Immediate next steps (this session, after approval)
1. **Save the plan in the repo.** Copy this plan to `projects/thai-binh-social-hub/PLAN.md` in `orcasus`, commit it on branch `ccr-e6d85c90-14dl5b`, and push with `git push -u origin ccr-e6d85c90-14dl5b`.
2. **Build the board pitch deck (Vietnamese).** Presenter: the Marcom Director. Audience: the Board of Directors (BOD/HĐQT).
   - **Format:** a Slides artifact (quickstart `intent: "slides"`) built on the **Thai Binh design system** (https://claude.ai/artifact/DWNMgAxFRgSUc4PWrAo1C1). That system was extracted from the corporate 1440×810 deck, so it fits well: navy/red, Montserrat, circle-photo ring motif, section dividers on `royal`, logo top-right. It downloads as .pptx/PDF.
   - **Language:** Vietnamese throughout, with UPPERCASE noun-led titles and no emoji, per the brand.
   - **Figures:** concrete and **sourced**, per the brand rule. Where Thai Binh's own data is missing (Page followers, reach, engagement), the slide shows a clearly marked placeholder "[Số liệu cần bổ sung]". Numbers are never invented.
   - **Outline (13 slides):**
     1. **Bìa (Cover):** THAI BINH SOCIAL HUB / "Nền tảng kết nối nhân viên với kênh truyền thông Thái Bình" ("A platform connecting employees with Thai Binh's channels"). Presenter: Giám đốc Marcom (Marcom Director).
     2. **Bối cảnh & cơ hội (Context & opportunity):** 1000+ employees as 1000+ brand ambassadors; why employee engagement amplifies organic reach (sourced data); the current state of TB's channels (placeholder).
     3. **Section 01: Giải pháp (Solution)**, as a royal divider.
     4. **Thai Binh Social Hub là gì? (What is it?):** 3 value cards: Kết nối (Connect), Gắn kết (Engage), Ghi nhận (Recognise).
     5. **Hành trình nhân viên (Employee journey):** a timeline from FB login → profile → approval → missions → interact on FB/IG → points → rewards.
     6. **Gamification:** Level Ring, badges named after the 5 core values, department leaderboards, campaigns, prizes for breadth of participation.
     7. **Trải nghiệm (Experience):** mobile screen mockups (Today, Feed, Leaderboard, Celebration) with a cheerful style on the brand system. They're labelled "thiết kế minh hoạ" (illustrative design), not the real product.
     8. **Section 02: Triển khai (Rollout)**, as a divider.
     9. **Lộ trình (Roadmap):** Phases 0–4 with estimated weeks. Meta App Review is the critical path.
     10. **Tuân thủ & quản trị rủi ro (Compliance & risk):** Meta policy (no buying or trading likes), PDPL 2026 and Decree 13, anti-inauthentic engagement, honest limits (actions happen in the FB/IG app; shares can't be verified).
     11. **Ngân sách & nguồn lực (Budget & resources):** a cost structure of infrastructure (Vercel/Neon), AI development (the token estimate), prize fund and staff time. Figures marked "ước tính" (estimate) or "cần báo giá" (quote needed); vendor prices are verified before they're written in.
     12. **KPI & đề xuất phê duyệt (KPIs & approval request):** KPIs (active-employee rate, verified engagements per month, Page reach growth, campaign participation). The ask: approve the pilot of 50–100 people, the budget, Meta Business access, and legal review.
     13. **Cảm ơn (Thank you):** closing, royal ground.
   - **Brand assets:** use the system's real logos (color/white lockups and the 3 Décadas mark). Real company photography isn't in the system, so photo slots use neutral placeholders marked "[Ảnh thật cần bổ sung]" (real photo needed), never generated photos. Line icons are a flagged substitute for the missing 3D icons.
   - **Checks:** text contrast, a Vietnamese diacritics check in Montserrat, no fabricated figures. A data-gap list is handed to the Marcom Director together with the deck link.
3. Phases 0–4 below start only after BOD approval and the owner actions are done.

## Context
Thai Binh Corp (1000+ employees) wants an internal, mobile-first web app where staff:
- sign in with Facebook
- browse the company's fanpages, Instagram accounts and their posts
- engage with those posts
- take part in gamification programs that encourage them to interact with company channels

The UI must use the **Thai Binh Corp design system** with a **more gamified, fun, cheering style**. The project must follow **Orcasus fully**, with **Next.js** as the code framework.

### Owner decisions already made
| Topic | Constraint found in discovery | Decision |
|---|---|---|
| Engagement | Since 2018, an API comment on a Page post can only be posted *as the Page*; commenting as a user returns error 1705. No API reacts or shares as a user. IG comment creation only works on media the account owns. | **Hub + deep link + webhook attribution.** Our app lists posts and campaigns. Comment/React opens the post in the FB/IG app in one tap, and Share uses the Share Dialog or native share sheet. Webhooks on Thai Binh's own Pages/IG accounts credit points. Shares are self-reported/unverified. |
| Sign-in | Facebook Login doesn't prove someone is an employee. IG login only works for Business/Creator accounts. | **Facebook Login + basic employee profile + admin approval.** Facebook and Instagram accounts are proven with a one-time code (below). |
| Rewards | Meta Developer Policies forbid trading Likes/Shares/Comments for value, and there's an inauthentic-behaviour risk. | **Recognition + small prizes, after legal review.** Reward breadth of participation, not pay-per-like. No scripted comments. |
| Platform | — | **Mobile-first web app reached by a link**, deployed on **Vercel** with **Neon Postgres**. |
| Framework | — | **Next.js**, built with the **Orcasus** operating system applied fully. |
| Code home | — | **New dedicated repo** (proposed name `tb-social-hub`) with Orcasus installed. |
| Design system | — | Claude artifact "Thai Binh Corporation" (https://claude.ai/artifact/DWNMgAxFRgSUc4PWrAo1C1). |

### What the design system contains (read 2026-11-04)
- **Tokens:**
  - navy family (`navy #00377b`, `heading #0c3469`, `ink #002060`, `royal #1c489c`, `navy-panel`, `navy-block`)
  - reds (`red-signal #eb2127`, `red-headline #df1f2b`, `red-block #ed1d24`, logo `red`)
  - light grounds (`mist`, `ice`, `blush`) and `sky`, `sky-tint`, `cyan`, `decadas-cyan #19b1e7`
  - sector accents: TBFood orange, TBAgri greens, TBComm teal
  - Montserrat 400–700
  - `radius-card 20px`, `radius-none` for tags and bars, `radius-full`
  - `shadow-card`
  - light theme = content slides; dark theme (`royal`) = section dividers
- **Motifs:** a circle photo framed by a cyan→red ring ending in the 3 Décadas open hand; the red swoosh that closes sector slides; stepped squares (navy-panel, navy-block, red-block); a timeline with red-signal ring dots.
- **Rules:**
  - no emoji
  - `sky` only at ≥32px (it's 2.25:1)
  - `cyan` on royal only for display numbers
  - white on `red-signal` only at ≥17px medium
  - red is an accent, never a ground for long text
  - one sector accent per surface
  - use the source ring art; don't redraw it
  - icons are glossy 3D rasters, which are **not included**; substitute navy line icons with red-signal accents and flag the substitution
- **Gaps for an app:**
  - it was extracted from a slide deck at 1440×810, so it has no mobile type scale
  - no app components (buttons, inputs, nav, lists, sheets, toasts, dialogs)
  - no motion tokens
  - no gamification patterns
  - voice is English/Spanish, while employees need Vietnamese

## Recommended architecture
- **Next.js (App Router, TypeScript strict) modular monolith** on Vercel. Server Actions and route handlers serve as the API, and the app is an installable PWA. Vietnamese is the primary UI language (`next-intl`), with English secondary.
- **Neon Postgres + Drizzle ORM**, with versioned migrations and a Neon branch for each Vercel preview and for integration tests.
- **Auth.js Facebook provider** with the `public_profile` scope (no App Review needed) and database sessions.
- **UI stack:**
  - Tailwind CSS, with the theme **generated from the design system's `tokens.json`** by a build script, so the brand is the single source
  - Radix UI primitives for accessible dialogs, sheets, tabs and toasts
  - Lucide line icons as the flagged substitute for the missing 3D icons
  - `motion` for animation, respecting `prefers-reduced-motion`
  - `canvas-confetti` in brand colours only

  All new dependencies are recorded in an ADR, per Orcasus.
- **Meta integration module:**
  - An admin connects each Page and IG Business account via Facebook Login for Business. Page tokens are stored encrypted, with the key in a Vercel env var.
  - Permissions: `pages_show_list`, `pages_read_engagement`, `pages_read_user_content`, `pages_manage_metadata`, `instagram_basic`, `instagram_manage_comments`, `business_management`. These need **App Review + Business Verification**.
  - Post sync: `feed` webhooks plus a Vercel Cron reconcile job, with posts cached in Neon.
  - `POST /api/webhooks/meta` checks `X-Hub-Signature-256` and stores raw events idempotently (unique provider event key) before they're processed into the points ledger.
- **Modules:**
  - `identity`: accounts, profiles, approval, roles
  - `social`: pages, posts, identity binding, webhooks
  - `gamification`: campaigns, missions, rules engine, append-only `point_ledger`, levels, badges, streaks, leaderboards
  - `rewards`: prize periods, winners, fulfilment
  - `admin`
  - `platform`: audit, rate limits, observability
- **Core tables:** `users`, `employee_profiles` (code, name, department, site, phone, status pending/approved/rejected/suspended), `departments`, `roles`, `social_accounts`, `posts`, `social_identities`, `engagement_events`, `point_ledger`, `campaigns`, `missions`, `levels`, `badges`, `user_badges`, `streaks`, `prize_periods`, `awards`, `audit_log`, `consents`.

### Identity binding
Facebook Login gives an app-scoped ID, and webhook `from.id` may use a different scope. Instagram personal accounts can't sign in at all. So each employee proves ownership once:
1. The app shows a one-time code, such as `TB-7K3Q`.
2. The employee comments it on a pinned verification post on the Page or IG account.
3. The webhook binds `from.id` / `from.username` to the employee in `social_identities`, and the comment is then hidden via the Page token.

### Gamification rules (finalised by `/team-debate` + legal review → ADR-004)
- Points for verified comments and reactions on company posts, with daily and per-post caps.
- Comments must meet a minimum length and must not repeat the user's earlier comments or be copied templates.
- A deleted comment (webhook `remove` verb) reverses its points through a compensating ledger entry.
- Shares: low points, flagged self-reported, never enough to win a prize on their own.
- Missions and campaigns run in time windows. Streaks have a weekly "freeze" so they stay forgiving.
- Leaderboards by individual, department and site.
- Prizes per period for breadth of participation (for example, joined ≥ N campaigns), with program rules published in-app.
- Abuse controls: anomaly flags, an admin review queue, suspension.

## UX/UI plan — "Thai Binh, but cheering"
**Principle:** keep the brand recognisable and corporate-proud, and get the fun from **motion, progress, celebration and warm copy**. No new colours, emoji or invented brand art. Every new element is derived from existing tokens and motifs and documented as an **App & Gamification layer** of the design system.

### 1. App foundation layer (new tokens, derived from the brand)
- **Mobile type scale**, Montserrat, keeping the slide styles' role mapping:
  - `app-display` 28/34 700 uppercase (from `section-title`)
  - `app-title` 20/26 700 uppercase (from `slide-title`)
  - `app-card-title` 16/22 700
  - `app-body` 15/22 400
  - `app-label` 13/18 600
  - `app-caption` 12/16 500
  - `app-number` 32–48 700 tabular, for points, ranks and counters
- **Grounds:** `mist` for the app background, white cards with `radius-card` and `shadow-card`, `ice` for section bars and the bottom nav. Celebration and level-up screens use the **dark theme** (`royal` ground, white text, `cyan` display numbers), echoing the brand's section dividers.
- **Accents:** `red-signal` for primary CTAs and active states. Text on it is ≥17px medium, so buttons are 17px/600; small text uses `red-headline` instead. `decadas-cyan` is for progress and decoration, never text.
- **Teams:** department or business-unit teams may take one sector accent (TBFood orange, TBAgri green, TBComm teal), one accent per card.
- **Motion tokens:** `pop` (spring, 250ms), `celebrate` (600ms), `count-up` (800ms). Everything degrades to a fade under reduced motion.
- **Contrast checks:** `sky` is used only ≥32px or not at all in the app. Every pair is checked to 4.5:1 (3:1 for large text and icons), in both themes.

### 2. Gamified components (built on the brand motifs)
| Component | Brand source | Fun factor |
|---|---|---|
| **Level Ring avatar** | circle photo + cyan→red ring | The employee's photo sits in a ring that fills cyan→red as they progress to the next level, and pulses on gain. A new derived component: needs brand-owner approval because the brand says not to redraw the ring art. |
| **Points Pop** | `red-signal` tag, square | A "+10" square tag springs from the action button and counts up into the header total. |
| **Mission Card** | InfoCard (white, `radius-card`, red underline) | Progress bar, countdown chip, "Nhận thưởng" (claim) button that bursts brand confetti. |
| **Campaign Hero** | SectorTitle + bottom **swoosh** | A kicker plus a heavy title on a photo, ending in the campaign's accent swoosh. |
| **Podium / Leaderboard** | stepped squares (navy-panel, navy-block, red-block) | Top 3 stand on stepped squares, then "you" and your nearest rivals, with a rank-change arrow. |
| **Streak Timeline** | TimelineMilestone (red ring dots on a navy line) | Days glow as dots, with a "freeze" token shown as an `ice` dot. |
| **Badge medallion** | `radius-full` icon disc + core values | Five badge families named after the core values: Chính trực (Integrity), Tận tâm (Dedication), Sáng tạo (Creativity), Kiên trì (Perseverance), Vững mạnh (Strength). Locked badges show as silhouettes. |
| **Level-up / Celebration sheet** | Section divider (`royal`, `cyan` number) | A full-screen moment: big cyan level number, cheering line, confetti, and a share-to-team action. |
| **Banner bar** | BannerBar | Section headers: "NHIỆM VỤ HÔM NAY" (today's missions), "BẢNG VÀNG" (hall of fame). |

Standard app components are also needed: Button, IconButton, Input, Select, BottomNav, Tabs, Sheet, Dialog, Toast, Skeleton, EmptyState, Avatar, Chip and PostCard. Each gets loading, empty, error, success, disabled and permission-denied states.

### 3. Voice — cheering, in Vietnamese
- A warm, upbeat, team-spirited tone, for example "Tuyệt vời! +10 điểm cho Tận tâm" ("Great! +10 points for Dedication") and "Còn 2 nhiệm vụ nữa là lên cấp!" ("2 more missions to level up!").
- Celebrate effort, never shame. Below the top 10, leaderboards show the employee's own progress and nearest peers instead of a bare rank. People can opt out of public ranking.
- Titles stay UPPERCASE and noun-led, per the brand. No emoji in UI chrome, per the brand rule; fun comes from motion and illustration. Relaxing this rule is an **owner/brand decision**.
- A microcopy library (vi/en) covers every state, celebration and error. Reviewed with `design:ux-copy`.

### 4. Screens (mobile-first, 360–430px primary; responsive up to an admin desktop)
1. **Onboarding:** FB login → consent (PDPL) → profile → "waiting for approval" screen with progress and a cheerful note. A first-run tour of points and missions follows.
2. **Home ("Hôm nay", Today):** Level Ring header with points, streak, today's missions, and the live campaign hero.
3. **Feed:** posts from all Pages and IG accounts, with filter chips. Each card has Comment/React/Share deep-link actions and a "points available" tag.
4. **Post detail:** after the employee returns from the FB/IG app, a "points pending" toast appears, then a live Points Pop when the webhook confirms.
5. **Campaigns:** list and detail, with rules, countdown and progress.
6. **Leaderboard:** tabs for Individual, Department and Site; podium plus the "near you" section.
7. **Me:** badges wall, level history, linked accounts with identity verification, notification settings.
8. **Admin (desktop-first):** approvals queue, Pages/IG connections, campaign and mission builder, rules and caps, abuse queue, prize periods, analytics and CSV export.

### 5. Design deliverables and gates
- **D1.** An **App & Gamification layer** for the Thai Binh design system. It goes as a new section in the design system artifact, so the brand stays the single source: tokens, `README` section and component guidelines. It's published only after owner approval, since the artifact is shared with other editors (last edited by "Quijote").
- **D2.** Hi-fi mobile designs of the 8 screens and the key celebration moments, on a design canvas using this design system (Claude Design, or Figma via MCP if the team prefers). Also an interactive prototype of the core loop: mission → deep link → points pop → level up.
- **D3.** `/design-quality-gate` review: hierarchy, contrast, reduced motion, touch targets ≥44px, focus, Vietnamese text length.
- **D4.** A small usability check with 5–8 employees from two sites, including factory/field staff on low-end Android, run with `ux-researcher` before building Phase 3.

## Orcasus application (new repo `tb-social-hub`)
- **Install Orcasus v2.2.0:** copy `CLAUDE.md`, `.claude/` (settings with Agent Teams and logger hooks, 15 agents, 9 skills), `scripts/`, `templates/` and `docs/` from `haidongkixot/orcasus`. Add a project section to `CLAUDE.md` (stack, module boundaries, Meta constraints, design-system link). Pass `python scripts/validate_bundle.py` and `python scripts/test_meeting_logger.py`.
- **Next.js code conventions, recorded as `docs/CODING_CONVENTIONS.md` + ADR:**
  - `src/modules/<module>/{domain,application,infrastructure,ui}`; modules import each other only via their `index.ts` public API, enforced by an ESLint boundaries rule
  - `src/app` for routes only
  - TypeScript strict, Zod at every boundary
  - Conventional Commits
  - no secrets in code; `.env*` is already denied by the Orcasus settings
- **Gates in order:** `/project-discovery` → `/platform-discovery` (PRD, capability map, roadmap) → `/team-debate` for material choices → `/efficient-testing` → `/vertical-slice-delivery` → `/design-quality-gate` → `/delivery-readiness`.
- **Agent Team:** a real team of 4–5 when we start:
  - `product-manager`: PRD and gamification rules
  - `product-designer` + `ux-researcher`: owns `src/modules/*/ui`, the design system layer and the designs
  - `integration-engineer`: owns `src/modules/social`, Meta and webhooks
  - `backend-engineer`/`data-platform-engineer`: owns `gamification`, `identity`, schema and migrations
  - `team-secretary` for debates; `security-reviewer` and `devil-advocate` at review gates

  File ownership is explicit, with no concurrent edits to the same files.
- **Durable records:**
  - `docs/agent-ops/READINESS_MATRIX.md`, `DISCOVERY_SUMMARY.md`, `TEST_PLAN.md`
  - `projects/thai-binh-social-hub/PRD.md`, `CAPABILITY_MAP.md`, `ROADMAP.md`, `RISK_REGISTER.md`
  - `decisions/ADR-001` engagement model, `ADR-002` identity/approval, `ADR-003` stack (Vercel, Neon, Next.js, UI libs), `ADR-004` gamification rules, `ADR-005` design-system app layer
  - meeting records in `meetings/`

## Phased delivery
- **Phase 0 — Discovery, decisions, design.** Orcasus install, readiness records, PRD, ADRs, gamification debate, test plan, design deliverables D1–D3.
- **Phase 1 — Technical spike (must pass before Phase 2).** On a test Page in Meta Development mode, confirm that:
  - (a) the `feed` webhook delivers comments and reactions with a usable `from.id`
  - (b) the IG `comments` webhook delivers `from.username`/`id`
  - (c) code-based identity binding works
  - (d) deep links open the native apps from iOS Safari, Android Chrome and the Zalo/Messenger in-app browsers
  - (e) Graph API rate limits fit post sync

  Evidence goes in `evidence/`. If (a) or (b) fails, return to the owner.
- **Phase 2 — Vertical slice.** FB login → profile → approval → identity binding → feed from one Page → Comment deep link → webhook → ledger → Points Pop + Level Ring + department leaderboard. Fully styled with the design system layer. Deployed to a Vercel preview with a Neon branch.
- **Phase 3 — Breadth.** Instagram, campaigns and missions, badges, streaks, celebration sheets, prize periods, abuse queue, admin analytics/CSV, PWA install and web push, D4 usability check.
- **Phase 4 — Pilot → rollout.** Pilot with 50–100 employees in two departments, tune rules and copy, then roll out to 1000+. The production deploy needs owner approval.

## Blockers / owner actions (UNKNOWN until verified)
1. **New repo:** the owner creates `haidongkixot/tb-social-hub`, which I can't create from this session, and attaches it.
2. **Meta:** Business Manager admin access, the Pages and linked IG Business accounts, the Meta app, Business Verification and App Review. This is the critical path and usually takes weeks.
3. **Legal/HR:**
   - program rules and prizes reviewed against Meta Developer Policies and Facebook Promotions Guidelines
   - Vietnam's PDPL (effective 1 Jan 2026) and Decree 13/2023: consent, retention, opt-out
   - the account approver role
   - an optional HR employee-list import
4. **Brand owner approvals:**
   - derived Level Ring and swoosh components
   - emoji policy
   - the App & Gamification layer added to the shared design system
   - whether a mascot is wanted (it would need an illustrator; no generated brand art)
5. **Missing brand assets:**
   - the 3 Décadas ring art as a separate file
   - the brand 3D icon PNGs (otherwise the flagged Lucide substitute is used)
   - an approved photography library
   - the "TBCorp Brand Assets library" mentioned in the design system's history
6. **Vercel/Neon:**
   - team and project access
   - Vercel Pro for crons more frequent than daily (paid)
   - Neon tier
   - domain
7. **Session network:** `developers.facebook.com` must be allowed in the environment's network settings so current Meta docs can be checked during implementation.

## Token-burn estimate (order of magnitude; NOT VERIFIED until measured)

**How the numbers were built:**
- Each agent turn re-reads its context, around 40–80k tokens. Most of that is prompt-cache reads, which cost far less than fresh input.
- Output is about 1–4k tokens per turn, more when writing code or designs.
- Totals = turns per agent × average context × number of agents, plus overhead from the Orcasus gates, reviews and debugging.

| Phase | Who runs | Input tokens (≈85–90% cached) | Output tokens |
|---|---|---|---|
| 0a Orcasus install, discovery, PRD, ADRs, test plan | Main + 3 subagents (PM, analyst, architect) | ~6M | ~0.25M |
| 0b Gamification `/team-debate` (2 cycles) | 5 agents incl. Secretary + Devil's Advocate | ~3M | ~0.1M |
| 0c Design D1–D3 (app layer, 8 screens, prototype, quality gate) | Designer + UX researcher | ~4M | ~0.4M |
| 1 Meta spike | Integration engineer + main | ~2.5M | ~0.1M |
| 2 Vertical slice | Team of 4 + 3 reviewers + main | ~30M | ~1.2M |
| 3 Breadth (IG, campaigns, badges, admin, PWA, D4) | Team of 4–5 + reviewers | ~60–75M | ~2.5–3M |
| 4 Pilot tuning + rollout readiness | Main + 2 agents | ~10M | ~0.4M |
| **Total** | | **~115–130M** (range 70M–200M) | **~5M** (range 3–8M) |

**What drives the range:**
- *Low end:* the spike passes first time, little rework, and lean teams.
- *High end:* App Review rejections, webhook or ID-scope surprises that reopen discovery, design iterations, and flaky E2E debugging.

**Ways to cut cost (built into the plan):**
- **Phase 1 is a hard gate.** If the spike fails, we stop before Phase 2. That avoids roughly 100M tokens.
- Use one session or subagents for sequential work. A full Agent Team is used only for debates and parallel Phase 2/3 work, with 3–4 teammates rather than 5+.
- Run read-only Explore agents and routine coding agents on a smaller model; keep the top model for architecture, security review and the orchestrator.
- Keep screenshot, trace and video budgets at 0, run targeted tests rather than full suites, and keep contexts short with durable docs instead of long chats.

The planning done in this session so far has used roughly 1M input tokens. Dollar cost depends on the model mix and on whether this runs on a subscription or the API; I can convert these numbers to cost on request.

## Verification
- **Static:** `tsc --noEmit`, ESLint (including module-boundary rules), a token-sync check that the Tailwind theme matches `tokens.json`, and a contrast lint over token pairs.
- **Unit (Vitest):**
  - rules engine: caps, duplicates, reversals, windows, streak freeze, level thresholds
  - webhook signature check
  - idempotent ingestion
  - identity-code expiry and reuse
- **Component (Vitest + Testing Library):** gamified components' states, accessible names and focus, and reduced-motion behaviour, asserted via the DOM rather than screenshots.
- **Integration (Neon branch):** migrations, ledger and leaderboard queries, RBAC, approval flow.
- **Contract:** recorded **real** webhook payloads from the Phase 1 spike, used as fixtures only.
- **E2E (Playwright, 3–5 flows):** onboarding → approval, feed → post, mission claim → celebration, admin campaign creation. Screenshot, trace and video budgets are 0 unless a named visual question is approved.
- **Live preview check:**
  - a real comment on the test Page credits points and plays the Points Pop
  - deleting the comment reverses the points
  - an unapproved user is blocked
- **Reporting:** commands, exit codes, test counts and unverified areas are reported per the Orcasus Definition of Done.
