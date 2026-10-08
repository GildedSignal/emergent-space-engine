"""Dump-then-analyze: run the physics once, cache mean elements, analyze fast.

Usage: python3 reband2.py phys   (~7 min: writes /tmp/reband-means.npy)
       python3 reband2.py analyze (seconds: the whole table + pricing)
"""
import math
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "orig"))
import hlive_belt as H
import reband as R  # cells, Store, KS, WIDTHS, price, N_ORIG, CP_ORBITS, REF_ORBIT

DUMP = "/tmp/reband-means.npy"
LOG_EVERY = 25


def phys():
    H.MU_J = 9.5459e-4
    T = 2400.0
    rng = np.random.default_rng(7)
    a0, e0, lam, varpi, m = H.belt(R.N_ALL, rng)
    s = H.state(a0, e0, lam, varpi)
    dt = H.PJ / 775
    nst = int(round(T / dt))
    cp_step = max(1, round(R.REF_ORBIT * R.CP_ORBITS / dt))
    ring_a = np.zeros((R.SMOOTH_N, R.N_ALL))
    ring_e = np.zeros((R.SMOOTH_N, R.N_ALL))
    ri = 0
    t = 0.0
    cp = 0
    means = []
    orbs = []
    for step in range(nst + 1):
        if step % cp_step == 0:
            a, e = H.elements(s[0], s[1], s[2], s[3])
            ring_a[ri], ring_e[ri] = a, e
            ri = (ri + 1) % R.SMOOTH_N
            filled = min(cp + 1, R.SMOOTH_N)
            means.append(np.stack([ring_a[:filled].mean(0), ring_e[:filled].mean(0)]).astype(np.float32))
            orbs.append(t / R.REF_ORBIT)
            cp += 1
        if step == nst:
            break
        xj, yj = H.jup(t + dt / 2)
        s[0] += s[2] * dt / 2
        s[1] += s[3] * dt / 2
        ax, ay = H.accel(s[0], s[1], xj, yj)
        s[2] += ax * dt
        s[3] += ay * dt
        s[0] += s[2] * dt / 2
        s[1] += s[3] * dt / 2
        t += dt
    np.save(DUMP, np.asarray(means))
    np.save("/tmp/reband-orbs.npy", np.asarray(orbs))
    print(f"dumped {len(means)} checkpoints to {DUMP}")


def analyze():
    means = np.load(DUMP).astype(np.float64)
    orbs = np.load("/tmp/reband-orbs.npy")
    m = R.N_ORIG
    T = orbs[-1]
    stores, last_orb = {}, {}
    log, samples, twins = [], {}, []
    for ci, orb in enumerate(orbs):
        ma, me = means[ci, 0], means[ci, 1]
        out = {b: R.cells(ma[:m], me[:m], b) for b in R.WIDTHS}
        kA = out[12][0] * (1 << 18) + out[12][1]
        kB = R.cells(ma[m:2 * m], me[m:2 * m], 12)
        kC = R.cells(ma[2 * m:], me[2 * m:], 12)
        twins.append((orb, float((kB[0] * (1 << 18) + kB[1] != kA).mean()),
                      float((kC[0] * (1 << 18) + kC[1] != kA).mean())))
        for b in R.WIDTHS:
            js, jh = out[b]
            for k in R.KS:
                key = (b, k)
                if key not in stores:
                    stores[key] = R.Store(js, jh, k)
                    last_orb[key] = 0.0
                st = stores[key]
                scarred, d, multi = st.step(js, jh)
                if st.maybe_reband(js, jh, orb - last_orb[key]):
                    last_orb[key] = orb
                if abs(orb % LOG_EVERY) < R.CP_ORBITS / 2:
                    r0 = log_row(log, orb, b, k)
                    r0.update(f=float(scarred.mean()),
                              fm=float(scarred[multi].mean()) if multi.any() else 0.0,
                              med=float(np.median(d[scarred])) if scarred.any() else 0.0,
                              p90=float(np.percentile(d[scarred], 90)) if scarred.any() else 0.0,
                              R=st.R)
                near_end = orb >= T - 120
                want = (isinstance(k, (int, float)) and k != math.inf and near_end
                        and len(samples.get(key, [])) < 6
                        and (abs(orb % k - k / 2) <= 0.2 or abs(orb % k - (k - R.CP_ORBITS)) <= 0.2))
                want_static = (k in (math.inf, "frozen") and orb >= T - 30
                               and len(samples.get(key, [])) < 1)
                if want or want_static:
                    idx = np.flatnonzero(scarred)
                    ds = js - st.rec_s
                    dh = jh - st.rec_h
                    samples.setdefault(key, []).append(
                        [(int(i), int(ds[i]), int(dh[i])) for i in idx])
    print(f"{'b':>3} {'k':>6} {'occ':>6} {'f_scar':>7} {'f_mult':>7} {'med|d|':>6} {'p90':>6} "
          f"{'R':>6} {'bits/b':>7} {'scarb/b':>7} {'recb/b':>7} {'tot':>7} {'H_live':>8}")
    for b in R.WIDTHS:
        for k in R.KS:
            rows = [r for r in log if r["b"] == b and r["k"] == k and r["orb"] >= T - 111]
            if not rows:
                continue
            f = np.mean([r["f"] for r in rows])
            fm = np.mean([r["fm"] for r in rows])
            med = np.mean([r["med"] for r in rows])
            p90 = np.mean([r["p90"] for r in rows])
            Rn = int(np.mean([r["R"] for r in rows]))
            occ = R.N_ORIG / Rn
            name = k if k != math.inf else "inf"
            pr = [R.price(s, R.N_ORIG) for s in samples.get((b, k), [])]
            sb = float(np.mean([p[0] for p in pr]) / R.N_ORIG) if pr else float("nan")
            nsc = int(np.mean([p[1] for p in pr])) if pr else 0
            bps = float(np.mean([p[0] / max(p[1], 1) for p in pr])) if pr else float("nan")
            rb = Rn * 32.0 / R.N_ORIG
            kk = k if isinstance(k, (int, float)) and k != math.inf else 541
            print(f"{b:3d} {str(name):>6} {occ:6.1f} {f:7.3f} {fm:7.3f} {med:6.1f} {p90:6.1f} "
                  f"{Rn:6d} {bps:7.1f} {sb:7.2f} {rb:7.2f} {sb + rb:7.2f} {(sb + rb) / kk:8.4f}"
                  f"   scars~{nsc}")
    print("--- twin anchor b=12 (orbit, split@+0.2q, split@+0.05q):")
    for orb, f4, f1 in twins:
        if abs(orb % 50) < R.CP_ORBITS / 2:
            print(f"  {orb:6.1f}  {f4:.3f}  {f1:.3f}")
    print("--- convergence b=6, b=5 (orb then f per k in KS order):")
    for b in (6, 5):
        for r in log:
            if r["b"] == b and abs(r["orb"] % 100) < R.CP_ORBITS / 2:
                same = sorted([r2 for r2 in log if r2["b"] == b and r2["orb"] == r["orb"]],
                              key=lambda r2: R.KS.index(r2["k"]))
                print(f"  b{b} {r['orb']:6.1f}  " + "  ".join(f"{x['f']:.3f}" for x in same))


def log_row(log, orb, b, k):
    for r in log:
        if r["orb"] == orb and r["b"] == b and r["k"] == k:
            return r
    r = dict(orb=orb, b=b, k=k)
    log.append(r)
    return r


if __name__ == "__main__":
    phys() if sys.argv[1] == "phys" else analyze()
