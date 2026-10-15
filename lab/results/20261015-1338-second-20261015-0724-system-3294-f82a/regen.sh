#!/bin/sh
# Regen: every number in dossier.md, from the shipped tree + work/patch.diff (already applied).
# Builds the census+stagger instrument and flies: the four 10^4 arms (coast/burn x baseline/stagger,
# full 55 s horizon, fire trains), the canonical-digest protocol flights (8 s flight, then a forward
# settle to the cut: a digest after over-flying its cut is NOT canonical), and the 10^5 coast pair.
# Then the wave and dimensionless analysis. ~8 min on an idle 8-vCPU host, < 1 GB peak.
set -e
cd "$(dirname "$0")/../../.."   # the repo root
R=lab/results/20261015-1338-second-20261015-0724-system-3294-f82a/raw
mkdir -p "$R/dg"

cargo build --release -p emergent-universe --example nladder
BIN="${CARGO_TARGET_DIR:-/home/glmlab/lab-target-0}/release/examples/nladder"
[ -x "$BIN" ] || BIN=/home/glmlab/lab-target-0/release/examples/nladder

# D1: the four 10^4 arms, full horizon (55 s wall, rtf 1500 -> ~80 k game-s: 3 grid intervals).
CENSUS_TRAIN="$R/train_1e4_coast_base.txt" "$BIN" 10000 coast 55 1500 > "$R/n1e4_coast_base.txt" 2>&1
CENSUS_TRAIN="$R/train_1e4_coast_stag.txt" STAGGER_GENESIS=1 "$BIN" 10000 coast 55 1500 > "$R/n1e4_coast_stag.txt" 2>&1
CENSUS_TRAIN="$R/train_1e4_burn_base.txt"  "$BIN" 10000 burn  55 1500 > "$R/n1e4_burn_base.txt"  2>&1
CENSUS_TRAIN="$R/train_1e4_burn_stag.txt"  STAGGER_GENESIS=1 "$BIN" 10000 burn  55 1500 > "$R/n1e4_burn_stag.txt"  2>&1
# D2: the canonical digests: an 8 s flight never reaches the cut, then settle() moves *forward* to it
# (nothing resolved past the cut: the canonical-cut contract). Coast base x3, coast stag x2, burn once each.
DIGEST_AT=76000 "$BIN" 10000 coast 8 1500 > "$R/dg/cb1.txt" 2>&1
DIGEST_AT=76000 "$BIN" 10000 coast 8 1500 > "$R/dg/cb2.txt" 2>&1
DIGEST_AT=76000 "$BIN" 10000 coast 8 1500 > "$R/dg/cb3.txt" 2>&1
DIGEST_AT=76000 STAGGER_GENESIS=1 "$BIN" 10000 coast 8 1500 > "$R/dg/cs1.txt" 2>&1
DIGEST_AT=76000 STAGGER_GENESIS=1 "$BIN" 10000 coast 8 1500 > "$R/dg/cs2.txt" 2>&1
DIGEST_AT=76000 "$BIN" 10000 burn 8 1500 > "$R/dg/bb1.txt" 2>&1
DIGEST_AT=76000 "$BIN" 10000 burn 8 1500 > "$R/dg/bb2.txt" 2>&1
DIGEST_AT=76000 STAGGER_GENESIS=1 "$BIN" 10000 burn 8 1500 > "$R/dg/bs1.txt" 2>&1
# D3: the 10^5 coast pair (one wave in the horizon; frame tail at 10x bodies).
CENSUS_TRAIN="$R/train_1e5_coast_base.txt" "$BIN" 100000 coast 55 600 > "$R/n1e5_coast_base.txt" 2>&1
CENSUS_TRAIN="$R/train_1e5_coast_stag.txt" STAGGER_GENESIS=1 "$BIN" 100000 coast 55 600 > "$R/n1e5_coast_stag.txt" 2>&1

echo "== census and frame tails (all arms)"
for a in 1e4_coast_base 1e4_coast_stag 1e4_burn_base 1e4_burn_stag 1e5_coast_base 1e5_coast_stag; do
  echo "-- $a"
  grep -E "ladder:" "$R/n$a.txt" | cut -c1-400
  grep -oE "ship/root kicks=[0-9]+ fired=[0-9]+ fire_rate=[0-9.e-]+ dv_log2=\[[^]]*\]" "$R/n$a.txt"
  grep -oE "catalogue [0-9]+ entries" "$R/n$a.txt"
done
echo "== digests (canonical cut 76000 game-s from tick 0)"
grep -h "digest at" "$R"/dg/*.txt
echo "== waves (baseline vs staggered)"
python3 lab/results/20261015-1338-second-20261015-0724-system-3294-f82a/waves.py \
  "$R/train_1e4_coast_base.txt" "$R/train_1e4_coast_stag.txt" \
  "$R/train_1e4_burn_base.txt" "$R/train_1e4_burn_stag.txt" \
  "$R/train_1e5_coast_base.txt" "$R/train_1e5_coast_stag.txt" | tee "$R/waves.txt"
echo "== dimensionless impulses"
python3 lab/results/20261015-1338-second-20261015-0724-system-3294-f82a/dim.py \
  "$R/n1e4_coast_base.txt" "$R/n1e4_coast_stag.txt" "$R/n1e5_coast_base.txt" | tee "$R/dim.txt"
echo "machine state:"; uptime
