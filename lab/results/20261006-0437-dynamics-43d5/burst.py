#!/usr/bin/env python3
"""Burst anatomy + honest cone-margin re-setup multiplier, from elastic dumps."""
import numpy as np
import math

ln2 = math.log(2)

for f in ['dump_s1.npz', 'dump_s2.npz', 'dump_s3.npz']:
    d = np.load(f)
    t, i, j = d['t'], d['i'], d['j']
    ordm = np.argsort(t, kind='stable')
    t, i, j = t[ordm], i[ordm], j[ordm]
    TWOPI = 2 * math.pi
    print('==', f, 'events', len(t), 'orbits', round(t[-1] / TWOPI, 1))
    # top burst: window of 1 orbit with max events; anatomy of that window
    nb = int(t[-1] // TWOPI)
    cnt, _ = np.histogram(t, bins=np.arange(0, (nb + 1) * TWOPI, TWOPI))
    k = int(np.argmax(cnt))
    print('  max orbit bin: %d events (mean %.1f)' % (cnt[k], cnt.mean()))
    sel = (t >= k * TWOPI) & (t < (k + 1) * TWOPI)
    bi, bj = i[sel], j[sel]
    pairs = set(zip(bi.tolist(), bj.tolist()))
    bodies = set(bi.tolist()) | set(bj.tolist())
    from collections import Counter
    pc = Counter(zip(bi.tolist(), bj.tolist()))
    bc = Counter(bi.tolist()); bc.update(bj.tolist())
    top_pair = pc.most_common(3)
    print('  burst anatomy: %d events, %d distinct pairs, %d distinct bodies' % (sel.sum(), len(pairs), len(bodies)))
    print('  top pairs:', top_pair, ' max per-body multiplicity:', bc.most_common(3))
    # same-pair refire times within the burst
    if top_pair:
        (a, b), c = top_pair[0]
        m = ((bi == a) & (bj == b))
        tt = np.sort(t[sel][m])
        if len(tt) > 2:
            dt = np.diff(tt)
            print('  top-pair inter-event gaps (orbits):', [round(x / TWOPI, 4) for x in dt[:6]])
    # global: inter-event time for repeated pairs anywhere
    key = np.array([a * 100000 + b for a, b in zip(i.tolist(), j.tolist())])
    # per-body kick multiplicity over whole run, last 50%
    m50 = t > t[-1] / 2
    cc = Counter(i[m50].tolist()); cc.update(j[m50].tolist())
    vals = np.array(list(cc.values()))
    print('  per-body kicks in last half: mean %.1f, p99 %d, max %d (Fano %.2f)' % (
        vals.mean(), np.percentile(vals, 99), vals.max(), vals.var() / vals.mean()))

# honest cone-margin multiplier from final elements snapshot (s1)
print()
for f in ['dump_s1.npz', 'dump_N1536.npz']:
    d = np.load(f)
    p, e, w = d['p'], d['e'], d['w']
    U = 1.0 / p
    V = e * np.cos(w) / p
    Ww = e * np.sin(w) / p
    n = len(U)
    ordU = np.argsort(U)
    qu = ln2 / 16  # m=16 quantum in ln u; but cone lives in (U,V,W) linear in 1/p ~ O(1)
    # pairs within one quantum qu of the cone boundary |dU^2 - (dV^2+dW^2)| < 2*qu*|U|
    # candidate = pairs with radial reach overlap: |a_i-a_j| < e_i a_i + e_j a_j + bmax
    a = p / (1 - e * e)
    ea = e * a
    idx = np.argsort(a)
    bmax = 2.0 * ((2.0 * 5e-8 / 3.0) ** (1.0 / 3.0)) * 1.2
    margin_cnt = 0; tot_cnt = 0
    aa = a[idx]
    eaa = ea[idx]
    UU = U[idx]; VV = V[idx]; WW = Ww[idx]
    import bisect
    for k in range(n):
        lo = bisect.bisect_left(aa, aa[k] - (eaa.max() + bmax))
        hi = bisect_right(aa, aa[k] + (eaa.max() + bmax))
        for q in range(lo, hi):
            if q <= k: continue
            tot_cnt += 1
            dU2 = (UU[k] - UU[q]) ** 2
            dVW = (VV[k] - VV[q]) ** 2 + (WW[k] - WW[q]) ** 2
            if abs(dU2 - dVW) < 2 * qu:
                margin_cnt += 1
    print(f, 'cone-margin pairs / crossing-window pairs: %d / %d = %.4f' % (margin_cnt, tot_cnt, margin_cnt / max(1, tot_cnt)))
