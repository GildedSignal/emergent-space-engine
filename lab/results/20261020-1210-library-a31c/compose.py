#!/usr/bin/env python3
"""Composition of the 1e9 era wall from page-cited constants (nladder, run 8365:
45.9 µs/kick and 8.6 µs/boundary sequential item cost, checker-confirmed
45.6/8.57; era = 27.9k game-s; stream share 49.7% burn / 50.7% coast boundary;
play rtf 400; kick-item floor ~50 ns per the scoreboard's 42–55 ns kick floor).
Every number below derives from those constants; nothing is re-measured."""
US_KICK, US_BND = 45.9e-6, 8.6e-6   # s per item, sequential carrier (8365)
ERA_GS = 27_900                     # game-s per era (one clock period)
RTF = 400                           # play cadence (0a46/ca63 arms)
FLOOR = 50e-9                       # s per item at the scoreboard's kick floor

budget = ERA_GS / RTF
kick_h = 1e9 * US_KICK / 3600
bnd_h = 1e9 * US_BND / 3600
floor_s = 1e9 * FLOOR

print("era wall budget at rtf 400      : %8.2f s" % budget)
print("kick comb  1e9 x 45.9us         : %8.2f h   (%.0fx over budget)" % (kick_h, kick_h * 3600 / budget))
print("bnd comb   1e9 x  8.6us         : %8.2f h   (%.0fx over budget)" % (bnd_h, bnd_h * 3600 / budget))
print("boundary share of stream events : ~50% (49.7 burn / 50.7 coast, 8365 regen)")
print("kick comb at 50ns item floor    : %8.2f s   (%.2fx budget -> fits)" % (floor_s, floor_s / budget))
print("gap carried by the kick item    : %.0fx  (45.9us -> ~50ns)" % (US_KICK / FLOOR))
print("boundary deletion buys          : %.1fx on the era wall (12.75+2.39 -> 12.75 h)" % ((kick_h + bnd_h) / kick_h))
print("era-2/4 wall at 1e5 after delete: 105k x 8.6us = %.2f s of items deleted (P4)" % (105e3 * US_BND))
