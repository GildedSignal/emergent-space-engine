#!/usr/bin/env python3
"""Belt-scale entropy: N = 2^20 test particles, birth vs mature (a, L).

Same physics as hlive.py (leapfrog KDK, same placement code, same grids).
No counters: this run exists to give the entropy estimators a sample at the
belt scale where plug-in at coarse grids converges, and to show that plug-in
at the fine (bits16) grid is STILL pinned at log2(N)+0.72 even at N = 2^20
(effective occupancy ~1e7 cells >> N). k-NN (Kozachenko-Leonenko) is the
N-scalable estimator; reported in bits on raw (a, L) sim units.
"""
import argparse, json, time, math
import numpy as np
from scipy.spatial import cKDTree
from scipy.special import digamma


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


def keys(x, y, vx, vy):
    r = np.sqrt(x * x + y * y)
    E = 0.5 * (vx * vx + vy * vy) - 1.0 / r
    aE = np.where(E < 0, -0.5 / np.where(E < 0, E, 1e-300), 8.0 + 1.0)
    L = x * vy - y * vx
    return aE, L


def plugin(aE, L, bits, A_LO=1.0, A_HI=8.0, L_LO=0.40, L_HI=2.50):
    qA = (A_HI - A_LO) / (2.0 ** bits)
    qL = (L_HI - L_LO) / (2.0 ** bits)
    ia = np.clip(((aE - A_LO) / qA).astype(np.int64), 0, (1 << bits) - 1)
    iL = np.clip(((L - L_LO) / qL).astype(np.int64), 0, (1 << bits) - 1)
    _, cnt = np.unique(ia * (1 << bits) + iL, return_counts=True)
    c = cnt[cnt > 0].astype(float)
    H = float(np.log2(len(c)) - (c @ np.log2(c)) / c.sum()
              + (len(c) - 1) / (2.0 * c.sum() * math.log(2)))
    return H, int(len(c))


def knn_entropy(aE, L, k):
    """Kozachenko-Leonenko k-NN differential entropy, 2D, bits, raw units."""
    X = np.column_stack([aE, L]).astype(float)
    N = X.shape[0]
    tree = cKDTree(X)
    d, _ = tree.query(X, k=k + 1)  # +1: self at distance 0
    r = d[:, k]
    r = r[r > 0]
    h = ((digamma(N) - digamma(k)) / math.log(2) + math.log2(math.pi)
          + 2.0 * np.mean(np.log2(r)))
    return float(h)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--tag", default="big")
    p.add_argument("--seed", type=int, default=11)
    p.add_argument("--N", type=int, default=1 << 20)
    p.add_argument("--po", type=float, default=100.0)
    p.add_argument("--dtpo", type=float, default=64.0)
    p.add_argument("--mu", type=float, default=1e-3)
    p.add_argument("--ap", type=float, default=1.6)
    p.add_argument("--ep", type=float, default=0.05)
    p.add_argument("--a0", type=float, default=2.0)
    p.add_argument("--a1", type=float, default=3.5)
    p.add_argument("--sige", type=float, default=0.02)
    args = p.parse_args()

    rng = np.random.default_rng(args.seed)
    dt = 2.0 * np.pi / args.dtpo
    steps = int(round(args.po * 2.0 * np.pi * args.ap ** 1.5 / dt))
    N = args.N

    a = args.a0 + (args.a1 - args.a0) * rng.random(N)
    e = rng.rayleigh(args.sige, N)
    om = 2.0 * np.pi * rng.random(N)
    Ma = 2.0 * np.pi * rng.random(N)
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

    aE0, L0 = keys(x, y, vx, vy)
    xp, yp, _, _ = planet_xv(0.0, args.ap, args.ep)
    ax, ay = accel(x, y, xp, yp, args.mu)
    t = 0.0
    t0 = time.time()
    for step in range(1, steps + 1):
        vhx, vhy = vx + 0.5 * dt * ax, vy + 0.5 * dt * ay
        x = x + dt * vhx
        y = y + dt * vhy
        t += dt
        xp, yp, _, _ = planet_xv(t, args.ap, args.ep)
        ax, ay = accel(x, y, xp, yp, args.mu)
        vx = vhx + 0.5 * dt * ax
        vy = vhy + 0.5 * dt * ay
    wall = time.time() - t0
    aE1, L1 = keys(x, y, vx, vy)
    live = (aE1 >= 1.0) & (aE1 < 8.0) & (L1 >= 0.40) & (L1 < 2.50)

    res = {"tag": args.tag, "seed": args.seed, "N": N, "po": args.po,
           "steps": steps, "mu": args.mu, "wall_s": wall,
           "live_frac_final": float(live.mean()),
           "machine": {"nproc": __import__("os").cpu_count(),
                       "load": open("/proc/loadavg").read().split()[0],
                       "memfree_gb": open("/proc/meminfo").readline().split()[1]}}

    # plug-in at coarse grids (converged when cells << N) and at bits16 (pinned)
    for b_ in (6, 8, 10, 12, 16):
        Hb, cb = plugin(aE0, L0, b_)
        Hf, cf = plugin(aE1[live], L1[live], b_)
        res[f"plugin_bits{b_}"] = {"birth_H": Hb, "birth_cells": cb,
                                   "final_H": Hf, "final_cells": cf}
    res["plugin_log2N_plus_072"] = math.log2(N) + 0.7213

    # kNN differential entropy on full sample (final) and birth, k in {1,8,16}
    sub0 = rng.choice(N, size=min(262144, N), replace=False)
    res["knn_birth"] = {f"k{k}": knn_entropy(aE0[sub0], L0[sub0], k) for k in (1, 8, 16)}
    res["knn_final_full"] = {f"k{k}": knn_entropy(aE1[live], L1[live], k) for k in (1, 8, 16)}
    # N-invariance probe: 4000-ship subsample of the same final population
    sub4k = rng.choice(int(live.sum()), size=4000, replace=False)
    res["knn_final_4k"] = {f"k{k}": knn_entropy(aE1[live][sub4k], L1[live][sub4k], k)
                           for k in (1, 8, 16)}

    np.savez_compressed(f"{args.tag}_samples.npz",
                        birth_a=aE0[sub0].astype(np.float32), birth_L=L0[sub0].astype(np.float32),
                        final_a=aE1[live][sub4k].astype(np.float32),
                        final_L=L1[live][sub4k].astype(np.float32))
    with open(f"{args.tag}_entropy.json", "w") as fh:
        json.dump(res, fh, indent=1)
    print(json.dumps({k: v for k, v in res.items() if k not in ("machine",)}, indent=1)[:1200])


if __name__ == "__main__":
    main()
