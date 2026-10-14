#!/usr/bin/env python3
"""Endgame arithmetic: the resolved-battle cost per game-second with the record's named,
verified levers applied to the m4000/rtf1 census arm. Projection from measured factors,
each cited in dossier.md; not a new measurement. Components built up, not subtracted,
so no lever is counted twice.

Census facts (m4000, rtf 1, 8 game-s, seed 1, this run):
  D = 192.0 ms/game-s = bind 125.2 (65.2%) + fixed tier 40.3 (21.0%) + rest 26.5 (13.8%)
  bind = hand-out bind 110.4 (80% of hand-out wall) + kick bind 14.8
  retry (fit2) = 48.2 ms/gs = 38.5% of the bind
Levers (cited; 009b and 7055 bit-identical on shipped code, 5eb6/8b43 digest-safe pending
merge, de99 oracle-verified Carlson kernel):
  009b  word fix:        deletes the retry (fit2) outright
  7055  hand-out memo:   -31% of hand-out bind wall (33.0% of hand-out compiles, exact)
  5eb6/8b43 fixed tier:  rekey+requeue+take_due deleted
  de99  Carlson kernel:  compile is the bind's interior (49-97% per the record);
                         conservative 10x on 70% of the surviving bind
"""
D = 192.0
bind, fixed, rest = 0.652 * D, 0.210 * D, D - 0.652 * D - 0.210 * D
ho = 1103.6 / 8.0
ho_bind = 0.800 * ho
retry = 0.385 * bind

bind_1 = bind - retry                 # 009b: the retry never compiles
bind_2 = bind_1 - 0.31 * ho_bind      # 7055: every second hand-out compile is served
bind_3 = bind_2 - 0.9 * 0.7 * bind_2  # de99: Carlson x10 on the compile share

print(f"census D at 4,000 members:            {D:8.1f} ms/game-s (bind {100*bind/D:.0f}%, "
      f"fixed {100*fixed/D:.0f}%, rest {100*rest/D:.0f}%)")
print(f"bind after word fix (009b):           {bind_1:8.1f}")
print(f"bind after hand-out memo (7055):      {bind_2:8.1f}")
print(f"bind after Carlson x10 (de99):        {bind_3:8.1f}")
after = bind_3 + rest
print(f"D after levers (fixed tier deleted):  {after:8.1f} ms/game-s = {100*after/D:.0f}% of D")
print()
# Battle ceiling: cost per member per game-second, 4k arm slope (the conservative high one:
# 1.5k arm gives 0.145, 12k arm 0.189 ms/member/gs against 4k's 0.384 -- superlinear to 4k,
# softening by 12k, so 4k is the safe slope). Budget: 25% of 4 performance cores.
budget = 0.25 * 4 * 1000.0
slope = after / 4000.0
print(f"slope after levers:                   {slope*1000:8.1f} us/member/game-s")
print(f"resolved-battle ceiling (25% of 4c):  {budget/slope:10.0f} members   (today: ~1-4x10^3)")
print(f"quiet 10^9 belt (3.6e-5 ev/body/gs, 30 us/event): "
      f"{1e9 * 3.6e-5 * 30e-3 / 1000.0:.2f} cores of event work")
