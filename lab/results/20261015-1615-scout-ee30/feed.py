#!/usr/bin/env python3
"""feed.py — the view's birth/death feed priced on a float replica of the ladder scene.

Birth law: scenario.rs:333-344 (belt a in [2,3) AU, e Rayleigh 0.07 capped 0.4,
uniform periapsis/phase, prograde; periapsis >= 1.2 AU by construction a(1-e)).
Map criterion: page.html drawMap — square window in the star's frame, centred on the
observer's CURRENT position, testing each body's RETARDED offset, half-width W.
Fitted W from fitLog ~ 7x the nearest local's distance (3.5 ls here);
belt zoom W = 750 ls (half-window 1.5 AU: the belt in-window from an observer at 1 AU).
Observer: circular at 1 AU about a solar star; burns add a radial ramp.
Units: AU, seconds. c = 1 AU / 499.005 s. Output: JSON on argv[1].
"""
import numpy as np, json, time, sys

AU_LS = 499.005
GM = 4 * np.pi**2 / 3.156e7**2   # AU^3/s^2
C = 1.0 / AU_LS                  # AU/s
FRAME = 100.0 / 60.0             # game-seconds per frame at rtf 100, 60 fps

def validate_solver(iters=200000):
    """Instrument self-check: residuals of the solver on a random (M, e) grid."""
    rng = np.random.default_rng(0)
    M0 = (rng.random(iters) * 2 - 1) * np.pi
    e = rng.random(iters) * 0.4
    E = M0.copy()
    for _ in range(8):
        sE, cE = np.sin(E), np.cos(E)
        d = (E - e * sE - M0) / (1.0 - e * cE)
        d = np.clip(d, -0.6, 0.6)
        E = np.clip(E - d, M0 - e - 1e-9, M0 + e + 1e-9)
    return float(np.max(np.abs(E - e * np.sin(E) - M0)))
def make_belt(N, seed):
    rng = np.random.default_rng(seed)
    a = 2.0 + rng.random(N)
    e = np.minimum(rng.rayleigh(0.07, N), 0.4)
    om = rng.random(N) * 2 * np.pi
    M0 = rng.random(N) * 2 * np.pi
    return a, e, om, M0

def kepler_xy(a, e, om, c_om, s_om, g, M0, t):
    n = np.sqrt(GM) * a ** -1.5
    M = (M0 + n * t) % (2 * np.pi) - np.pi       # wrap: E lives in [M-e, M+e]
    E = M.copy()
    for _ in range(8):
        sE, cE = np.sin(E), np.cos(E)
        d = (E - e * sE - M) / (1.0 - e * cE)    # f monotone: bracketed damped Newton cannot diverge
        d = np.clip(d, -0.6, 0.6)
        E = np.clip(E - d, M - e - 1e-9, M + e + 1e-9)
    sE, cE = np.sin(E), np.cos(E)
    den = 1.0 - e * cE
    cn = (cE - e) / den
    sn = g * sE / den
    r = a * den
    return r * (c_om * cn - s_om * sn), r * (s_om * cn + c_om * sn)

def observer(t, burn=None):
    n = np.sqrt(GM)
    th = n * t
    x, y = np.cos(th), np.sin(th)
    if burn is not None:
        t0, T, bmax = burn
        dt = np.clip(t - t0, 0.0, T)
        excursion = 0.5 * bmax * C * dt**2 / T      # integral of beta(t)*c, radial
        x, y = x * (1.0 + excursion), y * (1.0 + excursion)
    return x, y

def membership(st, t, W, burn=None):
    a, e, om, M0, g, c_om, s_om = st
    ox, oy = observer(t, burn)
    x, y = kepler_xy(a, e, om, c_om, s_om, g, M0, t)
    d = np.hypot(x - ox, y - oy)
    te = t - d / C                                 # one fixed-point pass (2nd-order error ~1e-8 AU)
    x, y = kepler_xy(a, e, om, c_om, s_om, g, M0, te)
    return (np.abs(x - ox) < W) & (np.abs(y - oy) < W), float(np.hypot(x - ox, y - oy).min())

def run_arm(name, N, W_of_t, ts, seed=4, heldout_seed=None, burn=None):
    t0 = time.time()
    seeds = [seed] if heldout_seed is None else [seed, heldout_seed]
    out = {"arm": name, "N": N, "seeds": {}}
    for sd in seeds:
        a, e, om, M0 = make_belt(N, sd)
        st = (a, e, om, M0, np.sqrt(1 - e * e), np.cos(om), np.sin(om))
        prev, gap0 = membership(st, ts[0], W_of_t(0), burn)
        inside0 = int(prev.sum())
        ev_per_step, min_gap = [], gap0
        for j in range(1, len(ts)):
            cur, gp = membership(st, ts[j], W_of_t(j), burn)
            ev_per_step.append(int((cur ^ prev).sum()))
            prev, min_gap = cur, min(min_gap, gp)
        ev = np.array(ev_per_step, dtype=float)
        rate = ev.sum() / (ts[-1] - ts[0])
        per_frame = ev / np.maximum(np.diff(ts), 1e-9) * FRAME
        out["seeds"][str(sd)] = {
            "inside_at_start": inside0,
            "events_total": int(ev.sum()),
            "horizon_s": float(ts[-1] - ts[0]),
            "events_per_game_s": float(rate),
            "per_body_per_game_s": float(rate / N),
            "worst_frame_events": float(per_frame.max()) if len(per_frame) else 0.0,
            "p99_frame_events": float(np.percentile(per_frame, 99)) if len(per_frame) else 0.0,
            "min_body_distance_AU": float(min_gap),
        }
    out["wall_s"] = round(time.time() - t0, 1)
    return out

def main():
    R = {"constants": {"frame_game_s": FRAME, "r_event_entry_us": 3.5, "r_event_exit_us": 0.5,
                       "scan_us_per_body": 3.5, "scan_period_game_s": 400.0}}

    # fitted zoom (W = 3.5 ls): the group-envelope arm
    ts = np.linspace(0.0, 5e6, 260)
    R["coast_fitted"] = run_arm("coast_fitted", 100_000, lambda j: 3.5 / AU_LS, ts)

    # belt zoom steady coast, two seeds (one held out), + N-linearity arm
    R["coast_belt_1e5"] = run_arm("coast_belt", 100_000, lambda j: 750.0 / AU_LS, ts, heldout_seed=7)
    ts2 = np.linspace(0.0, 2e6, 130)
    R["coast_belt_2e5"] = run_arm("coast_belt", 200_000, lambda j: 750.0 / AU_LS, ts2)

    # sensitivity control: straddling window, edge cutting the belt
    R["control_straddle"] = run_arm("ctl", 100_000, lambda j: 400.0 / AU_LS, ts2)

    # burn: beta to 0.05 radial over 600 s, both zooms
    tsb = np.arange(0.0, 900.0, FRAME)
    R["burn_beltzoom"] = run_arm("burn", 100_000, lambda j: 750.0 / AU_LS, tsb, burn=(100.0, 600.0, 0.05))
    R["burn_fitted"] = run_arm("burn", 100_000, lambda j: 3.5 / AU_LS, tsb, burn=(100.0, 600.0, 0.05))

    # zoom: W 3.5 -> 750 ls over 90 frames (~1.5 dex/s, the wheel's pace)
    nfr = 90
    Ws = 3.5 * 10 ** (np.linspace(0, np.log10(750 / 3.5), nfr))
    tsz = np.arange(0, nfr) * FRAME
    R["zoom_1e5"] = run_arm("zoom", 100_000, lambda j: Ws[j] / AU_LS, tsz)
    R["zoom_2e5"] = run_arm("zoom", 200_000, lambda j: Ws[j] / AU_LS, tsz)

    print(json.dumps(R, indent=1))
    with open(sys.argv[1] if len(sys.argv) > 1 else "feed_out.json", "w") as f:
        json.dump(R, f, indent=1)

if __name__ == "__main__":
    main()
