#!/usr/bin/env python3
"""Belt surrogate of the kick layer: fixed cadence vs level-triggered scheduled kicks.

Machinery for every policy: exact Kepler drift between kicks (mean anomaly + Newton),
impulse kick dv = a_pert * dt at each kick. Truth = same machinery at 512 kicks/orbit.
Trigger policies (no per-frame checks; the next kick is SCHEDULED in closed form):
  mag :  dt = delta_v / |a_pert|                     (killed by the first run)
  jerk:  dt = sqrt(2 delta_v / jerk_est), jerk_est = max(2 mu_p |ddot|/d^3, a_pert |n-n_p|)
Cost counted = kicks applied. Deterministic seeds. Floats explore; kick counts (integers) decide.
"""
import json
import sys

import numpy as np

MU = 1.0
MU_P = 3e-3
A_P = 1.6
N_P = np.sqrt(MU / A_P**3)  # perturber mean motion
T_ORB = 10.0
MAX_DT = 1.0


def make_belt(n, sigma_e, seed):
    rng = np.random.default_rng(seed)
    a = rng.uniform(0.95, 1.05, n)
    e = rng.rayleigh(sigma_e, n).clip(0.0, 0.4)
    w = rng.uniform(0.0, 2 * np.pi, n)
    M0 = rng.uniform(0.0, 2 * np.pi, n)
    return a, e, w, M0


def kepler_state(a, e, w, M):
    E = M.copy()
    for _ in range(6):
        E = E - (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    cosE, sinE = np.cos(E), np.sin(E)
    denom = 1.0 - e * cosE
    xo = a * (cosE - e)
    yo = a * np.sqrt(1.0 - e * e) * sinE
    n = np.sqrt(MU / a**3)
    vxo = -a * n * sinE / denom
    vyo = a * n * np.sqrt(1.0 - e * e) * cosE / denom
    cw, sw = np.cos(w), np.sin(w)
    return (cw * xo - sw * yo, sw * xo + cw * yo,
            cw * vxo - sw * vyo, sw * vxo + cw * vyo)


def planet_state(t):
    th = N_P * t
    xp, yp = A_P * np.cos(th), A_P * np.sin(th)
    vpx, vpy = -A_P * N_P * np.sin(th), A_P * N_P * np.cos(th)
    return xp, yp, vpx, vpy


def a_pert(x, y, t):
    xp, yp, _, _ = planet_state(t)
    dx, dy = x - xp, y - yp
    d2 = dx * dx + dy * dy
    return -MU_P * dx / (d2 * np.sqrt(d2)), -MU_P * dy / (d2 * np.sqrt(d2)), MU_P / d2


def jerk_interval(x, y, vx, vy, nn, t, delta_v, dt_min):
    """dt = sqrt(2 delta_v / jerk_est); local, closed form."""
    xp, yp, vpx, vpy = planet_state(t)
    dx, dy = x - xp, y - yp
    d2 = dx * dx + dy * dy
    d = np.sqrt(d2)
    ddot = ((vx - vpx) * dx + (vy - vpy) * dy) / d
    a_mag = MU_P / d2
    n_rel = np.abs(nn - N_P)
    jerk = np.maximum(2.0 * MU_P * np.abs(ddot) / (d2 * d), a_mag * n_rel)
    return np.clip(np.sqrt(2.0 * delta_v / jerk), dt_min, MAX_DT)


def rederive(idx, x, y, vx, vy, a, e, w, M):
    r2 = x * x + y * y
    r = np.sqrt(r2)
    v2 = vx * vx + vy * vy
    rv = x * vx + y * vy
    a_new = 1.0 / (2.0 / r - v2 / MU)
    ex = (v2 * x - rv * vx) / MU - x / r
    ey = (v2 * y - rv * vy) / MU - y / r
    e_new = np.sqrt(ex * ex + ey * ey)
    w_new = np.arctan2(ey, ex)
    ok = e_new > 1e-12
    cosE = np.clip((1.0 - r / a_new) / np.where(ok, e_new, 1.0), -1, 1)
    vr = rv / r
    sinE = np.where(ok, vr * r / (e_new * np.sqrt(MU * np.maximum(a_new, 1e-9))), 0.0)
    E = np.arctan2(sinE, cosE)
    a[idx] = a_new
    e[idx] = np.where(ok, e_new, 0.0).clip(0.0, 0.4)
    w[idx] = w_new
    M[idx] = np.mod(E - e_new * np.sin(E), 2 * np.pi)


def run_policy(a, e, w, M, policy, param, kgrid):
    n = a.size
    nn = np.sqrt(MU / np.maximum(a, 1e-9) ** 3)
    t_last = np.zeros(n)
    kicks = np.zeros(n, dtype=np.int64)
    dtg = 1.0 / kgrid
    kick_dt = 1.0 / param
    x0, y0, vx0, vy0 = kepler_state(a, e, w, M)
    if policy == "trigger":
        _, _, amag = a_pert(x0, y0, 0.0)
        next_t = np.clip(param / amag, dtg, MAX_DT)
    elif policy == "jerk":
        next_t = jerk_interval(x0, y0, vx0, vy0, nn, 0.0, param, dtg)
    else:
        next_t = np.full(n, kick_dt)
    t_sim = 0.0
    while t_sim < T_ORB - 1e-12:
        t_sim += dtg
        due = next_t <= t_sim + 1e-12
        if not due.any():
            continue
        M[due] += nn[due] * (t_sim - t_last[due])
        xd, yd, vxd, vyd = kepler_state(a[due], e[due], w[due], M[due])
        ax, ay, amag = a_pert(xd, yd, t_sim)
        dtk = t_sim - t_last[due]
        vx = vxd + ax * dtk
        vy = vyd + ay * dtk
        kicks[due] += 1
        t_last[due] = t_sim
        rederive(due, xd, yd, vx, vy, a, e, w, M)
        nn[due] = np.sqrt(MU / np.maximum(a[due], 1e-9) ** 3)
        if policy == "trigger":
            next_t[due] = t_sim + np.clip(param / amag, dtg, MAX_DT)
        elif policy == "jerk":
            next_t[due] = t_sim + jerk_interval(xd, yd, vx, vy, nn[due], t_sim, param, dtg)
        else:
            next_t[due] = t_sim + kick_dt
    return a, kicks


def metrics(ap, a_truth, kk):
    ok = np.isfinite(ap) & np.isfinite(a_truth) & (ap > 0)
    err = np.abs(ap[ok] - a_truth[ok]) / a_truth[ok]
    return dict(med=float(np.median(err)) if err.size else float("nan"),
                p95=float(np.percentile(err, 95)) if err.size else float("nan"),
                kicks=int(kk.sum()), k_med=int(np.median(kk)),
                k_p99=int(np.percentile(kk, 99)), lost=int((~ok).sum()))


def main():
    scene = sys.argv[1] if len(sys.argv) > 1 else "cold"
    sigma_e = 0.05 if scene == "cold" else 0.20
    rows = []
    for seed in (1, 2, 3):
        a0, e0, w0, M0 = make_belt(1000, sigma_e, seed)
        a_truth, _ = run_policy(a0.copy(), e0.copy(), w0.copy(), M0.copy(), "fixed", 512, 512)
        row = {"seed": seed}
        for k in (8, 16, 32, 64):
            ap, kk = run_policy(a0.copy(), e0.copy(), w0.copy(), M0.copy(), "fixed", k, k)
            row[f"fixed{k}"] = metrics(ap, a_truth, kk)
        for dv in (1e-6, 3e-6, 1e-5, 3e-5, 1e-4):
            ap, kk = run_policy(a0.copy(), e0.copy(), w0.copy(), M0.copy(), "trigger", dv, 128)
            row[f"mag{dv:g}"] = metrics(ap, a_truth, kk)
        for dv in (1e-6, 3e-6, 1e-5, 3e-5, 1e-4):
            ap, kk = run_policy(a0.copy(), e0.copy(), w0.copy(), M0.copy(), "jerk", dv, 128)
            row[f"jerk{dv:g}"] = metrics(ap, a_truth, kk)
        rows.append(row)
    keys = [k for k in rows[0] if isinstance(rows[0][k], dict)]
    agg = {key: {m: float(np.median([r[key][m] for r in rows])) for m in
                 ("med", "p95", "kicks", "k_med", "k_p99", "lost")} for key in keys}
    with open(f"cadence_{scene}.json", "w") as f:
        json.dump({"scene": scene, "sigma_e": sigma_e, "rows": rows, "aggregate_median": agg}, f, indent=1)
    print(f"scene={scene} sigma_e={sigma_e}  (N=1000, T=10 orbits, truth=512/orbit)")
    print(f"{'policy':>10} {'med_err':>10} {'p95_err':>10} {'total_kicks':>12} {'k_med':>7} {'k_p99':>7} {'lost':>5}")
    for key, v in agg.items():
        print(f"{key:>10} {v['med']:10.3e} {v['p95']:10.3e} {int(v['kicks']):12d} "
              f"{int(v['k_med']):7d} {int(v['k_p99']):7d} {int(v['lost']):5d}")


if __name__ == "__main__":
    main()
