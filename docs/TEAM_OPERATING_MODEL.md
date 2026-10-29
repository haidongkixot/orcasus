# Team Operating Model — v2.2.0

## Roles
The Lead/Orchestrator scopes and coordinates the work. Product Manager and Analyst define outcomes, workflows and acceptance criteria. Domain Architect designs modular boundaries. Designer and UX Researcher handle interaction quality and usability. Frontend, Backend, Mobile, Data and Integration Engineers implement bounded work. QA validates behavior. Security and Performance Reviewers independently inspect risks. Devil's Advocate seeks disconfirming evidence. Team Secretary records observable messages, ballots and decisions without voting by default.

## Select teams deliberately
Start with 3–5 focused teammates for substantial tasks. Do not spawn every role by default. Use one session or a focused subagent for simple/sequential work. Agent Teams consume additional tokens and introduce coordination overhead.

## Standard lifecycle
1. Inspect repository, user goal, current changes and decisions.
2. Run Project Discovery and complete an evidence-backed readiness record.
3. Escalate missing assets, access, permissions, integrations and material trade-offs to the owner.
4. Define scope, acceptance criteria, dependencies and a risk-based test plan.
5. For ambiguous decisions, run independent proposals, peer critique, rebuttal, weighted comparison and explicit ballots.
6. Record significant decisions in an ADR and meeting files.
7. Build one thin vertical slice with frozen API/data/UI contracts and explicit file ownership.
8. Test at the lowest-cost reliable layer; capture artifacts only by approved exception.
9. Run independent QA/security/UX/performance reviews as applicable.
10. Reconcile meeting records, report test evidence, risks and next steps.

## Collaboration rules
Give each teammate a bounded deliverable, constraints and acceptance criteria. Parallelize only genuinely independent work. Do not allow multiple teammates to own the same file concurrently without an integration plan. Main Agent remains accountable for synthesis and the final decision. Team chat and in-memory task status are not durable records.

## Escalation
Pause only work that depends on unavailable resources or decisions; continue safe, independent, reversible work. Never silently use a fake integration, placeholder asset or degraded implementation to hide a blocker. Production deployment, destructive changes, external communication and paid commitments require authorization.

## Recovery
After interruption, recover from PRD, ADRs, readiness/test plans, meeting events, ballots, action items, git diff and reports. Verify branch and filesystem state before resuming. Do not assume that runtime team state persists.
