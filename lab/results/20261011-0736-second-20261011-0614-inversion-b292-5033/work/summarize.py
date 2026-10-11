import json, glob, os

base = os.path.dirname(os.path.abspath(__file__))
rows = []
for f in sorted(glob.glob(os.path.join(base, "invert-*.jsonl"))):
    rows.append(json.load(open(f)))

print(f"{'scene':22s} {'enc':>5s} {'dmax':>4s} {'thmax':>5s} | {'raw_max':>7s} {'raw_p90':>7s} {'raw_gt4':>7s} | {'MOD_max':>7s} {'MOD_p90':>7s} {'MOD_gt4':>7s} | {'k_hat':>6s} {'k/n_c':>6s} {'fracQ':>6s} | meth_miss")
for d in rows:
    r, w, m = d["ranks"], d["watch"], d["method"]
    ran = m["s"] > 0.005 or m["pairs"] > 0
    miss = f"{m['missed']}/{d['enc']}" if ran else "--"
    print(
        f"{d['scene']:22s} {d['enc']:5d} {r['dist']['max']:4d} {r['true']['max']:5d} | "
        f"{r['lbar']['max']:7d} {r['lbar']['p90']:7d} {r['lbar']['gt4_frac']:7.3f} | "
        f"{r['lbar_mod']['max']:7d} {r['lbar_mod']['p90']:7d} {r['lbar_mod']['gt4_frac']:7.3f} | "
        f"{w['k_hat']:6.1f} {w['k_hat']/d['nc']:6.3f} {w['frac_quad']:6.3f} | {miss}"
    )

print("\nwindow soundness (all must be < 0) and worst samples:")
for d in rows:
    ws = d["window"]
    print(f"  {d['scene']:22s} lbwin={ws['lb_max']:.2e} sound_viol={ws['sound_viol_max']:+.1e} 2term_viol={ws['twoterm_viol_max']:+.1e} worst={d['worst'][0] if d['worst'] else None}")
