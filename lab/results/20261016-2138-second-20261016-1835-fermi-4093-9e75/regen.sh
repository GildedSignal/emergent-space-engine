#!/bin/sh
# Regen: rebuild the patched nladder, fly the four freeze arms, reprint the ledger.
# ~4 min warm / ~12 min cold on 8 vCPU. The patch (work/patch.diff: the Linux footprint()
# fallback + the additive `freeze:` print, no law touched) is applied by the runner before
# this runs; if not, it is applied here. Arms are sequential on purpose: the freeze numbers
# are timing measurements, parallel flights would contend. The burn arm flies last: it peaks
# at ~5.9 GB (the held-scan backlog) and may be killed under a 2-GB per-process cap; its
# numbers then stand on the committed flights.log.
set -e
cd "$(dirname "$0")/../../.."
if ! grep -q 'freeze: lag_frames' crates/universe/examples/nladder.rs 2>/dev/null; then
  git apply "$OLDPWD/work/patch.diff" 2>/dev/null || git apply "${0%/*}/work/patch.diff"
fi
if [ -d /home/glmlab/lab-target-9e75 ]; then
  export CARGO_TARGET_DIR=/home/glmlab/lab-target-9e75
fi
cargo build --release -p emergent-universe --example nladder 2>&1 | tail -1
B="$CARGO_TARGET_DIR/release/examples/nladder"
[ -x "$B" ] || B=target/release/examples/nladder
OUT="${0%/*}/flights.log"
: > "$OUT"
{ date; uptime; free -m | head -2; } > "${0%/*}/state.txt"
for args in "100000 coast 40 1800" "300000 coast 40 1800" "300000 coast 30 3600" "300000 burn 40 1800"; do
  echo "=== $args" >> "$OUT"
  "$B" $args >> "$OUT" 2>&1 || echo "FAILED $args" >> "$OUT"
done
{ date; uptime; } >> "${0%/*}/state.txt"
python3 "${0%/*}/ledger.py" "$OUT" | tee "${0%/*}/ledger.txt"
