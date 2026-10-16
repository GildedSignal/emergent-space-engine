#!/usr/bin/env bash
# Regenerates every number in this run's dossier (kickbench.json + the doc/code citations).
# Runtime here: ~45 s build (cold cache longer; 15-min budget) + ~1 s per bench run.
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root
OUT="$(dirname "$0")"

echo "== build (release, 2 jobs) =="
cargo build --release -p xtask -j 2

echo "== kick bench: the shipped resolver, two runs (digest must repeat) =="
"$CARGO_TARGET_DIR/release/xtask" universe --kick-bench --seconds 20 --rtf 600 > "$OUT/kickbench.json"
"$CARGO_TARGET_DIR/release/xtask" universe --kick-bench --seconds 20 --rtf 600 > "$OUT/kickbench-2nd.json"
python3 - "$OUT" <<'EOF'
import json, sys
o = sys.argv[1]
a = json.load(open(f"{o}/kickbench.json")); b = json.load(open(f"{o}/kickbench-2nd.json"))
assert a["digest"] == b["digest"] and a["memo"] == b["memo"], "bench not deterministic"
print("digest", a["digest"][:16])
print("kick_us(made)  median %.1f us  p99 %.1f us  (%d samples)" % (a["kick_us"]["median"], a["kick_us"]["p99"], a["kick_us"]["samples"]))
print("kick_us(leavers) median %.1f us  p99 %.1f us  (%d samples)" % (a["kick_us_leavers"]["median"], a["kick_us_leavers"]["p99"], a["kick_us_leavers"]["samples"]))
print("memo: %d rebinds, exact_hit_rate %.4f, quantized_hit_rate %.4f" % (a["memo"]["cycle_rebinds"], a["memo"]["exact_hit_rate"], a["memo"]["quantized_hit_rate"]))
print("vs docs/representation.md L114 '~50 ns each': %.0fx at the median" % (a["kick_us"]["median"] * 1000 / 50))
EOF

echo "== the doc's letters under attack =="
grep -n "multiply-add" docs/representation.md
grep -n "50 ns" docs/representation.md
grep -n "primary in-cell" docs/representation.md
grep -n "crosses the observer" docs/representation.md

echo "== the record inside shipped code =="
grep -n "authoritative" crates/space/ENVELOPE.md crates/space/QUADRATURE.md
grep -n "replaced the in-band" docs/law.md
grep -n "jet is retired" docs/law.md

echo "done"
