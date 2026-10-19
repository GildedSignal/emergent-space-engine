#!/usr/bin/env python3
"""Final numbers for the dossier. Complements analyze.py (which carries the hump-based
table; its spacing columns are noise there because no periodic clock exists — that is
the finding). Here: seasons by smoothed extrema, plateau law, autocorrelation, area
extensivity, free-space season, and the 6400 long-horizon blocks."""
import glob, json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze import load, windows, stats

HERE = os.path.dirname(os.path.abspath(__file__))
WIN = 64

def smooth(xs, k=4):
    return [sum(xs[max(0, i - k):i + k + 1]) / len(xs[max(0, i - k):i + k + 1]) for i in range(len(xs))]

def extrema(sm):
    """indices of alternating local maxima/minima of the smoothed series (monotone in/out)."""
    ex = []
    for i in range(1, len(sm) - 1):
        a, b, c = sm[i - 1], sm[i], sm[i + 1]
        if (b >= a and b >= c and b > sm[i - 1] + 1e-9) or (b <= a and b <= c):
            if ex and ((ex[-1][1] == 'max' and b >= sm[ex[-1][0]]) or (ex[-1][1] == 'min' and b <= sm[ex[-1][0]])):
                ex[-1] = (i, ex[-1][1])
            else:
                ex.append((i, 'max' if b >= a else 'min'))
    return [e for e in ex if e[1] == 'max'], [e for e in ex if e[1] == 'min']

def autocorr_peak(ws):
    """lag (in windows) of max |autocorr| over the second half of lags; ~0 => no clock."""
    n = len(ws)
    m = sum(ws) / n
    x = [v - m for v in ws]
    den = sum(v * v for v in x)
    if den == 0:
        return None
    best, bl = -2, 0
    for lag in range(1, n // 2):
        num = sum(x[i] * x[i + lag] for i in range(n - lag))
        r = num / den
        if abs(r) > best:
            best, bl = abs(r), lag
    return bl, round(best, 3)

def excess(arm, ctrl, t0, t1):
    _, c, _, _ = load(f"{HERE}/work/{arm}.tsv")
    _, cc, _, _ = load(f"{HERE}/work/{ctrl}.tsv")
    return sum(c[t0 - 1:t1]) - sum(cc[t0 - 1:t1])

def one(arm):
    meta, c, w, ops = load(f"{HERE}/work/{arm}.tsv")
    cw = windows(c)
    sm = smooth(cw)
    mx, mn = extrema(sm)
    late = cw[len(cw) * 2 // 3:]
    m_l, f_l, mod_l = stats(late)
    return meta, cw, sm, mx, mn, m_l, f_l, mod_l

def main():
    out = {}
    # --- bounce arms: seasons, plateau, autocorr, area product
    for arm, ctrl in [('mb1600_bs1_s1', None), ('mb1600_bs2_s1', 'co1600_bs2_s1'),
                      ('mb1600_bs2_s2', 'co1600_bs2_s2'), ('mb1600_bs3_s1', None),
                      ('mb400_bs2_s1', 'co400_bs2_s1'), ('mb400_bs2_s2', 'co400_bs2_s1'),
                      ('mb6400_bs2_s1', None), ('mj1600_bs2_s1', 'co1600_bs2_s1'),
                      ('mh1600_bs2_s1', 'co1600_bs2_s1')]:
        meta, cw, sm, mx, mn, m_l, f_l, mod_l = one(arm)
        w_box = int(meta['w']); n = int(meta['n'])
        ac = autocorr_peak(cw[len(cw) // 3:])
        r = {'n': n, 'w': w_box, 'late_mean': round(m_l, 1), 'F64_late': round(f_l, 2),
             'm_late': round(mod_l, 4), 'late_x_area': round(m_l * w_box),
             'autocorr_lag_ch': ac[0] * WIN if ac else None, 'autocorr_r': ac[1] if ac else None,
             'smoothed_maxima_t': [i * WIN + 1 for i, _ in mx[:8]],
             'per_ch_walls_max': max(load(f"{HERE}/work/{arm}.tsv")[2])}
        if ctrl:
            # first season = up to first trough after first max (skip genesis window 0)
            firstmx = [i for i, _ in mx if i >= 4]
            if firstmx:
                p = firstmx[0]
                tr = [i for i, _ in mn if i > p]
                t1 = (tr[0] * WIN + WIN) if tr else len(cw) // 3
                ex1 = excess(arm, ctrl, 257, t1)
                r['season1_end'] = t1
                r['season1_excess_per_fleet_body'] = round(ex1 / (n / 2), 2)
                # echo: next max to next trough
                if len(firstmx) > 1 and len(tr) > 1:
                    p2 = firstmx[1]
                    t2 = tr[1] * WIN + WIN if len(tr) > 1 else len(cw) // 3
                    if p2 * WIN < t2:
                        ex2 = excess(arm, ctrl, t1 + 1, t2)
                        r['echo_excess_per_fleet_body'] = round(ex2 / (n / 2), 2)
                        r['echo_over_season1'] = round(ex2 / max(ex1, 1), 3)
        out[arm] = r
    # --- controls and free
    for arm in ['co1600_bs2_s1', 'co1600_bs2_s2', 'co400_bs2_s1']:
        meta, cw, sm, mx, mn, m_l, f_l, mod_l = one(arm)
        out[arm] = {'late_mean': round(m_l, 1), 'F64_late': round(f_l, 2)}
    for arm in ['mf1600_s1', 'mf1600_s2', 'mf400_s1']:
        meta, c, w, _ = load(f"{HERE}/work/{arm}.tsv")
        cw = windows(c)
        late = cw[len(cw) * 2 // 3:]
        m_l, f_l, _ = stats(late)
        pk = max(range(len(cw)), key=lambda i: cw[i])
        out[arm] = {'peak_t': (pk + 1) * WIN, 'late_mean': round(m_l, 2), 'F64_late': round(f_l, 2),
                    'walls_total': sum(w)}
    # --- 6400 long horizon: block means (first 8192 excluded by construction)
    meta, c, w, _ = load(f"{HERE}/work/mb6400_bs2_s1_long.tsv")
    cw = windows(c)
    blocks = [round(sum(cw[i:i + 128]) / 128) for i in range(0, len(cw), 128)]
    tail = cw[len(cw) * 2 // 3:]
    m_l, f_l, mod_l = stats(tail)
    out['mb6400_bs2_s1_long'] = {'H': int(meta['horizon']), 'block_means_8192ch': blocks,
                                 'late_mean': round(m_l, 1), 'F64_late': round(f_l, 2),
                                 'late_x_area': round(m_l * int(meta['w']))}
    print(json.dumps(out, indent=1))
    with open(f"{HERE}/work/final.json", 'w') as fh:
        json.dump(out, fh, indent=1)

if __name__ == '__main__':
    main()
