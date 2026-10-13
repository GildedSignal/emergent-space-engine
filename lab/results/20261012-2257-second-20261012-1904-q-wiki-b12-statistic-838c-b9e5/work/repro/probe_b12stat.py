#!/usr/bin/env python3
"""Probe v2: per-seed max vs time-mean for B12 (bounded vs compounding error).

v1 flaw (reported): noise drawn from student-t df=2 has infinite variance; its
running max swamped the leak signal. v2 keeps heavy-ish tails finite (df=5,
sigma 0.5) with mean reversion (bounded stationary process), and leaks that
actuate on 1% of steps. AUC (threshold-free) + misclassification at the optimal
Youden threshold, 200 seeds per class, T in {100, 1000}.
Statistic per seed: slope of the statistic across 4 quarter-windows in log space
(max-of-window, mean-of-window, and RMS-of-window as a third control).
"""
import numpy as np, json

LAM = 0.98
NOISE_DF, NOISE_SD = 5, 0.5
JUMP_P, JUMP = 0.01, 1.0

def make(proc, T, rng):
    x = np.zeros(T); cur = 0.0; leak = 0.0
    for t in range(T):
        cur = LAM * cur + rng.standard_t(NOISE_DF) * NOISE_SD / np.sqrt(NOISE_DF / (NOISE_DF - 2))
        if proc == 'leak' and rng.random() < JUMP_P:
            leak += JUMP
        elif proc == 'always':
            leak += 0.02
        x[t] = cur + leak
    return x

def slope(x, stat):
    q = len(x) // 4
    vals = [max(stat(x[i*q:(i+1)*q]), 1e-9) for i in range(4)]
    return np.polyfit(np.log([1, 2, 3, 4]), np.log(vals), 1)[0]

def auc(pos, neg):
    allv = np.concatenate([pos, neg]); ranks = allv.argsort().argsort() + 1
    r = ranks[:len(pos)]
    return (r.sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))

def misclass(pos, neg):
    thr = np.concatenate([pos, neg])
    best = 1.0
    for t in thr:
        err = (pos <= t).mean() * 0.5 + (neg > t).mean() * 0.5
        best = min(best, err)
    return best

S = 200
out = {}
print(f"{'T':>5s} {'stat':>5s} {'leak AUC':>9s} {'always AUC':>11s} {'leak mis':>9s} {'always mis':>11s}")
for T in (100, 1000):
    data = {}
    for proc in ('bounded', 'leak', 'always'):
        xs = [make(proc, T, np.random.default_rng(T * 7919 + s)) for s in range(S)]
        data[proc] = xs
    for name, stat in (('max', lambda v: np.abs(v).max()),
                       ('mean', lambda v: np.abs(v).mean()),
                       ('rms', lambda v: np.sqrt((v ** 2).mean()))):
        aucs, misses = {}, {}
        for proc_pos in ('leak', 'always'):
            pos = np.array([slope(x, stat) for x in data[proc_pos]])
            neg = np.array([slope(x, stat) for x in data['bounded']])
            aucs[proc_pos] = auc(pos, neg)
            misses[proc_pos] = misclass(pos, neg)
        out[f"T{T}/{name}"] = {k: (aucs[k], misses[k]) for k in aucs}
        print(f"{T:5d} {name:>5s} {aucs['leak']:9.3f} {aucs['always']:11.3f} {misses['leak']:9.2%} {misses['always']:11.2%}")
json.dump(out, open('probe_b12_out.json', 'w'), indent=1)
