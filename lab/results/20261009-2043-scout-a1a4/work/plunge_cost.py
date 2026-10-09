#!/usr/bin/env python3
"""Tier C: near-critical divergence, root precision, and cost of plunge tubes."""
import time
import numpy as np
import mpmath as mp
from scipy.integrate import solve_ivp
from plunge_falsifier import make_tube, Lcrit, U_H, roots_of

mp.mp.dps = 40


def dphi_mp(E, L):
    """DeltaPhi from psi_a to pi/2 at 40 dps (mp.quad, adaptive)."""
    u1, a, b = roots_of(E, L)
    rho = U_H - u1
    if u1 > 0:
        psi_a = mp.mpf("0")
    else:
        psi_a = mp.asin(mp.sqrt(mp.mpf("0.05") / rho))
    f = lambda p: mp.sqrt(2 * rho) * mp.cos(p) / mp.sqrt((u1 + rho * mp.sin(p) ** 2 - a) ** 2 + b * b)
    return mp.quad(f, [psi_a, mp.pi / 2]), u1, a, b


def main():
    E = 1.0
    Lc = Lcrit(E)
    print("== near-critical scan (E=1), L = Lc*(1-10^-k) ==")
    print(f"{'k':>2} {'DeltaPhi(mp40)':>16} {'d_k':>8} {'u1 err (np vs mp50)':>20} {'pair b':>10} {'512-panel dPhi err':>18}")
    prev = None
    for k in range(1, 8):
        L = Lc * (1 - 10.0 ** (-k))
        dphi, u1, a, b = dphi_mp(E, L)
        # double-precision roots vs 50-dp polyroots
        mp.mp.dps = 50
        rp = mp.polyroots([2 * mp.mpf(L) ** 2, -mp.mpf(L) ** 2, 2, mp.mpf(E) ** 2 - 1])
        reals = [r for r in rp if abs(mp.im(r)) < mp.mpf("1e-30")]
        u1_true = reals[0]
        mp.mp.dps = 40
        u1_err = abs(mp.mpf(float(u1)) - u1_true) / max(abs(u1_true), mp.mpf("1e-30"))
        # fixed 512 GL4-panel tube error in DeltaPhi
        tube = make_tube(E, L, n_panels=512)
        dphi_t = tube["Phi"][-1]
        panel_err = abs(mp.mpf(float(dphi_t)) - dphi) / dphi
        d_k = (float(dphi) - prev) if prev is not None else float("nan")
        print(f"{k:>2} {float(dphi):>16.4f} {d_k:>8.3f} {float(u1_err):>20.3e} {b:>10.3e} {float(panel_err):>18.3e}")
        prev = float(dphi)

    print("\n== cost, case C (E=1, L=3.6), 512 GL4 panels ==")
    E, L = 1.0, 0.9 * 4.0
    t0 = time.perf_counter()
    for _ in range(100):
        tube = make_tube(E, L, n_panels=512)
    t_compile = (time.perf_counter() - t0) / 100 * 1e3
    tau_edges = tube["Tau"]; psi_edges = tube["psi"]
    rng = np.random.default_rng(0)
    taus = rng.uniform(tau_edges[1], tau_edges[-2], 1000)
    t0 = time.perf_counter()
    us = []
    for tt in taus:   # O(1) readout: panel index + linear interp + u lookup
        j = np.searchsorted(tau_edges, tt) - 1
        w = (tt - tau_edges[j]) / (tau_edges[j + 1] - tau_edges[j])
        us.append(tube["u"][j] + w * (tube["u"][j + 1] - tube["u"][j]))
    t_sample = (time.perf_counter() - t0) / 1000 * 1e6
    print(f"compile: {t_compile:.3f} ms   table readout sample: {t_sample:.3f} us/sample")

    # DOP853 at rtol 1e-12 for the same plunge, forward from apoapsis edge
    def rhs(tau, y):
        u = y[0]
        F = E * E - (1 - 2 * u) * (1 + L * L * u * u)
        s = np.sqrt(max(F, 0.0))
        return [u * u * s, L * u * u]
    t0 = time.perf_counter()
    sol = solve_ivp(rhs, [0, float(tube["Tau"][-1])], [tube["u"][0], 0.0],
                    method="DOP853", rtol=1e-12, atol=1e-14)
    t_ode = (time.perf_counter() - t0) * 1e3
    print(f"DOP853 rtol=1e-12 whole plunge: {t_ode:.3f} ms, nfev={sol.nfev}, "
          f"phi_end={sol.y[1][-1]:.6f} (tube {tube['Phi'][-1]:.6f})")


if __name__ == "__main__":
    main()
