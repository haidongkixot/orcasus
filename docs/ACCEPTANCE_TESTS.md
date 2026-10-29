# Acceptance Tests — Complete Agent Team System

Run in a non-production workspace. Static tests do not substitute for runtime acceptance.

## A. Package/configuration
- [ ] JSON in .claude/settings.json parses.
- [ ] Exactly 15 named role definitions are discoverable under .claude/agents.
- [ ] All 9 skills have valid frontmatter and a non-empty body.
- [ ] Python logger unit tests pass.
- [ ] Bundle validator passes.
- [ ] Permission rules preserve secret-file guards and ask before sensitive operations.

## B. Agent Team runtime
- [ ] A new interactive Claude Code session actually starts a team when requested.
- [ ] Team lead creates named teammates, task ownership and dependencies.
- [ ] At least two teammates successfully message each other.
- [ ] Shared task list/task dependencies work in this specific runtime, or limitation is reported.
- [ ] Team Secretary starts before substantive debate.

## C. Secretary capture and ballots
- [ ] Create an active meeting manifest with a unique safe meeting ID.
- [ ] Send test messages from at least two real teammates through the supported message tool.
- [ ] Verify a hook-created JSON event exists with correct meeting ID, sender/recipient and usable stated content.
- [ ] Compare sampled actual messages to event files and document missing/redacted fields.
- [ ] Each designated voter sends an explicit FINAL_BALLOT.
- [ ] Missing ballots are marked missing; no votes are inferred from silence.
- [ ] Coverage report status is CAPTURE VERIFIED only if evidence supports it; otherwise PARTIAL or NOT VERIFIED.
- [ ] Secretary logs no hidden chain-of-thought and redacts common secret patterns.

## D. Discovery and blocker gate
- [ ] Orchestrator invokes Project Discovery for a non-trivial feature.
- [ ] Readiness matrix includes repository, assets/licenses, integrations, permissions/scopes, environments, test tools and budget.
- [ ] UNKNOWN is not treated as AVAILABLE.
- [ ] Missing required resource yields a blocker plus feasible options and recommendation.
- [ ] No silent fake integration, placeholder asset or degraded workaround is implemented.
- [ ] Implementation is not delegated until readiness is reviewed; independent read-only discovery may proceed.

## E. Testing economics
- [ ] Test plan maps every acceptance criterion to a justified test layer.
- [ ] Screenshot, trace and video budgets start at zero.
- [ ] Routine tests do not create visual artifacts unnecessarily.
- [ ] Any nonzero capture has a named question, bounded count, target viewports, storage/retention and approval or pre-approved CI policy.
- [ ] Generated images are not used as evidence that the running app works.
- [ ] Test failure is diagnosed before retry; targeted tests run before a broad suite.
- [ ] Report includes actual commands, exit codes, counts, artifact counts and unverified areas.

## F. Debate and decision quality
- [ ] Independent first proposals exist before peer discussion.
- [ ] Each option receives a concrete peer challenge and a rebuttal.
- [ ] Devil's Advocate identifies credible alternative and failure mode.
- [ ] Scoring criteria/weights are explicit and scores have evidence.
- [ ] Votes are explicit, secretary does not vote by default, and dissent is preserved.
- [ ] ADR documents chosen option, alternatives, rationale, risks, unknowns and revisit trigger.

## G. Delivery readiness
- [ ] QA and relevant security/UX/performance/mobile reviewers inspect actual evidence.
- [ ] Critical data-integrity, tenant-isolation or authorization defects block readiness.
- [ ] Tests and visual inspections are not claimed if not executed.
- [ ] Deployment/publishing remains separately approval-gated.

## Expected report format
Record each check as PASS, FAIL, BLOCKED, NOT RUN or NOT APPLICABLE. Include the evidence path and explain runtime checks not attempted.
