#!/usr/bin/env python3
"""B18b belt gate mirror (wt/b18-belt af07b33, xtask/src/behave/belt.rs) + red-team plants.

Mirrors: SPEC, SplitMix64 counter stream, rayleigh_grid, scores, chi2 128x128 on (p,t),
serial 18 lags + cross pairs, per-column KS (2^16 bins) vs an iid reference, tail tests
(count z var 2K, reach vs ref's 20th largest, overshoot, tail-shape KS). Thresholds: the
judge's Z_CHI=4.5 Z_SERIAL=5.0 KS_C=2.470 Z_TAIL=4.5, RUNS = 3x 2^20 (seeds 20261008..10)
+ 2^23 (seed 20261011). Verdict per run = every finding passes, as the judge's.
"""
import numpy as np, sys, math

M1 = np.uint64(0xBF58476D1CE4E5B9); M2 = np.uint64(0x94D049BB133111EB)
GAMMA = np.uint64(0x9E3779B97F4A7C15)
def mix64(z):
    z = (z ^ (z >> np.uint64(30))) * M1
    z = (z ^ (z >> np.uint64(27))) * M2
    return z ^ (z >> np.uint64(31))
def at(seed, k):  # k: uint64 array
    return mix64(np.uint64(seed) + (k + np.uint64(1)) * GAMMA)

P_LO, P_BITS, SIG, E_BITS, E_CAP, W_BITS, T_BITS = np.uint64(2048 << 16), 27, 0.070, 30, np.uint64(644245094), 32, 44
def rayleigh_grid(u):
    v = ((u >> np.uint64(12)).astype(np.float64) + 0.5) / 4503599627370496.0
    e = SIG * np.sqrt(-2.0 * np.log(v))
    return np.minimum((e * float(1 << E_BITS)).astype(np.uint64), E_CAP)
def e_quantile(q):
    return min(int(SIG * math.sqrt(-2.0 * math.log(q)) * (1 << E_BITS)), int(E_CAP))

def base_stream(seed, n):
    i4 = np.arange(n, dtype=np.uint64) * np.uint64(4)
    return {  # (p, e, w, t) raw grid values
        "p": P_LO + (at(seed, i4) >> np.uint64(64 - P_BITS)),
        "e": rayleigh_grid(at(seed, i4 + np.uint64(1))),
        "w": at(seed, i4 + np.uint64(2)) >> np.uint64(64 - W_BITS),
        "t": at(seed, i4 + np.uint64(3)) >> np.uint64(64 - T_BITS),
        "we": at(seed, i4 + np.uint64(1)),  # the e word, for table plants
    }

def iid_reference(n, seed):
    rng = np.random.Generator(np.random.PCG64(seed))
    return {"p": P_LO + (rng.integers(0, 1 << P_BITS, n, dtype=np.uint64)),
            "e": rayleigh_grid(rng.integers(0, 1 << 64, n, dtype=np.uint64)),
            "w": rng.integers(0, 1 << W_BITS, n, dtype=np.uint64),
            "t": rng.integers(0, 1 << T_BITS, n, dtype=np.uint64)}

def plant(name, seed, n):
    b = base_stream(seed, n)
    i = np.arange(n, dtype=np.uint64)
    if name == "none": pass
    elif name == "table12":
        tab = np.array([e_quantile(1.0 - (j + 0.5) / 4096.0) for j in range(4096)], dtype=np.uint64)
        b["e"] = tab[(b["we"] >> np.uint64(52)).astype(np.int64)]
    elif name == "table20":
        tab = np.array([e_quantile(1.0 - (j + 0.5) / float(1 << 20)) for j in range(1 << 20)], dtype=np.uint64)
        b["e"] = tab[(b["we"] >> np.uint64(44)).astype(np.int64)]
    elif name == "winsor":
        b["e"] = np.minimum(b["e"], np.uint64(e_quantile(1e-4)))
        b["p"] = np.minimum(b["p"], P_LO + np.uint64(int(0.9999 * (1 << P_BITS))))
    elif name.startswith("crush"):
        f = float(name[5:]) / 100.0; thr = np.uint64(e_quantile(1e-4))
        m = b["e"] > thr
        b["e"] = np.where(m, thr + ((b["e"] - thr) * np.float64(f)).astype(np.uint64), b["e"])
    elif name == "innerclip":
        b["p"] = np.maximum(b["p"], P_LO + np.uint64(int(1e-4 * (1 << P_BITS))))
    elif name == "aligned":
        m = b["e"] > np.uint64(e_quantile(1e-4))
        b["w"] = np.where(m, b["w"] >> np.uint64(27), b["w"])
    elif name == "lattice":
        g = [at(seed, c) | np.uint64(1) for c in range(4)]
        b = {"p": P_LO + ((i * g[0]) >> np.uint64(64 - P_BITS)), "e": rayleigh_grid(i * g[1]),
             "w": (i * g[2]) >> np.uint64(64 - W_BITS), "t": (i * g[3]) >> np.uint64(64 - T_BITS)}
    elif name == "serial":
        prev_t = at(seed, (i - np.uint64(1)) * np.uint64(4) + np.uint64(3)) >> np.uint64(64 - T_BITS)
        m = (i % np.uint64(2) == np.uint64(1)) & (at(seed ^ 0x5E21A1, i) >> np.uint64(61) == np.uint64(0))
        b["t"] = np.where(m, prev_t, b["t"])
    else: raise SystemExit(f"unknown plant {name}")
    return b

def scores(b):
    x_e = (np.minimum(b["e"], E_CAP).astype(np.float64) + 0.5) / float(1 << E_BITS)
    return [(b["p"] - P_LO).astype(np.float64) * 0,  # placeholder, filled below
            ] and [
        ((b["p"] - P_LO).astype(np.float64) + 0.5) / float(1 << P_BITS),
        -np.expm1(-(x_e * x_e) / (2.0 * SIG * SIG)),
        (b["w"].astype(np.float64) + 0.5) / float(1 << W_BITS),
        (b["t"].astype(np.float64) + 0.5) / float(1 << T_BITS)]

LAGS = [1, 2, 3, 4, 5, 6, 7, 8, 16, 32, 64, 128, 256, 512, 1024, 4096, 16384, 65536]
PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
COLS = ["p", "e", "omega", "t_p"]
BINS, SIDE, Z_CHI, Z_SER, KS_C, Z_TAIL, REACH_J = 1 << 16, 128, 4.5, 5.0, 2.470, 4.5, 20

def run_one(name, seed, n, ref, ref_stats):
    b = plant(name, seed, n)
    u = scores(b); x = [c - 0.5 for c in u]
    f = []  # (pass, text)
    h = lambda s, t, ok: f.append((ok, s)) or print(("  ok   " if ok else "  FAIL ") + s + t)
    # exact duplicates on the full state, via a 64-bit mix (false-positive rate ~n^2/2^64)
    hh = mix64(b["p"] ^ mix64(b["e"] ^ mix64(b["w"] ^ mix64(b["t"]))))
    dups = n - np.unique(hh).size
    h("no two bodies share a state", f" ({dups} repeats)", dups == 0)
    # 2-D chi2 on (p, t_p)
    cell = (np.minimum((u[0] * SIDE).astype(np.int64), SIDE - 1)) * SIDE + np.minimum((u[3] * SIDE).astype(np.int64), SIDE - 1)
    cnt = np.bincount(cell, minlength=SIDE * SIDE).astype(np.float64)
    chi2 = ((cnt - n / (SIDE * SIDE)) ** 2 / (n / (SIDE * SIDE))).sum()
    dof = SIDE * SIDE - 1; zchi = (chi2 - dof) / math.sqrt(2 * dof)
    h("2-D chi2 in (p, t_p)", f": z = {zchi:+.2f} (ref {ref_stats['zchi']:+.2f}; limit {Z_CHI})", abs(zchi) <= Z_CHI)
    # serial + cross
    worst = (0.0, "")
    for c in range(4):
        for L in LAGS:
            z = 12.0 * float(np.dot(x[c][L:], x[c][:-L])) / math.sqrt(n - L)
            if abs(z) > worst[0]: worst = (abs(z), f"{COLS[c]} lag {L} z = {z:+.2f}")
    for (a, c) in PAIRS:
        z = 12.0 * float(np.dot(x[a], x[c])) / math.sqrt(n)
        if abs(z) > worst[0]: worst = (abs(z), f"{COLS[a]} x {COLS[c]} z = {z:+.2f}")
    for a in range(4):
        for c in range(4):
            if a != c:
                z = 12.0 * float(np.dot(x[a][1:], x[c][:-1])) / math.sqrt(n - 1)
                if abs(z) > worst[0]: worst = (abs(z), f"{COLS[a]} x prev {COLS[c]} z = {z:+.2f}")
    h("serial and cross correlation", f": worst |z| = {worst[0]:.2f} ({worst[1]}; limit {Z_SER})", worst[0] <= Z_SER)
    # per-column KS vs the reference (2^16-bin quantized, as the judge)
    crit = KS_C * math.sqrt(2.0 / n)
    for c in range(4):
        hb = np.bincount(np.minimum((u[c] * BINS).astype(np.int64), BINS - 1), minlength=BINS)
        D = np.abs(np.cumsum(hb) / n - ref_stats["cum"][c]).max()
        h(f"KS {COLS[c]} vs reference", f": D = {D:.4f} (critical {crit:.4f})", D <= crit)
    # tails of e and p
    k = math.ceil(1e-4 * n)
    for c, cn in [(0, "p"), (1, "e")]:
        top = ref_stats["top"][c]
        thr = top[k - 1]
        vals = b[cn if cn in b else "e"] if False else (b["p"] if c == 0 else b["e"])
        X = int((vals >= thr).sum())
        bt = np.sort(vals[vals >= thr])[::-1]
        reach = len(bt) > 0 and bt[0] >= top[REACH_J - 1]
        over = len(bt) >= REACH_J and bt[REACH_J - 1] <= top[0]
        h(f"tail {cn}: count", f" {X} vs {k} (z = {z:+.2f}, limit {Z_TAIL})", abs(z) <= Z_TAIL)
        h(f"tail {cn}: reaches ref's 20th largest", f" (belt max {bt[0] if len(bt) else 'none'}, ref {top[REACH_J-1]})", reach)
        h(f"tail {cn}: 20th does not pass ref max", f" (belt 20th {bt[REACH_J-1] if len(bt) >= REACH_J else 'n/a'}, ref max {top[0]})", over)
        mine = np.sort(bt)[::-1].astype(np.float64); theirs = top[:k][::-1].astype(np.float64)
        allv = np.concatenate([mine, theirs])
        cdf1 = np.searchsorted(np.sort(mine), allv, side="right") / max(len(mine), 1)
        cdf2 = np.searchsorted(np.sort(theirs), allv, side="right") / len(theirs)
        D = np.abs(cdf1 - cdf2).max()
        dcrit = KS_C * math.sqrt((len(mine) + k) / (max(len(mine), 1) * k))
        h(f"tail {cn}: shape KS", f" D = {D:.3f} vs {dcrit:.3f} ({len(mine)} values)", len(mine) >= 8 and D <= dcrit)
    ok = all(p for p, _ in f)
    print(f"  ==> {name} @ n=2^{int(math.log2(n))} seed {seed}: {'PASS' if ok else 'FAIL'}")
    return ok

def ref_stats_for(n, seed):
    r = iid_reference(n, seed)
    u = scores(r)
    cell = (np.minimum((u[0] * SIDE).astype(np.int64), SIDE - 1)) * SIDE + np.minimum((u[3] * SIDE).astype(np.int64), SIDE - 1)
    cnt = np.bincount(cell, minlength=SIDE * SIDE).astype(np.float64)
    chi2 = ((cnt - n / (SIDE * SIDE)) ** 2 / (n / (SIDE * SIDE))).sum()
    return {"zchi": (chi2 - (SIDE * SIDE - 1)) / math.sqrt(2 * (SIDE * SIDE - 1)),
            "cum": [np.cumsum(np.bincount(np.minimum((c * BINS).astype(np.int64), BINS - 1), minlength=BINS)) / n for c in u],
            "top": [np.sort(r["p"])[::-1].copy(), np.sort(r["e"])[::-1].copy()]}

RUNS = [(20, 20261008), (20, 20261009), (20, 20261010), (23, 20261011)]

if __name__ == "__main__":
    names = sys.argv[1:]
    for name in names:
        gate = True
        for (l2, seed) in RUNS:
            n = 1 << l2
            print(f"--- {name} n=2^{l2} seed {seed}")
            ref = ref_stats_for(n, seed + 12345)
            if not run_one(name, seed, n, ref if False else ref, ref):
                gate = False
                break  # the judge stops at the first failing run
        print(f"=== GATE {name}: {'PASSES' if gate else 'FAILS'}\n")
