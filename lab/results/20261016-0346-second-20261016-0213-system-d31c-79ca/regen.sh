#!/bin/bash
# Regenerates every dossier number from the patch (applied by the runner before this runs).
# Budget: ~9-11 min on the lab box (build ~12 s, grid ~75 s = 29 flights, three suite runs are the
# tail; the planets-only and constants-only configs are archived in out/suites.log, run in-session).
# The repo root is three levels up from this file (lab/results/<run>/regen.sh); all builds go to
# /home/glmlab/lab-target-3 because grid.sh flies that exact binary.
set -e
export CARGO_TARGET_DIR=/home/glmlab/lab-target-3
RUN_DIR="$(cd "$(dirname "$0")" && pwd)"   # absolute, so invocation cwd never matters
cd "$RUN_DIR/../../.."                     # the repo root
cargo build --release -p emergent-universe --example birth_rail
cd "$RUN_DIR"
mkdir -p out
bash grid.sh > out/grid_regen.log 2>&1
echo "--- digests (must pair across all arms at each N,seed) ---"
python3 - <<'EOF'
import re
cells = {}
for line in open('out/grid_regen.log'):
    m = re.match(r'=== N=(\d+) seed=(\d+) arm=(\w+)', line)
    if m: cur = m.groups()
    m = re.search(r'digest=([0-9a-f]{64})', line)
    if m and cur: cells.setdefault((cur[0], cur[1]), {})[cur[2]] = m.group(1)
bad = sum(1 for a in cells.values() if len(set(a.values())) != 1)
for k, a in sorted(cells.items()): print(k, {x: d[:8] for x, d in a.items()})
print('cells:', len(cells), 'digest mismatches across arms:', bad)
assert bad == 0 and len(cells) == 7
EOF
echo "--- pass per body, all arms (off/on/state/full) ---"
grep -E "===|pass_us_per" out/grid_regen.log | paste - - | sed 's/.*arm=/arm=/; s/ ===.*pass_us_per=/ pass=/; s/ replan.*readout_calls_per=/ readout_calls=/; s/ const_hits_per=/ const_hits=/; s/ secondaries.*//'
cd "$RUN_DIR/../../.."                     # the repo root
for env in "off:" "state:ES_STATE_ONCE=1" "full:ES_PLANETS_AT_T=1 ES_STATE_ONCE=1 ES_CONSTANTS_ONCE=1"; do
  name=${env%%:*}; vars=${env#*:}
  env $vars CARGO_TARGET_DIR=/home/glmlab/lab-target-3 cargo test --release -p emergent-universe --tests 2>&1 | grep -E "test result" | awk -v n="$name" '{p+=$4; f+=$6} END {print "suite "n": passed="p" failed="f}'
done
