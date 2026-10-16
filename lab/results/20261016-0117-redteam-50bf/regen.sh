#!/usr/bin/env bash
# Regenerates every number in dossier.md for run 20261016-0117-redteam-50bf.
# The falsifier is standalone float64 (numpy/scipy only): the multiply-add
# cycle-update path does not exist in shipped code, so the oracle is built
# from primary GR closed forms and validated in `validate` mode (Kepler
# kappa_E = 15/8, 1PN kappa_L = 18/(2L^2+6), circular orbits, quadrature
# stability).  Runtime ~2.5 min single-threaded, <100 MB.
set -euo pipefail
cd "$(dirname "$0")"
[ -s work/patch.diff ] && { echo "unexpected patch; this run ships none" >&2; exit 1; }
python3 falsifier.py validate 2>/dev/null | tee validate.json
python3 falsifier.py sweep 2>/dev/null | tee sweep_report.json
python3 falsifier.py chain 2>/dev/null | tee chain.json
python3 - <<'EOF'
import json
rows = [r for r in json.load(open('sweep.json')) if not r.get('unbound_or_degenerate')]
print(f"regen check: {len(rows)} usable sweep rows")
for ch in ('err_phi', 'err_t', 'err_tau'):
    w = max((r[ch], r) for r in rows if r['p'] >= 20 and r['e'] <= 0.9 and r['eps'] == 1e-2)
    print(f"  bulk eps=1e-2 worst {ch}: {w[0]:.2e} at p={w[1]['p']} e={w[1]['e']} d={w[1]['d']}")
for r in rows:
    if r['p'] == 8.0 and r['e'] == 0.9 and r['eps'] == 1e-3 and r['d'] == 'L':
        print(f"  separatrix (p=8,e=0.9,eps=1e-3,L): phi={r['err_phi']:.3e} t={r['err_t']:.3e} tau={r['err_tau']:.3e}")
for k, arms in json.load(open('chain.json'))['chains'].items():
    t = arms['recompile']
    for tag in ('ma_stale_sh', 'ma_r8_sh'):
        a = arms[tag]
        print(f"  {k} {tag}: dt_merge={100*(a['t_merge']/t['t_merge']-1):+.1f}% dphi={a['phi_total']-t['phi_total']:+.2f} rad")
EOF
