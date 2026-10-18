#!/bin/sh
# Regen: every dossier number from scan_replica.py (needs python3 + numpy only).
# work/patch.diff is empty for this run (no tree edits outside lab/results/<run>/);
# applied by the runner before this runs, harmless either way.
set -e
cd "$(dirname "$0")"
python3 scan_replica.py
python3 - <<'EOF'
import json
r = json.load(open("scan_replica.json"))
p2, p3, p4, p5, nc = r["P2_answer_tier_circular"], r["P3_eccentricity"], r["P4_shear"], r["P5_price"], r["negative_control"]
assert p2["d_dot_w_max"] < 1e-13, "d.w != 0: the collapse premise fails"
assert p2["closed_form_vs_brute_max_err"] < 1e-14, "closed form != shipped predicate at e=0"
for rho, lo, hi in [("rho=1e-07", 25, 50), ("rho=1e-06", 280, 400), ("rho=1e-05", 2900, 3600)]:
    n = p2[rho]["near_set_uniform_per_1e6"]
    assert lo <= n <= hi, f"near-set window {rho}: {n} outside [{lo},{hi}]"
assert p2["rho=1e-06"]["near_set_clustered_sigma0.02_per_1e6"] > 100 * p2["rho=1e-06"]["near_set_uniform_per_1e6"], "clustering growth"
assert p3["e=0.0_periapsis"]["naive_circular_chord_membership_error"] == 0.0, "e=0 exactness control"
assert p3["e=0.5_periapsis"]["naive_circular_chord_membership_error"] > 0.01, "chord must degrade at e=0.5"
assert p3["e=0.5_periapsis"]["curve_2^14_membership_error"] < 0.02, "curve grid-limited claim"
assert p4["sigma_a=1.0e-05"]["unsound_misses"] == 0, "phase-only tier unsound below the measured bound"
assert abs(p4["sigma_a=1.0e-03"]["unsound_misses"]) > 0, "shear failure mode must appear by 1e-3"
assert abs(p4["predicted_sigma_star"] / 1.0e-3 - 1) < 0.5, "onset vs predicted sigma*"
ratio = p5["shipped_answer_s_at_1e6"] / (p5["K"] * p5["vectorised_per_member_ns"] * 1e-9 + p5["exact_reads_needed_coast_rho1e-6"] * 7.1e-6)
assert ratio >= 200, f"instrument-measured gain {ratio:.0f}x < 200x"
assert nc["shuffled_disagreement"] > 0.30 and nc["unshuffled_disagreement"] == 0.0, "negative control"
print(f"regen OK: instrument gain {ratio:.0f}x, exact reads {p5['exact_reads_needed_coast_rho1e-6']}, "
      f"near sets {p2['rho=1e-07']['near_set_uniform_per_1e6']}/{p2['rho=1e-06']['near_set_uniform_per_1e6']}/"
      f"{p2['rho=1e-05']['near_set_uniform_per_1e6']}")
EOF
