#!/usr/bin/env python3
"""Falsification sweep for prediction 2 (re-fit residual).

Q: is the re-fit residual's growth (2.25 -> 6.32 bits over 8192 orbits at m=256) real
information, or the quantile table's resolution in the spreading tails?
If it is resolution, bits/body(m) = resid(m) + 32m/N must fall toward ~2 as m grows,
with program cost still negligible. Control: r=0 (no encounter jumps) isolates the
diffusion-only constants of predictions 1 and 3.

Run: python3 sweep.py     (~2.5 min)
"""
import json
import numpy as np

N = 1 << 20
rng = np.random.default_rng(7)

def H(c):
    c = c[c > 0].astype(np.float64)
    n = c.sum()
    return float(np.log2(n) - (c * np.log2(c)).sum() / n)

def ent_of(v):
    v = np.asarray(v, dtype=np.int64)
    return H(np.bincount(v - v.min()))

def knots_program(xs, m):
    idx = (np.arange(m + 1) * (len(xs) - 1)) // m
    ranks = np.arange(len(xs), dtype=np.float64)
    return np.rint(np.interp(ranks, idx.astype(np.float64),
                             xs[idx].astype(np.float64))).astype(np.int64)

def evolve(s, J, r, T):
    x0 = ((np.arange(N, dtype=np.float64) + 0.5)).astype(np.int32)
    x = x0.copy()
    B, t = 32, 1
    while t <= T:
        nb = min(B, T - t + 1)
        d = np.rint(rng.standard_normal((nb, N), dtype=np.float32) * s)
        hit = rng.random((nb, N)) < r
        fi = np.nonzero(hit.ravel())[0]
        if fi.size:
            d.ravel()[fi] += np.rint(rng.standard_normal(fi.size,
                                                         dtype=np.float32) * J)
        for i in range(nb):
            x += d[i].astype(np.int32)
        t += nb
    return x0, x

out = {"with_jumps": {}, "no_jump_control": {}}

# 1) m-sweep on the jumped trajectory (s=1, J=100, r=r8 belt), T=4096
R_ENC = 427.0 / (1e4 * 20.0)
x0, x = evolve(1.0, 100.0, R_ENC, 4096)
order = np.argsort(x, kind="stable")
xs = x[order].astype(np.int64)
for m in (256, 1024, 4096, 16384):
    resid = ent_of(xs - knots_program(xs, m))
    prog_bits_per_body = 32.0 * m / N
    out["with_jumps"][m] = {"resid_bits": resid,
                            "program_bits_per_body": prog_bits_per_body,
                            "total": resid + prog_bits_per_body}
    print(f"m={m:6d}  resid={resid:6.2f}  program={prog_bits_per_body:.4f}  "
          f"total={resid + prog_bits_per_body:6.2f} bits/body")

# 2) no-jump control (r=0): diffusion-only frozen scar and label entropy at T=8192
x0c, xc = evolve(1.0, 0.0, 0.0, 8192)
frozen = ent_of(xc.astype(np.int64) - x0c.astype(np.int64))
order = np.argsort(xc, kind="stable")
ranks = np.empty(N, dtype=np.int64)
ranks[order] = np.arange(N, dtype=np.int64)
label = ent_of(ranks - np.arange(N, dtype=np.int64))
print(f"\nno-jump control, s=1, T=8192: frozen={frozen:.2f} "
      f"(pred 1: 8.55)  label={label:.2f} (pred 3 formula: 9.05)")
out["no_jump_control"] = {"frozen_bits": frozen, "label_bits": label}

with open("sweep.json", "w") as f:
    json.dump(out, f, indent=1)
