#!/usr/bin/env bash
# Regen: every dossier number, from the shipped tree + this folder's scripts. ~5 s.
# No tree edits were needed outside this run folder (work/patch.diff applies clean/no-op).
set -euo pipefail
cd "$(dirname "$0")"

echo "== provenance: the shipped law the replica implements (crates/universe/src/thrust.rs) =="
sed -n '1,7p'    ../../../crates/universe/src/thrust.rs
sed -n '104,127p' ../../../crates/universe/src/thrust.rs

echo
echo "== run (float64; oracle: exact Schwarzschild invariants + DOP853 powered geodesics) =="
python3 kink_law.py > run_output.txt

python3 - <<'EOF'
import json, sys
d = json.load(open("kink_law_results.json"))
c = d["controls"]
# instrument gates: fail loudly if any control breaks
assert c["geodesic_conservation_drift"] == [0.0, 0.0], "geodesic conservation broken"
assert c["weakfield_r1e4"]["shipped_relerr_E"] < 1e-12, "shipped replica broken"
flat = [r for r in d["compose"] if r["mass"] == 0.0]
assert all(r["flat_speed_err"] < 1e-12 for r in flat), "flat composition broken"
assert abs(c["radial_impulse_dL_r6"]["dL_shipped_map"] - 0.108818) < 1e-4
print("controls: GREEN")

print("\nletter/exact ratio for dE (dL tracks it to 3 digits), prograde impulse:")
for row in d["letter"]:
    tag = "flat" if row["M"] == 0 else (f"r={row['r']:g}M" if row["r"] < 1e5 else "r=1e4M")
    print(f"  {tag:>9} eta={row['eta']}: {row['letter_E_ratio']:.4f}"
          + (f"  [shipped relerr {row['shipped_relerr_E']:.1e}]" if "shipped_relerr_E" in row else ""))

print("\nescape burn (deta to E=1 from circular): letter over-calls:")
for row in d["escape"]:
    print(f"  r={row['r']:g}M: exact {row['eta_escape_exact']:.4f}  letter {row['eta_escape_letter']:.4f}"
          f"  x{row['eta_escape_letter']/row['eta_escape_exact']:.3f}")

t = d["three_readings_radial_r6"]
rc = d["controls"]["radial_impulse_dL_r6"]
print(f"\nradial impulse r=6M eta=0.25: dL  axis-boost {rc['dL_axis_boost']}  shipped(FW) +{rc['dL_shipped_map']:.4f}"
      f" (+{rc['dL_shipped_map']/3.4641*100:.2f}% of L0=3.4641)  letter {rc['dL_letter']}")
print(f"held-heading burn dtau=5M: E axis {t['axis_boost_E']:.5f}  FW/compass {t['fw_nose_E']:.5f}/{t['compass_E']:.5f}"
      f"  dL/L {t['axis_boost_dL_over_L']:+.4f}/{t['fw_nose_dL_over_L']:+.4f}/{t['compass_dL_over_L']:+.4f}")

print("\nflush deferral (engine lump vs own continuous law):")
for row in d["compose"]:
    if row["mass"]:
        print(f"  r={row['r']:g}M q={row['q']:.5f}: relerr_E {row['relerr_E']:+.5f} relerr_L {row['relerr_L']:+.5f}")
print("\nREGEN OK")
EOF
