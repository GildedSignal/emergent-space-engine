#!/usr/bin/env bash
# Regenerates every number in dossier.md from shipped code + this run's probe
# (work/patch.diff adds examples/wavetrain.rs and resolves the nladder wiki page).
# ~13 min on the lab box: one build, seven flights (A/B on the presented-time cut,
# A2/B2 on the canonical tick cut, C the 250 k game-s train, one smoke per protocol).
set -e
cd "$(dirname "$0")/../../.."
cargo build --release -p emergent-universe --example wavetrain
W="${CARGO_TARGET_DIR:-/home/glmlab/lab-target-2}/release/examples/wavetrain"
OUT=lab/results/20261014-2248-inversion-4af4/out
mkdir -p "$OUT"
R=lab/results/20261014-2248-inversion-4af4
$W 3000 2500 > "$OUT/smoke3e3_tick.txt"              # both protocols agree at N=3000 (digest 47fd4a85…)
$W 3000 2500 100 12 250 now > "$OUT/smoke3e3_now.txt"
$W 300000 150000 100 12 250 now > "$OUT/armA_3e5_cut150k.txt"     # the wave train, presented-time cut
$W 300000 150000 100 12 250 now > "$OUT/armB_3e5_rerun.txt"       # its rerun: the cut wobble (±5 kicks, digest differs)
$W 300000 150000 > "$OUT/armA2_3e5_fixtick.txt"                   # canonical cut: identical digest 58de94ab…
$W 300000 150000 > "$OUT/armB2_3e5_fixtick_rerun.txt"
$W 200000 250000 > "$OUT/armC_2e5_cut250k.txt"                    # 10 waves at 2x10^5
python3 "$R/analyze.py" "$OUT/armA_3e5_cut150k.txt" > "$OUT/regen_reportA.txt" || true
python3 "$R/analyze.py" "$OUT/armC_2e5_cut250k.txt" > "$OUT/regen_reportC.txt" || true
grep -hE "^(end|digest|train):" "$OUT"/*.txt | sort > "$OUT/regen_summary.txt"
echo "--- determinism pairs ---"
paste <(grep -E "^(end|digest):" "$OUT/armA_3e5_cut150k.txt") <(grep -E "^(end|digest):" "$OUT/armB_3e5_rerun.txt") >> "$OUT/regen_summary.txt"
paste <(grep -E "^(end|digest):" "$OUT/armA2_3e5_fixtick.txt") <(grep -E "^(end|digest):" "$OUT/armB2_3e5_fixtick_rerun.txt") >> "$OUT/regen_summary.txt"
echo done
