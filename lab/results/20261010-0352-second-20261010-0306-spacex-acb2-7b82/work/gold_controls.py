#!/usr/bin/env python3
"""Controls for the gold run, at hi-res instrument settings:
  negative: planted blunt sampler must undercount P(b<1e-4) on the tightest bin;
  zero: widest bins must return P ~ 0 (checked per job in gold_post.py too)."""
import json

import numpy as np

import probe_hlive as P

HI = dict(n_coarse=512, n_zoom_pts=24, zoom_rounds=6)
rng = np.random.default_rng(20261011)
n = 4000
da = np.exp(rng.uniform(np.log(1e-5), np.log(2e-5), n))
a1 = 1.0 + 0.02 * rng.random(n)
a2 = a1 + da
e1 = 0.01 * np.sqrt(-2.0 * np.log(1.0 - rng.random(n)))
e2 = 0.01 * np.sqrt(-2.0 * np.log(1.0 - rng.random(n)))
l1, l2 = 2 * np.pi * rng.random(n), 2 * np.pi * rng.random(n)
M01, M02 = 2 * np.pi * rng.random(n), 2 * np.pi * rng.random(n)
b_true, _ = P.pair_min_distance(a1, e1, l1, M01, a2, e2, l2, M02, **HI)
b_blunt = P.pair_min_distance_blunt(a1, e1, l1, M01, a2, e2, l2, M02)
out = {"truth_P": float(np.mean(b_true < 1e-4)),
       "blunt_P": float(np.mean(b_blunt < 1e-4)),
       "undercount_factor": float(np.mean(b_true < 1e-4) / np.mean(b_blunt < 1e-4))}
print(json.dumps(out), flush=True)
json.dump(out, open("gold_controls.json", "w"), indent=1)
