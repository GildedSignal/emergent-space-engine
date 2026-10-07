#!/usr/bin/env python3
"""Scout falsifier: per-body self-triggered kick cadence vs one global fixed cadence.

Scene: planar restricted 3-body, primary-centric frame. Primary mu=1 at origin,
perturber (mass ratio mu_r) on a fixed circular orbit of radius D.
Perturbing acceleration on the test body (tidal form, primary stays at origin):

    a_pert = mu_r * [ (r_p - x)/|r_p - x|^3 - r_p/|r_p|^3 ]

Truth: RK4, fixed dt (convergence checked). Model: exact Kepler drift between
kick times + the exact impulse integral of a_pert along the drifted arc
(12-pt Gauss-Legendre in eccentric anomaly), split half at each interval end
(KDK, second order, the plane's split). Kick evaluation is idealised: the ONLY
variable is WHEN kicks happen, so cadence is isolated.

Schedulers:
  fixed-N : N kicks per orbit, uniform in the drift's phase (mean anomaly).
  ruleA   : self-triggered. At each kick, tabulate |a_pert| along the upcoming
            osculating orbit (closed form, no trajectory integration), take the
            largest dt with sup_{[t,t+dt]} |a| * dt^2/2 <= eps_v, capped at one
            radial period. Within-orbit adaptive.
  ruleB   : same, sup over the whole orbit -> uniform per-orbit cadence,
            re-decided at each kick. Per-body adaptivity only.

Budget (behaviour, fixed before held-out runs; B14's flavour):
  |slope(varpi)_model - slope(varpi)_truth| / |slope_truth| <= 0.10
  |q(T)_model - q(T)_truth| / q(T)_truth <= 0.02
  |e(T)_model - e(T)_truth| <= 0.01
  (e0 = 0: varpi slope undefined; budget uses dq, de only)
"""
import json
import sys
import numpy as np

GL_X, GL_W = np.polynomial.legendre.leggauss(8)
TWO_PI = 2.0 * np.pi


def a_pert(x, y, t, mu_r, D):
    n_p = np.sqrt((1.0 + mu_r) / D**3)
    xp = D * np.cos(n_p * t)
    yp = D * np.sin(n_p * t)
    dx = xp - x
    dy = yp - y
    r3 = (dx * dx + dy * dy) ** 1.5
    return (mu_r * (dx / r3 - xp / D**3), mu_r * (dy / r3 - yp / D**3))


def deriv(state, t, mu_r, D):
    x, y, vx, vy = state[..., 0], state[..., 1], state[..., 2], state[..., 3]
    r = np.hypot(x, y)
    r3 = r**3
    ax, ay = a_pert(x, y, t, mu_r, D)
    return np.stack([vx, vy, -x / r3 + ax, -y / r3 + ay], axis=-1)


def elements(states):
    x, y, vx, vy = states[..., 0], states[..., 1], states[..., 2], states[..., 3]
    r = np.hypot(x, y)
    v2 = vx * vx + vy * vy
    a = 1.0 / (2.0 / r - v2)
    rv = x * vx + y * vy
    ex = (v2 - 1.0 / r) * x - rv * vx
    ey = (v2 - 1.0 / r) * y - rv * vy
    e = np.hypot(ex, ey)
    varpi = np.arctan2(ey, ex)
    return np.stack([a, e, varpi], axis=-1)


def rk4(state0, mu_r, D, T, dt, sample_every):
    n = int(round(T / dt))
    s = state0.astype(float).copy()
    nsamp = n // sample_every + 1
    out = np.empty((s.shape[0], nsamp, 3))
    j = 0
    out[:, j] = elements(s)
    for i in range(n):
        t = i * dt
        k1 = deriv(s, t, mu_r, D)
        k2 = deriv(s + 0.5 * dt * k1, t + 0.5 * dt, mu_r, D)
        k3 = deriv(s + 0.5 * dt * k2, t + 0.5 * dt, mu_r, D)
        k4 = deriv(s + dt * k3, t + dt, mu_r, D)
        s = s + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        if (i + 1) % sample_every == 0:
            j += 1
            if j < nsamp:
                out[:, j] = elements(s)
    return out[:, : j + 1]


def ecc_anomaly(x, y, a, e, varpi):
    c, s = np.cos(-varpi), np.sin(-varpi)
    xp = x * c - y * s
    yp = x * s + y * c
    return np.arctan2(yp / (a * np.sqrt(np.maximum(1 - e * e, 1e-18))),
                      xp / a + e)


def state_from_E(a, e, varpi, E):
    xp = a * (np.cos(E) - e)
    yp = a * np.sqrt(np.maximum(1.0 - e * e, 1e-18)) * np.sin(E)
    n = a ** -1.5
    den = np.maximum(1.0 - e * np.cos(E), 1e-12)
    vxp = -a * n * np.sin(E) / den
    vyp = a * n * np.sqrt(np.maximum(1.0 - e * e, 1e-18)) * np.cos(E) / den
    c, s = np.cos(varpi), np.sin(varpi)
    return (xp * c - yp * s, xp * s + yp * c, vxp * c - vyp * s, vxp * s + vyp * c)


def kepler_E(M, e):
    M = np.asarray(M, dtype=float)
    E = M.copy()
    for _ in range(80):
        d = (E - e * np.sin(E) - M) / np.maximum(np.abs(1.0 - e * np.cos(E)), 1e-15)
        E = E - d
        if np.max(np.abs(d)) < 1e-14:
            break
    return E


def impulse(t0, dt, mu_r, D, a, e, varpi, E0):
    n = a ** -1.5
    M0 = E0 - e * np.sin(E0)
    E1 = kepler_E(M0 + n * dt, e)
    u = 0.5 * (GL_X + 1.0) * (E1 - E0) + E0
    w = GL_W * 0.5 * (E1 - E0)
    x, y, _, _ = state_from_E(a, e, varpi, u)
    t = t0 + (u - e * np.sin(u) - M0) / n
    ax, ay = a_pert(x, y, t, mu_r, D)
    fac = w * (1.0 - e * np.cos(u)) / n
    return float(np.sum(ax * fac)), float(np.sum(ay * fac))


def aprof_orbit(a, e, varpi, t0, mu_r, D, npts=64):
    n = a ** -1.5
    u = np.linspace(0.0, TWO_PI, npts, endpoint=False)
    x, y, _, _ = state_from_E(a, e, varpi, u)
    ax, ay = a_pert(x, y, t0 + (u - e * np.sin(u)) / n, mu_r, D)
    return (u - e * np.sin(u)) / n, np.hypot(ax, ay)


def run_kicked(s0, mu_r, D, T, sched, P_orbit=TWO_PI, max_kicks=None):
    s = s0.astype(float).copy()
    t = 0.0
    kicks = 0
    log = [(0.0, s.copy())]
    while t < T - 1e-12:
        a, e, varpi = elements(s[None, :])[0]
        E0 = ecc_anomaly(s[0], s[1], a, e, varpi)
        n = a ** -1.5
        M0 = E0 - e * np.sin(E0)
        dt = float(min(sched(s, t, (a, e, varpi, E0)), T - t))
        Ix, Iy = impulse(t, dt, mu_r, D, a, e, varpi, E0)
        vx_h, vy_h = s[2] + 0.5 * Ix, s[3] + 0.5 * Iy  # half kick
        x, y, _, _ = s[0], s[1], vx_h, vy_h
        # exact drift of the half-kicked state over [t, t+dt]
        a2, e2, w2 = elements(np.array([[x, y, vx_h, vy_h]]))[0]
        n2 = a2 ** -1.5
        E02 = ecc_anomaly(x, y, a2, e2, w2)
        M02 = E02 - e2 * np.sin(E02)
        E12 = kepler_E(M02 + n2 * dt, e2)
        x2, y2, vx2, vy2 = state_from_E(a2, e2, w2, E12)
        s = np.array([x2, y2, vx2 + 0.5 * Ix, vy2 + 0.5 * Iy])  # half kick at end
        log.append((t, s.copy()))
        t += dt
        kicks += 1
        if max_kicks is not None and kicks >= max_kicks:
            break
    return s, kicks, log


def slope_rows(ts, vs):
    """Least-squares slope of each row of unwrapped vs over the second half."""
    m = ts.shape[0] // 2
    t = ts[m:] - ts[m:].mean()
    v = vs[:, m:]
    v = v - v.mean(axis=1, keepdims=True)
    return (v @ t) / (t @ t)


def slope_of(times, varpis):
    t = np.asarray(times, dtype=float)
    tv = np.unwrap(np.asarray(varpis, dtype=float))
    m = len(t) // 2
    tt = t[m:] - t[m:].mean()
    vv = tv[m:] - tv[m:].mean()
    return float(vv @ tt / (tt @ tt))


def dense_elements(log, ts):
    """Osculating elements of the kicked model at sample times ts
    (exact Kepler drift inside each segment)."""
    kts = np.array([k[0] for k in log])
    out = np.empty((len(ts), 3))
    idx = np.clip(np.searchsorted(kts, ts, side="right") - 1, 0, len(kts) - 1)
    for j, t in enumerate(ts):
        tk, s = log[idx[j]]
        a, e, varpi = elements(s[None, :])[0]
        n = a ** -1.5
        E0 = ecc_anomaly(s[0], s[1], a, e, varpi)
        M0 = E0 - e * np.sin(E0)
        E1 = kepler_E(M0 + n * (t - tk), e)
        x, y, vx, vy = state_from_E(a, e, varpi, E1)
        out[j] = elements(np.array([[x, y, vx, vy]]))[0]
    return out


def metrics(model_out, truth, e0, T, ts=None):
    ms, kicks, log = model_out
    a_t, e_t = truth["a_end"], truth["e_end"]
    q_t = a_t * (1.0 - e_t)
    a_m, e_m, _ = elements(ms[None, :])[0]
    q_m = a_m * (1.0 - e_m)
    res = {
        "kicks_per_orbit": kicks / T * TWO_PI,
        "dq_rel": abs(q_m - q_t) / abs(q_t),
        "de_abs": abs(e_m - e_t),
    }
    if e0 > 1e-3 and ts is not None and len(log) >= 8:
        de = dense_elements(log, ts)
        sl = slope_of(ts, de[:, 2])
        res["slope_relerr"] = abs(sl - truth["slope_true"]) / abs(truth["slope_true"])
    else:
        res["slope_relerr"] = None
    return res


def holds(res, e0):
    ok = res["dq_rel"] <= 0.02 and res["de_abs"] <= 0.01
    if e0 > 1e-3:
        ok = ok and res["slope_relerr"] is not None and res["slope_relerr"] <= 0.10
    return bool(ok)


def make_ruleA(eps_v, mu_r, D):
    def sched(s, t, el):
        a, e, varpi, E0 = el
        lag, prof = aprof_orbit(a, e, varpi, t, mu_r, D)
        ok = np.maximum.accumulate(prof) * lag**2 / 2.0 <= eps_v
        idx = np.nonzero(ok)[0]
        return min(lag[idx[-1]] if len(idx) else lag[1] * 0.5, TWO_PI * a ** 1.5)
    return sched


def make_ruleB(eps_v, mu_r, D):
    def sched(s, t, el):
        a, e, varpi, E0 = el
        lag, prof = aprof_orbit(a, e, varpi, t, mu_r, D)
        return min(np.sqrt(2.0 * eps_v / max(prof.max(), 1e-30)), TWO_PI * a ** 1.5)
    return sched


def avar_orbit(a, e, varpi, E0, t0, mu_r, D, npts=64):
    """|a_pert(f) - a_pert(f0)| vs lag along one upcoming osculating orbit."""
    n = a ** -1.5
    u = E0 + np.linspace(0.0, TWO_PI, npts, endpoint=False)
    x, y, _, _ = state_from_E(a, e, varpi, u)
    M0 = E0 - e * np.sin(E0)
    ts = t0 + (u - e * np.sin(u) - M0) / n
    ax, ay = a_pert(x, y, ts, mu_r, D)
    return ts - t0, np.hypot(ax - ax[0], ay - ay[0])


def avar_full(a, e, varpi, E0, t0, mu_r, D, npts=64):
    """Variation profile vs lag, and |net impulse over one osculating orbit|."""
    n = a ** -1.5
    u = E0 + np.linspace(0.0, TWO_PI, npts, endpoint=False)
    x, y, _, _ = state_from_E(a, e, varpi, u)
    M0 = E0 - e * np.sin(E0)
    ts = t0 + (u - e * np.sin(u) - M0) / n
    ax, ay = a_pert(x, y, ts, mu_r, D)
    lag = ts - t0
    # net impulse over the orbit: integrate a dt, dt = (1 - e cosE)/n dE
    dE = u[1] - u[0]
    w = (1.0 - e * np.cos(u)) / n * dE
    Ix, Iy = float(np.sum(ax * w)), float(np.sum(ay * w))
    return lag, np.hypot(ax - ax[0], ay - ay[0]), np.hypot(Ix, Iy), float(np.sum(np.hypot(ax, ay) * w))


def make_rulePA(eps_rel, mu_r, D):
    """Path-normalised: per-interval error vs the non-cancelling per-orbit
    path impulse int|a| dt (closed form from the osculating orbit)."""
    def sched(s, t, el):
        a, e, varpi, E0 = el
        lag, prof, _o, I_path = avar_full(a, e, varpi, E0, t, mu_r, D)
        thr = eps_rel * max(I_path, 1e-30)
        ok = np.maximum.accumulate(prof) * lag**2 / 2.0 <= thr
        idx = np.nonzero(ok)[0]
        return min(lag[idx[-1]] if len(idx) else lag[1] * 0.5, TWO_PI * a ** 1.5)
    return sched


def make_rulePB(eps_rel, mu_r, D):
    def sched(s, t, el):
        a, e, varpi, E0 = el
        lag, prof, _o, I_path = avar_full(a, e, varpi, E0, t, mu_r, D)
        thr = eps_rel * max(I_path, 1e-30)
        return min(np.sqrt(2.0 * thr / max(prof.max(), 1e-30)), TWO_PI * a ** 1.5)
    return sched


def make_ruleRA(eps_rel, mu_r, D):
    """Scale-free self-triggered rule: per-interval error budget relative to
    the body's own per-orbit impulse (both from the osculating orbit)."""
    def sched(s, t, el):
        a, e, varpi, E0 = el
        n = a ** -1.5
        lag, prof, I_orb, _p = avar_full(a, e, varpi, E0, t, mu_r, D)
        thr = eps_rel * max(I_orb, 1e-30)
        ok = np.maximum.accumulate(prof) * lag**2 / 2.0 <= thr
        idx = np.nonzero(ok)[0]
        return min(lag[idx[-1]] if len(idx) else lag[1] * 0.5, TWO_PI * a ** 1.5)
    return sched


def make_ruleRB(eps_rel, mu_r, D):
    def sched(s, t, el):
        a, e, varpi, E0 = el
        lag, prof, I_orb, _p = avar_full(a, e, varpi, E0, t, mu_r, D)
        thr = eps_rel * max(I_orb, 1e-30)
        return min(np.sqrt(2.0 * thr / max(prof.max(), 1e-30)), TWO_PI * a ** 1.5)
    return sched


def make_ruleVA(eps_v, mu_r, D):
    def sched(s, t, el):
        a, e, varpi, E0 = el
        lag, prof = avar_orbit(a, e, varpi, E0, t, mu_r, D)
        ok = np.maximum.accumulate(prof) * lag**2 / 2.0 <= eps_v
        idx = np.nonzero(ok)[0]
        return min(lag[idx[-1]] if len(idx) else lag[1] * 0.5, TWO_PI * a ** 1.5)
    return sched


def make_ruleVB(eps_v, mu_r, D):
    def sched(s, t, el):
        a, e, varpi, E0 = el
        lag, prof = avar_orbit(a, e, varpi, E0, t, mu_r, D)
        return min(np.sqrt(2.0 * eps_v / max(prof.max(), 1e-30)), TWO_PI * a ** 1.5)
    return sched


def state0_from_elements(a0, e0):
    x, y, vx, vy = state_from_E(a0, e0, 0.0, 0.0)
    return np.array([x, y, vx, vy])


SCENES = {
    "cal": dict(e0=0.3, mu_r=0.05, D=12.0, T_orb=48.0),
    "h1": dict(e0=0.0, mu_r=0.05, D=12.0, T_orb=48.0),
    "h2": dict(e0=0.7, mu_r=0.05, D=30.0, T_orb=48.0),
    "h3": dict(e0=0.5, mu_r=0.01, D=12.0, T_orb=48.0),
}


def make_truth(s0, mu_r, D, T, dt_per_orbit=2048.0):
    dt = TWO_PI / dt_per_orbit
    samp = rk4(s0[None, :], mu_r, D, T, dt, int(dt_per_orbit / 8))
    ns = samp.shape[1]
    ts = np.linspace(0.0, T, ns)
    return {
        "ts": ts, "varpi": samp[0, :, 2],
        "a_end": float(samp[0, -1, 0]), "e_end": float(samp[0, -1, 1]),
        "slope_true": slope_of(ts, samp[0, :, 2]),
    }


def run_scene(name, eps_v=None, ladder=(1, 2, 4, 8, 16, 32, 128)):
    sc = SCENES[name]
    T = sc["T_orb"] * TWO_PI
    s0 = state0_from_elements(1.0, sc["e0"])
    truth = make_truth(s0, sc["mu_r"], sc["D"], T)
    out = {"scene": name, **{k: v for k, v in sc.items()}, "eps_v": eps_v,
           "slope_true": truth["slope_true"], "runs": {}}
    for N in ladder:
        m = run_kicked(s0, sc["mu_r"], sc["D"], T, lambda s, t, el, N=N: TWO_PI / N)
        res = metrics(m, truth, sc["e0"], T, ts=truth["ts"])
        res["holds"] = holds(res, sc["e0"])
        out["runs"][f"fixed{N}"] = res
    if eps_v is not None:
        for rn, mk in (("ruleA", make_ruleA), ("ruleB", make_ruleB)):
            m = run_kicked(s0, sc["mu_r"], sc["D"], T, mk(eps_v, sc["mu_r"], sc["D"]))
            res = metrics(m, truth, sc["e0"], T, ts=truth["ts"])
            res["holds"] = holds(res, sc["e0"])
            out["runs"][rn] = res
    return out


def calibrate(name="cal", lo=1e-8, hi=3e-3, iters=7, rules=None, max_kicks=None):
    sc = SCENES[name]
    T = sc["T_orb"] * TWO_PI
    s0 = state0_from_elements(1.0, sc["e0"])
    truth = make_truth(s0, sc["mu_r"], sc["D"], T)
    best, trace = None, []
    rules = rules or (("ruleA", make_ruleA), ("ruleB", make_ruleB))
    for _ in range(iters):
        mid = float(np.sqrt(lo * hi))
        oks = {}
        for rn, mk in rules:
            m = run_kicked(s0, sc["mu_r"], sc["D"], T, mk(mid, sc["mu_r"], sc["D"]),
                           max_kicks=max_kicks)
            res = metrics(m, truth, sc["e0"], T, ts=truth["ts"])
            oks[rn] = [holds(res, sc["e0"]), res["kicks_per_orbit"],
                       res["dq_rel"], res["de_abs"], res["slope_relerr"]]
        trace.append({"eps": mid, **oks})
        if all(v[0] for v in oks.values()):
            best, lo = mid, mid
        else:
            hi = mid
    return best, trace


def run_mixed(eps_v, nb=192, T_orb=32.0, seed=7, ladder=(1, 2, 4, 8, 16), rules=None):
    """Belt-like scene: nb bodies, mixed e, one global (mu_r, D)."""
    rng = np.random.default_rng(seed)
    half = rng.random(nb) < 0.5
    e0s = np.where(half, np.clip(rng.rayleigh(0.1, nb), 0.0, 0.6),
                   rng.uniform(0.15, 0.7, nb))
    mu_r, D = 0.05, 25.0
    T = T_orb * TWO_PI
    S0 = np.array([state0_from_elements(1.0, e) for e in e0s])
    dt = TWO_PI / 4096.0
    samp = rk4(S0, mu_r, D, T, dt, 512)
    ns = samp.shape[1]
    ts = np.linspace(0.0, T, ns)
    slope_true = slope_rows(ts, np.unwrap(samp[:, :, 2], axis=1))
    a_end, e_end = samp[:, -1, 0], samp[:, -1, 1]
    q_true = a_end * (1 - e_end)
    out = {"nb": nb, "T_orb": T_orb, "mu_r": mu_r, "D": D, "eps_v": eps_v,
           "e_hist": np.histogram(e0s, bins=8, range=(0, 0.7))[0].tolist(),
           "ladder": {}, "rules": {}}
    minN = np.full(nb, 32.0)  # bodies failing at 16 need >= 32
    for N in ladder:
        kpo = np.empty(nb)
        hold = np.empty(nb, dtype=bool)
        for i in range(nb):
            m = run_kicked(S0[i], mu_r, D, T, lambda s, t, el, N=N: TWO_PI / N)
            res = metrics(m, {"a_end": a_end[i], "e_end": e_end[i],
                              "slope_true": slope_true[i]}, e0s[i], T, ts=ts)
            kpo[i] = res["kicks_per_orbit"]
            hold[i] = holds(res, e0s[i])
        minN[hold] = np.minimum(minN[hold], N)
        out["ladder"][f"fixed{N}"] = {
            "all_hold": bool(hold.all()),
            "frac_hold": float(hold.mean()),
            "kicks_per_orbit_mean": float(kpo.mean()),
        }
    global_fixed = float(minN.max())
    fixed_total = global_fixed * T_orb * nb
    for rn, mk in (rules or (("ruleA", make_ruleA), ("ruleB", make_ruleB))):
        kpo = np.empty(nb)
        hold = np.empty(nb, dtype=bool)
        for i in range(nb):
            m = run_kicked(S0[i], mu_r, D, T, mk(eps_v, mu_r, D))
            res = metrics(m, {"a_end": a_end[i], "e_end": e_end[i],
                              "slope_true": slope_true[i]}, e0s[i], T, ts=ts)
            kpo[i] = res["kicks_per_orbit"]
            hold[i] = holds(res, e0s[i])
        out["rules"][rn] = {
            "frac_hold": float(hold.mean()),
            "kicks_per_orbit_mean": float(kpo.mean()),
            "total_kicks": float(kpo.sum() * T_orb),
            "cut_vs_global_fixed": float(fixed_total / (kpo.sum() * T_orb)),
            "global_fixed_cadence": global_fixed,
            "failing_e": e0s[~hold].tolist()[:20],
        }
    return out


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "calib":
        eps, trace = calibrate()
        print(json.dumps({"eps_v": eps, "trace": trace}, indent=1, default=float))
    elif cmd in SCENES:
        eps = float(sys.argv[2]) if len(sys.argv) > 2 else None
        print(json.dumps(run_scene(cmd, eps_v=eps), indent=1, default=float))
    elif cmd == "mixed":
        print(json.dumps(run_mixed(float(sys.argv[2])), indent=1, default=float))
    elif cmd == "calibv":
        eps, trace = calibrate(rules=(("ruleVA", make_ruleVA), ("ruleVB", make_ruleVB)))
        print(json.dumps({"eps_v": eps, "trace": trace}, indent=1, default=float))
    elif cmd == "scenev":
        nm, eps = sys.argv[2], float(sys.argv[3])
        sc = SCENES[nm]
        T = sc["T_orb"] * TWO_PI
        s0 = state0_from_elements(1.0, sc["e0"])
        truth = make_truth(s0, sc["mu_r"], sc["D"], T)
        out = {"scene": nm, "slope_true": truth["slope_true"], "runs": {}}
        for rn, mk in (("ruleVA", make_ruleVA), ("ruleVB", make_ruleVB)):
            m = run_kicked(s0, sc["mu_r"], sc["D"], T, mk(eps, sc["mu_r"], sc["D"]))
            res = metrics(m, truth, sc["e0"], T, ts=truth["ts"])
            res["holds"] = holds(res, sc["e0"])
            out["runs"][rn] = res
        print(json.dumps(out, indent=1, default=float))
    elif cmd == "calibr":
        eps, trace = calibrate(rules=(("ruleRA", make_ruleRA), ("ruleRB", make_ruleRB)),
                               lo=1e-3, hi=0.3, iters=6, max_kicks=2500)
        print(json.dumps({"eps_rel": eps, "trace": trace}, indent=1, default=float))
    elif cmd == "scener":
        nm, eps = sys.argv[2], float(sys.argv[3])
        sc = SCENES[nm]
        T = sc["T_orb"] * TWO_PI
        s0 = state0_from_elements(1.0, sc["e0"])
        truth = make_truth(s0, sc["mu_r"], sc["D"], T)
        out = {"scene": nm, "slope_true": truth["slope_true"], "runs": {}}
        for rn, mk in (("ruleRA", make_ruleRA), ("ruleRB", make_ruleRB)):
            m = run_kicked(s0, sc["mu_r"], sc["D"], T, mk(eps, sc["mu_r"], sc["D"]))
            res = metrics(m, truth, sc["e0"], T, ts=truth["ts"])
            res["holds"] = holds(res, sc["e0"])
            out["runs"][rn] = res
        print(json.dumps(out, indent=1, default=float))
    elif cmd == "mixedr":
        print(json.dumps(run_mixed(float(sys.argv[2]),
                                   rules=(("ruleRA", make_ruleRA), ("ruleRB", make_ruleRB))),
                         indent=1, default=float))
    elif cmd == "calibp":
        eps, trace = calibrate(rules=(("rulePA", make_rulePA), ("rulePB", make_rulePB)),
                               lo=1e-3, hi=0.3, iters=6, max_kicks=2500)
        print(json.dumps({"eps_rel": eps, "trace": trace}, indent=1, default=float))
    elif cmd == "scenep":
        nm, eps = sys.argv[2], float(sys.argv[3])
        sc = SCENES[nm]
        T = sc["T_orb"] * TWO_PI
        s0 = state0_from_elements(1.0, sc["e0"])
        truth = make_truth(s0, sc["mu_r"], sc["D"], T)
        out = {"scene": nm, "slope_true": truth["slope_true"], "runs": {}}
        for rn, mk in (("rulePA", make_rulePA), ("rulePB", make_rulePB)):
            m = run_kicked(s0, sc["mu_r"], sc["D"], T, mk(eps, sc["mu_r"], sc["D"]))
            res = metrics(m, truth, sc["e0"], T, ts=truth["ts"])
            res["holds"] = holds(res, sc["e0"])
            out["runs"][rn] = res
        print(json.dumps(out, indent=1, default=float))
    elif cmd == "mixedp":
        print(json.dumps(run_mixed(float(sys.argv[2]),
                                   rules=(("rulePA", make_rulePA), ("rulePB", make_rulePB))),
                         indent=1, default=float))
    elif cmd == "mixedv":
        print(json.dumps(run_mixed(float(sys.argv[2]),
                                   rules=(("ruleVA", make_ruleVA), ("ruleVB", make_ruleVB))),
                         indent=1, default=float))
    elif cmd == "selftest":
        sc = SCENES["cal"]
        T = sc["T_orb"] * TWO_PI
        s0 = state0_from_elements(1.0, sc["e0"])
        tr = make_truth(s0, sc["mu_r"], sc["D"], T)
        r = {}
        for N in (8, 64):
            m = run_kicked(s0, sc["mu_r"], sc["D"], T, lambda s, t, el, N=N: TWO_PI / N)
            r[f"fixed{N}"] = metrics(m, tr, sc["e0"], T, ts=tr["ts"])
        # truth convergence: halve dt
        tr2 = make_truth(s0, sc["mu_r"], sc["D"], T, 1024.0)
        r["slope_conv_rel"] = abs(tr["slope_true"] - tr2["slope_true"]) / abs(tr2["slope_true"])
        r["slope_true"] = tr["slope_true"]
        print(json.dumps(r, indent=1, default=float))
    else:
        raise SystemExit("unknown cmd")
