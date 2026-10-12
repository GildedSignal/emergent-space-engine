#!/usr/bin/env python3
"""Score the pre-registered predictions from a run's JSON."""
import json, sys
import numpy as np

def load(tag):
    with open(f"{tag}.json") as f:
        return json.load(f)

def spearman(x, y):
    rx = np.argsort(np.argsort(x)); ry = np.argsort(np.argsort(y))
    return float(np.corrcoef(rx, ry)[0, 1])

def analyse(tag="m1m"):
    r = load(tag)
    B = r["bodies"]; q = r["qstats"]; ql = r["qlist"]
    lam = np.array([b["lam"] for b in B])
    dres = np.array([b["d_res"] for b in B])
    slope = np.array([b["msd_slope"] for b in B])
    am = np.array([b["a_mean"] for b in B])
    rev = {k: np.array([s["revisit"] for s in q[k]]) for k in ql}
    churn = {k: np.array([s["churn"] for s in q[k]]) for k in ql}
    distinct = {k: np.array([s["distinct2"] for s in q[k]]) for k in ql}
    floor = r["lam_floor"]
    rep = {}
    rep["config"] = dict(mu=r["mu"], T=r["T"], N=r["N"], e0=r["e0"], wall=r["wall"], lam_floor=floor)
    # P2 bimodality at 1e-4
    rv = rev["1e-04"]
    rep["P2"] = dict(n=int(rv.size),
                     frac_reg=int((rv > 0.8).sum()), frac_cha=int((rv < 0.05).sum()),
                     frac_mid=float(((rv >= 0.05) & (rv <= 0.8)).mean()))
    # P3 resonance web
    chaotic = (rv < 0.05) | (lam >= floor / 2)
    rep["P3"] = dict(chaotic_frac=float(chaotic.mean()),
                     p_chaotic_given_dres_lt_01=float(chaotic[dres < 0.01].mean()) if (dres < 0.01).any() else None,
                     p_reg_given_dres_gt_03=float((~chaotic[dres > 0.03]).mean()) if (dres > 0.03).any() else None,
                     coorb_chaotic=float(chaotic[np.abs(am - 1) < 0.12].mean()) if (np.abs(am - 1) < 0.12).any() else None,
                     interior_chaotic=float(chaotic[(am > 0.55) & (am < 0.60)].mean()))
    # P4 collapse quantum vs element range
    arange = np.array([b["a_range"] for b in B])
    rel_range = arange / am
    regular = rv > 0.8
    rep["P4"] = dict(frac_churn_gt_half={k: float((churn[k] >= 0.5).mean()) for k in ql},
                     median_rel_range_regular=float(np.median(rel_range[regular])) if regular.any() else None,
                     frac_reg_with_range_gt_3q=float((rel_range[regular] > 3e-4).mean()) if regular.any() else None)
    # P5 concentration
    tot = {k: distinct[k].sum() for k in ql}
    top5 = {}
    for k in ql:
        d = distinct[k]; s = np.sort(d)[::-1]
        k5 = max(int(np.ceil(0.05 * d.size)), 1)
        top5[k] = float(s[:k5].sum() / d.sum())
    rep["P5"] = dict(top5_share=top5)
    # P6 correlations
    rep["P6"] = dict(spearman_lam_churn_1e4=spearman(lam, churn["1e-04"]),
                     spearman_dres_churn_1e4=spearman(dres, churn["1e-04"]),
                     spearman_lam_rev_1e4=spearman(lam, rv))
    # P7 agreement
    diff = slope > 0.7; bounded = slope < 0.3
    ok = 0; n = 0
    ok += int((rv[diff] < 0.05).sum()); n += int(diff.sum())
    ok += int((rv[bounded] > 0.8).sum()); n += int(bounded.sum())
    rep["P7"] = dict(agreement=ok / max(n, 1), n_diff=int(diff.sum()), n_bounded=int(bounded.sum()))
    # extra: regime table by a bins
    bins = np.linspace(0.55, 1.9, 14)
    tab = []
    for i in range(len(bins) - 1):
        m = (am >= bins[i]) & (am < bins[i + 1])
        if m.sum():
            tab.append(dict(a=float(bins[i]), n=int(m.sum()), chaotic=float(chaotic[m].mean()),
                            rev_med=float(np.median(rv[m])), churn_med_1e4=float(np.median(churn["1e-04"][m])),
                            churn_med_1e6=float(np.median(churn["1e-06"][m]))))
    rep["a_table"] = tab
    return rep

if __name__ == "__main__":
    tag = sys.argv[1] if len(sys.argv) > 1 else "m1m"
    rep = analyse(tag)
    print(json.dumps(rep, indent=1))
    with open(f"analysis-{tag}.json", "w") as f:
        json.dump(rep, f, indent=1)
