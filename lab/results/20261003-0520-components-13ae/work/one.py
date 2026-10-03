"""Reproduce one seed end to end in <= ~15 s: python3 one.py aR e0 s [T]"""
import sys, json
sys.path.insert(0, '.')
import numpy as np
from hillkit import *

aR, e0, s, T = float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), 30
if len(sys.argv) > 4:
    T = int(sys.argv[4])
w0, M0 = 0.7, 1.1
a = aR * RH
tr = truth_run(a, e0, w0, M0, s, T_orb=T, npts=2000)
row = dict(truth_wdot=tr['wdot'], apse=tr['apse'], e_max=tr['e_max'])
if tr['apse']:
    row['rel2Q'] = abs(wdot_2Q(a, e0, s) - tr['wdot']) / abs(tr['wdot'])
a1 = avg1Q_run(a, e0, w0, s, T_orb=T)
if tr['apse']:
    row['rel1Q'] = abs(a1['wdot'] - tr['wdot']) / abs(tr['wdot'])
for N in (8, 32):
    k = kickN_run(a, e0, w0, M0, s, N=N, T_orb=T)
    if k['apse'] and tr['apse']:
        row[f'rel_kick{N}'] = abs(k['wdot'] - tr['wdot']) / abs(tr['wdot'])
print(json.dumps(row, indent=1, default=str))
