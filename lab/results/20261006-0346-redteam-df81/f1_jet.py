#!/usr/bin/env python3
"""F1 — does 'a kick updates the cycle by a multiply-add' hold under correlated kicks?

Exact Schwarzschild bound-orbit cycle increments by Darwin-psi Gauss-Legendre
quadrature (the oracle); the 'jet' is the anchor cycle's stored first
derivatives (what representation.md 3 says a kick uses). Kicks: dL/L = eps per
radial cycle, same sign (Peters inspiral / tidal torque: monotone, listed in
the design). Floor: 1e-6 relative (the compiled cycle's own accuracy, law.md).

M = 1, c = 1 geometric units. P(u) = 2u^3 - u^2 + (2/L^2)u + (E^2-1)/L^2.
With u = c + A cos(psi), du/sqrt(P) = d psi / sqrt(2 (u3 - u))  on [0, pi].
"""
import numpy as np
from numpy.polynomial.legendre import leggauss

X, W = leggauss(64)          # nodes on [-1, 1]
PSI = 0.5 * np.pi * (X + 1)  # map to [0, pi]
FLOOR = 1e-6
NMAX = 10_000


def roots_from_EL(E, L):
    """roots of P(u); bound iff 3 real roots with 0 < u1 < u2 < u3 <= 1/2."""
    r = np.roots([2.0, -1.0, 2.0 / L**2, (E * E - 1.0) / L**2])
    r = np.sort(r.real[np.abs(r.imag) < 1e-10 * np.maximum(1, np.abs(r))])
    return r


def cycle(E, L):
    """(dphi, dt) increments of one radial cycle; nan if unbound/plunging."""
    r = roots_from_EL(E, L)
    if len(r) != 3 or r[2] >= 0.5 - 1e-12:
        return np.nan, np.nan
    u1, u2, u3 = r
    c, A = 0.5 * (u1 + u2), 0.5 * (u2 - u1)
    u = c + A * np.cos(PSI)
    s = np.sqrt(2.0 * (u3 - u))
    dphi = np.pi * np.sum(W / s)
    dt = 2.0 * np.pi * 0.5 * np.sum(W * E / ((1.0 - 2.0 * u) * L * u**2 * s))
    return dphi, dt


def EL_from_pe(p, e):
    u1, u2 = (1 - e) / p, (1 + e) / p
    u3 = 0.5 - u1 - u2
    L = 1.0 / np.sqrt(u1 * u2 + u1 * u3 + u2 * u3)
    E = np.sqrt(1.0 - 2.0 * L**2 * u1 * u2 * u3)
    return E, L


def run_case(p0, e0, eps, mode, nmax=NMAX):
    """Per-cycle relative errors of jet vs frozen against truth, for dphi and dt.

    mode: 'sys'  - correlated kicks dL/L = +eps per cycle (torque-like)
          'rand' - random-sign kicks dL/L = +-eps (uncorrelated contrast)
          'E'    - correlated kicks dE/|1-E| = +eps per cycle (Peters-like:
                   the inspiral shrinks |1-E|, and T ~ |1-E|^-3/2)
    """
    E0, L0 = EL_from_pe(p0, e0)
    f0 = np.array(cycle(E0, L0))
    hL = 1e-7 * L0
    hE = 1e-7 * abs(1.0 - E0)
    fdE = np.array(cycle(E0 + hE, L0))
    fdL = np.array(cycle(E0, L0 + hL))
    J_E = (fdE - f0) / hE
    J_L = (fdL - f0) / hL

    rng = np.random.default_rng(20261006)
    signs = rng.choice([-1.0, 1.0], size=nmax) if mode == "rand" else np.ones(nmax)
    errs_jet = np.full((nmax, 2), np.nan)
    errs_frozen = np.full((nmax, 2), np.nan)
    En, Ln = E0, L0
    for n in range(nmax):
        if mode == "E":
            En = En + eps * abs(1.0 - E0)          # deepen binding: inspiral-like
            truth = np.array(cycle(En, L0))
        else:
            Ln = Ln * (1.0 + eps * signs[n])
            truth = np.array(cycle(E0, Ln))
        if not np.all(np.isfinite(truth)):
            break  # left the bound regime (separatrix crossed)
        jet = f0 + J_L * (Ln - L0) + J_E * (En - E0)
        errs_jet[n] = np.abs(jet - truth) / np.abs(truth)
        errs_frozen[n] = np.abs(f0 - truth) / np.abs(truth)
    return errs_jet, errs_frozen


def first_cross(err, floor=FLOOR):
    idx = np.nonzero(np.isfinite(err) & (err > floor))[0]
    return (idx[0] + 1) if len(idx) else None  # 1-based cycle count


def curvature_C(p0, e0):
    """C = |f_LL L^2 / (2 f)| at the anchor, from a second difference."""
    E0, L0 = EL_from_pe(p0, e0)
    f0 = np.array(cycle(E0, L0))
    h = 1e-4 * L0
    fp = np.array(cycle(E0, L0 + h))
    fm = np.array(cycle(E0, L0 - h))
    return np.abs((fp - 2 * f0 + fm) * L0**2 / (2 * h**2 * f0))


def main():
    print("== P1: instrument control (quadrature dphi vs exact Darwin elliptic form) ==")
    print("   dphi_exact = 4 K(k) / sqrt(2 (u3-u1)),  k^2 = (u2-u1)/(u3-u1)")
    from scipy.special import ellipk
    worst = 0.0
    for e0 in (0.1, 0.5, 0.9, 0.995):
        for p0 in (20.0, 50.0):
            E0, L0 = EL_from_pe(p0, e0)
            dphi, _ = cycle(E0, L0)
            u1, u2 = (1 - e0) / p0, (1 + e0) / p0
            u3 = 0.5 - u1 - u2
            k2 = (u2 - u1) / (u3 - u1)
            closed = 4.0 * ellipk(k2) / np.sqrt(2.0 * (u3 - u1))
            rel = abs(dphi - closed) / closed
            worst = max(worst, rel)
            print(f"  p={p0:5.0f} e={e0:5.3f}  quad={dphi:.12f} closed={closed:.12f} rel={rel:.2e}")
    print(f"  worst rel = {worst:.2e}  -> {'OK (<1e-12)' if worst < 1e-12 else 'VOID: instrument broken'}")
    print("  (first run VOIDED: the control had used the precession 2*pi*(1/kappa-1),")
    print("   not the total advance 2*pi/kappa that the quadrature computes)")

    print("\n== C = |f_LL L^2 / 2f| at anchors (P3/P4 input) ==")
    for e0 in (0.5, 0.995):
        print(f"  e0={e0}: C(dphi)={curvature_C(20.0, e0)[0]:.3g}  C(dt)={curvature_C(20.0, e0)[1]:.3g}")

    print("\n== P2/P3/P4/P5: floor crossings (floor=1e-6, N=10^4 cycles) ==")
    print(f"{'p0':>4} {'e0':>6} {'eps':>8} {'mode':>4} | {'n*(dphi)':>9} {'n*(dt)':>9} | {'err@end dphi':>12} {'err@end dt':>12} | {'frozen n*(dphi)':>15} {'frozen n*(dt)':>15}")
    for e0 in (0.5, 0.995):
        for eps in (1e-6, 1e-4):
            for mode in ("sys", "rand", "E"):
                ej, ef = run_case(20.0, e0, eps, mode)
                fin = np.isfinite(ej[:, 0])
                last = np.nonzero(fin)[0][-1] if fin.any() else -1
                e_end = ej[last] if last >= 0 else (np.nan, np.nan)
                print(f"{20.0:4.0f} {e0:6.3f} {eps:8.1e} {mode:>4} | "
                      f"{str(first_cross(ej[:,0])):>9} {str(first_cross(ej[:,1])):>9} | "
                      f"{e_end[0]:12.3e} {e_end[1]:12.3e} | "
                      f"{str(first_cross(ef[:,0])):>15} {str(first_cross(ef[:,1])):>15}")

    print("\n== P6: implied re-anchor cost (38 crossings per n* kicks) ==")
    for e0 in (0.5, 0.995):
        for eps in (1e-6, 1e-4):
            ej, _ = run_case(20.0, e0, eps, "sys")
            ns = [n for n in (first_cross(ej[:, 0]), first_cross(ej[:, 1])) if n]
            nstar = min(ns) if ns else NMAX
            print(f"  e0={e0}, eps={eps:.0e}: n*={nstar}, re-anchor cost ~ 38/{nstar} = {38.0/nstar:.3g} crossings per kick")


if __name__ == "__main__":
    main()
