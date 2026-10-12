#!/usr/bin/env python3
"""Dynamics-lens probe: the (E,L) key process of a belt under a Jupiter-like secondary.

Scene: circular restricted three-body. Star M=1 fixed at origin; planet (mass ratio mu)
on an exact circle a=1; test particles (ships) integrated.
Integrator: the design's own path — exact Kepler drift in the star's doll (universal
variables, warm-started Newton) + second-order kicks for the planet's direct +
indirect term (WHD split). With mu=0 the trajectory is machine-exact: the control.

Per body, once per planet orbit, sample E, L and the key k=(round(E/qE), round(L/qL))
at relative quantum q. Reported per body:
  revisit    steady-state fraction of samples whose key was seen before (memo hit, lagged)
  churn      distinct keys per planet orbit in the steady-state half (compile rate proxy)
  lam_hat    ln(max separation / d0) / T of an unrenormalised shadow pair:
             ~0 regular; = lambda while unsaturated; = ln(d_sat/d0)/T once saturated
             (regime classifier, not an exponent estimator; shear-unbiased)
  d_res      min_p/q |n_b/n_pl - p/q| over q<=15 from the second-half mean a
             (the engine's own detector: resonance distance from compiled frequencies)
  msd_slope  log-log slope of Var(a(t+tau)-a(t)) over lags 8/32/128 planet orbits
             (~1 diffusive, ~0 bounded)
"""
import argparse, json, math, os, time
import numpy as np

def stumpff(z):
    C = np.where(z > 1e-8, (1 - np.cos(np.sqrt(np.maximum(z, 0)))) / np.maximum(z, 1e-300),
                0.5 - z / 24.0 + z * z / 720.0)
    sq = np.sqrt(np.maximum(z, 0))
    S = np.where(z > 1e-8, (sq - np.sin(sq)) / np.maximum(z * sq, 1e-300),
                1.0 / 6.0 - z / 120.0 + z * z / 5040.0)
    return C, S

def kepler_drift(x, v, dt, chi0=None):
    """Exact two-body drift (mu=1), vectorised universal variables."""
    r0 = np.sqrt((x * x).sum(axis=1))
    v2 = (v * v).sum(axis=1)
    rv = (x * v).sum(axis=1)
    alpha = 2.0 / r0 - v2
    sa = np.sqrt(np.maximum(alpha, 0.0))
    chi = sa * dt if chi0 is None else chi0 + sa * dt
    for _ in range(8):
        z = alpha * chi * chi
        C, S = stumpff(z)
        F = rv * chi * chi * C + (1 - alpha * r0) * chi ** 3 * S + r0 * chi - dt
        dF = rv * chi * (1 - z * S) + (1 - alpha * r0) * chi * chi * C + r0
        st = F / dF
        chi = chi - st
        if np.abs(st).max() < 1e-15:
            break
    z = alpha * chi * chi
    C, S = stumpff(z)
    f = 1.0 - chi * chi / r0 * C
    g = dt - chi ** 3 * S
    xn = f[:, None] * x + g[:, None] * v
    rn = np.sqrt((xn * xn).sum(axis=1))
    fd = (alpha * chi ** 3 * S - chi) / (r0 * rn)
    gd = 1.0 - chi * chi / rn * C
    vn = fd[:, None] * x + gd[:, None] * v
    return xn, vn, chi

def kepler_start(a, e, Ma, w):
    E = Ma
    for _ in range(10):
        E = E - (E - e * math.sin(E) - Ma) / (1 - e * math.cos(E))
    xf = np.array([a * (math.cos(E) - e), a * math.sqrt(1 - e * e) * math.sin(E)])
    vf = np.array([-math.sin(E), math.sqrt(1 - e * e) * math.cos(E)]) * math.sqrt(1.0 / a) / (1 - e * math.cos(E))
    cw, sw = math.cos(w), math.sin(w)
    R = np.array([[cw, -sw], [sw, cw]])
    return R @ xf, R @ vf

def res_distance(nb_over_npl):
    """min over p/q (q<=15) of |ratio - p/q|."""
    best = 1e9
    for q in range(1, 16):
        p = max(1, int(round(q * nb_over_npl)))
        for pp in (p - 1, p, p + 1):
            if pp < 1:
                continue
            d = abs(nb_over_npl - pp / q)
            best = min(best, d)
    return best

QLIST = [1e-4, 1e-5, 1e-6]

def run(mu, T, spf, N, e0, amin, amax, seed):
    rng = np.random.default_rng(seed)
    P = 2.0 * math.pi
    h = P / spf
    n_pl = 1.0

    a0 = amin + (amax - amin) * rng.random(N)
    M0 = rng.uniform(0, 2 * math.pi, N)
    w0 = rng.uniform(0, 2 * math.pi, N)
    x = np.empty((N, 2)); v = np.empty((N, 2))
    for i in range(N):
        x[i], v[i] = kepler_start(a0[i], e0, M0[i], w0[i])

    d0 = 1e-9
    dx = rng.normal(size=(N, 2)); dx /= np.linalg.norm(dx, axis=1, keepdims=True)
    xs = x + d0 * dx; vs = v.copy()
    dmax = np.zeros(N)

    def kick(xx, t):
        cp, sp = math.cos(n_pl * t), math.sin(n_pl * t)
        rx = xx[:, 0] - cp; ry = xx[:, 1] - sp
        rpl = np.sqrt(rx * rx + ry * ry) ** 3
        return np.stack([mu * (rx / rpl - cp), mu * (ry / rpl - sp)], axis=1)

    E_s = np.empty((T, N)); L_s = np.empty((T, N))
    t = 0.0; idx = 0; t0 = time.time()
    chi = None; chis = None
    for step in range(T * spf):
        if step % spf == 0 and idx < T:
            r = np.sqrt((x * x).sum(axis=1)); v2 = (v * v).sum(axis=1)
            E_s[idx] = 0.5 * v2 - 1.0 / r
            L_s[idx] = x[:, 0] * v[:, 1] - x[:, 1] * v[:, 0]
            idx += 1
        v = v + 0.5 * h * kick(x, t)
        x, v, chi = kepler_drift(x, v, h, chi)
        v = v + 0.5 * h * kick(x, t + h)
        vs = vs + 0.5 * h * kick(xs, t)
        xs, vs, chis = kepler_drift(xs, vs, h, chis)
        vs = vs + 0.5 * h * kick(xs, t + h)
        t += h
        if (step + 1) % spf == 0:
            d = np.sqrt(((xs - x) ** 2).sum(axis=1))
            dmax = np.maximum(dmax, d)
    lam_hat = np.log(np.maximum(dmax, d0) / d0) / (T * P)
    wall = time.time() - t0

    a_typ = 0.5 * (amin + amax)
    half = T // 2
    qstats = {}
    for qq in QLIST:
        qE = qq / (2 * a_typ); qL = qq / math.sqrt(a_typ)
        key = np.round(E_s / qE).astype(np.int64) * 2000000011 + np.round(L_s / qL).astype(np.int64)
        st = []
        for i in range(N):
            k2 = key[half:, i]
            distinct_2 = int(len(np.unique(k2)))
            seen = set(); revisits = 0
            for kk in k2.tolist():
                if kk in seen: revisits += 1
                seen.add(kk)
            st.append(dict(churn=distinct_2 / max(len(k2), 1), distinct2=distinct_2,
                           revisit=revisits / max(len(k2) - 1, 1)))
        qstats[f"{qq:.0e}"] = st
    out = []
    for i in range(N):
        a_s = -0.5 / E_s[:, i]
        tail = a_s[half:]
        lags = [8, 32, 128]
        msd = [float(np.var(tail[lag:] - tail[:-lag])) for lag in lags]
        slope = float(np.polyfit(np.log(lags), np.log(np.maximum(msd, 1e-300)), 1)[0]) if msd[2] > 0 else 0.0
        a_mean = float(tail.mean())
        nb = (a_mean if a_mean > 0 else float(a0[i])) ** -1.5
        out.append(dict(a0=float(a0[i]), a_mean=a_mean, lam=float(lam_hat[i]),
                        d_res=float(res_distance(nb)) if a_mean > 0 else -1.0,
                        msd=msd, msd_slope=slope,
                        a_range=float(tail.max() - tail.min()),
                        a_range1=float(a_s[:half].max() - a_s[:half].min())))
    return dict(wall=wall, bodies=out, qstats=qstats, mu=mu, T=T, spf=spf, N=N, e0=e0,
                amin=amin, amax=amax, seed=seed, qlist=[f"{qq:.0e}" for qq in QLIST],
                lam_floor=math.log(0.5 / d0) / (T * P))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mu", type=float, default=1e-3)
    ap.add_argument("--T", type=int, default=2000)
    ap.add_argument("--spf", type=int, default=24)
    ap.add_argument("--N", type=int, default=96)
    ap.add_argument("--e0", type=float, default=0.05)
    ap.add_argument("--amin", type=float, default=0.55)
    ap.add_argument("--amax", type=float, default=1.9)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--tag", default="run")
    args = ap.parse_args()
    r = run(args.mu, args.T, args.spf, args.N, args.e0, args.amin, args.amax, args.seed)
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, f"{args.tag}.json"), "w") as f:
        json.dump(r, f, indent=1)
    lam = np.array([b["lam"] for b in r["bodies"]])
    rev = np.array([s["revisit"] for s in r["qstats"][r["qlist"][0]]])
    print(f"{args.tag}: wall={r['wall']:.1f}s lam[max]={lam.max():.2e} revisit[q={r['qlist'][0]}]mean={rev.mean():.3f}")

if __name__ == "__main__":
    main()
