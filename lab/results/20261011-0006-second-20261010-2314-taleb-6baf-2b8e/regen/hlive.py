#!/usr/bin/env python3
"""H_live of a stirred belt: quantum-key departures per game-second.

Model: massless ships (test particles) around the Sun (GM=1), one stirrer of
mass mu on an analytic Kepler orbit (a_p, e_p). Leapfrog KDK, fixed dt,
heliocentric + indirect term (standard test-particle form).

Law's representation (docs/law.md): a ship lives as (population, ordinal);
the tube view is keyed by quantized (E, L). On-program = the key the
population program predicts (birth key: Kepler drift conserves E, L exactly).
A key change is a live distinction (scar-layer event); counted on integer
cell indices only. Naive and deadband (+-1 cell hysteresis) quantizers.
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
    p.add_argument("--bits", default="4,8,12,16")
    args = p.parse_args()

    rng = np.random.default_rng(args.seed)
    dt = 2.0 * np.pi / args.dtpo
    steps = int(round(args.po * 2.0 * np.pi * args.ap ** 1.5 / dt))

    # --- ship state (heliocentric, perifocal placement) ---
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
    vy = vxp_ * sO + vyp_ * cO

    # --- quantization grid (a from E; L scalar in 2D) ---
    A_LO, A_HI = 1.0, 8.0
    L_LO, L_HI = 0.40, 2.50
    bits = [int(b) for b in args.bits.split(",")]
    qA = [(A_HI - A_LO) / (2.0 ** b) for b in bits]
    qL = [(L_HI - L_LO) / (2.0 ** b) for b in bits]
    NA16 = 1 << 16

    def keys(x, y, vx, vy):
        r = np.sqrt(x * x + y * y)
        E = 0.5 * (vx * vx + vy * vy) - 1.0 / r
        aE = np.where(E < 0, -0.5 / np.where(E < 0, E, 1e-300), A_HI + 1.0)
        L = x * vy - y * vx
        return aE, L

    aE, L = keys(x, y, vx, vy)
    pk = [((aE - A_LO) / q).astype(np.int64) * NA16 + ((L - L_LO) / ql).astype(np.int64)
          for q, ql in zip(qA, qL)]
    cum = [np.zeros(args.N, np.int64) for _ in bits]
    departed = [np.zeros(args.N, bool) for _ in bits]
    # smoothed-key (secular-residual) counters: rolling mean over SM_W samples,
    # one sample per SM_STRIDE steps; kills synodic/short oscillation, keeps drift
    SM_STRIDE, SM_W = 8, 128
    sm_bufA = np.zeros((SM_W, args.N))
    sm_bufL = np.zeros((SM_W, args.N))
    sm_cum = np.zeros(args.N, np.int64)
    sm_dep = np.zeros(args.N, bool)
    sm_n, sm_kA, sm_kL = 0, None, None
    db_ia, db_iL = ((aE - A_LO) / qA[-1]).astype(np.int64), ((L - L_LO) / qL[-1]).astype(np.int64)
    db_cum = np.zeros(args.N, np.int64)

    active = np.ones(args.N, bool)
    exited = np.zeros(args.N, bool)

    xp, yp, _, _ = planet_xv(0.0, args.ap, args.ep)
    ax, ay = accel(x, y, xp, yp, args.mu)
    t = 0.0

    snap_steps = np.unique(np.round(np.geomspace(10, steps, 40)).astype(int)).tolist()
    snap_rows = []
    ent_steps = set(np.round(np.geomspace(10, steps, 8)).astype(int).tolist())
    ent_snaps = []
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

        if step % 4 == 0:
            aE, L = keys(x, y, vx, vy)
            out = (aE < A_LO) | (aE >= A_HI) | (L < L_LO) | (L >= L_HI)
            exited |= out & active
            active &= ~out
            m = active
            for j in range(len(bits)):
                k = ((aE - A_LO) / qA[j]).astype(np.int64) * NA16 + ((L - L_LO) / qL[j]).astype(np.int64)
                chg = (k != pk[j]) & m
                cum[j] += chg
                departed[j] |= chg
                pk[j] = np.where(m, k, pk[j])
            ia_ = ((aE - A_LO) / qA[-1]).astype(np.int64)
            iL_ = ((L - L_LO) / qL[-1]).astype(np.int64)
            move = ((np.abs(ia_ - db_ia) > 1) | (np.abs(iL_ - db_iL) > 1)) & m
            db_cum += move
            db_ia = np.where(move, ia_, db_ia)
            db_iL = np.where(move, iL_, db_iL)
            if step % SM_STRIDE == 0:
                idx = sm_n % SM_W
                sm_bufA[idx] = aE
                sm_bufL[idx] = L
                sm_n += 1
                if sm_n >= SM_W:
                    sm_mA = sm_bufA.mean(axis=0)
                    sm_mL = sm_bufL.mean(axis=0)
                    if sm_kA is None:
                        sm_kA = ((sm_mA - A_LO) / qA[-1]).astype(np.int64)
                        sm_kL = ((sm_mL - L_LO) / qL[-1]).astype(np.int64)
                    else:
                        jA = ((sm_mA - A_LO) / qA[-1]).astype(np.int64)
                        jL = ((sm_mL - L_LO) / qL[-1]).astype(np.int64)
                        mv = ((jA != sm_kA) | (jL != sm_kL)) & m
                        sm_cum += mv
                        sm_dep |= mv
                        sm_kA = np.where(mv, jA, sm_kA)
                        sm_kL = np.where(mv, jL, sm_kL)

        if si < len(snap_steps) and step >= snap_steps[si]:
            snap_rows.append({"step": step, "t": t / (2.0 * np.pi),
                              "f": [float(d.mean()) for d in departed],
                              "x": [int(c.sum()) for c in cum],
                              "smx": int(sm_cum.sum()),
                              "exited": int(exited.sum())})
            if step in ent_steps:
                jj = len(bits) - 1
                ia2 = np.clip(((aE - A_LO) / qA[jj]).astype(np.int64), 0, (1 << bits[jj]) - 1)
                iL2 = np.clip(((L - L_LO) / qL[jj]).astype(np.int64), 0, (1 << bits[jj]) - 1)
                packed, cnt = np.unique(ia2 * (1 << 16) + iL2, return_counts=True)
                c = cnt[cnt > 0].astype(float)
                Hj = float(np.log2(len(c)) - (c @ np.log2(c)) / c.sum()
                           + (len(c) - 1) / (2.0 * c.sum() * math.log(2)))
                ha, ca = np.unique(ia2, return_counts=True)
                ca = ca.astype(float)
                Ha = float(np.log2(len(ca)) - (ca @ np.log2(ca)) / ca.sum())
                ent_snaps.append({"t": t / (2.0 * np.pi), "H_joint": Hj, "H_a": Ha,
                                  "cells": int(len(c))})
            si += 1

    wall = time.time() - t_start
    po_elapsed = (steps * dt) / (2.0 * np.pi * args.ap ** 1.5)
    P_p_yr = args.ap ** 1.5

    def dist(v):
        v = np.sort(v.astype(float))
        n = len(v)
        return {"med": float(np.median(v)), "mean": float(v.mean()),
                "p90": float(v[int(0.90 * (n - 1))]), "p99": float(v[int(0.99 * (n - 1))]),
                "p999": float(v[int(0.999 * (n - 1))]), "max": float(v[-1])}

    per_band = {}
    for i, (_, _, nm) in enumerate(bands):
        m = band_id == i
        if m.sum() < 30:
            continue
        v = np.sort(cum[-1][m].astype(float))
        k1 = max(1, int(m.sum()) // 100)
        per_band[nm] = {"n": int(m.sum()),
                        "xings_per_po": dist(cum[-1][m] / po_elapsed),
                        "f_departed": float(departed[-1][m].mean()),
                        "top1pct_share": float(v[-k1:].sum() / max(1, v.sum()))}

    fits = {}
    xs = np.array([r["t"] for r in snap_rows])
    for j in (len(bits) - 1, len(bits) - 2):
        ys = np.array([r["x"][j] for r in snap_rows], float)
        sel = (xs > xs[-1] * 0.3) & (ys > 0)
        if sel.sum() > 4:
            fits[f"bits{bits[j]}"] = float(np.polyfit(np.log(xs[sel]), np.log(ys[sel]), 1)[0])

    halflife = {}
    xs_po = xs / P_p_yr
    for j, b in enumerate(bits):
        fs = np.array([r["f"][j] for r in snap_rows])
        if (fs >= 0.5).any():
            idx = int(np.argmax(fs >= 0.5))
            halflife[f"bits{b}"] = float(np.interp(0.5, fs[:idx + 1], xs_po[:idx + 1]))
        else:
            halflife[f"bits{b}"] = None

    out = {
        "tag": args.tag, "seed": args.seed, "N": args.N, "mu": args.mu, "ep": args.ep,
        "ap": args.ap, "sige": args.sige, "ring": args.ring, "dt": dt, "steps": steps,
        "po": po_elapsed, "wall_s": wall, "bits": bits, "sample_every": 4,
        "xings_per_po_naive": {f"bits{b}": dist(cum[j] / po_elapsed) for j, b in enumerate(bits)},
        "xings_per_po_deadband_bits16": dist(db_cum / po_elapsed),
        "exited_domain_frac": float(exited.mean()),
        "xings_per_po_smoothed_bits16": dist(sm_cum / po_elapsed),
        "f_departed_smoothed_bits16": float(sm_dep.mean()),
        "sm_stride": SM_STRIDE, "sm_w": SM_W,
        "machine": {"nproc": __import__("os").cpu_count(),
                    "load": open("/proc/loadavg").read().split()[0],
                    "memfree_gb": open("/proc/meminfo").readline().split()[1]},
        "halflife_po": halflife,
        "exponent_fits": fits,
        "per_band": per_band,
        "entropy_snaps": ent_snaps,
        "snaps": snap_rows,
    }
    with open(f"{args.tag}.json", "w") as fh:
        json.dump(out, fh)
    print(f"{args.tag}: wall {wall:.1f}s exited {out['exited_domain_frac']:.4f} "
          f"med16 {out['xings_per_po_naive']['bits16']['med']:.3f} "
          f"p99_16 {out['xings_per_po_naive']['bits16']['p99']:.3f} "
          f"fit16 {fits.get('bits16')} hl16 {halflife.get('bits16')}")

if __name__ == "__main__":
    main()
