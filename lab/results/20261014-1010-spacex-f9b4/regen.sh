#!/usr/bin/env bash
# Regen 20261014-1010: every dossier number from shipped code + work/patch.diff.
# Total wall: ~2-3 minutes on the lab Linux box.
set -euo pipefail
cd "$(dirname "$0")"
ROOT=../../..
cd "$ROOT"
[ -s lab/results/20261014-1010-spacex-f9b4/work/patch.diff ] && git apply \
    lab/results/20261014-1010-spacex-f9b4/work/patch.diff || true
python3 -c "import mpmath" 2>/dev/null || pip install --quiet mpmath
cargo build --release -p emergent-space --example thin_edge
T=$(ls /home/glmlab/lab-target-2/release/examples/thin_edge 2>/dev/null || \
   ls target/release/examples/thin_edge)
cd lab/results/20261014-1010-spacex-f9b4
for set in grid heldout; do
    for cfg in ladder a:4 b:4 c:4 1:4 2:4; do
        if [ "$cfg" = ladder ]; then
            $T $set > ${set}_ladder.csv
        else
            ES_THIN_EDGE=$cfg $T $set > ${set}_$(echo $cfg | tr ':' '_').csv
        fi
    done
done
$T dev > dev_ladder.csv
ES_THIN_EDGE=a:4 $T dev > dev_a_4.csv
echo "# dev tuning set (predictions.md): panels ladder vs a:4 at p=20:"
paste -d' ' dev_ladder.csv dev_a_4.csv
ES_THIN_EDGE=c:8 "$T" heldout > heldout_c_8.csv
python3 ref.py grid_*.csv heldout_*.csv > verdicts_all.csv
echo "# summary (from ref.py):"; tail -8 verdicts_all.csv
echo; echo "# bands and passages:"; python3 summarize.py
echo; echo "# the c:8 placement-immunity control at (6.7, 0.3):"
grep "^6.7,0.3" verdicts_all.csv
echo; echo "# identity control: the shipped-ladder arm (env unset) through the probe's"
echo "# refactor must keep the crate's own suite green (env unset = the None arm):"
cd "$ROOT"
cargo test --release -p emergent-space 2>&1 | tail -3
