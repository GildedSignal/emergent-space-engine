#!/usr/bin/env bash
# Regenerates every number in dossier.md for run 20261021-0829-inversion-3c40.
# work/patch.diff (the nladder Linux memory port + guard + window telemetry) is applied
# by the runner before this runs. ~10-13 min on the 8-vCPU lab box.
set -u
cd "$(dirname "$0")/../../.." || exit 1   # repo root
R=lab/results/20261021-0829-inversion-3c40/raw
mkdir -p "$R"
NL=${NL:-/home/glmlab/lab-target-2/release/examples/nladder}

cargo build --release -p emergent-universe --example nladder || exit 1

state() { { echo "=== $1 $(date -u +%H:%M:%S) $(uptime)"; free -m | head -2; } >> "$R/state.txt"; }

# The certificate at the rung class (25 s page, shipped gate horizon is 20 s)
state gates
"$NL" 700000 coast 25 100 12 > "$R/gate-7e5-coast-25s.log" 2>&1
"$NL" 700000 burn  25 100 12 > "$R/gate-7e5-burn-25s.log"  2>&1

# The decisive arms (past every prior horizon at this rung class)
state burn-arms
ES_NL_GUARD_MB=1900 ES_NL_MAX_S=600 "$NL" 700000 burn 600 100 12 > "$R/burn-7e5-guard1900.log" 2>&1 &
ES_NL_GUARD_MB=1900 ES_NL_MAX_S=600 "$NL" 500000 burn 600 100 12 > "$R/burn-5e5-guard1900.log" 2>&1 &
ES_NL_GUARD_MB=1900 ES_NL_MAX_S=600 "$NL" 100000 burn 600 100 12 > "$R/burn-1e5-guard1900.log" 2>&1 &
wait

# The wave arm (coast: no ratchet; through >= 2 comb eras)
state wave
ES_NL_GUARD_MB=1900 ES_NL_MAX_S=900 "$NL" 700000 coast 700 100 12 > "$R/coast-7e5-2eras.log" 2>&1
state done

echo "--- gate coast ---";  grep -hE "rung|frames after|memory:|ladder:" "$R/gate-7e5-coast-25s.log"
echo "--- gate burn ---";   grep -hE "rung|frames after|memory:|ladder:" "$R/gate-7e5-burn-25s.log"
echo "--- burn 7e5 ---";    grep -hE "nl:|frames after|ladder:" "$R/burn-7e5-guard1900.log"
echo "--- burn 5e5 ---";    grep -hE "nl:|frames after|ladder:" "$R/burn-5e5-guard1900.log"
echo "--- burn 1e5 ---";    grep -hE "nl:|frames after|ladder:" "$R/burn-1e5-guard1900.log"
echo "--- coast 7e5 eras ---"; grep -hE "nl:|frames after|ladder:" "$R/coast-7e5-2eras.log"
