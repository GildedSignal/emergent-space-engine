#!/usr/bin/env bash
# Regen: rebuilds the patched nladder (Linux footprint stub + the ES_WAVE_PROBE print-only
# per-frame decomposition + the ES_RSS_CAP_MB flight guard) and reflies the five arms of
# the dossier. A PRIVATE target dir: the lab boxes run several runs a window and a sibling
# run's nladder build once replaced the shared target's binary mid-regen (caught by the
# probe check below; the flights then flew someone else's instrument).
# Wall: ~4-6 min build (fresh deps) + ~2.5 min flights.
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"
out=lab/results/20261019-2017-inversion-cc9d
mkdir -p "$out/out"
export CARGO_TARGET_DIR="$out/work/target"
cargo build --release -p emergent-universe --example nladder --features prof || exit 1
B="$CARGO_TARGET_DIR/release/examples/nladder"
[ -x "$B" ] || { echo "no binary"; exit 1; }
run() { local tag=$1; shift; echo "=== $tag: $* ==="; ES_WAVE_PROBE=1 ES_RSS_CAP_MB=${RSS_CAP:-0} timeout 90 "$B" "$@" > "$out/out/$tag.log" 2>&1; local rc=$?; grep -q "^wave probe" "$out/out/$tag.log" || { echo "BAD BINARY OR PROBE OFF in $tag (exit $rc)"; return 1; }; grep -E "^rung|^ladder:|flight stopped" "$out/out/$tag.log"; }
run k1e4  10000 burn 20 1000 12 || exit 1
run k5e4  50000 burn 24 1000 12 || exit 1
run k1e5  100000 burn 24 1000 12 || exit 1
RSS_CAP=1750 run k2e5 200000 burn 24 1000 12 || exit 1
run rtf600 100000 burn 26 600 12 || exit 1
echo; echo "— the worst frame of each arm, decomposed (one top-level player item, nested clock-kicks):"
for t in k1e4 k5e4 k1e5 k2e5 rtf600; do echo "[$t]"; grep -A2 "^wave probe" "$out/out/$t.log" | head -3; done
rm -rf "$CARGO_TARGET_DIR"
python3 - "$out" <<'PY'
import re, sys, pathlib
rows = []
for t, k in [("k1e4", 1e4), ("k5e4", 5e4), ("k1e5", 1e5), ("k2e5", 2e5), ("rtf600", 1e5)]:
    log = (pathlib.Path(sys.argv[1]) / "out" / f"{t}.log").read_text()
    lad = re.search(r"ladder: .*?max_ms=([\d.]+)", log)
    fr = re.search(r"^  f (\d+)\s+([\d.]+) ms items (\d+) kicks (\d+)", log, re.M)
    if lad and fr:
        ms, kicks = float(lad.group(1)), int(fr.group(4))
        rows.append((t, int(k), ms, kicks, ms / kicks if kicks else 0))
print(f"{'arm':<7}{'K':>8}{'max_ms':>10}{'gulp kicks':>12}{'us/kick':>9}")
for t, k, ms, kicks, upk in rows:
    print(f"{t:<7}{k:>8}{ms:>10.1f}{kicks:>12}{upk*1000:>9.1f}")
lin = [r for r in rows if r[0] in ("k1e5", "k2e5")]
if len(lin) == 2:
    c_us = lin[1][2] * 1000.0 / lin[1][1]
    print(f"\nsaturated law: max_ms ≈ {c_us:.1f} µs × K  (10⁵ check {lin[0][1]*c_us/1000:.2f} s vs {lin[0][2]/1000:.2f} s measured; 10⁶ → {c_us:.0f} s; 10⁹ → {c_us*1e9/1e6/60/60:.1f} h a frame)")
PY
