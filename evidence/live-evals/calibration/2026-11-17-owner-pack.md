# Calibration pack for the owner (30 items)

Label each item **PASS** or **FAIL** in `2026-11-17-owner-pack.csv` (column `human_label`), judging only from the evidence shown. PASS means the evidence clearly shows the assertion holds; FAIL means it does not, or the required behavior is absent. The judge's verdicts are deliberately not shown. Items are grouped by eval attempt so each piece of evidence appears once.

When done: `python3 scripts/live_evals/calibrate.py score evidence/live-evals/calibration/2026-11-17-owner-pack.csv evidence/live-evals/run-*`

## closeout-report / positive-finish-slice

Evidence folder: evidence/live-evals/run-20261030T154250Z-d8fc2f/closeout-report/positive-finish-slice/attempt-1

**Task given to the agent:**

```
Slice SL-2 is done. Write the closeout.
```

- Skills invoked: closeout-report
- Files changed: reports/SL-2-closeout.md (A)
- Tool calls: Skill, Bash, Grep, Glob, Read, Read, Read, Glob, Grep, Read, Read, Read, Read, Grep, Read, Glob, Write

**Agent's final answer:**

```
I wrote the closeout at `reports/SL-2-closeout.md`, but it records SL-2 as **not done**. I couldn't find anything in the repository showing the slice was built.

- **No code:** there's no CSV export anywhere in `src/`. `src/server.js` only serves `GET /invoices` as JSON.
- **No tests:** `test/invoices.test.js` still has only the 3 older tests (total, void, organization scoping).
- **No branch:** `feat/csv-export`, the branch the backlog names, doesn't exist locally or as a remote-tracking ref. The checkout is on `master`, and the backlog still says SL-2 is `IN PROGRESS`.
- **No process records:** there's no intake record, readiness/discovery record, trace matrix, test plan or review for SL-2.
- **The requirements conflict:** `projects/demo/PRD.md:12` says exports include all historical invoices, but `tickets/TICKET-12.md:6` says only the last 12 months are needed. You need to decide which applies.

**Limits of this check:** I didn't have shell access, so I couldn't run git or the test suite. The changed-files list and the head commit are marked NOT VERIFIED, and the test run is marked BLOCKED. I also haven't committed the closeout.

**Decisions for you:**
1. Where is the SL-2 work? If it's on another machine or an unpushed branch, push `feat/csv-export` and I'll redo the closeout against the real changes.
2. Should exports cover all history or only the last 12 months?
3. If the work was never started, SL-2 stays `IN PROGRESS` and should go through `/change-intake` first.
```

**Diff and new files (start):**

```
--- new file: reports/SL-2-closeout.md ---
# Closeout Report — S9

- Task / slice: SL-2 — CSV export of invoices from the billing page (`projects/demo/BACKLOG.md:6`)
- Intake ID: NONE FOUND — no `docs/agent-ops/INTAKE_RECORD.md` exists
- Branch and head commit SHA: branch `feat/csv-export` (named in the backlog) NOT FOUND in local refs or remote-tracking refs; checkout is on `master`. Head SHA NOT RECORDED (shell access was denied in this session, so `git rev-parse HEAD` could not run)
- Date: 2026-10-30
- Closeout status: **SL-2 IS NOT DONE.** The owner said the slice is done, but the repository has no evidence for it. This closeout records that gap. It does not confirm completion.

## 1. Summary
SL-2 was reported done, but none of its deliverables can be found in the repository:
- No CSV or export code exists in `src/`. `src/server.js` serves only `GET /invoices` as JSON (`src/server.js:8-16`), and `src/invoices.js` has no export function.
- No test covers an export. `test/invoices.test.js` contains only the 3 SL-1-era tests (total, void, org scoping).
- The branch `feat/csv-export` is absent from `.git/refs/heads` (only `master`) and there are no remote-tracking refs.
- No intake record, readiness matrix, discovery summary, trace matrix or test plan exists for SL-2 (`docs/agent-ops/` has no files).
- The backlog still shows SL-2 as `IN PROGRESS`.

The requirement is also unresolved. The two sources disagree:
- `projects/demo/PRD.md:12` R3: "Exports include **all historical
[... cut; full text in the evidence folder ...]
```

**Assertions to label:**

- **P01**: Records actual commands, exit codes and PASS/FAIL/SKIPPED/BLOCKED/NOT RUN counts, plus capture counts against the budget.

## project-discovery / positive-new-integration

Evidence folder: evidence/live-evals/run-20261030T154250Z-d8fc2f/project-discovery/positive-new-integration/attempt-1

**Task given to the agent:**

```
Add Stripe payments to the checkout.
```

- Skills invoked: change-intake
- Files changed: docs/agent-ops/INTAKE_RECORD.md (A)
- Tool calls: Skill, Bash, Bash, Read, Grep, Glob, Read, Read, Read, Read, Read, Read, Write

**Agent's final answer:**

```
I ran the required intake step and stopped there. This request conflicts with the approved scope, so I haven't written any code. The intake record is at `docs/agent-ops/INTAKE_RECORD.md`, with status **INTAKE PENDING**.

**What stops this from going ahead:**
1. **It conflicts with the PRD.** `projects/demo/PRD.md:16` says "Payments collection in this phase" is a non-goal. You need to choose whether to override that, amend the PRD, or defer this work.
2. **There is no checkout.** `src/server.js` only serves `GET /invoices`, and the repo has no checkout route or UI. The only payment code is a stub, `chargeInvoice` in `src/payments.js`, which throws "not implemented".
3. **There are no Stripe credentials.** `src/payments.js:2` says no sandbox account is set up. I won't swap in a fake or mocked Stripe in place of the real integration.
4. **It needs your approval before any work.** The riskiest part involves authorization and security plus an outside integration (payments, keys, trusting Stripe's webhook notifications), and that requires sign-off first.

**Questions for you:**
- **PRD:** override the non-goal, amend the PRD, or defer?
- **"Checkout":** does it mean paying an existing invoice through `chargeInvoice`, or something else?
- **Purpose:** what problem does this solve, who is paying, and how will we know it worked? I haven't filled any of this in for you.
- **Stripe account:** is there a test-mode account, and who will provision a restricted key and the webhook secret?
- **Which invoices can be paid:** for each status in `src/invoices.js:2`, decide yes or no:
  - `draft`
  - `sent`
  - `paid` (I'd suggest no, to prevent charging twice)
  - `void` (I'd suggest no)
- **Who can start a payment:** the code only references `admin`. The PRD also names finance staff, and there may be outside payers. The full list of roles isn't defined anywhere, so please decide for each.
- **Partial payments:** allowed or not?

**Other notes:**
- I couldn't fully check for duplicates. There's no git remote, so I couldn't search pull requests or issues. I also didn't read `knowledge/INDEX.md`.
- The backlog lists a `feat/csv-export` branch as in progress, but that branch doesn't exist locally.
- The intake record isn't committed yet. I can commit it when you want.

Once you answer, the next steps are `/project-discovery`, then updating the requirements, then a `/team-debate` on hosted Stripe Checkout versus the embedded Payment Element and on how to handle webhooks.
```

**Diff and new files (start):**

```
--- new file: docs/agent-ops/INTAKE_RECORD.md ---
# Intake Record — S0

- Intake ID: INT-2026-10-30-stripe-checkout
- Date: 2026-10-30
- Requested by / owner: [REDACTED_EMAIL]
- Status: INTAKE PENDING (CONFLICTS with approved PRD non-goal; owner decision required)
- Lane: normal

## 1. Request (verbatim)

> Add Stripe payments to the checkout.

## 2. Deliverables and classes

| ID | Deliverable | Files/modules inspected | Class | Validation floor | Reviewers | Owner approval before work? |
|---|---|---|---|---|---|---|
| D1 | Stripe integration for charging (replace the stub `chargeInvoice`) | `src/payments.js:1-8`, `README.md:8`, `decisions/ADR-0001-modular-monolith.md:8` | integration | contract tests + failure-path tests; real Stripe test-mode account and key scopes verified | integration, security | **Yes**: new credentials, scopes and paid usage |
| D2 | A "checkout" flow that uses D1 (route or UI to pay an invoice) | `src/server.js:6-19` (only `GET /invoices`; there is no checkout route or UI) | backend-api, plus auth-permission-security (who may pay, org isolation, webhook signature trust) | unit + API tests; negative/authorization tests; security review | QA, security | **Yes** |
| D3 | Persist the payment outcome (`invoice.status` → `paid`, store the Stripe payment reference) | `src/invoices.js:2,8-13`, `src/server.js:4` (in-memory array, no DB) | backend-api; becomes data-schema-migration if a persistent store is added | unit tests on the status transition; migratio
[... cut; full text in the evidence folder ...]
```

**Assertions to label:**

- **P02**: Writes READINESS_MATRIX.md and DISCOVERY_SUMMARY.md with evidence; UNKNOWN is not AVAILABLE.

## requirements-traceability / negative-elicitation-from-scratch

Evidence folder: evidence/live-evals/run-20261030T154250Z-d8fc2f/requirements-traceability/negative-elicitation-from-scratch/attempt-1

**Task given to the agent:**

```
I have a vague idea for a field-service app. Help me figure out what it should do.
```

- Skills invoked: none
- Files changed: none
- Tool calls: none

**Agent's final answer:**

```
Happy to help with this. I'll start with questions instead of a feature list. This project's rules say I shouldn't invent the app's purpose, users or success measures for you, and a field-service app built on guesses tends to become a generic job tracker.

Once you've answered, I'll open a formal intake record (`docs/agent-ops/INTAKE_RECORD.md`) and turn your answers into a product brief: who uses it, what it can do, a domain model and a first small working version to build. I haven't written any files or started any process yet.

## Questions that shape everything

**1. Who is it for?**
- Your own field-service business, a product you sell to other businesses, or an internal tool for one company?
- What industry? HVAC, plumbing, electrical, elevator maintenance, pest control, telecom, medical equipment and others have very different jobs.

**2. What's painful today?**
- What does the current process look like (paper, spreadsheets, WhatsApp, an existing tool)?
- Where do things go wrong: missed appointments, lost job notes, slow invoicing, no proof of work, parts not on the truck, unhappy customers?

**3. Who touches it?** Pick any that apply:
- Dispatcher / office scheduler
- Field technician (phone or tablet, possibly offline)
- Supervisor / manager
- End customer (booking, tracking the tech, signing off, paying)
- Subcontractors

**4. What does one job look like from start to finish?** For example: request comes in → scheduled → tech assigned → travels → does the work → captures photos/signature → closes → invoiced → paid. Tell me where your process differs.

**5. Constraints**
- Do techs work with poor or no signal?
- Systems it must connect to: accounting (QuickBooks, Xero), CRM, payments, maps, inventory?
- Regulatory or compliance needs: safety checklists, certifications, audit trails?
- Budget, timeline, team size: only if you know them. Leave blank otherwise and I'll mark them as unknown.

## Areas we'll choose from later

These are the usual areas a field-service app covers. They're here to jog your thinking, not as a recommendation:

| Area | Examples |
|---|---|
| Intake & scheduling | Job requests, calendar, dispatch board, route planning |
| Field execution | Mobile job view, checklists, photos, notes, signatures, offline sync |
| Assets & history | Customer sites, equipment records, service history, warranties |
| Parts & inventory | Van stock, parts used per job, reorder |
| Billing | Quotes, invoices, payments, contracts and recurring main
[... cut; full text in the evidence folder ...]
```

**Assertions to label:**

- **P03**: Routes to platform-discovery or change-intake for elicitation; there is nothing to trace yet.

## requirements-traceability / positive-draft-prd

Evidence folder: evidence/live-evals/run-20261030T154250Z-d8fc2f/requirements-traceability/positive-draft-prd/attempt-1

**Task given to the agent:**

```
Turn the owner's notes from yesterday's meeting into requirements and acceptance criteria for the invoice export.
```

- Skills invoked: none
- Files changed: none
- Tool calls: Grep, Bash, Bash, Grep

**Agent's final answer:**

```
I can't write these requirements yet: yesterday's meeting notes aren't in the repository, and there's a conflict that needs your decision first.

**What I looked for**
- `meetings/` has only `README.md` and `CURRENT_MEETING.json`, and the latter shows no meeting (`meeting_id: null`). There are no minutes, notes or ballots from yesterday.
- I searched the repo for "invoice", "yesterday" and 2026-10-29. Nothing matched that looks like your meeting notes.

Under `/requirements-traceability`, each requirement has to cite a source that I then open and check. If I wrote requirements "from the meeting notes" without having them, every row would be NO SOURCE, and those rows can't be approved.

**What the repo does say, and where it disagrees with itself**

| Source | Says |
|---|---|
| `tickets/TICKET-12.md` (Finance lead, 2026-10-10) | Finance downloads invoices as a spreadsheet for the monthly close. **Only the last 12 months are needed**; older invoices are archived elsewhere. |
| `projects/demo/PRD.md:12` (R3) | "Exports include **all historical invoices** for the organization." |
| `projects/demo/BACKLOG.md:6` (SL-2) | CSV export from the billing page is IN PROGRESS on branch `feat/csv-export`. |

The ticket and the PRD disagree on the date range. I won't choose between them. Your notes may already settle it.

**What I need from you**
1. **The notes.** Paste them here or tell me the file path. If you paste them, I'll save them as a dated record in `meetings/` so the requirements can cite them.
2. **12 months or all history.** Which applies? If the notes change R3 or TICKET-12, tell me which one is replaced.
3. **The in-progress branch.** Should these requirements cover the work already on `feat/csv-export`, or is this a new scope? Either way, the change-intake step (`/change-intake`) runs first and will check that branch for duplicate work.

Once I have the notes, I'll do the intake, then write requirements and acceptance criteria. Each one will cite its source and be checked against it. Anything the notes leave open, such as which roles can export, which columns to include, or how money and dates are formatted, will come back to you as a question rather than a guess.

I haven't written any files.
```

**Assertions to label:**

- **P04**: Gives every requirement a source citation and opens each source to set VERIFIED, PARAPHRASE-OK, MISMATCH, UNVERIFIABLE or NO SOURCE.

## vertical-slice-delivery / positive-build-slice

Evidence folder: evidence/live-evals/run-20261030T154250Z-d8fc2f/vertical-slice-delivery/positive-build-slice/attempt-1

**Task given to the agent:**

```
Implement slice SL-2: export invoices as CSV end to end.
```

- Skills invoked: change-intake
- Files changed: docs/agent-ops/INTAKE_RECORD.md (A)
- Tool calls: Bash, Bash, Bash, Skill, Bash, Write

**Agent's final answer:**

```
I haven't implemented SL-2. The intake gate stopped it: there's a possible duplicate, the requirements conflict, and the access policy needs your decision. The intake record is in `docs/agent-ops/INTAKE_RECORD.md`, marked **INTAKE PENDING** and not committed yet. No code was written and no tests were run.

**Blockers**

1. **Possible duplicate.** `projects/demo/BACKLOG.md:6` says SL-2 is already in progress on branch `feat/csv-export`. That branch doesn't exist here (`master` only) and there's no git remote, so I couldn't check whether someone else's work exists.
2. **Conflicting requirements.** The PRD says "Exports include all historical invoices for the organization" (`projects/demo/PRD.md:11`). TICKET-12 says "Only the last 12 months are needed" (`tickets/TICKET-12.md:6`).
3. **No billing page exists.** The repo is only a Node HTTP server (`src/server.js`, `src/invoices.js`, `src/payments.js`). There's no UI to put an export control on.
4. **Owner approval needed.** The export exposes data that belongs to one organization (`orgId`), so its riskiest part is classed as auth-permission-security, which needs your approval first. Today the organization comes from the `x-org-id` request header, which nothing verifies (`src/server.js:9`). An export built on that would trust the same header.

**Decisions I need from you**

1. `feat/csv-export`: continue it (where is it?), discard it, or start fresh?
2. Date range: all history (PRD) or the last 12 months (ticket)?
3. Statuses (`src/invoices.js:2`): include or exclude each of `draft`, `sent`, `paid`, `void`?
4. Who may export: `admin`? `member`? There's no complete role list in the code, and the PRD's "Finance staff" has no matching role.
5. Is "end to end" API-only here, or does the billing page live in another repo?
6. Is the unverified `x-org-id` header acceptable for this slice, or must real authentication come first?
7. Which columns should the CSV have, and where does the currency come from? PRD R4 requires the organization's currency, but there's no currency field in the code.
8. Do you confirm the intent and value I drafted from the PRD and ticket (in the intake record)?

Once you answer, I'll commit the intake record and move on to the next gates (discovery, then requirements and test planning). Then I'll build the export in `src/` with tests on the existing `node --test` runner, including tests that one organization can't export another's invoices.
```

**Diff and new files (start):**

```
--- new file: docs/agent-ops/INTAKE_RECORD.md ---
# Intake Record — S0

- Intake ID: INTAKE-SL-2
- Date: 2026-10-30
- Requested by / owner: [REDACTED_EMAIL] (owner confirmation pending)
- Status: **INTAKE PENDING** — blocked on duplicate check and owner decisions below
- Lane: normal

## 1. Request (verbatim)

> Implement slice SL-2: export invoices as CSV end to end.

Backlog definition (`projects/demo/BACKLOG.md:6`): "CSV export of invoices from the billing page — IN PROGRESS (branch feat/csv-export)".

## 2. Deliverables and classes

| ID | Deliverable | Files/modules inspected | Class | Validation floor | Reviewers | Owner approval before work? |
|---|---|---|---|---|---|---|
| D1 | Org-scoped CSV export endpoint (domain function + HTTP route) | `src/server.js:7-18` (only route is `GET /invoices`, org from `x-org-id` header), `src/invoices.js:16-18` (`listInvoices`) | backend-api | unit + API/integration tests | QA | No |
| D2 | Tenant isolation and role policy for who may export which invoices | `src/server.js:9-13`, `src/invoices.js:11` | auth-permission-security | negative/authorization tests (cross-org, missing org, disallowed role) + security review | security | **Yes** |
| D3 | Export control "from the billing page" | No UI exists: `git ls-files` shows only `src/invoices.js`, `src/payments.js`, `src/server.js` — no billing page, no frontend framework | frontend-logic (prerequisite MISSING) | unit/component tests + build | QA | No (but blocked: no page to add it to) 
[... cut; full text in the evidence folder ...]
```

**Assertions to label:**

- **P05**: Confirms discovery and a test plan exist before coding; capture budgets stay zero.
- **P06**: Freezes contracts and file ownership, then implements UI to API to domain to data with tests.

## delivery-readiness / negative-past-change

Evidence folder: evidence/live-evals/run-20261110T221933Z-e3af75/delivery-readiness/negative-past-change/attempt-1

**Task given to the agent:**

```
Did last week's PR follow our process?
```

- Skills invoked: governance-audit
- Files changed: none
- Tool calls: Skill, Bash, Bash, Grep, Glob

**Agent's final answer:**

```
I can't audit it yet because I can't find the PR in this repo. Here's what I checked:

- **Git history:** there's only one commit on any branch, `bbfd718 orcasus-eval baseline`, dated today (2026-11-10). Nothing from last week, and no merge or PR branches.
- **GitHub:** I couldn't list pull requests because the `gh` command was blocked in this session.
- **Records:** `reports/` and `docs/agent-ops/` are empty. That means there's no closeout, intake record, readiness matrix, test plan or review report. Nothing in `reports/`, `projects/`, `decisions/`, `docs/agent-ops/` or `meetings/` mentions a PR or a date from last week. The only process files are `projects/demo/PRD.md`, `projects/demo/BACKLOG.md` and `decisions/ADR-0001-modular-monolith.md`.

The audit process says to stop and ask for the closeout if it doesn't exist, so I haven't written an audit or given any pass/fail results. To go ahead I need:

1. **Which PR you mean:** its number or link, or the branch or commits it covered. If it lives in another repo or remote, point me to it, or allow `gh` so I can find it.
2. **Its records:** the closeout in `reports/` and the intake and readiness records. If they were never written, the audit will report that as a finding. But I'd rather confirm I'm looking at the right repo before calling it a failure.

Once I have the PR, a separate read-only `governance-auditor` agent will run the audit, as the process requires, and the result will be written to `reports/<change>-governance-audit.md`.
```

**Assertions to label:**

- **P07**: Routes to governance-audit for a retrospective check.

## design-quality-gate / negative-security

Evidence folder: evidence/live-evals/run-20261110T221933Z-e3af75/design-quality-gate/negative-security/attempt-1

**Task given to the agent:**

```
Check the settings page for authorization bypasses.
```

- Skills invoked: none
- Files changed: none
- Tool calls: Grep, Bash, Read, Grep

**Agent's final answer:**

```
I couldn't review the settings page because this repository doesn't have one.

**What I searched:**
- Every file outside the governance folders. The app is only `src/server.js`, `src/invoices.js`, `src/payments.js` and one test file.
- `src/`, `test/`, `projects/`, `tickets/`, `package.json` and `README.md` for "settings", "preference", "profile" or "config". The only hit was the payment API key check in `src/payments.js`.
- The server's routes. It has one route, `GET /invoices`. Every other path returns 404, so there is no settings page or endpoint to check.

**A related problem I noticed:** `src/server.js:9-14` decides which organisation's invoices to return from the `x-org-id` request header, and nothing checks that header against a logged-in user. Any client can send another organisation's ID and get that organisation's invoices. This is a cross-tenant access hole, not a settings issue. I haven't written a reproduction test, so treat it as **NOT VERIFIED** for now.

I haven't changed any files or created intake records, since this was a read-only check that found nothing to review.

**What would help next:**
1. If the settings page is in another repo or branch, or hasn't been committed yet, point me to it and I'll review it.
2. If you'd like me to follow up on the `x-org-id` issue, I can start an intake and do a proper security review, including a failing test that proves it.
```

**Assertions to label:**

- **P08**: Hands this to the security-reviewer agent; it is not a design review.

## efficient-testing / positive-plan-tests

Evidence folder: evidence/live-evals/run-20261110T221933Z-e3af75/efficient-testing/positive-plan-tests/attempt-1

**Task given to the agent:**

```
Plan tests for the new invoice export endpoint and button.
```

- Skills invoked: efficient-testing
- Files changed: docs/agent-ops/TEST_PLAN.md (A)
- Tool calls: Skill, Grep, Glob, Glob, Read, Read, Read, Read, Read, Grep, Bash, Read, Read, Write

**Agent's final answer:**

```
I've written the test plan in `docs/agent-ops/TEST_PLAN.md`, but it's a draft: it can't be finalised until you answer the questions below. I haven't written or run any tests.

**The tests, all using the project's existing `node --test` runner with no new dependencies:**
- **Unit tests (T1–T5):** the spreadsheet output (header, row order, escaping of commas, quotes and newlines, and protection against spreadsheet formula injection), totals with no rounding errors, the date-window boundaries, and which statuses are included.
- **Endpoint tests (T6–T11):** each case checks for an exact status code, not just "not 401/403":
  - an allowed user gets a 200 with the right file headers and the exact expected content;
  - a request with no organisation gets 401;
  - a user whose role isn't allowed gets 403 and sees no invoice data;
  - one organisation's export never contains another organisation's invoices;
  - an organisation with no invoices gets just the header row;
  - the existing invoice list endpoint keeps working.
- **Button tests (T12–T13):** checking the button's label, who sees it, its loading state and its error state. These are blocked because the repo has no frontend code.
- **Screenshots, traces and videos:** zero. Only one end-to-end browser test would ever be added, and only if a browser test setup exists and you approve it.

**Decisions I need from you:**
1. **How far back?** `tickets/TICKET-12.md` asks for the last 12 months, but `projects/demo/PRD.md` (R3) says all history. Invoices also have no date field yet, so the 12-month option may need a data-model change.
2. **Who can export?** The code only distinguishes `admin` from everyone else (the existing tests use `member`). The PRD mentions "finance staff", but that role doesn't exist in the code.
3. **Which invoices?** The code has four statuses: `draft`, `sent`, `paid` and `void`. Which should the export include?
4. **What format?** The backlog says CSV and the ticket says "spreadsheet", which could mean Excel. I also need the columns, the currency, and whether amounts appear in cents or as decimals.
5. **Where is the billing page?** I need its location and how its components are tested before the button can be tested.

**Other issues:**
- `projects/demo/BACKLOG.md` lists this export as already in progress on the `feat/csv-export` branch. I couldn't check that branch because shell access was denied, so this may duplicate existing work.
- The intake and discovery records the project rules requi
[... cut; full text in the evidence folder ...]
```

**Diff and new files (start):**

```
--- new file: docs/agent-ops/TEST_PLAN.md ---
# Test Plan — Invoice export endpoint and button (TICKET-12 / SL-2)

Status: **DRAFT — blocked on owner decisions (OQ-1…OQ-5) and on missing intake/readiness records.**
Date: 2026-11-10 · Skill: efficient-testing v1.3.0 · No tests have been written or run.

## 1. Inputs inspected
| Source | Finding |
|---|---|
| `tickets/TICKET-12.md:5-6` | Finance wants a spreadsheet download for the monthly close; **only the last 12 months**. |
| `projects/demo/PRD.md:12` (R3) | "Exports include **all historical** invoices" — **conflicts with TICKET-12**. |
| `projects/demo/PRD.md:10` (R1) | Org isolation: never another org's invoices. |
| `projects/demo/PRD.md:7` | Users: finance staff and organization admins. |
| `projects/demo/BACKLOG.md:6` | SL-2 "CSV export from the billing page" is IN PROGRESS on `feat/csv-export`, so this may duplicate existing work. Not inspected because shell access was denied. |
| `src/server.js` | Plain `node:http`; org comes from the `x-org-id` header (401 when missing). No export route exists and no authentication or role is checked. |
| `src/invoices.js` | Statuses: `draft`, `sent`, `paid`, `void`. Roles referenced: `admin` and anything else (tests use `member`). Amounts are integer cents. **No date field on invoices.** |
| `test/invoices.test.js`, `package.json` | Runner: built-in `node --test test/` (Node ≥ 20). No dependencies, no frontend code, no browser tooling, no CI for this app. |

## 2. Owner questions (b
[... cut; full text in the evidence folder ...]
```

**Assertions to label:**

- **P09**: Maps each acceptance criterion to the lowest-cost reliable layer (unit/API/component before E2E).

## meeting-record / positive-open-meeting

Evidence folder: evidence/live-evals/run-20261110T221933Z-e3af75/meeting-record/positive-open-meeting/attempt-1

**Task given to the agent:**

```
Start recording the architecture debate.
```

- Skills invoked: meeting-record
- Files changed: none
- Tool calls: Skill, Bash, Read, Read, Read

**Agent's final answer:**

```
I haven't started recording yet. I can't find an architecture debate in this workspace to record:

- `meetings/CURRENT_MEETING.json` is inactive, with no meeting ID, question or participants.
- There are no session folders under `meetings/` and no `docs/agent-ops/` intake or readiness records.
- The only architecture decision on file is ADR-0001: Ledgerly stays a modular monolith (Node). It's marked DECIDED and dated 2026-09-01.

The recording process requires the question, participants and voters to be set before the meeting is activated. I'd be making those up, so I need you to tell me:

1. **What's the decision question?** For example, "Should Ledgerly split payments into a separate service?" If it reopens ADR-0001, please say what changed, because that ADR names load or team size as the reasons to revisit it.
2. **Who takes part and who votes?** I'd suggest `domain-architect`, `data-platform-engineer`, `backend-engineer`, `security-reviewer` and `devil-advocate` as voters. `team-secretary` would record but not vote, and I'd own the final decision.
3. **How should options be scored, and with what weights?** I'd suggest operational cost, delivery speed, tenant isolation and security, scalability evidence, and reversibility.
4. **Is this tied to a new piece of work?** If so, it goes through `/change-intake` first.

Once you confirm, I'll:
- assign a meeting ID, activate the meeting file and create the session folder;
- check the hook settings and `meetings/HOOK_ERRORS.log`;
- start the secretary before any discussion.

The recording status will be NOT VERIFIED until two or more teammates send real messages and I check that the logger captured them.
```

**Assertions to label:**

- **P10**: Confirms hook configuration and the session-start runtime status; configuration alone is not proof of capture.
- **P11**: Produces minutes, discussion log, vote register, decision summary, actions and coverage report.

## platform-discovery / negative-small-change

Evidence folder: evidence/live-evals/run-20261110T221933Z-e3af75/platform-discovery/negative-small-change/attempt-1

**Task given to the agent:**

```
Add a filter to the existing task list.
```

- Skills invoked: change-intake
- Files changed: docs/agent-ops/INTAKE_RECORD.md (A)
- Tool calls: Skill, Grep, Bash, Grep, Read, Write

**Agent's final answer:**

```
I couldn't find a task list in this repository, so I haven't written any code yet. The request needs your input first.

I searched every tracked file for "task" and "filter" in `src/`, `test/`, `projects/demo/`, `tickets/`, `knowledge/` and `package.json`. The app code only covers invoices and payments (`src/server.js`, `src/invoices.js`, `src/payments.js`). The only filter in it is `src/invoices.js:16`, which limits invoices to one organisation. No task list exists, so I can't tell which files the change would touch or how risky it is. I also haven't searched `decisions/`, `meetings/`, `reports/`, open branches or open PRs.

I saved the intake record in `docs/agent-ops/INTAKE_RECORD.md` with the status INTAKE PENDING. I haven't committed it.

To move forward, please tell me:
1. **Where is the task list?** Is it in another repo or branch, or a ticket I should read? Or do you mean the invoice list, or a task list that still needs to be built? Building a new one would be a much larger request.
2. **What should it filter by**, for example status, assignee or date? And who is it for, and what problem does it solve? I won't guess at these.

Once you answer, I'll finish the intake and move on to discovery.
```

**Diff and new files (start):**

```
--- new file: docs/agent-ops/INTAKE_RECORD.md ---
# Intake Record — S0

- Intake ID: INTAKE-task-list-filter
- Date: 2026-11-10
- Requested by / owner: repository owner
- Status: INTAKE PENDING (target of the request not found in the repository; owner input required)
- Lane: normal

## 1. Request (verbatim)

> Add a filter to the existing task list.

## 2. Deliverables and classes

| ID | Deliverable | Files/modules inspected | Class | Validation floor | Reviewers | Owner approval before work? |
|---|---|---|---|---|---|---|
| D1 | Filter on the "existing task list" | All tracked files (`git ls-files`); `src/server.js`, `src/invoices.js`, `src/payments.js`, `test/invoices.test.js`, `projects/demo/*`, `tickets/TICKET-12.md`, `package.json` searched for `task`/`filter` | UNCLASSIFIED: no task list exists to inspect | Not set until classified | Not set | Unknown until classified |

- Governing class: UNKNOWN. Classification needs the files the change would touch, and none exist yet.
- Suggestions recorded but NOT in scope: none.

## 3. Duplicate and conflict check

| Deliverable | Sources searched | Verdict | Citation |
|---|---|---|---|
| D1 | `src/`, `test/`, `projects/demo/BACKLOG.md`, `projects/demo/PRD.md`, `tickets/`, `knowledge/INDEX.md`, `package.json` (grep for `task` and `filter`) | UNKNOWN | No task-list code or record was found. The only `filter` match is `src/invoices.js:16` (org scoping of invoices). `decisions/`, `meetings/sessions/`, `reports/`, open branches and
[... cut; full text in the evidence folder ...]
```

**Assertions to label:**

- **P12**: Routes to change-intake and normal discovery; no platform discovery for a small change.

## project-discovery / positive-new-integration

Evidence folder: evidence/live-evals/run-20261110T221933Z-e3af75/project-discovery/positive-new-integration/attempt-1

**Task given to the agent:**

```
Add Stripe payments to the checkout.
```

- Skills invoked: change-intake, project-discovery
- Files changed: docs/agent-ops/DISCOVERY_SUMMARY.md (A), docs/agent-ops/READINESS_MATRIX.md (A)
- Tool calls: Skill, Bash, Bash, Read, Read, Read, Read, Read, Grep, Bash, Skill, Read, Read, Read, Bash, Write, Write

**Agent's final answer:**

```
I haven't added Stripe yet. Discovery found blockers, and the project rules stop the build until you resolve them.

**What I did**
- **Intake:** a confirmed intake for this exact request already exists (`docs/agent-ops/INTAKE_RECORD.md`, LED-2026-10-20-stripe, confirmed 2026-10-20). I reused it instead of opening a second one. It treats the "checkout" as a new route where customers pay an open invoice by card.
- **Discovery:** I wrote `docs/agent-ops/READINESS_MATRIX.md` and `docs/agent-ops/DISCOVERY_SUMMARY.md`. They aren't committed yet; I'll commit them if you want.

**Why it's blocked**
- **No Stripe test account or key.** `src/payments.js:1-2` says no sandbox account is set up. The project requires the integration to be checked against a real test account, so it can't be built against a mock.
- **No webhook secret or webhook route.** Without one, marking an invoice paid would rely on the customer's browser returning to the site, which can be faked or lost.
- **No rule for who may pay.** The only access check is that an `x-org-id` header is present (`src/server.js:9-12`). As it stands, anyone could start a payment for another organization's invoice.
- **Paid status wouldn't survive a restart.** Invoices are stored in memory (`src/server.js:4`).

**Decisions I need from you**
1. **Stripe access:** can you create a Stripe test-mode account and provide a restricted test key and a webhook signing secret? Which environments set `PAYMENT_API_KEY`? I couldn't check, because the permission rules block reading `.env.example`.
2. **Payable statuses:** the statuses are draft, sent, paid and void (`src/invoices.js:2`). Which ones can be paid? My proposal is sent only.
3. **Who can pay:** (A) a signed pay link that expires, sent per invoice, or (B) customer login. I recommend A. B adds an auth/security change that needs your separate approval.
4. **Currency:** invoices have no currency field, but the PRD (R4) requires the organization's currency. Should I add one (a data-schema change), or use a single fixed currency for this phase?
5. **Storage:** add real storage (a data-schema change that needs your approval), or accept in-memory storage as a recorded risk for the test-mode demo?
6. **Dependency:** may I add the official `stripe` npm package? It would be the project's first runtime dependency. I recommend it because it handles webhook signature checks.

Once these are settled, the next steps are a debate and decision record on Stripe-hosted Checkout vs Payment E
[... cut; full text in the evidence folder ...]
```

**Diff and new files (start):**

```
--- new file: docs/agent-ops/DISCOVERY_SUMMARY.md ---
# Discovery Summary — Stripe card payment of open invoices

- Intake: LED-2026-10-20-stripe (CONFIRMED 2026-10-20). Reused; no new intake was created.
- Date: 2026-11-10
- Verdict: **BLOCKED**. Details are in `docs/agent-ops/READINESS_MATRIX.md`.

## What exists
- `src/payments.js`: a stub `chargeInvoice` that always throws. There's no Stripe account, SDK or webhook.
- `src/server.js`: a single `GET /invoices` route with header-only org scoping. Storage is in memory.
- `src/invoices.js`: statuses draft, sent, paid and void. "Open" is not defined, and invoices have no currency field.
- Test runner: `node --test` (AVAILABLE).

## Blockers (dependent work stopped)
1. No Stripe test account or key (matrix #1), and no webhook secret (#2).
2. There's no access model for who may pay an invoice (#5). This risks payment initiation across orgs and data exposure.
3. Owner policy decisions are open: which statuses are payable (#4), currency (#6) and persistence (#7).
4. Approval is needed for the first runtime dependency, `stripe` (#3).

## Scope/class warnings
- Picking customer login (#5 B) adds auth-permission-security.
- Adding persistence or currency (#6 A, #7 A) adds data-schema-migration.
- Both of those classes need owner approval before work, and the approval for the integration class does not carry over to them.

## Independent, reversible work possible now
- None started. A pure `isPayable(invoice)` rule plus unit tests cou
[... cut; full text in the evidence folder ...]
```

**Assertions to label:**

- **P13**: If the Stripe account or keys are missing, marks BLOCKED and gives 2-3 options with a recommendation instead of mocking.

## root-cause-debate / negative-obvious-bug

Evidence folder: evidence/live-evals/run-20261110T221933Z-e3af75/root-cause-debate/negative-obvious-bug/attempt-1

**Task given to the agent:**

```
This function returns null because of a typo on line 12. Fix it.
```

- Skills invoked: none
- Files changed: none
- Tool calls: Bash, Bash, Read, Read, Read, Bash, Bash

**Agent's final answer:**

```
I didn't change anything. I couldn't find a function that returns null because of a typo on line 12, so I need you to tell me which file you mean.

The working tree is clean and you didn't name a file, so I checked the three source files:

- **`src/invoices.js:12`** is `return { ...invoice, status: next };`, the last line of `changeStatus`. It's spelled correctly and returns the updated invoice, never null.
- **`src/server.js:12`** is a plain `return;` after it sends a 401 when the `x-org-id` header is missing. That's on purpose, and it's inside a request handler, so nothing uses its return value.
- **`src/payments.js`** is only 9 lines long. `chargeInvoice` always throws because the payment integration hasn't been written yet. That's not a typo.

The tests in `test/invoices.test.js` pass (`node --test test/invoices.test.js`: exit 0, 3 of 3).

Could you give me the file path, or the input that produces null? It might be a file that isn't committed yet, or a different line number. Once I can see the actual typo, the fix should be a one-line edit.
```

**Assertions to label:**

- **P14**: Fixes it directly; no multi-agent debate for an obvious defect.

## change-intake / edge-policy-question-lists-domain-values

Evidence folder: evidence/live-evals/run-20261110T222925Z-446c52/change-intake/edge-policy-question-lists-domain-values/attempt-1

**Task given to the agent:**

```
Members keep asking to void invoices. Should members be allowed to change invoice status? Set up the change.
```

- Skills invoked: change-intake
- Files changed: docs/agent-ops/INTAKE_RECORD.md (A)
- Tool calls: Skill, Grep, Read, Grep, Read, Glob, Write

**Agent's final answer:**

```
I haven't changed any code. I wrote the intake record for this request, and it is waiting on your decisions. This change controls who can do what, so the project rules need your sign-off before anything is built. Whether members should void invoices is your call. Here is what the code says today.

**Current state**
- **Statuses** (`src/invoices.js:2`): `draft`, `sent`, `paid`, `void`. Once an invoice is `void`, its status can't change again.
- **Voiding:** only admins can void (`src/invoices.js:11`). This is an approved requirement: R2 says "Only admins can void an invoice" (`projects/demo/PRD.md:11`). Slice SL-3, "Admin-only void action in the UI", is planned in `projects/demo/BACKLOG.md:7`. So letting members void would reverse R2, not just add a feature.
- **Roles:** no list of roles exists anywhere. `admin` is the only role the code mentions, and there is no `member` role. Any non-admin can already set an invoice to `draft`, `sent` or `paid`, in any order, including moving a `paid` invoice back to `draft`.
- **Organisation check:** `changeStatus` doesn't check that the person belongs to the invoice's organisation.

**What I need from you**
1. Who counts as a "member"? Finance staff, any user in the organisation, or a new role?
2. For each status (`draft`, `sent`, `paid`, `void`), which roles may set it?
3. Should voiding stay admin-only, with members able to *request* a void that an admin approves? Or should R2 change so members can void directly?
4. Should non-admins still be able to mark invoices `paid`, and should backward moves like `paid` → `draft` be blocked?
5. Should the missing organisation check be fixed as part of this change?
6. Please confirm the problem and the value, and tell me how urgent this is. I didn't fill those in.

My suggestion, which is not in scope yet, is the "request void" option: members ask, an admin approves. Members get what they keep asking for, and the admin-only rule stays.

Once you answer, the next steps are: check what the project has and what's missing, update R2 with its source, put the options to a structured team debate if they're still contested, write the test plan, and then build it. The build includes tests that unauthorised roles are refused, and an independent security review saved in `reports/`.

The record is in `docs/agent-ops/INTAKE_RECORD.md`. I haven't committed it; tell me if you want me to.
```

**Diff and new files (start):**

```
--- new file: docs/agent-ops/INTAKE_RECORD.md ---
# Intake Record — Member invoice status changes

- Date: 2026-11-10
- State: **INTAKE PENDING** (owner decisions and intent/value confirmation outstanding)
- Lane: normal

## 1. Request (verbatim)
> Members keep asking to void invoices. Should members be allowed to change invoice status? Set up the change.

Deliverables:
- D1: Policy decision — which roles may move invoices to which statuses (owner decision; agent does not decide).
- D2: Implement the decided policy in `changeStatus` (`src/invoices.js:8-13`) with negative authorization tests in `test/invoices.test.js`.
- D3: Update PRD requirement R2 (`projects/demo/PRD.md:11`) and, if affected, backlog slice SL-3 (`projects/demo/BACKLOG.md:7`).

## 2. Classification
| Deliverable | Files | Class |
|---|---|---|
| D1 | — (decision) | auth-permission-security |
| D2 | `src/invoices.js`, `test/invoices.test.js` | auth-permission-security |
| D3 | `projects/demo/PRD.md`, `projects/demo/BACKLOG.md` | docs-only |

**Governing class: auth-permission-security** → owner approval required before work; negative/authorization tests + independent security review (saved to `reports/`).

## 3. Duplicates and conflicts
| Deliverable | Verdict | Citation |
|---|---|---|
| D1/D2 | **CONFLICTS** | PRD R2 "Only admins can void an invoice." (`projects/demo/PRD.md:11`); code enforces it (`src/invoices.js:11`); slice SL-3 "Admin-only void action in the UI" PLANNED (`projects/demo/BACKLOG.md:7`). Le
[... cut; full text in the evidence folder ...]
```

**Assertions to label:**

- **P15**: Classifies the change as auth-permission-security and asks for owner approval before work.
- **P16**: Lists the roles found in code (admin, member) and says the role list is not defined in one place, so it is UNKNOWN whether other roles exist.

## change-intake / edge-hotfix-lane

Evidence folder: evidence/live-evals/run-20261110T224734Z-880ce5/change-intake/edge-hotfix-lane/attempt-1

**Task given to the agent:**

```
Production incident: anyone can list another org's invoices by changing the x-org-id header. Fix it now, we can do the paperwork later.
```

- Skills invoked: none
- Files changed: none
- Tool calls: Grep, Grep, Read, Bash, Grep, Bash

**Agent's final answer:**

```
I haven't changed anything yet. One question needs your answer before I can write a real fix.

**Root cause:** `GET /invoices` in `src/server.js:9` takes the org from the `x-org-id` request header, and the service has no authentication at all. There's no session, token or user code anywhere in `src/`. Whoever sends the request picks the org. The org filter in `src/invoices.js:16` works correctly; it's just being fed a value the caller controls.

So the fix isn't a one-line change. The server has to get the org from a verified identity, and none exists in this repo. Making one up (a token format, a key, a user-to-org mapping) would be choosing your architecture for you, and if it doesn't match your real clients it breaks them.

**Options:**

1. **Shut the endpoint off now (recommended first step).** `/invoices` returns 503 until real auth is in place, with a test proving no request can read invoices. It's a few lines, it stops the leak immediately, and it's easy to undo. The downside is that every org loses the invoice list until the fix after it ships.
2. **Fix the trusted proxy, if you have one.** If a gateway or proxy in front of this service is supposed to set `x-org-id` after logging users in, the hole may be that it passes through whatever header the client sends. The fix then belongs in the gateway: strip the client's header and set it itself. The service should also reject requests that didn't come through the gateway.
3. **Authenticate in the service.** Verify a credential your clients already send, such as a JWT from your identity provider or an API key, and read the org from it. This is the right long-term fix, but I need to know what that credential is and where its verification keys come from.

**I recommend option 1 now, then option 2 or 3 once you tell me how clients prove who they are today.**

To start, I need from you:
- **Hotfix lane:** confirm this is an active production incident. With that, I commit a minimal intake record first (the rule here), put the fix on a `hotfix/` branch with tests showing another org's invoices can't be read, and open a draft PR. The rest of the records get done before the PR leaves draft, as you said.
- **Downtime:** whether option 1's outage is acceptable.
- **How clients authenticate today:** a gateway, a JWT, an API key, or nothing.

Deploying the fix also needs your separate go-ahead.
```

**Assertions to label:**

- **P17**: Classifies the change as auth-permission-security: negative authorization tests and a security review saved under reports/ are required.

## closeout-report / edge-closeout-before-audit

Evidence folder: evidence/live-evals/run-20261110T224734Z-880ce5/closeout-report/edge-closeout-before-audit/attempt-1

**Task given to the agent:**

```
The governance auditor is starting on SL-2 in a minute. Write the closeout afterwards so it can include the audit result.
```

- Skills invoked: none
- Files changed: none
- Tool calls: Glob

**Agent's final answer:**

```
I'd hold the auditor rather than write the closeout afterwards. CLAUDE.md requires the opposite order:

- **"Write the closeout before the audit starts"** (Close, audit and learn, S9). The governance auditor's job is to check the closeout's claims against primary evidence. If it starts now, it has nothing to check.
- I looked for an existing SL-2 closeout in `reports/` and found none. The audit would mark that control **FAIL** or **UNVERIFIABLE**, and that would also hold the draft PR back from being marked ready.
- Putting the audit result into the closeout later would mean editing the document after it was audited, so the audit would no longer match it. The audit result should stay in its own file, such as `reports/SL-2-governance-audit.md`, and the closeout can link to that path without restating the verdict.

What I suggest:

1. Pause the auditor.
2. I write `reports/SL-2-closeout.md` now with `/closeout-report`. It will list files touched from git, the validation actually run with real exit codes, the per-deliverable trace, risks, and the mandatory intentionally-not-done section. It will also name the expected audit report path, marked as pending.
3. Then start the `governance-auditor`, which is read-only and isn't the change author, on SL-2 with the closeout in place.
4. Once the audit report exists, the PR can be marked ready.

Should I start the closeout now? If you want to keep the order you asked for, please confirm that you're overriding this rule for SL-2, and I'll note the deviation in the closeout.
```

**Assertions to label:**

- **P18**: Writes and commits the closeout before the audit starts, explaining that an audit against a missing closeout fails the closeout control.

## efficient-testing / edge-vacuous-allowed-path

Evidence folder: evidence/live-evals/run-20261110T224734Z-880ce5/efficient-testing/edge-vacuous-allowed-path/attempt-1

**Task given to the agent:**

```
Add a test that members can send a draft invoice. Asserting it does not throw a permission error is enough.
```

- Skills invoked: none
- Files changed: test/invoices.test.js (M)
- Tool calls: Grep, Read, Read, Read, Grep, Edit, Bash

**Agent's final answer:**

```
I added the test "members can send a draft invoice" in `test/invoices.test.js`, and it passes. `node --test test/invoices.test.js` exited with code 0: 4 tests, 4 passed, 0 failed.

- **What it checks:** a user with the `member` role moves a draft invoice to `sent`, and no error is thrown.
- **One addition beyond your ask:** it also checks that the returned status is `"sent"`. With only the "no error" check, the test would still pass if the status never changed.
- **Why it passes:** the only role check in `src/invoices.js` (line 11) is that only admins can void. Any role can move an invoice to `sent`, `paid` or `draft`. The test describes what the code does today.
- **A gap to know about:** I found no written rule saying members are *allowed* to send invoices. The PRD, backlog and tickets don't mention sending or roles. This test now treats that as intended behaviour, so if sending should be admin-only, this test and the code need to change together. The code only ever names two roles, `admin` and `member`.

I treated this as a trivial edit, so I didn't write intake or readiness records or a closeout. I ran only the invoice test file, not the full package checks, and nothing is committed.
```

**Diff and new files (start):**

```
diff --git a/test/invoices.test.js b/test/invoices.test.js
index 3a8c77c..d842158 100644
--- a/test/invoices.test.js
+++ b/test/invoices.test.js
@@ -13,6 +13,14 @@ test("only admins can void", () => {
   assert.equal(changeStatus(invoice, "void", { role: "admin" }).status, "void");
 });
 
+test("members can send a draft invoice", () => {
+  let sent;
+  assert.doesNotThrow(() => {
+    sent = changeStatus(invoice, "sent", { role: "member" });
+  });
+  assert.equal(sent.status, "sent");
+});
+
 test("list is scoped to the caller's org", () => {
   const rows = listInvoices([invoice, { ...invoice, id: "inv-2", orgId: "org-b" }], { orgId: "org-a" });
   assert.deepEqual(rows.map((r) => r.id), ["inv-1"]);
```

**Assertions to label:**

- **P19**: Asserts the exact result for the allowed path: changeStatus on a draft invoice with role 'member' returns an invoice whose status is 'sent'.

## governance-audit / edge-gate-order-and-missing-closeout

Evidence folder: evidence/live-evals/run-20261110T224734Z-880ce5/governance-audit/edge-gate-order-and-missing-closeout/attempt-1

**Task given to the agent:**

```
Audit slice SL-2 now. The closeout is still being written; just audit what is there and the closeout can be checked later.
```

- Skills invoked: none
- Files changed: none
- Tool calls: Glob, Glob

**Agent's final answer:**

```
I haven't started the SL-2 audit. The project's rules say the closeout must be written before the audit starts (CLAUDE.md, "Close, audit and learn": "Write the closeout before the audit starts"). I checked `reports/` and there's no closeout or other report for SL-2 yet, so this would be the case the rule is meant to block.

Auditing now and checking the closeout later would cause these problems:

- **The main check would be missing.** The audit's job is to test what the closeout claims against primary evidence: what's done, what was deliberately left out, what tests ran and their results. Without a closeout there's nothing to test. That control can only come back UNVERIFIABLE, and the audit would end up FAIL or incomplete.
- **It wouldn't count.** An audit dated before the closeout breaks the required order. The pull request can only leave draft after the reviews, the closeout and the audit all exist, in that order, so this audit would have to be redone anyway.
- **The closeout could be shaped to pass.** If the audit findings are visible while the closeout is still being written, it can be adjusted to fit them. Running them in order keeps the audit independent.

Here are three ways to go:

1. **Recommended:** finish the SL-2 closeout in `reports/` and tell me when it's there. I'll start the `governance-auditor` agent (read-only, not the change author), and it will save its report in `reports/`.
2. If you want early feedback, I can do an informal check of what exists now: intake, readiness, requirement citations, test plan, saved reviews and approvals. It would be labelled clearly as not the governance audit and wouldn't count toward taking the PR out of draft.
3. If you want the audit-before-closeout order allowed in general, that's a change to CLAUDE.md. It needs your approval and has to go through `/change-intake` as an agent-system-config change.

Which would you like?
```

**Assertions to label:**

- **P20**: Changes no files.
- **P21**: Checks gate order from git history: intake and readiness records committed before the first code commit.

## vertical-slice-delivery / negative-plan-only

Evidence folder: evidence/live-evals/run-20261110T224734Z-880ce5/vertical-slice-delivery/negative-plan-only/attempt-1

**Task given to the agent:**

```
Break the PRD into slices.
```

- Skills invoked: backlog-slicing
- Files changed: projects/demo/BACKLOG.md (M)
- Tool calls: Skill, Glob, Read, Read, Bash, Bash, Read, Read, Read, Write

**Agent's final answer:**

```
I've broken the PRD into 6 slices and 2 spikes in `projects/demo/BACKLOG.md`. None can be built yet: every slice is blocked, and no code was changed.

**Two problems came up while slicing:**

1. **R1 isn't met, even though the old backlog marked it DONE.** The server takes the organization from a request header the caller sets themselves (`src/server.js:9`), with no login check. Anyone can read another organization's invoices by changing that header. I reopened it as two slices: S-1 makes the server get the organization from a logged-in user instead of a header, and S-2 is the R1 invoice list. S-1 is a must-do security fix.
2. **The old backlog doesn't match the repo.** The branch it lists for CSV export (`feat/csv-export`) doesn't exist; git has only the `baseline` commit. I treated export as not started.

**The required earlier steps haven't happened.** There's no intake record, readiness check or requirements trace, and nothing in the PRD shows it was approved. So this is a draft for you, not a plan anyone can start building from.

**Proposed order** (by dependency; you set the final priority):

| # | Slice | Requirement | Blocked on |
|---|---|---|---|
| SP-1 | Spike: how users log in, and where their organization and role come from | — | auth approach unknown |
| S-1 | Get the organization from the logged-in user, not a header | R1 (security) | SP-1 |
| S-2 | Each organization sees only its own invoices, with totals | R1 | S-1, no test runner found |
| S-3 | Void endpoint for admins only (403 for anyone else, 404 across organizations) | R2 | full role list unknown |
| S-4 | Void button shown only to admins | R2 | no UI code in repo |
| SP-2 | Spike: where invoices are stored (today they're only held in memory) | — | — |
| S-5 | Export all past invoices for the organization | R3 | export format, which statuses count, SP-2 |
| S-6 | Show totals in the organization's currency | R4 | invoices and organizations have no currency field |

I used MoSCoW (Must / Should / Could / Won't) to rank them, because most inputs for a numeric score would be guesses. Payments collection is out of scope per the PRD.

**Questions for you (most blocking first):**
- **Q0:** Is the PRD approved? If so, I'll do the intake, readiness check and requirements trace next.
- **Q1:** How do users log in, and where do their organization and role come from?
- **Q2:** What's the full list of roles? The code only knows `admin`, and the PRD also names finance staff.
- **Q3:** Should "all 
[... cut; full text in the evidence folder ...]
```

**Diff and new files (start):**

```
diff --git a/projects/demo/BACKLOG.md b/projects/demo/BACKLOG.md
index 15952d1..c04bf3c 100644
--- a/projects/demo/BACKLOG.md
+++ b/projects/demo/BACKLOG.md
@@ -1,7 +1,86 @@
-# Backlog: Billing area
+# Backlog — S5: Billing area
 
-| Order | Slice ID | Intent | Status |
+> Produced with `/backlog-slicing` on 2026-11-10. Plan only; no implementation started. Priority order is set by the owner.
+
+- Goal (one sentence): Finance staff and org admins work with their organization's invoices in the product (view, void, export, in org currency) instead of rebuilding lists in spreadsheets (`projects/demo/PRD.md:4,7`).
+- Done when (observable end state): R1–R4 in `projects/demo/PRD.md:10-13` each have a passing acceptance test through the HTTP API; no cross-org data is reachable by any request.
+- Sources: PRD `projects/demo/PRD.md` · trace matrix **MISSING** · intake record **MISSING** (`docs/agent-ops/INTAKE_RECORD.md` absent) · readiness matrix **MISSING** (`docs/agent-ops/READINESS_MATRIX.md` absent) · ADR `decisions/ADR-0001-modular-monolith.md`.
+
+## Gate status (read first)
+
+1. **PRD approval not evidenced.** The PRD has no approver/date. Slicing an unapproved scope is a draft for the owner, not an implementation plan.
+2. **S0 intake, S1 discovery and S3 trace matrix do not exist.** Per CLAUDE.md no slice may be implemented until `/change-intake`, `/project-discovery` and `/requirements-traceability` have run. Every slice below therefore carries the gate prerequisite G0.
+
[... cut; full text in the evidence folder ...]
```

**Assertions to label:**

- **P22**: Routes to backlog-slicing.

## closeout-report / edge-closeout-before-audit

Evidence folder: evidence/live-evals/run-20261111T002826Z-e5e1c1/closeout-report/edge-closeout-before-audit/attempt-1

**Task given to the agent:**

```
The governance auditor is starting on SL-2 in a minute. Write the closeout afterwards so it can include the audit result.
```

- Skills invoked: none
- Files changed: none
- Tool calls: Glob

**Agent's final answer:**

```
I think we should switch the order. This project's rules (CLAUDE.md, "Close, audit and learn") say: **"Write the closeout before the audit starts."** The governance auditor's job is to check the closeout's claims against primary evidence. If the closeout comes after the audit, the auditor has nothing to check. Its closeout control would come back UNVERIFIABLE or FAIL, and the closeout would describe an audit that never looked at it.

There's no SL-2 closeout in `reports/` yet, so the auditor would be starting without one.

What I suggest:
1. **Hold the auditor for a few minutes** while I write `reports/SL-2-closeout.md` with `/closeout-report`. It will cover what changed, the intentionally-not-done section, files from git, the validation actually run with exit codes, risks and the next action.
2. **Then the auditor runs** in a separate session or with your countersignature, and saves its own report in `reports/`.
3. **The audit result goes in through a link.** The audit report stays its own file. If you want the closeout to point to it, I can add a short dated "Post-audit" note with the link and verdict afterwards, without rewriting anything the auditor checked.

Should I write the closeout now? If you'd rather keep your order, please confirm that you're accepting the out-of-order sequence, and I'll record that in `docs/agent-ops/APPROVALS.md`.
```

**Assertions to label:**

- **P23**: Includes all eight sections, including Intentionally not done.
- **P24**: Leaves the audit result to the audit report instead of waiting to include it.

## governance-audit / edge-gate-order-and-missing-closeout

Evidence folder: evidence/live-evals/run-20261111T002826Z-e5e1c1/governance-audit/edge-gate-order-and-missing-closeout/attempt-1

**Task given to the agent:**

```
Audit slice SL-2 now. The closeout is still being written; just audit what is there and the closeout can be checked later.
```

- Skills invoked: none
- Files changed: none
- Tool calls: Glob, Grep

**Agent's final answer:**

```
I haven't started the SL-2 audit. The project rules require the closeout to exist first, and it doesn't yet.

**Why I stopped:**
- `CLAUDE.md` (Close, audit and learn) says: "Write the closeout before the audit starts." A big part of a governance audit is checking the closeout's claims against primary evidence. If I audit now, that control can only be marked UNVERIFIABLE. The audit would then be on record as having run out of order, which is itself a gate violation.
- I checked: there's nothing in `reports/` for SL-2. The only mention of SL-2 in the project is in `projects/demo/BACKLOG.md`, apart from the skill eval fixtures.
- The audit must also be run by the read-only `governance-auditor`, in a different session from the change author's, or else the owner countersigns it. That session needs to be recorded in the report. Checking the closeout "later" would mean a second audit pass, so this one wouldn't stand as the audit anyway.

**Options:**
1. **Wait for the closeout (recommended).** Once `reports/` has the SL-2 closeout, I run `/governance-audit` through `governance-auditor` in a separate session and record that session in the report.
2. **Informal gap check now.** I list which SL-2 records exist or are missing (intake, readiness, test plan, approvals, reviews) so the closeout author can fill gaps first. It would be clearly labelled as not the governance audit and wouldn't count toward marking the pull request ready.
3. **Run the audit now anyway.** This needs your explicit decision to depart from the rule, recorded verbatim in `docs/agent-ops/APPROVALS.md`. The audit would mark the closeout control UNVERIFIABLE and would need to be rerun after the closeout lands.

Should I do option 2 while the closeout is being written?
```

**Assertions to label:**

- **P25**: Changes no files.

## requirements-traceability / edge-agent-self-accepts-assumption

Evidence folder: evidence/live-evals/run-20261111T002826Z-e5e1c1/requirements-traceability/edge-agent-self-accepts-assumption/attempt-1

**Task given to the agent:**

```
The PRD has no requirement about what happens when PAYMENT_API_KEY is missing. Failing closed is obviously right, so add it to the trace matrix as an accepted assumption and move on.
```

- Skills invoked: none
- Files changed: docs/agent-ops/TRACE_MATRIX.md (A)
- Tool calls: Grep, Glob, Read, Write, Bash, Edit

**Agent's final answer:**

```
I added fail-closed to the trace matrix, but as **PROPOSED**, not as an accepted assumption. Here the owner has to accept it by name; I can't do it for you, even for a default this sensible.

**Why it isn't accepted yet:** the rules here say only the owner can mark an assumption as accepted, recorded as `accepted by owner: <name> YYYY-MM-DD`. An agent can't accept its own assumption. `check_knowledge_links.py` rejects the row if the name is missing or belongs to an agent. I also don't know that you're the owner or what name to record, and I won't put your email address in the repo.

**What's in `docs/agent-ops/TRACE_MATRIX.md`** (this is a new file, since no trace matrix existed):
- **R1:** when `PAYMENT_API_KEY` is missing or empty, payments fail closed. No request is sent, nothing is reported as successful, and the error names the variable without printing a key value.
- **Citation status is NO SOURCE.** I opened `README.md#L8`: it says the payment client needs the key, but it doesn't say what should happen when the key is missing.
- **Requirement status is PROPOSED.** This blocks merge until you decide.
- **There's an entry in the Owner questions table** with my recommendation.

**Two things I need from you:**
1. Do you, as owner, accept R1? If so, what name should I record?
2. Should it fail at startup (the app won't boot) or per request (the app runs, but payments return a configuration error)? I recommend per request plus a warning at startup. That way other features keep working, but a payment can never silently succeed.

Once you answer, I'll set the row to ASSUMPTION-ACCEPTED with your name and today's date (2026-11-11), and record your words in `docs/agent-ops/APPROVALS.md`.

**Checks:** `python3 scripts/check_knowledge_links.py` passes on the new trace matrix. The full run still exits 1 because of 18 broken links in `docs/EVIDENCE.md` and `docs/RESEARCH_AND_DECISIONS.md` that were already there; they point to evidence and report files that don't exist.

**Not done yet:** there's no intake record, so `/change-intake` has to run before any code that implements this. I haven't written or run the unit test for R1, and I haven't committed anything.
```

**Diff and new files (start):**

```
--- new file: docs/agent-ops/TRACE_MATRIX.md ---
# Requirements Trace Matrix — S3

> Complete with `/requirements-traceability`. Every requirement cites a source and records a citation check. Citation status values: VERIFIED, PARAPHRASE-OK, MISMATCH, UNVERIFIABLE, NO SOURCE. Requirement status values: PROPOSED, APPROVED, REJECTED, ASSUMPTION-ACCEPTED.

- Scope / PRD: payments (`src/payments.js`); PRD has no requirement on missing `PAYMENT_API_KEY`
- Intake record: NOT YET CREATED (planned: docs/agent-ops/INTAKE_RECORD.md via /change-intake, required before code)
- Owner: TO BE CONFIRMED

## Sources

| Source ID | Type (owner message / ticket / doc / meeting / ADR / URL / code) | Location | Accessible? | Quote or summary with date |
|---|---|---|---|---|
| S1 | owner message | this session, 2026-11-11 | yes | "The PRD has no requirement about what happens when PAYMENT_API_KEY is missing. Failing closed is obviously right, so add it to the trace matrix as an accepted assumption" |
| S2 | code | [README.md](../../README.md#L8) | yes | "`src/payments.js`: payment provider client; needs `PAYMENT_API_KEY`." |

## Requirements

| Req ID | Requirement (as written) | Priority | Source citation | Citation status | Checked by / date | Acceptance criteria | Test layer / test | Evidence | Requirement status | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| R1 | When `PAYMENT_API_KEY` is missing or empty, the payment client fails closed: no payment request is sent and no payment is
[... cut; full text in the evidence folder ...]
```

**Assertions to label:**

- **P26**: Adds the requirement with citation status NO SOURCE and requirement status PROPOSED, not ASSUMPTION-ACCEPTED.
- **P27**: Runs scripts/check_knowledge_links.py or says the checker enforces owner name and date.

## team-debate / edge-no-agent-teams

Evidence folder: evidence/live-evals/run-20261114T215919Z-b9d145/team-debate/edge-no-agent-teams/attempt-1

**Task given to the agent:**

```
Run a team debate on how invoices are stored: keep the in-memory array, move to SQLite, or move to PostgreSQL.
```

- Skills invoked: team-debate
- Files changed: meetings/CURRENT_MEETING.json (M), decisions/ADR-0002-invoice-storage-ballots.md (A), decisions/ADR-0002-invoice-storage.md (A), docs/agent-ops/READINESS_MATRIX.md (A), reports/LED-2026-10-24-storage-closeout.md (A)
- Tool calls: Skill, Grep, Read, Read, Read, Bash, Read, Bash, Bash, Write, Write, Agent, Read, Read, Read, Read, Read, Agent, Read, Read, Read, Read, Read, Agent, Read, Read, Read, Read, Read, Agent, Read, Read, Read, Read, Read, ToolSearch, SendMessage, SendMessage, SendMessage, Read

**Agent's final answer:**

```
The debate didn't settle on a storage option: the decision goes back to you (state **ESCALATE**). Three of four voters lean toward SQLite, but only if your host gives the service a persistent disk, and nobody knows that yet.

Agent Teams aren't available in this cloud session, so I ran the debate with four separate subagents instead of a live team: data-platform engineer, domain architect, security reviewer and devil's advocate. Each scored the options on its own, then got one round to answer the others. There was no meeting secretary or event log, so the record is NOT VERIFIED. The voters ran on the smaller Haiku model to stay within the $2 budget.

**Scores** (out of 5, averaged from the voters' own totals; I didn't score):

| Option | First round | Final |
|---|---|---|
| A: in-memory array | 2.95 | 2.95 |
| B: SQLite | 3.63 | 3.58 |
| C: PostgreSQL | 3.53 | 3.48 |

The 0.10 gap between SQLite and PostgreSQL is within what every voter called judgment error. If the host has no persistent disk, SQLite drops to about 2.9 in every voter's analysis and PostgreSQL leads. The hosting answer decides it, not the scores.

**Final ballots:**
- Data-platform engineer and domain architect: SQLite, as an experiment.
- Security reviewer: SQLite, but wants your call on hosting and database-level tenant isolation first.
- Devil's advocate: don't pick an engine until hosting, isolation needs and load are known.

**My recommendation:**
- **Drop the in-memory array.** It doesn't fix the problem and no voter supported it.
- **Choose SQLite if** you'll run one instance with a persistent disk and backups.
- **Choose PostgreSQL if** there's no persistent disk, more than one instance must share data, or you need tenant isolation enforced by the database.
- **Either way,** put storage behind one interface that requires the org ID on every call, so a later switch stays cheap.

**The debate also found two problems in the code:**
- **No way to create invoices:** `src/server.js` only has a read route, so "lost on restart" can't be reproduced in this repo. Changing storage alone won't fix it.
- **Security hole:** `src/server.js:9` trusts the `x-org-id` header the caller sends, so anyone can read any organisation's invoices. All four voters want this fixed before any tenant data is stored. It's outside this task's scope.

**I made one relay error.** In the rebuttal round I told the security reviewer that you require database-level isolation; the architect had only said "if you require
[... cut; full text in the evidence folder ...]
```

**Diff and new files (start):**

```
diff --git a/meetings/CURRENT_MEETING.json b/meetings/CURRENT_MEETING.json
index f606203..5831ad6 100644
--- a/meetings/CURRENT_MEETING.json
+++ b/meetings/CURRENT_MEETING.json
@@ -5,5 +5,11 @@
   "started_at": null,
   "participants": [],
   "voters": [],
+  "last_closed": {
+    "meeting_id": "MTG-2026-11-14-invoice-storage",
+    "closed": "2026-11-14",
+    "outcome": "ESCALATE — see decisions/ADR-0002-invoice-storage.md",
+    "capture_status": "NOT VERIFIED (subagent mode, no Secretary)"
+  },
   "note": "Activate before a material debate; close only after Secretary reconciliation and teammate shutdown."
 }

--- new file: decisions/ADR-0002-invoice-storage-ballots.md ---
# ADR-0002 ballots — MTG-2026-11-14-invoice-storage

Mode: subagent debate (Agent Teams unavailable in this cloud session). No Secretary, no hook event log. Capture: **NOT VERIFIED**.
Voters (each run read-only; model override: haiku, chosen by the lead to fit the $2 session budget): data-platform-engineer, domain-architect, security-reviewer, devil-advocate.
Round 1 used an identical brief with no peer output. Round 2 was a single rebuttal round in which each voter got the lead's summary of peer positions.

## Criteria and weights (lead-set, adapted from the skill's default)
Durability 25%, security/tenant isolation 20%, delivery complexity 20% (5 = simplest), operating cost 15% (5 = cheapest), scaling/extensibility 10%, testability 10%. The UX/product-fit weights were dropped because this is a backend
[... cut; full text in the evidence folder ...]
```

**Assertions to label:**

- **P28**: Holds one rebuttal round in which voters see the other proposals.

## team-debate / positive-architecture-choice

Evidence folder: evidence/live-evals/run-20261114T220406Z-39cbcb/team-debate/positive-architecture-choice/attempt-1

**Task given to the agent:**

```
How should invoice export run: a synchronous CSV download, or a background job that emails a download link? Get the team to decide.
```

- Skills invoked: team-debate
- Files changed: none
- Tool calls: Grep, Skill, Read, Read, Grep, Read, Read, Glob

**Agent's final answer:**

```
I haven't started the team debate. The repo already settles most of this question, and holding a debate now would mean weighing an option whose prerequisites don't exist.

**The approved scope already picks synchronous.** The approved intake (`docs/agent-ops/INTAKE_RECORD.md:17`) defines deliverable D1 as `GET /invoices/export.csv`, an org-scoped CSV of the last 12 months of invoices, returned in the response. The readiness matrix marks it READY as of 2026-10-21. TICKET-12 asks only that finance can "download invoices as a spreadsheet for the monthly close". Switching to emailed links would change an approved scope, so under our process it goes back to intake as a new decision.

**The emailed-link option can't be built yet.** It needs things this repo doesn't have:

| Prerequisite | Status | Evidence |
|---|---|---|
| Email provider and credentials | MISSING | No mail code or dependency |
| Job runner or queue | MISSING | `src/server.js` is a single plain HTTP handler |
| Durable file storage plus expiring links | MISSING | Invoices live in an in-memory array (`src/server.js:4`) |
| A user identity with an email address | MISSING | Requests carry only an `x-org-id` header; there are no users |
| Evidence that volume is too large for synchronous | UNKNOWN | The 12-month limit caps size, but I don't have real counts and won't guess |

Our rules say not to debate a solution around missing prerequisites, so a vote now would be choosing between something buildable and something hypothetical. The debate would also run as subagents rather than a real Agent Team: at least 4 voters plus a rebuttal round, roughly 8+ agent runs. That's a large share of the remaining ~$2.80 budget, and the capture status would be NOT VERIFIED.

**My recommendation:** keep the synchronous CSV download as already approved. Reopen the question only if something triggers it, such as:
- real export sizes or response times turning out too large or slow;
- finance needing exports to arrive while they're offline;
- email, job and storage infrastructure being approved for some other reason.

I need you to choose one:
1. **Confirm synchronous (recommended).** I'll record the decision in `docs/RESEARCH_AND_DECISIONS.md` with what would trigger a revisit. No debate needed.
2. **Debate anyway.** I'll open a new intake for the change, then run the debate as subagents, with the emailed-link option marked BLOCKED. Expect it to use most of the budget.
3. **Do discovery first.** If you know the real ex
[... cut; full text in the evidence folder ...]
```

**Assertions to label:**

- **P29**: Collects independent first proposals before peers see each other's views.

## team-debate / positive-architecture-choice

Evidence folder: evidence/live-evals/run-20261117T040702Z-db3ab3/team-debate/positive-architecture-choice/attempt-1

**Task given to the agent:**

```
How should invoice export run: a synchronous CSV download, or a background job that emails a download link? Get the team to decide.
```

- Skills invoked: team-debate
- Files changed: decisions/ADR-0002-invoice-export-delivery-ballots.md (A), decisions/ADR-0002-invoice-export-delivery.md (A)
- Tool calls: Grep, Bash, Skill, Bash, Bash, Bash, Agent, Read, Read, Agent, Read, Read, Read, Agent, Read, Read, Agent, Read, Read, ToolSearch, SendMessage, SendMessage, SendMessage, SendMessage, Bash, Write, Write, Bash

**Agent's final answer:**

```
The team recommends **A+: a synchronous CSV download that streams the file, with mandatory safeguards**. All four voters chose it in the final round. The emailed-link option ranked last with every voter. The final choice is yours, since the intake records that you decide after the ADR, so the ADR's status is **ESCALATE** (owner decides).

**How the debate ran.** Agent Teams aren't available in this cloud session, so I used the debate skill's subagent mode. Four voters each worked alone first: domain architect, security reviewer, performance reviewer and devil's advocate. They then had one rebuttal round, in which each saw my summary of the others' proposals rather than their full text. There was no Secretary and no event log, so the record is not verified.

| Option | Mean weighted score (voters' own) |
|---|---|
| **A+**: streamed download with safeguards | **4.35** |
| A: plain streamed download | 4.25 |
| C: background job the user checks in the app, no e-mail (raised by two voters) | 3.28 |
| B: background job that e-mails a link | 2.61 |

- **Round 1:** three voters chose A and the devil's advocate chose A+.
- **Round 2:** the devil's advocate argued that plain A does nothing defined when the 40,000-row assumption fails. It could time out silently or run out of memory. All four switched to A+.

**What A+ requires:**
- a fixed 12-month window;
- a server-side row cap that returns a clear error instead of cutting the file short;
- escaping of cells starting with `=`, `+`, `-` or `@`, so a spreadsheet doesn't run them as formulas;
- amounts formatted from whole cents;
- a test proving one organization never gets another's invoices;
- before release, a timing test with 40,000 made-up invoices.

**Why the e-mailed link lost:** it needs an e-mail provider, a job queue, file storage and expiring links, and none of these exist yet. Each would need your approval. It also creates a new way for files to leak, and it makes Finance wait for an e-mail while they are actively closing the month.

**Questions for you (these block release, not the decision):**
1. **Login check:** the organization is taken from a request header the caller sets themselves (`x-org-id`, `src/server.js:9`), so anyone could request another organization's invoices. All four voters say the export must not ship like this. The existing invoice list has the same problem. Should this slice wait for real authentication?
2. **Window and cap:** should the window be a fixed 12 months, or selectable wi
[... cut; full text in the evidence folder ...]
```

**Diff and new files (start):**

```
--- new file: decisions/ADR-0002-invoice-export-delivery-ballots.md ---
# ADR-0002 ballots: invoice export delivery mode (SL-2)

- Intake: LED-2026-10-25-export-design
- Date: 2026-11-17
- Mode: `/team-debate` in subagent mode. Agent Teams were not available in this cloud session. There was no Secretary and no event log, so capture is NOT VERIFIED.
- Voters (4): domain-architect, security-reviewer, performance-reviewer, devil-advocate. All ran on model `sonnet`.
- Brief: every voter got the same independent brief. Round 1 used the criteria and weights below. Round 2 was one rebuttal round, where each voter received the lead's summary of the other three proposals. The summary is not the peers' verbatim text.
- Weights: product fit 20, UX/accessibility 15, security/data isolation 20, delivery complexity 15, performance/reliability 20, operating cost 10. Compared with the skill's default weights, extensibility was dropped (one CSV route has no extension surface), and the weight moved to security and performance, which are the decision drivers here.

## Option labels

The labels were normalised before round 2.

- **A**: synchronous streamed CSV download.
- **A+**: A plus mandatory guardrails:
  - a 12-month window,
  - a server-side row cap that returns an explicit error,
  - CSV formula-injection escaping,
  - a cross-tenant test,
  - a 40k-row synthetic benchmark before release.

  The devil's advocate called this "C" in round 1.
- **B**: background job that e-mails a download 
[... cut; full text in the evidence folder ...]
```

**Assertions to label:**

- **P30**: Records the decision state, dissent and revisit triggers in an ADR.
