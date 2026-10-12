#!/usr/bin/env python3
"""Probe: per-kick repair vs drift-quantum skin for encounter certificates.

Element-space model of the encounters design (r8 v2, q-candidate-degree, the slack skin):
- Bodies on Kepler orbits; positions re-derived analytically (no ticks, generators).
- The ONLY element changes are kicks (plane reality: ~32 per orbit per body).
- A pair certificate: built from a 1-D window on a (|a_i - a_j| < R_ENC + slack),
  next conjunction predicted analytically (circular orbits: miss = |da| at conjunction).
- Structures differ ONLY in when a body re-pays its window query + pair rebuild:
    A (per-kick): every kick of body i re-pays i's window. Arrival-process driven.
    B (skin): kicks accumulate; body i re-pays only when accumulated |da_i| crosses
       the quantum W_SLACK. Zero-miss by 1-D triangle inequality: windows are built
       with radius R_ENC + W_SLACK, and while |da_i| + |da_j| <= W_SLACK any pair
       coming within R_ENC was already inside the built window.
  Both evaluate conjunctions at predicted deadlines (never polled).
Truth: independent physical x-sweep per checkpoint (exact). Misses = truth pairs not
covered by cert geometry (width failures; identical for A and B by construction).
A and B run with identical seeded kick realizations (same physical world).
Work: pair-evals + query ops, each distinct event once.
Runtime ~40 s, < 300 MB.
"""
import numpy as np, json

R_ENC = 2e-4          # encounter distance
W_SLACK = 1e-4        # drift quantum (skin width); R_ENC/2 keeps the zero-miss bound
SIGMA_KICK = 5e-5     # per-kick da sigma (at a=1)
E_TYP = 0.05          # eccentricity the wide element tier must cover
T_CK = 150            # checkpoints per orbit at a=1
DT = 2*np.pi / T_CK
WIN = R_ENC + W_SLACK # cert window radius at build time

def make_belt(n, a0=0.9, a1=1.1, seed=0):
    r = np.random.default_rng(100 + seed)
    return r.uniform(a0, a1, n), np.zeros(n), r.uniform(0, 2*np.pi, n)

def make_tail_belt(n):
    r = np.random.default_rng(101)
    a, m = r.uniform(0.9, 1.1, n), r.uniform(0, 2*np.pi, n)
    e = np.zeros(n)
    idx = r.choice(n, n//10, replace=False)
    a[idx] = r.uniform(0.95, 1.05, len(idx)); e[idx] = r.uniform(0.7, 0.9, len(idx))
    return a, e, m

def make_formation(n, siga=0.02):
    r = np.random.default_rng(102)
    return 1.0 + r.normal(0, siga, n), np.zeros(n), r.uniform(0, 2*np.pi, n)

def positions(a, e, m0, t):
    n_ = a ** -1.5
    th = m0 + n_*t
    if not np.any(e > 1e-9):
        return a*np.cos(th), a*np.sin(th)
    M = th % (2*np.pi)
    E = M.copy()
    for _ in range(80):
        f = E - e*np.sin(E) - M
        fp = 1 - e*np.cos(E)
        E = E - np.clip(f/np.where(np.abs(fp) > 1e-12, fp, 1e-12), -0.8, 0.8)
    nu = 2*np.arctan2(np.sqrt(1+e)*np.sin(E/2), np.sqrt(1-e)*np.cos(E/2))
    r = a*(1 - e*np.cos(E))
    return r*np.cos(nu), r*np.sin(nu)

def truth_pairs(a, e, m0, t):
    x, y = positions(a, e, m0, t)
    o = np.argsort(x); xs, ys = x[o], y[o]
    out = set()
    for k in range(1, 9):
        dx = xs[k:] - xs[:-k]
        ii = np.nonzero(dx < R_ENC)[0]
        if ii.size == 0 and k > 2: break
        keep = np.abs(ys[k:] - ys[:-k]) < R_ENC
        for p in ii[keep[ii]]:
            i, j = o[p], o[p+k]
            out.add((i, j) if i < j else (j, i))
    return out

def window_size(a_sorted, a_vals, width):
    lo = np.searchsorted(a_sorted, a_vals - width, 'left')
    hi = np.searchsorted(a_sorted, a_vals + width, 'right')
    return (hi - lo).astype(np.int64)

def run(name, a, e, m0, lam, struct):
    n = len(a)
    rng = np.random.default_rng(11)     # identical kick realization for A and B
    a_cur = a.copy()
    drift = np.zeros(n)                 # accumulated |da| since last window payment
    win_paid = 0                        # window queries + window scan ops paid
    pair_evals = 0                      # deadline (conjunction) evaluations
    encounters = set(); width_miss = 0
    per_ck = []
    for ck in range(T_CK):
        t = ck*DT
        w0 = win_paid + pair_evals
        kicks = rng.random(n) < (lam / T_CK)
        nk = int(kicks.sum())
        if nk:
            da_k = rng.normal(0, SIGMA_KICK, n) * kicks
            a_cur = a_cur + da_k
            drift = drift + np.abs(da_k)
            a_sorted = np.sort(a_cur)
            if struct == 'A':
                idx = np.nonzero(kicks)[0]                 # pay per kick
                win_paid += nk + int(window_size(a_sorted, a_cur[idx], WIN).sum())
            else:
                cross = drift >= W_SLACK                    # pay per quantum crossing
                if cross.any():
                    idx = np.nonzero(cross)[0]
                    win_paid += len(idx) + int(window_size(a_sorted, a_cur[idx], WIN).sum())
                    drift[cross] = 0.0
        else:
            a_sorted = np.sort(a_cur)
        # deadline evaluations this interval (equal for both structures): conjunction
        # rate of live |da|<R_ENC pairs ~ live_pairs * |dn|*DT/2pi, |dn| ~ 1.5*R_ENC
        live_pairs = int(window_size(a_sorted, a_cur, R_ENC).sum()) // 2
        pair_evals += int(live_pairs * (1.5 * R_ENC * DT / (2*np.pi)))
        # truth at this checkpoint (independent of all cert machinery)
        for (i, j) in truth_pairs(a_cur, e, m0, t):
            encounters.add((i, j))
            if abs(a_cur[i] - a_cur[j]) > WIN:   # width failure (same for A and B)
                width_miss += 1
        per_ck.append(win_paid + pair_evals - w0)
    a_s = np.sort(a)
    e_setup = int(window_size(a_s, a, E_TYP + R_ENC).sum() // 2)   # wide tier setup
    b_live  = int(window_size(a_s, a, WIN).sum() // 2)             # skin window pairs
    enc = len(encounters)
    work = win_paid + pair_evals
    pc = np.array(per_ck, dtype=float)
    return dict(name=name, struct=struct, n=n, lam=lam, encounters=enc,
                work=work, work_per_enc=work/max(enc, 1), win_paid=win_paid,
                pair_evals=pair_evals, width_miss=width_miss, b_live=b_live,
                e_setup=e_setup, med_ck=float(np.median(pc)),
                p99_ck=float(np.percentile(pc, 99)))

if __name__ == '__main__':
    results = []
    for i, n in enumerate((10_000, 20_000, 40_000)):   # dilution: annulus grows, density fixed
        area = n/15_910.
        a1 = np.sqrt(0.81 + area/np.pi); a0 = 1.0 - (a1 - 0.9)
        a, e, m = make_belt(n, a0, a1, seed=i)
        for st in ('A', 'B'):
            results.append(run(f'belt{n}-lam32', a, e, m, 32.0, st))
    a, e, m = make_belt(20_000, seed=7)
    for st in ('A', 'B'):
        results.append(run('belt20k-lam0.5', a, e, m, 0.5, st))
    a, e, m = make_tail_belt(20_000)
    for st in ('A', 'B'):
        results.append(run('belt20k+tail', a, e, m, 32.0, st))
    a, e, m = make_formation(5_000)
    for st in ('A', 'B'):
        results.append(run('formation5k', a, e, m, 32.0, st))
    json.dump(results, open('probe_out.json', 'w'), indent=1)
    for r in results:
        print(f"{r['name']:15s} {r['struct']} enc={r['encounters']:5d} work/enc={r['work_per_enc']:9.1f} "
              f"win_paid={r['win_paid']:11d} evals={r['pair_evals']:8d} wmiss={r['width_miss']:4d} "
              f"B-live={r['b_live']:9d} E-setup={r['e_setup']:10d} "
              f"p99/med={r['p99_ck']/max(r['med_ck'],1e-9):5.2f}")
