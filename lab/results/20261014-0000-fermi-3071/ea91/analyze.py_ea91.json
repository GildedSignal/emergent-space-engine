#!/usr/bin/env python3
"""The surprise-rate census, analysed: tail shape, attribution, rank stability in time,
intermittency of the aggregate stream. Input: census-*.json from ES_SURPRISE=1 universe --bench."""
import json, sys, glob, os
import numpy as np
from scipy import stats as st

HERE = os.path.dirname(os.path.abspath(__file__))

def gini(x):
    x = np.sort(np.asarray(x, float))
    n = len(x)
    if n == 0 or x.sum() == 0: return float('nan')
    return float((2 * np.arange(1, n + 1) - n - 1).dot(x) / (n * x.sum()))

def zipf_slope(counts):
    """OLS slope of log(count) on log(rank) over the sorted counts (top 90%)."""
    c = np.sort(np.asarray(counts, float))[::-1]
    c = c[c > 0][:max(3, int(0.9 * len(c)))]
    if len(c) < 3: return float('nan')
    r = np.arange(1, len(c) + 1)
    slope, intercept = np.polyfit(np.log(r), np.log(c), 1)
    return float(slope)

def top_share(x, frac):
    x = np.sort(np.asarray(x, float))[::-1]
    k = max(1, int(round(frac * len(x))))
    return float(x[:k].sum() / x.sum()) if x.sum() else float('nan')

def spearman(a, b):
    if len(a) < 3: return float('nan')
    r = st.spearmanr(a, b).statistic
    return float(r) if r == r else float('nan')

def analyse(path):
    d = json.load(open(path))
    s = d['surprise']
    kinds = np.array(s['entities']); items = np.array(s['items'], float); kicks = np.array(s['kicks'], float)
    born = np.array(s['born'], float) if s['born'] else np.zeros(len(kinds))
    half = np.array(s['half_items'] or [], float)
    enc = s['encounters']; pfe = np.array(s['per_frame_events'], float)
    alive = np.array(s.get('alive') or [True] * n, bool)
    cut = d['cut_tick']; n = len(kinds)
    alive0 = born == 0                       # alive the whole canonical window
    native = np.array([k in ('Planet', 'Moon', 'Star', 'Player') for k in kinds])
    player = kinds == 'Player'
    out = {'scene': os.path.basename(path), 'digest': d['digest'][:12], 'bodies': n,
           'live_at_start': int(alive0.sum()), 'promoted': int((born > 0).sum()),
           'items': int(items.sum()), 'kicks': int(kicks.sum()), 'encounters': len(enc)}
    for name, mask in [('all', np.ones(n, bool)), ('native', native & alive0 & ~player),
                       ('promoted', (born > 0) & ~player), ('player', player)]:
        x = items[mask]
        if len(x) and x.sum():
            out[f'{name}'] = {'n': len(x), 'items': int(x.sum()), 'gini': round(gini(x), 3),
                              'top10_share': round(top_share(x, 0.10), 3), 'top1_share': round(top_share(x, 0.01), 3),
                              'zipf_slope': round(zipf_slope(x), 3), 'max_over_median': round(float(x.max() / max(np.median(x[x > 0]), 1)), 1)}
    # death split of the promotions (the churn channel: dead bodies resolve nothing after they die)
    h2full = None
    if len(half):
        h2full = items[:n].copy(); h2full[:len(half)] -= half
    prom_mask = (born > 0) & (kinds == 'Ship')
    pl = prom_mask & alive
    out['promotions'] = {'promoted': int(prom_mask.sum()), 'dead': int((prom_mask & ~alive).sum()),
                         'dead_frac': round(float((prom_mask & ~alive).sum() / prom_mask.sum()), 3) if prom_mask.sum() else None,
                         'alive': int(pl.sum())}
    if h2full is not None and pl.sum():
        out['promotions']['alive_dormant_h2'] = int((pl & (h2full == 0)).sum())
        out['promotions']['alive_h2_topdecile_share'] = round(float(np.sort(h2full[pl])[::-1][:max(1, pl.sum() // 10)].sum() / max(h2full[pl].sum(), 1)), 3)
        out['promotions']['alive_h2_median'] = float(np.median(h2full[pl]))
    # rank stability: first half vs second half, bodies present in the snapshot and alive throughout
    m = len(half)
    if m and n >= m:
        h1 = half.copy(); h2 = items[:m] - h1
        sel = (born[:m] <= cut / 2) & ((h1 + h2) > 0) & alive[:m]   # alive the whole second half
        prom = sel & (born[:m] > 0); nat = sel & (born[:m] == 0)
        # exposure-fair rates: the first-half window is shorter for a body born inside it
        expo1 = np.maximum(cut / 2 - born[:m], cut / 16)
        r1, r2 = h1 / expo1, h2 / (cut / 2)
        # top-decile overlap between halves (Jaccard), on rates
        k = max(1, sel.sum() // 10)
        t1 = set(np.argsort(np.where(sel, r1, -1))[::-1][:k].tolist())
        t2 = set(np.argsort(np.where(sel, r2, -1))[::-1][:k].tolist())
        out['rank_stability'] = {'n': int(sel.sum()), 'promoted_n': int(prom.sum()),
                                 'spearman_rates': round(spearman(r1[sel], r2[sel]), 3),
                                 'spearman_native': round(spearman(r1[nat], r2[nat]), 3) if nat.sum() > 3 else None,
                                 'spearman_promoted': round(spearman(r1[prom], r2[prom]), 3) if prom.sum() > 3 else None,
                                 'topdecile_jaccard': round(len(t1 & t2) / len(t1 | t2), 3)}
        # Poisson-remeasurement null for the same counts (are the ranks better than re-noise?)
        if sel.sum() > 3:
            rng = np.random.default_rng(7)
            rs = []
            base = (h1[sel] + h2[sel]) / 2.0
            for _ in range(200):
                a = rng.poisson(np.maximum(base, 0.1)); b = rng.poisson(np.maximum(base, 0.1))
                rs.append(spearman(a, b))
            out['rank_stability']['spearman_poisson_null'] = round(float(np.nanmedian(rs)), 3)
    # encounters: per-body counts, halves split at the half-run tick (linear pacing: cut/2)
    if len(enc):
        half_t = cut / 2
        cnt = np.zeros(n); c1 = np.zeros(n); c2 = np.zeros(n)
        for a, b, t, contact in enc:
            cnt[a] += 1; cnt[b] += 1
            (c1 if t <= half_t else c2)[a] += 1; (c1 if t <= half_t else c2)[b] += 1
        m2 = (cnt > 0) & (born == 0)
        out['encounters'] = {'bodies_with_any': int((cnt > 0).sum()), 'total': len(enc),
                             'gini': round(gini(cnt[cnt > 0]), 3) if (cnt > 0).any() else None,
                             'top10_share': (round(top_share(cnt, 0.10), 3) if cnt.sum() else None),
                             'spearman_halves': round(spearman(c1[m2], c2[m2]), 3) if m2.sum() > 3 else None}
    # intermittency of the aggregate stream, whole run and the steady tail (last 30% of frames)
    if len(pfe) and pfe.sum():
        tail = pfe[int(0.7 * len(pfe)):]
        out['decile_items'] = [int(pfe[i * len(pfe) // 10:(i + 1) * len(pfe) // 10].sum()) for i in range(10)]
        out['steady_tail'] = {'mean_per_frame': round(float(tail.mean()), 2),
                              'fano': round(float(tail.var() / tail.mean()), 2) if tail.mean() else None,
                              'top1pct_frames_share': round(top_share(tail, 0.01), 3),
                              'zero_frac': round(float((tail == 0).mean()), 3)}
        mu, var = pfe.mean(), pfe.var()
        out['stream'] = {'frames': len(pfe), 'mean': round(float(mu), 2), 'fano': round(float(var / mu), 2) if mu else None,
                         'burstiness': round(float((np.sqrt(var) - mu) / (np.sqrt(var) + mu)) if (np.sqrt(var) + mu) else None, 3),
                         'lag1_autocorr': round(float(np.corrcoef(pfe[:-1], pfe[1:])[0, 1]), 3) if len(pfe) > 2 else None,
                         'max': int(pfe.max()), 'p99': float(np.percentile(pfe, 99)),
                         'zero_frac': round(float((pfe == 0).mean()), 3),
                         'top1pct_frames_share': round(top_share(pfe, 0.01), 3),
                         'worst_frame_share': round(float(pfe.max() / pfe.sum()), 4)}
    # the five busiest bodies, attributed
    idx = np.argsort(items)[::-1][:5]
    out['top5'] = [{'e': int(i), 'kind': kinds[i], 'items': int(items[i]), 'born': int(born[i])} for i in idx]
    return out

if __name__ == '__main__':
    rows = [analyse(p) for p in (sys.argv[1:] or sorted(glob.glob(f'{HERE}/census-*.json')))]
    print(json.dumps(rows, indent=1))
