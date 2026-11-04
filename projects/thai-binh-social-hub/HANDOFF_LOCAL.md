# Handoff: continue Thai Binh Social Hub on a local computer

Prepared 2026-11-04 at the end of a cloud session. This guide moves the work to Claude Code on your own computer, signed in with your Claude account.

## 1. What exists today
All of it is pushed to `haidongkixot/orcasus`, branch `ccr-e6d85c90-14dl5b`, folder `projects/thai-binh-social-hub/`:

| Path | What |
|---|---|
| `PLAN.md` | Approved plan: architecture, gamified UX/UI layer, Orcasus application, phases, owner blockers, token estimate, verification |
| `Thai-Binh-Social-Hub-BOD-Pitch-VI.pptx` | 13-slide Vietnamese board deck with speaker notes |
| `deck/build.js`, `deck/README.md` | Deck generator and rebuild steps |
| `design-system/` | Offline snapshot of the Thai Binh design system (tokens, brand book, CSS); see `SOURCE.md` |
| `bootstrap/install-orcasus.sh` | Creates the new app repo with Orcasus installed (tested: validators 58/0, logger tests 5/5) |
| `bootstrap/CLAUDE.project.md` | Project section appended to the new repo's `CLAUDE.md` |
| `HANDOFF_LOCAL.md` | This file |

**Not started:** Phase 0 (discovery records, PRD, ADRs, debate, test plan, designs). No application code exists yet. That's expected: the Orcasus gates come first.

## 2. Repo visibility (decide first)
`haidongkixot/orcasus` is a **public** repository. The plan and the deck (which contains Thai Binh logos and internal strategy) are now publicly visible on that branch.

- **Recommended:** keep the project in a **private** repo `tb-social-hub` (step 4 below creates it), then delete the branch `ccr-e6d85c90-14dl5b` from the public `orcasus` repo once the private repo holds everything.
- Deleting the branch is irreversible and is your call. Forks or caches may already hold copies. Ask Claude to do it only after the private repo is pushed.
- Don't merge this branch into the public `orcasus` main.

## 3. Install on the new computer
| Tool | Why | Check |
|---|---|---|
| Git | Clone, commit, push | `git --version` |
| Node.js 22 LTS (20+ works) | Next.js app, deck rebuild | `node -v` |
| Python 3 | Orcasus hooks and validators | `python --version` or `python3 --version` |
| Claude Code | The agent; install per https://code.claude.com/docs/en/setup | `claude --version` |
| VS Code + Claude Code extension (optional) | Orcasus setup docs assume VS Code | — |
| Montserrat font | Brand font, for the deck and design work | installed from Google Fonts |
| Later: Vercel CLI, Neon CLI (`neonctl`), GitHub CLI `gh` | Deploy previews, DB branches, PRs | when Phase 2 starts |

Windows: use Git Bash or WSL to run the bootstrap script. Orcasus hooks call `python`, and the script rewires them to `python3` or `py` if `python` doesn't exist.

## 4. Steps
```bash
# 4.1 Get the plan + Orcasus
git clone https://github.com/haidongkixot/orcasus.git
cd orcasus
git checkout ccr-e6d85c90-14dl5b

# 4.2 On github.com create an EMPTY private repo: haidongkixot/tb-social-hub (no README, no licence)

# 4.3 Build the new app repo with Orcasus installed (validates and makes the first commit; no push)
bash projects/thai-binh-social-hub/bootstrap/install-orcasus.sh ../tb-social-hub

# 4.4 Publish it to the private repo
cd ../tb-social-hub
git remote add origin https://github.com/haidongkixot/tb-social-hub.git
git push -u origin main

# 4.5 Start Claude Code in the new repo
claude        # first run: /login with your Claude account, then trust this folder
```

After launch, check inside Claude Code:
- `/agents` lists the 15 Orcasus roles.
- The 9 Orcasus skills, such as `/project-discovery`, show up as slash commands.
- `.claude/settings.json` turns on experimental Agent Teams (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`). Whether teams and peer messaging actually work on your installed version is **NOT VERIFIED**. The Orcasus initialization prompt in `INITIALIZE_AGENTS.md` tests that.
- Keep the default permission mode from Orcasus (`acceptEdits`, with asks for push, deploy and `rm`). Don't use `--dangerously-skip-permissions` on your workstation.

## 5. Local vs cloud: what changes
| Topic | Cloud session (used so far) | Local |
|---|---|---|
| GitHub | Via the session's GitHub app | Your own git credentials; `gh` optional |
| claude.ai connectors (Vercel, Neon, Figma, Canva, Google) | Were attached to the cloud session | **NOT VERIFIED** whether your account's connectors appear in local Claude Code. If not, add MCP servers with `claude mcp add` (see the Claude Code MCP docs) or use the Vercel/Neon CLIs. |
| Design system artifact | Read with the Artifact tool | The link opens in your browser. Whether local Claude Code can read artifacts directly is **NOT VERIFIED**; the offline snapshot in `design-system/` is enough to start. |
| Network | Proxy-restricted (`developers.facebook.com` was blocked) | Your normal internet, so Meta's docs can be checked directly |
| Secrets | None used | Create `.env.local` yourself (step 7). Orcasus blocks Claude from reading `.env*`. |
| Token use | Counted on the cloud session | Counts against your Claude plan's limits. The estimate is in PLAN.md (~115–130M input tokens, mostly cached). |

## 6. First-session prompt (paste into Claude Code in `tb-social-hub`)
> Read CLAUDE.md, projects/thai-binh-social-hub/PLAN.md and projects/thai-binh-social-hub/HANDOFF_LOCAL.md. Then run the Orcasus initialization check from INITIALIZE_AGENTS.md: run both validation scripts and report the exit codes, and say whether Agent Teams and peer messaging really work in this local runtime. Then start Phase 0 of the plan:
> - Run /project-discovery and create docs/agent-ops/READINESS_MATRIX.md and DISCOVERY_SUMMARY.md. Mark the Meta, legal, brand, Vercel and Neon items honestly (UNKNOWN or MISSING until verified).
> - Run /platform-discovery and write PRD.md, CAPABILITY_MAP.md, ROADMAP.md and RISK_REGISTER.md under projects/thai-binh-social-hub/.
> - Write ADR-001 to ADR-003 in decisions/ from the owner decisions already recorded in the plan.
> - Propose the /team-debate setup for the gamification rules (ADR-004), but wait for my go before running it.
>
> Don't scaffold Next.js, install packages, connect paid services or deploy yet. Stop and report blockers and the owner decisions you need from me.

## 7. Owner actions (open)
1. **Repo:** create the private `tb-social-hub` repo (step 4.2). Decide whether to delete the public `orcasus` branch (section 2).
2. **Meta:**
   - admin access to Thai Binh's Business Manager, Pages and linked IG Business accounts
   - create the Meta app (Business type) and start Business Verification
   - plan for App Review of `pages_show_list`, `pages_read_engagement`, `pages_read_user_content`, `pages_manage_metadata`, `instagram_basic`, `instagram_manage_comments`, `business_management`

   This is the critical path.
3. **Board:** present the deck. First fill the slide 2 figures from Meta Business Suite and the slide 11 costs.
4. **Legal/HR:** review program rules and prizes against Meta's policies and Vietnam's PDPL (effective 01/01/2026) and Decree 13/2023. Decide who approves employee accounts and whether to import an HR list.
5. **Brand:** approve the Level Ring and swoosh-derived components and the emoji policy, and supply the 3 Décadas ring art, the 3D icon PNGs and real photography.
6. **Vercel/Neon:** team access, plan tier (Pro for frequent crons is paid), domain.
7. **Secrets:** when Phase 2 starts, create `.env.local` (never committed) with these **names**; values come from you:
   - `AUTH_SECRET`
   - `AUTH_FACEBOOK_ID`
   - `AUTH_FACEBOOK_SECRET`
   - `META_APP_SECRET`
   - `META_WEBHOOK_VERIFY_TOKEN`
   - `TOKEN_ENCRYPTION_KEY`
   - `DATABASE_URL`

   Store the same names in Vercel project environment variables for previews and production.
