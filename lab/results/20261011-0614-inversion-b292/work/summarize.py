import json, glob, os

base = os.path.dirname(os.path.abspath(__file__))
rows = []
for f in sorted(glob.glob(os.path.join(base, "invert-*.jsonl"))):
    d = json.load(open(f))
    rows.append(d)
    r, w, m = d["ranks"], d["watch"], d["method"]
    ran = m["s"] > 0.005 or m["pairs"] > 0
    miss = f"{m['missed']}/{d['enc']}" if ran else "n/a (not run)"
    print(
        f"{d['scene']:20s} enc={d['enc']:5d} dmax={r['dist']['max']:3d} thmax={r['true']['max']:3d} "
        f"lb_max={r['lbar']['max']:4d} lb_p50={r['lbar']['p50']:4d} lb_p90={r['lbar']['p90']:4d} "
        f"lb_gt4={r['lbar']['gt4_frac']:.3f} lbwin={d['window']['lb_max']:.2e} "
        f"sviol={d['window']['sound_viol_max']:+.1e} 2tviol={d['window']['twoterm_viol_max']:+.1e} "
        f"k={w['k_hat']:6.1f} fracQ={w['frac_quad']:.3f} meth_miss={miss}"
    )

print("\nscaling (k_hat/n_c vs 8*mean_amp/spread):")
for d in rows:
    if d["sig_lam"] > 0:
        print(f"  {d['scene']:20s} sig_e={d['sig_e']:.0e} sig_lam={d['sig_lam']:.3f} "
              f"k/n_c={d['watch']['k_hat']/d['nc']:.3f} lb_max={d['ranks']['lbar']['max']}")
