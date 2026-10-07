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


def window_impulse(a, e, varpi, lam0, t0, t1, S=64, vec=False):
    """Simpson integral of the Gauss rates over [t0,t1], unperturbed motion.

    vec=False: law B, increments of (da, de, dvarpi, dlam) — dvarpi carries a
    1/e factor, so the window's non-orbit-closure residual is O(mu/e).
    vec=True: law B2, increments of the eccentricity vector (da, d(e cos varpi),
    d(e sin varpi), dlam) at the window-start varpi — regular at e -> 0.
    """
    ts = np.linspace(t0, t1, 2 * S + 1)
    lam = lam0 + a ** -1.5 * (ts - t0)
    M = lam - varpi
    da, de, dw, dl = gauss_rates(a, e, varpi, M, ts)
    if vec:
        cw, sw = math.cos(varpi), math.sin(varpi)
        dhx = de * cw - e * sw * dw
        dhy = de * sw + e * cw * dw
        arr = np.stack([da, dhx, dhy, dl])
    else:
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


def run_B(particle, H, vec=False):
    """One impulse per synodic conjunction, memoized on pair geometry.

    vec=True (law B2): the state is the eccentricity vector (hx, hy) =
    (e cos varpi, e sin varpi); impulses are its regular components.
    """
    a, e, varpi = particle["a"], particle["e"], particle["varpi"]
    hx, hy = e * math.cos(varpi), e * math.sin(varpi)
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
            imp = window_impulse(a, e, varpi, lam, t, t_c, vec=vec)
            memo[key] = imp
            misses += 1
        if vec:
            da, dhx, dhy, dl = imp
            a = a + da
            hx = hx + dhx
            hy = hy + dhy
            e = math.hypot(hx, hy)
            varpi = math.atan2(hy, hx)
        else:
            da, de, dw, dl = imp
            a = a + da
            e = abs(e + de)
            varpi = varpi + dw
        lam = lam_Jc + dl
        events.append((t_c, a, e, varpi))
        conj_longs.append(lam_Jc % TAU)
        t = t_c
    if t < H:
        imp = window_impulse(a, e, varpi, lam, t, H, vec=vec)
        a += imp[0]
        if vec:
            hx += imp[1]
            hy += imp[2]
            e = math.hypot(hx, hy)
            varpi = math.atan2(hy, hx)
        else:
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


class NoMemo(dict):
    """A memo that never stores and never hits (the no-memo control)."""

    def __contains__(self, key):
        return False

    def __setitem__(self, key, value):
        pass


C0 = 2.5 * MU_J ** (2.0 / 3.0) / math.sqrt(MU_J * 0.02)
# Width model (a priori, law.md's compiled-frequency test + B17's frozen width):
# order-k resonance half-width in mean-motion ratio  W_k(e) = C * sqrt(mu * e^k)
# (pendulum scaling, Murray & Dermott ch. 8), anchored so that the first-order
# half-width at e0 = 0.02 equals B17's W = 2.5 * mu^(2/3).  The verdict is
# reported at C in {C0/2, C0, 2*C0}: the factor-2 band covers B17's
# a-vs-frequency normalization ambiguity.


def build_resonances():
    """Reduced interior pairs (p, q) whose a_res lands near the belt."""
    res = []
    for q in range(2, 15):
        for p in range(1, q):
            if math.gcd(p, q) != 1:
                continue
            k = q - p
            if not 1 <= k <= 8:
                continue
            a_res = A_J * (p / q) ** (2.0 / 3.0)
            if 2.45 <= a_res <= 3.55:
                res.append((p, q, k, a_res))
    return res


RES = build_resonances()


def freq_diag(a, e):
    """Nearest compiled-frequency resonance, in detune / width units."""
    n = a ** -1.5
    best = None
    for (p, q, k, a_res) in RES:
        ratio = q / p
        detune = abs(n / N_J - ratio) / ratio
        unit = detune / math.sqrt(e ** k)  # excluded(C) iff unit < C*sqrt(mu)
        if best is None or unit < best[0]:
            best = (unit, p, q, k, a_res, detune,
                    C0 * math.sqrt(MU_J * e ** k))
    return best


def tailstats(vals):
    v = sorted(vals)
    n = len(v)
    if n == 0:
        return None
    med = v[n // 2] if n % 2 else 0.5 * (v[n // 2 - 1] + v[n // 2])
    p90 = v[min(n - 1, int(math.ceil(0.9 * n)) - 1)]
    return dict(n=n, med=round(med, 4), p90=round(p90, 4), max=round(v[-1], 4))


def agg(recs, C):
    sq = C * math.sqrt(MU_J)
    away = [r for r in recs if r["min_detunit"] >= sq]
    excl = [r for r in recs if r["min_detunit"] < sq]
    return dict(
        n_rec=len(recs), n_away=len(away), n_excluded=len(excl),
        excluded_a=sorted(r["a"] for r in excl),
        rate_B=tailstats([r["relerr_rate_B"] for r in away]),
        rate_A=tailstats([r["relerr_rate_A"] for r in away]),
        wrongsign_B=sum(r["wrongsign_B"] for r in away),
        wrongsign_A=sum(r["wrongsign_A"] for r in away),
        env_B=tailstats([r["err_env_B"] for r in away]),
        env_A=tailstats([r["err_env_A"] for r in away]),
        cadence_med=round(float(np.median([r["ev_per_orbit"] for r in away])), 3)
        if away else None,
        rate_B_worst_a=max(away, key=lambda r: r["relerr_rate_B"])["a"]
        if away else None,
    )


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--H", type=float, default=24000.0)
    ap.add_argument("--seed", type=int, default=20261007)
    ap.add_argument("--memo", choices=["on", "off"], default="on")
    ap.add_argument("--law", choices=["B", "B2"], default="B")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    if args.memo == "off":
        globals()["MEMO"] = NoMemo()
    rng = np.random.default_rng(args.seed)
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

    H = args.H
    h = TAU * 2.6 ** 1.5 / 96.0
    log_t, log_a, log_e, log_w, hstep = run_ref(particles, H, h)

    def ref_at(t, arr, idx):
        i = min(max(int(round(t / hstep)), 0), len(log_t) - 1)
        return arr[i, idx]

    results = []
    total_hits = total_misses = 0
    for idx, p in enumerate(particles):
        events, hits, misses, cl = run_B(p, H, vec=(args.law == "B2"))
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
        unit, rp, rq, rk, ra_res, detune, W0 = freq_diag(p["a"], p["e"])
        rec = dict(
            idx=idx, a=round(p["a"], 4), e0=round(p["e"], 4),
            q_return=round(q, 3),
            ev_per_orbit=round(ev_per_orbit, 3),
            res_p=rp, res_q=rq, res_k=rk, res_a=round(ra_res, 4),
            detune=round(detune, 6), W_C0=round(W0, 6),
            min_detunit=round(unit, 6),
            excluded_C=[unit < c * math.sqrt(MU_J) for c in (C0 / 2, C0, 2 * C0)],
            rate_ref=round(rate_ref, 8), rate_B=round(rate_B, 8),
            rate_A=round(rate_A, 8),
            relerr_rate_B=round(abs(rate_B - rate_ref) / max(abs(rate_ref), 1e-9), 4),
            relerr_rate_A=round(abs(rate_A - rate_ref) / max(abs(rate_ref), 1e-9), 4),
            signmag_B=round(rate_B / max(abs(rate_ref), 1e-9) * (1 if rate_ref >= 0 else -1), 3),
            wrongsign_B=int((rate_B < 0) != (rate_ref < 0)),
            wrongsign_A=int((rate_A < 0) != (rate_ref < 0)),
            err_w_B=round(float(np.median(errs_w)), 5),
            pump_ref=round(float(e_ref_max / p["e"]), 3),
            pump_B=round(float(e_B_max / p["e"]), 3),
            pump_ratio_B=round(float(e_B_max / max(e_ref_max, 1e-9)), 3),
            err_env_B=round(abs(float(e_B_max / max(e_ref_max, 1e-9)) - 1.0), 3),
            err_env_A=round(abs(1.0 / max(e_ref_max / p["e"], 1e-9) - 1.0), 3),
            err_e_final=round(abs(events[-1][2] - ref_at(events[-1][0], log_e, idx)), 5),
        )
        results.append(rec)

    belt = [r for r in results if r["idx"] < 30]
    out = dict(
        exp="conjunction-unified-kick-r2", H=H, seed=args.seed, memo=args.memo,
        law=args.law,
        n_part=len(particles), C0=round(C0, 4),
        B_events_per_orbit_median=round(float(np.median([r["ev_per_orbit"] for r in results])), 3),
        memo_hits=total_hits, memo_misses=total_misses,
        memo_hit_rate=round(total_hits / max(total_hits + total_misses, 1), 3),
        unfiltered_rate_B=tailstats([r["relerr_rate_B"] for r in belt]),
        unfiltered_rate_A=tailstats([r["relerr_rate_A"] for r in belt]),
        unfiltered_wrongsign_B=sum(r["wrongsign_B"] for r in belt),
        filtered={
            "C_half": {"belt": agg(belt, C0 / 2), "all": agg(results, C0 / 2)},
            "C0": {"belt": agg(belt, C0), "all": agg(results, C0)},
            "C_2x": {"belt": agg(belt, 2 * C0), "all": agg(results, 2 * C0)},
        },
        results=results,
    )
    line = json.dumps(out)
    print(line)
    if args.out:
        with open(args.out, "w") as f:
            f.write(line + "\n")


if __name__ == "__main__":
    main()
