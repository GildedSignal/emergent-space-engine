#!/bin/sh
# Regen for 20261020-2158-m2-meso-motion-a877: the family-certificate probe.
# Applies work/patch.diff (adds crates/universe/examples/family.rs), builds, runs the three
# instruments, and restores the tree. Every number in dossier.md regenerates from this.
# Total wall on the lab box (8 vCPU): ~40 s build + ~15 s run (well under 15 min).
set -e
cd "$(dirname "$0")/../../.."   # the repo root
git apply --check lab/results/20261020-2158-m2-meso-motion-a877/work/patch.diff 2>/dev/null && git apply lab/results/20261020-2158-m2-meso-motion-a877/work/patch.diff || echo "patch already applied"
cargo build --release -p emergent-universe --example family
OUT=lab/results/20261020-2158-m2-meso-motion-a877/work
cargo run --release -p emergent-universe --example family -- census   > $OUT/census.txt 2>&1
cargo run --release -p emergent-universe --example family -- growth   > $OUT/growth.txt 2>&1
cargo run --release -p emergent-universe --example family -- split    > $OUT/split.txt 2>&1
echo "--- regen done: $OUT/{census,growth,split}.txt ---"
grep -c . $OUT/census.txt $OUT/growth.txt $OUT/split.txt
