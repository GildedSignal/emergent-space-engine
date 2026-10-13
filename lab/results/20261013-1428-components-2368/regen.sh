#!/bin/bash
# Regenerates every dossier number from the shipped tree + work/patch.diff (already applied
# by the runner). Linux x86 shared box: expect ~5% run-to-run drift; the ratios are stable.
set -e
cd "$(dirname "$0")/../../.."   # repo root
S=crates/space/src
TMP=$(mktemp -d)
echo "== patched tree (work/patch.diff applied) =="
(cd crates/space && cargo run --release --example cos_bench 2>/dev/null | grep -E "bit-identity|rep |grid|shape digest|compile best")
(cd crates/space && cargo test --release 2>&1 | grep -cE "test result: ok")
cargo run --release -p emergent-universe --example tail 20 1 1 48 2>/dev/null | grep digest
cargo run --release -p emergent-universe --example cost_split 2>/dev/null | head -1
echo "== pristine control (A/B/A): revert the three law files =="
cp $S/orbit.rs $S/lib.rs $S/num.rs $TMP/
git checkout -- $S/orbit.rs $S/lib.rs $S/num.rs
cargo run --release -p emergent-universe --example tail 20 1 1 48 2>/dev/null | grep digest
cargo run --release -p emergent-universe --example cost_split 2>/dev/null | head -1
# The cos_bench example needs `pub mod num`/`pub mod tables` (in the patch), so time the
# pristine compile grid through the same example with only the visibility lines restored.
sed -i 's/^mod num;$/pub mod num;/; s/^mod tables;$/pub mod tables;/' $S/lib.rs
(cd crates/space && cargo run --release --example cos_bench 2>/dev/null | grep -E "bit-identity|shape digest|compile best")
cp $TMP/orbit.rs $TMP/lib.rs $TMP/num.rs $S/
echo "== patch restored; final identity check =="
(cd crates/space && cargo run --release --example cos_bench 2>/dev/null | grep -E "shape digest|compile best")
