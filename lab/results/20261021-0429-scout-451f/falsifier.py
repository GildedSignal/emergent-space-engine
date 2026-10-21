#!/usr/bin/env python3
"""Exponential-map member congruences vs the deviation ODE (fleet-doll-speed od 5).

Schwarzschild M=1. Instruments (all numpy, no sympy at runtime):
  - Christoffels hand-coded (verified against sympy, notebook of this run);
  - Riemann: static-orthonormal pair components R_{trtr}=-2/r^3, R_{tttt}=0,
    R_{thth}=R_{phph}=+1/r^3, R_{rthr}=R_{rphr}=-1/r^3, R_{thphthph}=+2/r^3,
    E(u) built as sum of outer products and rotated into the parallel-transported
    tetrad (validated by the periapsis eigenvalue control vs 4c79's certified
    closed forms);
  - reference geodesic + parallel tetrad, RK4 shared step;
  - members: exponential-map ICs (position O(xi^2), velocity O(xi); the residual
    floor is exposed by the xi sweep);
  - truth: member geodesics; Fermi coords by the O(xi^2) log-map inversion;
  - prediction: d2xi/dtau2 = -E(u) xi.
Modes: control | flyby | circular. All output JSON to stdout.
"""
import json
import sys
import numpy as np

M = 1.0


def gamma_at(x):
    r, th = x[1], x[2]
    f = 1 - 2 * M / r
    s, c = np.sin(th), np.cos(th)
    G = np.zeros((4, 4, 4))
    G[0, 0, 1] = G[0, 1, 0] = 1 / (r * (r - 2 * M))
    G[1, 0, 0] = (r - 2 * M) / r**3
    G[1, 1, 1] = -1 / (r * (r - 2 * M))
    G[1, 2, 2] = 2 * M - r
    G[1, 3, 3] = (2 * M - r) * s * s
    G[2, 1, 2] = G[2, 2, 1] = 1 / r
    G[2, 3, 3] = -s * c
    G[3, 1, 3] = G[3, 3, 1] = 1 / r
    G[3, 2, 3] = G[3, 3, 2] = c / s
    return G


def metric_at(x):
    r, th = x[1], x[2]
    f = 1 - 2 * M / r
    return np.diag([-f, 1 / f, r * r, r * r * np.sin(th) ** 2])


def static_tetrad(x):
    r, th = x[1], x[2]
    f = 1 - 2 * M / r
    return np.stack([np.array([1 / np.sqrt(f), 0, 0, 0]),
                     np.array([0, np.sqrt(f), 0, 0]),
                     np.array([0, 0, 1 / r, 0]),
                     np.array([0, 0, 0, 1 / (r * np.sin(th))])])


def E_of_u(x, u, tetT):
    """E(u)_ab = R_{a mu b nu} u^mu u^nu in the transported tetrad (tetT[b,mu]=e_b^mu).

    Static-orthonormal Riemann has only the 6 pair components; E in the static
    frame is the outer-product sum, then rotated by Lambda = (S^T)^{-1} tet."""
    r = x[1]
    st = static_tetrad(x)
    Lam = np.linalg.solve(st.T, tetT.T).T          # Lam[a, A]
    ust = np.linalg.solve(st.T, u)                  # static components of u
    om = {}
    for A in range(4):
        for B in range(4):
            if A < B:
                Wm = np.zeros((4, 4))
                Wm[A, B], Wm[B, A] = 1.0, -1.0
                om[(A, B)] = Wm
    c = {(0, 1): -2 * M / r**3, (0, 2): M / r**3, (0, 3): M / r**3,
         (1, 2): -M / r**3, (1, 3): -M / r**3, (2, 3): 2 * M / r**3}
    Est = np.zeros((4, 4))
    for P, cp in c.items():
        v = om[P] @ ust
        Est += cp * np.outer(v, v)
    return Lam @ Est @ Lam.T


def make_member_ic(x0, u0, tetT, xi_vec):
    w = tetT.T @ xi_vec                       # coordinate displacement, O(xi)
    Gm = gamma_at(x0)
    x = x0 + w - 0.5 * np.einsum("mab,a,b->m", Gm, w, w)
    u = u0 + np.einsum("mab,a,b->m", Gm, u0, w)
    return x, u

def fermi_coords(xm, x0, tetT):
    d = xm - x0
    g4 = metric_at(x0)
    signs = np.array([-1.0, 1.0, 1.0, 1.0])
    dc = signs * (tetT @ g4 @ d)          # dual-tetrad projection X^a = eta^{aa} e_a.g.d
    Gm = gamma_at(x0)
    Gtet = np.einsum("am,bn,co,mno->abc", tetT, tetT, tetT, Gm)
    return dc + 0.5 * np.einsum("cab,a,b->c", Gtet, dc, dc)


def init_reference(rp, beta, kind):
    x = np.array([0.0, rp, np.pi / 2, 0.0])
    f = 1 - 2 * M / rp
    st = static_tetrad(x)
    if kind == "flyby":
        g = 1 / np.sqrt(1 - beta**2)
        u = g * (st[0] + beta * st[3])
        e2 = g * (beta * st[0] + st[3])
        tet = np.stack([u, st[1], e2, st[2]])
    else:
        u = np.array([1 / np.sqrt(1 - 3 * M / rp), 0, 0,
                      np.sqrt(M / rp**3) / np.sqrt(1 - 3 * M / rp)])
        e2 = st[3] + (st[3] @ metric_at(x) @ u) * u
        e2 = e2 / np.sqrt(e2 @ metric_at(x) @ e2)
        tet = np.stack([u, st[1], e2, st[2]])
    beta_loc = float(np.linalg.norm(np.linalg.solve(st.T, u)[1:4]))
    return x, u, tet, beta_loc


def run(kind, rp, beta, offs, xis, n_orbits=600, spo=300):
    x0, u0, tet, _ = init_reference(rp, beta, kind)
    tetT = tet.copy()
    E0 = E_of_u(x0, u0, tetT)
    ev = np.sort(np.linalg.eigvalsh(E0[1:4, 1:4]) / (M / rp**3))
    # members
    mem = []
    for alpha in offs:
        for xi0 in xis:
            xi_vec = np.zeros(4)
            if alpha == "z":
                xi_vec[3] = xi0 * rp
            else:
                xi_vec[1] = np.cos(alpha) * xi0 * rp
                xi_vec[2] = np.sin(alpha) * xi0 * rp
            xm, um = make_member_ic(x0, u0, tetT, xi_vec)
            mem.append((alpha, xi0, xm, um, xi_vec))
    n = len(mem)
    xs = np.array([m[2] for m in mem])
    us = np.array([m[3] for m in mem])
    xis_state = np.zeros((n, 8))
    for i, m in enumerate(mem):
        xis_state[i, 1:4] = m[4][1:4]
    x, u = x0.copy(), u0.copy()
    if kind == "flyby":
        nsteps, h = 4000, (8.0 * rp / max(beta, 0.25)) / 4000.0
        snaps = {nsteps - 1}
    else:
        Om = np.sqrt(M / rp**3) / np.sqrt(1 - 3 * M / rp)
        nsteps = n_orbits * spo
        h = 2 * np.pi / Om / spo
        snaps = {int(nsteps * fr) - 1 for fr in (0.02, 0.1, 0.5, 1.0)}
    checks = {}
    E = E_of_u(x, u, tetT)
    for step in range(nsteps):
        # reference + tetrad (RK4)
        def Fref(y):
            xx, uu, tt = y[:4], y[4:8], y[8:].reshape(4, 4)
            Gm = gamma_at(xx)
            return np.concatenate([uu, -np.einsum("mab,a,b->m", Gm, uu, uu),
                                   -np.einsum("mab,a,cb->cm", Gm, uu, tt.reshape(4, 4)).ravel()])
        y = np.concatenate([x, u, tetT.ravel()])
        k1 = Fref(y); k2 = Fref(y + 0.5 * h * k1); k3 = Fref(y + 0.5 * h * k2); k4 = Fref(y + h * k3)
        y = y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        x, u, tetT = y[:4], y[4:8], y[8:].reshape(4, 4)
        E = E_of_u(x, u, tetT)
        # members (batched RK4)
        def Fm(ym):
            xx, uu = ym[:, :4], ym[:, 4:]
            Gm = gamma_at(x)  # same point approximation is WRONG; recompute per member
            out = np.empty_like(ym)
            out[:, :4] = uu
            for i in range(ym.shape[0]):
                Gmi = gamma_at(xx[i])
                out[i, 4:] = -np.einsum("mab,a,b->m", Gmi, uu[i], uu[i])
            return out
        def Fxi(yxi):
            o = np.empty_like(yxi)
            o[:, :4] = yxi[:, 4:]
            o[:, 4:] = -np.einsum("ab,nb->na", E, yxi[:, :4])
            return o
        if n:
            k1 = Fm(np.concatenate([xs, us], 1)); k2 = Fm(np.concatenate([xs, us], 1) + 0.5 * h * k1)
            k3 = Fm(np.concatenate([xs, us], 1) + 0.5 * h * k2); k4 = Fm(np.concatenate([xs, us], 1) + h * k3)
            ym = np.concatenate([xs, us], 1) + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
            xs, us = ym[:, :4], ym[:, 4:]
            k1 = Fxi(xis_state); k2 = Fxi(xis_state + 0.5 * h * k1); k3 = Fxi(xis_state + 0.5 * h * k2)
            k4 = Fxi(xis_state + h * k3)
            xis_state = xis_state + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        if step in snaps:
            for i, m in enumerate(mem):
                X = fermi_coords(xs[i], x, tetT)
                err = np.linalg.norm(X[1:4] - xis_state[i, 1:4]) / (m[1] * rp)
                checks.setdefault((m[0], m[1]), {})[step] = float(err)
    drift = abs(u @ metric_at(x) @ u + 1)
    mdrift = max(abs(us[i] @ metric_at(xs[i]) @ us[i] + 1) for i in range(n)) if n else 0.0
    return {"eigs_norm": ev.tolist(), "u_drift": float(drift), "member_u_drift": float(mdrift),
            "checkpoints": {f"{a}|{x_}": {str(k): v for k, v in d.items()} for (a, x_), d in checks.items()}}


if __name__ == "__main__":
    mode = sys.argv[1]
    out = {}
    if mode == "control":
        for rp, beta in [(18, 0.25), (18, 0.5), (18, 0.9), (18, 0.95), (100, 0.5), (100, 0.9), (6, 0.9)]:
            g = 1 / np.sqrt(1 - beta**2)
            closed = sorted([-g**2 * (2 + beta**2), 1.0, g**2 * (1 + 2 * beta**2)])
            res = run("flyby", rp, beta, offs=[], xis=[])
            out[f"rp{rp}_b{beta}"] = {"measured": res["eigs_norm"], "closed": closed,
                                      "u_drift": res["u_drift"]}
    elif mode == "flyby":
        grid = []
        for rp in (18,):
            for beta in (0.5, 0.9, 0.95):
                res = run("flyby", rp, beta, offs=[0.0, np.pi / 4, np.pi / 2, "z"],
                          xis=[1e-4, 1e-3, 3e-2])
                grid.append({"rp": rp, "beta": beta, **res})
        out["flyby"] = grid
    elif mode == "circular":
        grid = []
        for rp in (18,):
            res = run("circular", rp, 0.0, offs=[0.0, np.pi / 2, "z"],
                      xis=[1e-3, 1e-2, 3e-2], n_orbits=600, spo=300)
            grid.append({"rp": rp, **res})
        out["circular"] = grid
    print(json.dumps(out, indent=1, default=float))
