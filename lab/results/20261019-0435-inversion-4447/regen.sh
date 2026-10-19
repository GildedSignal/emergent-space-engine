#!/usr/bin/env bash
# Regenerates every number in dossier.md: builds the patched nladder (work/patch.diff,
# applied by the runner before this runs) and flies the three arms sequentially on a
# quiet box, then prints the window slopes. ~7 min warm, ~10 min cold build.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
root="$(cd "$here/../../.." && pwd)"
cd "$root"
BIN=$(cargo metadata --no-deps --format-version 1 | jq -r .target_directory)/release/examples/nladder
if [ ! -x "$BIN" ] || [ "${FORCE_BUILD:-0}" = 1 ]; then cargo build --release -p emergent-universe --example nladder; fi
run() { local log="$1"; shift; LADDER_PROBE=1 LADDER_CAP_S=500 LADDER_RSS_MB=1600 "$BIN" "$@" > "$here/logs/$log" 2>&1; echo "== $log: $(grep -c '^probe:' "$here/logs/$log") probes; $(grep -m1 'guard hit' "$here/logs/$log" || echo 'no guard (ran to frames/wall cap)')"; tail -1 "$here/logs/$log"; }
run burn-1e4.log 10000 burn 8000 100 12
run coast-1e4.log 10000 coast 8000 100 12
run burn-3e4.log 30000 burn 8000 100 12
echo "== window slopes (MB per 1k game-s), burn 1e4:"; python3 "$here/slopes.py" "$here/logs/burn-1e4.log"
echo "== coast 1e4 (control):"; python3 "$here/slopes.py" "$here/logs/coast-1e4.log"
echo "== burn 3e4:"; python3 "$here/slopes.py" "$here/logs/burn-3e4.log"
echo "== one-wall-hour marks (360k game-s):"; grep -m1 'gs=360' "$here/logs/burn-1e4.log"; grep -m1 'gs=360' "$here/logs/burn-3e4.log" || grep 'gs=33[0-9][0-9][0-9][0-9] ' "$here/logs/burn-3e4.log" | tail -1
uptime
