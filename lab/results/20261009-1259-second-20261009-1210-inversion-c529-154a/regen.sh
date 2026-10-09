#!/bin/sh
# Regenerate every number in this run's record from the shipped patches (clean tree).
# Each command <= 60 s (Linux x86, 8 vCPU, < 200 MB). CARGO_TARGET_DIR may be shared.
set -e
R=$(dirname "$0")/work
export CARGO_TARGET_DIR=${CARGO_TARGET_DIR:-/home/glmlab/lab-target-1}
cd "$(git rev-parse --show-toplevel)"

# 1. the first author's probe (from lab/results/20261009-1210-inversion-c529/work/patch.diff,
#    copied here) and this run's probe
git apply --reject "$R/patch.diff"
git apply --reject "$R/patch2.diff"
cargo build --release -p emergent-encounters --bin inversion --bin inversion2   # ~5 s

# 2. reproduction of the first author's record (bit-identical mod wall-clock)
$CARGO_TARGET_DIR/release/inversion control  > "$R/repro-control.jsonl"   # 3 s
$CARGO_TARGET_DIR/release/inversion heldout  > "$R/repro-heldout.jsonl"   # ~45 s
diff <(sed 's/"secs":[0-9.]*//' "$R/repro-control.jsonl") <(sed 's/"secs":[0-9.]*//' "$R/control.jsonl")
diff <(sed 's/"secs":[0-9.]*//' "$R/repro-heldout.jsonl")  <(sed 's/"secs":[0-9.]*//' "$R/heldout.jsonl")

# 3. the decisive experiment: the watch as specified (rebuild-on-overtakes) + the gold's
#    distance-rank oracle, per event, on controls, held-out scenes and the fleet family
$CARGO_TARGET_DIR/release/inversion2 a > "$R/refresh-a.jsonl"   # ~24 s
$CARGO_TARGET_DIR/release/inversion2 b > "$R/refresh-b.jsonl"   # ~18 s

# 4. independent audits (pure Python: Kepler solver; generator + rank reimplementation)
cd "$R"
python3 audit2_check.py > audit2-check.txt   # ~5 s: pair 89/107 physics (contact real, recurs)
python3 audit3_check.py > audit3-check.txt   # ~1 s: population rank recount vs Rust, 6 events
