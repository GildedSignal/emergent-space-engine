#!/usr/bin/env python3
"""Falsifier for representation.md line 67 / law.md line 35 (the jet):
"Perturbations are kicks on E and L. A cycle's derivatives are stored with
it, so a kick updates the cycle by a multiply-add" — the derivative (jet)
update, and its re-anchor cost, near the two separatrices of Schwarzschild.

G = c = M = 1, equatorial. Radial motion (dr/dtau)^2 = E^2 - V2(r),
V2 = (1-2/r)(1+L^2/r^2). Per radial cycle:
  Dphi = 2 int_{r1}^{r2} L / (r^2 sqrt(E^2-V2)) dr
  Dt   = 2 int_{r1}^{r2} E / ((1-2/r) sqrt(E^2-V2)) dr
Substitution r = r1 + (r2-r1) sin^2(theta) removes the endpoint roots.

Inner separatrix: E -> E_sep (local max of V2; the plunge). L = 3.5.
Outer (parabolic) side: E -> 1 (e -> 1) at L = 10. Kepler homogeneity
predicts the relative Dt sensitivity is (3/2) dE/E, independent of e.
"""
import json
import sys
import numpy as np

N = 20000


def roots_of_w(E2, L, r_lo=2.05, r_hi=2000.0, n=400000):
    r = np.linspace(r_lo, r_hi, n)
    w = E2 - (1 - 2 / r) * (1 + L * L / (r * r))
    s = np.sign(w)
    idx = np.where(np.diff(s) < 0)[0]  # + -> - : inner turning point r1
    r1 = None
    r2 = None
    if len(idx):
        i = idx[-1]  # the barrier crossing closest to the max from outside
        r1 = 0.5 * (r[i] + r[i + 1])
    j = np.where(np.diff(s) > 0)[0]  # - -> + going out: outer turning point
    if len(j):
        i = j[0]
        r2 = 0.5 * (r[i] + r[i + 1])
    return r1, r2


def cycle(E, L):
    r1, r2 = roots_of_w(E * E, L)
    if r1 is None or r2 is None or r2 <= r1:
        return None
    th = np.linspace(0.0, np.pi / 2, N)
    s, c = np.sin(th), np.cos(th)
    r = r1 + (r2 - r1) * s * s
    w = E * E - (1 - 2 / r) * (1 + L * L / (r * r))
    dw = w[-2] - w[-1]
    # replace near-endpoint garbage by analytic limits
    w[0] = 1e-300
    w[-1] = 1e-300
    sqrtw = np.sqrt(np.maximum(w, 0.0))
    # limits: g(0) = 2 L sqrt(r2-r1) / (r1^2 sqrt(|w'(r1)|))
    wp1 = ((E * E - (1 - 2 / (r1 + 1e-9)) * (1 + L * L / (r1 + 1e-9) ** 2))
           - (E * E - (1 - 2 / (r1 - 1e-9)) * (1 + L * L / (r1 - 1e-9) ** 2))) / 2e-9
    wp2 = ((E * E - (1 - 2 / (r2 + 1e-9)) * (1 + L * L / (r2 + 1e-9) ** 2))
           - (E * E - (1 - 2 / (r2 - 1e-9)) * (1 + L * L / (r2 - 1e-9) ** 2))) / 2e-9
    gphi = 2 * (r2 - r1) * L * s * c / (r * r * sqrtw)
    gphi[0] = 2 * L * np.sqrt(r2 - r1) / (r1 * r1 * np.sqrt(abs(wp1)))
    gphi[-1] = 2 * L * np.sqrt(r2 - r1) / (r2 * r2 * np.sqrt(abs(wp2)))
    gt = gphi * (E / L) * (r * r) / (1 - 2 / r)
    gt[0] = gphi[0] * (E / L) * (r1 * r1) / (1 - 2 / r1)
    gt[-1] = gphi[-1] * (E / L) * (r2 * r2) / (1 - 2 / r2)
    dphi = 2 * np.trapz(gphi, th)
    dt = 2 * np.trapz(gt, th)
    return {"r1": r1, "r2": r2, "dphi": dphi, "dt": dt}


def jet_row(E, L, dE, tag):
    base = cycle(E, L)
    if base is None:
        return None
    h = dE / 100.0
    up, dn = cycle(E + h, L), cycle(E - h, L)
    dphi_prime = (up["dphi"] - dn["dphi"]) / (2 * h)
    dt_prime = (up["dt"] - dn["dt"]) / (2 * h)
    kicked = cycle(E + dE, L)
    jet_phi = base["dphi"] + dphi_prime * dE
    jet_t = base["dt"] + dt_prime * dE
    return {
        "tag": tag, "E": E, "L": L, "dE": dE,
        "r1": base["r1"], "r2": base["r2"],
        "dphi": base["dphi"], "dt": base["dt"],
        "dphi_prime": dphi_prime, "dt_prime": dt_prime,
        "phi_jet_err": abs(kicked["dphi"] - jet_phi),
        "t_jet_err": abs(kicked["dt"] - jet_t),
        "phi_jet_err_rel": abs(kicked["dphi"] - jet_phi) / abs(kicked["dphi"]),
        "t_jet_err_rel": abs(kicked["dt"] - jet_t) / abs(kicked["dt"]),
        "sens_phi": abs(dphi_prime) * abs(E) / abs(base["dphi"]),
        "sens_t": abs(dt_prime) * abs(E) / abs(base["dt"]),
        "kicked_exact": kicked,
    }


def main():
    out = []

    # ---- inner separatrix (plunge): L = 3.5 ----
    L = 3.5
    Esep = float(np.sqrt(max((1 - 2 / r) * (1 + L * L / (r * r))
                             for r in np.linspace(4.5, 6.5, 200001))))
    print(f"# L={L} E_sep={Esep:.9f}")
    for dist in [1e-2, 1e-3, 1e-4, 1e-5]:
        E = Esep - dist
        for frac in [0.01, 0.1, 1.0]:
            row = jet_row(E, L, frac * dist, f"plunge dist={dist:g} frac={frac:g}")
            if row:
                row["dist_to_sep"] = dist
                row.pop("kicked_exact")
                out.append(row)
                print(json.dumps({k: row[k] for k in
                     ["tag", "r1", "dphi", "phi_jet_err", "phi_jet_err_rel",
                      "t_jet_err_rel", "sens_phi", "sens_t"]}))

    # ---- outer (parabolic) side: L = 10, E -> 1 ----
    L = 10.0
    for E in [0.999, 0.9999, 0.99999, 0.999999]:
        for rel in [1e-4, 1e-3]:
            row = jet_row(E, L, rel * (1.0 - E) * 0 + rel * (1 - E) * 10,
                          f"parabolic E={E:g} dE={rel:g}*(1-E)*10")
            # kicks sized relative to (1-E): 10% and 100% of the binding margin
            if row:
                row["dist_to_sep"] = 1.0 - E
                row.pop("kicked_exact")
                out.append(row)
                print(json.dumps({k: row[k] for k in
                     ["tag", "r2", "dphi", "phi_jet_err", "phi_jet_err_rel",
                      "t_jet_err_rel", "sens_phi", "sens_t"]}))

    with open(sys.argv[1] if len(sys.argv) > 1 else "jet-results.json", "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
