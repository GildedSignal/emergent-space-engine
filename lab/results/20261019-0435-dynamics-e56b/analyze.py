#!/usr/bin/env python3
"""Wall-reflection train analysis (run e56b). Reads work/*.tsv (tick contacts walls ops).

Instruments (window W = 64 ch, matching the wiki's F64):
- windows: contact sums per W; late = last third of the horizon.
- mean_late / m_late / F64_late as in 90b7's analyze.py.
- HUMPS: local maxima of the smoothed window series above baseline+thresh; the train
  clock = median hump spacing; amplitude = peak height above the cloud-only baseline
  (from the nofleet control at the same n/boxscale, else the series' own late mean).
- walls clock: same peak detection on the walls series (the fleet bouncing).
- verdict per arm: 'train' (>=3 humps, spacing within 25% of median, last/first >= 0.7),
  'ringdown' (>=3 humps, last/first < 0.5), 'one-shot' (1 hump region, flat tail),
  'flat' (no humps above threshold).
Prints one JSON row per arm + a table; work/analysis.json holds everything.
"""
import glob, json, math, os

WIN = 64
HERE = os.path.dirname(os.path.abspath(__file__))

def load(p):
    meta, rows = {}, []
    for line in open(p):
        if line.startswith('#') and '=' in line:
            for kv in line[1:].split():
                if '=' in kv:
                    k, v = kv.split('=', 1)
                    meta[k] = v
            continue
        if line.startswith('#') or not line.strip():
            continue
        rows.append(tuple(map(int, line.split())))
        rows = rows
        if line.startswith('#') or not line.strip():
            continue
        rows.append(tuple(map(int, line.split())))
    H = int(meta['horizon'])
    c, w, ops = [0] * H, [0] * H, [0] * H
    for t, cc, ww, oo in rows:
        c[t - 1] = cc; w[t - 1] = ww; ops[t - 1] = oo
    return meta, c, w, ops

def windows(series):
    return [sum(series[i:i + WIN]) for i in range(0, len(series) - WIN + 1, WIN)]

def stats(ws):
    m = sum(ws) / len(ws)
    var = sum((x - m) ** 2 for x in ws) / len(ws)
    return m, (var / m if m > 0 else float('inf')), (math.sqrt(var) / m if m > 0 else 0.0)

def humps(ws, baseline, frac=0.35):
    """Indices of local maxima above baseline + frac*(max-baseline), separated >=2 windows."""
    hi = max(ws)
    thr = baseline + frac * max(hi - baseline, 1e-9)
    out = []
    for i in range(1, len(ws) - 1):
        if ws[i] >= ws[i - 1] and ws[i] >= ws[i + 1] and ws[i] > thr:
            if not out or i - out[-1][0] >= 2:
                out.append((i, ws[i]))
            elif ws[i] > out[-1][1]:
                out[-1] = (i, ws[i])
    return out

def spacing(hs):
    if len(hs) < 2:
        return None
    sp = [b[0] - a[0] for a, b in zip(hs, hs[1:])]
    med = sorted(sp)[len(sp) // 2]
    ok = all(abs(s - med) <= 0.25 * med for s in sp)
    return med * WIN, ok

def analyze(path, baselines):
    meta, c, w, ops = load(path)
    name = os.path.basename(path)[:-4]
    H = int(meta['horizon'])
    cw, ww = windows(c), windows(w)
    late = cw[len(cw) * 2 // 3:]
    m_l, f_l, mod_l = stats(late)
    w_sp = float(meta.get('w', 0))
    key = f"co{meta['n']}_bs{float(meta['boxscale']):g}"
    base = baselines.get(key)
    base_note = 'control' if base is not None else 'late-mean'
    hbase = base if base is not None else m_l
    hs = humps(cw, hbase)
    whs = humps(ww, 0.5 * (max(ww) if ww else 0))
    csp, wsp_ok = (spacing(hs) or (None, None))
    wsp, wsp_ok = (spacing(whs) or (None, None))
    amps = [h - hbase for _, h in hs]
    verdict = 'flat'
    if hs:
        if len(hs) >= 3 and amps[0] > 0:
            ratio = amps[-1] / amps[0]
            if csp is not None and wsp_ok and ratio >= 0.7:
                verdict = 'train'
            elif ratio < 0.5:
                verdict = 'ringdown'
            else:
                verdict = 'smeared'
        elif len(hs) <= 2:
            verdict = 'one-shot' if m_l > 0 and mod_l < 0.5 else 'few'
    excess_total = sum(c) - (baselines.get(key + '_total') or 0)
    return {
        'arm': name, 'n': int(meta['n']), 'w': int(w_sp), 'H': H,
        'seed': int(meta['seed']), 'free': meta.get('free', 'false'),
        'nofleet': meta.get('nofleet', 'false'), 'jitter': meta.get('jitter', 'false'),
        'cloudvmax': int(meta['cloudvmax']) if meta.get('cloudvmax') else None,
        'contacts': sum(c), 'walls_total': sum(w),
        'mean_late': round(m_l, 1), 'F64_late': round(f_l, 2), 'm_late': round(mod_l, 4),
        'maxW_over_late': round(max(cw) / m_l, 2) if m_l else None,
        'humps': len(hs), 'spacing_ch': csp, 'spacing_reg': wsp_ok,
        'pred_4w': round(4 * w_sp, 0),
        'spacing_over_w': round(csp / w_sp, 3) if csp and w_sp else None,
        'wall_humps': len(whs), 'wall_spacing_ch': wsp, 'wall_spacing_ok': wsp_ok,
        'amp_last_first': round(amps[-1] / amps[0], 3) if amps and amps[0] > 0 else None,
        'baseline_from': base_note,
        'excess_per_body_per_crossing': round(excess_total / max(int(meta['n']) / 2, 1) / max(len(hs), 1), 2),
        'verdict': verdict,
        'digest': meta.get('digest', ''),
    }

def main():
    files = sorted(glob.glob(os.path.join(HERE, 'work', '*.tsv')))
    # baselines from the nofleet controls: late mean of windowed contacts, and totals
    baselines = {}
    for f in files:
        meta, c, _, _ = load(f)
        if meta.get('nofleet') == 'true':
            cw = windows(c)
            late = cw[len(cw) * 2 // 3:]
            key = f"co{meta['n']}_bs{float(meta['boxscale']):g}"
            baselines[key] = sum(late) / len(late)
            baselines[key + '_total'] = sum(c)
    res = [analyze(f, baselines) for f in files]
    with open(os.path.join(HERE, 'work', 'analysis.json'), 'w') as fh:
        json.dump(res, fh, indent=1)
    cols = ['arm', 'verdict', 'humps', 'spacing_ch', 'pred_4w', 'spacing_over_w',
            'spacing_reg', 'amp_last_first', 'maxW_over_late', 'F64_late', 'm_late',
            'mean_late', 'wall_humps', 'wall_spacing_ch', 'excess_per_body_per_crossing']
    print(' | '.join(cols))
    for r in res:
        print(' | '.join(str(r.get(cn)) for cn in cols))

if __name__ == '__main__':
    main()
