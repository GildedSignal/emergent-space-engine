import sys, json, time, random
sys.path.insert(0, '.')
import numpy as np
from hillkit import *

f = open('grid.jsonl', 'w')

def rec(**kw):
    f.write(json.dumps(kw, default=str) + '\n')
    f.flush()

def run_seed(aR, e0, s, w0, M0, T, tag, kickNs=()):
    a = aR * RH
    t0 = time.time()
    tr = truth_run(a, e0, w0, M0, s, T_orb=T, npts=2000)
    row = dict(tag=tag, aR=aR, e0=e0, s=s, w0=w0, M0=M0, T=T,
               truth_wdot=tr['wdot'], apse=tr['apse'], escaped=tr['escaped'],
               e_min=tr['e_min'], e_max=tr['e_max'], e_med=tr['e_med'])
    if tr['apse']:
        row['rel2Q'] = abs(wdot_2Q(a, e0, s) - tr['wdot']) / abs(tr['wdot'])
        a1 = avg1Q_run(a, e0, w0, s, T_orb=T)
        row['rel1Q'] = abs(a1['wdot'] - tr['wdot']) / abs(tr['wdot'])
        row['avg1Q_emax'] = a1['e_max']
    else:
        a1 = avg1Q_run(a, e0, w0, s, T_orb=T)
        row['avg1Q_emax'] = a1['e_max']
    for N in kickNs:
        k = kickN_run(a, e0, w0, M0, s, N=N, T_orb=T)
        row[f'kick{N}'] = k['wdot']
        if k['apse'] and tr['apse']:
            row[f'rel_kick{N}'] = abs(k['wdot'] - tr['wdot']) / abs(tr['wdot'])
        row[f'kick{N}_emax'] = k['e_max']
    row['sec'] = round(time.time() - t0, 1)
    rec(**row)
    print(tag, aR, e0, s, 'rel2Q', row.get('rel2Q'), 'rel1Q', row.get('rel1Q'),
          'sec', row['sec'], flush=True)

t00 = time.time()
# main grid (fixed phases, tuned set)
for aR in [0.10, 0.14, 0.18, 0.22, 0.26, 0.30]:
    for e0 in [0.0, 0.3]:
        for s in [+1, -1]:
            run_seed(aR, e0, s, 0.7, 1.1, 30, 'main')
print('main done', time.time() - t00, flush=True)

# held-out cases (random phases, longer window, unseen a/e combos)
rng = random.Random(42)
for aR, e0 in [(0.12, 0.15), (0.12, 0.6), (0.20, 0.15), (0.20, 0.6),
               (0.25, 0.15), (0.25, 0.6), (0.35, 0.15), (0.35, 0.6)]:
    for s in [+1, -1]:
        w0 = rng.uniform(0, 2 * np.pi)
        M0 = rng.uniform(0, 2 * np.pi)
        run_seed(aR, e0, s, w0, M0, 40, 'heldout')
print('heldout done', time.time() - t00, flush=True)

# kick-floor subset
for (aR, e0, s) in [(0.18, 0.3, +1), (0.25, 0.3, -1), (0.30, 0.15, +1)]:
    run_seed(aR, e0, s, 0.7, 1.1, 30, 'kickfloor',
             kickNs=(2, 4, 8, 16, 32, 64))
print('kickfloor done', time.time() - t00, flush=True)
f.close()
