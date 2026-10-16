#!/bin/sh
# Regenerates every dossier number from shipped code + this run's patch (work/patch.diff).
# < 5 min total on the lab's Linux machine. Every process stays under 500 MB.
set -e
cd "$(dirname "$0")"
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo ../../..)"
cd "$ROOT"
# apply the patch if the tree is clean (the runner may have applied it already)
if [ ! -f crates/universe/examples/memwalk.rs ]; then
  git apply lab/results/20261016-2138-inversion-58be/work/patch.diff
fi
cargo build --release -p emergent-universe --example memwalk --example nladder
RUN="cargo run --release -q -p emergent-universe --example memwalk --"
OUT=lab/results/20261016-2138-inversion-58be/raw
mkdir -p "$OUT"
$RUN 100000 coast 100000 100 12 48 1  > "$OUT/a_n1e5_gs100k.txt" 2>&1
$RUN 10000  coast 100000 100 12 48 1  > "$OUT/b_n1e4_gs100k.txt" 2>&1
$RUN 1000   coast  40000 100 12 400 1 > "$OUT/c_battle400_gs40k.txt" 2>&1
$RUN 0      coast 100000 100 12 48 1  > "$OUT/d_n0_gs100k.txt" 2>&1
$RUN 100000 coast  60000 100 12 48 2  > "$OUT/e_n1e5_seed2_gs60k.txt" 2>&1
cd lab/results/20261016-2138-inversion-58be
python3 analyze.py | tee analysis.txt
