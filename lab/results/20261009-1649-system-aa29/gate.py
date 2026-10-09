#!/usr/bin/env python3
"""Calibrate (on calib.json only) or evaluate (held-out) the one-pass CF gate.

Label FAIL = the truth's secular e-pump exceeds a local floor: the orbit-averaged
layer (flat in e for a coplanar circular external perturber) misses behaviour the
player would see. Floor = 2.5x a rolling median (window +-0.05 in alpha) of pump
over deep off-resonance seeds (dN1 > 20) only.
Detector FLAG = nearest-convergent detuning below delta_crit, in one of two width
normalisations. Calibration picks (normalisation, delta_crit); it is then frozen.
"""
import json, sys
import numpy as np


def load(path):
    d = json.load(open(path))
    rows = d["rows"]
    al = np.array([r["alpha"] for r in rows])
    pu = np.array([r["pump"] for r in rows])
    d1 = np.array([r["dN1"] if r["dN1"] is not None else np.inf for r in rows])
    d2 = np.array([r["dN2"] if r["dN2"] is not None else np.inf for r in rows])
    ad = np.array([r["a_drift"] for r in rows])
    return d, al, pu, d1, d2, ad


def labels(al, pu, d1):
    """Local floor from deep off-resonance seeds; FAIL label and its margin."""
    off = d1 > 20.0
    order = np.argsort(al)
    floor = np.full(len(al), np.nan)
    w = 0.05
    als, pus = al[off], pu[off]
    if len(als) < 5:
        floor[:] = 2.5 * np.median(pu)
    else:
        for i, a in enumerate(al):
            sel = np.abs(als - a) <= w
            med = np.median(pus[sel]) if sel.sum() >= 3 else np.median(pus)
            floor[i] = 2.5 * med
    fail = pu > floor
    margin = pu / floor
    return floor, fail, margin


def agreement(fail, dval, crit):
    flag = dval < crit
    return float((flag == fail).mean()), flag


def calibrate(path):
    _, al, pu, d1, d2, ad = load(path)
    _, fail, margin = labels(al, pu, d1)
    best = None
    for name, dval in (("N1_mu23", d1), ("N2_sqrtmue", d2)):
        for crit in np.arange(1.0, 20.01, 0.25):
            acc, flag = agreement(fail, dval, crit)
            # margin: worst seed inside the correct side
            if best is None or acc > best["acc"]:
                best = dict(norm=name, crit=float(crit), acc=acc,
                            nfail=int(fail.sum()), n=int(len(fail)))
    frozen = dict(norm=best["norm"], crit=best["crit"], floor_k=2.5, floor_win=0.05,
                  off_delta=20.0, calib=path, calib_acc=best["acc"])
    json.dump(frozen, open("frozen.json", "w"), indent=1)
    # report the confusion and boundary for both norms at the chosen crit
    print(json.dumps(best))
    for name, dval in (("N1_mu23", d1), ("N2_sqrtmue", d2)):
        acc, flag = agreement(fail, dval, best["crit"])
        fp = int((flag & ~fail).sum()); fn = int((~flag & fail).sum())
        print(f"{name} crit={best['crit']:.2f}: acc={acc:.4f} falsepos={fp} falseneg={fn} "
              f"FAIL seeds={int(fail.sum())}/{len(fail)}")
    # where do disagreements live
    acc, flag = agreement(fail, d1 if best['norm'] == 'N1_mu23' else d2, best['crit'])
    dis = np.where(flag != fail)[0]
    for i in dis[:12]:
        print(f"  disagree alpha={al[i]:.4f} pump={pu[i]:.4f} margin={margin[i]:.2f} dN1={d1[i]:.1f}")
    return frozen


def evaluate(path, frozen):
    meta, al, pu, d1, d2, ad = load(path)
    floor, fail, margin = labels(al, pu, d1)
    dval = d1 if frozen["norm"] == "N1_mu23" else d2
    acc, flag = agreement(fail, dval, frozen["crit"])
    fp = np.where(flag & ~fail)[0]; fn = np.where(~flag & fail)[0]
    out = dict(mu=meta["meta"]["mu"], e0=meta["meta"]["e0"], T=meta["meta"]["T"],
               acc=acc, n=len(fail), nfail=int(fail.sum()),
               falsepos=int(len(fp)), falseneg=int(len(fn)))
    print(json.dumps(out))
    for i in list(fp[:6]) + list(fn[:6]):
        print(f"  {'FP' if i in list(fp) else 'FN'} alpha={al[i]:.4f} pump={pu[i]:.4f} "
              f"floor={floor[i]:.4f} dN1={d1[i]:.1f} adrift={ad[i]:.1e}")
    # per-resonance breakdown
    for p, q in ((4,3),(3,2),(5,3),(7,4),(2,1)):
        sel = (np.abs(al - p/q) < 0.06)
        if sel.sum():
            print(f"  near {p}:{q}: n={sel.sum()} FAIL={int(fail[sel].sum())} "
                  f"FLAG={int(flag[sel].sum())} maxpump={pu[sel].max():.3f}")
    return out


if __name__ == "__main__":
    if sys.argv[1] == "calibrate":
        calibrate(sys.argv[2])
    else:
        evaluate(sys.argv[2], json.load(open("frozen.json")))
