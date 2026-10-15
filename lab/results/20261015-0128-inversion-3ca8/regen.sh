#!/bin/sh
# Regen for 20261015-0128-inversion-3ca8: every dossier number, from shipped code + work/patch.diff.
# The runner applies work/patch.diff (adds crates/lattice/examples/shadow.rs) before this runs.
set -e
cd "$(dirname "$0")/../../.."   # repo root
B="cargo run --release -p emergent-lattice --example shadow --"
OUT="$(dirname "$0")/out"
mkdir -p "$OUT"

# Single-contact continuum-limit table (engine vs analytic, Q 2^16/18/20, light at rest / 0.97 / 0.999)
$B micro > "$OUT/micro.jsonl"

# Controls
$B neg engine 20 20 1   > "$OUT/neg_engine_q20_s1.jsonl"
$B neg float 20 20 1    > "$OUT/neg_float_q20_s1.jsonl"
$B pos engine 20 20 1   > "$OUT/pos_engine_q20_s1.jsonl"
$B pos float 20 20 1    > "$OUT/pos_float_q20_s1.jsonl"

# Decisive arm: pump, 3 seeds, engine vs float (continuum twin)
for s in 1 2 3; do
  $B pump engine 20 20 $s > "$OUT/pump_engine_q20_s$s.jsonl"
  $B pump float  20 20 $s > "$OUT/pump_float_q20_s$s.jsonl"
done

# Q-independence arms
$B pump engine 16 20 1  > "$OUT/pump_engine_q16_s1.jsonl"
$B pump engine 18 20 1  > "$OUT/pump_engine_q18_s1.jsonl"

# State-rounding discriminator (twin + 1/Q grid rounding, exact response)
$B pump grid 20 20 1    > "$OUT/pump_grid_q20_s1.jsonl"
$B pump grid 16 20 1    > "$OUT/pump_grid_q16_s1.jsonl"

cat "$OUT"/*.jsonl
echo "regen: $(ls "$OUT" | wc -l) result files in $OUT"
