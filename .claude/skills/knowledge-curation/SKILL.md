---
name: knowledge-curation
description: "S10 knowledge: link durable project knowledge (decisions, constraints, lessons, completion anchors, approved process changes) into knowledge/INDEX.md with tracked source links, provenance and dates, and govern agent memory (CLAUDE.md notes, auto-memory, project-state notes) so only verified, dated, secret-free facts are kept. Entries stay PROPOSED until a human curator approves them; superseded entries point to their replacement. Use after a closeout, retro or ADR, when memory may be stale, or for a periodic knowledge-hygiene sweep. Do NOT use for live source conflicts during a task or as a substitute for an ADR."
---

# Knowledge Curation and Memory Governance — S10

## Gate
The agent prepares and verifies; a human curator approves. An entry becomes APPROVED only with the curator's name and date in the index. Memory edits outside `knowledge/` (CLAUDE.md, auto-memory files, agent instructions) need explicit owner approval for each change.

## 1. Collect candidates
Read proposals from closeouts, retros, governance audits, ADRs and meeting decision summaries. Candidate types: DECISION, CONSTRAINT, LESSON, ANCHOR (completed work pinned to merged evidence), PROCESS (approved process change), GLOSSARY.

## 2. Write rules (what may be kept)
- Confirmed, durable facts only; not in-flight state ("PR 12 is open" expires).
- One fact per entry, with absolute dates (YYYY-MM-DD), never "last week".
- Provenance: who proposed it, from which evidence.
- Store pointers, not copies: link the ADR, report or file instead of restating it.
- Never secrets, credentials, tokens, connection strings or personal data.

## 3. Link sources (tracked source links)
Every entry cites at least one source: repo-relative link (optionally with `#L<line>`), `meeting:<meeting-id>`, commit SHA, PR link or external URL. Link related entries both ways where useful (an ADR entry to the lessons it produced). Run `python3 scripts/check_knowledge_links.py`; fix broken links and add missing fields before asking for approval.

## 4. Trust rules (how memory is used)
Memory is a lead, not truth. Before acting on an entry that names a file, branch, PR, command or state, verify it against the live repository. When live state disagrees, live state wins; propose a correction to the entry instead of changing reality to match memory.

## 5. Hygiene sweep
Classify existing entries: CURRENT, STALE, WRONG-WHEN-WRITTEN, DUPLICATE, FORBIDDEN-CONTENT or UNVERIFIABLE, each with the check that justified it. Propose a disposition per entry: keep, correct (new text), merge into, supersede (with successor ID) or retire (with reason). Flag FORBIDDEN-CONTENT as urgent and recommend rotating any exposed secret; deleting an entry does not un-leak it.

## 6. Curator approval (stays human)
Present additions and dispositions as one table. Apply only approved items: set status, curator name and date; for SUPERSEDED entries fill "superseded by". Re-run the link checker after applying.

## Output
Updated `knowledge/INDEX.md` (format in `knowledge/README.md`), a hygiene report in `reports/<date>-knowledge-curation.md` when a sweep ran, and the approval record in the index rows.

## Guardrails
- Never approve your own entries; the curator is a human.
- Unindexed ADRs and closeouts are reported by the checker as warnings; index or explicitly exclude them.
- Retire by marking first; delete files only with owner approval.
