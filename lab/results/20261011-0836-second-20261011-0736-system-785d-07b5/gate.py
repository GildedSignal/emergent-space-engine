"""The certificate as the ONLY resonance gate (second-author run 20261011-0836).

The checker's named gold experiment, cheapest decisive form: wire the certificate
into the cheap path with the classifier and B17's W table DELETED.  Stand-in for
the plane's kick layer (the crates are off-limits here): outside the zone the
averaged law holds e within [e0-q_e, e0+q_e] (its own prediction, no truth
used); inside the zone the system is handed to the exact handler (the reference
integrator itself, so every behaviour mismatch is the GATE's fault — the doll's
own fidelity is r4 v3's question, not this one).

Certificate: excursion(d) = min(2 pdot_coh/|thdot(d)|, cap),  cap = c_H mu^(1/3)
with c_H re-derived per geometry from the exact-resonance column alone (median
band at d=0 / mu^(1/3); 8 seeds — the engine's one-column calibration, NOT an
analytic derivation, which stays open).
Old gate (deleted mechanism, for comparison): switch iff |d(P1/P2)| <= W (and
the W/2 variant), W = 2.5 mu^(2/3).

Miss = truth fails at quantum q_e (running-mean e leaves the tube) while the
gate keeps the system outside.  Guard form: switch at excursion >= q_e/2.

Run: python3 gate.py   (writes gate.json, prints tables)
"""
import json, os
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))
NSEED = 8
E0 = 0.02

import sys
sys.path.insert(0, OUT)
from probe import quad_cert, res_params, a_of_ratio  # noqa: E402

CASES = [("j1", 1, 3e-4, "quad.json"), ("j1", 1, 1e-3, "quad.json"),
         ("j1", 1, 3e-3, "quad.json"), ("j2", 2, 3e-4, "quad.json"),
         ("j2", 2, 1e-3, "quad.json"), ("j3", 3, 3e-4, "quad-j3.json"),
         ("j3", 3, 1e-3, "quad-j3.json")]


def excursion_of(q_ent, dgrid, cap):
    """Certificate per detuning (cheap side only)."""
    exc = {}
    for d in dgrid:
        v = q_ent["%+.5f" % d]
        p, t = v["pdot_coh"], v["thdot"]
        if p == 0.0:
            exc[d] = 0.0                      # mu=0: nothing to pump
        else:
            lin = np.inf if t == 0.0 else 2 * p / abs(t)
            exc[d] = min(lin, cap)
    return exc


out = {}
for tag, j, mu, quadfile in CASES:
    key = "%s_mu%g" % (tag, mu)
    S = np.load(OUT + "/scan-%s.npy" % key.replace("_", "-"), allow_pickle=True).item()
    quad = json.load(open(OUT + "/" + quadfile))
    q_ent = quad["j%d_mu%g" % (j, mu)]
    dgrid = np.array(S["dgrid"]); qgrid = np.array(S["qgrid"])
    Tage = np.array(S["Tage"]); band = np.array(S["band"])
    thnet = np.array(S["theta_net"])

    # per-geometry calibration: exact-resonance column only
    i0 = len(dgrid) // 2
    band0 = float(np.median(band[i0 * NSEED:(i0 + 1) * NSEED]))
    cap = band0                      # = cH_case * mu^(1/3) by construction
    cH_case = band0 / mu ** (1 / 3.)

    exc = excursion_of(q_ent, dgrid, cap)
    pr = j / (j + 1.0)               # P1/P2 at exact resonance
    W = 2.5 * mu ** (2 / 3.)         # B17's convention
    dW = W / (1.5 * pr)              # zone edge in delta units, |d(P1/P2)| <= W
    oldW = np.array([abs(1.5 * pr * d) <= W for d in dgrid])       # per delta
    oldWhalf = np.array([abs(1.5 * pr * d) <= W / 2 for d in dgrid])

    q_stats = []
    tot = {"miss_switch": 0, "miss_guard": 0, "miss_oldW": 0, "miss_oldWhalf": 0,
           "n_fail": 0, "worst_sev": 0.0, "worst_at": None, "regime_miss_switch": 0,
           "n_librate": 0}
    for qi, q in enumerate(qgrid):
        row = {"q": float(q)}
        ms = mg = mo = mo2 = nf = 0
        sev = 0.0; worst = None
        rms = 0
        for i, d in enumerate(dgrid):
            sl = slice(i * NSEED, (i + 1) * NSEED)
            fail = Tage[qi, sl] > 0
            nf += int(fail.sum())
            sw = exc[d] >= q
            gw = exc[d] >= q / 2
            ow = oldW[i]; ow2 = oldWhalf[i]
            lib = np.abs(thnet[sl]) <= 2 * np.pi
            rms += int((lib & ~np.broadcast_to(sw, lib.shape)).sum())
            for s in np.nonzero(fail)[0]:
                if not sw:
                    ms += 1
                    ssev = band[sl][s] / 2 - q
                    if ssev > sev:
                        sev, worst = ssev, (float(d), int(s), float(band[sl][s]))
                if not gw:
                    mg += 1
                if not ow:
                    mo += 1
                if not ow2:
                    mo2 += 1
        row.update({"n_fail": nf, "miss_switch": ms, "miss_guard": mg,
                    "miss_oldW": mo, "miss_oldWhalf": mo2,
                    "dollfrac_cert": float(np.mean([exc[d] >= q for d in dgrid])),
                    "dollfrac_oldW": float(oldW.mean()), "dollfrac_oldWhalf": float(oldWhalf.mean()),
                    "max_sev_switch": float(sev)})
        q_stats.append(row)
        tot["miss_switch"] += ms; tot["miss_guard"] += mg
        tot["miss_oldW"] += mo; tot["miss_oldWhalf"] += mo2; tot["n_fail"] += nf
        tot["regime_miss_switch"] += rms
        if sev > tot["worst_sev"]:
            tot["worst_sev"], tot["worst_at"] = sev, worst
    tot["n_librate"] = int((np.abs(thnet) <= 2 * np.pi).sum())
    out[key] = {"cH_calib": cH_case, "cap": cap, "W": W, "dW": dW,
                "q_stats": q_stats, "totals": tot}
    print("\n=== %s  cH_calib=%.3f cap=%.4f  W(conv)=%.4f (dW=%.4f)" % (key, cH_case, cap, W, dW))
    print("  q      nfail  MISScert MISSguard MISSoldW MISSoldW/2  doll%  oldW%  worstsev")
    for r in q_stats:
        print("  %.4f  %4d   %5d   %5d    %5d    %5d      %.2f  %.2f   %.4f" %
              (r["q"], r["n_fail"], r["miss_switch"], r["miss_guard"], r["miss_oldW"],
               r["miss_oldWhalf"], r["dollfrac_cert"], r["dollfrac_oldW"], r["max_sev_switch"]))
    print("  totals: fail=%d miss_cert=%d miss_guard=%d miss_oldW=%d miss_oldW/2=%d" %
          (tot["n_fail"], tot["miss_switch"], tot["miss_guard"], tot["miss_oldW"], tot["miss_oldWhalf"]))
    print("  regime: librating systems=%d, librating-kept-outside pairs=%d, worst (d,seed,band)=%s" %
          (tot["n_librate"], tot["regime_miss_switch"], tot["worst_at"]))

# ---------------- controls ----------------
print("\n=== controls")
ctl = {}
pr1, a1ex1, _ = res_params(1)
v = quad_cert(1, 0.0, a1ex1)
ctl["mu0_exact_pdot"] = v["pdot_coh"]
ctl["mu0_thdot"] = v["thdot"]
print("mu=0 at exact resonance: pdot_coh=%.3e (must be 0 -> excursion=0, no switch anywhere)"
      % v["pdot_coh"])
calib = json.load(open(OUT + "/calib.json"))
for j, farpr in ((1, 2.15), (2, 1.9)):
    for mu in (3e-4, 1e-3):
        a1far = a_of_ratio(farpr)
        vv = quad_cert(j, mu, a1far)
        exc_far = 2 * vv["pdot_coh"] / abs(vv["thdot"])
        qe = calib["j%d_mu%g" % (j, mu)]["q_e"]
        ctl["far_j%d_mu%g" % (j, mu)] = {"exc": exc_far, "q_e": qe}
        print("far j=%d mu=%g (pr %.2f): excursion=%.2e vs calib q_e=%.4f -> %s" %
              (j, mu, farpr, exc_far, qe, "no switch" if exc_far < qe else "SWITCH"))
out["controls"] = ctl
json.dump(out, open(OUT + "/gate.json", "w"), indent=1)
print("\ngate.json written")
