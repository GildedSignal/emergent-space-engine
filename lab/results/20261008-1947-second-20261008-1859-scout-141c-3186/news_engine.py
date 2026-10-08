#!/usr/bin/env python3
"""Both news channels on the plane's real kick stream, growing horizon (second-author run).

Input: kicks_massive.csv (the shipped engine's massive-body kicks, dumped through the public
API; massive streams bit-identical to the full plane with ships). Writes news_engine.json.

News model (engine registers, not assumed): a kick on a massive source is an impulse dv over
its window T; a receiver at distance d that ignores it accumulates retarded-force error
G m |dv| T / d^3 by the source's next kick. Event size s = Gm|dv|T/d^3, arrival t_e + d (c=1).
"""
import json
import sys
import numpy as np

RUN = "."
AU_T = 101_300_000.0          # 1 AU in root units = ticks (c = 1)
L_SYS = 16.0 * AU_T           # mean system separation: fixed surface density 1/L^2
R_MAX = 1024.0 * AU_T
T_STREAM = 4e13               # dumped stream length (ticks)
T_MEAS = 1e12                 # arrival measurement window (the last 1e12 of usable arrivals)
T_WIN = 2.5e11                # accumulator window (T_MEAS/4)
Q_ENGINE = 2.0 ** -112        # player anchor: 2^-74 (vel quantum) * 2^-16 (carry) / 2^22 (step)
MASS = np.array([2.0**-21, 2.0**-18, 2.0**-10, 2.0**-24])  # Cinder, Home, Giant, Moon (G*m, root)
NAMES = ["Cinder", "Home", "Giant", "Moon"]
D0 = 1.0 * AU_T               # shell unit
Q_SWEEP = Q_ENGINE * 10.0 ** np.arange(0, 10)
rng = np.random.default_rng(20261008)


def load(path):
    body, t, ln, dv0, dv1, ve, px, py = [], [], [], [], [], [], [], []
    with open(path) as f:
        for line in f:
            p = line.split(",")
            if p[0] == "K":
                body.append(int(p[1])); t.append(int(p[2])); ln.append(int(p[3]))
                dv0.append(int(p[5])); dv1.append(int(p[6])); ve.append(int(p[7]))
                px.append(float(p[9])); py.append(float(p[10]))
    return (np.array(body), np.array(t, dtype=np.int64), np.array(ln, dtype=np.int64),
            np.array(dv0, dtype=np.float64), np.array(dv1, dtype=np.float64),
            np.array(ve), np.array(px), np.array(py))


def sweep(mode, t, px, py, dvx, dvy, T, s_loc, gm, ang, rad, sys_x, sys_y, phase,
          k_sh_max, n_win, t_lo, cap):
    """Collect every arrival event: (shell, window, size s, vector ax, ay) + per-system counts."""
    sh = np.empty(cap, dtype=np.int32); wn = np.empty(cap, dtype=np.int32)
    sv = np.empty(cap); vx = np.empty(cap); vy = np.empty(cap)
    n = 0
    sys_counts = np.zeros(len(rad), dtype=np.int64)
    CH = 256
    idx = np.arange(len(t))
    for c0 in range(0, len(rad), CH):
        c1 = min(c0 + CH, len(rad))
        sx, sy, ph = sys_x[c0:c1, None], sys_y[c0:c1, None], phase[c0:c1, None]
        th, r = ang[c0:c1, None], rad[c0:c1, None]
        ct, st = np.cos(th), np.sin(th)
        X = sx + ct * px[None, :] - st * py[None, :]
        Y = sy + st * px[None, :] + ct * py[None, :]
        d = np.hypot(X, Y)
        t_arr = t[None, :] + (ph if mode == "staggered" else 0) + d
        sel = (t_arr >= t_lo) & (t_arr < t_lo + T_MEAS)
        cnt = sel.sum(axis=1)
        sys_counts[c0:c1] = cnt
        if not sel.any():
            continue
        dd, tt = d[sel], t_arr[sel]
        jj = np.broadcast_to(idx[None, :], X.shape)[sel]
        s = s_loc[jj] / dd**3
        m = n + len(dd)
        sh[n:m] = np.clip(np.log2(dd / D0).astype(int), 0, k_sh_max - 1)
        wn[n:m] = np.clip(((tt - t_lo) // T_WIN).astype(int), 0, n_win - 1)
        sv[n:m] = s
        ctb = np.broadcast_to(ct, X.shape)[sel]
        stb = np.broadcast_to(st, X.shape)[sel]
        ux, uy = X[sel] / dd, Y[sel] / dd
        dxx = (ctb * dvx[jj] - stb * dvy[jj]) * T[jj]
        dyy = (stb * dvx[jj] + ctb * dvy[jj]) * T[jj]
        pr = dxx * ux + dyy * uy
        fac = gm[jj] / dd**3
        vx[n:m] = fac * (dxx - 3 * pr * ux)
        vy[n:m] = fac * (dyy - 3 * pr * uy)
        n = m
    return sh[:n], wn[:n], sv[:n], vx[:n], vy[:n], sys_counts


def fires_table(sh, wn, sv, vx, vy, k_sh_max, n_win, Qs):
    """Toy semantics: events with s >= Q fire once individually; the rest accumulate per
    (shell, window) and fire floor(sum/Q) (scalar) or floor(|sum_vec|/Q) (vector)."""
    out = {}
    for qi, Q in enumerate(Qs):
        big = sv >= Q
        f = np.zeros((k_sh_max, n_win))
        f += np.bincount(sh[big] * n_win + wn[big], minlength=k_sh_max * n_win).reshape(k_sh_max, n_win)
        small = ~big
        if small.any():
            for chan, val in (("scalar", sv[small]),):
                tot = np.bincount(sh[small] * n_win + wn[small], weights=val,
                                  minlength=k_sh_max * n_win).reshape(k_sh_max, n_win)
                f += np.floor(tot / Q)
            tot_x = np.bincount(sh[small] * n_win + wn[small], weights=vx[small],
                                minlength=k_sh_max * n_win).reshape(k_sh_max, n_win)
            tot_y = np.bincount(sh[small] * n_win + wn[small], weights=vy[small],
                                minlength=k_sh_max * n_win).reshape(k_sh_max, n_win)
            fv = np.floor(np.hypot(tot_x, tot_y) / Q)
            fv += np.bincount(sh[big] * n_win + wn[big], minlength=k_sh_max * n_win).reshape(k_sh_max, n_win)
        else:
            fv = f.copy()
        out[f"Q{qi}"] = dict(scalar=(f.sum(axis=1) / T_MEAS).tolist(),
                             vector=(fv.sum(axis=1) / T_MEAS).tolist())
    return out


def main():
    body, t, ln, dv0, dv1, ve, px, py = load(f"{RUN}/kicks_massive.csv")
    dvx, dvy = dv0 * 2.0**ve, dv1 * 2.0**ve
    gm = MASS[body]
    T = ln.astype(np.float64)
    s_loc = gm * np.hypot(dvx, dvy) * T            # s(d) = s_loc / d^3
    t_lo = T_STREAM - T_MEAS
    in_win = (t >= t_lo - T_MEAS) & (t < T_STREAM)  # source ticks that can land in the window
    t, body, dvx, dvy, px, py, s_loc, T, gm = (a[in_win] for a in (t, body, dvx, dvy, px, py, s_loc, T, gm))

    # --- the receiver's own system at the engine-anchored Q (P6) -----------------------------
    own = {}
    d_own = np.hypot(px, py)
    s_own = s_loc / d_own**3
    for k, nm in enumerate(NAMES):
        m = body == k
        if m.any():
            own[nm] = dict(rate=float(m.sum() / T_MEAS), d_AU=float(np.median(d_own[m]) / AU_T),
                           s_med=float(np.median(s_own[m])), s_max=float(s_own[m].max()),
                           s_over_Q_med=float(np.median(s_own[m]) / Q_ENGINE))
    r_cut_engine = float(np.median(s_loc[body == 1] / Q_ENGINE)) ** (1.0 / 3.0) / AU_T

    # --- systems on the disk at fixed density ------------------------------------------------
    n_sys = int(np.pi * (R_MAX / L_SYS) ** 2)
    ang = rng.uniform(0, 2 * np.pi, n_sys)
    rad = np.sqrt(rng.uniform(0, 1, n_sys)) * R_MAX
    sys_x, sys_y = rad * np.cos(ang), rad * np.sin(ang)
    phase = rng.uniform(0, T_MEAS, n_sys)   # shift within the window: decorrelates, keeps counts
    k_sh_max = int(np.log2((R_MAX + 8 * AU_T) / D0)) + 2
    n_win = int(T_MEAS // T_WIN)
    shell_edges = D0 * 2.0 ** np.arange(k_sh_max + 1)

    res = {"meta": dict(n_sys=n_sys, events_per_system=float(len(t)), L_sys_AU=L_SYS / AU_T,
                        R_max_AU=R_MAX / AU_T, T_meas=T_MEAS, T_win=T_WIN, Q_engine=Q_ENGINE,
                        shells=k_sh_max, windows=n_win, shell_edges_AU=(shell_edges / AU_T).tolist()),
           "own_system": own, "r_cut_engine_AU": r_cut_engine, "Q_sweep": Q_SWEEP.tolist()}

    Rs = L_SYS * 2.0 ** np.arange(0, int(np.log2(R_MAX / L_SYS)) + 1)
    cap = n_sys * len(t) + 1000
    for mode in ("aligned", "staggered"):
        sh, wn, sv, vx, vy, sys_counts = sweep(
            mode, t, px, py, dvx, dvy, T, s_loc, gm, ang, rad, sys_x, sys_y, phase,
            k_sh_max, n_win, t_lo, cap)
        naive = [float(sys_counts[rad <= R].sum() / T_MEAS) for R in Rs]
        expo = float(np.polyfit(np.log2(Rs[1:]), np.log2(naive[1:]), 1)[0])
        acc = fires_table(sh, wn, sv, vx, vy, k_sh_max, n_win, Q_SWEEP)
        inc_s, inc_v = {}, {}
        k_mid = slice(2, k_sh_max - 2)
        for qi in range(len(Q_SWEEP)):
            f = np.array(acc[f"Q{qi}"]["scalar"])
            fv = np.array(acc[f"Q{qi}"]["vector"])
            inc_s[f"Q{qi}"] = [float(x) for x in np.diff(f[k_mid])]
            inc_v[f"Q{qi}"] = [float(x) for x in np.diff(fv[k_mid])]
        res[mode] = dict(R_AU=(Rs / AU_T).tolist(), naive_rate=naive, naive_exponent=expo,
                         accumulator_rates=acc, increments_scalar=inc_s, increments_vector=inc_v,
                         n_events=int(len(sv)),
                         shell_sum_s=[float(x) for x in np.bincount(sh, weights=sv, minlength=k_sh_max)])

    # crossover r_cut(Q): smallest R where naive(R) >= accumulator_total(R)
    cut, ratios = {}, {}
    for qi in range(len(Q_SWEEP)):
        accv = np.array(res["aligned"]["accumulator_rates"][f"Q{qi}"]["scalar"])
        acc_R = np.array([accv[shell_edges[:-1] <= R * AU_T].sum() for R in Rs])
        nv = np.array(res["aligned"]["naive_rate"])
        c = next((float(R / AU_T) for R, a, b in zip(Rs, nv, acc_R) if a >= b), None)
        cut[f"Q{qi}"] = c
        ratios[f"Q{qi}"] = float(nv[-1] / acc_R[-1]) if acc_R[-1] > 0 else None
    Qs = np.array(Q_SWEEP)
    cuts = np.array([cut[f"Q{qi}"] for qi in range(len(Qs))], dtype=float)
    m = np.isfinite(cuts) & (cuts > 0)
    slope = float(np.polyfit(np.log(Qs[m]), np.log(cuts[m]), 1)[0]) if m.sum() >= 3 else None
    res["crossover"] = dict(r_cut_AU=cut, ratio_at_Rmax=ratios, slope_logr_vs_logQ=slope)


    with open(f"{RUN}/news_engine.json", "w") as f:
        json.dump(res, f, indent=1)
    print("meta:", json.dumps(res["meta"]))
    print("own:", json.dumps(res["own_system"], indent=1))
    print("r_cut(engine Q):", r_cut_engine, "AU")
    print("naive exponent (aligned):", res["aligned"]["naive_exponent"])
    for qi in (0, 3, 6, 9):
        print(f"Q{qi} scalar increments:", [f"{x:.3g}" for x in res["aligned"]["increments_scalar"][f"Q{qi}"]])
        print(f"Q{qi} vector increments:", [f"{x:.3g}" for x in res["aligned"]["increments_vector"][f"Q{qi}"]])
    print("crossover:", json.dumps(res["crossover"]))
    return 0


if __name__ == "__main__" and not (len(sys.argv) > 1 and sys.argv[1] == "--selftest"):
    sys.exit(main())


def selftest():
    """Unit tests of the channel semantics (run by the checker): toy rules are s>=Q fires
    once individually; sub-quantum accumulate per (shell, window) and fire floor(sum/Q)."""
    import numpy as np
    Q = 1e-30
    sh = np.zeros(4000, dtype=np.int32); wn = np.tile(np.arange(4), 1000)
    sv = np.full(4000, 10 * Q)
    out = fires_table(sh, wn, sv, sv * 0, sv * 0, 2, 4, np.array([Q]))
    assert abs(out["Q0"]["scalar"][0] - 4000 / T_MEAS) < 1e-20, "big events fire once each"
    sv2 = np.full(4000, 0.00025 * Q)   # 1000/window -> 0.25*Q per window -> no fire
    out2 = fires_table(sh, wn, sv2, sv2 * 0, sv2 * 0, 2, 4, np.array([Q]))
    assert out2["Q0"]["scalar"][0] == 0.0, "sub-quantum spread over windows fires nothing"
    sh3 = np.zeros(4000, dtype=np.int32); wn3 = np.zeros(4000, dtype=np.int32)
    out3 = fires_table(sh3, wn3, np.full(4000, 0.001 * Q), sv2 * 0, sv2 * 0, 2, 4, np.array([Q]))
    assert abs(out3["Q0"]["scalar"][0] - 4 / T_MEAS) < 1e-20, "one window: floor(4*0.001*4000... =4)"
    print("selftest OK")
    return 0


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "--selftest":
    sys.exit(selftest())
