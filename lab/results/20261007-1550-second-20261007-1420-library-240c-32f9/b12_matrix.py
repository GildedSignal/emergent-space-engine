#!/usr/bin/env python3
"""The decisive experiment (checker-named): the B12 classification matrix at the gate's real
conditions — the dumped real series (plane + the gate's control laws on the frozen chaotic
ships, N=1601) against the frozen triple (N=1601, theta=0.10, min-detectable-leak stated),
worst-seed verdict — plus the checker's adversarials re-run at N=1601.
Allan/vario estimators are the previous run's, verbatim (probe_b12_stat.py, 20261007-1420)."""
import numpy as np

FLOOR = 1e-12
THETA = 0.10          # pre-registered threshold (predictions.md)
KS = np.array([8, 16, 32, 64, 128, 256, 512])
N = 1601

def allan_slope(e):
    sig = []
    for tau in KS:
        cs = np.concatenate(([0.0], np.cumsum(e)))
        m = (cs[tau:] - cs[:-tau]) / tau
        d = m[tau:] - m[:-tau]
        sig.append(np.sqrt(0.5 * np.mean(d * d)))
    return np.polyfit(np.log(KS), np.log(sig), 1)[0]

def load(name):
    rows = []
    for line in open(f"b12dump/series_{name}.tsv"):
        vals = [float(x) for x in line.split()]
        if vals:
            rows.append(np.array(vals))
    return rows

def pership(name):
    out = []
    for line in open(f"b12dump/series_pership_{name}.tsv"):
        f = line.split()
        if f:
            out.append((f[1] == "true", float(f[2]), float(f[3])))
    return out

print("=== the matrix: real series, worst-seed verdict (theta=%.2f, floor=%.0e) ===" % (THETA, FLOOR))
print(f"{'law':18} {'judged':>6} {'lost':>4} {'slope min':>9} {'median':>7} {'max':>7} {'exp min..max':>16}  verdict")
print("-" * 100)
bounded_max, leak_min = -np.inf, np.inf
for name, kind in [("echo", "bounded"), ("scaled1e_11", "bounded"), ("planted_bounded", "bounded"),
                   ("planted_compound", "leak"), ("planted_drift", "leak"), ("leak_per_period", "leak"),
                   ("plane", "real")]:
    rows = load(name)
    ps = pership(name)
    lost = sum(1 for a, _, _ in ps if not a)
    judged = [(e, x) for (a, top, x), e in zip(ps, rows) if a and top > FLOOR]
    slopes = np.array([allan_slope(e) for e, _ in judged])
    expos = np.array([x for _, x in judged])
    if lost:
        verdict = "FAIL (loses %d ships: no answer)" % lost
        if slopes.size:
            verdict += "; answered ships: %s" % ("leak" if slopes.max() > THETA else "bounded")
    elif not judged:
        verdict = "PASS (all under floor: not judged)"
    else:
        verdict = "LEAK->FAIL" if slopes.max() > THETA else "PASS (bounded)"
    if kind != "real" and judged:
        if kind == "bounded":
            bounded_max = max(bounded_max, slopes.max())
        else:
            leak_min = min(leak_min, slopes.min())
    if slopes.size:
        print(f"{name:18} {len(judged):>6} {lost:>4} {slopes.min():>9.3f} {np.median(slopes):>7.3f} {slopes.max():>7.3f} "
              f"{expos.min():>7.3f}..{expos.max():<7.3f}  {verdict}")
    else:
        einfo = "" if not expos.size else f"{expos.min():>7.3f}..{expos.max():<7.3f}  "
        print(f"{name:18} {len(judged):>6} {lost:>4} {'--':>9} {'--':>7} {'--':>7} {einfo} {verdict}")
    if name == "echo":
        es = np.array([allan_slope(e) for e in load("echo")])
        print(f"{'  (echo slopes':18} {'':>6} {'':>4} {es.min():>9.3f} {np.median(es):>7.3f} {es.max():>7.3f} {'':>16}  not judged: under floor")
print("\ndead band: bounded max %.3f  leak min %.3f  gap %.3f" % (bounded_max, leak_min, leak_min - bounded_max))

# P2: per-seed interleaving, exponent vs Allan
pb, pc = np.array([x for a, t, x in pership("planted_bounded") if a]), np.array([x for a, t, x in pership("planted_compound") if a])
inv = int(np.sum(pb[:, None] > pc[None, :]))
spb = np.array([allan_slope(e) for e in load("planted_bounded")])
spc = np.array([allan_slope(e) for e in load("planted_compound")])
inva = int(np.sum(spb[:, None] > spc[None, :]))
print("P2 per-seed: exponent inversions (bounded>compound) %d/%d ; Allan inversions %d/%d" % (inv, pb.size * pc.size, inva, spb.size * spc.size))

rng = np.random.default_rng(7)
print("\n=== adversarials at N=%d (theta=%.2f) ===" % (N, THETA))
# slow bounded oscillation: p periods per scene, 16 phases
for p in (1, 2, 3, 4, 8):
    sl = [allan_slope(1e-6 * np.sin(2 * np.pi * (np.arange(N) / N) * p + ph)) for ph in rng.uniform(0, 6.28, 16)]
    sl = np.array(sl)
    print("sine %d period(s)/scene: slope min %.3f median %.3f max %.3f -> false leaks %2d/16" % (p, sl.min(), np.median(sl), sl.max(), int((sl > THETA).sum())))
# AR(1)
for rho in (0.9, 0.99):
    sl = []
    for s in range(16):
        z = np.random.default_rng(30000 + s).standard_normal(N)
        x = np.zeros(N)
        for i in range(1, N):
            x[i] = rho * x[i - 1] + z[i]
        x *= 1e-9 / x.std()
        sl.append(allan_slope(x))
    sl = np.array(sl)
    print("AR(1) rho=%.2f (std 1e-9): slope min %.3f median %.3f max %.3f -> flagged leak %2d/16" % (rho, sl.min(), np.median(sl), sl.max(), int((sl > THETA).sum())))

# min-detectable-leak: leak-rw on top of the REAL bounded scaled1e-11 series (14 real chaotic bases)
base = load("scaled1e_11")
print("\nmin-detectable-leak ladder (leak-rw added to the 14 real scaled1e-11 series; end magnitude / floor):")
for k in (0.5, 1, 2, 3, 4, 8, 16):
    det, ends, mins = 0, [], []
    for s in range(16):
        for b in base:
            sig = k * FLOOR / (0.674 * np.sqrt(N))
            leak = np.cumsum(sig * np.random.default_rng(40000 + s).standard_normal(N))
            ends.append(np.median(np.abs(leak)) / FLOOR)
            sl = allan_slope(b + leak)
            mins.append(sl)
            det += sl > THETA
    print("  k=%4.1f (median end %.2f x floor): flagged %3d/%3d  min slope %.3f" % (k, np.median(ends), det, 16 * len(base), np.min(mins)))

# N-min note: the gate's N is 1601; leak detection per-seed at this N for the real leak laws
print("\nN check: gate N=%d >= 256 (previous run: per-seed misses only below N=256)" % N)
