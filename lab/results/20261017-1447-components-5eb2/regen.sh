#!/bin/sh
# Regenerates every number in dossier.md for run 20261017-1447-components-5eb2.
# Total wall: ~6 min (the digest parity check is the long half; every step < 60 s where possible).
set -e
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261017-1447-components-5eb2

# Idempotent start: heal whatever tree state regen inherits (a clean checkout, or the
# author's still-applied edits) back to pristine HEAD, so step 0 measures shipped code
# and step 1's git apply always lands on a clean base.
git checkout -- crates/ || true
rm -f crates/space/examples/kickfloor.rs crates/universe/examples/refit_probe.rs

echo "== 0. pristine digests (shipped tree, no patch) =="
cargo run --release -p emergent-universe --example ladder_digest -- "N=3000" 2>&1 | grep "^N=3000" > /tmp/pristine.txt || true

echo "== 1. apply instrument (print-only: nested prof stages + (doll,tick) census) =="
git apply $R/work/patch.diff
cp $R/work/kickfloor.rs crates/space/examples/
cp $R/work/refit_probe.rs crates/universe/examples/

echo "== 2. parity: patched tree, prof OFF, must be bit-identical =="
cargo run --release -p emergent-universe --example ladder_digest -- "N=3000" 2>&1 | grep "^N=3000" > /tmp/patched.txt
sed 's/ *\[[0-9.]* s\]$//' /tmp/pristine.txt > /tmp/pristine_d.txt
sed 's/ *\[[0-9.]* s\]$//' /tmp/patched.txt > /tmp/patched_d.txt
diff /tmp/pristine_d.txt /tmp/patched_d.txt && echo "PARITY: bit-identical (digests and counts; wall-time tails ignored)"

echo "== 3. the decisive flights (kick decomposition + census + real-state bind) =="
cargo run --release -p emergent-universe --features prof --example refit_probe -- 30000 30 600 2>&1 | tee $R/main_arm.txt | grep -E "item: kick \(clock\)|fit: bind|readout: one|secondaries: source|secondaries census|bind \(Re|game |events "
echo "-- held-out arm (N=1e4, rtf 1800; deeper into the first crest) --"
cargo run --release -p emergent-universe --features prof --example refit_probe -- 10000 20 1800 2>&1 | tee $R/heldout_arm.txt | grep -E "item: kick \(clock\)|fit: bind|readout: one|secondaries: source|secondaries census|bind \(Re|game |events "

echo "== 4. the compile bench: Orbit::compile on belt/strong keys + division micro =="
cargo run --release -p emergent-space --example kickfloor 2>&1 | tee $R/kickfloor.txt | grep -E "micro|class"

echo "== 5. restore the tree =="
git checkout -- crates/ && rm -f crates/space/examples/kickfloor.rs crates/universe/examples/refit_probe.rs
echo "done"
