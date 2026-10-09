#!/usr/bin/env python3
"""Frozen detector + FAIL labelling, and the rival normalisation.

FAIL (behaviour the averaged layer misses): truth's secular e-pump > 2.5x a local
baseline (rolling 20th percentile of pump over +-0.12 in alpha).

Detector (one CF pass): FLAG iff some convergent p/q (q<=12, order=p-q<=4) has
q*|alpha - p/q| < K_order. K frozen from the calibration sweep only:
  order 1: 0.11  (2:1 inner-flank boundary, the widest of 4:3/3:2/2:1)
  order 2: 0.035 (5:3 bump boundary)
  order 3: 0.012, order 4: 0.008 (no order>=3 FAIL observed in calibration;
                                   set just below the smallest observed q*d of
                                   those orders' nearest approaches)
Rival (B17's W scaling): same predicate with K_order * (mu/1e-3)^(2/3).
"""
import json, sys
import numpy as np

K = {1: 0.11, 2: 0.035, 3: 0.012, 4: 0.008}


def load(path):
    d = json.load(open(path))
    rows = d["rows"]
    return (d["meta"],
            np.array([r["alpha"] for r in rows]),
            np.array([r["pump"] for r in rows]),
            np.array([r["a_drift"] for r in rows]),
            [r for r in rows])


def flag_plain(al, rows):
    """FLAG from every convergent stored per seed is not enough (only nearest
    kept), so recompute convergents here - one pass, same as sim.delta_table."""
    out = np.zeros(len(al), dtype=bool)
    for i, a in enumerate(al):
        p_km2, q_km2, p_km1, q_km1 = 0, 1, 1, 0
        x, out_i = a, False
        for _ in range(14):
            ai = np.floor(x)
            p = ai * p_km1 + p_km2
            q = ai * q_km1 + q_km2
            if q >= 1 and p > q and (p - q) in K and q <= 12:
                if q * abs(a - p / q) < K[p - q]:
                    out_i = True
                    break
            p_km2, q_km2 = p_km1, q_km1
            p_km1, q_km1 = p, q
            if q > 12:
                break
            frac = x - ai
            if frac < 1e-12:
                break
            x = 1.0 / frac
        out[i] = out_i
    return out


def labels(al, pu):
    base = np.empty(len(al))
    for i, a in enumerate(al):
        sel = np.abs(al - a) <= 0.12
        base[i] = np.percentile(pu[sel], 20) if sel.sum() >= 8 else np.percentile(pu, 20)
    fail = pu > 2.5 * base
    return base, fail


def report(path, rival_mu_scale=True):
    meta, al, pu, ad, rows = load(path)
    base, fail = labels(al, pu)
    flag = flag_plain(al, rows)
    acc = float((flag == fail).mean())
    fp = np.where(flag & ~fail)[0]
    fn = np.where(~flag & fail)[0]
    res = dict(mu=meta["mu"], e0=meta["e0"], T=meta["T"], acc=acc, n=len(fail),
               nfail=int(fail.sum()), FP=int(len(fp)), FN=int(len(fn)))
    print(json.dumps(res))
    for i in list(fn[:8]) + list(fp[:8]):
        side = "FN" if i in list(fn) else "FP"
        print(f"  {side} a={al[i]:.4f} pump={pu[i]:.4f} base={base[i]:.4f} adrift={ad[i]:.1e}")
    if rival_mu_scale:
        # rival: K scaled by (mu/1e-3)^(2/3)
        s = (meta["mu"] / 1e-3) ** (2.0 / 3.0)
        if abs(s - 1.0) > 0.05:
            global K
            K0 = dict(K)
            for o in K:
                K[o] = K0[o] * s
            flag_r = flag_plain(al, rows)
            K.clear(); K.update(K0)
            print(f"  rival (mu^(2/3) scaling): acc={float((flag_r == fail).mean()):.4f} "
                  f"FP={int((flag_r & ~fail).sum())} FN={int((~flag_r & fail).sum())}")
    # overlap-zone report: FAIL seeds not flagged, are they between first-order resonances?
    if len(fn):
        print("  FN alphas:", " ".join(f"{al[i]:.3f}" for i in fn[:20]))
    return res


if __name__ == "__main__":
    for p in sys.argv[1:]:
        report(p)
