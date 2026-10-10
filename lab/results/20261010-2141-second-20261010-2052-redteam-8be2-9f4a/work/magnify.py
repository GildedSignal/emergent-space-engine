#!/usr/bin/env python3
"""The named missing experiment (checker 2): magnification of the winding images.

Exact map of the original run's oracle, per image branch (side x winding k):
the screen angle psi solves beta(psi) = beta_true, where beta(psi) is the flat
source angle implied by the exact geodesic launched at psi.  Magnification of
the axisymmetric point-source map (psi signed, cw negative):

    mu = (sin psi / sin beta_true) * (d psi / d beta)

d(beta)/d(psi) by chain rule on the exact map:
  d(beta_flat)/d(Phi_im) (geometry, central diff, free)
  * d(sweep)/db          (2 oracle calls, central diff with near-critical guard)
  * db/dpsi = r_o cos|psi| / sqrt(1-2/r_o)  (analytic).
Phi_im = +(sweep - 2 pi k) for ccw, -(sweep - 2 pi k) for cw; both give the
same expression (odd symmetry of beta_flat and sgn^2 cancellation), evaluated
at each branch's own b.  Parity (sign of mu) comes from sin(psi_signed).

Controls: (i) sum of signed mu over all images ~ 1 (flux conservation);
(ii) at the weak control scene the primary matches the textbook point-lens
mu(u) = (u^2+2)/(2u sqrt(u^2+4)) + 1/2 with u from flat-distances theta_E;
(iii) beta(psi_image) = beta_true to solver tolerance (branch consistency).
"""
import json
import time

import numpy as np

import falsifier2 as f2


def geom_beta(r_o, r_s, Phi):
    """Flat source angle (rad) seen from observer, from the hole direction (-x)."""
    S = np.array([r_s * np.cos(Phi), r_s * np.sin(Phi)])
    O = np.array([r_o, 0.0])
    d = (S - O) / np.linalg.norm(S - O)
    return np.arctan2(d[1], -d[0])


def dgeom_dPhi(r_o, r_s, Phi, h=1e-6):
    return (geom_beta(r_o, r_s, Phi + h) - geom_beta(r_o, r_s, Phi - h)) / (2 * h)


def dsweep_db(b, r_o, r_s):
    """d(sweep)/db with a guard against crossing the critical b."""
    for rel in (1e-6, 1e-7, 1e-8, 1e-9):
        db = rel * b
        hi, lo = f2.sweep(b + db, r_o, r_s), f2.sweep(b - db, r_o, r_s)
        if np.isfinite(hi) and np.isfinite(lo):
            return (hi - lo) / (2 * db), rel
    return np.nan, None


def images_with_mu(r_o, r_s, off_deg, windings=(0, 1, 2)):
    """All exact images at this offset with signed magnifications."""
    f2.R_O, f2.R_S = r_o, r_s
    Phi = np.pi - np.radians(off_deg)
    beta_true = geom_beta(r_o, r_s, Phi)
    f = 1.0 - 2.0 / r_o
    dbetadPhi = dgeom_dPhi(r_o, r_s, Phi)  # same value on both branches (periodicity)
    out = []
    for fam, base in (("ccw", Phi), ("cw", 2 * np.pi - Phi)):
        for k in windings:
            b = f2.exact_b_for_sweep(base + 2 * np.pi * k)
            if b is None:
                continue
            psi = np.arcsin(min(1.0, b * np.sqrt(f) / r_o)) * (1.0 if fam == "ccw" else -1.0)
            dsdb, dbrel = dsweep_db(b, r_o, r_s)
            dbetadpsi = dbetadPhi * dsdb * (r_o * np.cos(abs(psi)) / np.sqrt(f))
            mu = (np.sin(psi) / np.sin(beta_true)) / dbetadpsi
            # branch consistency: implied source angle at the image == beta_true
            phi_im = (f2.sweep(b, r_o, r_s) - 2 * np.pi * k) * (1.0 if fam == "ccw" else -1.0)
            out.append(dict(fam=fam, k=k, b=b, psi_deg=round(float(np.degrees(psi)), 4),
                            mu=None if not np.isfinite(mu) else float(mu),
                            db_rel_used=dbrel,
                            beta_err=float(abs(geom_beta(r_o, r_s, phi_im) - beta_true))))
    return beta_true, out


def main():
    t0 = time.time()
    scenes = [("weak", 5000.0, 20000.0, [0.5, 1.0, 2.0, 5.0]),
              ("mid", 50.0, 200.0, [0.02, 0.5, 5.0, 15.0, 40.0]),
              ("near", 10.0, 50.0, [0.02, 0.5, 5.0, 15.0, 40.0]),
              ("deep", 6.0, 30.0, [0.02, 0.5, 5.0, 15.0, 40.0])]
    out = {}
    for name, r_o, r_s, offs in scenes:
        rows = []
        for off in offs:
            beta, imgs = images_with_mu(r_o, r_s, off)
            ok = [i for i in imgs if i["mu"] is not None]
            prim = [abs(i["mu"]) for i in ok if i["k"] == 0]
            wind = [abs(i["mu"]) for i in ok if i["k"] >= 1]
            bright = max(prim) if prim else float("nan")
            tot = sum(prim) + sum(wind)
            rows.append(dict(
                off_deg=off, beta_deg=round(float(np.degrees(beta)), 4), n_images=len(ok),
                images=[dict(fam=i["fam"], k=i["k"], psi_deg=i["psi_deg"],
                             mu=round(i["mu"], 8)) for i in ok],
                mu_brightest_primary=round(bright, 6),
                winding_share=round(sum(wind) / tot, 6),
                max_single_winding_vs_brightest=round((max(wind) if wind else 0.0) / bright, 6),
                signed_mu_sum=round(sum(i["mu"] for i in ok), 6),
                psi_shadow_deg=round(float(np.degrees(np.arcsin(
                    f2.BCRIT * np.sqrt(1.0 - 2.0 / r_o) / r_o))), 4),
                max_beta_err=max(i["beta_err"] for i in ok)))
        out[name] = dict(r_o=r_o, r_s=r_s, rows=rows)

    # textbook control at the weak scene (flat distances, as the construction uses)
    txt = []
    r_o, r_s = 5000.0, 20000.0
    for off in (0.5, 1.0, 2.0, 5.0):
        Phi = np.pi - np.radians(off)
        beta = geom_beta(r_o, r_s, Phi)
        S = np.array([r_s * np.cos(Phi), r_s * np.sin(Phi)])
        D_s = np.linalg.norm(S - np.array([r_o, 0.0]))
        thE = np.sqrt(4.0 * r_s / (r_o * D_s))  # theta_E^2 = 4 M D_ls/(D_l D_s), M=1
        u = beta / thE
        mu_txt = (u * u + 2) / (2 * u * np.sqrt(u * u + 4)) + 0.5
        _, imgs = images_with_mu(r_o, r_s, off, windings=(0,))
        got = [i["mu"] for i in imgs if i["fam"] == "ccw" and i["k"] == 0]
        if got:
            txt.append(dict(off_deg=off, u=round(float(u), 5), theta_E_deg=round(float(np.degrees(thE)), 5),
                            mu_exact=round(got[0], 6), mu_textbook=round(float(mu_txt), 6),
                            rel_err=round(abs(got[0] - mu_txt) / mu_txt, 5)))
    out["textbook_control_weak"] = txt

    # completeness: no images hide on the outgoing branch (launch psi > 90 deg).
    # Max swept azimuth from r_o outward to r_s over all b; behind-the-hole
    # sources sit at azimuth >= 140 deg in every scene above -> unreachable.
    from scipy.integrate import quad as _quad
    ob = []
    for name, r_o, r_s, _ in scenes:
        u_o, u_s = 1.0 / r_o, 1.0 / r_s
        bmax = r_o / np.sqrt(1.0 - 2.0 / r_o) * 0.999999
        bs = np.linspace(0.05, bmax, 1500)
        best, bbest = 0.0, None
        for b in bs:
            P = lambda u: 1.0 / b ** 2 - u * u + 2 * u ** 3
            us = np.linspace(u_s, u_o, 400)
            if (np.array([P(u) for u in us]) <= 0).any():
                continue
            val, _ = _quad(lambda u: 1.0 / np.sqrt(P(u)), u_s, u_o, limit=200)
            if val > best:
                best, bbest = val, b
        ob.append(dict(scene=name, outgoing_sweep_max_deg=round(float(np.degrees(best)), 2),
                       min_source_azimuth_deg=140.0))
    out["outgoing_branch_bound"] = ob
    out["runtime_s"] = round(time.time() - t0, 2)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
