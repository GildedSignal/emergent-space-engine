#!/usr/bin/env python3
"""Analysis: wall position vs mu, intermittency, kick-work implication."""
import json
import numpy as np

def wall(prefix, frac=0.5):
    d = json.load(open(prefix + '.json'))
    rows = [r for r in d['rows'] if r['e'] == 0.05]
    rows.sort(key=lambda r: r['a'])
    aw = None
    for r in rows:
        if r['frac_dec'] >= frac:
            aw = r['a']
            break
    return aw, d

print('=== wall position (innermost a with frac_dec >= 0.5, e=0.05) ===')
mus = [(1.23e-5, 'floor'), (1e-4, 'sweep0.0001'), (1e-3, 'sweep0.001'),
       (0.0123, 'main'), (0.03, 'sweep0.03'), (0.05, 'held0.05'), (0.1, 'held0.1')]
pts = []
for mu, pref in mus:
    aw, d = wall(pref)
    pts.append((mu, aw))
    interior = [r for r in d['rows'] if r['e'] == 0.05 and (aw is None or r['a'] < aw - 0.03)]
    mx = max((r['frac_dec'] for r in interior), default=0.0)
    print(f'mu={mu:9.3g}  a_wall={aw}  deco_all={d["frac_deco_all"]:.3f}  '
          f'max_frac_dec_interior={mx:.3f}')

print()
print('=== fit 1 - a_wall = C mu^alpha (where wall exists) ===')
fit = [(m, a) for m, a in pts if a is not None]
if len(fit) >= 2:
    x = np.log10([m for m, a in fit])
    y = np.log10([1 - a for m, a in fit])
    p = np.polyfit(x, y, 1)
    print('alpha = %.3f, C = %.3f' % (p[0], 10**p[1]))
    for m, a in fit:
        pred = 1 - 10**(np.polyval(p, np.log10(m)))
        print(f'  mu={m:8.3g} measured 1-a={1-a:.3f} fitted={pred:.3f}')

print()
print('=== main run: geography at e=0, 0.05, 0.2 (mu=0.0123) ===')
d = json.load(open('main.json'))
for ev in (0.0, 0.05, 0.2):
    rows = sorted([r for r in d['rows'] if r['e'] == ev], key=lambda r: r['a'])
    line = ' '.join(f"{r['a']:.2f}:{r['frac_dec']:.2f}" for r in rows)
    print(f'e={ev}: {line}')

print()
print('=== intermittency: decorrelation/death times at and near the wall ===')
z = np.load('main.npz')
bodies, Td, deadA, deadT = z['bodies'], z['Td'], z['deadA'], z['deadT']
for lo, hi in ((0.60, 0.68), (0.68, 0.90)):
    sel = (bodies[:, 0] >= lo) & (bodies[:, 0] < hi) & (bodies[:, 1] == 0.05)
    t = Td[sel][Td[sel] <= 120]
    if len(t):
        print(f'a in [{lo},{hi}): n_dec={len(t)}, Td percentiles '
              f'10/50/90 = {np.percentile(t,10):.0f}/{np.percentile(t,50):.0f}/{np.percentile(t,90):.0f}')
    surv = (Td[sel] > 120).mean()
    print(f'  survival fraction past 120 orbits: {surv:.2f}')

print()
print('=== kick-work implication (plane numbers) ===')
# uniform: 32 kicks/orbit for every body (H0190 K1)
# classified: averaged layer 0.3/orbit in the predictable zone, full 32 in the web
for label, f in (('LEO fleet a<0.65 a_M (mu=0.0123)', 0.0),
                 ('whole belt [0.3,0.85] (mu=0.0123)', 0.348)):
    work_old = 32.0
    work_new = 32.0 * f + 0.3 * (1 - f)
    print(f'{label}: chaotic fraction {f:.3f} -> work ratio {work_old/work_new:.0f}x')
