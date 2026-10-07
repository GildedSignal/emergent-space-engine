#!/usr/bin/env python3
"""Aggregate the B18b-sampler decisive runs with the checker's relabels applied.

Label fixes vs the original run's dossier:
  (a) per-body median first-cross (crossing.q.median_first_cross_yr), not the aggregate's
      RMS-reaches-q time (T_cross), is what 'median first-cross' may name;
  (b) the 4 GB fill time is quoted at the rate it is computed from: the early peak rate
      (frac(t=20 yr)/20 yr) and the long-run rate (frac(T=1000)/1000), separately;
  (c) the outer-edge |dv| multiple is recomputed from the stored dv_profile bins.
"""
import json
import numpy as np

SEEDS = [7, 8, 9]
N9 = 1e9
YR_S = 3.156e7
def med(v):
    v = [x for x in v if x is not None]
    return float(np.median(v)) if v else None

def scene_stats(tag, files):
    R = {s: json.load(open(files[s])) for s in SEEDS}
    out = {'files': files}
    T = np.array(R[7]['frac_crossed_vs_t']['q=0.001']['t'])
    out['snap_years'] = T.tolist()
    # growth exponent of reabsorbed e-residual, 50 -> 1000 yr
    def expo(d):
        r = np.array(d['rms_resid_e']); t = np.array(d['snap_years'])
        m = (t >= 50) & (r > 0)
        return float(np.polyfit(np.log(t[m]), np.log(r[m]), 1)[0])
    out['resid_e_growth_exponent'] = {s: expo(R[s]) for s in SEEDS}
    out['resid_e_growth_exponent_median'] = med([expo(R[s]) for s in SEEDS])
    # long-run crossing rate and per-body median first-cross (label a)
    for qk, q in [('0.001', 1e-3), ('0.003', 3e-3)]:
        out[f'rate_q={qk}_longrun'] = med([R[s]['crossing'][f'q={qk}_all']['rate_per_body_per_yr'] for s in SEEDS])
        out[f'frac_crossed_final_q={qk}'] = med([R[s]['crossing'][f'q={qk}_all']['frac_crossed'] for s in SEEDS])
        out[f'median_first_cross_yr_q={qk}'] = med([R[s]['crossing'][f'q={qk}']['median_first_cross_yr'] for s in SEEDS])
        out[f'median_first_cross_yr_q={qk}_by_seed'] = {s: R[s]['crossing'][f'q={qk}']['median_first_cross_yr'] for s in SEEDS}
    # T*: first t with out-of-sample crossed fraction >= 25% (and 10%), at q=1e-3
    for thr in [0.10, 0.25]:
        ts = []
        for s in SEEDS:
            fr = np.array(R[s]['frac_crossed_vs_t']['q=0.001']['frac_outofsample'])
            tt = T[fr >= thr]
            ts.append(float(tt[0]) if len(tt) else None)
        out[f'Tstar_frac{int(thr*100)}_q=0.001_yr'] = med([t for t in ts if t is not None]) if any(t is not None for t in ts) else None
        out[f'Tstar_frac{int(thr*100)}_q=0.001_yr_by_seed'] = ts
    # early peak rate (label b): frac crossed by t=20 yr, per year
    out['early_rate_q=0.001_per_yr'] = med([R[s]['frac_crossed_vs_t']['q=0.001']['frac_outofsample'][5] / 20.0 for s in SEEDS])
    out['session_lag_frac2yr_q=0.001'] = med([R[s]['frac_crossed_vs_t']['q=0.001']['frac_outofsample'][1] for s in SEEDS])
    # fit-noise control
    out['fitnoise_ratio_insample_over_oos_q=0.001'] = med(
        [R[s]['crossing']['q=0.001_insample']['frac_crossed'] / R[s]['crossing']['q=0.001_all']['frac_crossed'] for s in SEEDS])
    # resonance split (b17 only; b16 has no windows)
    if 'near' in str(R[7]['crossing']):
        out['frac_near_resonance'] = med([R[s]['crossing']['frac_near_resonance'] for s in SEEDS])
        for qk in ['0.003', '0.01']:
            k = f'q={qk}_near'
            if k in R[7]['crossing'] and f'q={qk}_far' in R[7]['crossing']:
                out[f'rate_ratio_near_over_far_q={qk}'] = med(
                    [R[s]['crossing'][k]['rate_per_body_per_yr'] / R[s]['crossing'][f'q={qk}_far']['rate_per_body_per_yr'] for s in SEEDS])
    # dv profile: max/min bin multiple in median |dv| (label c), and the p99
    prof = R[7]['dv_profile_by_a']
    meds = [p['med_dv'] for p in prof]
    out['dv_med_profile_max_over_min'] = float(max(meds) / min(meds))
    out['dv_profile_extremes'] = dict(
        max_bin=[prof[int(np.argmax(meds))]['a_lo'], prof[int(np.argmax(meds))]['a_hi']],
        min_bin=[prof[int(np.argmin(meds))]['a_lo'], prof[int(np.argmin(meds))]['a_hi']])
    # coherence at the coarse cell
    for cell in R[7]['coherence_cells']:
        out[f'coh_{cell}'] = {kk: med([R[s]['coherence_cells'][cell][kk] for s in SEEDS])
                              for kk in R[7]['coherence_cells'][cell]}
    # ---- memory verdict at 1e9, honest labels (label b) ----
    verdict = {}
    for name, rate in [('longrun_q=0.001', out['rate_q=0.001_longrun']),
                       ('early_peak_q=0.001', out['early_rate_q=0.001_per_yr'])]:
        b_gs = rate / YR_S * N9 * 16
        verdict[name] = dict(
            rate_per_body_per_yr=rate,
            scar_bytes_per_game_second_at_1e9_16B=b_gs,
            scar_bytes_per_real_second_rtf100=b_gs * 100,
            game_years_to_fill_4GB=4e9 / b_gs / YR_S)
    out['verdict_1e9_16B'] = verdict
    return out

def main():
    agg = {}
    agg['b16'] = scene_stats('b16', {s: f'b16_s{s}.json' for s in SEEDS})
    agg['b17'] = scene_stats('b17', {s: f'b17_s{s}.json' for s in SEEDS})
    # original scene relabels, straight off the shipped record (no rerun)
    orig = {}
    Ro = {s: json.load(open(f'orig/belt_s{s}.json')) for s in SEEDS}
    orig['median_first_cross_yr_q=0.001'] = med([Ro[s]['crossing']['q=0.001']['median_first_cross_yr'] for s in SEEDS])
    orig['median_first_cross_yr_q=0.003'] = med([Ro[s]['crossing']['q=0.003']['median_first_cross_yr'] for s in SEEDS])
    Ao = json.load(open('orig/aggregate.json'))
    orig['T_cross_RMS_reaches_q_yr'] = dict(q3=Ao['T_cross_q=0.003_yr'], q1=Ao['T_cross_q=0.001_yr'])
    orig['rate_q=0.001_longrun'] = Ao['rate_q=0.001_all']
    # honest fill arithmetic on the original numbers
    for name, rate in [('longrun_q=0.001', Ao['rate_q=0.001_all']),
                       ('early_peak_q=0.001', 3.7e-2)]:
        b_gs = rate / YR_S * N9 * 16
        orig.setdefault('verdict_1e9_16B', {})[name] = dict(
            rate_per_body_per_yr=rate, scar_bytes_per_game_second_at_1e9_16B=b_gs,
            scar_bytes_per_real_second_rtf100=b_gs * 100, game_years_to_fill_4GB=4e9 / b_gs / YR_S)
    prof = Ro[7]['dv_profile_by_a']
    meds = [p['med_dv'] for p in prof]
    orig['dv_med_profile_max_over_min'] = float(max(meds) / min(meds))
    orig['dv_profile_extremes'] = dict(
        max_bin=[prof[int(np.argmax(meds))]['a_lo'], prof[int(np.argmax(meds))]['a_hi']],
        min_bin=[prof[int(np.argmin(meds))]['a_lo'], prof[int(np.argmin(meds))]['a_hi']])
    # q-insensitivity (checker's missed point): raw (unrefit) crossed fraction at each q
    orig['crossing_raw_frac_s7'] = Ro[7]['crossing_raw_frac']
    agg['orig_relabeled'] = orig
    json.dump(agg, open('aggregate2.json', 'w'), indent=1)
    for tag in ['b16', 'b17', 'orig_relabeled']:
        print(f'== {tag} ==')
        print(json.dumps({k: v for k, v in agg[tag].items()
                          if not isinstance(v, (list, dict)) or k.startswith(('rate_', 'Tstar', 'median_first'))}, indent=1))

if __name__ == '__main__':
    main()
