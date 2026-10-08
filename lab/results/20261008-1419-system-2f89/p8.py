#!/usr/bin/env python3
"""P8 (Opus motion memo, the one probe assigned to GLM): the SEM step on the v2 clock.

The system question: the fictitious clock s and the energy register p_t carry ONE constraint
twice, K = H_D - U_P + p_t = 0 (memo 2.2). The v2 split leaves K's residual O(ds^2) per step
(the shadow offset); B12's statistic reads exactly that residual (C = 2J - 2K, J exact).
The symplectic-energy-momentum step (Kane, Marsden, Ortiz 1999) solves each step's physical
time so K = 0 exactly at the step's end. If it holds, the law passes B12 by construction and
the "keep the offset small" strategy is deleted; if it fails at closest approaches (the memo's
named failure: dU_P/dt = 0), the configuration dies, not the method.

Float replica of memo 2.2 (circular restricted three-body, star doll, ship = test body):

  H_D  = |v|^2/2 - 1/r                      (Kepler drift, exact: universal variables)
  U_P  = mu/|x - x_p(t)| - mu*(x . x_p)/sep^3   (planet's pull + the origin's fall)
  f'(y) = 1/y^2 + 1/(b*y),  c = mu/R_H (floor 10*mu/sep),  b = 30*c
  step  = D(ds/2) Kc(ds) D(ds/2):  drift tau = (ds/2)*f'(H_D + p_t + c);  kick w = ds*f'(U_P + c);
         dv = w*grad U_P,  dp_t = -Omega_planet * (x x dv)_z   [keeps J = p_t + Omega*L exact per kick]

SEM variant: solve alpha (a multiplier on this step's tau1, w, tau2) by Newton so
K(end(alpha)) = 0. Failures (no convergence / out of bracket) count and fall back to alpha = 1.

Subcommands: smoke, b12 <k> <plain|sem> <periods>, b13 <k> <plain|sem> <n>.
"""
import json
import sys
import numpy as np

# ---------------------------------------------------------------- scene
MU = 3.003e-6          # planet mass / star mass (Jupiter/Sun)
SEP = 5.2              # star-planet separation (code units, star GM = 1)
OMEGA = np.sqrt((1.0 + MU) / SEP**3)   # planet's mean motion (circular)
R_H = SEP * (MU / 3.0) ** (1.0 / 3.0)  # Hill radius
C_CLOCK = max(MU / R_H, 10.0 * MU / SEP)
B_CLOCK = 30.0 * C_CLOCK
R_PLANET_TRUE = 9.2e-5 * SEP           # Jupiter's radius in these units
R_PLANET_SHRUNK = R_PLANET_TRUE * 1e-3 # memo 1.8: shrink, so losses are chaos not law
P_PLANET = 2.0 * np.pi / OMEGA


def planet(t):
    ang = np.asarray(OMEGA * t, dtype=float)
    xp = SEP * np.stack([np.cos(ang), np.sin(ang)], axis=-1)
    vp = OMEGA * SEP * np.stack([-np.sin(ang), np.cos(ang)], axis=-1)
    return xp, vp


def up_field(x, t):
    """U_P, grad U_P, dU_P/dt at state x, time t (per unit mass, star frame). Batched."""
    xp, vp = planet(t)
    xp = xp.reshape(-1, 2)
    vp = vp.reshape(-1, 2)
    d = x - xp
    r12 = np.linalg.norm(d, axis=-1, keepdims=True)
    sep3 = SEP**3
    u = MU / r12 - MU * np.sum(x * xp, axis=-1, keepdims=True) / sep3
    gu = -MU * d / r12**3 - MU * xp / sep3
    du_dt = MU * np.sum(d * vp, axis=-1, keepdims=True) / r12**3 \
        - MU * np.sum(x * vp, axis=-1, keepdims=True) / sep3
    return u, gu, du_dt



def fprime(y):
    return 1.0 / y**2 + 1.0 / (B_CLOCK * y)


# ---------------------------------------------------------------- exact Kepler drift
def _c2c3(z):
    z = np.asarray(z, dtype=float)
    c2 = np.where(np.abs(z) < 1e-8, 0.5 - z / 24.0 + z * z / 720.0, np.zeros_like(z))
    c3 = np.where(np.abs(z) < 1e-8, 1.0 / 6.0 - z / 120.0 + z * z / 5040.0, np.zeros_like(z))
    big = np.abs(z) >= 1e-8
    zb = z[big]
    pos = zb > 0
    s = np.sqrt(np.where(pos, zb, -zb))
    c2[big] = np.where(pos, (1.0 - np.cos(s)) / zb, (np.cosh(s) - 1.0) / (-zb))
    c3[big] = np.where(pos, (s - np.sin(s)) / (zb * s), (np.sinh(s) - s) / (-zb * s))
    return c2, c3


def kepler_drift(x, v, tau):
    """Exact Kepler drift (star GM = 1) by universal variables. Batched over leading axis."""
    r0 = np.linalg.norm(x, axis=-1, keepdims=True)
    v2 = np.sum(v * v, axis=-1, keepdims=True)
    r0s = np.sum(x * v, axis=-1, keepdims=True)
    alpha = 2.0 / r0 - v2
    chi = np.where(np.abs(alpha) < 1e-9, tau / np.sqrt(r0), np.sqrt(np.abs(alpha)) * tau)
    for _ in range(60):
        z = alpha * chi**2
        c2, c3 = _c2c3(z)
        F = (r0s * chi**2 * c2 + (1.0 - alpha * r0) * chi**3 * c3 + r0 * chi) - tau
        r = r0 + r0s * chi**2 * c2 + (1.0 - alpha * r0) * chi**3 * c3  # = dF/dchi
        r = np.maximum(r, 1e-12)
        chi = chi - F / r
        if np.all(np.abs(F) < 1e-13 * np.maximum(np.abs(tau), 1.0)):
            break
    z = alpha * chi**2
    c2, c3 = _c2c3(z)
    f = 1.0 - chi**2 / r0 * c2
    g = tau - chi**3 * c3
    xn = f * x + g * v
    r = np.linalg.norm(xn, axis=-1, keepdims=True)
    gdot = 1.0 - chi**2 / r * c2
    fdot = (1.0 / (r * r0)) * (alpha * chi**3 * c3 - chi)
    vn = fdot * x + gdot * v
    return xn, vn


# ---------------------------------------------------------------- one step
def kick(x, t, w):
    """The kick of weight w at (x, t): returns dv, dp_t (J-exact form)."""
    u, gu, du = up_field(x, t)
    dv = w * gu
    dp_t = (-OMEGA * np.cross(x, dv))[..., None]  # keeps dJ = dp_t + Omega*dL = 0 exactly
    return dv, dp_t


def k_residual(x, v, p_t, t):
    u, _, _ = up_field(x, t)
    hd = 0.5 * np.sum(v * v, axis=-1, keepdims=True) - 1.0 / np.linalg.norm(x, axis=-1, keepdims=True)
    return hd - u + p_t


def step_plain(x, v, p_t, t, ds, alpha_mul=1.0):
    """One v2 step D(ds/2) Kc(ds) D(ds/2). alpha_mul scales the whole step (SEM's unknown)."""
    hd = 0.5 * np.sum(v * v, axis=-1, keepdims=True) - 1.0 / np.linalg.norm(x, axis=-1, keepdims=True)
    tau1 = alpha_mul * (0.5 * ds) * fprime(hd + p_t + C_CLOCK)
    x1, v1 = kepler_drift(x, v, tau1)
    t1 = t + tau1
    w = alpha_mul * ds * fprime(up_field(x1, t1)[0] + C_CLOCK)
    dv, dp_t = kick(x1, t1, w)
    v1 = v1 + dv
    p1 = p_t + dp_t
    hd1 = 0.5 * np.sum(v1 * v1, axis=-1, keepdims=True) - 1.0 / np.linalg.norm(x1, axis=-1, keepdims=True)
    tau2 = alpha_mul * (0.5 * ds) * fprime(hd1 + p1 + C_CLOCK)
    x2, v2 = kepler_drift(x1, v1, tau2)
    return x2, v2, p1, t1 + tau2


def step_sem(x, v, p_t, t, ds, state):
    """One SEM step: alpha solved so K(end) = 0. Falls back to alpha = 1 on failure."""
    def kend(a):
        x2, v2, p1, t2 = step_plain(x, v, p_t, t, ds, alpha_mul=a)
        return k_residual(x2, v2, p1, t2), (x2, v2, p1, t2)

    k1, pack = kend(1.0)
    kscale = max(abs(float(np.max(k1))), 1e-30)
    h = 1e-4
    kh, _ = kend(1.0 + h)
    d = (kh - k1) / h
    a = 1.0
    ok = np.all(np.abs(k1) < 1e-12 * kscale + 1e-14)
    for _ in range(12):
        if ok or not np.all(np.abs(d) > 1e-14):
            break
        step = np.clip(-k1 / d, -0.5, 0.5)
        an = np.clip(a + step, 0.125, 8.0)
        kn, pk = kend(an)
        d = (kn - k1) / (an - a + 1e-30)
        a, k1, pack = an, kn, pk
        ok = np.all(np.abs(kn) < 1e-12 * kscale + 1e-14)
    state["fail"] += 0 if ok else 1
    state["steps"] += 1
    state["alpha_dev"] += float(np.sum(np.abs(a - 1.0)))
    return pack


# ---------------------------------------------------------------- scenes
def b12_ships(n, seed):
    rng = np.random.default_rng(seed)
    a = SEP * rng.uniform(0.65, 1.35, n)
    e = rng.uniform(0.0, 0.3, n)
    ang = rng.uniform(0, 2 * np.pi, n)
    nu = rng.uniform(0, 2 * np.pi, n)
    r = a * (1 - e**2) / (1 + e * np.cos(nu))
    x = np.stack([r * np.cos(nu + ang), r * np.sin(nu + ang)], axis=1)
    h_circ = np.sqrt(np.maximum(a * (1 - e**2), 1e-9))
    vv = h_circ / r
    v = np.stack([-vv * np.sin(nu + ang), vv * np.cos(nu + ang)], axis=1)
    return x, v


def init_p_t(x, v, t=0.0):
    hd = 0.5 * np.sum(v * v, axis=1, keepdims=True) - 1.0 / np.linalg.norm(x, axis=1, keepdims=True)
    return -hd + up_field(x, t)[0]


def run_b12(n_ships=16, periods=200.0, k=8, sem=False, seed=4, r_planet=R_PLANET_SHRUNK):
    x, v = b12_ships(n_ships, seed)
    p_t = init_p_t(x, v)
    t = 0.0
    ds = (P_PLANET / 2**k) / fprime(C_CLOCK)
    state = {"fail": 0, "steps": 0, "alpha_dev": 0.0}
    hd0 = 0.5 * np.sum(v * v, axis=1, keepdims=True) - 1.0 / np.linalg.norm(x, axis=1, keepdims=True)
    C0 = 2.0 * (-hd0 + up_field(x, 0.0)[0] + OMEGA * np.cross(x, v)[:, None])
    t_end = periods * P_PLANET
    n_save = 200
    total_steps = int(t_end / (ds * fprime(C_CLOCK))) + 8  # far-field rate; near-field is slower
    save_every = max(1, total_steps // n_save)
    hist_t, hist_cmax = [], []
    cmax = np.zeros((n_ships, 1))
    alive = np.ones((n_ships, 1), dtype=bool)
    i = 0
    while np.min(t) < t_end:
        if sem:
            x, v, p_t, t = step_sem(x, v, p_t, t, ds, state)
        else:
            x, v, p_t, t = step_plain(x, v, p_t, t, ds)
        xp, _ = planet(t)
        d = np.linalg.norm(x - xp.reshape(-1, 2), axis=1, keepdims=True)
        alive &= d > r_planet
        # B12 reads the OBSERVABLE Jacobi constant from (x, v, t); it differs from the
        # register's C = 2(p_t + Omega L) by exactly -2K (the constraint residual).
        hd = 0.5 * np.sum(v * v, axis=1, keepdims=True) - 1.0 / np.linalg.norm(x, axis=1, keepdims=True)
        C = 2.0 * (-hd + up_field(x, t)[0] + OMEGA * np.cross(x, v)[:, None])
        cmax = np.where(alive, np.maximum(cmax, np.abs(C - C0)), cmax)
        if i % save_every == 0:
            hist_t.append(np.array(t).ravel().copy())
            hist_cmax.append(cmax.ravel().copy())
        i += 1
    hist_t = np.stack(hist_t, axis=0)      # (nsave, nships) per-ship event times
    hist_cmax = np.stack(hist_cmax, axis=0)
    exps = []
    for j in range(n_ships):
        if not alive[j, 0]:
            continue
        tj = hist_t[:, j]
        cm = np.maximum(hist_cmax[:, j], 1e-300)
        m = tj > 0.05 * t_end
        exps.append(np.polyfit(np.log10(tj[m]), np.log10(cm[m]), 1)[0])
    return {
        "exponent_median": float(np.median(exps)) if exps else None,
        "exponents": [round(float(e), 3) for e in exps],
        "lost": int(n_ships - int(np.sum(alive))),
        "worst_err": float(np.max(cmax)),
        "fail_rate": state["fail"] / max(state["steps"], 1),
        "alpha_dev_mean": state["alpha_dev"] / max(state["steps"], 1),
        "steps": state["steps"],
    }


def run_b13(n=64, k=8, sem=False, seed=7):
    """Flybys: |dE_helio|, |dL| error vs a converged reference (DOP853 on the same CR3BP)."""
    from scipy.integrate import solve_ivp
    rng = np.random.default_rng(seed)
    kms = 29.78  # km/s of a 1 AU circular orbit, in code units
    q_r = rng.uniform(1.2, 50.0, n) * R_PLANET_TRUE
    vinf = rng.uniform(5.0, 20.0, n) / kms
    de_err, dl_err = [], []
    stats = {"fail": 0, "steps": 0, "alpha_dev": 0.0}
    for i in range(n):
        r_start = 0.5 * R_H
        e_h = 1.0 + vinf[i] ** 2 * q_r[i] / MU
        cosnu = ((q_r[i] * (1 + e_h)) / r_start - 1.0) / e_h
        nu0 = -np.arccos(np.clip(cosnu, -1, 1))
        v_peri = np.sqrt(vinf[i] ** 2 + 2.0 * MU / q_r[i])
        b_ang, phi = rng.uniform(0, 2 * np.pi), rng.uniform(0, 2 * np.pi)
        ed = np.array([np.cos(b_ang), np.sin(b_ang)])
        td = np.array([-ed[1], ed[0]])
        r_dir = np.cos(nu0) * ed + np.sin(nu0) * td
        t_dir = -np.sin(nu0) * ed + np.cos(nu0) * td
        h_p = q_r[i] * v_peri
        v_rad = -np.sqrt(max(vinf[i] ** 2 + 2.0 * MU / r_start - h_p**2 / r_start**2, 0.0))
        v_rel = v_rad * r_dir + (h_p / r_start) * t_dir
        ang = phi
        xp0 = SEP * np.array([np.cos(ang), np.sin(ang)])
        vp0 = OMEGA * SEP * np.array([-np.sin(ang), np.cos(ang)])
        x0 = xp0 + r_start * r_dir
        v0 = vp0 + v_rel
        p_t0 = float(init_p_t(x0[None, :], v0[None, :])[0, 0])
        x, v, p_t, t = x0[None, :], v0[None, :], np.array([[p_t0]]), 0.0
        ds = (P_PLANET / 2**k) / fprime(C_CLOCK)
        E0 = 0.5 * v0 @ v0 - 1.0 / np.linalg.norm(x0)
        L0 = np.cross(x0, v0)
        t_end = 2.0 * P_PLANET
        while t < t_end:
            if sem:
                x, v, p_t, t = step_sem(x, v, p_t, t, ds, stats)
            else:
                x, v, p_t, t = step_plain(x, v, p_t, t, ds)
        E1 = 0.5 * v[0] @ v[0] - 1.0 / np.linalg.norm(x[0])
        L1 = np.cross(x[0], v[0])

        def rhs(tt, y):
            xp, _ = planet(tt)
            d = y[:2] - xp
            acc = -y[:2] / np.linalg.norm(y[:2]) ** 3 + MU * (-d / np.linalg.norm(d) ** 3 - xp / SEP**3)
            return np.concatenate([y[2:], acc])

        sol = solve_ivp(rhs, [0.0, t_end], np.concatenate([x0, v0]), method="DOP853",
                        rtol=1e-12, atol=1e-14)
        yr = sol.y[:, -1]
        Er = 0.5 * yr[2:] @ yr[2:] - 1.0 / np.linalg.norm(yr[:2])
        Lr = np.cross(yr[:2], yr[2:])
        if abs(Er - E0) > 1e-14:
            de_err.append(abs((E1 - E0) - (Er - E0)) / abs(Er - E0))
        if abs(Lr - L0) > 1e-14:
            dl_err.append(abs((L1 - L0) - (Lr - L0)) / abs(Lr - L0))
    return {
        "within1_E": int(np.sum(np.array(de_err) < 0.01)),
        "within1_L": int(np.sum(np.array(dl_err) < 0.01)),
        "n": n,
        "worst_E": float(np.max(de_err)),
        "fail_rate": stats["fail"] / max(stats["steps"], 1),
        "alpha_dev_mean": stats["alpha_dev"] / max(stats["steps"], 1),
        "steps": stats["steps"],
    }


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "smoke"
    if cmd == "smoke":
        # controls: J conservation of one kick, Kepler drift roundtrip sanity, 20-period run
        x, v = b12_ships(8, 3)
        p_t = init_p_t(x, v)
        J0 = p_t + OMEGA * np.cross(x, v)[:, None]
        xn, vn, pn, tn = step_plain(x, v, p_t, 0.0, (P_PLANET / 256) / fprime(C_CLOCK))
        dJ = np.max(np.abs(pn + OMEGA * np.cross(xn, vn)[:, None] - J0))
        print(json.dumps({"dJ_per_step": float(dJ)}, indent=1))
        print(json.dumps(run_b12(n_ships=8, periods=20.0, k=8), indent=1))
    elif cmd == "b12":
        k = int(sys.argv[2]) if len(sys.argv) > 2 else 8
        sem = (sys.argv[3] == "sem") if len(sys.argv) > 3 else False
        per = float(sys.argv[4]) if len(sys.argv) > 4 else 200.0
        print(json.dumps(run_b12(n_ships=16, periods=per, k=k, sem=sem), indent=1))
    elif cmd == "b13":
        k = int(sys.argv[2]) if len(sys.argv) > 2 else 8
        sem = (sys.argv[3] == "sem") if len(sys.argv) > 3 else False
        n = int(sys.argv[4]) if len(sys.argv) > 4 else 64
        print(json.dumps(run_b13(n=n, k=k, sem=sem), indent=1))
