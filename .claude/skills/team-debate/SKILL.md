---
name: team-debate
description: Run structured Agent Team discussion and critique to compare competing product, architecture, UX, or implementation options and record a justified decision.
---

# Team Debate Protocol

Use native Agent Teams for material choices with genuine uncertainty. The current main session is lead and decision owner.

## Before the debate
1. For architecture/implementation decisions, run project-discovery and classify readiness first. The team may perform parallel read-only discovery, but do not debate a chosen solution around unverified prerequisites.
2. Choose 4–6 relevant voters/specialists, not the whole roster. Start team-secretary before substantive discussion.
3. Activate meetings/CURRENT_MEETING.json with a unique meeting ID; define question, constraints, non-goals, criteria and weights.
4. Explain privacy boundary: only outwardly stated messages/rationales are recorded; no hidden chain-of-thought.
5. Confirm actual Agent Teams support, peer messaging and task tools. If unavailable, report it without simulating success.

## Debate rounds
1. Independent proposals: recommendation, evidence, assumptions, risks, costs, confidence and what would change the recommendation before reading peers.
2. Evidence sharing: cite sources, code paths, runtime facts or labelled hypotheses.
3. Peer critique: each option receives at least one concrete challenge.
4. Rebuttal/revision: proposal owners respond and revise or explain disagreement.
5. Devil's Advocate: strongest counterargument and credible simpler alternative.
6. Score options with weighted matrix; justify scores with evidence, not invented measurements.
7. Vote: each designated voter sends one FINAL_BALLOT directly to team-secretary. Secretary does not vote and never infers a vote from silence.
8. Converge: lead records decision, dissent, unknowns, risks and revisit triggers in an ADR.

Default example weights for platform choices: product fit 20%, UX/accessibility 20%, extensibility 15%, security/data isolation 15%, delivery complexity 10%, performance/reliability 10%, operating cost 10%. Adapt to decision and explain changes.

## Subagent mode (Agent Teams unavailable)
When step 5 shows Agent Teams or peer messaging are unavailable (for example in `claude -p` or a cloud session), run the debate with subagents instead of skipping it:
1. Use at least 4 voters, one of them `devil-advocate`. Each gets the same brief and no peer output, so the first proposals stay independent.
2. Each voter scores every option in the weighted matrix itself and ends its report with a FINAL_BALLOT in the protocol format. The lead never scores for the voters.
3. Hold one rebuttal round: give each voter the other proposals and ask for challenges and a revised or confirmed ballot.
4. Save every ballot and the voters' matrix rows verbatim in `decisions/<adr-id>-ballots.md` before writing the ADR; the ADR links to that file and averages the voters' scores.
5. There is no Secretary or event log, so capture status is NOT VERIFIED. Record each deviation from the full protocol in the ADR.

## Decision states
- DECIDED — evidence/criteria are sufficient.
- EXPERIMENT — bounded spike, usability or load test required.
- ESCALATE — owner decision required.
- DEFER — not important enough now.

## Guardrails
- Maximum two critique/rebuttal cycles per decision unless lead documents why more are needed.
- No unsupported consensus. Preserve minority views.
- Do not call a choice optimal without objective, constraints and trade-offs.
- No silent workaround for missing resource, permission or asset.
- Record stated rationale/evidence, never hidden or unexpressed thought.

Close with secretary reconciliation, coverage report and CAPTURE VERIFIED / PARTIAL / NOT VERIFIED status.
