import sys, json, time
sys.path.insert(0, '.')
import numpy as np
from hillkit import *

t0 = time.time()
out = {}
for tag, (aR, e0, s) in {
    'safe-pro': (0.12, 0.3, +1),
    'safe-retro': (0.12, 0.3, -1),
    'safe-pro-circ': (0.12, 0.0, +1),
}.items():
    a = aR * RH
    w0, M0 = 0.7, 1.1
    tr = truth_run(a, e0, w0, M0, s, T_orb=30)
    q2 = wdot_2Q(a, e0, s)
    a1 = avg1Q_run(a, e0, w0, s, T_orb=30)
    row = dict(truth_wdot=tr['wdot'], apse=tr['apse'], escaped=tr['escaped'],
               e_med=tr['e_med'], e_min=tr['e_min'], e_max=tr['e_max'],
               avg2Q=q2, avg1Q=a1['wdot'], avg1Q_emax=a1['e_max'],
               rel2Q=abs(q2 - tr['wdot']) / abs(tr['wdot']) if tr['apse'] else None,
               rel1Q=abs(a1['wdot'] - tr['wdot']) / abs(tr['wdot']) if tr['apse'] else None)
    if tag != 'safe-pro-circ':
        k = kickN_run(a, e0, w0, M0, s, N=64, T_orb=30)
        row['kick64'] = k['wdot']
        row['rel_kick64'] = abs(k['wdot'] - tr['wdot']) / abs(tr['wdot']) if k['apse'] else None
    out[tag] = row
    print(tag, json.dumps(row, default=str))

# truth convergence control
a = 0.12 * RH
tr_tight = truth_run(a, 0.3, 0.7, 1.1, +1, T_orb=30, rtol=1e-13)
print('tight', tr_tight['wdot'], 'delta rel',
      abs(tr_tight['wdot'] - out['safe-pro']['truth_wdot']) / abs(tr_tight['wdot']))

# multipole truncation: quadrupole closed form vs numeric, residual size
for (aR, e0) in [(0.3, 0.3), (0.3, 0.6), (0.45, 0.3)]:
    a = aR * RH
    full, q, resid = double_avg_exact(a, e0, 0.7)
    C = MU_S * a**2 / 4
    closed = C * (1 + 1.5 * e0**2)
    print(f'mult a={aR}R_H e={e0}: quad_num={q:.4e} closed={closed:.4e} '
          f'resid/quad={resid/q:.2e}')

print('elapsed', time.time() - t0)
