---
name: process-retro
description: "S9 adapt step: run an evidence-based retrospective over recent closeouts, governance audits, meeting coverage reports, test failures and owner feedback; summarize what worked and what failed, find repeated causes, and propose specific changes to CLAUDE.md, agents, skills, templates, hooks or settings as PROPOSED items for owner approval. Use at the end of a milestone, after an incident or failed audit, or on a regular cadence. Do NOT use to audit one change (governance-audit) or to edit the process without owner approval."
---

# Process Retrospective — S9 Adapt

## Gate
The retro proposes; the owner decides. No change to `CLAUDE.md`, `.claude/agents/`, `.claude/skills/`, `.claude/settings.json`, hooks or templates is applied before the owner approves that specific change.

## 1. Define the window and inputs
State the period or milestone. Gather `reports/*-closeout.md`, `reports/*-governance-audit.md`, `reports/*-readiness.md`, meeting `COVERAGE_REPORT.md` files, `meetings/HOOK_ERRORS.log`, CI results, reverted commits and owner feedback in the window. List inputs that were missing.

## 2. Summarize with evidence
For each item record what happened, its evidence path and its effect (time, quality, cost, risk). Separate facts from opinions; label opinions with their author.

## 3. Find repeated causes
Group findings by cause: missing rule (policy gap), rule bypassed (discipline gap), tooling failure, unclear instruction, missing resource, estimate error. Count occurrences; one-off events do not justify new rules unless the impact was severe.

## 4. Propose changes
For each repeated cause propose the smallest change that would prevent it: the exact file, the rule or check to add, change or remove, the expected effect, how to measure it at the next retro, and the cost (more gates slow work; over-gating gets bypassed). Prefer removing a rule that did nothing over adding a new one.

## 5. Owner decision and follow-through (stays human)
Present proposals as PROPOSED. Record each owner decision as APPROVED, REJECTED or DEFERRED with date. Approved process changes become their own change through `/change-intake` (class agent-system-config), with an ADR in `decisions/` when material. Hand durable lessons to `/knowledge-curation`.

## Output
Write `reports/<period>-retro.md` from `templates/RETRO_TEMPLATE.md`.

## Guardrails
- Blameless: describe actions and systems, not personal fault.
- Do not claim a process change worked until the next retro measured it.
- Never weaken a human approval point, the discovery gate or the zero-capture default without an explicit owner decision recorded in an ADR.
