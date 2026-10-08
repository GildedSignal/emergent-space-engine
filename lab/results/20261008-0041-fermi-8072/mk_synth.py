"""Build the synthetic 'program' belt from a true state: the shuffle test's D.

Program family (B18b-style + refit): a from a smoothed histogram (gaps included),
e from per-band empirical, angles uniform (phases decohered). Fresh PRNG ordinals.
"""
import sys
import numpy as np
import belt

src, dst, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
s = np.load(src)
x, y, vx, vy, t = s["x"], s["y"], s["vx"], s["vy"], float(s["t"])
r = np.hypot(x, y); v2 = vx * vx + vy * vy; rv = x * vx + y * vy
a = 1.0 / (2.0 / r - v2)
exv = (v2 - 1.0 / r) * x - rv * vx
eyv = (v2 - 1.0 / r) * y - rv * vy
e = np.hypot(exv, eyv)
n = len(a)
rng = np.random.default_rng(seed)

# a: smoothed histogram resample (bin 0.01 AU, Gaussian smooth sigma=3 bins)
lo, hi, bw = 1.8, 4.4, 0.01
nb = int((hi - lo) / bw)
hist, edges = np.histogram(a, bins=nb, range=(lo, hi))
k = np.exp(-0.5 * (np.arange(-6, 7) / 3.0) ** 2); k /= k.sum()
hist = np.convolve(hist.astype(float), k, mode="same"); hist[hist < 0] = 0
pa = hist / hist.sum()
a_new = lo + (np.searchsorted(np.cumsum(pa), rng.random(n)) + rng.random(n)) * bw

# e: per-band empirical resample + kernel jitter (sigma ~ quantum of fit)
bands = np.clip(((a_new - lo) / 0.2).astype(int), 0, 12)
e_new = np.empty(n)
for b in np.unique(bands):
    m = bands == b
    pool = e[(a >= lo + 0.2 * b) & (a < lo + 0.2 * (b + 1))]
    if len(pool) < 5:
        pool = e
    e_new[m] = pool[rng.integers(0, len(pool), m.sum())] + rng.normal(0, 0.003, m.sum())
e_new = np.clip(e_new, 0, None)

w_new = rng.uniform(0, 2 * np.pi, n)
M_new = rng.uniform(0, 2 * np.pi, n)
x2, y2, vx2, vy2 = belt.elements_to_state(a_new, e_new, w_new, M_new)
np.savez(dst, x=x2, y=y2, vx=vx2, vy=vy2, t=t)
print(f"synthetic {dst}: n={n} t={t:.0f} a[{a_new.min():.2f},{a_new.max():.2f}] "
      f"e mean {e_new.mean():.3f} (true {e.mean():.3f})")
