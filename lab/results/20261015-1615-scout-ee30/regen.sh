#!/bin/sh
# regen.sh — regenerates every number in dossier.md for 20261015-1615-scout-ee30.
# No tree edits outside this run folder (work/patch.diff is empty); the instrument is
# feed.py alone. Total wall ~4 min (each arm ≤ 32 s, < 2 GB RSS). numpy required.
set -e
cd "$(dirname "$0")"
python3 -c "import feed; r = feed.validate_solver(); print('solver residual max:', r); assert r < 1e-9"
python3 feed.py feed_out.json >/dev/null
python3 - <<'EOF'
import json
R = json.load(open("feed_out.json"))
for k, v in R.items():
    if k == "constants":
        continue
    for sd, d in v["seeds"].items():
        print(f"{k:22s} seed {sd}: in0={d['inside_at_start']:7d} ev={d['events_total']:6d} "
              f"/{d['horizon_s']:.0e}s = {d['events_per_game_s']:.3e}/s per-body "
              f"{d['per_body_per_game_s']:.3e} worst_fr={d['worst_frame_events']:.0f} "
              f"mindist={d['min_body_distance_AU']:.3f}AU")
N = 1e9
rate = 3.35e-8  # per-body upper end of the measured steady range
print(f"scan  at 1e9: {3.5e-6*N/400:.2f} cores   feed at 1e9: {rate*N*3.5e-6:.2e} cores")
print(f"zoom worst frame at 1e9: {2722*N/1e5:.2g} entries (~{2722*N/1e5*3.5e-6:.2g} s undrained)")
print(f"row-value rail at 1e9 full zoom: {3.55e-5*N*4e-6:.3f} cores")
EOF
