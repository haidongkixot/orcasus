---
name: root-cause-debate
description: Investigate hard-to-reproduce defects with competing hypotheses, independent experiments, peer falsification, and evidence-based convergence.
---

# Root Cause Debate

1. Capture symptom, reproduction, environment, expected/actual result, change history and logs with secrets removed.
2. Inspect access, environment, test data, assets and integrations before assuming a code defect.
3. Spawn 3–5 teammates with distinct hypotheses; record independent first assessments.
4. Each hypothesis states supporting/contradicting evidence and a discriminating experiment.
5. Teammates challenge peers and update beliefs as evidence changes.
6. Run safe, controlled experiments. No production-impacting changes or data deletion.
7. Use the cheapest test that can falsify a hypothesis; do not create screenshot batches as a substitute for diagnosis.
8. Update hypothesis table: claim, evidence, experiment, result and confidence.
9. Add regression tests for confirmed causes; rerun targeted tests.
10. Stop after two rounds with no new evidence; report unresolved cause and next experiment.
