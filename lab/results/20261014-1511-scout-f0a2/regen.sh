#!/usr/bin/env bash
# Regenerates every number in dossier.md from the run's own scripts.
# Runtime: ~35 s (two 8-s scans + compile). No network, no repo state needed.
set -euo pipefail
cd "$(dirname "$0")"

gcc -O2 -o work/screen work/screen.c -lm
./work/screen 20261014 > work/scan.json
./work/screen 777       > work/scan_seed777.json

# key-number assertions (the dossier's load-independent cells)
python3 - <<'EOF'
import json
rows = [json.loads(l) for l in open('work/scan.json')]
s   = next(r for r in rows if r['exp'] == 'summary')
led = next(r for r in rows if r['exp'] == 'ledger')
cc  = next(r for r in rows if r['exp'] == 'charge-control')
hd  = next(r for r in rows if r['exp'] == 'horizon-dial')
assert abs(s['q_energy_m2s2'] - 319.302) < 0.01, s['q_energy_m2s2']
assert s['gate_deletable'] == 1.00000, s['gate_deletable']
assert 0.996 < s['screen_deletable'] < 0.999, s['screen_deletable']
assert 0.998 < s['screen_pairfloor_deletable'] < 1.0
assert s['all_50m_screen'] == 1.0 and s['all_470km_screen'] == 0.0
assert 1000 < s['Dstar_m'] < 1600, s['Dstar_m']
assert s['min_vrel_all'] < 1e-5, s['min_vrel_all']          # P4 falsifier
assert 9e5 < s['bench_ns_per_pair'] < 1.2e6, s['bench_ns_per_pair']
assert led['all10km_gate_deletable'] == 1.00000              # the anchor exhibit
assert led['survivor_fraction_analytic'] < 1e-8
assert all(0.9995 < r['ratio_exact_over_formula'] < 1.0005 for r in cc['rows'])
rc = led['routing_cores']
assert 0.02 < rc[0][0] < 0.05 and 0.5 < rc[0][2] < 0.8       # averaged cadence, 10/200 ns
assert 13 < rc[1][0] < 16 and 250 < rc[1][2] < 310           # shipped cadence
[hr] = [r for r in hd['rows'] if r['horizon_orbits'] == 100]
assert 3500 < hr['Dstar_m'] < 4500 and 1.5e5 < hr['routing_evals_s'] < 2e5
r777 = [json.loads(l) for l in open('work/scan_seed777.json')]
s7 = next(r for r in r777 if r['exp'] == 'summary')
assert s7['gate_deletable'] == 1.00000 and 0.996 < s7['screen_deletable'] < 0.999
print('regen OK: all dossier key numbers reproduced (seeds 20261014 and 777)')
EOF
