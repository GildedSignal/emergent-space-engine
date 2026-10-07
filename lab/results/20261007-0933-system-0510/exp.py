#!/usr/bin/env python3
"""System-lens probe: are kicks and encounters one event?

Claim under test: the synodic conjunction (one per pair, timed by the integer
circle rotation that crates/encounters already runs for encounter windows) can
carry the *kick* too: one impulse per conjunction, memoized on a quasi-static
pair-geometry key, replaces (a) the fixed-cadence orbit-averaged kick layer,
(b) the separate resonance detector, and (c) the duplicate window setup.

Scene: Sun + one Jupiter (circular, a=5.2 AU, mu=9.5455e-4 in GM_sun=1 units,
t in yr/2pi), planar, test particles (belt + a 2:1 resonance scan).

Three laws:
  REF : Wisdom-Holman style, Kepler drift + Jupiter kick every h = T(2.6)/96.
  A   : the current design's away-from-resonance layer: orbit-averaged
        (double-averaged) quadrupole rate, dvarpi/dt = 0.75 n mu alpha^3.
  B   : the unified event: one Gauss-equation impulse per synodic conjunction,
        quadrature along the unperturbed orbit over the elapsed window,
        memoized by (quantized a, e, conjunction phase).

Prints one JSON line.
"""
import json
import math
import sys

import numpy as np

TAU = 2.0 * math.pi
MU_J = 9.5455e-4
A_J = 5.2
N_J = A_J ** -1.5
LAM_J0 = 0.0

MEMO = {}


def kepler_E(M, e):
    M = np.mod(M, TAU)
    E = M.copy()
    for _ in range(12):
        f = E - e * np.sin(E) - M
        fp = 1.0 - e * np.cos(E)
        d = np.clip(f / fp, -1.0, 1.0)
        E = E - d
        if np.max(np.abs(d)) < 1e-14:
            break
    return E


def elem_to_cart(a, e, varpi, M):
    n = a ** -1.5
    E = kepler_E(M, e)
    cosE, sinE = np.cos(E), np.sin(E)
    r = a * (1.0 - e * cosE)
    cosf = (cosE - e) / (1.0 - e * cosE)
    sinf = np.sqrt(1.0 - e * e) * sinE / (1.0 - e * cosE)
    th = varpi + np.arctan2(sinf, cosf)
    x = r * np.cos(th)
    y = r * np.sin(th)
    # velocities: d(position)/dE * dE/dt, GM = 1
    dEdt = n / (1.0 - e * cosE)
    sa, ca = np.sin(varpi), np.cos(varpi)
    b = a * np.sqrt(1.0 - e * e)
    vx = (-a * sinE * ca - b * cosE * sa) * dEdt
    vy = (-a * sinE * sa + b * cosE * ca) * dEdt
    return x, y, vx, vy


def cart_to_elem(x, y, vx, vy):
    r = np.hypot(x, y)
    v2 = vx * vx + vy * vy
    a = 1.0 / (2.0 / r - v2)
    rv = x * vx + y * vy
    ex = (v2 - 1.0 / r) * x - rv * vx
    ey = (v2 - 1.0 / r) * y - rv * vy
    e = np.hypot(ex, ey)
    varpi = np.arctan2(ey, ex)
    cosE = np.clip((1.0 - r / a) / np.maximum(e, 1e-300), -1.0, 1.0)
    E = np.sign(rv) * np.arccos(cosE)
    E = np.where(rv >= 0, np.arccos(cosE), -np.arccos(cosE))
    M = E - e * np.sin(E)
    return a, e, varpi, M


def jupiter_xy(t):
    lam = LAM_J0 + N_J * t
    return A_J * np.cos(lam), A_J * np.sin(lam)


def accel(x, y, t):
    xj, yj = jupiter_xy(t)
    dx = xj - x
    dy = yj - y
    d3 = (dx * dx + dy * dy) ** 1.5
    ax = MU_J * dx / d3 - MU_J * xj / A_J ** 3
    ay = MU_J * dy / d3 - MU_J * yj / A_J ** 3
    return ax, ay


def gauss_rates(a, e, varpi, M, t):
    """Instantaneous Gauss rates at osculating (a,e,varpi,M), Jupiter at t."""
    n = a ** -1.5
    E = kepler_E(M, e)
    cosE, sinE = np.cos(E), np.sin(E)
    r = a * (1.0 - e * cosE)
    cosf = (cosE - e) / (1.0 - e * cosE)
    sinf = math.sqrt(max(1.0 - e * e, 0.0)) * sinE / (1.0 - e * cosE)
    th = varpi + np.arctan2(sinf, cosf)
    x = r * np.cos(th)
    y = r * np.sin(th)
    ax, ay = accel(x, y, t)
    rx, ry = x / r, y / r
    R = ax * rx + ay * ry
    T = -ax * ry + ay * rx
    p = a * (1.0 - e * e)
    sq = math.sqrt(max(1.0 - e * e, 1e-18))
    da = 2.0 / (n * sq) * (e * sinf * R + (p / r) * T)
    de = sq / (n * a) * (R * sinf + T * (cosf + cosE))
    dvarpi = sq / (n * a * max(e, 1e-12)) * (-R * cosf + T * sinf * (1.0 + r / p))
    dlam = -2.0 * r * R / (n * a * a)
    return da, de, dvarpi, dlam


def window_impulse(a, e, varpi, lam0, t0, t1, S=64):
    """Simpson integral of the Gauss rates over [t0,t1], unperturbed motion."""
    ts = np.linspace(t0, t1, 2 * S + 1)
    lam = lam0 + a ** -1.5 * (ts - t0)
    M = lam - varpi
    da, de, dw, dl = gauss_rates(a, e, varpi, M, ts)
    arr = np.stack([da, de, dw, dl])
    w = np.ones(2 * S + 1)
    w[1:-1:2] = 4.0
    w[2:-1:2] = 2.0
    w *= (t1 - t0) / (6.0 * S)
    return arr @ w


def run_ref(particles, H, h, stride=16):
    """Leapfrog: half kick, Kepler drift, half kick. Logs elements per stride."""
    a0 = np.array([p["a"] for p in particles])
    e0 = np.array([p["e"] for p in particles])
    w0 = np.array([p["varpi"] for p in particles])
    M0 = np.array([p["M"] for p in particles])
    x, y, vx, vy = elem_to_cart(a0, e0, w0, M0)
    n_steps = int(round(H / h))
    n_log = n_steps // stride + 1
    log_t = np.empty(n_log)
    log_a = np.empty((n_log, len(particles)))
    log_e = np.empty_like(log_a)
    log_w = np.empty_like(log_a)
    j = 0
    for i in range(n_steps + 1):
        t = i * h
        a_, e_, w_, _ = cart_to_elem(x, y, vx, vy)
        if i % stride == 0:
            log_t[j], log_a[j], log_e[j], log_w[j] = t, a_, e_, w_
            j += 1
        if i == n_steps:
            break
        ax, ay = accel(x, y, t)
        vx = vx + 0.5 * h * ax
        vy = vy + 0.5 * h * ay
        a_, e_, w_, M_ = cart_to_elem(x, y, vx, vy)
        x, y, vx, vy = elem_to_cart(a_, e_, w_, M_ + a_ ** -1.5 * h)
        ax, ay = accel(x, y, t + h)
        vx = vx + 0.5 * h * ax
        vy = vy + 0.5 * h * ay
    return log_t, log_a, log_e, log_w, h * stride


def run_B(particle, H):
    """One impulse per synodic conjunction, memoized on pair geometry."""
    a, e, varpi = particle["a"], particle["e"], particle["varpi"]
    lam = particle["varpi"] + particle["M"]
    memo = MEMO
    hits = misses = 0
    t = 0.0
    events = []
    conj_longs = []
    first = True
    while True:
        n = a ** -1.5
        if first:
            t_c = ((LAM_J0 - lam) % TAU) / (n - N_J)
            first = False
        else:
            t_c = t + TAU / (n - N_J)
        if t_c > H:
            break
        lam_Jc = LAM_J0 + N_J * t_c
        Mc = (lam_Jc - varpi) % TAU
        key = (round(a / 0.02), round(e / 0.01), int(Mc / TAU * 64) % 64)
        if key in memo:
            imp = memo[key]
            hits += 1
        else:
            imp = window_impulse(a, e, varpi, lam, t, t_c)
            memo[key] = imp
            misses += 1
        da, de, dw, dl = imp
        a = a + da
        e = abs(e + de)
        varpi = varpi + dw
        lam = lam_Jc + dl
        events.append((t_c, a, e, varpi))
        conj_longs.append(lam_Jc % TAU)
        t = t_c
    if t < H:
        imp = window_impulse(a, e, varpi, lam, t, H)
        a += imp[0]
        e = abs(e + imp[1])
        varpi += imp[2]
        events.append((H, a, e, varpi))
    return events, hits, misses, conj_longs


def wrap_pi(x):
    return (x + math.pi) % TAU - math.pi


def cluster_return(conj_longs, dmax=4):
    """Conjunction-longitude return quality: best d<=dmax clustering."""
    cl = np.array(conj_longs)
    best = 0.0
    for d in range(1, dmax + 1):
        res = cl * d
        spread = np.std(np.mod(res + math.pi, TAU) - math.pi)
        best = max(best, 1.0 - spread / math.pi)
    return best


def main():
    rng = np.random.default_rng(20261007)
    particles = []
    for _ in range(30):
        particles.append(dict(a=float(rng.uniform(2.60, 3.15)),
                              e=float(rng.uniform(0.02, 0.15)),
                              varpi=float(rng.uniform(0, TAU)),
                              M=float(rng.uniform(0, TAU))))
    a_res = A_J * 2.0 ** (-2.0 / 3.0)
    for fac in (0.97, 0.985, 0.995, 1.0, 1.005, 1.015, 1.03):
        particles.append(dict(a=a_res * fac, e=0.05,
                              varpi=float(rng.uniform(0, TAU)),
                              M=float(rng.uniform(0, TAU))))

    H = float(sys.argv[1]) if len(sys.argv) > 1 else 24000.0
    h = TAU * 2.6 ** 1.5 / 96.0
    log_t, log_a, log_e, log_w, hstep = run_ref(particles, H, h)

    def ref_at(t, arr, idx):
        i = min(max(int(round(t / hstep)), 0), len(log_t) - 1)
        return arr[i, idx]

    away, near = [], []
    results = []
    total_hits = total_misses = 0
    for idx, p in enumerate(particles):
        events, hits, misses, cl = run_B(p, H)
        total_hits += hits
        total_misses += misses
        q = cluster_return(cl)
        T_orb = TAU * p["a"] ** 1.5
        ev_per_orbit = len(events) * T_orb / H
        errs_w = []
        for (t_c, _a, _e, wB) in events[::5]:
            errs_w.append(abs(wrap_pi(wB - ref_at(t_c, log_w, idx))))
        e_ref_max = max(float(ref_at(t_c, log_e, idx)) for (t_c, _, _, _) in events)
        e_B_max = max(e for (_, _, e, _) in events)
        gA = 0.75 * p["a"] ** -1.5 * MU_J * (p["a"] / A_J) ** 3
        ts = np.array([ev[0] for ev in events[::5]])
        wB_u = np.unwrap([ev[3] for ev in events[::5]])
        wR_u = np.unwrap([ref_at(t, log_w, idx) for t in ts])
        rate_B = float(np.polyfit(ts, wB_u, 1)[0])
        rate_ref = float(np.polyfit(ts, wR_u, 1)[0])
        rate_A = gA
        rec = dict(
            idx=idx, a=round(p["a"], 4), e0=p["e"], q_return=round(q, 3),
            ev_per_orbit=round(ev_per_orbit, 3),
            rate_ref=round(rate_ref, 8), rate_B=round(rate_B, 8),
            rate_A=round(rate_A, 8),
            relerr_rate_B=round(abs(rate_B - rate_ref) / max(abs(rate_ref), 1e-9), 4),
            relerr_rate_A=round(abs(rate_A - rate_ref) / max(abs(rate_ref), 1e-9), 4),
            err_w_B=round(float(np.median(errs_w)), 5),
            pump_ref=round(float(e_ref_max / p["e"]), 3),
            pump_B=round(float(e_B_max / p["e"]), 3),
            pump_ratio_B=round(float(e_B_max / max(e_ref_max, 1e-9)), 3),
            err_e_final=round(abs(events[-1][2] - ref_at(events[-1][0], log_e, idx)), 5),
        )
        results.append(rec)
        (near if q > 0.8 else away).append(rec)

    out = dict(
        exp="conjunction-unified-kick", H=H, n_part=len(particles),
        B_events_per_orbit_median=round(float(np.median([r["ev_per_orbit"] for r in results])), 3),
        memo_hits=total_hits, memo_misses=total_misses,
        memo_hit_rate=round(total_hits / max(total_hits + total_misses, 1), 3),
        n_away=len(away), n_near=len(near),
        away_relerr_rate_B_median=round(float(np.median([r["relerr_rate_B"] for r in away])), 4),
        away_relerr_rate_A_median=round(float(np.median([r["relerr_rate_A"] for r in away])), 4),
        away_err_w_B_median=round(float(np.median([r["err_w_B"] for r in away])), 5),
        away_err_e_final_median=round(float(np.median([r["err_e_final"] for r in away])), 5),
        away_pump_ref_median=round(float(np.median([r["pump_ref"] for r in away])), 3),
        away_pump_B_median=round(float(np.median([r["pump_B"] for r in away])), 3),
        near=[{k: r[k] for k in ("a", "q_return", "pump_ref", "pump_B", "pump_ratio_B")} for r in near],
        results=results,
    )
    print(json.dumps(out))


if __name__ == "__main__":
    main()
