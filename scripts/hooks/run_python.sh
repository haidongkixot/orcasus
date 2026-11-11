#!/bin/sh
# Portable Python launcher for Orcasus hooks.
#
#   run_python.sh <script.py> [args...]   run a hook script; hook JSON stays on stdin
#   run_python.sh --check                 print interpreter status (SessionStart)
#
# Candidates, in order: $ORCASUS_PYTHON, python3, python, py -3. Each candidate is
# probed by running it, so a launcher stub that exists but is not Python 3.8+
# (for example the Windows Store alias) is skipped. When no interpreter works,
# the launcher records the failure in meetings/HOOK_ERRORS.log, prints a warning
# on stderr and exits 1: a non-blocking hook error that never stops a team message.
set -u

root="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"

probe() {
    "$@" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' </dev/null >/dev/null 2>&1
}

resolve() {
    for candidate in "${ORCASUS_PYTHON:-}" python3 python; do
        [ -n "$candidate" ] || continue
        if probe "$candidate"; then
            echo "$candidate"
            return 0
        fi
    done
    if probe py -3; then
        echo "py -3"
        return 0
    fi
    return 1
}

if [ "${1:-}" = "--check" ]; then
    if interpreter=$(resolve); then
        # Unquoted on purpose: "py -3" is a command plus one argument.
        version=$($interpreter -c 'import platform; print(platform.python_version())' </dev/null 2>/dev/null)
        echo "Orcasus hook runtime: OK ($interpreter, Python $version). Meeting logger hooks can run."
    else
        echo "Orcasus hook runtime: WARNING - no Python 3.8+ interpreter found (tried ORCASUS_PYTHON, python3, python, py -3)."
        echo "Meeting logger hooks will fail and team messages will NOT be recorded. Meeting capture can be at most PARTIAL until fixed."
        echo "Fix: install Python 3.8+ or set ORCASUS_PYTHON to the interpreter path, then start a new session."
    fi
    exit 0
fi

if [ "$#" -lt 1 ]; then
    echo "[orcasus hook] usage: run_python.sh <script.py> [args...] | --check" >&2
    exit 1
fi

script="$1"
shift

if interpreter=$(resolve); then
    # Unquoted on purpose: "py -3" is a command plus one argument.
    exec $interpreter "$script" "$@"
fi

stamp=$(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || echo unknown-time)
if mkdir -p "$root/meetings" 2>/dev/null; then
    printf '%s\t%s\t%s\n' "$stamp" "${script##*/}" "no Python 3.8+ interpreter (tried ORCASUS_PYTHON, python3, python, py -3)" >> "$root/meetings/HOOK_ERRORS.log" 2>/dev/null
fi
echo "[orcasus hook] ${script##*/} did not run: no Python 3.8+ interpreter found. Event NOT recorded; see meetings/HOOK_ERRORS.log." >&2
exit 1
