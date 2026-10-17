#!/usr/bin/env python3
"""S* sensitivity of the composed 10^9 CPU ledger to a boundary-into-kick merge.

All inputs are the kick-cadence page's published constants (4e2d, 8ffc):
  kick 51.6-53.8 us/event, boundary 12.6-13.2 us/event, 1 of each per belt body
  per 28,141.5 game-s interval; composed ledger 10.3 M1 cores at split 8 with
  required split S* = 20.7x; the belt is everything at 10^9.
The merge's guaranteed saving is the boundary item's machinery (queue, canonical
key, apply); the certificates ride either readout. We bound it by the two cases.
"""
kick_lo, kick_hi = 51.6, 53.8
bnd_lo, bnd_hi = 12.6, 13.2
S_star, cores = 20.7, 10.3
for label, saved in (('lower bound: only item machinery, 25% of 13 us', 0.25),
                     ('upper bound: the whole boundary item', 1.0)):
    save_us = (bnd_lo + bnd_hi) / 2 * saved
    per_interval_now = (kick_lo + kick_hi) / 2 + (bnd_lo + bnd_hi) / 2
    per_interval_after = per_interval_now - save_us
    print(f'{label}: save {save_us:.1f} us of {per_interval_now:.1f} -> belt CPU '
          f'x{per_interval_after / per_interval_now:.2f}, '
          f'cores {cores * per_interval_after / per_interval_now:.1f}, '
          f"S* {S_star * per_interval_after / per_interval_now:.1f}x")
