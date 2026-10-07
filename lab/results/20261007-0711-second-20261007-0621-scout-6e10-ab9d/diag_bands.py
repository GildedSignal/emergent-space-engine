#!/usr/bin/env python3
"""Diagnostic: per-band program fits (post-hoc, not pre-registered).
Where does the synodic program's residual live, and what would per-band
(per-population) event programs buy? -> diag_bands.json"""
import json

import numpy as np

src = open('real_kick_ledger.py').read()
exec(src.split('if MODE == "control"')[0])
h0, k0 = e0 * np.cos(w0), e0 * np.sin(w0)
s = np.load("int.npz")
dz = (s["hT"] - h0) + 1j * (s["kT"] - k0)
Q24 = 0.6 * 2.0 ** -24


def dh(r, q):
    sd = float(np.std(r))
    return 0.0 if sd <= 0 else max(0.0, float(np.log2(sd * np.sqrt(2 * np.pi * np.e) / q)))


def fit(X, rh, rk):
    c, *_ = np.linalg.lstsq(X, np.column_stack([rh, rk]), rcond=None)
    r = np.column_stack([rh, rk]) - X @ c
    return r[:, 0], r[:, 1]


def H(rh, rk):
    return dh(rh, Q24) + dh(rk, Q24)


def syn(idx):
    tm_all = (0.0 - lam0[idx] + C2PI * np.arange(10)[:, None]) / (n[idx] - NJ)[None, :]
    cols = []
    for m in range(10):
        tm = tm_all[m]
        mask = ((tm > 0) & (tm < T_win[idx])).astype(float)
        base = np.exp(1j * (lam0[idx] + n[idx] * tm)) * mask
        for w in (1.0 + 0j, np.exp(1j * w0[idx]), np.exp(-1j * w0[idx]), e0[idx] + 0j):
            cols.append(np.column_stack([(base * w).real, (base * w).imag]))
    return np.column_stack(cols)


out = {}
for i, idx in enumerate(np.array_split(np.argsort(a), 3)):
    Xs = syn(idx)
    rs, ks = fit(Xs, dz.real[idx], dz.imag[idx])
    Hk = H(dz.real[idx], dz.imag[idx])
    out[f"third{i}_a{a[idx].mean():.2f}"] = dict(
        kick_bits=round(Hk, 2), syn_bits=round(H(rs, ks), 2),
        kick_sd=round(float(dz.real[idx].std()), 5),
        resid_sd=round(float(rs.std()), 5),
        recaptured=round(1 - H(rs, ks) / Hk, 3))
loe = e0 < 0.07
Xs = syn(loe)
rs, ks = fit(Xs, dz.real[loe], dz.imag[loe])
Hk = H(dz.real[loe], dz.imag[loe])
out["low_e"] = dict(n=int(loe.sum()), kick_bits=round(Hk, 2),
                    syn_bits=round(H(rs, ks), 2), recaptured=round(1 - H(rs, ks) / Hk, 3))
print(json.dumps(out, indent=1))
with open("diag_bands.json", "w") as f:
    json.dump(out, f, indent=1)
