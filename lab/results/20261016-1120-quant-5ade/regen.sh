#!/bin/sh
# Regenenerates every number in dossier.md from the shipped tree plus work/patch.diff (the walk
# counters, the two exact tau carries behind ES_TAU_CARRY, and examples/waveprobe.rs), in < 15 min
# on the lab's Linux box. Order: build once, then the four waveprobe arms and the frame_digest A/B.
set -e
cd "$(dirname "$0")/../../.."   # the repo root (the runner applies work/patch.diff before this)
OUT="$(dirname "$0")/raw"
mkdir -p "$OUT"
echo "== build (prof on) =="
cargo build --release --features prof -p emergent-universe --example waveprobe --example frame_digest 2>&1 | tail -1
echo "== wave 1 (the belt's first kicks, 13-15 ks) =="
cargo run --release --features prof -p emergent-universe --example waveprobe -- 100000 13000 15000 > "$OUT/w1_off.txt" 2>&1
ES_TAU_CARRY=1 cargo run --release --features prof -p emergent-universe --example waveprobe -- 100000 13000 15000 > "$OUT/w1_on.txt" 2>&1
echo "== waves 2-3 (steady state, 70-150 ks) =="
cargo run --release --features prof -p emergent-universe --example waveprobe -- 100000 70000 150000 > "$OUT/w23_off.txt" 2>&1
ES_TAU_CARRY=1 cargo run --release --features prof -p emergent-universe --example waveprobe -- 100000 70000 150000 > "$OUT/w23_on.txt" 2>&1
echo "== the plane's flights, both arms (bit-identity beyond the belt) =="
cargo run --release -p emergent-universe --example frame_digest -- 14 > "$OUT/fd_off.txt" 2>&1
ES_TAU_CARRY=1 cargo run --release -p emergent-universe --example frame_digest -- 14 > "$OUT/fd_on.txt" 2>&1
echo "== digests =="
for f in w1 w23; do
  a=$(grep '^wave:' "$OUT/${f}_off.txt" | awk '{print $NF}')
  b=$(grep '^wave:' "$OUT/${f}_on.txt" | awk '{print $NF}')
  echo "$f digest_off=$a digest_on=$b same=$([ "$a" = "$b" ] && echo yes || echo NO)"
done
grep -E 'seed|every flight' "$OUT/fd_off.txt" | sed 's/  \[.*$//' > "$OUT/fd_off_stripped.txt"
grep -E 'seed|every flight' "$OUT/fd_on.txt"  | sed 's/  \[.*$//' > "$OUT/fd_on_stripped.txt"
if diff "$OUT/fd_off_stripped.txt" "$OUT/fd_on_stripped.txt" > /dev/null; then
  echo "frame_digest: identical across arms"
else
  echo "frame_digest: DIGESTS DIVERGE"
fi
diff "$OUT/fd_pristine_main.txt" "$OUT/fd_off_stripped.txt" > /dev/null \
  && echo "off arm == pristine main (bit for bit)" || echo "off arm vs pristine main: check raw/" 
echo "== the table =="
for f in w1 w23; do
  echo "--- $f off ---"; grep -E "waveprobe:|wave:|sources:|item: kick|fit:|walk:|rebind|apply|position walk|us_per" "$OUT/${f}_off.txt"
  echo "--- $f on ---";  grep -E "waveprobe:|wave:|sources:|item: kick|fit:|walk:|rebind|apply|position walk|us_per" "$OUT/${f}_on.txt"
done
