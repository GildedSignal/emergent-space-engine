#!/usr/bin/env python3
"""Formation burst analysis, final instruments.

Reads work/*.tsv (tick contacts walls ops). Definitions:
- W = 64-chronon window contact sums (window 1 = ticks 1-64), matching the wiki's F64.
- late = last third of the run (past every transient; for one-shot arms the merged
  steady state, for trains several full periods).
- mean_late/F64_late/m_late = window mean / Fano / relative modulation over late.
- burst windows: W > 1.5 x mean_late; train peaks = local maxima of W separated by
  >= 2 windows; verdict: 'train' (>=3 peaks, spacing within 25% of median, last/first
  >= 0.7), 'one-shot' (one contiguous burst region, flat late tail), else 'smeared'.
- concentration = (share of contacts in the top 1% of chronons) / 1%.
"""
import glob, json, math, os, sys

WIN = 64
HERE = os.path.dirname(os.path.abspath(__file__))

def load(p):
    meta, rows = {}, []
    for line in open(p):
        if line.startswith('#'):
            for kv in line[2:].split():
                if '=' in kv:
                    k, v = kv.split('=', 1); meta[k] = v
        else:
            rows.append(tuple(map(int, line.split())))
    H = int(meta['horizon'])
    c, w, ops = [0]*H, [0]*H, [0]*H
    for t, cc, ww, oo in rows:
        c[t-1] = cc; w[t-1] = ww; ops[t-1] = oo
    # old headers (pre sx/sy split): sigma= is isotropic; jitter only if not stated
    if 'sx' not in meta and 'sigma' in meta:
        meta['sx'] = meta['sy'] = meta['sigma']
        if 'jitter' not in meta:
            meta['jitter'] = 'true' if meta['sigma'] != '0' else 'false'
    if meta.get('scene') == 'head' and meta.get('aligned') != 'true' and meta.get('jitter') is None:
        meta['jitter'] = 'true'
    return meta, c, w, ops

def fano(ws):
    m = sum(ws)/len(ws)
    var = sum((x-m)**2 for x in ws)/len(ws)
    return m, (var/m if m > 0 else float('inf')), (math.sqrt(var)/m if m > 0 else float('inf'))

def analyze(path):
    meta, c, w, ops = load(path)
    n = int(meta['n']); H = len(c)
    W = [sum(c[i:i+WIN]) for i in range(0, H-WIN+1, WIN)]
    late = W[(len(W)*2)//3:]
    lm, lf64, lmm = fano(late) if late else (0, None, None)
    peaks = [i for i in range(2, len(W)-2)
             if W[i] == max(W[i-2:i+3]) and W[i] > 1.5*lm]
    # merge peaks closer than 2 windows, keep order
    sp = [b-a for a, b in zip(peaks, peaks[1:])]
    period = sorted(sp)[len(sp)//2] if sp else None
    verdict = 'one-shot'
    if period and len(peaks) >= 3 and sp and max(sp) <= 1.25*period and min(sp) >= 0.75*period \
       and W[peaks[-1]]/W[peaks[0]] >= 0.7:
        verdict = 'train'
    elif len(peaks) >= 3 or (peaks and W[peaks[-1]]/W[peaks[0]] < 0.7):
        verdict = 'smeared'
    burst_win = [i for i, x in enumerate(W) if x > 1.5*lm]
    # contiguous burst regions
    regions = []
    for i in burst_win:
        if regions and i - regions[-1][-1] <= 1: regions[-1].append(i)
        else: regions.append([i])
    width = max((r[-1]-r[0]+1)*WIN for r in regions) if regions else 0
    excess = sum(max(0, x-lm) for x in W)
    in_burst = set()
    for r in regions: in_burst.update(range(r[0]*WIN, (r[-1]+1)*WIN))
    ic = sum(x for i, x in enumerate(c) if i in in_burst)
    iops = sum(x for i, x in enumerate(ops) if i in in_burst)
    oc = sum(x for i, x in enumerate(c) if i not in in_burst)
    oops = sum(x for i, x in enumerate(ops) if i not in in_burst)
    cs = sorted(c, reverse=True)
    k = max(1, H//100)
    top1 = sum(cs[:k])/max(1, sum(c))
    tail_rate = sum(c[(H*2)//3:])/max(1, H-(H*2)//3)
    return {
        'file': os.path.basename(path), 'scene': meta.get('scene'), 'n': n,
        'sx': int(meta.get('sx', 0)), 'sy': int(meta.get('sy', 0)),
        'jitter': meta.get('jitter'), 'aligned': meta.get('aligned'), 'seed': meta.get('seed'),
        'H': H, 'contacts': sum(c), 'walls': sum(w),
        'rate_mean': sum(c)/H, 'rate_late': tail_rate,
        'maxc': max(c), 'maxc_per_n': max(c)/n,
        'mean64_late': lm, 'F64_late': lf64, 'm_late': lmm,
        'maxW_over_meanlate': max(W)/lm if lm else None,
        'verdict': verdict, 'n_peaks': len(peaks), 'period_ch': period*WIN if period else None,
        'amp_last_over_first': (W[peaks[-1]]/W[peaks[0]]) if peaks else None,
        'width_ch': width, 'extent': int(meta.get('extent', 0)),
        'width_over_extent': width/int(meta['extent']) if int(meta.get('extent', 0)) else None,
        'excess_per_n': excess/n, 'top1_share': top1, 'concentration': top1*100,
        'ops_per_contact_burst': iops/ic if ic else None,
        'ops_per_contact_quiet': oops/oc if oc else None,
        'digest': meta.get('digest'),
    }

def main():
    res = [analyze(f) for f in sorted(glob.glob(os.path.join(HERE, 'work', '*.tsv')))]
    json.dump(res, open(os.path.join(HERE, 'work', 'analysis.json'), 'w'), indent=1)
    cols = ['file', 'n', 'sx', 'sy', 'jitter', 'aligned', 'verdict', 'n_peaks', 'period_ch',
            'amp_last_over_first', 'maxc', 'maxc_per_n', 'maxW_over_meanlate', 'F64_late',
            'm_late', 'width_ch', 'width_over_extent', 'excess_per_n', 'concentration',
            'ops_per_contact_burst', 'ops_per_contact_quiet', 'rate_late']
    print(' | '.join(cols))
    for r in res:
        print(' | '.join(f"{r.get(c)}" if not isinstance(r.get(c), float) else f"{r.get(c):.3f}" for c in cols))

if __name__ == '__main__':
    main()
