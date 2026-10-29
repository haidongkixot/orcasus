---
name: change-intake
description: "S0 intake gate for every incoming request before discovery or design. Classify the change type and risk class, check it against existing records for duplicates or conflicts, confirm intent and value with the owner, and declare the scope contract and the gates the class requires. Mid-task scope growth forces reclassification. Use when a new feature, bug, redesign, integration or change request arrives, when a task mixes change types, or when work drifts beyond what was asked. Do NOT use for conceptual questions, for discovery itself (project-discovery) or for slicing an approved scope into tasks (backlog-slicing)."
---

# Change Intake — S0 Gate

## Gate
No discovery, debate or implementation starts until the request has an intake record: a change class, a duplicate/conflict verdict, an owner-confirmed intent and value statement, and a scope contract. Reuse a current intake record instead of creating a second one.

## 1. Restate the request
Quote the request verbatim, then split it into concrete deliverables. Do not add deliverables the owner did not ask for; record extra ideas as SUGGESTIONS, never as scope.

## 2. Classify each deliverable
Inspect the files and layers each deliverable would touch before classifying; never classify from wording alone.

| Class | Minimum validation | Required reviewers | Owner approval before work? |
|---|---|---|---|
| docs-only | link check + review | — | no |
| ui-style | component/accessibility assertions; visual check only by approved question | design | no |
| frontend-logic | unit/component tests + build | QA | no |
| backend-api | unit + API/integration tests | QA | no |
| data-schema-migration | migration plan, rollback, data-loss statement, migration test | data, security | **yes** |
| auth-permission-security | negative/authorization tests + security review | security | **yes** |
| integration | contract tests + failure-path tests; real account/scope verified | integration, security | yes when credentials, scopes or paid usage change |
| mobile-platform | device/emulator tests on supported targets | mobile, QA | no |
| infra-deploy-release | plan/diff reviewed, rollback, delivery-readiness | security, performance | **yes** |
| agent-system-config | evals + validator pass (CLAUDE.md, agents, skills, hooks, settings) | governance-auditor | **yes** when permissions, hooks or tool grants change |
| test-only | test run proving intent | QA | no |
| refactor | behavior-preservation proof (same tests pass before/after) | QA | yes when broad/multi-module |
| bug-fix | failing case reproduced, then passing | QA | no |

The highest-risk class present governs the approval path. Each deliverable still keeps its own validation floor.

## 3. Check for duplicates and conflicts
Search existing records before accepting the request: `knowledge/INDEX.md`, `projects/*/BACKLOG.md`, `projects/*/PRD.md`, `decisions/`, `meetings/sessions/`, `reports/`, `docs/agent-ops/`, open branches and, when accessible, open issues/PRs. Verdict per deliverable:
- NEW — no matching record.
- DUPLICATE — already done or in progress; cite the record and stop that deliverable.
- EXTENDS — builds on a record; cite it and inherit its decisions.
- CONFLICTS — contradicts an ADR, approved scope or another request; cite both and ask the owner.
- UNKNOWN — records were not searchable; say which.

## 4. Confirm intent and value with the owner (stays human)
Draft, do not decide: problem, who is affected, expected value, success signal, urgency and non-goals. Ask the owner to confirm or correct it in one concise question. Never invent a value statement, metric or deadline. Without confirmation the record stays INTAKE PENDING.

## 5. Declare the scope contract and route
Record expected files/modules, classes, validation floors, reviewers, approval path and next gate:
- every non-trivial class → `/project-discovery`;
- competing viable options → `/team-debate`;
- multi-slice or multi-PR scope → `/backlog-slicing`;
- requirements to be written → `/requirements-traceability`.

## 6. Scope lock
During work, any file, layer or behavior outside the contract stops the affected work and returns here for reclassification. A previous approval does not transfer to a new class.

## Output
Write `docs/agent-ops/INTAKE_RECORD.md` from `templates/INTAKE_RECORD_TEMPLATE.md`: request quote, deliverables, classes, governing class, duplicate/conflict verdicts with citations, intent/value statement and owner confirmation, scope contract, validation floors, reviewers, approval path, next gate and open questions.

## Guardrails
- Guard inventiveness: no unrequested features, metrics, personas or deadlines in scope.
- UNKNOWN is not NEW: an unsearched record source is reported, not assumed empty.
- Never downgrade a class to avoid an approval or a review.
