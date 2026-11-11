---
name: requirements-traceability
description: "S3 requirements with verified citations. Draft requirements and acceptance criteria where every requirement cites its source (owner message, ticket, document path and line, meeting ID, ADR, research URL), then verify each citation by opening the source and recording VERIFIED, PARAPHRASE-OK, MISMATCH, UNVERIFIABLE or NO SOURCE. Trace each requirement forward to acceptance criteria, test layer and evidence. Use when writing or reviewing a PRD, user stories or acceptance criteria, or when a requirement's origin is unclear. Do NOT use to elicit needs from scratch (platform-discovery) or to plan test execution (efficient-testing)."
---

# Requirements Traceability — S3

## Gate
A requirement enters approved scope only when its citation was checked against the source, or when the owner explicitly accepted it as an assumption. Uncited requirements are questions, not scope.

## 1. Collect sources first
List the sources available for this scope: owner messages (quote with date), tickets/issues, `docs/agent-ops/INTAKE_RECORD.md`, PRD drafts, ADRs in `decisions/`, meeting records in `meetings/sessions/<id>/`, research links and existing code behavior (path:line). Record inaccessible sources as UNVERIFIABLE; never paraphrase from memory.

## 2. Draft requirements with citations
For each requirement record: ID, the requirement as written, priority, source citation and source type. Use repo-relative links with line anchors where possible (`docs/PRD.md#L42`), `meeting:<meeting-id>` for meetings and full URLs for external sources. One requirement per row; split compound requirements.

## 3. Verify every citation
Open each cited source and compare it with the requirement:
- VERIFIED — the source states this requirement.
- PARAPHRASE-OK — wording differs; meaning checked and equivalent.
- MISMATCH — the source says something different or narrower; quote the difference.
- UNVERIFIABLE — the source is missing or inaccessible; say why.
- NO SOURCE — nobody asked for it; it is an assumption or suggestion.

Record who checked and when. Do not upgrade a status without opening the source again.

## 4. Resolve gaps with the owner (stays human)
MISMATCH, UNVERIFIABLE and NO SOURCE rows go to the owner as grouped, concise questions with a recommendation. The owner accepts, corrects or removes each one. Never silently keep an uncited requirement or quietly narrow a cited one.

Only the owner may set ASSUMPTION-ACCEPTED. Record it in the row as `accepted by owner: <name> YYYY-MM-DD` and copy the owner's words into the Owner questions table. An agent, the lead or a reviewer never accepts an assumption, even a sound security default; until the owner answers, the row stays PROPOSED and blocks merge. `check_knowledge_links.py` fails a row whose acceptance is missing or names an agent.

## 5. Trace forward
Link each approved requirement to observable acceptance criteria (observable outcome, pass/fail threshold, evidence that will prove it), the lowest-cost reliable test layer from `/efficient-testing`, and the evidence path once tests run. Flag criteria that cannot be observed as UNTESTABLE and rewrite them with the owner.

## Output
Write `docs/agent-ops/TRACE_MATRIX.md` (or `projects/<slug>/TRACE_MATRIX.md`) from `templates/TRACE_MATRIX_TEMPLATE.md`. Run `python3 scripts/check_knowledge_links.py` to confirm repo-relative citations resolve and statuses use the allowed vocabulary; a resolving link does not prove the content matches — step 3 does.

## Guardrails
- Do not invent sources, quotes, users, metrics or line numbers.
- A citation to chat history alone is weak: copy the quote with its date into the trace record.
- Scope and acceptance approval stay with the owner; this skill prepares the decision.
