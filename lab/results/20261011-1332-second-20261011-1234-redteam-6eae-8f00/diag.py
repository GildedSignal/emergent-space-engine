#!/usr/bin/env python3
"""4 s subset of view_images.py: the Phi(psi) curve structure (surviving segments, wraps).
The multiplicity logic lives in view_images.py; this exists so a checker can see the
families fast."""
from view_images import trace
import numpy as np

for r_o, r_e in [(100.0, 200.0), (10.0, 20.0), (3.2, 20.0)]:
    ps = np.linspace(0.02, np.pi - 0.02, 32768)
    res = trace(r_o, r_e, ps)
    Phi, fin = res["Phi"], np.isfinite(res["Phi"])
    segs, start = [], None
    for i in range(ps.size):
        if fin[i] and start is None:
            start = i
        elif not fin[i] and start is not None:
            segs.append((start, i)); start = None
    if start is not None:
        segs.append((start, ps.size))
    for s, e in segs:
        print(f"r_o={r_o}: psi [{np.degrees(ps[s]):.2f}, {np.degrees(ps[e-1]):.2f}] deg"
              f" -> Phi span {Phi[e-1]-Phi[s]:.3f} rad = {(Phi[e-1]-Phi[s])/2/np.pi:.3f} wraps")
