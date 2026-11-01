# Structured Debate Protocol

## Purpose
Use independent contributions and evidence-based falsification to select the best supported option under explicit constraints, not to stage a vote that validates the first proposal.

## Preparation
1. Run Project Discovery where feasibility depends on repository resources.
2. State decision question, constraints, non-goals, deadline, criteria and decision owner.
3. Select 3–5 relevant specialists plus non-voting Team Secretary.
4. Define weighted criteria and explain why they fit this decision.
5. Activate a unique meeting record and confirm actual Agent Teams support.

## Rounds
1. Independent proposals: recommendation, evidence, assumptions, cost, benefits, risks, confidence and what would change the view.
2. Evidence sharing: sources, code paths, environment facts and labelled hypotheses.
3. Peer critique: each proposal receives a concrete challenge.
4. Rebuttal: proposal owners respond and may revise.
5. Devil's Advocate: strongest counterargument, simpler viable alternative and worst credible failure mode.
6. Score options in a weighted matrix; each score needs evidence, not invented metrics.
7. Every designated voter sends one explicit FINAL_BALLOT to the secretary. Never infer a vote from silence.
8. Lead records DECIDED, EXPERIMENT, ESCALATE or DEFER in an ADR, including dissent, uncertainty and revisit triggers.

## Subagent mode
When Agent Teams are unavailable, run the rounds with at least 4 independent subagent voters, including the Devil's Advocate. Each voter scores the matrix and returns a FINAL_BALLOT; one rebuttal round follows. Save ballots and scores verbatim in `decisions/<adr-id>-ballots.md`. Capture status is NOT VERIFIED. See the team-debate skill.

## Example criteria for platform decisions
Product fit 20%, UX/accessibility 20%, extensibility 15%, security/data isolation 15%, delivery complexity 10%, performance/reliability 10%, operating cost 10%. Adjust and explain weights for the actual question.

## Ballot format
FINAL_BALLOT
meeting_id: <meeting-id>
voter: <agent-name>
choice: <option-id | EXPERIMENT | DEFER | ABSTAIN>
confidence: <1-5>
rationale: <concise stated reason>
evidence_ids: <references or NONE>
reservation: <main concern or NONE>

## Guardrails
Secretary does not vote unless the owner explicitly changes that rule. A vote is an input, not proof. Preserve minority views. Limit critique/rebuttal to two cycles unless new evidence justifies more. If evidence is insufficient, run a bounded experiment or escalate. Record expressed rationale only; never request or claim access to hidden chain-of-thought.
