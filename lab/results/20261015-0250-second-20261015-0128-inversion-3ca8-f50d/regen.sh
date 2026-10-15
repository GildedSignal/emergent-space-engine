#!/bin/sh
# Regen for 20261015-0250-second-20261015-0128-inversion-3ca8-f50d: every dossier number,
# from shipped code + work/patch.diff (adds crates/lattice/examples/shadow2.rs; no library
# file touched). One process at a time, < 100 MB each, ~8 minutes total.
set -e
RUN="$(cd "$(dirname "$0")" && pwd)"
cd "$RUN/../../.."   # repo root
B="cargo run --release -q -p emergent-lattice --example shadow2 --"
OUT="$RUN/out"
mkdir -p "$OUT"

# Instrument validation: glancing micro table + pre-contact identity (neg, T=2^9/2^10)
$B micro > "$OUT/micro.jsonl" 2>/dev/null
for t in 9 10; do
  $B neg engine 20 $t 1 > "$OUT/pre_neg_engine_t$t.jsonl" 2>/dev/null
  $B neg exact  20 $t 1 > "$OUT/pre_neg_exact_t$t.jsonl" 2>/dev/null
done

# Controls: pos (equal masses) and neg (two-body pump, all four arms)
$B pos engine 20 20 1 > "$OUT/pos_engine_q20_s1.jsonl" 2>/dev/null
$B pos exact  20 20 1 > "$OUT/pos_exact_q20_s1.jsonl" 2>/dev/null
$B neg engine 20 20 1 > "$OUT/neg_engine_q20_s1.jsonl" 2>/dev/null
$B neg exact  20 20 1 > "$OUT/neg_exact_q20_s1.jsonl" 2>/dev/null
$B neg float  20 20 1 > "$OUT/neg_float_q20_s1.jsonl" 2>/dev/null
$B neg srskip 20 20 1 > "$OUT/neg_srskip_q20_s1.jsonl" 2>/dev/null

# Decisive arm: pump, 5 seeds, engine vs exact twin; float and srskip for the record
for s in 1 2 3 4 5; do
  $B pump engine 20 20 $s > "$OUT/pump_engine_q20_s$s.jsonl" 2>/dev/null
  $B pump exact  20 20 $s > "$OUT/pump_exact_q20_s$s.jsonl" 2>/dev/null
done
$B pump float  20 20 1 > "$OUT/pump_float_q20_s1.jsonl" 2>/dev/null
$B pump srskip 20 20 1 > "$OUT/pump_srskip_q20_s1.jsonl" 2>/dev/null
$B pump srskip 20 20 2 > "$OUT/pump_srskip_q20_s2.jsonl" 2>/dev/null

# Q-flat arms (the exact twin is Q-free; identical output at any q_log2)
$B pump engine 16 20 1 > "$OUT/pump_engine_q16_s1.jsonl" 2>/dev/null
$B pump engine 18 20 1 > "$OUT/pump_engine_q18_s1.jsonl" 2>/dev/null
$B pump exact  16 20 1 > "$OUT/pump_exact_q16_s1.jsonl" 2>/dev/null
$B pump exact  18 20 1 > "$OUT/pump_exact_q18_s1.jsonl" 2>/dev/null

# New scenes: soft (100:1, beta 0.8) and tall (128 lights, 512x8)
for s in 1 2; do
  $B soft engine 20 20 $s > "$OUT/soft_engine_q20_s$s.jsonl" 2>/dev/null
  $B soft exact  20 20 $s > "$OUT/soft_exact_q20_s$s.jsonl" 2>/dev/null
done
$B tall engine 20 20 1 > "$OUT/tall_engine_q20_s1.jsonl" 2>/dev/null
$B tall exact  20 20 1 > "$OUT/tall_exact_q20_s1.jsonl" 2>/dev/null

# Comparison table (what the dossier quotes)
python3 "$RUN/table.py" | tee "$OUT/table.txt"
echo "regen: $(ls "$OUT" | wc -l) result files in $OUT"
