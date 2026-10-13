#!/usr/bin/env python3
"""The news scar: what a source's rebind leaves in a consumer, permanently.

Scene: a test moon on a circular orbit (r=1, v=1, G=M=1, P=2*pi) about a source.
At t_k the source's motion changes: an impulsive dV (a kick/rebind) or a
sustained burn (a player thrust). The moon's force is read three ways:

  inst : the source's TRUE state at t   (today's plane; the 1PN near-zone oracle's
                                         instantaneous gauge)
  news : the newest source TUBE VERSION whose emission the moon's past light cone
         has met (law.md:33); versions are free-fall (straight-line) tubes keyed
         at their emission event; the switch is located by bisection + linear
         interpolation inside the bracketing step (a237 located it to one step)
  ret  : pull toward the source's retarded position (Laplace control; must fail)

Units are scaled so beta_c = v_c/c is the only knob: c = 1/beta_c, light window
T = r/c = beta_c. Cloud float64, orders of magnitude. Writes scar.json.
"""
import json, math, statistics

P = 2.0 * math.pi
DV = 0.01  # impulse size (linear regime)

def accel(xm, xs):
    dx0, dx1 = xm[0] - xs[0], xm[1] - xs[1]
    r = math.hypot(dx0, dx1)
    return (-dx0 / r**3, -dx1 / r**3)

def true_at(t, t_k, kick, burn):
    """True source worldline: straight until t_k; kick applied at t_k; optional
    burn a along +x for duration D from t_k."""
    if t < t_k:
        return (0.0, 0.0), (0.0, 0.0)
    if burn is None:
        kv = kick if kick is not None else (0.0, 0.0)
        x, v = (kv[0] * (t - t_k), kv[1] * (t - t_k)), (kv[0], kv[1])
    else:
        a, D = burn
        tau = min(t - t_k, D)
        x, v = (0.5 * a * tau * tau, 0.0), (a * tau, 0.0)
        if tau >= D:
            x = (0.5 * a * D * D + a * D * (t - t_k - D), 0.0)
    return x, v

def tube_eval(ver, t):
    (t0, x0, y0, vx, vy) = ver
    dt = t - t0
    return (x0 + vx * dt, y0 + vy * dt)

def cone_first(xa, xb, ta, tb, x_emit, t_emit, c):
    """First t in [ta, tb] with c(t-t_emit) >= |x_m(t) - x_emit| (linear x_m)."""
    def h(t):
        f = (t - ta) / (tb - ta) if tb > ta else 0.0
        xm = (xa[0] + f * (xb[0] - xa[0]), xa[1] + f * (xb[1] - xa[1]))
        return c * (t - t_emit) - math.hypot(xm[0] - x_emit[0], xm[1] - x_emit[1])
    if h(tb) < 0.0:
        return None
    if h(ta) >= 0.0:
        return ta
    lo, hi = ta, tb
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if h(mid) < 0.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)

def retarded_x(t, xm, c, t_k, kick, burn):
    t_ret = t - math.hypot(*xm) / c
    for _ in range(10):
        xs, _ = true_at(t_ret, t_k, kick, burn)
        t_ret = t - math.hypot(xm[0] - xs[0], xm[1] - xs[1]) / c
    xs, _ = true_at(t_ret, t_k, kick, burn)
    return xs

def kepler_E(xm, vm, t, t_k, kick, burn):
    xs, vs = true_at(t, t_k, kick, burn)
    d = (xm[0] - xs[0], xm[1] - xs[1])
    w = (vm[0] - vs[0], vm[1] - vs[1])
    return 0.5 * (w[0] * w[0] + w[1] * w[1]) - 1.0 / math.hypot(*d)

def integrate(law, beta_c, phase0, t_end, dtA, dtB, t_k=2.0, kick=None,
              burn=None, epoch=None, fine_until=None, lag_samples=None):
    """Velocity-Verlet for the moon under law in {inst, news, ret}.
    Returns (xm, vm, switch_t, lags)."""
    c = 1.0 / beta_c
    T = beta_c
    xm = (math.cos(phase0), math.sin(phase0))
    vm = (-math.sin(phase0), math.cos(phase0))
    t = 0.0
    versions = [(0.0, 0.0, 0.0, 0.0, 0.0)]  # (t_e, x, y, vx, vy)
    if kick is not None:
        versions.append((t_k, 0.0, 0.0, kick[0], kick[1]))
    ver_i = 0
    next_rebase = t_k
    switch_t = None
    lags = []
    fine_until = fine_until if fine_until is not None else (t_k + T)
    def force(t, xm):
        if law == "inst":
            xs, _ = true_at(t, t_k, kick, burn)
        elif law == "ret":
            xs = retarded_x(t, xm, c, t_k, kick, burn)
        else:
            xs = tube_eval(versions[ver_i], t)
        return accel(xm, xs)
    def step(t, xm, vm, dt):
        a1 = force(t, xm)
        xm2 = (xm[0] + vm[0] * dt + 0.5 * a1[0] * dt * dt,
               xm[1] + vm[1] * dt + 0.5 * a1[1] * dt * dt)
        a2 = force(t + dt, xm2)
        vm2 = (vm[0] + 0.5 * (a1[0] + a2[0]) * dt,
               vm[1] + 0.5 * (a1[1] + a2[1]) * dt)
        return xm2, vm2
    guard = 0
    while t < t_end - 1e-12:
        guard += 1
        if guard > 30_000_000:
            raise RuntimeError("runaway")
        dt = dtA if (t_k - 2 * dtA) <= t <= (fine_until + 2 * dtA) else dtB
        if t + dt > t_end:
            dt = t_end - t
        if law == "news":
            if burn is not None and epoch is not None and t >= next_rebase - 1e-15:
                x, v = true_at(next_rebase, t_k, kick, burn)
                versions.append((next_rebase, x[0], x[1], v[0], v[1]))
                next_rebase += epoch
            if ver_i + 1 < len(versions):
                t_e = versions[ver_i + 1][0]
                x_e = (versions[ver_i + 1][1], versions[ver_i + 1][2])
                arr = cone_first(xm, xm, t, t, x_e, t_e, c)
                if arr is None:
                    xm_end = (xm[0] + vm[0] * dt, xm[1] + vm[1] * dt)
                    arr = cone_first(xm, xm_end, t, t + dt, x_e, t_e, c)
                if arr is not None:
                    if arr > t + 1e-14:
                        xm, vm = step(t, xm, vm, arr - t)
                        t = arr
                    ver_i += 1
                    switch_t = t
                    continue
            if lag_samples is not None and burn is not None:
                if guard % max(1, int(round((P / 40) / dt))) == 0 and t > t_k:
                    xs_t, _ = true_at(t, t_k, kick, burn)
                    xs_v = tube_eval(versions[ver_i], t)
                    lags.append((t, versions[ver_i][0],
                                 math.hypot(xs_t[0] - xs_v[0], xs_t[1] - xs_v[1])))
        xm, vm = step(t, xm, vm, dt)
        t += dt
    return xm, vm, switch_t, lags

def impulse_case(beta_c, phase0, kick_dir, dt_div=60.0, t_end_extra=2.0 * P):
    t_k = 2.0
    kick = (DV * math.cos(kick_dir), DV * math.sin(kick_dir))
    T = beta_c
    dtA = min(T / dt_div, P / 3000.0)
    dtB = P / 600.0
    t_end = t_k + T + t_end_extra
    out = {}
    for law in ("inst", "news", "ret"):
        xm, vm, sw, _ = integrate(law, beta_c, phase0, t_end, dtA, dtB, t_k=t_k,
                                  kick=kick)
        out[law] = (xm, vm, sw)
    # scar at the switch (transient accrued during the window only)
    t_sw = t_k + T
    xm_i, vm_i, _, _ = integrate("inst", beta_c, phase0, t_sw, dtA, dtB, t_k=t_k,
                                 kick=kick)
    xm_n, vm_n, _, _ = integrate("news", beta_c, phase0, t_sw, dtA, dtB, t_k=t_k,
                                 kick=kick)
    scar_switch = math.hypot(vm_i[0] - vm_n[0], vm_i[1] - vm_n[1])
    # twins: no kick at all, news vs inst must agree (mechanism identity)
    xa, va, _, _ = integrate("inst", beta_c, phase0, t_end, dtA, dtB, t_k=t_k)
    xb, vb, _, _ = integrate("news", beta_c, phase0, t_end, dtA, dtB, t_k=t_k)
    twin = math.hypot(xa[0] - xb[0], xa[1] - xb[1])
    dv_end = lambda a, b: math.hypot(a[1][0] - b[1][0], a[1][1] - b[1][1])
    E = {}
    for law in ("inst", "news", "ret"):
        xm, vm = out[law][0], out[law][1]
        E[law] = kepler_E(xm, vm, t_end, t_k, kick, None)
    return {"beta_c": beta_c, "phase0": phase0, "kick_dir": kick_dir,
            "scar_news": dv_end(out["news"], out["inst"]),
            "scar_E_news": abs(E["news"] - E["inst"]),
            "scar_E_ret": abs(E["ret"] - E["inst"]),
            "scar_ret": dv_end(out["ret"], out["inst"]),
            "scar_at_switch": scar_switch,
            "pred": DV * beta_c * beta_c / 2.0,
            "switch_late": (out["news"][2] - t_sw) if out["news"][2] else None,
            "twin_no_kick": twin}

def burn_case(beta_c, cad_div):
    t_k = 2.0
    T = beta_c
    epoch = T / cad_div
    dtA = min(epoch / 20.0, P / 3000.0)
    dtB = P / 600.0
    a_b, D = 0.05, 2.0 * P
    t_end = t_k + D + 2.0 * P
    res = {}
    for law in ("inst", "news"):
        xm, vm, _, lags = integrate(law, beta_c, 0.0, t_end, dtA, dtB, t_k=t_k,
                                    burn=(a_b, D), epoch=epoch,
                                    fine_until=t_k + D + T,
                                    lag_samples=True)
        res[law] = (xm, vm, lags)
    at_age = [l for (t, te, l) in res["news"][2]
              if t > t_k + 3 * T and 0.9 * T <= (t - te) <= 1.1 * T]
    E = {law: kepler_E(res[law][0], res[law][1], t_end, t_k, None, (a_b, D))
         for law in ("inst", "news")}
    dv_end = math.hypot(res["news"][1][0] - res["inst"][1][0],
                        res["news"][1][1] - res["inst"][1][1])
    return {"beta_c": beta_c, "cad_div": cad_div, "epoch": epoch,
            "lag_at_ageT": statistics.median(at_age) if at_age else None,
            "n_lag": len(at_age), "plateau_pred": 0.5 * a_b * T * T,
            "moon_dv_end": dv_end, "scar_E": abs(E["news"] - E["inst"])}

def main():
    out = {"impulse": [], "burn": [], "dt_conv": [], "fit": {}}
    print("== P1/P2 impulsive rebind: scar = permanent moon delta-v (news vs inst), |dv|=0.01")
    print(f"{'beta_c':>7} {'ph':>5} {'dE/dv':>11} {'at_switch':>11} {'b^2/2':>9} {'ret/dv':>9} {'sw_late':>10}")
    for beta_c in (0.003, 0.01, 0.03, 0.1, 0.2, 0.3):
        for phase0, kdir in ((0.0, 0.0), (math.pi / 3, math.pi / 2),
                             (2 * math.pi / 3, math.pi), (math.pi, -math.pi / 3)):
            r = impulse_case(beta_c, phase0, kdir)
            out["impulse"].append(r)
            sw = r["switch_late"]
            print(f"{beta_c:7.3f} {phase0:5.2f} {r['scar_E_news'] / DV:11.3e} "
                  f"{r['scar_at_switch'] / DV:11.3e} {r['pred'] / DV:9.2e} "
                  f"{r['scar_ret'] / DV:9.1e} {sw:+10.2e}" if sw is not None else "sw=None")
    means = {b: statistics.mean([r["scar_E_news"] for r in out["impulse"]
                                 if r["beta_c"] == b])
             for b in (0.003, 0.01, 0.03, 0.1, 0.2, 0.3)}
    expo = math.log(means[0.3] / means[0.003]) / math.log(0.3 / 0.003)
    out["fit"] = {"exponent": expo,
                  "means": {str(k): v for k, v in means.items()},
                  "k_bar_0.3": means[0.3] / DV / (0.3 ** 2 / 2),
                  "twin_max": max(r["twin_no_kick"] for r in out["impulse"])}
    print(f"\nfitted exponent scar ~ beta_c^x : x = {expo:.3f}   "
          f"k_bar(0.3) = {out['fit']['k_bar_0.3']:.2f}   twin_max = {out['fit']['twin_max']:.2e}")
    for b, m in means.items():
        print(f"  beta_c={b:6.3f}  mean scar/|dv| = {m / DV:11.4e}")
    print("\n== P4 sustained burn a=0.05 (D=2P): news readout lag plateau (vs pred 0.5aT^2)")
    print(f"{'beta_c':>7} {'cad':>4} {'epoch':>9} {'lag@ageT':>9} {'n':>4} {'pred':>9} {'dE_end':>11} {'dv_end':>10}")
    for beta_c in (0.05, 0.1, 0.3):
        for cad in (8, 32):
            r = burn_case(beta_c, cad)
            out["burn"].append(r)
            print(f"{beta_c:7.3f} {cad:4d} {r['epoch']:9.4f} "
                  f"{r['lag_at_ageT']:9.4f} {r['n_lag']:4d} "
                  f"{r['plateau_pred']:9.4f} {r['scar_E']:11.3e} {r['moon_dv_end']:10.3e}")
    print("\n== P5 dt convergence (beta=0.1, phase 0): scar at dt_div 60 vs 120")
    s60 = impulse_case(0.1, 0.0, 0.0, dt_div=60.0)["scar_news"]
    s120 = impulse_case(0.1, 0.0, 0.0, dt_div=120.0)["scar_news"]
    out["dt_conv"] = [{"dt_div": 60, "scar": s60}, {"dt_div": 120, "scar": s120}]
    print(f"  scar(T/60)={s60:.6e}  scar(T/120)={s120:.6e}  rel diff {abs(s60 - s120) / s60:.3f}")
    with open("scar.json", "w") as f:
        json.dump(out, f, indent=1)
    print("\nwrote scar.json")

if __name__ == "__main__":
    main()
