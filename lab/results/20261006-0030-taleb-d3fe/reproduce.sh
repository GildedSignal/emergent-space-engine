#!/bin/bash
# Reproduces the dossier's numbers. Each command <= 60 s on this 8-vCPU Linux box.
# Build once (48 s cold):  cargo build --release -p xtask
# The binary lands in $CARGO_TARGET_DIR/release/xtask (this host: /home/glmlab/lab-target-3/release/xtask).
set -u
X=${XTASK_BIN:-/home/glmlab/lab-target-3/release/xtask}
run() { # members rtf seed
  timeout 55 /usr/bin/time -v "$X" universe --bench --seed "$3" --seconds 8 --unpaced --threads 1 --members "$1" --rtf "$2" \
    >/tmp/r.json 2>/tmp/tv
  rss=$(grep 'Maximum resident' /tmp/tv | grep -o '[0-9]*')
  echo "members=$1 rtf=$2 seed=$3 rss_MB=$(( ${rss:-0} / 1024 )) $(jq -r .stats /tmp/r.json 2>/dev/null | grep -o 'kicks: [0-9]*\|leavers: [0-9]*\|dissolved: [0-9]*' | tr '\n' ' ')"
}
echo "== the law: memory grows with game time while every event counter stays flat (seed 3, members 48)"
for r in 10000 20000 40000 80000; do run 48 "$r" 3; done
echo "== control: a battle that dissolves is flat (members 16)"
run 16 40000 3
echo "== fat tail across seeds at the same config (members 48, rtf 80000)"
for s in 3 4 5; do run 48 80000 "$s"; done
echo "== determinism across processes and threads (must print 3 equal lines then a different one)"
for t in 1 1 4; do "$X" universe --bench --seed 3 --seconds 5 --unpaced --threads "$t" 2>/dev/null | jq -r .digest; done
"$X" universe --bench --seed 4 --seconds 5 --unpaced 2>/dev/null | jq -r .digest
echo "== the engine's own memory instrument at the ruin point (bytes_per_body ~ 9 KB x ~74 bodies)"
"$X" universe --bench --seed 3 --seconds 8 --unpaced --members 48 --rtf 80000 2>/dev/null | jq '[.bytes_per_body, .bodies]'
