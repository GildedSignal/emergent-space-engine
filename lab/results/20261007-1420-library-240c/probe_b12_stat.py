#!/usr/bin/env python3
"""B12 statistic probe: does the variogram/Allan slope separate bounded from
compounding error where the median-seed growth exponent does not?
Cases and predictions pre-registered in predictions.md (written before this ran)."""
import numpy as np

N = 2048
NSEED = 16
KS = np.array([8, 16, 32, 64, 128, 256, 512])  # dyadic lags (crossings)

def bounded_white(rng, n=N):
    t = np.arange(n)
    return 1e-6 * np.sin(2 * np.pi * t * 10 / n) + 1e-7 * rng.standard_normal(n)

def bounded_chaotic(rng, n=N):
    x = rng.uniform(0.1, 0.9)
    out = np.empty(n)
    for i in range(n):
        x = 4.0 * x * (1.0 - x)
        out[i] = 1e-6 * (2 * x - 1)
    return out

def leak_rw(rng, n=N):
    return np.cumsum(2.2e-8 * rng.standard_normal(n))

def leak_slow(rng, n=N):
    return 1e-7 * np.sin(2 * np.pi * np.arange(n) * 10 / n) + np.cumsum(2.2e-8 * rng.standard_normal(n))

def drift(rng, n=N):
    return 1e-6 * np.arange(n) / n

def leak_tiny(rng, n=N):
    return 1e-6 * np.sin(2 * np.pi * np.arange(n) * 10 / n) + np.cumsum(2.2e-10 * rng.standard_normal(n))

def expo(e):
    """Current-gate shape: OLS slope of log running-max|e| vs log t (t from 16)."""
    t = np.arange(1, len(e) + 1)
    m = np.maximum.accumulate(np.abs(e))
    sel = (t >= 16) & (m > 0)
    return np.polyfit(np.log(t[sel]), np.log(m[sel]), 1)[0]

def vario_slope(e):
    g = [np.mean((e[k:] - e[:-k]) ** 2) for k in KS]
    return np.polyfit(np.log(KS), np.log(g), 1)[0]

def allan_slope(e):
    sig = []
    n = len(e)
    for tau in KS:
        cs = np.concatenate(([0.0], np.cumsum(e)))
        m = (cs[tau:] - cs[:-tau]) / tau          # sliding tau-averages, every offset
        d = m[tau:] - m[:-tau]                     # overlap-tau difference, all starts
        sig.append(np.sqrt(0.5 * np.mean(d * d)))  # overlapping Allan deviation
    sig = np.array(sig)
    return np.polyfit(np.log(KS), np.log(sig), 1)[0]

CASES = {"bounded-white": bounded_white, "bounded-chaotic": bounded_chaotic,
         "leak-rw": leak_rw, "leak-slow": leak_slow, "drift": drift, "leak-tiny": leak_tiny}

rng_master = np.random.default_rng(0)
rows = {}
for name, fn in CASES.items():
    E = np.array([fn(np.random.default_rng(1000 + s)) for s in range(NSEED)])
    rows[name] = {
        "expo": np.array([expo(e) for e in E]),
        "vario": np.array([vario_slope(e) for e in E]),
        "allan": np.array([allan_slope(e) for e in E]),
    }

def band_v(v):  # variogram bands (predictions P1)
    return "bounded" if v <= 0.3 else ("leak-rw" if 0.7 <= v <= 1.3 else ("drift" if v >= 1.7 else "ambiguous"))

def band_a(a):  # allan bands: half the variogram values
    return "bounded" if a <= 0.15 else ("leak-rw" if 0.35 <= a <= 0.65 else ("drift" if a >= 0.85 else "ambiguous"))

print(f"{'case':16s} {'stat':6s} {'min':>7s} {'median':>7s} {'max':>7s}   bands(seed majority)")
print("-" * 78)
for name, r in rows.items():
    for st in ("expo", "vario", "allan"):
        v = r[st]
        band = band_v if st == "vario" else (band_a if st == "allan" else (lambda x: f"expo {x:.2f}"))
        from collections import Counter
        bs = Counter(band(x) for x in v)
        print(f"{name:16s} {st:6s} {v.min():7.3f} {np.median(v):7.3f} {v.max():7.3f}   {dict(bs)}")

# P2: the fleet — 15 chaotic-bounded + 1 slow leak; current rule = median-seed expo <= 0.2
E = [bounded_chaotic(np.random.default_rng(100 + s)) for s in range(15)]
E.append(leak_slow(np.random.default_rng(100)))
expo_seeds = np.array([expo(e) for e in E]); vario_seeds = np.array([vario_slope(e) for e in E])
allan_seeds = np.array([allan_slope(e) for e in E])
print("\nfleet-16: median-seed expo = %.3f -> current gate %s" %
      (np.median(expo_seeds), "PASSES (leak certified)" if np.median(expo_seeds) <= 0.2 else "fails"))
print("fleet-16: worst-seed vario = %.3f / allan = %.3f (both seed %d) -> tail rule %s" %
      (vario_seeds.max(), allan_seeds.max(), int(np.argmax(vario_seeds)),
       "FLAGS the leak" if (vario_seeds.max() >= 0.7 or allan_seeds.max() >= 0.35) else "clear"))

# P3: inversion count — seeds where expo(chaotic) > expo(leak-slow)
inv = int(np.sum(rows["bounded-chaotic"]["expo"][:, None] > rows["leak-slow"]["expo"][None, :]))
print("\nP3 inversions (chaotic expo > leak-slow expo, pairwise): %d / %d" % (inv, NSEED * NSEED))

# P4: controls
fp = int(np.sum(rows["bounded-chaotic"]["vario"] > 0.3))
fn = int(np.sum(rows["leak-rw"]["vario"] < 0.7))
print("P4 controls: chaotic-bounded false leaks: %d/16 ; leak-rw misses: %d/16" % (fp, fn))

# P5: stability at N=4096 for two cases
for nm, fn in (("leak-rw", leak_rw), ("bounded-chaotic", bounded_chaotic)):
    v2 = np.median([vario_slope(fn(np.random.default_rng(2000 + s), 4096)) for s in range(8)])
    print("P5 %s vario slope at N=4096: %.3f (N=2048 median %.3f)" % (nm, v2, np.median(rows[nm]["vario"])))
