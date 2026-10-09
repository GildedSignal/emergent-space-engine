#!/usr/bin/env python3
"""Plunge tubes: one-real-root Darwin panels for Schwarzschild capture orbits.

Tube (candidate representation): cubic F(u) = 2L^2 u^3 - L^2 u^2 + 2u + E^2-1
(M=1, u=1/r) has ONE real root u1 + pair a+-ib for capture orbits.
Substitute u = u1 + rho*sin(psi)^2, rho = u_h - u1, u_h = 1/2:
    dphi/dpsi = sqrt(2 rho) cos(psi) / (L sqrt(Q)),   Q(u) = (u-a)^2 + b^2
    dtau/dpsi = sqrt(2 rho) cos(psi) / (L u^2 sqrt(Q))
    dv/dpsi   = (1 + L^2 u^2)/(E + sqrt(F)) * dtau/dpsi     [Eddington-Finkelstein]
All smooth on [psi_a, pi/2]; v is finite at the horizon.
Photon: F~(u) = 2u^3 - u^2 + 1/b^2, dphi/dpsi = sqrt(2 rho) cos(psi)/sqrt(Q),
dv/dphi = b/(1 + b sqrt(F~)).

Oracles (independent of the substitution):
  ODE in tau (or phi for photons), DOP853 rtol 1e-13, started AT the horizon,
  integrated backward; mpmath tanh-sinh at 40 dps for spot checks.
"""
import json, time
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
import mpmath as mp

mp.mp.dps = 40
M = 1.0
U_H = 0.5           # horizon in u
GLX, GLW = leggauss(4)
U_EDGE = 0.05       # doll-edge entry for direct infall (r = 20M)


def ucrit(E):
    """Unstable circular u_c for capture boundary; None if no critical orbit."""
    if 9 * E * E - 8 < 0:
        return None
    b = 3 * E * E - 4
    D = E * np.sqrt(9 * E * E - 8)
    # plus-branch root of 4u^2 + (3E^2-4)u + (1-E^2) = 0, cancellation-free
    return 2 * (1 - E * E) / (4 - 3 * E * E - D) if b > 0 else (-b + D) / 8.0


def Lcrit(E):
    uc = ucrit(E)
    return None if uc is None else 1.0 / np.sqrt(uc * (1 - 3 * uc))


def roots_of(E, L):
    """u1 (real), (a, b) of pair, from double-precision np.roots."""
    r = np.roots([2 * L * L, -L * L, 2.0, E * E - 1.0])
    real = r[np.abs(r.imag) < 1e-10]
    pair = r[np.abs(r.imag) >= 1e-10]
    assert len(real) == 1 and len(pair) == 2, f"root pattern {r}"
    return real[0].real, pair[0].real, abs(pair[0].imag)
def make_tube(E, L, n_panels=512, deg=4, u_start=None, photon_b=None):
    """Compile the crossing table: psi edges -> (u, Phi, Tau, V)."""
    if photon_b is not None:
        b = photon_b
        r = np.roots([2.0, -1.0, 0.0, 1.0 / (b * b)])
        real = r[np.abs(r.imag) < 1e-12]; pair = r[np.abs(r.imag) >= 1e-12]
        u1, a, bb = real[0].real, pair[0].real, abs(pair[0].imag)
        rho = U_H - u1
        if u_start is None: u_start = U_EDGE
        Q = lambda u: (u - a) ** 2 + bb * bb
        sqF = lambda u: np.sqrt(2 * (u - u1) * Q(u))
        dphidpsi = lambda p: np.sqrt(2 * rho) * np.cos(p) / np.sqrt(Q(u1 + rho * np.sin(p) ** 2))
        dvdpsi = lambda p: (b / (1 + b * sqF(u1 + rho * np.sin(p) ** 2))) * dphidpsi(p)
        integrands = (dphidpsi, lambda p: np.zeros_like(p), dvdpsi)  # no proper time for photons
    else:
        if L == 0.0:
            u1, a, bb = (1 - E * E) / 2.0, np.nan, np.nan   # cubic degenerates: F = 2(u-u1)
        else:
            u1, a, bb = roots_of(E, L)
        rho = U_H - u1
        Q = lambda u: (u - a) ** 2 + bb * bb if L > 0 else np.ones_like(np.atleast_1d(u) * 1.0)
        if L == 0.0:
            dphidpsi = lambda p: np.zeros_like(p)
            dtaudpsi = lambda p: np.sqrt(2 * rho) * np.cos(p) / (u1 + rho * np.sin(p) ** 2) ** 2
        else:
            # (du/dphi)^2 = F/L^2 and sqrt(F) = L sqrt(2(u-u1)Q): the L cancels for phi, stays for tau
            dphidpsi = lambda p: np.sqrt(2 * rho) * np.cos(p) / np.sqrt(Q(u1 + rho * np.sin(p) ** 2))
            dtaudpsi = lambda p: (np.sqrt(2 * rho) / L * np.cos(p)
                                  / ((u1 + rho * np.sin(p) ** 2) ** 2 * np.sqrt(Q(u1 + rho * np.sin(p) ** 2))))
        sqF = lambda u: L * np.sqrt(2 * (u - u1) * Q(u)) if L > 0 else np.sqrt(2 * (u - u1))
        dvdpsi = lambda p: (1 + L * L * (u1 + rho * np.sin(p) ** 2) ** 2) / (E + sqF(u1 + rho * np.sin(p) ** 2)) * dtaudpsi(p)
        integrands = (dphidpsi, dtaudpsi, dvdpsi)
        if u_start is None:
            u_start = u1 if u1 > 0 else U_EDGE   # apoapsis turn if u1>0, else edge entry
    psi_a = np.arcsin(np.sqrt(max(0.0, (u_start - u1) / rho)))
    assert u_start < U_H and psi_a < np.pi / 2
    edges = np.linspace(psi_a, np.pi / 2, n_panels + 1)
    h = edges[1] - edges[0]
    gx, gw = (GLX, GLW) if deg == 4 else leggauss(deg)
    nodes = (edges[:-1, None] + h / 2 * (1 + gx[None, :])).ravel()
    wts = np.tile(gw * h / 2, n_panels)
    # per-panel GL sums, cumsum -> crossing table at panel edges
    Phi, Tau, Vv = [np.concatenate(([0.0], np.cumsum((f(nodes) * wts).reshape(n_panels, deg).sum(axis=1))))
                    for f in integrands]
    return dict(E=E, L=L, b=photon_b, u1=u1, a=a, bb=bb, rho=rho,
                psi_a=psi_a, psi=edges, u=u1 + rho * np.sin(edges) ** 2,
                Phi=Phi, Tau=Tau, V=Vv, dphidpsi=integrands[0])


def oracle_massive(E, L, tau_targets, tube):
    """Backward-from-horizon DOP853 in tau; returns u,phi,v at -tau_targets."""
    def rhs(tau, y):
        u = y[0]
        F = E * E - (1 - 2 * u) * (1 + L * L * u * u)
        s = np.sqrt(max(F, 0.0))
        return [u * u * s, L * u * u, (1 + L * L * u * u) / (E + s)]
    u_start = tube["u"][0]
    y0 = [U_H * (1 - 1e-13), 0.0, 0.0]
    def hit_start(tau, y): return y[0] - u_start
    hit_start.terminal = True; hit_start.direction = -1
    tau_tot = float(tube["Tau"][-1])
    sol = solve_ivp(rhs, [0.0, -(tau_tot * 1.05 + 1e-9)], y0, method="DOP853",
                    rtol=1e-13, atol=1e-15, dense_output=True, events=hit_start)
    neg = -(tau_tot - np.asarray(tau_targets))   # tube tau counts apoapsis->horizon
    ok = neg >= sol.t[-1]
    Y = sol.sol(np.clip(neg, sol.t[-1], 0.0))
    return Y[0], Y[1], Y[2], ok


def oracle_photon(b, phi_targets, tube):
    def rhs(phi, y):
        u = y[0]
        F = 1 / (b * b) - u * u + 2 * u ** 3
        s = np.sqrt(max(F, 0.0))
        return [s, b / (1 + b * s)]
    u_start = tube["u"][0]
    y0 = [u_start, 0.0]
    def hit_h(phi, y): return y[0] - U_H
    phi_tot = float(tube["Phi"][-1])
    sol = solve_ivp(rhs, [0.0, phi_tot * 1.05], y0, method="DOP853",
                    rtol=1e-13, atol=1e-15, dense_output=True, events=hit_h)
    ph = np.clip(np.asarray(phi_targets), 0.0, sol.t[-1])
    Y = sol.sol(ph)
    return Y[0], Y[1]


def mp_check_massive(E, L, tube, k=8):
    """40-dps tanh-sinh check of the psi integrals at k edges (shares only algebra)."""
    u1, a, bb, rho = tube["u1"], tube["a"], tube["bb"], tube["rho"]
    out = []
    for i in np.linspace(1, len(tube["psi"]) - 2, k).astype(int):
        p = mp.mpf(float(tube["psi"][i]))
        def f_phi(p): return mp.sqrt(2 * rho) * mp.cos(p) / mp.sqrt((u1 + rho * mp.sin(p) ** 2 - a) ** 2 + bb ** 2)
        def f_tau(p): return (mp.sqrt(2 * rho) / L * mp.cos(p)
                              / ((u1 + rho * mp.sin(p) ** 2) ** 2 * mp.sqrt((u1 + rho * mp.sin(p) ** 2 - a) ** 2 + bb ** 2)))
        Phi = mp.quad(f_phi, [mp.mpf(float(tube["psi"][0])), p])
        Tau = mp.quad(f_tau, [mp.mpf(float(tube["psi"][0])), p])
        u = u1 + rho * mp.sin(p) ** 2
        sqF = L * mp.sqrt(2 * (u - u1) * ((u - a) ** 2 + bb ** 2))
        V = mp.quad(lambda q: (1 + L * L * (u1 + rho * mp.sin(q) ** 2) ** 2) / (E + L * mp.sqrt(
            2 * (u1 + rho * mp.sin(q) ** 2 - u1) * ((u1 + rho * mp.sin(q) ** 2 - a) ** 2 + bb ** 2)))
            * f_tau(q), [mp.mpf(float(tube["psi"][0])), p])
        out.append((i, float(Phi), float(Tau), float(V)))
    return out


def relerr(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    d = np.abs(x - y)
    s = np.maximum(np.abs(y), 1e-300)
    return d / s


def case_massive(name, E, L, n_panels=512, verbose=True):
    t0 = time.perf_counter()
    tube = make_tube(E, L, n_panels=n_panels)
    t_compile = time.perf_counter() - t0
    idx = sorted(set(np.linspace(1, n_panels - 1, 32).astype(int)))
    tau_t = tube["Tau"][idx]
    u_o, phi_o, v_o, ok = oracle_massive(E, L, tau_t, tube)
    tube_u = tube["u"][idx]; tube_phi = tube["Phi"][idx]; tube_v = tube["V"][idx]
    e_r = relerr(1.0 / tube_u, 1.0 / u_o)[ok]
    e_phi = relerr(tube_phi, tube["Phi"][-1] + phi_o)[ok]   # oracle phi counts back from the horizon
    e_v = relerr(tube_v, tube["V"][-1] + v_o)[ok]
    res = dict(case=name, E=E, L=L, u1=tube["u1"], DeltaPhi=float(tube["Phi"][-1]),
               DeltaTau=float(tube["Tau"][-1]), DeltaV=float(tube["V"][-1]),
               max_rel_r=float(e_r.max()), max_rel_phi=float(e_phi.max()),
               max_rel_v=float(e_v.max()), n_ok=int(ok.sum()),
               compile_ms=t_compile * 1e3, u1_sign=("apoapsis" if tube["u1"] > 0 else "direct"))
    if verbose:
        print(f"{name:18s} E={E:8.3g} L={L:9.4g} u1={tube['u1']:+.6g} "
              f"dPhi={res['DeltaPhi']:9.4f} dTau={res['DeltaTau']:.6g} dV={res['DeltaV']:.6g} | "
              f"r:{e_r.max():.2e} phi:{e_phi.max():.2e} v:{e_v.max():.2e} n={ok.sum()}")
    return tube, res


def main():
    Lc97 = Lcrit(0.97); Lc12 = Lcrit(1.2); Lc2000 = Lcrit(2000.0)
    cases = [
        ("A apoapsis E0.8", 0.8, 3.8),
        ("B apoapsis E0.97", 0.97, 0.9 * Lc97),
        ("C direct E1", 1.0, 0.9 * 4.0),
        ("D direct E1.2", 1.2, 0.99 * Lc12),
        ("E gamma2000", 2000.0, 0.99 * Lc2000),
        ("F radial L0", 1.0, 0.0),
    ]
    print(f"Lcrit(0.97)={Lc97:.6f} Lcrit(1.2)={Lc12:.6f} Lcrit(2000)={Lc2000:.6f} (photon lim {3*np.sqrt(3):.6f})")
    results = {}
    tubes = {}
    for name, E, L in cases:
        tube, res = case_massive(name, E, L)
        results[name[0]] = res; tubes[name[0]] = tube

    # Photon capture
    bc = 3 * np.sqrt(3); b = 0.9 * bc
    tube = make_tube(0, 0, photon_b=b)
    idx = sorted(set(np.linspace(1, 511, 32).astype(int)))
    phi_t = tube["Phi"][idx]
    u_o, v_o = oracle_photon(b, phi_t, tube)
    e_r = relerr(1.0 / tube["u"][idx], 1.0 / u_o)
    e_v = relerr(tube["V"][idx], v_o)
    print(f"{'G photon b=0.9bc':18s} u1={tube['u1']:+.6g} dPhi={tube['Phi'][-1]:9.4f} "
          f"dV={tube['V'][-1]:.6g} | r:{e_r.max():.2e} v:{e_v.max():.2e}")
    results["G"] = dict(case="photon", b=b, u1=tube["u1"], DeltaPhi=float(tube["Phi"][-1]),
                        DeltaV=float(tube["V"][-1]), max_rel_r=float(e_r.max()), max_rel_v=float(e_v.max()))

    # 40-dps tanh-sinh spot check, case C
    tube = tubes["C"]
    mc = mp_check_massive(1.0, 0.9 * 4.0, tube)
    errs = [(abs(tube["Phi"][i] - P), abs(tube["Tau"][i] - T), abs(tube["V"][i] - V)) for i, P, T, V in mc]
    ep = max(e[0] for e in errs); et = max(e[1] for e in errs); ev = max(e[2] for e in errs)
    print(f"mpmath 40dps spot (C): dPhi={ep:.2e} dTau={et:.2e} dV={ev:.2e}")
    results["mpcheck_C"] = dict(dPhi=ep, dTau=et, dV=ev)

    with open("plunge_main.json", "w") as f:
        json.dump(results, f, indent=1)


if __name__ == "__main__":
    main()
