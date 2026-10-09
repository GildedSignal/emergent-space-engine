#!/usr/bin/env python3
"""Frozen detector + labels + BOTH constant sets. One record: every number in the
dossier regenerates from this file (run-log.txt holds the eval loop output).

Labels (second author, run 1754):
  FAIL_pump = pump > 2.5 x local (+-0.12 in alpha) 20th-percentile baseline
  LOCK      = lockR >= 0.90, lockR = max(R_1, R_2) circular statistics on the
              conjunction phases, NO linear detrend (run 1649's detrended RMS
              was broken: it removed the circulation it should expose)
  chaos     = a_drift > 0.05 (resonance overlap; owned by the dense tier,
              excluded from pairwise counts, counted separately)
  pos       = (FAIL_pump or LOCK) and not chaos   <- what the gate must catch

Detector: FLAG iff some CF convergent p/q (q<=12, order=p-q in 1..4) has
q|alpha - p/q| < K_order. Two constant sets, both frozen from the calibration
runs only (data/calib.json, data/calib_o23.json, data/calib_e010.json;
mu=1e-3, e0 in {0.02, 0.10}):

  F1 (frozen):  pooled zero-calibration-miss fit = max gate coordinate over pos
                seeds, pooled over all three calibration runs:
                K = {1: 0.100, 2: 0.110, 3: 0.093, 4: 0.070}
                (run 1649's claim needed ONE frozen set; this is its best case)

  F2 (scaled):  K_o(mu, e0) = K_o^0 * (mu/1e-3)^(2/3) * (e0/0.02)^gamma_o,
                K^0 = max over the e0=0.02 calibration runs, gamma from the
                e0=0.10 boundary movement (zero-miss per run, per order):
                o1: 0.100 gamma 0.000   o2: 0.0696 gamma 0.278
                o3: 0.0147 gamma 1.157  o4: 0.0696 gamma 1.157 (see note)
                Note: order-4 pos evidence is 4 seeds at 13:9 inside the
                4:3-3:2 overlap zone (stragglers, not order-4 physics); K4 is
                carried for zero-miss with gamma_4 = gamma_3 as the
                conservative choice.

FP cost (what run 1649 never measured): the flagged fraction of a belt
(uniform in alpha over the run's window) that the per-conjunction tier would
own = flagged (union chaos for the dense tier), reported per run.
"""
import json, sys
import numpy as np

LOCK_THR = 0.90
K_F1 = {1: 0.100, 2: 0.110, 3: 0.093, 4: 0.070}
K0_F2 = {1: 0.100, 2: 0.0696, 3: 0.0147, 4: 0.0696}
GAMMA = {1: 0.000, 2: 0.278, 3: 1.157, 4: 1.157}
MU0, E00 = 1e-3, 0.02


def k_f2(mu, e0):
    s = (mu / MU0) ** (2.0 / 3.0)
    e = (max(e0, 1e-4) / E00)
    return {o: K0_F2[o] * s * e ** GAMMA[o] for o in K0_F2}


def load(path):
    d = json.load(open(path))
    rows = d["rows"]
    al = np.array([r["alpha"] for r in rows])
    pu = np.array([r["pump"] for r in rows])
    base = np.empty(len(al))
    for i, a in enumerate(al):
        sel = np.abs(al - a) <= 0.12
        base[i] = np.percentile(pu[sel], 20) if sel.sum() >= 8 else np.percentile(pu, 20)
    for i, r in enumerate(rows):
        r["fail"] = bool(pu[i] > 2.5 * base[i])
        r["chaos"] = bool(r["a_drift"] > 0.05)
        r["lock"] = bool(r["lockR"] >= LOCK_THR)
        r["pos"] = (r["fail"] or r["lock"]) and not r["chaos"]
    return d["meta"], al, rows


def cf_flag(a, K):
    p_km2, q_km2, p_km1, q_km1 = 0, 1, 1, 0
    x = a
    for _ in range(14):
        ai = np.floor(x)
        p = ai * p_km1 + p_km2
        q = ai * q_km1 + q_km2
        if q >= 1 and p > q and (p - q) in K and q <= 12:
            if q * abs(a - p / q) < K[p - q]:
                return True
        p_km2, q_km2 = p_km1, q_km1
        p_km1, q_km1 = p, q
        if q > 12:
            return False
        frac = x - ai
        if frac < 1e-12:
            return False
        x = 1.0 / frac
    return False


def gate_coord(a):
    """(x, order) of the convergent with the smallest x/K_F2-normalised distance,
    for tail diagnostics; order None if no convergent of order<=4 with q<=12."""
    p_km2, q_km2, p_km1, q_km1 = 0, 1, 1, 0
    x = a
    best = (9.9, None)
    for _ in range(14):
        ai = np.floor(x)
        p = ai * p_km1 + p_km2
        q = ai * q_km1 + q_km2
        if q >= 1 and p > q and (p - q) in K0_F2 and q <= 12:
            xc = q * abs(a - p / q)
            if xc < best[0]:
                best = (xc, p - q)
        p_km2, q_km2 = p_km1, q_km1
        p_km1, q_km1 = p, q
        if q > 12:
            break
        frac = x - ai
        if frac < 1e-12:
            break
        x = 1.0 / frac
    return best


def score(flag, pos):
    tp = int((flag & pos).sum()); fn = int((pos & ~flag).sum()); fp = int((flag & ~pos).sum())
    return dict(recall=tp / max(tp + fn, 1), fn=fn, fp=fp,
                flagged=float(flag.mean()), acc=float((flag == pos).mean()),
                prec=tp / max(tp + fp, 1))


def report(path):
    meta, al, rows = load(path)
    mu, e0 = meta["mu"], meta["e0"]
    K2 = k_f2(mu, e0)
    nc = [r for r in rows if not r["chaos"]]
    pos = np.array([r["pos"] for r in nc])
    f1 = np.array([cf_flag(r["alpha"], K_F1) for r in nc])
    f2 = np.array([cf_flag(r["alpha"], K2) for r in nc])
    s1, s2 = score(f1, pos), score(f2, pos)
    chaos_frac = 1 - len(nc) / len(rows)
    nlock = sum(1 for r in nc if r["lock"])
    lockonly = sum(1 for r in nc if r["lock"] and not r["fail"])
    # lock recall by F2 (the judge-validity check: lock lives inside the gate)
    lockv = np.array([r["lock"] for r in nc])
    lr = score(f2, lockv)
    # tail diagnostics around the F2 boundary (per nearest convergent)
    bins = {"in [0.5K,K)": [0, 0], "in [K,2K)": [0, 0]}
    for r in nc:
        x, o = gate_coord(r["alpha"])
        if o is None:
            continue
        ratio = x / K2[o]
        for key, (lo, hi) in [("in [0.5K,K)", (0.5, 1.0)), ("in [K,2K)", (1.0, 2.0))]:
            if lo <= ratio < hi:
                bins[key][0] += 1
                bins[key][1] += int(r["pos"])
    out = dict(mu=mu, e0=e0, n=len(rows), chaos=round(chaos_frac, 3),
               npos=int(pos.sum()), nfail=sum(r['fail'] for r in nc),
               nlock=nlock, lockonly=lockonly,
               F1={k: round(v, 3) if isinstance(v, float) else v for k, v in s1.items()},
               F2={k: round(v, 3) if isinstance(v, float) else v for k, v in s2.items()},
               lock_recall_F2=round(lr["recall"], 3),
               owned_F2=round(float((f2 | np.array([r['chaos'] for r in nc])).mean()), 3),
               tail={k: f"{v[1]}/{v[0]}" for k, v in bins.items()},
               K_eff={o: round(K2[o], 4) for o in sorted(K2)})
    print(path)
    print(json.dumps(out, sort_keys=False))
    return out


if __name__ == "__main__":
    for p in sys.argv[1:]:
        report(p)
