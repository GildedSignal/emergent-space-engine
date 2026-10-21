#!/usr/bin/env bash
# Regenerates every dossier number from this folder's falsifier.py (no repo patch needed).
set -e
cd "$(dirname "$0")"
python3 falsifier.py control > control.json
python3 -c "
import json
d = json.load(open('control.json'))
ok = all(max(abs(a-b) for a,b in zip(sorted(v['measured']), sorted(v['closed']))) < 1e-9 for v in d.values())
print('controls:', 'ALL PASS' if ok else 'FAIL')
assert ok
"
timeout 120 python3 falsifier.py flyby > flyby.json
python3 -c "
import json
d = json.load(open('flyby.json'))['flyby']
print('beta  channel   err(1e-4)    err(3e-2)    c2')
for g in d:
    lo = None
    for k in sorted(g['checkpoints'], key=lambda k: float(k.split('|')[1])):
        a, xi = k.split('|'); xi = float(xi)
        err = list(g['checkpoints'][k].values())[-1]
        if abs(xi - 1e-4) < 1e-9:
            lo = err
        elif abs(xi - 3e-2) < 1e-9:
            print(f\"{g['beta']:<5} {a[:8]:<9} {lo:>9.2e}  {err:>10.2e}   {(err-lo)/(9e-4):>6.0f}\")
"
echo "tau-growth probe (dossier): in-plane err grows ~linearly in tau at both IC signs; z oscillates then drifts."
