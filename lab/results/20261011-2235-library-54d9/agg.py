#!/usr/bin/env python3
"""Aggregate: error-cost table, walk slopes, matched-cost comparison."""
import json, math

def load(p):
    return json.load(open(p))['bodies']

def slope(r):
    s = r['samples']
    s = [(t, v) for t, v in s if t > 50]          # second half of horizon
    if len(s) < 8 or s[-1][1] <= 0:
        return float('nan')
    n = len(s); sx = sum(math.log(t) for t, _ in s); sy = sum(math.log(v) for _, v in s)
    sxx = sum(math.log(t) ** 2 for t, _ in s); sxy = sum(math.log(t) * math.log(v) for t, v in s)
    return (n * sxy - sx * sy) / (n * sxx - sx * sx)

def summ(bodies):
    ds = sorted(r['d1'] for r in bodies if r['ok'])
    sl = sorted(slope(r) for r in bodies if r['ok'])
    rs = sorted(r['rate'] for r in bodies if r['ok'])
    n = len(ds)
    return dict(med_d=ds[n // 2], p90_d=ds[int(0.9 * (n - 1))],
                med_slope=sl[n // 2], mean_rate=sum(rs) / len(rs))

A = {k: summ(load(f'jA{k}.json')) for k in [8, 16, 32, 64, 128, 256, 512]}
B = {k: summ(load(f'jB{k}.json')) for k in ['0.02', '0.05', '0.1', '0.2', '0.5']}
C = {k: summ(load(f'jC{k}.json')) for k in ['0.05', '0.1', '0.2']}
D = {k: summ(load(f'jD{k}.json')) for k in ['4', '8', '16', '32', '64']}

print('scheme param  rate/orbit   medD       p90D       med_slope')
for name, tab in (('A', A), ('B', B), ('C', C), ('D', D)):
    for k, s in tab.items():
        print(f'{name}      {str(k):>5}  {s["mean_rate"]:9.2f}  {s["med_d"]:.3e}  {s["p90_d"]:.3e}  {s["med_slope"]:6.2f}')

# power-law fit for A and B (log D vs log rate), then rate needed for D=1e-5
def fit(tab):
    xs = [math.log(s['mean_rate']) for s in tab.values()]
    ys = [math.log(s['med_d']) for s in tab.values()]
    n = len(xs); sx = sum(xs); sy = sum(ys); sxx = sum(x * x for x in xs); sxy = sum(x * y for x, y in zip(xs, ys))
    sl = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    ic = (sy - sl * sx) / n
    return sl, ic

for name, tab in (('A', A), ('B', B)):
    sl, ic = fit(tab)
    need = math.exp((math.log(1e-5) - ic) / sl)
    print(f'{name}: logD/lograte slope {sl:.2f}; rate for medD=1e-5: {need:.0f} evals/body-orbit')

# behaviour: final-state errors vs reference jA512 for one matched-cost triple
ref = load('jA512.json')
for f, label in [('jA32.json', 'A@32 (8.8/orb)'), ('jB0.1.json', 'B@0.1 (36/orb)'),
                 ('jC0.1.json', 'C@0.1 (41/orb)'), ('jD16.json', 'D@16 (11.6/orb)')]:
    b = load(f)
    ea = sorted(abs(math.log(r['a_f'] / q['a_f'])) for r, q in zip(b, ref))
    ee = sorted(abs(r['e_f'] - q['e_f']) for r, q in zip(b, ref))
    el = sorted(abs((r['L_f'] - q['L_f'] + math.pi) % (2 * math.pi) - math.pi) for r, q in zip(b, ref))
    n = len(ea)
    print(f'{label}: med |dln a| {ea[n//2]:.2e}  med |de| {ee[n//2]:.2e}  med |dL| {el[n//2]:.3f}')
