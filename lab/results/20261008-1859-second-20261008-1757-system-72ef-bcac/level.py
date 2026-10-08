#!/usr/bin/env python3
"""Wall-free level measurement for the scar store (second author run).

The shipped `scars.py` instrument (plug-in entropy over N bodies at quantum q)
is capped at log2(N) bits per channel: at N = 1e4 no channel can read above
13.29 bits, so the original run's "saturation level ~64 bits" is the wall, not
the physics (checker, 20261008-1757).

Replacement instrument — a two-part population code, i.e. what a real store
would ship at 1e9 bodies:
  * a shared table: a k-bin histogram of the population (model cost reported
    separately, amortised to ~0 at 1e9);
  * per body: the bin index coded under the table (cost = plug-in entropy of
    the coarse histogram, which is far below ITS log2(k) cap for k = 256),
    plus the exact within-bin offset at quantum q as fractional bits
    log2(binwidth/q). The q-resolution never becomes distinct symbols, so the
    sample-size wall is gone.

Controls: wrapped-uniform (analytic log2(2*pi/q)) and Gaussian (analytic
h + log2(1/q)); the old plug-in estimator is run on the same data as a
negative control (it must read the wall).
"""
import json
import sys

import numpy as np

TAU = 2.0 * np.pi


def wrap(x):
    return (x + np.pi) % TAU - np.pi


def _bins(v, k, q, circle):
    """Bin edges and clipped indices for a 1D channel."""
    if circle:
        lo, hi = -np.pi, np.pi
    else:
        lo, hi = float(v.min()), float(v.max())
        span = hi - lo
        lo -= 0.01 * span + 1e-300
        hi += 0.01 * span + 1e-300
    # never bin below the quantum: then the histogram IS the symbol set
    k = max(1, min(k, int((hi - lo) / q)))
    w = (hi - lo) / k
    idx = np.clip(((v - lo) / w).astype(np.int64), 0, k - 1)
    return idx, k, w


def level_bits_1d(v, q, k=256, circle=False):
    """Bits/body for one channel at quantum q, wall-free. Returns
    (bits, n_bins, bin_width)."""
    v = np.asarray(v, float)
    idx, k, w = _bins(v, k, q, circle)
    cnt = np.bincount(idx, minlength=k).astype(np.float64)
    p = cnt / cnt.sum()
    p = p[p > 0]
    h_bin = float(-(p * np.log2(p)).sum())
    return h_bin + np.log2(w / q), k, w


def level_bits_2d(vx, vy, q, k=64):
    """Bits/body for two channels coded jointly at quantum q."""
    vx, vy = np.asarray(vx, float), np.asarray(vy, float)
    kx = max(1, min(k, int((vx.max() - vx.min()) / q)))
    ky = max(1, min(k, int((vy.max() - vy.min()) / q)))
    wx = (vx.max() - vx.min() + 2e-300) / kx
    wy = (vy.max() - vy.min() + 2e-300) / ky
    ix = np.clip(((vx - vx.min()) / wx).astype(np.int64), 0, kx - 1)
    iy = np.clip(((vy - vy.min()) / wy).astype(np.int64), 0, ky - 1)
    joint = np.bincount(ix * ky + iy, minlength=kx * ky).astype(np.float64)
    p = joint / joint.sum()
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum()) + np.log2(wx / q) + np.log2(wy / q)


def heldout_bits_1d(fit_v, code_v, q, k=256, circle=False):
    """Table fitted on fit_v, code length measured on held-out code_v."""
    fit_v, code_v = np.asarray(fit_v, float), np.asarray(code_v, float)
    if circle:
        lo, hi = -np.pi, np.pi
    else:
        lo, hi = float(fit_v.min()), float(fit_v.max())
        span = hi - lo
        lo -= 0.01 * span + 1e-300
        hi += 0.01 * span + 1e-300
    k = max(1, min(k, int((hi - lo) / q)))
    w = (hi - lo) / k
    cnt = np.bincount(np.clip(((fit_v - lo) / w).astype(np.int64), 0, k - 1),
                      minlength=k)
    p = (cnt + 0.5) / (cnt.sum() + 0.5 * k)   # Krichevsky-Trofimov, codeable
    idx = np.clip(((code_v - lo) / w).astype(np.int64), 0, k - 1)
    cross = -np.log2(p[idx]).mean()
    over = (code_v < lo) | (code_v > hi)
    if over.any():  # escape code: log2(1/pmin) + uniform range bits
        r = np.log2((hi - lo) / q) + 20.0
        cross = cross * (1 - over.mean()) + over.mean() * r
    return float(cross + np.log2(w / q)), int(over.mean())


def plugin_bits(v, q):
    """The original shipped estimator (kept as the negative control)."""
    codes = np.round(np.asarray(v, float) / q).astype(np.int64)
    _, cnt = np.unique(codes, return_counts=True)
    p = cnt / cnt.sum()
    return float(-(p * np.log2(p)).sum())


CHANNELS = ("da_rel", "dh", "dk", "dvarpi", "dlambda")
CIRCLE = {"dvarpi": True, "dlambda": True}


def channel_levels(d, q, k=256, with_joint=True):
    out = {}
    for ch in CHANNELS:
        out[ch] = level_bits_1d(d[ch], q, k, CIRCLE.get(ch, False))[0]
    if with_joint:
        out["joint_hk"] = level_bits_2d(d["dh"], d["dk"], q)
        out["MI_hk"] = out["dh"] + out["dk"] - out["joint_hk"]
    return out


def model_cost_bits(N, k=256):
    """Two-part code model cost: k bin probabilities, KT-coded counts."""
    return k * (np.log2(N + k / 2) - np.log2(k / 2)) / N


def controls(seed=20261008):
    rng = np.random.default_rng(seed)
    q = 1e-6
    N = 10000
    uni = rng.uniform(-np.pi, np.pi, N)
    gau = rng.normal(0.0, 0.01, N)
    u_true = np.log2(TAU / q)
    g_true = 0.5 * np.log2(2 * np.pi * np.e * 0.01 ** 2) + np.log2(1 / q)
    res = {
        "q": q, "N": N,
        "uniform_true": u_true,
        "uniform_level": level_bits_1d(uni, q, 256, True)[0],
        "uniform_plugin": plugin_bits(uni, q),
        "gauss_true": g_true,
        "gauss_level": level_bits_1d(gau, q, 256, False)[0],
        "gauss_plugin": plugin_bits(gau, q),
        "wall": np.log2(N),
    }
    for kk in (128, 512, 1024):
        res[f"gauss_level_k{kk}"] = level_bits_1d(gau, q, kk, False)[0]
        res[f"uniform_level_k{kk}"] = level_bits_1d(uni, q, kk, True)[0]
    return res


def stored(npz_path):
    d = dict(np.load(npz_path))
    N = len(d["da_rel"])
    res = {"npz": npz_path, "N": N,
           "model_cost_bits_per_body_at_1e9": model_cost_bits(10 ** 9),
           "model_cost_bits_per_body_here": model_cost_bits(N)}
    for q in (1e-3, 1e-4, 1e-5, 1e-6, 1e-7):
        res[f"q={q:g}"] = channel_levels(d, q)
    # headline decomposition at q = 1e-6 with per-channel detail
    q = 1e-6
    det = {}
    for ch in CHANNELS:
        b, k, w = level_bits_1d(d[ch], q, 256, CIRCLE.get(ch, False))
        det[ch] = {"level_bits": b, "n_bins": k, "bin_width": w,
                   "plugin": plugin_bits(d[ch], q),
                   "wall": float(np.log2(N))}
    det["joint_hk"] = {"level_bits": level_bits_2d(d["dh"], d["dk"], q)}
    res["detail_q1e-6"] = det
    # 8 GiB pricing at 1e9 bodies (genesis program 0.126 bits/body, H0203 gold)
    budget = 8 * 2 ** 33 / 1e9 - 0.126
    res["budget_bits_per_body"] = budget
    for label, chans in (("raw5", CHANNELS),
                         ("joint_hk", ("da_rel", "joint_hk", "dvarpi",
                                       "dlambda"))):
        qs = np.array([1e-3, 1e-4, 1e-5, 1e-6, 1e-7])
        lv = np.array([sum(res[f"q={q:g}"][c] for c in chans) for q in qs])
        res[f"level_{label}"] = dict(zip(map(lambda x: f"{x:g}", qs),
                                         lv.round(2)))
        # solve level(q) = budget by log-linear fit (slope should be ~5)
        A = np.vstack([np.log10(qs), np.ones_like(qs)]).T
        slope, icept = np.linalg.lstsq(A, lv, rcond=None)[0]
        q_star = 10 ** ((budget - icept) / slope)
        res[f"q_star_{label}"] = {"q_star": float(q_star),
                                  "bits_per_decade": float(slope)}
        res[f"gib_{label}_at_1e-6"] = float(lv[-2] * 1e9 / 2 ** 33)
        res[f"gib_{label}_at_qstar"] = float(
            sum(res[f"q={q_star:g}"][c] for c in chans) * 1e9 / 2 ** 33) \
            if f"q={q_star:g}" in res else None
    return res


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "controls"
    if mode == "controls":
        print(json.dumps(controls(), indent=1))
    elif mode == "stored":
        print(json.dumps(stored(sys.argv[2]), indent=1))
