#!/usr/bin/env python3
"""Analyze scar growth: fits, crossings, horizon arithmetic."""
import json, math, sys, glob

def load(tier, s):
    return json.load(open('data/%s_s%d.json' % (tier, s)))

def fit_log2(ts, ys, lo=None, hi=None):
    """Least squares slope of y vs log2(t) on window; returns (s, A, r2)."""
    pts = [(math.log2(t), y) for t, y in zip(ts, ys) if (lo is None or t >= lo) and (hi is None or t <= hi)]
    n = len(pts)
    mx = sum(p[0] for p in pts) / n
    my = sum(p[1] for p in pts) / n
    sxx = sum((p[0] - mx) ** 2 for p in pts)
    sxy = sum((p[0] - mx) * (p[1] - my) for p in pts)
    s = sxy / sxx if sxx else 0.0
    A = my - s * mx
    ss_res = sum((y - (A + s * x)) ** 2 for x, y in pts)
    ss_tot = sum((y - my) ** 2 for x, y in pts)
    r2 = 1 - ss_res / ss_tot if ss_tot else 1.0
    return s, A, r2

def qseries(tier, s, quant, col='bpb'):
    d = load(tier, s)
    return ([x['orbit'] for x in d['snaps']], [x[quant][col] for x in d['snaps']])

def cross(ts, ys, level):
    for t, y in zip(ts, ys):
        if y >= level:
            return t
    return None

def med(v):
    v = sorted(v)
    return v[len(v) // 2]

out = {}
for tier in sys.argv[1:]:
    seeds = [0, 1, 2]
    rows = []
    for s in seeds:
        d = load(tier, s)
        ts = [x['orbit'] for x in d['snaps']]
        r = dict(seed=s, orbits=ts[-1], kicks=d['stats']['kicks'],
                 rw_frac=d['stats']['rowwrites'] / max(d['stats']['kicks'], 1),
                 enc=d['stats']['enc'])
        for quant in ('work', 'behav'):
            ys = [x[quant]['bpb'] for x in d['snaps']]
            fl = [x[quant]['floor'] for x in d['snaps']]
            persb = [x[quant]['persb'] for x in d['snaps']]
            kfrac = [x[quant]['k'] / d['stats']['n'] for x in d['snaps']]
            sl, A, r2 = fit_log2(ts, ys, lo=max(40, ts[-1] // 8))
            r[quant] = dict(
                final=ys[-1], final_floor=fl[-1], persb_max=max(persb),
                k_final=kfrac[-1], slope=sl, r2=r2, A=A,
                c16=cross(ts, ys, 16), c51=cross(ts, ys, 51),
                percol_final=d['snaps'][-1][quant]['percol'],
                idx_final=d['snaps'][-1][quant]['idx'])
        r['dev'] = d['snaps'][-1]['dev']
        dl90 = [x['dev']['dl_p90'] for x in d['snaps']]
        da90 = [x['dev']['da_p90'] for x in d['snaps']]
        sl_dl, _, r2dl = fit_log2(ts, dl90, lo=max(40, ts[-1] // 8))
        sl_da, _, r2da = fit_log2(ts, da90, lo=max(40, ts[-1] // 8))
        r['spread'] = dict(dl90_final=dl90[-1], da90_final=da90[-1],
                           dl_slope=sl_dl, da_slope=sl_da)
        rows.append(r)
    out[tier] = rows
    print('=' * 20, tier)
    for r in rows:
        print('seed %d orbits %5d kicks %7d rw/kick %.2f enc %d' %
              (r['seed'], r['orbits'], r['kicks'], r['rw_frac'], r['enc']))
        for quant in ('work', 'behav'):
            q = r[quant]
            lam_share = q['percol_final'][3] / max(sum(q['percol_final']), 1e-12)
            print('  %-5s final %7.2f bpb (floor-model %7.2f), persb_max %7.1f, k %.2f, '
                  'slope %+.3f (r2 %.3f), x16 %s, x51 %s, lambda-share %.2f, idx %.2f bpb' %
                  (quant, q['final'], q['final_floor'], q['persb_max'], q['k_final'],
                   q['slope'], q['r2'], q['c16'], q['c51'], lam_share, q['idx_final']))
        print('  dev final: da p50 %.2e p90 %.2e max %.2e | dl p50 %.3f p90 %.3f max %.3f'
              % (r['dev']['da_p50'], r['dev']['da_p90'], r['dev']['da_max'],
                 r['dev']['dl_p50'], r['dev']['dl_p90'], r['dev']['dl_max']))
        print('  spread slopes: dl90 %+.3f (r2 %.2f) da90 %+.3f (r2 %.2f)'
              % (r['spread']['dl_slope'], r2dl, r['spread']['da_slope'], r2da))
json.dump(out, open('analysis.json', 'w'), indent=1)
