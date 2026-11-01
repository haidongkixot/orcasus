# Team Operating Model — v2.4.0

## Roles
The Lead/Orchestrator scopes and coordinates the work. Product Manager and Analyst define outcomes, workflows and acceptance criteria. Domain Architect designs modular boundaries. Designer and UX Researcher handle interaction quality and usability. Frontend, Backend, Mobile, Data and Integration Engineers implement bounded work. QA validates behavior. Security and Performance Reviewers independently inspect risks. Devil's Advocate seeks disconfirming evidence. Team Secretary records observable messages, ballots and decisions without voting by default. Governance Auditor independently audits finished changes, read-only. Knowledge Steward prepares linked knowledge entries for a human curator to approve.

## Select teams deliberately
Start with 3–5 focused teammates for substantial tasks. Do not spawn every role by default. Use one session or a focused subagent for simple/sequential work. Agent Teams consume additional tokens and introduce coordination overhead.

## Standard lifecycle (S0–S10)
Stage details, owning skills, fences and human decisions: [AI SDLC Stage Map](AI_SDLC_STAGE_MAP.md).

0. **Intake** — `/change-intake`: classify, check duplicates/conflicts, owner confirms intent and value, declare the scope contract.
1. **Understand** — `/project-discovery`: evidence-backed readiness record; escalate missing assets, access, permissions, integrations and material trade-offs to the owner.
2. **Explore** — `/platform-discovery` for new platforms or large features; bounded spikes for open questions.
3. **Requirements** — `/requirements-traceability`: cited requirements, checked citations, observable acceptance criteria; owner approves scope.
4. **Solutioning** — `/team-debate` for ambiguous decisions: independent proposals, critique, rebuttal, weighted comparison, explicit ballots, ADR and meeting files.
5. **Backlog** — `/backlog-slicing`: testable vertical slices and a prioritization proposal; owner sets the order.
6. **Readiness gate** — consolidated readiness before build; `/efficient-testing` test plan before implementation.
7. **Build** — `/vertical-slice-delivery`: one thin slice with frozen API/data/UI contracts, explicit file ownership and the intake scope contract.
8. **Review and test** — lowest-cost reliable tests, capture only by approved exception; independent QA/security/UX/performance reviews saved in `reports/`; `/delivery-readiness` before handoff; a human merges. Push to a **draft** pull request first: some runtimes (stop hooks, cloud sessions) require a push before the session ends, and a draft keeps that push from looking ready. Mark it ready only after the reviews, closeout and audit exist.
9. **Close and adapt** — `/closeout-report` for every task; `/governance-audit` for spot checks and incidents; `/process-retro` at milestone ends with owner-approved process changes.
10. **Knowledge** — `/knowledge-curation`: linked, dated, secret-free entries approved by a human curator.

## Collaboration rules
Give each teammate a bounded deliverable, constraints and acceptance criteria. Parallelize only genuinely independent work. Do not allow multiple teammates to own the same file concurrently without an integration plan. Main Agent remains accountable for synthesis and the final decision. Team chat and in-memory task status are not durable records.

## Escalation
Pause only work that depends on unavailable resources or decisions; continue safe, independent, reversible work. Never silently use a fake integration, placeholder asset or degraded implementation to hide a blocker. Production deployment, destructive changes, external communication and paid commitments require authorization.

## Recovery
After interruption, recover from the intake record, PRD, trace matrix, backlog, ADRs, readiness/test plans, closeouts, `knowledge/INDEX.md`, meeting events, ballots, action items, git diff and reports. Verify branch and filesystem state before resuming. Do not assume that runtime team state persists.
