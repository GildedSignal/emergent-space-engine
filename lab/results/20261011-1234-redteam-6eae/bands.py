#!/usr/bin/env python3
"""Secondary probe (v2, seeds fixed): the m=16 Binet band model where r1's sampler never
goes (e > 0.7 and p < 10; r1 drew p log-uniform in [10,1000], e uniform in [0,0.7]).

v1 defect: seeds derived L from a wrong first integral (1/L^2 = u_p^2 (1-2u_p), dropping
the 2u/L^2 term), producing unphysical orbits that cross u = 0. Correct turning-point
construction: u_p = (1+e)/p, u_a = (1-e)/p, 1/L^2 = 1/p - (3+e^2)/p^2.

Exact timelike Schwarzschild (M=1): u'' + u = 1/L^2 + 3 u^2.
Band model (representation.md / r1): band k covers r in [2^(k/16), 2^((k+1)/16)), u_k at its
geometric centre; inside it u'' + (1 - 6 u_k) u = 1/L^2 - 3 u_k^2, u and u' continuous.
Seeds start at periapsis (u(0)=u_p, u'(0)=0). One radial cycle = periapsis to periapsis
(w: + -> - with u > 0.9 u_p, after one apoapsis crossing)."""
import json
import numpy as np

H = 5e-4
PHI_MAX = 80 * np.pi


def rhs_w(u, one_over_L2, model):
    if not model:
        return -u + one_over_L2 + 3.0 * u * u
    k = np.floor(16.0 * np.log2(1.0 / u))
    u_k = 2.0 ** (-(k + 0.5) / 16.0)
    return -(1.0 - 6.0 * u_k) * u + one_over_L2 - 3.0 * u_k * u_k


def integrate(u_p, one_over_L2, model, h=H, phi_max=PHI_MAX):
    u, w, phi = u_p, 0.0, 0.0
    seen_apo = False
    for _ in range(int(phi_max / h)):
        k1u, k1w = w, rhs_w(u, one_over_L2, model)
        k2u, k2w = w + 0.5 * h * k1w, rhs_w(u + 0.5 * h * k1u, one_over_L2, model)
        k3u, k3w = w + 0.5 * h * k2w, rhs_w(u + 0.5 * h * k2u, one_over_L2, model)
        k4u, k4w = w + h * k3w, rhs_w(u + h * k3u, one_over_L2, model)
        un = u + (h / 6.0) * (k1u + 2 * k2u + 2 * k3u + k4u)
        wn = w + (h / 6.0) * (k1w + 2 * k2w + 2 * k3w + k4w)
        w_old = w
        u, w, phi = un, wn, phi + h
        if not np.isfinite(u) or u <= 0.0:
            return phi, "escaped-through-zero"
        if u > 0.5:
            return phi, "plunge"
        if w_old < 0.0 <= wn and phi > 0.5:
            seen_apo = True
        elif seen_apo and w_old > 0.0 >= wn and u > 0.9 * u_p:
            return phi, "bound"
    return phi, "truncated"


def one_over_L2_of(e, p):
    return 1.0 / p - (3.0 + e * e) / (p * p)


def run_seed(e, p):
    u_p = (1.0 + e) / p
    c = one_over_L2_of(e, p)
    if c <= 0 or u_p >= 0.5:
        return None
    dE, cE = integrate(u_p, c, False)
    dM, cM = integrate(u_p, c, True)
    return {"e": round(float(e), 3), "p": round(float(p), 3),
            "dphi_exact": round(dE, 4), "class_exact": cE,
            "dphi_model": round(dM, 4), "class_model": cM,
            "rel_err": round(abs(dM - dE) / dE, 5) if cE == cM == "bound" and dE > 0 else None}


def main():
    rng = np.random.default_rng(20261011)
    rows = []
    for _ in range(20):  # r1-domain replication control
        e = rng.uniform(0.0, 0.7)
        p = 10 ** rng.uniform(1.0, 2.0)
        r = run_seed(e, p)
        if r:
            r["domain"] = "r1"
            rows.append(r)
    for e in [0.8, 0.9, 0.95]:  # excluded domain; p_sep(e) = 6 + 2e
        for dp in [1.0, 0.5, 0.2, 0.1]:
            r = run_seed(e, 6.0 + 2.0 * e + dp)
            if r:
                r["domain"] = "excluded"
                r["p_minus_sep"] = dp
                rows.append(r)
    with open("bands.json", "w") as f:
        json.dump(rows, f, indent=1)
    for r in rows:
        print(r)

    # jet derivative: d(dphi)/dL (exact) as p -> p_sep at fixed e = 0.9
    out = []
    e = 0.9
    for dp in [1.0, 0.5, 0.2, 0.1]:
        p = 6.0 + 2.0 * e + dp
        L = 1.0 / np.sqrt(one_over_L2_of(e, p))
        hL = 1e-3 * L
        dps = []
        for L2 in (L - hL, L + hL):
            x = 1.0 / L2
            # solve x = 1/p - (3+e^2)/p^2 for 1/p near the original
            a, b, c2 = 3.0 + e * e, -1.0, x
            disc = b * b - 4 * a * c2
            invp = (-b + np.sqrt(disc)) / (2 * a)  # root near 1/p (the larger root)
            p2 = 1.0 / invp
            d, _ = integrate((1.0 + e) / p2, one_over_L2_of(e, p2), False)
            dps.append(d)
        slope = (dps[1] - dps[0]) / (2 * hL)
        out.append({"p_minus_sep": dp, "L": round(L, 4), "dphi": round(dps[0], 3),
                    "d_dphi_dL": slope})
    base = out[0]["d_dphi_dL"]
    for o in out:
        o["ratio_to_dp_1.0"] = o["d_dphi_dL"] / base
    print(json.dumps(out, indent=1, default=float))
    with open("bands_jet.json", "w") as f:
        json.dump(out, f, indent=1, default=float)


if __name__ == "__main__":
    main()
