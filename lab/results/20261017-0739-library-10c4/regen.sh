#!/usr/bin/env bash
# Regenenerates every number in dossier.md. ~2 min on the lab box (plus one cold release build).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
RUN="$ROOT/lab/results/20261017-0739-library-10c4"
cd "$ROOT"

# 1. the link stub (Linux proc_pid_rusage) — the run's only source edit.
#    Idempotent: the tree may be clean or may already carry the edit (the
#    runner's first attempt applied the patch onto the still-edited tree
#    and died here), so accept both states and only fail if it fits neither.
if git apply --check --reverse "$RUN/work/patch.diff" 2>/dev/null; then
    echo "patch already applied; leaving the tree as is"
elif git apply --check "$RUN/work/patch.diff" 2>/dev/null; then
    git apply "$RUN/work/patch.diff"
else
    echo "FATAL: patch.diff fits neither a clean nor a patched tree" >&2
    exit 1
fi

# 2. the Readwise cache (verbatim quotes). Fetch fresh pages, but never let
#    a token/network failure overwrite the cached pages with garbage.
cd "$RUN/work"
if [ -n "${READWISE_TOKEN:-}" ]; then
    rm -f tmp_page_*.json
    cursor=""; i=0; ok=1
    while :; do
        i=$((i+1))
        resp=$(curl -s --max-time 30 -H "Authorization: Token $READWISE_TOKEN" \
            "https://readwise.io/api/v2/export/?pageCursor=$cursor") || resp=""
        if ! printf '%s' "$resp" | python3 -c \
            'import sys,json; d=json.load(sys.stdin); sys.exit(0 if isinstance(d,dict) and "results" in d else 1)' 2>/dev/null; then
            echo "Readwise fetch failed at page $i; keeping the cached pages"
            ok=0; break
        fi
        printf '%s' "$resp" > "tmp_page_$i.json"
        nc=$(printf '%s' "$resp" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("nextPageCursor") or "")')
        [ -z "$nc" ] && break
        cursor="$nc"
    done
    if [ "$ok" = 1 ]; then
        rm -f page_*.json
        for f in tmp_page_*.json; do mv "$f" "page_${f#tmp_page_}"; done
    fi
    rm -f tmp_page_*.json
else
    echo "READWISE_TOKEN unset; using the cached pages"
fi
python3 build_index.py
python3 verify_quotes.py

# 3. the boundary outcome-class census (one shipped flight, its own stats print)
cd "$ROOT"
cargo build --release -p emergent-universe --example nladder
"${CARGO_TARGET_DIR:-target}/release/examples/nladder" 10000 coast 60 600 > "$RUN/work/flight_10k.log" 2>&1
python3 "$RUN/work/census.py" "$RUN/work/flight_10k.log"

# 4. the S* sensitivity arithmetic on the page's published constants
python3 "$RUN/work/arithmetic.py"
