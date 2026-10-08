#!/usr/bin/env python3
"""Lookahead-depth error: fixed-frequency certificate fitted on conjunctions
0-99, |prediction error|/amplitude vs lookahead, random non-resonant pairs."""
import collections

import numpy as np

src = open("probe_conjunctions.py").read().split("def run_case")[0]
exec(src)
MU = 1.0
rows = []
for s in range(8):
    r = np.random.default_rng(100 + s)
    a1, a2 = 1.0, 1.0 * (1.03 + 0.22 * r.uniform(0, 1))
    p1 = (a1, 0.3 * r.uniform(0, 1), r.uniform(0, 2 * np.pi), r.uniform(0, 2 * np.pi), np.sqrt(MU / a1**3), 0.003 * r.uniform(0, 1) * np.sqrt(MU / a1**3))
    p2 = (a2, 0.3 * r.uniform(0, 1), r.uniform(0, 2 * np.pi), r.uniform(0, 2 * np.pi), np.sqrt(MU / a2**3), 0.003 * r.uniform(0, 1) * np.sqrt(MU / a2**3))
    d, tk = conjunction_distances(p1, p2, n_cyc=165)
    d = d[:150]
    train, test = d[:100], d[100:]
    D, coef = fit_one_freq(train)
    pred = _design(np.arange(100, 150), [D]) @ coef
    amp = train.max() - train.min()
    err = np.abs(pred - test) / amp
    for lag in (1, 2, 3, 5, 10, 20, 50):
        rows.append((lag, float(err[lag - 1])))
by = collections.defaultdict(list)
for lag, e in rows:
    by[lag].append(e)
print("lookahead (conjunctions ahead) -> median/max |pred err| / amplitude")
for lag in sorted(by):
    print(f"  lag {lag:3d}: median={np.median(by[lag]):.3f}  max={np.max(by[lag]):.3f}")
with open("lookahead.json", "w") as f:
    import json
    json.dump({str(k): dict(median=float(np.median(v)), max=float(np.max(v))) for k, v in by.items()}, f, indent=1)
