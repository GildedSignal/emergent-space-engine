#!/usr/bin/env python3
"""Controls + aggregation for the conjunction-map runs.

Controls on both sides for the burstiness estimator:
- synthetic Poisson series (must give Allan ~ 1),
- synthetic supercritical Hawkes series (must give Allan growing with window).
Then aggregates all conjmap JSONs into one table.
"""
import json, math, sys, glob
import numpy as np

def allan_factor(ts, T_total, windows, unit):
    out = {}
    for w in windows:
        bw = w * unit
        nb = int(T_total // bw)
        if nb < 8: continue
        c, _ = np.histogram(ts, bins=np.arange(0, (nb + 1) * bw, bw))
        mu = c.mean()
        out[f'{w}'] = float(c.var() / mu) if mu > 0 else float('nan')
    return out

rng = np.random.default_rng(7)
Nev = 700
Ttot = 30 * 2 * math.pi
# Poisson control
pois = rng.uniform(0, Ttot, Nev * 20)
# Hawkes control (supercritical self-exciting, exp kernel; children of each event: Poisson(m), delay ~ Exp(theta))
def hawkes(n0=0.05, m=1.5, theta=1.0 / (0.5 * 2 * math.pi), T=Ttot, cap=200000):
    lam = n0 * T
    immigrants = rng.uniform(0, T, rng.poisson(lam))
    ev = list(immigrants); k = 0
    while k < len(ev) and len(ev) < cap:
        t0 = ev[k]; k += 1
        for _ in range(rng.poisson(m)):
            dt = rng.exponential(1.0 / theta)
            if t0 + dt < T:
                ev.append(t0 + dt)
    return np.array(sorted(ev))
haw = hawkes()
print(f'# controls: Poisson n={len(pois)}  Hawkes n={len(haw)} (supercritical)')
unit = 2 * math.pi
windows = (0.25, 0.5, 1.0, 2.0, 4.0, 8.0)
print('# Allan factors, window in orbits:')
print('# Poisson :', {k: round(v, 2) for k, v in allan_factor(pois, Ttot, windows, unit).items()})
print('# Hawkes  :', {k: round(v, 2) for k, v in allan_factor(haw, Ttot, windows, unit).items()})

hdr = ('run', 'N', 'seed', 'frag', 'orb', 'kicks/body/orb(last20%)', 'cross16', 'cross8',
       'work16/enc', 'Allan.5', 'Allan2', 'branch(post/base)', 'E_drift', 'e_rms', 'alive')
print('\t'.join(hdr))
for f in sorted(glob.glob((sys.argv[1] if len(sys.argv) > 1 else 'run_*.json'))):
    d = json.load(open(f))
    p = d['params']
    al = d.get('allan', {})
    bp = d.get('branch_proxy_post', float('nan')); bb = d.get('branch_proxy_base', float('nan'))
    cr = d.get('cross_rate', {})
    print('\t'.join(str(x) for x in (
        f.replace('.json', ''), p['N'], p['seed'], p['frag'], round(d['orbits_done'], 1),
        round(d.get('kick_rate_last20pct', float('nan')), 4),
        round(cr.get('16', float('nan')), 5), round(cr.get('8', float('nan')), 5),
        round(d.get('setup_work_vs_enc_m16', float('nan')), 2),
        round(al.get('0.5', float('nan')), 2), round(al.get('2.0', float('nan')), 2),
        f'{bp:.3f}/{bb:.3f}', f"{d['E_drift_rel']:.1e}",
        round(d.get('e_rms_final', float('nan')), 4), d['n_alive_end'])))
