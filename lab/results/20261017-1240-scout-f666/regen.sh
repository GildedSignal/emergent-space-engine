#!/bin/sh
# Regen for 20261017-1240-scout-f666. No repo-tree patch (work/patch.diff empty);
# the run's only instrument is handoff_rule.py. Total < 2 min.
set -e
cd "$(dirname "$0")"
python3 handoff_rule.py --json results.json
python3 handoff_rule.py --mu 1e-4 > heldout-mu1e-4.txt
python3 handoff_rule.py --mu 1e-2 > heldout-mu1e-2.txt
python3 - <<'EOF' > longwindow-kick.txt
import handoff_rule as H
for r0f, sense, nP in [(0.7,H.RET,100),(0.5,H.RET,100),(0.3,H.RET,100),(0.3,H.PRO,100),(0.5,H.PRO,100)]:
    r = H.run_case(1e-3, r0f, sense, nP)
    print(f"({r0f},{'pro' if sense>0 else 'ret'}) {nP}P truth={r['truth']} max_r2/RH={r['max_r2_RH']:.2f} R0={r['R0']} R1={r['R1']} R2={r['R2']} R3={r['R3']} apo={r['n_apo']}")
r = H.run_case(1e-3, 0.5, H.PRO, 20, kick_t=10, kick_dv=0.03)
print('kick 3% at 10P on (0.5,pro):', r['truth'], 'R0=',r['R0'],'R1=',r['R1'],'R2=',r['R2'],'R3=',r['R3'])
r = H.run_case(1e-3, 0.5, H.RET, 20, kick_t=10, kick_dv=0.03)
print('kick 3% at 10P on (0.5,ret):', r['truth'], 'R0=',r['R0'],'R1=',r['R1'],'R2=',r['R2'],'R3=',r['R3'])
EOF
