#!/usr/bin/env bash
# Regenerates every dossier number from shipped code + work/patch.diff (< 15 min).
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261017-1240-spacex-9c67
T=${CARGO_TARGET_DIR:-target}/release
mkdir -p $R/work /tmp/pos9c67
PB=/tmp/pos9c67

echo "== build pristine =="
git stash -q || true          # regen runs on a pristine tree + patch; stash is a no-op there
git checkout -q -- crates/ || true
cargo build --release -p xtask 2>&1 | tail -1
cargo build --release -p emergent-universe --example cost_split 2>&1 | tail -1
cp $T/xtask $PB/xtask-pristine; cp $T/examples/cost_split $PB/cost_split-pristine

echo "== apply patch, build patched =="
git apply $R/work/patch.diff
cargo build --release -p xtask 2>&1 | tail -1
cargo build --release -p emergent-universe --example cost_split 2>&1 | tail -1
cp $T/xtask $PB/xtask-patched; cp $T/examples/cost_split $PB/cost_split-patched

echo "== identity + coverage (verify mode) =="
ES_POS_VERIFY=1 $PB/cost_split-patched | tee $R/work/regen-cost-split.txt

echo "== digest identity, seeds 1 and 7 =="
for s in 1 7; do
  $PB/xtask-pristine universe --kick-bench --seconds 5 --seed $s > $R/work/regen-kick-pristine-s$s.json
  ES_POS_VERIFY=1 $PB/xtask-patched  universe --kick-bench --seconds 5 --seed $s > $R/work/regen-kick-patched-s$s.json
done
python3 - <<'EOF'
import json
def load(p):
    t=open(p).read(); return json.loads(t[t.index('{'):])
for s in (1,7):
    a=load(f'lab/results/20261017-1240-spacex-9c67/work/regen-kick-pristine-s{s}.json')
    b=load(f'lab/results/20261017-1240-spacex-9c67/work/regen-kick-patched-s{s}.json')
    print(f'seed{s}: digest', 'SAME' if a['digest']==b['digest'] else 'DIFF',
          '| replay', 'SAME' if a['replay_digest']==b['replay_digest'] else 'DIFF',
          '| med', a['kick_us']['median'], '->', b['kick_us']['median'])
EOF

echo "== interleaved timing, 3 pairs =="
for i in 1 2 3; do
  $PB/cost_split-pristine | grep "whole universe" | sed "s/^/P$i pristine /"
  $PB/cost_split-patched  | grep "whole universe" | sed "s/^/P$i patched /"
done | tee $R/work/regen-timing.txt

echo "== restore tree =="
git checkout -q -- crates/
echo "done"
