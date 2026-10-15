#!/usr/bin/env python3
"""Gravity-is-news at strong field: the (x,v,a) payload vs the exact Kinnersley field.

Oracle: Kinnersley's photon-rocket metric, exact GR, in Carlip's retarded Kerr-Schild
form (gr-qc/9909087 eq. b1):  g_mn = eta_mn - 2 m(s_R) sigma_m sigma_n / r^3,
sigma = x - z(s_R) null, r = lambda.sigma.  G=c=1, m constant, arbitrary source
acceleration (the null dust absorbs the thrust).  Gamma computed TWO ways:
(1) central finite differences of g(x)  (independent implementation),
(2) Carlip's published analytic connection (eq. b1a)  (literature implementation).
Their agreement is the instrument control.

Arms (what a causal consumer can do with the broadcast; all data retarded only):
  R1 naive retarded  (Laplace): pull toward z(t_R).
  R0 as-if-now tube: pull toward z + v R + 1/2 a_grav R^2  (gravitational slot only,
     thrust-blind, the shipped 16 B tube's convention).
  R2 (x,v,a) payload: pull toward z + v R + 1/2 a_tot R^2  (quadratic extrapolation).
  R2b full Carlip b3: R2's eta-direction with the velocity prefactor 1/(g^2 (1-n.v)^2)
     and the nonlinear -2m/R term; eps_1, eps_2 (O(v^2), not published) are the
     measured residual.
Exact arm: -Gamma^i_00 (a momentarily static probe; the consumer's own kinematics is
the doll's own law, not the news channel).
Scar rho = |a_arm - a_exact| / |a_exact|; rho_perp = transverse part / |a_exact|.
"""
import numpy as np

ETA = np.diag([1.0, -1.0, -1.0, -1.0])


class Source:
    """Point source on an exactly-known program, coordinate time t."""

    def __init__(self, v0, a_burn=0.0, jerk=0.0, m=1.0):
        v0 = np.asarray(v0, float)
        if v0.size == 2:
            v0 = np.concatenate((v0, [0.0]))
        self.v0 = v0                          # free-fall (inertial) velocity, 3D
        self.a_burn = a_burn                  # constant coordinate acceleration along v0 (scalar)
        self.jerk = jerk                      # d(a)/dt along the same direction
        self.m = m

    def at(self, t):
        e = self.v0 / (np.linalg.norm(self.v0) + 1e-300)  # burn direction = coast direction
        a = self.a_burn + self.jerk * t
        v = self.v0 + e * (self.a_burn * t + 0.5 * self.jerk * t * t)
        x = self.v0 * t + e * (0.5 * self.a_burn * t * t + self.jerk * t ** 3 / 6.0)
        return x, v, a  # position, velocity, scalar acceleration along e (program truth)

    def a_grav(self, t):
        """The gravitational-only slot: nothing (a lone source in free fall)."""
        return 0.0


def retarded_time(src, t, x, tau0=None):
    """Solve t - tau = |x - z(tau)| for tau; f is monotone decreasing, Newton from a
    cold start (fallback bisection)."""
    R0 = np.linalg.norm(x - src.at(t)[0])
    lo, hi = t - 2.0 * R0 - 2.0, t
    if tau0 is None:
        tau = t - R0
    else:
        tau = tau0
    for _ in range(60):
        z, v, _ = src.at(tau)
        d = x - z
        R = np.linalg.norm(d)
        f = (t - tau) - R
        n = d / R
        fp = -1.0 - np.dot(v, n) * -1.0  # df/dtau = -1 + v.n
        fp = -1.0 + np.dot(v, n)
        step = f / fp
        tau_new = tau - step
        if not (lo <= tau_new <= hi):
            break
        tau = tau_new
        if abs(step) < 1e-14 * max(1.0, abs(tau)):
            break
    # bisection refinement (guards Newton under burn curvature)
    z, _, _ = src.at(tau)
    f = (t - tau) - np.linalg.norm(x - z)
    if abs(f) > 1e-12 * max(1.0, R0):
        a_, b_ = lo, hi
        for _ in range(100):
            c = 0.5 * (a_ + b_)
            z, _, _ = src.at(c)
            fc = (t - c) - np.linalg.norm(x - z)
            if fc == 0.0 or (b_ - a_) < 1e-15 * max(1.0, abs(t)):
                break
            fa_sign = ((t - a_) - np.linalg.norm(x - src.at(a_)[0])) > 0
            if (fc > 0) == fa_sign:
                a_ = c
            else:
                b_ = c
        tau = 0.5 * (a_ + b_)
    return tau


def metric_at(src, t, x):
    """g_mn(x) = eta - 2 m sigma_m sigma_n / r^3 at event (t, x); 4x4, lower indices."""
    tau = retarded_time(src, t, x)
    z, v, _ = src.at(tau)
    sig = np.concatenate(([t - tau], x - z))
    gam = 1.0 / np.sqrt(1.0 - np.dot(v, v))
    lam = gam * np.concatenate(([1.0], v))
    sig_lo = ETA @ sig
    r = np.dot(lam, sig_lo)  # lambda^mu sigma_mu (Carlip eq. a3)
    g = ETA - 2.0 * src.m * np.outer(sig_lo, sig_lo) / r ** 3
    return g, tau, sig, lam, r


def gamma_fd(src, t, x, h=None):
    """Christoffels of the exact metric by central differences of g."""
    if h is None:
        h = 1e-4 * src.m
    n = 4
    G = np.zeros((n, n, n))
    dg = np.zeros((n, n, n))  # dg[a,m,n] = d_a g_mn
    for a in range(n):
        xp = np.array(x, float); xm = np.array(x, float)
        if a == 0:
            gp, *_ = metric_at(src, t + h, x)
            gm, *_ = metric_at(src, t - h, x)
        else:
            xp[a - 1] += h; xm[a - 1] -= h
            gp, *_ = metric_at(src, t, xp)
            gm, *_ = metric_at(src, t, xm)
        dg[a] = (gp - gm) / (2 * h)
    g, tau, sig, lam, r = metric_at(src, t, x)
    ginv = np.linalg.inv(g)
    for p in range(n):
        for m_ in range(n):
            for n_ in range(n):
                G[p, m_, n_] = 0.5 * sum(ginv[p, s] * (dg[m_, s, n_] + dg[n_, s, m_] - dg[s, m_, n_])
                                        for s in range(n))
    return G


def gamma_analytic(src, t, x):
    """Carlip eq. b1a, the published connection (constant m)."""
    tau = retarded_time(src, t, x)
    z, v, a_s = src.at(tau)          # a_s = program acceleration (scalar along e)
    e = src.v0 / (np.linalg.norm(src.v0) + 1e-300)
    sig = np.concatenate(([t - tau], x - z))
    gam = 1.0 / np.sqrt(1.0 - np.dot(v, v))
    lam = gam * np.concatenate(([1.0], v))
    sig_lo = ETA @ sig
    lam_lo = ETA @ lam
    r = np.dot(lam, sig_lo)
    m = src.m
    # d(lam)/ds with ds/dt = gam:  d/ds = (1/gam) d/dt ; a_vec = a_s * e ; dgam/dt = gam^3 (v.a)
    a_vec = a_s * e
    vdotv = np.dot(v, v)
    gdot = gam ** 3 * np.dot(v, a_vec)
    dlam_dt = np.empty(4)
    dlam_dt[0] = gdot
    dlam_dt[1:] = gam * a_vec + gdot * v
    dlam = dlam_dt * gam            # d(lam^mu)/ds = (dt/ds) d/dt = gam d/dt
    dlam_lo = ETA @ dlam
    sig_lo = ETA @ sig
    lam_lo = ETA @ lam
    sigma_dot_dlam = np.dot(sig_lo, dlam)
    G = np.zeros((4, 4, 4))
    for m_ in range(4):
        for n_ in range(4):
            for p in range(4):
                val = (-2 * m / r ** 3 * ETA[m_, n_] * sig[p]
                       + m / r ** 4 * (3 * lam_lo[m_] * sig_lo[n_] * sig[p]
                                       + 3 * lam_lo[n_] * sig_lo[m_] * sig[p]
                                       - sig_lo[m_] * sig_lo[n_] * lam[p])
                       - 3 * m / r ** 5 * (1 - sigma_dot_dlam) * sig_lo[m_] * sig_lo[n_] * sig[p]
                       - 2 * m ** 2 / r ** 6 * sig_lo[m_] * sig_lo[n_] * sig[p])
                G[p, m_, n_] = val
    return G


def arms(src, t, x):
    """The readout arms' implied acceleration at (t, x); retarded data only."""
    tau = retarded_time(src, t, x)
    z, v, a_s = src.at(tau)
    e = src.v0 / (np.linalg.norm(src.v0) + 1e-300)
    R = t - tau
    d = x - z
    Rsp = np.linalg.norm(d)
    n_hat = d / Rsp
    m = src.m
    out = {}
    # R1: naive retarded (Laplace)
    out["R1"] = -m * d / Rsp ** 3
    # R0: as-if-now with the gravitational slot only (free fall tube: linear)
    x0 = z + v * R + 0.5 * (src.a_grav(tau) * e) * R ** 2
    d0 = x - x0
    out["R0"] = -m * d0 / np.linalg.norm(d0) ** 3
    # R2: (x,v,a) quadratic extrapolation
    x2 = z + v * R + 0.5 * (a_s * e) * R ** 2
    d2 = x - x2
    out["R2"] = -m * d2 / np.linalg.norm(d2) ** 3
    # R2b: Carlip b3 — eta direction + velocity prefactor + nonlinear -2m/R term
    gam = 1.0 / np.sqrt(1.0 - np.dot(v, v))
    ndotv = np.dot(n_hat, v)
    pref = m / Rsp ** 2 / (gam ** 2 * (1 - ndotv) ** 2)
    eta_dir = d2 / np.linalg.norm(d2)
    out["R2b"] = -pref * (eta_dir - (2 * m / Rsp) / (gam ** 4 * (1 - ndotv) ** 4) * n_hat)
    return out


def orbit_events(src, r0, n_samples=120, steps_per_orbit=240, n_orbits=1.2, seed=0):
    """Integrate a consumer geodesic (t-parameter, RK4) around the source; sample events.
    Start quasi-circular about the source's current position, co-moving."""
    m = src.m
    P = 2 * np.pi * np.sqrt(r0 ** 3 / m)
    x = np.array([r0, 0.0, 0.0])
    z0, v0s, _ = src.at(0.0)
    vc = np.sqrt(m / r0)
    v = np.array([0.0, vc, 0.0]) + v0s
    dt = P / steps_per_orbit
    n_steps = int(steps_per_orbit * n_orbits)
    events = []
    every = max(1, n_steps // n_samples)
    def acc(t_, x_, v_):
        V = np.concatenate(([1.0], v_))
        G = gamma_fd(src, t_, x_)
        A = np.zeros(3)
        Ai0 = sum(G[0, mu, nu] * V[mu] * V[nu] for mu in range(4) for nu in range(4))
        for i in range(1, 4):
            val = 0.0
            for mu in range(4):
                for nu in range(4):
                    val += G[i, mu, nu] * V[mu] * V[nu]
            A[i - 1] = -val + Ai0 * v_[i - 1]
        return A
    for k in range(n_steps + 1):
        if k % every == 0:
            events.append((k * dt, x.copy(), v.copy()))
        if k == n_steps:
            break
        # RK4
        k1x, k1v = v, acc(k * dt, x, v)
        k2x, k2v = v + 0.5 * dt * k1v, acc((k + 0.5) * dt, x + 0.5 * dt * k1x, v + 0.5 * dt * k1v)
        k3x, k3v = v + 0.5 * dt * k2v, acc((k + 0.5) * dt, x + 0.5 * dt * k2x, v + 0.5 * dt * k2v)
        k4x, k4v = v + dt * k3v, acc((k + 1) * dt, x + dt * k3x, v + dt * k3v)
        x = x + dt / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
        v = v + dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
    return events


def scene(v0, a_burn=0.0, jerk=0.0, r0=20.0, label="", n_samples=100):
    src = Source(np.array([v0, 0.0]), a_burn=a_burn, jerk=jerk)
    events = orbit_events(src, r0, n_samples=n_samples)
    rows = []
    for (t, x, v) in events:
        G = gamma_fd(src, t, x)
        Ga = gamma_analytic(src, t, x)
        rel = np.max(np.abs(G - Ga)) / max(np.max(np.abs(Ga)), 1e-300)
        a_ex = -G[1:4, 0, 0]
        A = arms(src, t, x)
        row = {"t": t, "xcheck": rel}
        row["r"] = np.linalg.norm(x - src.at(t)[0])
        row["beta_c"] = np.linalg.norm(v - src.at(t)[1])
        row["exact"] = np.linalg.norm(a_ex)
        for k, av in A.items():
            err = av - a_ex
            ax = a_ex / np.linalg.norm(a_ex)
            perp = np.linalg.norm(err - np.dot(err, ax) * ax)
            row[k] = np.linalg.norm(err) / np.linalg.norm(a_ex)
            row[k + "_perp"] = perp / np.linalg.norm(a_ex)
        rows.append(row)
    return rows


def summarize(rows):
    keys = ["R1", "R0", "R2", "R2b"]
    out = {"xcheck_max": max(r["xcheck"] for r in rows),
           "r_med": float(np.median([r["r"] for r in rows])),
           "beta_c_med": float(np.median([r["beta_c"] for r in rows]))}
    for k in keys:
        out[k + "_med"] = float(np.median([r[k] for r in rows]))
        out[k + "_max"] = max(r[k] for r in rows)
        out[k + "_perp_med"] = float(np.median([r[k + "_perp"] for r in rows]))
    return out


if __name__ == "__main__":
    import json, sys
    # instrument self-test: static source, v=0 a=0 -> Schwarzschild KS, pull = m/R^2 (1+2m/R)
    src = Source(np.array([0.0, 0.0]))
    t, x = 0.0, np.array([20.0, 0.0, 0.0])
    G = gamma_fd(src, t, x)
    Ga = gamma_analytic(src, t, x)
    rel = np.max(np.abs(G - Ga)) / np.max(np.abs(Ga))
    a_ex = -G[1:3, 0, 0]
    known = src.m / 20.0 ** 2 * (1 - 2 * src.m / 20.0)  # hand-derived static KS Gamma^i_00
    print(json.dumps({"fd_vs_analytic_rel": rel,
                      "static_pull": float(np.linalg.norm(a_ex)),
                      "ks_known_static": known,
                      "static_rel_err": float(abs(np.linalg.norm(a_ex) - known) / known)}, indent=1))
