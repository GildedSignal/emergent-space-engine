#!/usr/bin/env python3
"""Second author on 451f (fleet-doll-speed, od 1 of the corrected page): the
checker's two one-line fixes, a third instrument fix held to a measurement
(the Fermi log-map's dual projection), then the full grid.

Fix 1 (member-IC sign, the checker's x70/x1e4 probe): make_member_ic
PARALLEL-transports the reference tangent along the separation,
    u_m = u0 - Gamma(u0, w)          (was u0 + Gamma(u0, w), anti-parallel)
and normalizes the tangent so the member's affine parameter is proper time
(the truncated transport's O(xi^2) norm violation is a pure parameterization
artifact).  icsign=+1, normalize=False reproduces 451f's IC exactly.

Fix 2 (E-sampling, kills the O(h) floor): the deviation ODE is advanced by RK4
with E(u) evaluated at the four RK4 stage states of the reference step — RK4
on the coupled (reference, member, xi) system, 4th order in h.  esample=
"frozen" (E at the step's end state for all stages) reproduces 451f.

Fix 3 (map dual, held to the exact exponential map): fermi_coords' quadratic
term now projects the Christoffel's upper index with the DUAL tetrad
(mapdual=True).  The map control mode judges old vs new against geodesics of
the true exponential map; the measurement decides, not the derivation.

Modes (JSON to stdout): control | flyby | conv | mapcheck
Schwarzschild M=1, equatorial; flyby starts at periapsis, tau_total = 8 rp/beta
(identical to 451f).  err := |xi_fermi(member) - xi_ODE| / (xi0*rp).
"""
import json
import sys
import numpy as np

M = 1.0


def gamma_at(x):
    r, th = x[1], x[2]
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
    """E(u)_ab = R_{a mu b nu} u^mu u^nu in the transported tetrad (tetT[b,mu]=e_b^mu)."""
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


def geod_step(xs_, us_, hh):
    k1 = np.concatenate([us_, acc_vec(xs_[None], us_[None])[0]])
    u2 = us_ + 0.5 * hh * k1[4:]
    k2 = np.concatenate([u2, acc_vec((xs_ + 0.5 * hh * k1[:4])[None], u2[None])[0]])
    u3 = us_ + 0.5 * hh * k2[4:]
    k3 = np.concatenate([u3, acc_vec((xs_ + 0.5 * hh * k2[:4])[None], u3[None])[0]])
    u4 = us_ + hh * k3[4:]
    k4 = np.concatenate([u4, acc_vec((xs_ + hh * k3[:4])[None], u4[None])[0]])
    y = np.concatenate([xs_, us_]) + (hh / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
    return y[:4], y[4:]


def make_member_ic(x0, u0, tetT, xi_vec, icsign=-1, normalize=True):
    """Exponential-map member IC: position to O(xi^2); velocity = PARALLEL
    transport of u0 along w to O(xi) (FIX 1: icsign=-1; +1 = 451f), optionally
    normalized to unit norm (proper-time parameter)."""
    w = tetT.T @ xi_vec                       # coordinate displacement, O(xi)
    Gm = gamma_at(x0)
    x = x0 + w - 0.5 * np.einsum("mab,a,b->m", Gm, w, w)
    u = u0 + icsign * np.einsum("mab,a,b->m", Gm, u0, w)
    if normalize:
        u = u / np.sqrt(abs(u @ metric_at(x) @ u))
    return x, u


def fermi_coords(xm, x0, tetT, mapdual=True):
    """O(xi^2) log-map inversion.  mapdual=True: Christoffel upper index on the
    DUAL tetrad (algebraically correct inverse); False: 451f's all-vector form."""
    d = xm - x0
    g4 = metric_at(x0)
    signs = np.array([-1.0, 1.0, 1.0, 1.0])
    dc = signs * (tetT @ g4 @ d)
    Gm = gamma_at(x0)
    if mapdual:
        dual = signs[:, None] * (tetT @ g4)
        Gtet = np.einsum("cm,an,bo,mno->cab", dual, tetT, tetT, Gm)
    else:
        Gtet = np.einsum("am,bn,co,mno->cab", tetT, tetT, tetT, Gm)
    return dc + 0.5 * np.einsum("cab,a,b->c", Gtet, dc, dc)


def make_member_ic_exact(x0, u0, tetT, xi_vec, nsub=2000):
    """All-order comoving member IC: parallel-transport u0 along the TRUE
    exponential-map geodesic (tangent xi^i e_i, unit affine parameter)."""
    v = tetT[1:4, :].T @ xi_vec[1:4]

    def F(y):
        xx, t, up = y[:4], y[4:8], y[8:]
        Gm = gamma_at(xx)
        return np.concatenate([t,
                               -np.einsum("mab,a,b->m", Gm, t, t),
                               -np.einsum("mab,a,b->m", Gm, up, t)])

    y = np.concatenate([x0, v, u0])
    hh = 1.0 / nsub
    for _ in range(nsub):
        k1 = F(y); k2 = F(y + 0.5 * hh * k1); k3 = F(y + 0.5 * hh * k2); k4 = F(y + hh * k3)
        y = y + (hh / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
    xm, um = y[:4], y[8:]
    return xm, um / np.sqrt(abs(um @ metric_at(xm) @ um))




def exp_map_exact(x0, tetT, xi_vec, nsub=20000):
    """True exponential map: geodesic with tangent xi^i e_i, unit affine
    parameter (ground truth for the map control)."""
    v = tetT[1:4, :].T @ xi_vec[1:4]
    xs_, us_ = x0.copy(), v.copy()
    hh = 1.0 / nsub
    for _ in range(nsub):
        xs_, us_ = geod_step(xs_, us_, hh)
    return xs_


def init_reference(rp, beta, kind):
    x = np.array([0.0, rp, np.pi / 2, 0.0])
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
    return x, u, tet


def acc_vec(xs, us):
    """Geodesic RHS d2x/dtau2 = -Gamma(u,u) for a batch (vectorized Schwarzschild)."""
    r, th = xs[:, 1], xs[:, 2]
    ut, ur, uth, uph = us[:, 0], us[:, 1], us[:, 2], us[:, 3]
    s, c = np.sin(th), np.cos(th)
    rr = r * (r - 2 * M)
    a = np.empty_like(us)
    a[:, 0] = -2.0 * ut * ur / rr
    a[:, 1] = -((r - 2 * M) / r**3 * ut * ut - ur * ur / rr
                + (2 * M - r) * (uth * uth + s * s * uph * uph))
    a[:, 2] = -(2.0 * ur * uth / r - s * c * uph * uph)
    a[:, 3] = -(2.0 * (ur * uph / r + uth * uph * c / s))
    return a


def fl(a):
    return "z" if a == "z" else float(a)


def run(kind, rp, beta, offs, xis, nsteps=4000, esample="stage", icsign=-1,
        normalize=True, mapdual=True, ic="trunc", snap_fr=(0.02, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0),
        first_step_only=False):
    x0, u0, tet = init_reference(rp, beta, kind)
    tetT = tet.copy()
    E0 = E_of_u(x0, u0, tetT)
    ev = np.sort(np.linalg.eigvalsh(E0[1:4, 1:4]) / (M / rp**3))
    # members + tau=0 diagnostics
    mem, diag0, X0_all = [], [], []
    for alpha in offs:
        for xi0 in xis:
            xi_vec = np.zeros(4)
            if alpha == "z":
                xi_vec[3] = xi0 * rp
            else:
                xi_vec[1] = np.cos(alpha) * xi0 * rp
                xi_vec[2] = np.sin(alpha) * xi0 * rp
            if ic == "exact":
                xm, um = make_member_ic_exact(x0, u0, tetT, xi_vec)
            else:
                xm, um = make_member_ic(x0, u0, tetT, xi_vec, icsign=icsign, normalize=normalize)
            X0 = fermi_coords(xm, x0, tetT, mapdual=mapdual)
            mem.append((alpha, xi0, xm, um, xi_vec))
            X0_all.append(X0)
            diag0.append({"alpha": fl(alpha), "xi": xi0,
                          "udrift0": float(abs(um @ metric_at(xm) @ um + 1)),
                          "roundtrip0": float(np.linalg.norm(X0[1:4] - xi_vec[1:4]) / (xi0 * rp))})
    n = len(mem)
    xs = np.array([m[2] for m in mem]) if n else np.zeros((0, 4))
    us = np.array([m[3] for m in mem]) if n else np.zeros((0, 4))
    xis_state = np.zeros((n, 8))
    for i, m in enumerate(mem):
        xis_state[i, 1:4] = m[4][1:4]
    x, u = x0.copy(), u0.copy()
    if kind == "flyby":
        h = (8.0 * rp / max(beta, 0.25)) / nsteps
    else:
        Om = np.sqrt(M / rp**3) / np.sqrt(1 - 3 * M / rp)
        h = 2 * np.pi / Om / 300
    snaps = {max(0, min(nsteps - 1, int(nsteps * fr) - 1)): fr for fr in snap_fr}
    checks = {}
    rr_snap = {}
    vrel0_fd = None
    for step in range(nsteps):

        def Fref(y):
            xx, uu, tt = y[:4], y[4:8], y[8:].reshape(4, 4)
            Gm = gamma_at(xx)
            return np.concatenate([uu, -np.einsum("mab,a,b->m", Gm, uu, uu),
                                   -np.einsum("mab,a,cb->cm", Gm, uu, tt.reshape(4, 4)).ravel()])

        def Fm(xm_, um_):
            out = np.empty((xm_.shape[0], 8))
            out[:, :4] = um_
            out[:, 4:] = acc_vec(xm_, um_)
            return out

        def E_at(y):
            return E_of_u(y[:4], y[4:8], y[8:].reshape(4, 4))

        def Fxi(yxi, Ecur):
            o = np.empty_like(yxi)
            o[:, :4] = yxi[:, 4:]
            o[:, 4:] = -np.einsum("ab,nb->na", Ecur, yxi[:, :4])
            return o

        y = np.concatenate([x, u, tetT.ravel()])
        k1 = Fref(y); y1 = y + 0.5 * h * k1
        k2 = Fref(y1); y2 = y + 0.5 * h * k2
        k3 = Fref(y2); y3 = y + h * k3
        k4 = Fref(y3)
        # FIX 2: E at the four stage states (coupled RK4); "frozen" reproduces 451f
        if esample == "stage":
            Est = [E_at(y), E_at(y1), E_at(y2), E_at(y3)]
        else:
            Ef = E_at(y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4))
            Est = [Ef, Ef, Ef, Ef]
        if n:
            mk1 = Fm(xs, us)
            mk2 = Fm(xs + 0.5 * h * mk1[:, :4], us + 0.5 * h * mk1[:, 4:])
            mk3 = Fm(xs + 0.5 * h * mk2[:, :4], us + 0.5 * h * mk2[:, 4:])
            mk4 = Fm(xs + h * mk3[:, :4], us + h * mk3[:, 4:])
            ym = np.concatenate([xs, us], 1) + (h / 6) * (mk1 + 2 * mk2 + 2 * mk3 + mk4)
            xs, us = ym[:, :4], ym[:, 4:]
            xk1 = Fxi(xis_state, Est[0])
            xk2 = Fxi(xis_state + 0.5 * h * xk1, Est[1])
            xk3 = Fxi(xis_state + 0.5 * h * xk2, Est[2])
            xk4 = Fxi(xis_state + h * xk3, Est[3])
            xis_state = xis_state + (h / 6) * (xk1 + 2 * xk2 + 2 * xk3 + xk4)
        y = y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        x, u, tetT = y[:4], y[4:8], y[8:].reshape(4, 4)
        if step == 0 and n:
            vrel0_fd = [float(np.linalg.norm(fermi_coords(xs[i], x, tetT, mapdual=mapdual)[1:4]
                                             - X0_all[i][1:4]) / h / (mem[i][1] * rp))
                        for i in range(n)]
            if first_step_only:
                break
        if step in snaps:
            checks[snaps[step]] = []
            rr_snap[str(snaps[step])] = float(x[1] / rp)
            for i, m in enumerate(mem):
                X = fermi_coords(xs[i], x, tetT, mapdual=mapdual)
                err = np.linalg.norm(X[1:4] - xis_state[i, 1:4]) / (m[1] * rp)
                checks[snaps[step]].append([fl(m[0]), m[1], float(err)])
    drift = abs(u @ metric_at(x) @ u + 1)
    eta = np.diag([-1.0, 1.0, 1.0, 1.0])
    orth = float(np.abs(tetT @ metric_at(x) @ tetT.T - eta).max())
    mdrift = max(abs(us[i] @ metric_at(xs[i]) @ us[i] + 1) for i in range(n)) if n else 0.0
    return {"eigs_norm": ev.tolist(), "u_drift": float(drift), "orthonorm": orth,
            "member_u_drift_exit": float(mdrift),
            "r_over_rp": rr_snap, "tau0": diag0, "vrel0_fd": vrel0_fd,
            "snaps": {str(fr): rows for fr, rows in checks.items()},
            "exit": checks.get(1.0, [])}


if __name__ == "__main__":
    mode = sys.argv[1]
    out = {}
    if mode == "control":
        res = []
        for rp, beta in [(18, 0.25), (18, 0.5), (18, 0.9), (18, 0.95), (100, 0.5), (100, 0.9), (6, 0.9)]:
            g = 1 / np.sqrt(1 - beta**2)
            closed = sorted([-g**2 * (2 + beta**2), 1.0, g**2 * (1 + 2 * beta**2)])
            r = run("flyby", rp, beta, offs=[], xis=[], nsteps=4000)
            dev = max(abs(np.array(r["eigs_norm"]) - np.array(closed)))
            res.append({"rp": rp, "beta": beta, "measured": r["eigs_norm"],
                        "closed": closed, "eig_dev": float(dev),
                        "u_drift": r["u_drift"], "orthonorm": r["orthonorm"]})
        out["eigen_control"] = res
        signres = []
        for rp in (18, 100):
            for beta in (0.5, 0.9, 0.95):
                r = run("flyby", rp, beta, offs=[0.0, np.pi / 8, np.pi / 4, 3 * np.pi / 8, np.pi / 2, "z"],
                        xis=[1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2], nsteps=4000, first_step_only=True)
                d = r["tau0"]
                xis_ = sorted({t["xi"] for t in d})
                signres.append({
                    "rp": rp, "beta": beta,
                    "udrift0_max_by_xi": {str(x): float(max(t["udrift0"] for t in d if t["xi"] == x))
                                          for x in xis_},
                    "vrel0_fd_max_by_xi": {str(x): float(max(v for v, m in zip(r["vrel0_fd"], d) if m["xi"] == x))
                                           for x in xis_},
                    "roundtrip0_max_by_xi": {str(x): float(max(t["roundtrip0"] for t in d if t["xi"] == x))
                                             for x in xis_}})
        out["sign_control"] = signres
        # vectorized vs loop RHS agreement (guards acc_vec)
        rng = np.random.default_rng(7)
        xs = np.stack([np.zeros(8), rng.uniform(8, 60, 8), np.full(8, np.pi / 2) + rng.normal(0, 0.2, 8),
                       rng.uniform(-2, 2, 8)], 1)
        us = rng.normal(0, 0.1, (8, 4)); us[:, 0] = 1.0
        av = acc_vec(xs, us)
        al = np.array([-np.einsum("mab,a,b->m", gamma_at(xs[i]), us[i], us[i]) for i in range(8)])
        out["rhs_check"] = float(np.abs(av - al).max())
    elif mode == "mapcheck":
        # old vs dual map, judged against the TRUE exponential map
        res = []
        for rp, beta in [(18, 0.9), (18, 0.5), (100, 0.9)]:
            x0, u0, tet = init_reference(rp, beta, "flyby")
            for alpha, xi0 in [(0.0, 1e-2), (0.0, 3e-2), (np.pi / 2, 3e-2), ("z", 3e-2), (np.pi / 4, 1e-2)]:
                xi_vec = np.zeros(4)
                if alpha == "z":
                    xi_vec[3] = xi0 * rp
                else:
                    xi_vec[1] = np.cos(alpha) * xi0 * rp
                    xi_vec[2] = np.sin(alpha) * xi0 * rp
                xe = exp_map_exact(x0, tet, xi_vec)
                r_old = float(np.linalg.norm(fermi_coords(xe, x0, tet, mapdual=False)[1:4] - xi_vec[1:4]) / (xi0 * rp))
                r_new = float(np.linalg.norm(fermi_coords(xe, x0, tet, mapdual=True)[1:4] - xi_vec[1:4]) / (xi0 * rp))
                res.append({"rp": rp, "beta": beta, "alpha": fl(alpha), "xi": xi0,
                            "resid_old": r_old, "resid_dual": r_new})
        out["map_check"] = res
    elif mode == "flyby":
        grid = []
        for rp in (18, 100):
            for beta in (0.5, 0.9, 0.95):
                r = run("flyby", rp, beta,
                        offs=[0.0, np.pi / 8, np.pi / 4, 3 * np.pi / 8, np.pi / 2, "z"],
                        xis=[1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2], nsteps=4000)
                grid.append({"rp": rp, "beta": beta, **r})
        out["flyby"] = grid
    elif mode == "flyby2":
        grid = []
        for rp in (18, 100):
            for beta in (0.5, 0.9, 0.95):
                r = run("flyby", rp, beta,
                        offs=[0.0, np.pi / 8, np.pi / 4, 3 * np.pi / 8, np.pi / 2, "z"],
                        xis=[1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2], nsteps=4000, ic="exact")
                grid.append({"rp": rp, "beta": beta, **r})
        out["flyby2"] = grid
    elif mode == "conv":
        res = []
        # reproduction of 451f's instrument (old sign, unnormalized, old map, frozen E)
        for nst in (4000,):
            r = run("flyby", 18, 0.9, offs=["z"], xis=[1e-4, 3e-2], nsteps=nst,
                    esample="frozen", icsign=1, normalize=False, mapdual=False, snap_fr=(1.0,))
            res.append({"cfg": "repro451f", "nsteps": nst, "exit": r["exit"]})
        for nst in (2000, 4000, 8000, 16000):
            r = run("flyby", 18, 0.9, offs=[0.0, "z"], xis=[1e-4, 3e-2], nsteps=nst,
                    esample="stage", snap_fr=(1.0,))
            res.append({"cfg": "fixed", "nsteps": nst, "exit": r["exit"],
                        "u_drift": r["u_drift"], "orthonorm": r["orthonorm"],
                        "member_u_drift_exit": r["member_u_drift_exit"]})
        out["conv"] = res
    print(json.dumps(out, indent=1, default=float))
