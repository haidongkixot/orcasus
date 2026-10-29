# Pilot: Orcasus S0–S10 on tbagri-web (2026-10-29)

The first run of the full Orcasus v2.3.0 lifecycle on a real production repository. The change was an urgent authentication and personal-data fix in a private Next.js/Prisma site. Exploit details are intentionally left out; the private repository holds the full records (PR haidongkixot/tbagri-web#1, branch `ccr-6f83693d-3hxz8f`, head `07c656f`).

## Outcome

| Item | Result |
|---|---|
| Lifecycle artifacts | 11/11 stages written: intake, readiness and discovery, trace matrix, ADR with debate, backlog, test plan, readiness, security review, closeout, governance audit, retro, knowledge proposals |
| Code status | PR open, not merged or deployed (owner decision). Waits on the owner setting the signing secret and answering 3 open questions |
| Tests | 0 → 31 (`node:test` + existing `tsx`); typecheck, lint and build pass; a mutation check showed the negative table catches a removed guard |
| Independent security review | APPROVE WITH CHANGES; all requested changes applied |
| Governance audit | **FAIL** at the reviewed head (3 FAIL, 4 UNVERIFIABLE): self-accepted assumption, incomplete debate record, closeout missing at audit time. Record fixes applied; gate order not provable after the fact |
| Orcasus tooling on a real repo | `check_knowledge_links.py` caught 8 trace-matrix discipline errors in the pilot's own records; fixed |
| Owner decisions | 5 answered, 3 open |

## What this proves and what it doesn't

- **Proven:** the S0–S10 skills produce usable, linked records on a real codebase. Discovery found more than the owner knew (7 findings, plus 5 more in the debate). Independent review and audit found real defects in the agent's own work, including a build-breaker and weak tests.
- **Not proven:** that the fix works in production (post-deploy checks pending); Agent Teams debate capture (unavailable in the cloud session, so subagents were used and capture is NOT VERIFIED); auditor independence (same session; the owner should countersign).

## Proposed Orcasus changes from the retro (all PROPOSED, need owner approval)

1. Only the owner may set ASSUMPTION-ACCEPTED; the checker enforces an owner and date.
2. Subagent-mode debate protocol with verbatim ballots and voter-scored matrix.
3. Intake enumerates domain values (roles, statuses) before policy questions.
4. Commit S0–S5 records before code; closeout before audit; security review saved to `reports/`.
5. Read-only Bash for `security-reviewer` (tool-grant change).
6. Allow reading `.env.example` (permission change).
7. Allowed-path tests assert exact statuses.
8. Document the conflict between stop hooks and review-before-push.
