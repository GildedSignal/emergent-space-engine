#!/bin/sh
# Regen for 20261017-1829-spacex-d399. Everything from shipped code + work/patch.diff.
# Total ~7 min (build ~1 min, fitbench ~25 s, ladder_digest 2x ~160 s, nladder A/B ~20 s).
set -e
cd "$(dirname "$0")/../../.."
R=lab/results/20261017-1829-spacex-d399
OUT=$R/regen-out
mkdir -p "$OUT"

echo "== baseline digests (patch applied, inert; equals pristine main = ${0##*/} premise)"
cargo run --release -p emergent-universe --example ladder_digest -- N=3000 2>&1 | grep -E "^N=|every case" | tee "$OUT/ladder_digest_inert_n3000.txt"

echo "== delete-arm digests (FIT_NODECODED=1)"
FIT_NODECODED=1 cargo run --release -p emergent-universe --example ladder_digest -- N=3000 2>&1 | grep -E "^N=|every case" | tee "$OUT/ladder_digest_delete_n3000.txt"
diff <(grep -E "^N=" "$OUT/ladder_digest_inert_n3000.txt" | cut -d'|' -f1-3) \
     <(grep -E "^N=" "$OUT/ladder_digest_delete_n3000.txt" | cut -d'|' -f1-3) \
  && echo "DIGESTS+KICKS IDENTICAL under the delete arm"

echo "== fit stage decomposition + A/B replay on flown belt inputs"
cargo run --release -p emergent-universe --example fitbench 2>&1 | tee "$OUT/fitbench_stages.txt"

echo "== wall A/B on the wave flight (rtf 1000, 20 s wall, N=3000)"
cargo build --release -p emergent-universe --features prof --example nladder
B=$(ls -t ~/lab-target-1/release/examples/nladder | head -1)
"$B" 3000 coast 20 1000 2>&1 | grep -E "frames after|fit: bind|process \(whole\)|ladder:" > "$OUT/nladder_wave_shipped.txt"
FIT_NODECODED=1 "$B" 3000 coast 20 1000 2>&1 | grep -E "frames after|fit: bind|process \(whole\)|ladder:" > "$OUT/nladder_wave_delete.txt"
echo "-- shipped"; cat "$OUT/nladder_wave_shipped.txt"
echo "-- delete"; cat "$OUT/nladder_wave_delete.txt"
echo "== done"
