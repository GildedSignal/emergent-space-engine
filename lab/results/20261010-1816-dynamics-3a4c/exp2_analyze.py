#!/usr/bin/env python3
"""Exp2 analysis: P7 (excitation), P8 (cadence bites in NEAR only), P9."""
import numpy as np

FLOORS = dict(rel=(0.10, 0.15, 0.10), abs=(2e-3, 1.5e-3, 3e-3))


def scal(e):
    return e.mean(0), e.std(0), e.max(0)


res = {}
for tag in ("near", "far"):
    d = np.load(f"out_exp2_{tag}.npz")
    keys = sorted([k for k in d.files if k.startswith("e")], key=lambda k: int(k[1:]))
    mt, st, xt = scal(d[keys[-1]])
    kstar = np.full(len(mt), -1, int)
    for k in keys:
        K = int(k[1:]); m, s, x = scal(d[k])
        ok = ((np.abs(m - mt) / np.maximum(.1 * mt, 2e-3)) <= 1) & \
             ((np.abs(s - st) / np.maximum(.15 * st, 1.5e-3)) <= 1) & \
             ((np.abs(x - xt) / np.maximum(.1 * xt, 3e-3)) <= 1)
        kstar = np.where((kstar < 0) & ok, K, kstar)
    res[tag] = (kstar, st, mt, xt, keys[-1])
    print(f"{tag}: e_std med {np.median(st):.5f} p90 {np.percentile(st,90):.5f} "
          f"max {st.max():.5f}; e_mean med {np.median(mt):.4f} max {mt.max():.3f}")
    print(f"{tag}: K* hist {[(int(K), int((kstar==K).sum())) for K in np.unique(kstar)]}, "
          f"never-sufficient {(kstar<0).sum()}")

kn, sn, mn, xn, tn = res["near"]; kf, sf, mf, xf, tf = res["far"]
uni = 256 * 500
sched = int(kn.sum()) + int(kf.sum()) + int(256 * ((kn < 0).sum() + (kf < 0).sum()))
print(f"P8 pooled: uniform(256)/scheduled = {uni/sched:.1f}x "
      f"(near median K* {np.median(kn[kn>0]) if (kn>0).any() else -1:.0f}, "
      f"far median K* {np.median(kf[kf>0]) if (kf>0).any() else -1:.0f})")
b = np.load("out_exp2_birth.npz")
pool_k = np.concatenate([kn, kf]); pool_z = np.concatenate([b["zeta_near"], b["zeta_far"]])
need = pool_k >= 16
print(f"P9: bodies needing K*>=16: {need.sum()}, of which zeta below pooled median: "
      f"{(pool_z[need] < np.median(pool_z)).mean()*100 if need.sum() else float('nan'):.0f}%")
