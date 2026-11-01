---
name: backlog-slicing
description: "S5 backlog: break an approved PRD, epic or scope into small ordered vertical slices that each fit one reviewable change, carry one intent, an observable acceptance criterion and the evidence that will prove it, and pass a testability check; then rank them with an explicit prioritization frame for the owner to decide. Unknowns become spikes or owner questions, never guesses. Use when approved scope is too big for one change, when a roadmap must become a backlog, or when stakeholders argue about order. Do NOT use to build a slice (vertical-slice-delivery) or to write requirements (requirements-traceability)."
---

# Backlog Slicing and Prioritization — S5

## Gate
Implementation receives only slices that passed the testability check. Priority order is an owner decision; the team proposes it with evidence.

## 1. Confirm the goal and done state
Restate the approved goal in one sentence and the observable end state. Cite the PRD, trace matrix and intake record. If the goal fits one reviewable change, say so and hand it to `/vertical-slice-delivery`; do not pad a plan.

## 2. Map layers from the repository
List the layers the goal touches (UI, API, domain, data/migration, integrations, jobs, notifications, configuration, tests, docs) and the likely files/modules. Mark each VERIFIED (seen in the repo) or ASSUMED.

## 3. Cut vertical slices
Each slice: one intent, one observable behavior end to end, leaves the product working (behind a flag if needed). Prefer UI → API → domain → data → tests paths; use horizontal enabling tasks only where a later slice truly depends on them (for example an additive migration).

## 4. Testability check
For every slice record: acceptance criterion (observable outcome + pass/fail threshold), evidence that will prove it, lowest-cost reliable test layer, required fixtures/resources and the readiness status of those resources. Verdicts:
- TESTABLE — criterion observable and resources AVAILABLE.
- NEEDS SPLIT — mixes intents, spans unrelated layers or needs several reviewer specialties.
- BLOCKED — required resource/access is MISSING or UNKNOWN in the readiness matrix.
- UNTESTABLE — no observable criterion; becomes an owner question or a time-boxed spike.
Repeat splitting until every slice is TESTABLE, BLOCKED with a named blocker, or an explicit spike.

## 5. Classify, flag and order
Give each slice a provisional change class from `/change-intake`, known risks and approval flags. Order by dependency so each slice can merge on its own; spikes and owner questions come before the slices they unblock; irreversible steps go where they can be reverted.

## 6. Propose a priority (stays human)
Pick one frame and say why it fits: value/effort, RICE, WSJF/cost of delay, MoSCoW or Kano. List its inputs with confidence; mark guessed inputs as ESTIMATE. Keep must-do items (legal, security, blockers) outside the score. Do not present a score as more precise than its inputs. The owner sets the final order.

## Output
Write `projects/<slug>/BACKLOG.md` from `templates/BACKLOG_TEMPLATE.md`: goal, done state, layer map, ordered slices with criterion/evidence/test layer/testability verdict/class/dependencies, spikes, owner questions (blocking first), prioritization frame and inputs, and the owner's priority decision with date.

## Guardrails
- Produces a plan only; starts no implementation.
- No slice without an observable acceptance criterion.
- Do not hide a BLOCKED slice by mocking its missing resource.
