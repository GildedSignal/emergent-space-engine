#!/usr/bin/env python3
"""Aggregate decisive runs: cross-seed medians, growth exponent, memory verdict."""
import json, sys
import numpy as np

def load(f):
    return json.load(open(f))

def median_over(seeds, fn):
    vals = [fn(load(f'belt_s{s}.json')) for s in seeds]
    return float(np.median(vals))

def main():
    seeds = [7, 8, 9]
    R = {s: load(f'belt_s{s}.json') for s in seeds}
    null = load('null_1000.json')
    out = {'null': null}
    T = np.array(R[7]['snap_years'])
    out['snap_years'] = T.tolist()
    # growth exponent of reabsorbed e-residual, 50 -> 1000 yr
    def expo(d):
        r = np.array(d['rms_resid_e']); t = np.array(d['snap_years'])
        m = (t >= 50) & (r > 0)
        return np.polyfit(np.log(t[m]), np.log(r[m]), 1)[0]
    out['resid_e_growth_exponent'] = {s: expo(R[s]) for s in seeds}
    out['resid_e_growth_exponent_median'] = float(np.median([expo(R[s]) for s in seeds]))
    out['rms_resid_e_median'] = np.median(np.array([R[s]['rms_resid_e'] for s in seeds]), axis=0).tolist()
    out['rms_dv_over_v_median'] = np.median(np.array([R[s]['rms_dv_over_v'] for s in seeds]), axis=0).tolist()
    out['rms_da_resid_median'] = np.median(np.array([R[s]['rms_da_resid'] for s in seeds]), axis=0).tolist()
    # crossing rates, median over seeds
    def cr(d, key, field='rate_per_body_per_yr'):
        return d['crossing'][key][field]
    for q in ['1e-05', '0.0001', '0.001', '0.003', '0.01']:
        for tag in ['all', 'near', 'far', 'insample']:
            k = f'q={q}_{tag}'
            if k in R[7]['crossing']:
                out[f'rate_{k}'] = float(np.median([cr(R[s], k) for s in seeds]))
    out['frac_near_resonance'] = float(np.median([R[s]['crossing']['frac_near_resonance'] for s in seeds]))
    # frac crossed vs t at q=1e-3 (all, out-of-sample): reconstruct from rate*years
    # (rate = frac(final)/T_final; store frac directly too)
    for q in ['0.0001', '0.001', '0.003', '0.01']:
        fr = [R[s]['crossing'][f'q={q}_all']['frac_crossed'] for s in seeds]
        out[f'frac_crossed_final_q={q}'] = float(np.median(fr))
    # coherence
    for cell in R[7]['coherence_cells']:
        out[f'coh_{cell}'] = {kk: float(np.median([R[s]['coherence_cells'][cell][kk] for s in seeds]))
                              for kk in R[7]['coherence_cells'][cell]}
    # ===== memory verdict at 1e9 bodies =====
    N = 1e9
    yr_s = 3.156e7
    verdict = {}
    for q in ['0.0001', '0.001', '0.003', '0.01']:
        rate = out.get(f'rate_q={q}_all')
        if rate is None: continue
        per_game_second = rate / yr_s * N
        verdict[q] = dict(
            scars_per_game_second_at_1e9=per_game_second,
            scar_bytes_per_game_second_at_16B=per_game_second * 16,
            scar_bytes_per_real_second_rtf100=per_game_second * 16 * 100 / 1,  # game-s per real s = 100
            years_to_fill_4GB_at_16B=4e9 / (per_game_second * 16))
    out['verdict_1e9_16B'] = verdict
    # T*: time for frac=0.25 at q=1e-3 from residual growth (rms ~ t^p, crossing when rms ~ q)
    p = out['resid_e_growth_exponent_median']
    r = np.array(out['rms_resid_e_median']); t = np.array(T)
    # interpolate time when rms reaches 1e-3
    for q in [1e-3, 3e-3]:
        tt = np.interp(-np.log(q), -np.log(np.maximum(r, 1e-12)), np.log(t), left=np.nan, right=np.nan) if False else None
        # rms is increasing in t: find first crossing by log-log interpolation
        idx = np.where(r >= q)[0]
        if len(idx) > 0:
            i = idx[0]
            if i == 0:
                tq = t[0]
            else:
                # log-log interp between i-1, i
                lq = np.log(q)
                l1, l2 = np.log(r[i-1]), np.log(r[i])
                t1, t2 = np.log(t[i-1]), np.log(t[i])
                tq = float(np.exp(t1 + (lq - l1) * (t2 - t1) / max(l2 - l1, 1e-30)))
            out[f'T_cross_q={q:g}_yr'] = tq
    json.dump(out, open('aggregate.json', 'w'), indent=1)
    print(json.dumps({k: v for k, v in out.items() if not isinstance(v, (list, dict)) or k.startswith(('rate_', 'frac_'))}, indent=1)[:2500])
    print('verdict:', json.dumps(out.get('verdict_1e9_16B', {}), indent=1))
    print('T_cross:', out.get('T_cross_q=0.001_yr'), out.get('T_cross_q=0.003_yr'))

if __name__ == '__main__':
    main()
