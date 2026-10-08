import numpy as np, os
from runs import make_scene, truth_with_series, cadence_with_series, OUT
mu, T = 1e-3, 150
a0, e0, w0, M0 = make_scene(mu, 0.02, 7)
tr = truth_with_series(a0, e0, w0, M0, mu, T, 1024)
out = dict(a0=a0, e0=e0, truth=dict(a=tr["a"], e=tr["e"], w_tot=tr["w_tot"], maxdc=tr["maxdc"], dmin=tr["dmin"]))
print("truth done %.0fs" % tr["wall"], flush=True)
for k in [2, 4, 8, 16, 32, 64]:
    c = cadence_with_series(a0, e0, w0, M0, mu, T, np.full(a0.size, k))
    out[f"k{k}"] = dict(maxdc=c["maxdc"], a=c["a"], e=c["e"], w_tot=c["w_tot"], nkicks=c["nkicks"])
    print("k=%d med=%.1e p95=%.1e" % (k, np.median(c["maxdc"]), np.quantile(c["maxdc"], .95)), flush=True)
flat = {}
for k, v in out.items():
    if isinstance(v, dict):
        for kk, vv in v.items():
            flat[f"{k}_{kk}"] = np.asarray(vv, float)
    else:
        flat[k] = np.asarray(v, float)
np.savez_compressed(os.path.join(OUT, "backup.npz"), **flat)
print("saved", flush=True)
