#!/usr/bin/env bash
# Install Orcasus v2.2.0 into a new, empty app repository for Thai Binh Social Hub.
# Usage (from anywhere):  bash projects/thai-binh-social-hub/bootstrap/install-orcasus.sh ../tb-social-hub
# Works on macOS, Linux, WSL and Git Bash on Windows. It does not push, deploy or install packages.
set -euo pipefail

TARGET="${1:-}"
if [ -z "$TARGET" ]; then
  echo "Usage: $0 <target-directory>   (e.g. ../tb-social-hub)" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"           # projects/thai-binh-social-hub
ORCASUS="$(cd "$PROJECT_DIR/../.." && pwd)"           # orcasus repo root

[ -f "$ORCASUS/CLAUDE.md" ] && [ -f "$ORCASUS/scripts/validate_bundle.py" ] || {
  echo "Cannot find the Orcasus root at $ORCASUS" >&2; exit 1; }

mkdir -p "$TARGET"
if [ -n "$(ls -A "$TARGET" 2>/dev/null | grep -v '^\.git$' || true)" ]; then
  echo "Target $TARGET is not empty; refusing to overwrite. Use a new or empty folder." >&2
  exit 1
fi
TARGET="$(cd "$TARGET" && pwd)"

# Pick a Python 3 interpreter (Orcasus hooks and validators need one).
PY=""
for c in python python3 py; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; sys.exit(0 if sys.version_info[0]==3 else 1)' 2>/dev/null; then PY="$c"; break; fi
done
[ -n "$PY" ] || { echo "Python 3 is required (python, python3 or py)." >&2; exit 1; }

echo "==> Copying Orcasus from $ORCASUS"
( cd "$ORCASUS" && tar cf - --exclude=./.git --exclude=./projects --exclude='node_modules' --exclude='__pycache__' . ) \
  | ( cd "$TARGET" && tar xf - )
mkdir -p "$TARGET/projects"
touch "$TARGET/projects/.gitkeep"

echo "==> Copying project records (plan, deck, design-system snapshot, handoff)"
( cd "$ORCASUS/projects" && tar cf - --exclude='node_modules' thai-binh-social-hub ) | ( cd "$TARGET/projects" && tar xf - )

echo "==> Adding the project section to CLAUDE.md"
cat "$SCRIPT_DIR/CLAUDE.project.md" >> "$TARGET/CLAUDE.md"

echo "==> Writing a project README header (Orcasus README kept below it)"
{
  printf '# Thai Binh Social Hub\n\n'
  printf 'Internal mobile-first web app for Thai Binh Corp employees to engage with the company'\''s Facebook/Instagram channels, with gamification.\n\n'
  printf -- '- Plan: `projects/thai-binh-social-hub/PLAN.md`\n- Local handoff: `projects/thai-binh-social-hub/HANDOFF_LOCAL.md`\n- Operating system: Orcasus v2.2.0 (below and `CLAUDE.md`)\n\n---\n\n'
  cat "$ORCASUS/README.md"
} > "$TARGET/README.md"

# Orcasus hooks call `python`. On machines where only python3/py exists, point hooks at it.
if [ "$PY" != "python" ]; then
  echo "==> 'python' not found; pointing Orcasus hooks at '$PY'"
  "$PY" - "$TARGET/.claude/settings.json" "$PY" <<'EOF'
import json, sys
p, py = sys.argv[1], sys.argv[2]
d = json.load(open(p, encoding="utf-8"))
for groups in d.get("hooks", {}).values():
    for g in groups:
        for h in g.get("hooks", []):
            if h.get("command") == "python":
                h["command"] = py
json.dump(d, open(p, "w", encoding="utf-8"), indent=2)
open(p, "a", encoding="utf-8").write("\n")
EOF
fi

echo "==> Running Orcasus validators"
( cd "$TARGET" && "$PY" scripts/test_meeting_logger.py && "$PY" scripts/validate_bundle.py )

echo "==> Initialising git (no remote, no push)"
cd "$TARGET"
if [ ! -d .git ]; then git init -q -b main 2>/dev/null || { git init -q && git checkout -q -b main; }; fi
git add -A
git commit -q -m "chore: install Orcasus v2.2.0 and Thai Binh Social Hub project records" || true

cat <<EOF

Done. Next steps:
  1. Create an EMPTY *private* GitHub repo, e.g. haidongkixot/tb-social-hub (no README/licence).
  2. cd "$TARGET"
     git remote add origin https://github.com/haidongkixot/tb-social-hub.git
     git push -u origin main
  3. Run: claude   (log in with your Claude account, trust the folder)
  4. Paste the first-session prompt from projects/thai-binh-social-hub/HANDOFF_LOCAL.md section 6.
EOF
