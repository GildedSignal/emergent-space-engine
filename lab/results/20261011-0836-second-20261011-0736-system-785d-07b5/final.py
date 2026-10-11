"""Regenerate final.json from the shipped record (second-author run 20261011-0836).

Chain: probe.py quad / calib / scan  ->  analyze.py (metrics.json)  ->  final.py.
Every number in final.json is recomputed here from quad.json + the scan npys +
metrics.json.  Run: python3 final.py   (writes final.json, prints a diff against
work/orig/final.json — the author's shipped file — when present.)

Definitions (recovered and verified against the author's numbers):
  c_H[j]        = mean over mu of (median band at exact resonance / mu^(1/3));
                  cH_spread[j] = the per-mu values.
  capped_law    = over circulating systems (|theta_net| > 2 pi), per system
                  F = band / min(2 pdot_coh/|thdot|, c_H mu^(1/3)); n, med,
                  p10, p90, frac in [0.3, 3]; ALL pools the five cases.
  P4a_violations= len(metrics.json's list) (truth failed where uncapped
                  excursion < q_e/2).
  kappa_q0.0096 = median T_fail / (q_e/pdot_coh) at exact resonance,
                  q_e = qgrid[5] (= 0.0095654), rounded to 2 decimals.
  W_derived     = full width 2*d(P1/P2) at the crossing delta* where the
                  uncapped excursion 2 pdot/|thdot| equals the cap
                  c_H mu^(1/3) (linear interpolation of pdot, thdot on the
                  quad dgrid, bisection); d(P1/P2) = 1.5 * (j/(j+1)) * delta.
                  CORRECTION vs the author's final.json: the j2_mu0.0003 entry
                  there (0.0229) reproduces only with the 2:1 conversion factor
                  1.5*0.5 (gives 0.0228); with the 3:2 factor 1.5*(2/3) the
                  value is 0.0305.  The corrected value is written and the
                  original recorded in regen_notes.
  regime_boundary = measured (outermost |delta| with circ_frac <= 0.5) /
                  predicted (delta*), for cases with delta* inside the grid.
"""
import json, os
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))
NSEED = 8
CASES = [("j1", 1, 3e-4), ("j1", 1, 1e-3), ("j1", 1, 3e-3), ("j2", 2, 3e-4), ("j2", 2, 1e-3)]
HELD_OUT = [("j1", 1, 3e-4), ("j1", 1, 3e-3), ("j2", 2, 3e-4), ("j2", 2, 1e-3)]

quad = json.load(open(OUT + "/quad.json"))
metrics = json.load(open(OUT + "/metrics.json"))
scans = {}
for tag, j, mu in CASES:
    scans["%s_mu%g" % (tag, mu)] = np.load(
        OUT + "/scan-%s-mu%g.npy" % (tag, mu), allow_pickle=True).item()


def crossing_dstar(key, j, mu, cap):
    """delta* where interp(2 pdot/|thdot|) = cap, positive side, bisection."""
    q = quad[key]
    dg = sorted(float(k) for k in q if k[0] in "+-")
    ex = {d: q["%+.5f" % d] for d in dg}
    def exc(d):
        if d in ex:
            v = ex[d]
        else:
            lo = max(x for x in dg if x < d); hi = min(x for x in dg if x > d)
            f = (d - lo) / (hi - lo)
            v = {k: ex[lo][k] + f * (ex[hi][k] - ex[lo][k]) for k in ("pdot_coh", "thdot")}
        return 2 * v["pdot_coh"] / abs(v["thdot"])
    lo, hi = 0.0, max(dg)
    if (exc(hi) - cap) * (exc(lo) - cap) > 0:
        return hi  # crossing beyond the grid
    for _ in range(80):
        mid = (lo + hi) / 2
        if (exc(mid) - cap) * (exc(lo) - cap) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


# ---- c_H from the exact-resonance column (median band / mu^(1/3)), mean over mu
cH, cH_spread = {}, {}
for tag in ("j1", "j2"):
    vals = []
    for t, j, mu in CASES:
        if t != tag:
            continue
        S = scans["%s_mu%g" % (tag, mu)]
        dgrid = np.array(S["dgrid"]); band = np.array(S["band"])
        i0 = len(dgrid) // 2
        vals.append(float(np.median(band[i0 * NSEED:(i0 + 1) * NSEED])) / mu ** (1 / 3.))
    cH[tag] = float(np.mean(vals)); cH_spread[tag] = vals

# ---- capped law
capped, allF, heldF = {}, [], []
for tag, j, mu in CASES:
    S = scans["%s_mu%g" % (tag, mu)]
    q = quad["j%d_mu%g" % (j, mu)]
    dgrid = np.array(S["dgrid"]); band = np.array(S["band"])
    thnet = np.array(S["theta_net"])
    cap = cH[tag] * mu ** (1 / 3.)
    Fs = []
    for i, d in enumerate(dgrid):
        v = q["%+.5f" % d]
        exc = 2 * v["pdot_coh"] / abs(v["thdot"]) if v["thdot"] != 0 else np.inf
        sl = slice(i * NSEED, (i + 1) * NSEED)
        circ = np.abs(thnet[sl]) > 2 * np.pi
        Fs.extend((band[sl][circ] / min(exc, cap)).tolist())
    Fs = np.array(Fs); allF.extend(Fs.tolist())
    if (tag, j, mu) in HELD_OUT:
        heldF.extend(Fs.tolist())
    capped["%s_mu%g" % (tag, mu)] = {
        "n": int(Fs.size), "med": float(np.median(Fs)),
        "p10": float(np.percentile(Fs, 10)), "p90": float(np.percentile(Fs, 90)),
        "frac_in_0.3_3": float(np.mean((Fs >= 0.3) & (Fs <= 3)))}

def stats(F):
    F = np.array(F)
    return {"n": int(F.size), "med": float(np.median(F)),
            "p10": float(np.percentile(F, 10)), "p90": float(np.percentile(F, 90)),
            "frac_in_0.3_3": float(np.mean((F >= 0.3) & (F <= 3)))}

capped["ALL"] = stats(allF)

# ---- P4a (from analyze.py's own computation, uncapped excursion < q_e/2)
P4a = len(metrics["P4a_violations"])

# ---- kappa at qgrid[5]
kappa = {}
for tag, j, mu in CASES:
    S = scans["%s_mu%g" % (tag, mu)]
    q = quad["j%d_mu%g" % (j, mu)]
    dgrid = np.array(S["dgrid"]); Tage = np.array(S["Tage"]); qgrid = np.array(S["qgrid"])
    i0 = len(dgrid) // 2
    pdot0 = q["%+.5f" % dgrid[i0]]["pdot_coh"]
    tf = Tage[5, i0 * NSEED:(i0 + 1) * NSEED]; tf = tf[tf > 0]
    kappa["%s_mu%g" % (tag, mu)] = round(float(np.median(tf) / (qgrid[5] / pdot0)), 2)

# ---- W crossing, correct per-family conversion
W = {}
for tag, j, mu in CASES:
    cap = cH[tag] * mu ** (1 / 3.)
    dstar = crossing_dstar("j%d_mu%g" % (j, mu), j, mu, cap)
    if dstar >= 0.0319:      # crossing beyond the scanned grid: no entry (as shipped)
        continue
    W["%s_mu%g" % (tag, mu)] = [round(2 * 1.5 * (j / (j + 1.0)) * dstar, 4),
                                round(2.5 * mu ** (2 / 3.), 4)]

# ---- regime boundary: measured outermost |d| with circ_frac <= 0.5, over delta*
boundary = {}
for tag, j, mu in CASES:
    cap = cH[tag] * mu ** (1 / 3.)
    dstar = crossing_dstar("j%d_mu%g" % (j, mu), j, mu, cap)
    if dstar >= 0.0319:
        continue
    S = scans["%s_mu%g" % (tag, mu)]
    dgrid = np.array(S["dgrid"]); thnet = np.array(S["theta_net"])
    meas = 0.0
    for i, d in enumerate(dgrid):
        sl = slice(i * NSEED, (i + 1) * NSEED)
        if np.mean(np.abs(thnet[sl]) > 2 * np.pi) <= 0.5 and abs(d) > meas:
            meas = abs(d)
    boundary["%s_mu%g" % (tag, mu)] = round(meas / dstar, 2)

final = {"c_H": cH, "cH_spread": cH_spread, "capped_law": capped,
         "P4a_violations": P4a, "kappa_q0.0096": kappa,
         "W_derived_vs_convention": W, "regime_boundary_meas_over_pred": boundary,
         "capped_law_held_out_only": stats(heldF),
         "regen_notes": [
             "Regenerated by final.py from quad.json + scan npys + metrics.json "
             "(author's final.json had no generating script).",
             "W j2_mu0.0003 corrected: author's 0.0229 reproduces only with the 2:1 "
             "conversion 1.5*0.5 (gives 0.0228); with the 3:2 conversion 1.5*(2/3) "
             "it is 0.0305 (2.7x B17's 0.0112, not ~2x).",
             "capped_law_held_out_only added: the shipped ALL (n=327, 99.39%) includes "
             "the calibration case j1 mu=1e-3."]}

json.dump(final, open(OUT + "/final.json", "w"), indent=1)

# ---- diff against the author's shipped file
orig = OUT + "/work/orig/final.json"
if os.path.exists(orig):
    o = json.load(open(orig))
    diffs = []
    for k in ("c_H", "cH_spread", "P4a_violations", "kappa_q0.0096",
              "regime_boundary_meas_over_pred"):
        if final[k] != o.get(k):
            diffs.append((k, final[k], o.get(k)))
    for k, v in final["capped_law"].items():
        if k in o.get("capped_law", {}) and v != o["capped_law"][k]:
            diffs.append(("capped_law." + k, v, o["capped_law"][k]))
    for k, v in final["W_derived_vs_convention"].items():
        if k in o.get("W_derived_vs_convention", {}) and v != o["W_derived_vs_convention"][k]:
            diffs.append(("W." + k, v, o["W_derived_vs_convention"][k]))
    print("diff vs shipped final.json:", diffs if diffs else "NONE")
    print("held-out-only capped law:", final["capped_law_held_out_only"])
print("final.json regenerated")
