# Knowledge Index

`knowledge/INDEX.md` is the curated, linked record of durable project knowledge (S10). It is maintained with `/knowledge-curation`; the `knowledge-steward` agent prepares entries and a human curator approves them.

## Row format

| Column | Rule |
|---|---|
| ID | `K-0001`, unique, never reused |
| Type | DECISION, CONSTRAINT, LESSON, ANCHOR, PROCESS or GLOSSARY |
| Title | One fact per entry |
| Status | PROPOSED, APPROVED, SUPERSEDED or RETIRED |
| Sources | At least one: repo-relative link (optionally `#L<line>`), `meeting:<meeting-id>`, commit SHA, PR/ticket link or URL. Separate several with `;` |
| Related | Other entry IDs, separated by `;`, or `—` |
| Superseded by | Successor ID for SUPERSEDED rows, otherwise `—` |
| Proposed by / date | Author and absolute date `YYYY-MM-DD` |
| Curator approval | `<name> YYYY-MM-DD` for APPROVED, SUPERSEDED and RETIRED rows; `—` while PROPOSED |

Links inside the index are relative to this folder, for example `[ADR-0001](../decisions/ADR-0001.md)`.

## Checks
`python3 scripts/check_knowledge_links.py` verifies: required columns, unique IDs, allowed values, absolute dates, curator approval where required, successor IDs that exist, repo-relative links (and `#L<line>` anchors) that resolve, `meeting:` IDs that exist under `meetings/sessions/`, and no secret-like values. It also warns about ADRs in `decisions/` and closeouts in `reports/` that no entry references. A resolving link proves the source exists, not that it says what the entry claims; the curator checks content.

## Never store
Secrets, credentials, tokens, connection strings, personal data, in-flight state (open PRs, running jobs) or copies of content the repository already records.
