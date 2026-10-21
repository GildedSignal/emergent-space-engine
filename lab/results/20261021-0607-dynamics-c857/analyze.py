#!/usr/bin/env python3
"""The dumps' analysis (lab/results/20261021-0607-dynamics-c857): the two allocator-relevant
quantities the per-generation table cannot see, from the raw dues of every belt body.

1. Pooled worst-window load: ALL dues (every generation) on the game timeline, sliding windows of
   L = step_med/32, max count / mean against the Poisson expectation E[max/mu] for the same mean
   load and window count (analytic Gaussian head; the Monte-Carlo floor of the flight table is the
   same statistic per generation). Reported per decade of generation so the transient is visible.
2. Locked pairs: pairs of bodies whose dues stay within one window L for k >= 8 consecutive
   generations (co-firing); the chance rate is measured by the same count on dues re-drawn
   uniformly within each generation's span (the uniform control of the flight table). The seed
   contrast (a97f: seed 1 has a locked-pair part, seed 2 none) is the prediction P4.

用法: analyze.py <run folder>   (reads work/dues_s<seed>.bin, writes work/analysis.txt)
"""
import struct
import sys
from pathlib import Path


def load(path):
    """-> {g: [(id, due), ...]}"""
    data = path.read_bytes()
    out = {}
    o = 0
    while o + 16 <= len(data):
        g, n, mn = struct.unpack_from("<IIq", data, o)
        o += 16
        gen = []
        for _ in range(n):
            i, off = struct.unpack_from("<Hq", data, o)
            o += 10
            gen.append((i, mn + off))
        out[g] = gen
    return out


def floor_maxmu(mu, w, rng):
    """E[max count]/mu for w Poisson(mu) windows, 2000 draws."""
    import math
    reps = 2000
    maxes = []
    z = rng
    for _ in range(reps):
        # Poisson by inverse-CDF on a small mean: direct counting of uniforms
        c = [0] * w
        n = int(mu * w)
        for _ in range(n):
            k = z() % w
            c[k] += 1
        maxes.append(max(c))
    maxes.sort()
    return maxes[len(maxes) // 2] / mu, math.sqrt(mu)


def lcg(seed):
    state = [seed]

    def nxt():
        state[0] = (state[0] * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)
        return state[0] >> 16

    return nxt


def main(folder):
    out = []
    for seed in (1, 2):
        p = Path(folder) / f"work/dues_s{seed}.bin"
        if not p.exists():
            continue
        gens = load(p)
        gs = sorted(gens)
        out.append(f"== seed {seed}: generations {gs[0]}..{gs[-1]}, bodies {len(gens[gs[0]])}")
        # per-body due sequences for pair locking and step medians
        seq = {}
        for g in gs:
            for i, d in gens[g]:
                seq.setdefault(i, {})[g] = d
        # median step per body (modal interval), then the global median step
        steps = []
        for i, s in seq.items():
            kk = sorted(s)
            iv = [s[k + 1] - s[k] for k in kk[:-1]]
            if iv:
                steps.append(iv[len(iv) // 2])
        steps.sort()
        step_med = steps[len(steps) // 2]
        L = step_med // 32
        out.append(f"   step_med={step_med} ticks, window L={L}")
        # 1. pooled worst-window load per generation decade (windows tiled over the pooled dues)
        for lo, hi in [(1, 16), (17, 48), (49, 96), (97, gs[-1])]:
            dues = [d for g in gs if lo <= g <= hi for _, d in gens[g]]
            if len(dues) < 200:
                continue
            t0, t1 = min(dues), max(dues)
            w = max(1, (t1 - t0) // L)
            cnt = [0] * w
            for d in dues:
                cnt[min((d - t0) // L, w - 1)] += 1
            mu = len(dues) / w
            mx = max(cnt)
            fl, _ = floor_maxmu(mu, min(w, 512), lcg(0xC0FFEE + seed))
            out.append(f"   pooled g[{lo},{hi}] dues={len(dues)} windows={w} mu={mu:.1f} max/mu={mx / mu:.3f} poisson_floor={fl:.3f} excess={mx / mu - fl:+.3f}")
        # 2. locked pairs: |due_i - due_j| < L for >= 8 consecutive generations (sliding anchor)
        kk = sorted(seq)
        ids = kk
        lock_counts = {}
        run = {}
        for g in gs:
            cur = sorted((d, i) for i, d in ((i, seq[i].get(g)) for i in ids) if d is not None)
            close = set()
            for a in range(len(cur) - 1):
                if cur[a + 1][0] - cur[a][0] < L:
                    x, y = tuple(sorted((cur[a][1], cur[a + 1][1])))
                    close.add((x, y))
            for pr in close:
                run[pr] = run.get(pr, 0) + 1
                if run[pr] == 8:
                    lock_counts[pr] = g
            for pr in list(run):
                if pr not in close:
                    del run[pr]
        out.append(f"   locked pairs (>=8 consecutive gens within L): {len(lock_counts)}")
        # control: same count on uniform-redrawn dues (destroys pairs, keeps one-per-body-per-gen)
        rng = lcg(0xBADA55 + seed)
        locked_c = 0
        seq_c = {}
        for g in gs:
            dg = [d for _, d in gens[g]]
            mn, mx = min(dg), max(dg)
            span = max(1, mx - mn)
            for i in ids:
                seq_c.setdefault(i, {})[g] = mn + (rng() % span)
        run = {}
        for g in gs:
            cur = sorted((d, i) for i, d in ((i, seq_c[i].get(g)) for i in ids) if d is not None)
            close = set()
            for a in range(len(cur) - 1):
                if cur[a + 1][0] - cur[a][0] < L:
                    x, y = tuple(sorted((cur[a][1], cur[a + 1][1])))
                    close.add((x, y))
            for pr in close:
                run[pr] = run.get(pr, 0) + 1
                if run[pr] == 8:
                    locked_c += 1
            for pr in list(run):
                if pr not in close:
                    del run[pr]
        out.append(f"   control (uniform redraw, pairs destroyed): {locked_c}")
    txt = "\n".join(out)
    print(txt)
    (Path(folder) / "work/analysis.txt").write_text(txt + "\n")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
