#!/bin/sh
# Regen for 20261017-0428-spacex-d959: every dossier number from shipped code + work/patch.diff.
# ~5 min on 8 vCPU. Steps: apply the instrument, readwave at 3 N, nladder flight totals,
# and the pristine-vs-patched ladder_digest identity check (strip wall-time annotations).
set -e
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261017-0428-spacex-d959
git apply --allow-empty "$R/work/patch.diff" 2>/dev/null || true   # idempotent if already applied
cp "$R/work/readwave.rs" crates/universe/examples/readwave.rs
cargo build --release -p emergent-universe --example readwave --example nladder --example ladder_digest

echo "== readwave (the wave's read stream, settled to 14,600 game-s) =="
for n in 10000 100000 300000; do
  timeout 55 cargo run --release -p emergent-universe --example readwave -- "$n" 14600 | grep -E "^readwave|^readstat" | head -9
done

echo "== nladder 10^5 (flight-only totals; census printed before the one-shot view gather) =="
for f in coast burn; do
  timeout 55 cargo run --release -p emergent-universe --example nladder -- 100000 "$f" 20 2>/dev/null | grep -E "readstat: flight"
done

echo "== digest identity: patched vs pristine (strip wall-time annotations, compare) =="
timeout 120 cargo run --release -p emergent-universe --example ladder_digest > "$R/work/digest_patched_regen.txt" 2>&1 || true
cp crates/universe/src/bind.rs "$R/work/bind_instrumented.rs"
git checkout -- crates/universe/src/bind.rs crates/universe/src/ctx.rs
cargo build --release -p emergent-universe --example ladder_digest
timeout 120 cargo run --release -p emergent-universe --example ladder_digest > "$R/work/digest_pristine_regen.txt" 2>&1 || true
cp "$R/work/bind_instrumented.rs" crates/universe/src/bind.rs
cp "$R/work/ctx.rs" crates/universe/src/ctx.rs
sed -E 's/ *\[[0-9.]+ s\]//' "$R/work/digest_pristine_regen.txt" | md5sum
sed -E 's/ *\[[0-9.]+ s\]//' "$R/work/digest_patched_regen.txt" | md5sum
echo "(the two md5 sums must be equal: the instrument is print-only)"
