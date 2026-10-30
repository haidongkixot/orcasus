# AI SDLC Stage Map — Orcasus v2.3.0

This map shows how Orcasus covers the 11-stage AI SDLC lifecycle (S0–S10): what AI does, what is fenced, and what stays human at each stage. Each row names the owning skill, the agents involved, the evidence the stage must leave and the human decision that closes it. Skills are cited by name; their procedures live in `.claude/skills/<name>/SKILL.md`.

| Stage | Owning skill(s) | Agents | What AI does | Fence (guardrail) | Stays human | Evidence left behind |
|---|---|---|---|---|---|---|
| S0 Intake | `change-intake` | product-manager, product-analyst | Classify change type and risk; search records for duplicates and conflicts; draft intent and value | No unrequested scope, metrics or deadlines; UNKNOWN is not NEW; scope lock forces reclassification; domain values listed before policy questions; intake committed before code (hotfix lane: other records before merge) | Confirm intent and value; confirm the hotfix lane | `docs/agent-ops/INTAKE_RECORD.md` |
| S1 Understand | `project-discovery` | any role, read-only reconnaissance | Inventory repo, assets, integrations, credentials (presence only), environments, test resources | Evidence for every AVAILABLE; no substitutes while readiness is UNKNOWN | Validate the discovery summary | `READINESS_MATRIX.md`, `DISCOVERY_SUMMARY.md` |
| S2 Explore | `platform-discovery`, `team-debate` (EXPERIMENT state) | product-manager, domain-architect, ux-researcher, devil-advocate | Draft brief, capability map, options and spikes | Non-goals and one vertical slice constrain scope | Define goals and non-goals | `projects/<slug>/PRD.md`, `CAPABILITY_MAP.md`, `ROADMAP.md` |
| S3 Requirements | `requirements-traceability` | product-analyst, product-manager, qa-automation-engineer | Draft requirements and acceptance criteria with citations; check each citation | VERIFIED / PARAPHRASE-OK / MISMATCH / UNVERIFIABLE / NO SOURCE; uncited rows cannot be APPROVED; only the owner sets ASSUMPTION-ACCEPTED (checker enforces name and date); link checker | Approve scope and acceptance criteria; accept assumptions | `TRACE_MATRIX.md` |
| S4 Solutioning | `team-debate`, ADR template | domain-architect, devil-advocate, specialists, team-secretary | Propose and score options | Reference architecture, weighted matrix, explicit ballots, Devil's Advocate; subagent mode with verbatim ballots when Agent Teams are unavailable | Core design decision | ADR in `decisions/`, meeting records |
| S5 Backlog | `backlog-slicing` | product-manager, product-analyst, qa-automation-engineer | Slice into testable vertical slices; propose priority with a named frame | Testability verdict per slice; BLOCKED slices not mocked; guessed inputs marked ESTIMATE | Priority and backlog order | `projects/<slug>/BACKLOG.md` |
| S6 Readiness Gate | `project-discovery` (pre-build), `delivery-readiness` (pre-release) | orchestrator, qa-automation-engineer, reviewers | Check dependencies and evidence | READY / PARTIAL / BLOCKED; NOT READY or INSUFFICIENT EVIDENCE blocks release | Release readiness and deployment | readiness decision, `reports/<milestone>-readiness.md` |
| S7 Build | `vertical-slice-delivery`, `efficient-testing` | frontend, backend, mobile, integration, data engineers | Write code and tests for one slice | Intake scope contract and file ownership; permission `ask` rules on commit, push, merge, deploy and `rm` | Oversight of approvals and boundary crossings | diff, test plan, command results |
| S8 Review & Test | `efficient-testing`, `design-quality-gate`, `delivery-readiness` | qa-automation-engineer, security-reviewer, performance-reviewer, product-designer | Independent multi-lens first pass | Reviewers inspect actual outputs; zero-capture default; no weakened assertions | The merge decision (`gh pr merge` asks) | review findings, test evidence |
| S9 Close & Adapt | `closeout-report`, `governance-audit`, `process-retro` | governance-auditor, team-secretary | Summarize closeout, audit against gates, propose process changes | Mandatory not-done section; closeout before audit; gate-order control from git; PASS / FAIL / UNVERIFIABLE with primary evidence; proposals only | Approve process changes | `reports/*-closeout.md`, `*-governance-audit.md`, `*-retro.md` |
| S10 Knowledge | `knowledge-curation` | knowledge-steward, team-secretary | Link durable knowledge with tracked sources; keep memory clean | Required sources, absolute dates, no secrets, link checker in CI; agents never approve | Curator approval | `knowledge/INDEX.md` |

## Cross-cutting controls

- **Owner decisions:** blockers and material trade-offs return to the owner with options and a recommendation (`CLAUDE.md`, discovery gate).
- **Meeting records:** `team-secretary` and `meeting-record`; capture status is CAPTURE VERIFIED only after live multi-teammate testing.
- **Hook runtime:** every hook runs Python through `scripts/hooks/run_python.sh`; a SessionStart check reports whether logging can run, and launch failures are written to `meetings/HOOK_ERRORS.log`.
- **Package CI:** `.github/workflows/validate.yml` runs the bundle validator, skill eval validation, logger, launcher and link-checker tests and the knowledge/citation link check on every pull request.

## Evidence status

Every skill above is **EXPERIMENTAL** until the live eval scorecard marks it PROVEN (thresholds and current results in [EVIDENCE.md](EVIDENCE.md)). Agent Teams capture is proven only by the [runtime acceptance runbook](RUNTIME_ACCEPTANCE_RUNBOOK.md).

## Limits

Static checks and CI prove file contracts, configuration and script behavior. They do not prove that agents choose the right skill, that Agent Teams messaging works in a given runtime or that a resolving citation supports its claim. Use `python3 scripts/skill_evals.py sheet` for live skill evals and `docs/ACCEPTANCE_TESTS.md` for runtime checks.
