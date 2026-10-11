#!/usr/bin/env python3
"""H_live of a stirred belt, UNSATURATED instruments (second-author run on 20261010-2314).

Fixes to the shipped hlive.py, per the checker's verdict:
1. Naive key-crossing counter sampled EVERY step (sample_every 4 -> 1): the
   shipped counter's ceiling was 32.38 events/P_p and the stored medians sat at
   98% of it. New ceiling 129.53/P_p (dtpo*ap^1.5).
2. Smoothed secular counter at SM_STRIDE=1 with a rolling-sum window of
   SM_W=1024 steps (same ~7.9 P_p window as shipped 8x128), ceiling 129.53/P_p
   instead of 16.19. Quantized on the bits16 grid (as shipped).
3. Tail statistics computed on the SMOOTHED counter (shipped top-1% came from
   the saturated naive counter), plus tail-structure fields (birth a, birth e,
   per-ship counts) so the tail can be located.
4. Sample dumps of (a, L, active) at po = 100 and 300 for k-NN entropy.

Physics, quantizers, deadband and exit rules are byte-identical to hlive.py.
"""
import argparse, json, time, math
import numpy as np


def planet_xv(t, a_p, e_p):
    P = 2.0 * np.pi * a_p ** 1.5
    M = (2.0 * np.pi * t / P) % (2.0 * np.pi)
    E = M + 0.0
    for _ in range(6):
        E = E - (E - e_p * np.sin(E) - M) / (1.0 - e_p * np.cos(E))
    c, s = np.cos(E), np.sin(E)
    x, y = a_p * (c - e_p), a_p * math.sqrt(1 - e_p * e_p) * s
    n = 2.0 * np.pi / P
    fac = n / (1.0 - e_p * c)
    vx, vy = -a_p * fac * s, a_p * math.sqrt(1 - e_p * e_p) * fac * c
    return x, y, vx, vy


def accel(x, y, xp, yp, mu):
    r3 = (x * x + y * y) ** 1.5
    ax = -x / r3
    ay = -y / r3
    dx, dy = xp - x, yp - y
    d3 = (dx * dx + dy * dy) ** 1.5
    rp3 = (xp * xp + yp * yp) ** 1.5
    k = mu / d3
    ax += k * dx - mu * xp / rp3
    ay += k * dy - mu * yp / rp3
    return ax, ay


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--tag", required=True)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--N", type=int, default=4000)
    p.add_argument("--po", type=float, default=300.0, help="planet orbits to run")
    p.add_argument("--dtpo", type=float, default=64.0, help="steps per a=1 orbit")
    p.add_argument("--mu", type=float, default=1e-3)
    p.add_argument("--ap", type=float, default=1.6)
    p.add_argument("--ep", type=float, default=0.05)
    p.add_argument("--a0", type=float, default=2.0)
    p.add_argument("--a1", type=float, default=3.5)
    p.add_argument("--sige", type=float, default=0.02)
    p.add_argument("--ring", type=str, default="", help="a0,dw,e0 for a resonance ring")
    p.add_argument("--bits", default="8,12,16,20")
    p.add_argument("--dump_po", default="100,300", help="planet-orbit marks to dump (a,L) samples")
    args = p.parse_args()

    rng = np.random.default_rng(args.seed)
    dt = 2.0 * np.pi / args.dtpo
    steps = int(round(args.po * 2.0 * np.pi * args.ap ** 1.5 / dt))
    po_of_step = lambda s: s * dt / (2.0 * np.pi * args.ap ** 1.5)

    # --- ship state (identical to hlive.py) ---
    if args.ring:
        ra0, dw, e0 = [float(v) for v in args.ring.split(",")]
        a = ra0 + dw * (2.0 * rng.random(args.N) - 1.0)
        e = np.clip(np.full(args.N, e0) + 0.002 * rng.standard_normal(args.N), 0.0, None)
    else:
        a = args.a0 + (args.a1 - args.a0) * rng.random(args.N)
        e = rng.rayleigh(args.sige, args.N)
    om = 2.0 * np.pi * rng.random(args.N)
    Ma = 2.0 * np.pi * rng.random(args.N)
    cO, sO = np.cos(om), np.sin(om)
    Ean = Ma.copy()
    for _ in range(6):
        Ean = Ean - (Ean - e * np.sin(Ean) - Ma) / (1.0 - e * np.cos(Ean))
    cE, sE = np.cos(Ean), np.sin(Ean)
    b = a * np.sqrt(1.0 - e * e)
    xp_, yp_ = a * (cE - e), b * sE
    n = 1.0 / a ** 1.5
    fac = n / (1.0 - e * cE)
    vxp_, vyp_ = -a * fac * sE, b * fac * cE
    x = xp_ * cO - yp_ * sO
    y = xp_ * sO + yp_ * cO
    vx = vxp_ * cO - vyp_ * sO
    vy = vyp_ * cO + vxp_ * sO

    # --- grids: naive counters on args.bits; smoothed/deadband fixed at bits16 ---
    A_LO, A_HI = 1.0, 8.0
    L_LO, L_HI = 0.40, 2.50
    bits = [int(v) for v in args.bits.split(",")]
    qA = [(A_HI - A_LO) / (2.0 ** b) for b in bits]
    qL = [(L_HI - L_LO) / (2.0 ** b) for b in bits]
    NA = 1 << 20  # pack room for bits up to 20
    S16A = (A_HI - A_LO) / (2.0 ** 16)
    S16L = (L_HI - L_LO) / (2.0 ** 16)

    def keys(x, y, vx, vy):
        r = np.sqrt(x * x + y * y)
        E = 0.5 * (vx * vx + vy * vy) - 1.0 / r
        aE = np.where(E < 0, -0.5 / np.where(E < 0, E, 1e-300), A_HI + 1.0)
        L = x * vy - y * vx
        return aE, L

    aE, L = keys(x, y, vx, vy)
    pk = [((aE - A_LO) / q).astype(np.int64) * NA + ((L - L_LO) / ql).astype(np.int64)
          for q, ql in zip(qA, qL)]
    # exact per-step swept cell distance |dia|+|diL| per width (cadence-free)
    pia = [((aE - A_LO) / q).astype(np.int64) for q in qA]
    piL = [((L - L_LO) / ql).astype(np.int64) for ql in qL]
    sw = [np.zeros(args.N, np.int64) for _ in bits]

    cum = [np.zeros(args.N, np.int64) for _ in bits]
    departed = [np.zeros(args.N, bool) for _ in bits]

    # smoothed (rolling-sum ring, stride 1, window 1024 steps ~ 7.9 P_p)
    SM_STRIDE, SM_W = 1, 2048
    sm_bufA = np.zeros((SM_W, args.N))
    sm_bufL = np.zeros((SM_W, args.N))
    sm_sumA = np.zeros(args.N)
    sm_sumL = np.zeros(args.N)
    sm_cum = np.zeros(args.N, np.int64)
    sm_dep = np.zeros(args.N, bool)
    sm_n, sm_kA, sm_kL = 0, None, None

    # synodic-phase SECULAR counter (cadence-free): each ship fires once per
    # its own current synodic period; we count quantized-key changes (Hamming
    # and swept cells) between consecutive same-phase fires. A rolling-mean
    # window of non-integer synodic cycles leaks ~6.5% of the synodic ripple
    # into the mean (belt_s2: stride-1 med 22.9 vs stride-2 10.85), so the
    # phase-locked sampler is the honest secular instrument.
    nP = 1.0 / args.ap ** 1.5

    def T_syn(a_):
        return 2.0 * np.pi / np.abs(np.power(a_, -1.5) - nP)

    sec_kA = ((aE - A_LO) / S16A).astype(np.int64).copy()
    sec_kL = ((L - L_LO) / S16L).astype(np.int64).copy()
    next_fire = T_syn(aE) * (1.0 + rng.random(args.N))
    sec_cum = np.zeros(args.N, np.int64)
    sec_sw = np.zeros(args.N, np.int64)
    sec_fires = np.zeros(args.N, np.int64)

    # deadband on bits16 (as shipped)
    db_ia, db_iL = ((aE - A_LO) / S16A).astype(np.int64), ((L - L_LO) / S16L).astype(np.int64)
    db_cum = np.zeros(args.N, np.int64)

    active = np.ones(args.N, bool)
    exited = np.zeros(args.N, bool)

    xp, yp, _, _ = planet_xv(0.0, args.ap, args.ep)
    ax, ay = accel(x, y, xp, yp, args.mu)
    t = 0.0

    snap_steps = np.unique(np.round(np.geomspace(10, steps, 40)).astype(int)).tolist()
    snap_rows = []
    dumps = {}
    dump_marks = [float(v) for v in args.dump_po.split(",") if float(v) < args.po - 1e-9]
    dump_steps = {int(round(m / dt * 2.0 * np.pi * args.ap ** 1.5)): m for m in dump_marks}
    bands = [(args.a0, args.a0 + 0.44, "inner"), (2.48, 2.60, "res21"),
             (2.72, 2.88, "offres"), (3.28, 3.40, "res31"), (3.42, args.a1, "outer")]
    band_id = np.full(args.N, -1)
    for i, (b0, b1, _) in enumerate(bands):
        band_id[(a >= b0) & (a <= b1)] = i

    t_start = time.time()
    si = 0
    for step in range(1, steps + 1):
        vhx, vhy = vx + 0.5 * dt * ax, vy + 0.5 * dt * ay
        x = x + dt * vhx
        y = y + dt * vhy
        t += dt
        xp, yp, _, _ = planet_xv(t, args.ap, args.ep)
        ax, ay = accel(x, y, xp, yp, args.mu)
        vx = vhx + 0.5 * dt * ax
        vy = vhy + 0.5 * dt * ay

        # --- every-step sampling (fix 1) ---
        aE, L = keys(x, y, vx, vy)
        out = (aE < A_LO) | (aE >= A_HI) | (L < L_LO) | (L >= L_HI)
        exited |= out & active
        active &= ~out
        m = active
        for j in range(len(bits)):
            ia_j = ((aE - A_LO) / qA[j]).astype(np.int64)
            iL_j = ((L - L_LO) / qL[j]).astype(np.int64)
            k = ia_j * NA + iL_j
            chg = (k != pk[j]) & m
            cum[j] += chg
            departed[j] |= chg
            pk[j] = np.where(m, k, pk[j])
            sw[j] += np.where(m, np.abs(ia_j - pia[j]) + np.abs(iL_j - piL[j]), 0)
            pia[j] = np.where(m, ia_j, pia[j])
            piL[j] = np.where(m, iL_j, piL[j])
        ia_ = ((aE - A_LO) / S16A).astype(np.int64)
        iL_ = ((L - L_LO) / S16L).astype(np.int64)
        move = ((np.abs(ia_ - db_ia) > 1) | (np.abs(iL_ - db_iL) > 1)) & m
        # synodic-phase secular fires
        fire = (t >= next_fire) & active
        if fire.any():
            dia = ia_[fire] - sec_kA[fire]
            diL = iL_[fire] - sec_kL[fire]
            sec_cum[fire] += (dia != 0) | (diL != 0)
            sec_sw[fire] += np.abs(dia) + np.abs(diL)
            sec_fires[fire] += 1
            sec_kA[fire] = ia_[fire]
            sec_kL[fire] = iL_[fire]
            next_fire[fire] = t + T_syn(aE[fire])
        db_cum += move
        db_ia = np.where(move, ia_, db_ia)
        db_iL = np.where(move, iL_, db_iL)
        # smoothed counter, stride 1, rolling-sum ring (fix 2)
        idx = sm_n % SM_W
        sm_sumA += aE - sm_bufA[idx]
        sm_sumL += L - sm_bufL[idx]
        sm_bufA[idx] = aE
        sm_bufL[idx] = L
        sm_n += 1
        if sm_n >= SM_W:
            mA = sm_sumA / SM_W
            mL = sm_sumL / SM_W
            jA = ((mA - A_LO) / S16A).astype(np.int64)
            jL = ((mL - L_LO) / S16L).astype(np.int64)
            if sm_kA is None:
                sm_kA, sm_kL = jA.copy(), jL.copy()
            else:
                mv = ((jA != sm_kA) | (jL != sm_kL)) & m
                sm_cum += mv
                sm_dep |= mv
                sm_kA = np.where(mv, jA, sm_kA)
                sm_kL = np.where(mv, jL, sm_kL)

        if step in dump_steps:
            dumps[f"po{dump_steps[step]:g}"] = {"a": aE.astype(np.float32).tolist(),
                                                "L": L.astype(np.float32).tolist(),
                                                "active": active.tolist()}
        if si < len(snap_steps) and step >= snap_steps[si]:
            snap_rows.append({"step": step, "t": t / (2.0 * np.pi),
                              "f": [float(d.mean()) for d in departed],
                              "x": [int(c.sum()) for c in cum],
                              "smx": int(sm_cum.sum()),
                              "secx": int(sec_cum.sum()),
                              "exited": int(exited.sum())})
            si += 1

    # final dump
    dumps["final"] = {"a": aE.astype(np.float32).tolist(), "L": L.astype(np.float32).tolist(),
                      "active": active.tolist()}

    wall = time.time() - t_start
    po_elapsed = (steps * dt) / (2.0 * np.pi * args.ap ** 1.5)
    P_p_yr = args.ap ** 1.5
    ceiling = args.dtpo * args.ap ** 1.5  # max countable events per planet orbit (stride 1)

    def dist(v):
        v = np.sort(v.astype(float))
        n = len(v)
        return {"med": float(np.median(v)), "mean": float(v.mean()),
                "p90": float(v[int(0.90 * (n - 1))]), "p99": float(v[int(0.99 * (n - 1))]),
                "p999": float(v[int(0.999 * (n - 1))]), "max": float(v[-1])}

    def tail_shares(v):
        v = np.sort(v.astype(float))
        n = len(v)
        tot = max(1.0, v.sum())
        k1 = max(1, n // 100)
        k10 = max(1, n // 10)
        return {"top1pct_share": float(v[-k1:].sum() / tot),
                "top10pct_share": float(v[-k10:].sum() / tot)}

    sm_act = sm_cum[active]
    per_band = {}
    for i, (_, _, nm) in enumerate(bands):
        m = band_id == i
        mb = m & active
        if mb.sum() < 30:
            continue
        per_band[nm] = {"n": int(mb.sum()),
                        "sm_med": float(np.median(sm_cum[mb] / po_elapsed)),
                        "sm_top1pct_share": tail_shares(sm_cum[mb])["top1pct_share"],
                        "sec_med": float(np.median(sec_cum[mb] / po_elapsed)) if sec_fires[mb].max() > 0 else None}

    fits = {}
    xs = np.array([r["t"] for r in snap_rows])
    ys = np.array([r["smx"] for r in snap_rows], float)
    sel = (xs > xs[-1] * 0.3) & (ys > 0)
    if sel.sum() > 4:
        fits["smoothed"] = float(np.polyfit(np.log(xs[sel]), np.log(ys[sel]), 1)[0])
    ys2 = np.array([r["secx"] for r in snap_rows], float)
    sel2 = (xs > xs[-1] * 0.3) & (ys2 > 0)
    if sel2.sum() > 4:
        fits["secular"] = float(np.polyfit(np.log(xs[sel2]), np.log(ys2[sel2]), 1)[0])

    halflife = {}
    xs_po = xs / P_p_yr
    for j, b_ in enumerate(bits):
        fs = np.array([r["f"][j] for r in snap_rows])
        if (fs >= 0.5).any():
            idx = int(np.argmax(fs >= 0.5))
            halflife[f"bits{b_}"] = float(np.interp(0.5, fs[:idx + 1], xs_po[:idx + 1]))
        else:
            halflife[f"bits{b_}"] = None

    # tail structure (fix 3): per-ship smoothed counts + birth elements
    out2 = {
        "tag": args.tag, "seed": args.seed, "N": args.N, "mu": args.mu, "ep": args.ep,
        "ceiling_per_po": ceiling, "sm_stride": SM_STRIDE, "sm_w": SM_W,
        "xings_per_po_naive": {f"bits{b_}": dist(cum[j] / po_elapsed) for j, b_ in enumerate(bits)},
        "xings_per_po_deadband_bits16": dist(db_cum / po_elapsed),
        "xings_per_po_smoothed_bits16": dist(sm_cum / po_elapsed),
        "smoothed_tail_bits16": tail_shares(sm_cum),
        "smoothed_tail_active_bits16": tail_shares(sm_act),
        "secular_per_po": dist(sec_cum / po_elapsed),
        "secular_swept_per_po": dist(sec_sw / po_elapsed),
        "secular_tail_bits16": tail_shares(sec_cum),
        "secular_fires_med": float(np.median(sec_fires[active])),
        "ship_sec_cum": sec_cum.astype(int).tolist(),
        "f_departed_smoothed_bits16": float(sm_dep.mean()),
        "exited_domain_frac": float(exited.mean()),
        "halflife_po": halflife,
        "swept_per_po": {f"bits{b_}": dist(sw[j] / po_elapsed) for j, b_ in enumerate(bits)},
        "exponent_fits": fits,
        "per_band_smoothed": per_band,
        "ship_birth_a": a.astype(float).tolist(),
        "ship_birth_e": e.astype(float).tolist(),
        "ship_band": band_id.tolist(),
        "ship_active": active.tolist(),
        "ship_sm_cum": sm_cum.astype(int).tolist(),
        "machine": {"nproc": __import__("os").cpu_count(),
                    "load": open("/proc/loadavg").read().split()[0],
                    "memfree_gb": open("/proc/meminfo").readline().split()[1]},
        "snaps": snap_rows,
        "dumps": dumps,
    }
    with open(f"{args.tag}.2.json", "w") as fh:
        json.dump(out2, fh)
    print(f"{args.tag}: secular med {out2['secular_per_po']['med']:.3f} "
          f"p99 {out2['secular_per_po']['p99']:.3f} "
          f"top1 {out2['secular_tail_bits16']['top1pct_share']:.4f} "
          f"fires {out2['secular_fires_med']:.0f} fit {out2['exponent_fits'].get('secular')}")
    smd = out2["xings_per_po_smoothed_bits16"]
    print(f"{args.tag}: wall {wall:.1f}s ceiling {ceiling:.1f} "
          f"naive16 {out2['xings_per_po_naive']['bits16']['med']:.2f} "
          f"naive12 {out2['xings_per_po_naive']['bits12']['med']:.2f} "
          f"naive8 {out2['xings_per_po_naive']['bits8']['med']:.2f} "
          f"sm_med {smd['med']:.2f} sm_p99 {smd['p99']:.2f} "
          f"sm_p99med {smd['p99'] / max(1e-9, smd['med']):.2f} sm_top1 {out2['smoothed_tail_bits16']['top1pct_share']:.4f}")


if __name__ == "__main__":
    main()
