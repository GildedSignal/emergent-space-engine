#!/bin/sh
# Regenenerates every number in dossier.md from shipped code + work/patch.diff (already
# applied by the runner before this runs). ~4 minutes on the shared Linux box.
set -e
cd "$(dirname "$0")/../../.."   # repo root
OUT=lab/results/20261017-1447-system-6671
mkdir -p "$OUT"

echo "== build (patched: census module + Linux nladder link) =="
(cd crates/universe && cargo build --release --example nladder --example ladder_digest) > "$OUT/regen-build.log" 2>&1 || { tail -5 "$OUT/regen-build.log"; exit 1; }

echo "== digest control: census OFF vs ON (must be identical) =="
(cd crates/universe && cargo run --release --example ladder_digest -- "N=3000 coast through" 2>&1 | grep "N=3000") > "$OUT/digest-off.txt"
(cd crates/universe && ES_CENSUS=1 cargo run --release --example ladder_digest -- "N=3000 coast through" 2>&1 | grep "N=3000") > "$OUT/digest-on.txt"
diff "$OUT/digest-off.txt" "$OUT/digest-on.txt" && echo "digest identical"

echo "== census flight: nladder 10000 coast 60 600 =="
(cd crates/universe && ES_CENSUS=1 cargo run --release --example nladder -- 10000 coast 60 600 2>&1 | grep -E "^census|^game|^ladder:|^rung") > "$OUT/census-n10000.txt"
cat "$OUT/census-n10000.txt"

echo "== held-out arm for the checker (not in the dossier): N=30000 =="
(cd crates/universe && ES_CENSUS=1 cargo run --release --example nladder -- 30000 coast 60 600 2>&1 | grep -E "^census|^game|^ladder:|^rung") > "$OUT/census-n30000.txt" || true
grep -E "L1274184702 j" "$OUT/census-n30000.txt" || true
