#!/usr/bin/env python3
"""Experiment 2: does kick cadence bite at long horizon, and does resonance
proximity (from birth elements alone) pick the bodies where it bites?
Belt C physics (mu_J x3), 600 Jupiter orbits, NEAR (small zeta_raw) vs FAR
(large zeta_raw), 250 bodies each. Ladder {4,16,64,256}, truth 512."""
import numpy as np
import cadence as C
from analysis import zeta as zeta_raw_fn

MUJ3 = 3 * 9.545937e-4

# fresh belt, same a-range as A, e Rayleigh 0.05
state0, a0, e0 = C.make_belt(2048, 2.0, 3.6, 0.05, 44)
zr = zeta_raw_fn(a0, e0, MUJ3)
order = np.argsort(zr)
near = order[:250]
far = order[-250:]
np.savez("out_exp2_birth.npz", a=a0[near], e=e0[near], a_far=a0[far],
         e_far=e0[far], zeta_near=zr[near], zeta_far=zr[far])

for tag, sel in (("near", near), ("far", far)):
    s = state0[sel]
    out = {}
    for K in (4, 16, 64, 256, 512):
        es, _ = C.run(s, 600, K, muj=MUJ3, sample_every=8)
        out[f"e{K}"] = es
        print(f"exp2 {tag} K={K} done", flush=True)
    np.savez(f"out_exp2_{tag}.npz", **out)
print("exp2 complete")
