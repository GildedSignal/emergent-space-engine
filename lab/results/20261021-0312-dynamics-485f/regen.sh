#!/bin/bash
# Regenerates every dossier number for 20261021-0312-dynamics-485f.
# ~9 min on 2 cores. Run from anywhere; lands in the repo root.
set -e
RUN_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$RUN_DIR/../../.." && pwd)"
cd "$ROOT"
# apply this run's patch if not already applied (the runner usually has)
if git apply --check "$RUN_DIR/work/patch.diff" 2>/dev/null; then
  git apply "$RUN_DIR/work/patch.diff"
fi
cargo build --release --example beltledger -p emergent-lattice
B=${CARGO_TARGET_DIR:-target}/release/examples/beltledger
[ -x "$B" ] || B="$CARGO_TARGET_DIR/release/examples/beltledger"
R="$RUN_DIR/work"
rm -rf "$R/cold1" "$R/therm2"
"$B" --seed 1 --horizon 98304 --tag cold1 > "$R/cold1.run.log" 2>&1 &
"$B" --seed 2 --horizon 49152 --thermal 4 --tag therm2 > "$R/therm2.run.log" 2>&1 &
wait
cd "$RUN_DIR"
python3 analyze.py cold1 therm2 > work/analyze-out.txt
python3 - <<'EOF'
import json
rep = json.load(open("work/report.json"))
for tag, r in rep.items():
    w = r["walk"]; pb = r.get("perbody_walk", {}); ra = r.get("rattle", {}); p = r.get("pairs", {}); h = r.get("hottrace", {})
    print(f"{tag}: contacts={w['contacts_last']} alpha_storm={w['alpha_storm']:.3f} alpha_late={w['alpha_late'] and round(w['alpha_late'],3)} "
          f"perbody_alpha={pb.get('alpha'):.3f} r2={pb.get('r2'):.4f} res_max={w['res_max_last']} station_ratio={w['station_ratio'] and round(w['station_ratio'],3)} "
          f"bias_last={w['bias_last']:.3f} c64mean={ra.get('c64_mean',0):.0f} hot={ra.get('hot_mean',0):.0f} pmed={ra.get('pmed_last',0):.1f} "
          f"top1={p.get('top1_share',0):.4f} pairs={p.get('distinct_pairs')} halfdrift={h.get('half_drift_over_range_med'):.3f}")
EOF
echo REGEN_OK
