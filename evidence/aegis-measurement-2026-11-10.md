# Skill-description measurement: Orcasus vs Aegis

- Date: 2026-11-11 (re-measured; first measured on 2026-11-10 with an ad-hoc regex)
- Aegis: `haidongkixot/aegis-ref` at `3e11d6bba4eade68b9226bec06ca3cd36ef035c3` (Apache-2.0)
- Orcasus: `f7567a8` (before the focus rule) and the branch head after it
- Method: `scripts/skill_focus.descriptions()` over `.claude/skills/*/SKILL.md` front matter, excluding `_template`. The routing graph comes from Aegis's own `artifacts/audits/corpus-route-graph.json`.

```
python3 - <aegis-root> <<'PY'
import sys, json; sys.path.insert(0, 'scripts'); import skill_focus
from pathlib import Path
d = skill_focus.descriptions(Path(sys.argv[1])); d.pop('_template', None)
print(len(d), sum(map(len, d.values())), sum('Do NOT use' in v for v in d.values()))
PY
```

| Repository | Skills | Description characters | Descriptions with "Do NOT use" | Routing graph |
|---|---:|---:|---:|---|
| Aegis `3e11d6b` | 194 | 173,103 | 177 | 186 nodes, 990 edges |
| Orcasus `f7567a8` (before) | 16 | 5,757 | 7 | — |
| Orcasus after the focus rule | 16 | 6,698 | 16 | — |

Corrections to earlier figures:
- The first measurement (173,285 characters) used a different regex.
- The first measurement claimed a "Do NOT use" clause in every Aegis skill. That count came from whole files: 177 descriptions have the clause, while all 194 files contain the phrase somewhere.
- The Orcasus "before" figure was 5,771 in the first measurement and is 5,757 by the same method.
