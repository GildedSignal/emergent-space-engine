#!/usr/bin/env python3
"""Second-author re-issue (run 20261010-2141): the original falsifier with the
Kerr retrograde critical-b root CORRECTED (checker 2's named fix), plus the
verification the author missed: double-root-in-r check, Bardeen limits,
monotonicity, and internal consistency with kerr_alpha capture.

The corrected branch: the circular photon orbit at r_ph must be a DOUBLE root of
R(r) in r. R is quadratic in b:  (r-2)b^2 + 4ab - (r^3 + a^2 r + 2a^2) = 0,
so  b = (-2a +- r*sqrt(Delta)) / (r-2).  Prograde (s=-1) takes +r*sqrt(Delta),
retrograde (s=+1) takes -r*sqrt(Delta).  The original took the + branch for both.

Everything else is falsifier2.py verbatim (imported, not copied): the
Schwarzschild cases must come out identical, so out3.json differs from out2.json
exactly in the Kerr block.
"""
import json
import time

import numpy as np

import falsifier2 as f2


def corrected_kerr_photon_orbits(a):
    """Closed-form equatorial circular photon orbits (Bardeen 1973), correct branch."""
    out = {}
    for name, sign in (("pro", -1), ("retro", +1)):
        r_ph = 2.0 * (1.0 + np.cos((2.0 / 3.0) * np.arccos(np.clip(sign * a, -1, 1))))
        D = r_ph * r_ph - 2.0 * r_ph + a * a
        b = (-2.0 * a - sign * r_ph * np.sqrt(D)) / (r_ph - 2.0)  # -sign = +r*sqrt(D) for pro
        out[name] = (r_ph, b)
    return out


def Rfun(b, a, r):
    D = r * r - 2 * r + a * a
    return ((r * r + a * a) - a * b) ** 2 - D * (b - a) ** 2


def dRfun_dr(b, a, r):
    """Analytic dR/dr: 4r(r^2+a^2-ab) - (2r-2)(b-a)^2."""
    return 4.0 * r * (r * r + a * a - a * b) - (2.0 * r - 2.0) * (b - a) ** 2


def kerr_verification():
    """R1-R4 checks on the corrected roots (analytic R', no finite differences)."""
    from scipy.optimize import brentq
    rows = []
    sD = 3.0 * np.sqrt(3.0)
    for a in (0.0, 0.5, 0.9, 0.998, 1.0 - 1e-9):
        bc = corrected_kerr_photon_orbits(a)
        row = dict(a=a)
        for name, sign in (("pro", -1), ("retro", +1)):
            r_ph, b = bc[name]
            b_other = (-2.0 * a + sign * r_ph * np.sqrt(r_ph * r_ph - 2 * r_ph + a * a)) / (r_ph - 2.0)
            # R1: analytic double-root condition R = 0 AND dR/dr = 0 at the chosen b
            row[name] = dict(
                r_ph=round(r_ph, 6), b=round(b, 6),
                R_chosen=float(f"{abs(Rfun(b, a, r_ph)):.3g}"),
                dRdr_chosen=float(f"{abs(dRfun_dr(b, a, r_ph)):.3g}"),
                R_rejected=float(f"{abs(Rfun(b_other, a, r_ph)):.3g}"),
                dRdr_rejected=float(f"{abs(dRfun_dr(b_other, a, r_ph)):.3g}"),
                b_numeric_root=round(float(min(
                    (r_ for r_ in np.roots([r_ph - 2.0, 4.0 * a,
                                            -(r_ph ** 3 + a * a * r_ph + 2 * a * a)])
                    if abs(r_.imag) < 1e-9), key=lambda rr: abs(rr - b))), 10))
        row["retro_over_bcrit"] = round(abs(bc["retro"][1]) / sD, 6)
        row["bcrit_over_pro"] = round(sD / bc["pro"][1], 6) if a > 0 else 1.0
        rows.append(row)
    out = dict(limits=rows,
               a1=dict(b_pro=rows[-1]["pro"]["b"], b_retro=rows[-1]["retro"]["b"],
                       expect_pro=2.0, expect_retro=-7.0),
               a0=dict(b_pro=rows[0]["pro"]["b"], b_retro=rows[0]["retro"]["b"],
                       expect=3.0 * np.sqrt(3.0)))
    # R4: internal consistency at a=0.9 — |b|=6 captures, |b|=7 bends
    a6 = f2.kerr_alpha(-6.0, 0.9, 50.0, 200.0)
    a7 = f2.kerr_alpha(-7.0, 0.9, 50.0, 200.0)
    out["consistency_a0.9"] = dict(alpha_minus6="inf(capture)" if not np.isfinite(a6) else round(a6, 4),
                                   alpha_minus7=round(a7, 4) if np.isfinite(a7) else "inf",
                                   b_crit_retro_mag=round(abs(corrected_kerr_photon_orbits(0.9)["retro"][1]), 4))
    return out


def main():
    t0 = time.time()
    f2.kerr_photon_orbits = corrected_kerr_photon_orbits  # the one fix
    out = {}
    out["weak_control"] = f2.run_case("weak", 5000.0, 20000.0, [0.001, 0.005, 0.02, 0.1])
    out["r_o50_r_s200"] = f2.run_case("mid", 50.0, 200.0, [0.02, 0.1, 0.5, 1, 2, 4, 8, 15, 25, 40])
    out["r_o10_r_s50"] = f2.run_case("near", 10.0, 50.0, [0.02, 0.1, 0.5, 1, 2, 4, 8, 15, 25, 40])

    kerr = {}
    for a in (0.5, 0.9, 0.998):
        bc = corrected_kerr_photon_orbits(a)
        kerr[f"a={a}"] = dict(r_ph_pro=round(bc["pro"][0], 4), b_pro=round(bc["pro"][1], 4),
                              r_ph_retro=round(bc["retro"][0], 4),
                              b_retro=round(abs(bc["retro"][1]), 4), b_retro_signed=round(bc["retro"][1], 4),
                              ratio=round(abs(bc["retro"][1]) / bc["pro"][1], 4))
    for bm in (6.0, 8.0, 12.0):
        ap = f2.kerr_alpha(+bm, 0.9, 50.0, 200.0)
        ar = f2.kerr_alpha(-bm, 0.9, 50.0, 200.0)
        kerr[f"a=0.9_|b|={bm}"] = dict(alpha_pro=round(ap, 4) if np.isfinite(ap) else None,
                                       alpha_retro=round(ar, 4) if np.isfinite(ar) else None,
                                       delta=round(abs(ap - ar), 4) if (np.isfinite(ap) and np.isfinite(ar)) else None)
    out["kerr"] = kerr
    out["kerr_verification"] = kerr_verification()
    out["p4_shapiro"] = []  # filled below exactly as f2.main does
    for v, r_o, r_s in ((0.5, 10.0, 15.0), (0.5, 10.0, 50.0), (0.5, 50.0, 200.0)):
        Phi = np.pi - 0.05
        ex = [e for e in f2.exact_images(r_o, r_s, Phi) if e["k"] == 0 and e["psi"] > 0]
        if not ex:
            continue
        b = ex[0]["b"]
        t_ex = f2.travel_time(b, r_o, r_s)
        S = np.array([r_s * np.cos(Phi), r_s * np.sin(Phi)])
        t_flat = np.linalg.norm(S - np.array([r_o, 0.0]))
        dt = t_ex - t_flat
        atab = f2.alpha_table(r_o, r_s)
        beta, con = f2.construction(r_o, r_s, Phi, atab)
        disp = ex[0]["psi"] - beta
        out["p4_shapiro"].append(dict(v=v, r_o=r_o, r_s=r_s, psi=round(ex[0]["psi"], 3),
                                      shapiro_M=round(dt, 2), pos_err_deg=round(np.degrees(v * dt / t_flat), 4),
                                      lens_disp_deg=round(disp, 3),
                                      ratio=round(np.degrees(v * dt / t_flat) / disp, 4) if disp else None))

    Phi = np.pi - 0.5
    r_o, r_s = 10.0, 50.0

    class ZeroAlpha:
        def __call__(self, b):
            return 0.0

    beta, con = f2.construction(r_o, r_s, Phi, ZeroAlpha())
    out["negative_control"] = dict(beta_deg=round(beta, 5),
                                   roots_deg=[round(np.degrees(t), 5) for t in con])
    out["oracle_selfcheck"] = dict(alpha_b100_weak=round(
        f2.sweep(100.0, 500.0, 2000.0) - (np.arccos(100 / 500) + np.arccos(100 / 2000)), 6),
        weak_expect_ge_4_over_b=0.04)
    out["runtime_s"] = round(time.time() - t0, 2)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
