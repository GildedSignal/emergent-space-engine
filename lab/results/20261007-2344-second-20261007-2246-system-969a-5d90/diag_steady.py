#!/usr/bin/env python3
"""Diagnose the steady-scene miss: rebuild the exact Rust scene (Rng port), run the
author's key_cells/widened_u/interval_pairs verbatim, and check membership of the
Rust-dumped missed pairs. Also: per-body window-vs-true-annulus soundness margin."""
import sys
import numpy as np

MASK = (1 << 64) - 1

class Rng:
    def __init__(s, seed): s.x = seed & MASK
    def next_u64(s):
        s.x = (s.x + 0x9E3779B97F4A7C15) & MASK
        z = s.x
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK
        return (z ^ (z >> 31)) & MASK
    def f64(s): return (s.next_u64() >> 11) / 9007199254740992.0

def steady_scene(n=3000, seed=20261013):
    rng = Rng(seed)
    a = np.empty(n); e = np.empty(n); pom = np.empty(n); lam = np.empty(n)
    for k in range(n):
        a[k] = 1.0 + 0.5 * rng.f64()
        e[k] = min(0.01 * np.sqrt(-2.0 * np.log(1.0 - rng.f64())), 0.5)
        pom[k] = 2 * np.pi * rng.f64()
        lam[k] = 2 * np.pi * rng.f64()
    return a, e, pom, lam

# ---- author's store_probe.py, verbatim ----
R = 1e-4
SCALE_BITS = 12
SHAPE_BITS = 12

def key_cells(a, e):
    p = a * (1 - e * e)
    g = (1 - e) / (1 + e)
    m, ex = np.frexp(p)
    mq = np.round(m * (1 << SCALE_BITS)).astype(np.int64)
    gq = np.clip(np.round(g * (1 << SHAPE_BITS)), 1, 1 << SHAPE_BITS).astype(np.int64)
    p_q = mq * 2.0 ** (ex - SCALE_BITS)
    g_q = gq / (1 << SHAPE_BITS)
    k_q = (1 + g_q) / 2
    r_peri = p_q * k_q
    r_apo = p_q * k_q / g_q
    return r_peri, r_apo

def widened_u(r_peri, r_apo, with_R=True, with_quantum=True):
    qp = 2.0 ** -SCALE_BITS
    lo_r, hi_r = r_peri.copy(), r_apo.copy()
    if with_quantum:
        g = r_peri / r_apo
        pad = r_apo * (qp + qp / g) + r_peri * qp
        lo_r, hi_r = lo_r - pad, hi_r + pad
    if with_R:
        lo_r, hi_r = lo_r - R, hi_r + R
    return 1.0 / hi_r, 1.0 / lo_r

def interval_pairs(u_lo, u_hi):
    n = len(u_lo)
    order = np.argsort(u_lo)
    lo_s, hi_s = u_lo[order], u_hi[order]
    pairs = []
    for rk in range(n - 1):
        stop = np.searchsorted(lo_s, hi_s[rk], side="right")
        for o in range(rk + 1, stop):
            if hi_s[o] >= lo_s[rk]:
                i, j = int(order[rk]), int(order[o])
                pairs.append((i, j) if i < j else (j, i))
    return pairs

a, e, pom, lam = steady_scene()
print("bodies 2338, 2447:", a[2338], e[2338], "|", a[2447], e[2447])

r_peri, r_apo = key_cells(a, e)
u_lo, u_hi = widened_u(r_peri, r_apo, True, True)
for k in (2338, 2447):
    print(f"body {k}: true annulus [{a[k]*(1-e[k]):.6f}, {a[k]*(1+e[k]):.6f}]  window(u) [{u_lo[k]:.6f}, {u_hi[k]:.6f}] = window(r) [{1/u_hi[k]:.6f}, {1/u_lo[k]:.6f}]")
print("u-intervals overlap:", u_lo[2338] <= u_hi[2447] and u_lo[2447] <= u_hi[2338])

pairs = interval_pairs(u_lo, u_hi)
print("python key pairs:", len(pairs))
ks = set(pairs)
for pr in [(2338, 2447), (1868, 2757), (149, 998)]:
    print(pr, "in python key window:", pr in ks)

# soundness margin: does each body's window cover its TRUE annulus +- R?
true_lo = a * (1 - e) - R
true_hi = a * (1 + e) + R
win_lo = 1.0 / u_hi
win_hi = 1.0 / u_lo
under = win_lo - true_lo   # >0 means window inner edge INSIDE true annulus (unsound)
over = true_hi - win_hi    # >0 means window outer edge INSIDE true annulus (unsound)
print("worst inner-edge violation (win_lo - true_lo, + = bad):", under.max())
print("worst outer-edge violation (true_hi - win_hi, + = bad):", over.max())
