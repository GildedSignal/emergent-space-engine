"""Dense all-pairs cross-check of the pipeline's contact set (n=64 deep jam)."""
import numpy as np, probe
rng = np.random.default_rng(27)
n, e0, esig, sig_M = 64, 0.0, 0.001, 0.002
e = e0 + probe.rayleigh(n, esig, rng)
pi = rng.uniform(-0.1, 0.1, n)
M0 = rng.normal(0, sig_M, n) % probe.TWO_PI
Sd = 65536
dmin = np.full((n, n), np.inf)
for c0 in range(0, Sd, 1024):
    c1 = c0 + 1024
    Mc = M0[None, :] + (np.arange(c0, c1) * (probe.TWO_PI / Sd))[:, None]
    x, y, r, lam, _ = probe.positions(Mc, np.broadcast_to(e, Mc.shape), np.broadcast_to(pi, Mc.shape))
    for a in range(n):
        d = np.hypot(x - x[:, a:a+1], y - y[:, a:a+1])
        np.minimum(dmin[a], d.min(axis=0), out=dmin[a])
dense = {(i, j): dmin[i, j] for i in range(n) for j in range(i+1, n) if dmin[i, j] < probe.RHO}
# pipeline on same scene (shift M0 into the pipeline's sampling by using M0 as given: emulate via sig_M sampling with same rng draw)
import types
res = probe.run_scene("verify", n, e0, esig, sig_M, seed=27)
print("dense contacts:", len(dense), "pipeline contacts:", res["contacts"])
