#!/usr/bin/env python3
"""H_live creation-rate probe: encounters and contacts on a Kepler belt (v2, fixed).

Units: length AU-like, mass = the doll's mass, G*M = 4*pi^2, time in orbits at a=1
(P(a) = a^1.5, v_circ(1) = 2*pi). Belt: B18b's frozen geometry (p one octave,
e Rayleigh sigma, uniform angles/phases).

Method: fixed steps (720 per a=1 orbit; worst-case per-step relative displacement of
counted events ~1e-2 < FLAG_D) with spatial hashing find every pair that comes within
FLAG_D; each flag's impact parameter b = |dr x dv|/|dv| is computed analytically from
the current (r, v), resolving encounter radii far below the step size. Rows dedupe to
one per conjunction, so one event set yields the rate at every rho simultaneously, plus
per-event kick geometry for the mass/quantum sweep.

v2 fix: slow near-co-orbital flybys (v_rel ~ 0.01, duration ~ an orbit) flooded the
compact row stream in low-sigma_e belts (the first run was OOM-killed there). The
stream now subsamples the b in (3e-4, 3e-3) band every 16th step (any event spans
>= 16 steps there, so none is lost), and the dedupe window is a parameter (2.0 for
low-sigma_e belts, where approach durations reach ~1 orbit; the minimum synodic
period of two distinct conjunctions is 1.67 orbits there).
"""
import numpy as np
import json
import time

TWO_PI = 2.0 * np.pi
G_CONST = 4.0 * np.pi ** 2
CELL = 1.2e-2
FLAG_D = 1.2e-2
STEPS_PER_ORBIT = 720
STRIDE = np.int64(1 << 21)
ORIGIN = 6.0
COMPACT_B = 3e-3
GEOM_B = 2e-4


def sample_belt(N, a0, a1, sigma_e, e_cap, seed):
    rng = np.random.default_rng(seed)
    a = rng.uniform(a0, a1, N)
    e = np.minimum(rng.rayleigh(sigma_e, N), e_cap)
    w = rng.uniform(0.0, TWO_PI, N)
    M0 = rng.uniform(0.0, TWO_PI, N)
    return a, e, w, M0


class Kepler:
    def __init__(self, a, e, w, M0):
        self.a, self.e, self.M0 = a, e, M0
        self.n = TWO_PI * a ** -1.5
        self.sq = np.sqrt(1.0 - e * e)
        self.cw, self.sw = np.cos(w), np.sin(w)

    def state(self, t):
        M = self.M0 + self.n * t
        E = M + self.e * np.sin(M)
        for _ in range(5):
            E -= (E - self.e * np.sin(E) - M) / (1.0 - self.e * np.cos(E))
        cE, sE = np.cos(E), np.sin(E)
        xo = self.a * (cE - self.e)
        yo = self.a * self.sq * sE
        x = self.cw * xo - self.sw * yo
        y = self.sw * xo + self.cw * yo
        dE = self.n / (1.0 - self.e * cE)
        vxo = -self.a * sE * dE
        vyo = self.a * self.sq * cE * dE
        vx = self.cw * vxo - self.sw * vyo
        vy = self.sw * vxo + self.cw * vyo
        return x, y, vx, vy


def pair_indices(x, y, max_run=24):
    nx = ((x + ORIGIN) / CELL).astype(np.int64)
    ny = ((y + ORIGIN) / CELL).astype(np.int64)
    key = nx * STRIDE + ny
    order = np.argsort(key, kind="stable")
    sk = key[order]
    pi, pj = [], []
    run_id = np.cumsum(np.r_[0, np.diff(sk) != 0])
    for d in range(1, max_run):
        m = run_id[:-d] == run_id[d:]
        if not m.any():
            break
        pi.append(order[:-d][m])
        pj.append(order[d:][m])
    body_sorted = np.arange(len(order))
    for dx, dy in ((1, 0), (0, 1), (1, 1), (1, -1)):
        nk = (nx + dx) * STRIDE + (ny + dy)
        lo = np.searchsorted(sk, nk, "left")
        hi = np.searchsorted(sk, nk, "right")
        cnt = hi - lo
        tot = int(cnt.sum())
        if tot == 0:
            continue
        rep = np.repeat(body_sorted, cnt)
        starts = np.cumsum(cnt) - cnt
        off = np.arange(tot) - np.repeat(starts, cnt)
        pi.append(order[rep])
        pj.append(order[lo[rep] + off])
    if not pi:
        return np.empty(0, np.int64), np.empty(0, np.int64)
    return np.concatenate(pi), np.concatenate(pj)


def dedupe(rows, window=0.3):
    """One row per conjunction: same (i,j) within `window` orbits; keep min b."""
    if len(rows) == 0:
        return rows
    R = rows
    order = np.lexsort((R[:, 2], R[:, 1], R[:, 0]))
    R = R[order]
    same = (R[1:, 0] == R[:-1, 0]) & (R[1:, 1] == R[:-1, 1]) & (R[1:, 2] - R[:-1, 2] < window)
    grp = np.r_[0, np.cumsum(~same)]
    o2 = np.lexsort((R[:, 4], grp))
    first = np.ones(len(R), dtype=bool)
    first[1:] = grp[o2][1:] != grp[o2][:-1]
    return R[o2[first]]


def simulate(N, a0, a1, sigma_e, seed, T, e_cap=0.6, window=0.3):
    a, e, w, M0 = sample_belt(N, a0, a1, sigma_e, e_cap, seed)
    kep = Kepler(a, e, w, M0)
    nsteps = int(round(T * STEPS_PER_ORBIT))
    compact, geom = [], []
    for k in range(nsteps):
        t = k / STEPS_PER_ORBIT
        x, y, vx, vy = kep.state(t)
        ci, cj = pair_indices(x, y)
        if len(ci) == 0:
            continue
        ci, cj = ci.copy(), cj.copy()
        sw = ci > cj
        ci[sw], cj[sw] = cj[sw], ci[sw]
        dx, dy = x[ci] - x[cj], y[ci] - y[cj]
        d2 = dx * dx + dy * dy
        m = d2 < FLAG_D * FLAG_D
        if not m.any():
            continue
        ci, cj, dx, dy, d2 = ci[m], cj[m], dx[m], dy[m], d2[m]
        dvx, dvy = vx[ci] - vx[cj], vy[ci] - vy[cj]
        vrel2 = dvx * dvx + dvy * dvy
        vrel = np.sqrt(vrel2)
        cross = dx * dvy - dy * dvx
        with np.errstate(invalid="ignore", divide="ignore"):
            b = np.abs(cross) / vrel
        mc = (b < 3e-4) | ((b < COMPACT_B) & (k % 16 == 0))
        if mc.any():
            compact.append(np.column_stack([ci[mc], cj[mc], np.full(int(mc.sum()), t),
                                            np.sqrt(d2[mc]), b[mc], vrel[mc]]))
        mg = b < GEOM_B
        if mg.any():
            dot = dx[mg] * dvx[mg] + dy[mg] * dvy[mg]
            bhx = dx[mg] - dot / vrel2[mg] * dvx[mg]
            bhy = dy[mg] - dot / vrel2[mg] * dvy[mg]
            bn = np.sqrt(bhx * bhx + bhy * bhy)
            safe = np.where(bn > 0, bn, 1.0)
            bhx, bhy = bhx / safe, bhy / safe
            geom.append(np.column_stack([
                ci[mg], cj[mg], np.full(int(mg.sum()), t), np.sqrt(d2[mg]), b[mg], vrel[mg],
                bhx, bhy, vx[ci[mg]], vy[ci[mg]], vx[cj[mg]], vy[cj[mg]],
                x[ci[mg]], y[ci[mg]], x[cj[mg]], y[cj[mg]]]))
    C = dedupe(np.concatenate(compact), window) if compact else np.empty((0, 6))
    Gm = dedupe(np.concatenate(geom), window) if geom else np.empty((0, 16))
    return C, Gm


def report(C, N, T):
    b = C[:, 4]
    out = {"events_per_body_per_a1orbit": {}, "b_slope": None}
    for rho in (1e-4, 3e-5, 1e-5, 3e-6, 1e-6):
        out["events_per_body_per_a1orbit"][f"{rho:.0e}"] = float((b < rho).sum() / (N * T))
    edges = np.logspace(-6, np.log10(COMPACT_B), 31)
    h, _ = np.histogram(b, bins=edges)
    ok = h > 20
    if ok.sum() > 5:
        cx = np.log(edges[:-1]) + 0.5 * np.log(edges[1:] / edges[:-1])
        out["b_slope"] = float(np.polyfit(cx[ok], np.log(h[ok]), 1)[0])
    return out


def kick_entropy(Gm, mu, qE, qL, rho_skin=1e-4):
    m = Gm[:, 4] < rho_skin
    if m.sum() < 30:
        return {"bits": 0.0, "n": int(m.sum()), "subquantum_frac": 1.0}
    b, vrel = Gm[m, 4], Gm[m, 5]
    bhx, bhy = Gm[m, 6], Gm[m, 7]
    vxi, vyi, vxj, vyj = Gm[m, 8], Gm[m, 9], Gm[m, 10], Gm[m, 11]
    xi, yi, xj, yj = Gm[m, 12], Gm[m, 13], Gm[m, 14], Gm[m, 15]
    scale = 2.0 * G_CONST * (2.0 * mu) / (vrel * b)
    dvx_rel, dvy_rel = scale * bhx, scale * bhy
    dvxi, dvyi = -0.5 * dvx_rel, -0.5 * dvy_rel
    dvxj, dvyj = 0.5 * dvx_rel, 0.5 * dvy_rel
    dEi, dEj = vxi * dvxi + vyi * dvyi, vxj * dvxj + vyj * dvyj
    dLi, dLj = xi * dvyi - yi * dvxi, xj * dvyj - yj * dvxj
    dE = np.concatenate([dEi, dEj])
    dL = np.concatenate([dLi, dLj])
    sub = (np.abs(dE) < 0.5 * qE) & (np.abs(dL) < 0.5 * qL)
    pairs = np.column_stack([np.round(dE / qE).astype(np.int64),
                             np.round(dL / qL).astype(np.int64)])
    _, cnt = np.unique(pairs, axis=0, return_counts=True)
    p = cnt / cnt.sum()
    return {"bits": float(-(p * np.log2(p)).sum()), "n": int(len(dE)),
            "subquantum_frac": float(sub.mean())}


def main():
    t0 = time.time()
    runs = [
        ("B18b_N1e4", dict(N=10_000, a0=1.0, a1=2.0, sigma_e=0.07, seed=1, T=6.0)),
        ("B18b_N2e3", dict(N=2_000, a0=1.0, a1=2.0, sigma_e=0.07, seed=2, T=6.0)),
        ("B18b_N5e4", dict(N=50_000, a0=1.0, a1=2.0, sigma_e=0.07, seed=3, T=1.5)),
        ("loE_N1e4", dict(N=10_000, a0=1.0, a1=2.0, sigma_e=0.01, seed=4, T=6.0)),
        ("r8box_mid", dict(N=10_000, a0=1.0, a1=1.5, sigma_e=0.02, seed=5, T=4.0, window=2.0)),
        ("r8box_lo", dict(N=10_000, a0=1.0, a1=1.5, sigma_e=0.004, seed=6, T=4.0, window=2.0)),
    ]
    results = {}
    for name, cfg in runs:
        t1 = time.time()
        C, Gm = simulate(**cfg)
        rep = report(C, cfg["N"], cfg["T"])
        rep.update(N=cfg["N"], T=cfg["T"], compact_events=int(len(C)), geom_events=int(len(Gm)),
                   wall_s=round(time.time() - t1, 1))
        results[name] = rep
        if name == "B18b_N1e4":
            np.save("events_B18b_N1e4_geom.npy", Gm)
        r1 = rep["events_per_body_per_a1orbit"]["1e-04"]
        print(f"{name}: N={cfg['N']} T={cfg['T']} ev={len(C)} rate(1e-4)={r1:.3e} "
              f"slope={rep['b_slope']} wall={rep['wall_s']}s", flush=True)
    with open("hlive.json", "w") as f:
        json.dump(results, f, indent=1)
    print(f"total wall {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
