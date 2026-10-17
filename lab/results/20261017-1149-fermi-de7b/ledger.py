#!/usr/bin/env python3
"""The 10⁹ belt CPU ledger on the two branches of the boundary question.

Constants (page-cited, not re-measured here):
  kick cost x86 52.7 µs, boundary 12.9 µs/event   (8ffc: 51.6–53.8, 12.6–13.2)
  kick cost M1 29.3 µs                            (e7ef)
  boundary M1 = 12.9 × 29.3/52.7 = 7.17 µs        [inference: same work, same ratio]
  belt interval 28,141.5 game-s                   (3294/8ffc, = 2 × h p50 14,071 here)
  belt survival 0.615                             (1a46's belt delete, via 4e2d)
  2 events per body per interval (1 kick + 1 boundary; this run, every octave)
"""
K_X, B_X = 52.7e-6, 12.9e-6
K_M, B_M = 29.3e-6, K_X and 12.9e-6 * 29.3e-6 / 52.7e-6
IV, SURV, RTF, N = 28141.5, 0.615, 100.0, 1e9

def cores(kick_us, bnd_us, split, survive=True):
    per_body_interval = kick_us + bnd_us
    return N * per_body_interval * RTF / (split * IV) * (SURV if survive else 1.0)

print(f"{'split':>6} | {'x86 riding':>10} | {'M1 riding':>9} | {'M1 boundary-pinned floor':>24}")
for S in (1, 8, 20.7, 58):
    # pinned: the boundary comb does NOT stretch with the split, so its cost is S-independent.
    print(f"{S:>6} | {cores(K_X, B_X, S):>9.1f}c | {cores(K_M, B_M, S):>8.2f}c | {cores(0.0, B_M, 1.0):>23.2f}c")
print(f"S* to 4 M1 cores, riding: {cores(K_M, B_M, 1.0) / 4.0:.1f}x  (pinned branch: a {cores(0.0, B_M, 1.0):.1f}-core floor no split touches)")
print("measured anchors (this run, N=10^4, shipped counters + per-body plans):")
for arm, h, ev in ((6, 28141, 2), (7, 14071, 4), (8, 7035, 8)):
    print(f"  step_log2={arm}: h p50 {h} gs, {ev} events/body by ~56.3-60k gs "
          f"(rate {ev / (2 * h):.3e}/gs/body = {ev / (2 * h) / (4 / (2 * 14071)):.4f}x shipped)")
