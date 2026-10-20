#!/bin/sh
# Regenerates every number in dossier.md from a clean tree plus this run's work/patch.diff
# (the fibers.rs example, print-only; no shipped behaviour changed). ~1 minute of compute.
set -e
cd "$(dirname "$0")/../../.." || exit 1
git apply --check lab/results/20261020-2306-m2-macro-structure-1bcc/work/patch.diff 2>/dev/null && git apply lab/results/20261020-2306-m2-macro-structure-1bcc/work/patch.diff || true
R=lab/results/20261020-2306-m2-macro-structure-1bcc
cargo build --release -p emergent-universe --example fibers
# The birth census (the fibration's base size F at each key width), seed 1 (shipped) and held-out seed 2:
cargo run --release -p emergent-universe --example fibers -- draw 1000000 1 | tee $R/regen-draw-1e6-s1.txt
cargo run --release -p emergent-universe --example fibers -- draw 1000000 2 | tee $R/regen-draw-1e6-s2.txt
cargo run --release -p emergent-universe --example fibers -- draw 300000 7 | tee $R/regen-draw-3e5-s7.txt
# The flight census (base stability under real kicks; the pending-tick and stride census):
cargo run --release -p emergent-universe --example fibers -- flight 100000 20 100000 | tee $R/regen-flight-1e5.txt
echo "regen done"
