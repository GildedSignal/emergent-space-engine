#!/usr/bin/env python3
"""The fleet doll's interior tide law at the game's own speeds (20261020-1002-redteam-288f).

Letter (representation.md L23, law.md L50, crates/engine/src/frame.rs L14-L19):
inside a fleet doll (a free-fall / Fermi frame) members feel only x'' = -E(t)x with the
NEWTONIAN tidal tensor E = (GM/r^3)(I - 3 r r^T) read along the origin's tube.
Shipped legality (frame.rs L83, ORBIT_SPEED_DIV = 4): the origin's orbit speed <= c/4.

Truth: exact Schwarzschild geodesics (M = 1, c = 1), a central body plus one member
born rigid at xi = 1e-3 r0, separation read in the parallel-transported (Fermi) frame
(the letter's own frame). Instantaneous truth: the Riemann contraction
E(u)_ab = R_{a c b d} u^c u^d (exact), cross-checked by finite differences of the
integrated member geodesics (independent path, Richardson-extrapolated).

Laws compared on the same Fermi axes and the same tau grid:
  letter: x'' = -E_N x,  E_N = w diag(-2, 1) in (r_hat, theta_hat), w = M/r^3
  cure:   x'' = -E(u) x, E(u) = the contraction above (closed form, O(1) coefficients)

All float64. Run: python3 falsifier.py   (from this directory; writes results.json)
"""
import json
import math

import numpy as np
from scipy.integrate import solve_ivp

M = 1.0
TOL = 1e-12


# ---------------------------------------------------------------- Schwarzschild
def gamma_of(r, ur, E):
    f = 1.0 - 2.0 * M / r
    return E / math.sqrt(f)


def local_beta(r, ur, E, L):
    """Velocity components in the static orthonormal frame: (beta_r, beta_th)."""
    f = 1.0 - 2.0 * M / r
    g = gamma_of(r, ur, E)
    return (ur / math.sqrt(f)) / g, (L / r) / g


def launch(r0, br, bth):
    """Launch state at (t=0, r0, phi=0) with local orthonormal velocity (br, bth)."""
    f = 1.0 - 2.0 * M / r0
    b2 = br * br + bth * bth
    assert b2 < 1.0, "subluminal launch required"
    gam = 1.0 / math.sqrt(1.0 - b2)
    ut, ur, uphi = gam / math.sqrt(f), gam * br * math.sqrt(f), gam * bth / r0
    E, L = f * ut, r0 * r0 * uphi
    return dict(E=E, L=L, ut=ut, ur=ur, uphi=uphi, gam=gam)


def gam_full(r):
    """Nonzero Christoffel symbols, equatorial Schwarzschild, M = 1 (with symmetry)."""
    f = 1.0 - 2.0 * M / r
    G = np.zeros((3, 3, 3))
    for (u_, a, b), v in {(0, 0, 1): 1.0 / (r**2 * f),      # Gamma^t_tr
                          (1, 0, 0): f / r**2,              # Gamma^r_tt
                          (1, 1, 1): -1.0 / (r**2 * f),     # Gamma^r_rr
                          (1, 2, 2): -r * f,                # Gamma^r_phiphi
                          (2, 1, 2): 1.0 / r}.items():      # Gamma^phi_rphi
        G[u_, a, b] += v
        if a != b:
            G[u_, b, a] += v
    return G


def member_launch(r0, br, bth, dx_len, axis):
    """Born-rigid member: dx = dx_len*e_axis, u_m = u - Gamma.dx.u at O(dx)."""
    f = 1.0 - 2.0 * M / r0
    c = launch(r0, br, bth)
    dx = (np.array([0.0, dx_len * math.sqrt(f), 0.0]) if axis == "r"
          else np.array([0.0, 0.0, dx_len / r0]))
    u = np.array([c["ut"], c["ur"], c["uphi"]])
    um = u - np.einsum("uab,a,b->u", gam_full(r0), dx, u)
    rm = r0 + dx[1]
    fm = 1.0 - 2.0 * M / rm
    # restore the mass shell along u (the u-component is gauge: a re-parametrisation
    # of the member's worldline; the O(xi) transport leaves a norm defect O(gamma^2 xi))
    gm = np.array([-fm, 1.0 / fm, rm * rm])
    n2 = float(np.dot(gm * um, um))
    gu = float(np.dot(gm * um, u))
    s = (-1.0 - n2) / (2.0 * gu)
    um = um + s * u
    Em = fm * um[0]
    Lm = rm * rm * um[2]
    return dict(y0=np.array([0.0, rm, dx[2], um[1]]), E=Em, L=Lm)


def geo_rhs(E, L, with_tetrad=False):
    def rhs(tau, y):
        r, ur = y[1], y[3]
        f = 1.0 - 2.0 * M / r
        ut, uphi = E / f, L / (r * r)
        dur = -(f / r**2) * ut * ut + ur * ur / (r * r * f) + f * L * L / r**3
        if not with_tetrad:
            return [ut, ur, uphi, dur]
        out = np.empty(10)
        out[:4] = [ut, ur, uphi, dur]
        G = gam_full(r)
        u = np.array([ut, ur, uphi])
        for k in range(2):
            e = y[4 + 3 * k:7 + 3 * k]
            out[4 + 3 * k:7 + 3 * k] = -np.einsum("uab,a,b->u", G, e, u)
        return out

    return rhs


def norm_drift(y, E, L):
    r, ur = y[1], y[3]
    f = 1.0 - 2.0 * M / r
    ut, uphi = E / f, L / (r * r)
    return abs(-f * ut * ut + ur * ur / f + r * r * uphi * uphi + 1.0)


# ------------------------------------------------------------------- the scene
def run_scene(name, r0, br, bth, tau_end, xi_rel=1e-3, axis="r", n_samples=400):
    c = launch(r0, br, bth)
    f0 = 1.0 - 2.0 * M / r0
    # Spatial Fermi axes, orthogonal to u: the axis along the motion is the boosted
    # gamma*(beta*e_t + e_par); the transverse static axis is orthogonal to u as is.
    if abs(bth) >= abs(br):          # motion along theta: e1 = e_r_hat, e2 boosted theta
        e1 = np.array([0.0, math.sqrt(f0), 0.0])
        e2 = np.array([c["gam"] * bth / math.sqrt(f0), 0.0, c["gam"] / r0])
    else:                            # motion along r: e2 = e_theta_hat, e1 boosted r
        e1 = np.array([c["gam"] * br / math.sqrt(f0), c["gam"] * math.sqrt(f0), 0.0])
        e2 = np.array([0.0, 0.0, 1.0 / r0])
    ycen0 = np.concatenate([np.array([0.0, r0, 0.0, c["ur"]]), e1, e2])
    cen = solve_ivp(geo_rhs(c["E"], c["L"], True), (0.0, tau_end), ycen0,
                    method="DOP853", rtol=TOL, atol=1e-13, dense_output=True,
                    max_step=tau_end / 40.0)
    assert cen.success, cen.message
    ml = member_launch(r0, br, bth, xi_rel * r0, axis)
    mem = solve_ivp(geo_rhs(ml["E"], ml["L"]), (0.0, tau_end), ml["y0"],
                    method="DOP853", rtol=TOL, atol=1e-13, dense_output=True,
                    max_step=tau_end / 40.0)
    assert mem.success, mem.message

    def sep(tau):
        yc, ym = cen.sol(tau), mem.sol(tau)
        dphi = (ym[2] - yc[2] + math.pi) % (2 * math.pi) - math.pi
        dx = np.array([ym[0] - yc[0], ym[1] - yc[1], dphi])
        r = yc[1]
        f = 1.0 - 2.0 * M / r
        g = np.array([-f, 1.0 / f, r * r])
        return np.array([np.dot(g * dx, yc[4:7]), np.dot(g * dx, yc[7:10])]), yc

    taus = np.linspace(0.0, tau_end, n_samples)
    truth = np.array([sep(t)[0] for t in taus]).T
    cons = max(norm_drift(cen.sol(t), c["E"], c["L"]) for t in (0.0, tau_end))
    cons = max(cons, max(norm_drift(mem.sol(t), ml["E"], ml["L"]) for t in (0.0, tau_end)))
    return dict(name=name, r0=r0, beta0=math.hypot(br, bth), taus=taus, truth=truth,
                cen=cen, mem=mem, E=c["E"], L=c["L"], cons=cons, xi0=xi_rel * r0,
                sep=sep)


# ------------------------------------------------------------ the two tide laws
def lam(yc):
    """Static-orthonormal components of the Fermi axes e_1, e_2 (columns)."""
    r = yc[1]
    f = 1.0 - 2.0 * M / r
    return np.array([[math.sqrt(f) * yc[4], math.sqrt(f) * yc[7]],
                     [yc[5] / math.sqrt(f), yc[8] / math.sqrt(f)],
                     [r * yc[6], r * yc[9]]])


def Efermi(yc, E, L, which):
    """The tide law's matrix in Fermi axes: a = -Efermi x.

    boost:  the exact GR tide measured by the moving origin,
            E'(ij) = e_i^a e_j^b R_{a c b d} u^c u^d as a FULL contraction:
            the t-row and the E_t-theta cross term are load-bearing (they
            cancel the naive gamma^2 along-track amplification exactly).
    newton: the letter's law (frame.rs): w(I - 3 n n^T) on the parent's
            direction in the comoving frame, the normalized Fermi-plane
            projection of e_r (aberrated at high beta).
    """
    r = yc[1]
    f = 1.0 - 2.0 * M / r
    w = M / r**3
    gam = gamma_of(r, yc[3], E)
    br, bth = local_beta(r, yc[3], E, L)
    g2 = gam * gam
    if which == "newton":
        g = np.array([-f, 1.0 / f, r * r])
        e_r = np.array([0.0, math.sqrt(f), 0.0])
        n = np.array([np.dot(g * e_r, yc[4:7]), np.dot(g * e_r, yc[7:10])])
        n = n / math.sqrt(float(n @ n))
        return w * (np.eye(2) - 3.0 * np.outer(n, n))
    Est = np.array([  # E(u)_ab in the static orthonormal basis, a = (t, r, th)
        [g2 * w * (bth**2 - 2 * br**2), 2 * g2 * br * w, -g2 * bth * w],
        [2 * g2 * br * w, -g2 * w * (2 + bth**2), 0.0],
        [-g2 * bth * w, 0.0, g2 * w * (1 - br**2)]])
    Lm = lam(yc)
    return Lm.T @ Est @ Lm


def law_track(sc, which):
    cen, E, L = sc["cen"], sc["E"], sc["L"]

    def rhs(tau, x):
        Ef = Efermi(cen.sol(tau), E, L, which)
        return [x[2], x[3], -(Ef[0, 0] * x[0] + Ef[0, 1] * x[1]),
                -(Ef[1, 0] * x[0] + Ef[1, 1] * x[1])]

    x0 = np.array([sc["truth"][0, 0], sc["truth"][1, 0], 0.0, 0.0])
    sol = solve_ivp(rhs, (0.0, sc["taus"][-1]), x0, method="DOP853", rtol=TOL,
                    atol=1e-14, dense_output=True, max_step=sc["taus"][-1] / 200.0)
    assert sol.success
    return sol.sol(sc["taus"])[:2]


def rel_err(a, b, floor):
    return float(np.linalg.norm(a - b)) / max(float(np.linalg.norm(b)), floor)


# ------------------------------------------------------- coefficient instrument
def fd_acc(sc, tau_p, h):
    """Richardson FD of the truth's Fermi acceleration vector at tau_p."""

    def acc(hh):
        xp, _ = sc["sep"](tau_p + hh)
        x0, _ = sc["sep"](tau_p)
        xm, _ = sc["sep"](tau_p - hh)
        return (xp - 2 * x0 + xm) / hh**2, x0

    a1, x0 = acc(h)
    a2, _ = acc(h / 2)
    return (4 * a2 - a1) / 3, x0


def coeff_row(name, r0, br, bth):
    """Matrix instrument: the truth's linear tide map A (a = A x) at tau_p vs both laws."""
    c = launch(r0, br, bth)
    h = min(0.02 * 2 * math.pi * r0**1.5,
            0.05 * r0 / (c["gam"] * math.hypot(br, bth) + 1e-9))
    A_cols, X_cols = [], []
    for axis in ("r", "th"):
        sc = run_scene(name, r0, br, bth, 5 * h, xi_rel=1e-3, axis=axis, n_samples=20)
        a, x0 = fd_acc(sc, 3 * h, h)
        A_cols.append(a)
        X_cols.append(x0)
    yc = sc["cen"].sol(3 * h)
    A = np.array(A_cols).T @ np.linalg.inv(np.array(X_cols).T)
    Ec = Efermi(yc, sc["E"], sc["L"], "boost")
    En = Efermi(yc, sc["E"], sc["L"], "newton")
    r = yc[1]
    b_r, b_th = local_beta(r, yc[3], sc["E"], sc["L"])
    beta = math.hypot(b_r, b_th)
    g2 = 1.0 / (1.0 - beta * beta)
    closed = g2 * (2.0 + beta * beta * (b_th / max(beta, 1e-12)) ** 2) / 2.0
    # clean scalar channel: the [r] offset stays aligned with the radial eigen-direction
    ar, xr = A_cols[0], X_cols[0]
    En_r = -float(np.dot(En @ xr, xr) / np.dot(xr, xr))
    ratio_radial = -float(np.dot(ar, xr) / np.dot(xr, xr)) / En_r
    return dict(name=name, r_probe=r, beta=beta, closed_radial=closed,
                ratio_radial=float(ratio_radial),
                cure_rel=float(np.linalg.norm(A + Ec) / np.linalg.norm(Ec)),
                letter_rel=float(np.linalg.norm(A + En) / np.linalg.norm(En)),
                ratio_norm=float(np.linalg.norm(A) / np.linalg.norm(En)),
                A=[[float(A[0, 0]), float(A[0, 1])], [float(A[1, 0]), float(A[1, 1])]],
                cure=[[float(Ec[i, j]) for j in range(2)] for i in range(2)],
                letter=[[float(En[i, j]) for j in range(2)] for i in range(2)])


def circle_beta(r):
    return math.sqrt(M / (r - 2.0 * M))


def main():
    out = {"meta": {"M": M, "c": 1.0, "tol": TOL}}
    print("== Member separation over the window: relative error of the law vs truth ==")
    print(f"\n{'scene':<26}{'beta0':>7}{'T':>9}{'|xi|end':>10}{'exit letter':>13}"
          f"{'exit cure':>11}{'max letter':>12}{'max cure':>10}{'cons':>9}")
    scenes = []
    bc = circle_beta(1000.0)
    scenes.append(("control circ r=1000M", 1000.0, 0.0, bc,
                   2 * math.pi * 1000.0 * math.sqrt(1 - bc**2) / bc))
    bp = circle_beta(18.0)
    scenes.append(("cap circ r=18M (c/4)", 18.0, 0.0, bp,
                   2 * math.pi * 18.0 * math.sqrt(1 - bp**2) / bp))
    for beta in (0.5, 0.9, 0.99, 0.999):
        scenes.append((f"flyby r=100M b={beta}", 100.0, 0.0, beta, 2.2 * 100.0 / beta))
    scenes.append(("radial infall b=0.5", 100.0, -0.5, 0.0, 120.0))
    scenes.append(("strong r=20M b=0.9", 20.0, 0.0, 0.9, 2.2 * 20.0 / 0.9))

    out["scenes"] = []
    for name, r0, br, bth, T in scenes:
        for axis in ("r", "th"):
            sc = run_scene(name, r0, br, bth, T, axis=axis)
            law_n, law_b = law_track(sc, "newton"), law_track(sc, "boost")
            tr = sc["truth"]
            en = rel_err(law_n[:, -1], tr[:, -1], sc["xi0"])
            eb = rel_err(law_b[:, -1], tr[:, -1], sc["xi0"])
            mn = max(rel_err(law_n[:, k], tr[:, k], sc["xi0"]) for k in range(tr.shape[1]))
            mb = max(rel_err(law_b[:, k], tr[:, k], sc["xi0"]) for k in range(tr.shape[1]))
            print(f"{name + ' [' + axis + ']':<26}{sc['beta0']:7.4f}{T:9.3g}"
                  f"{float(np.linalg.norm(tr[:, -1])):10.4g}{en:13.4g}{eb:11.4g}"
                  f"{mn:12.4g}{mb:10.4g}{sc['cons']:9.1e}")
            out["scenes"].append(dict(name=name + f" [{axis}]", r0=r0,
                                      beta0=sc["beta0"], tau_end=T,
                                      xi_end_truth=float(np.linalg.norm(tr[:, -1])),
                                      exit_err_letter=en, exit_err_cure=eb,
                                      max_err_letter=mn, max_err_cure=mb,
                                      cons=sc["cons"]))

    print("\n== The truth's tide matrix A (a = A x, Richardson FD) vs both laws ==")
    print(f"\n{'scene':<26}{'beta@':>8}{'r@':>8}{'|A|/|N|':>9}{'closed':>9}"
          f"{'cure relerr':>12}{'letter relerr':>14}")
    out["coeffs"] = []
    for name, r0, br, bth, T in scenes:
        row = coeff_row(name, r0, br, bth)
        print(f"{name:<26}{row['beta']:8.4f}{row['r_probe']:8.2f}"
              f"{row['ratio_radial']:9.4f}{row['closed_radial']:9.4f}"
              f"{row['ratio_norm']:9.4f}{row['cure_rel']:10.3g}{row['letter_rel']:10.3g}")
        out["coeffs"].append(row)

    print("\n== Closed forms at exact closest approach (transverse beta) ==")
    out["closed_forms"] = []
    for b in (0.25, 0.5, 0.9, 0.99, 0.999):
        rr = (2 + b * b) / (2 * (1 - b * b))
        out["closed_forms"].append(dict(beta=b, radial=rr))
        print(f"beta {b:6.3f}: radial eigenvalue x{rr:10.3f} (along-track is exactly 1x:")
        print(f"          the (1,1,1,1) cancellation E'_22 = w at any beta, transverse launch)")

    # linearity at xi/10 on the player-speed flyby
    sc = run_scene("flyby r=100M b=0.9", 100.0, 0.0, 0.9, 2.2 * 100.0 / 0.9,
                   xi_rel=1e-4, axis="r")
    law_n = law_track(sc, "newton")
    en_small = rel_err(law_n[:, -1], sc["truth"][:, -1], sc["xi0"])
    ref = next(s for s in out["scenes"] if s["name"] == "flyby r=100M b=0.9 [r]")
    out["linearity"] = dict(xi_rel=1e-4, exit_err_letter=en_small,
                            at_xi_1e3=ref["exit_err_letter"])
    print(f"\nlinearity (flyby b=0.9 radial): xi=1e-4 err {en_small:.4g} "
          f"vs xi=1e-3 err {ref['exit_err_letter']:.4g}")

    # formation stretch at exit (the player-visible channel)
    out["stretch_b0.9"] = dict(
        xi0=sc["xi0"],
        truth_end=float(np.linalg.norm(sc["truth"][:, -1])) / sc["xi0"],
        letter_end=float(np.linalg.norm(law_n[:, -1])) / sc["xi0"])
    print(f"formation stretch at exit (b=0.9, radial offset, xi=1e-4 arm): truth x"
          f"{out['stretch_b0.9']['truth_end']:.3f} vs letter x"
          f"{out['stretch_b0.9']['letter_end']:.3f}")

    with open("results.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print("\nwrote results.json")


if __name__ == "__main__":
    main()
