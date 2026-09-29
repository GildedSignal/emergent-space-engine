#!/usr/bin/env python3
"""Seed sampler for rung r1. Python random.Random(20260930), drawn in this order:
per bound seed: p = exp(uniform(log 10, log 1000)) then e = uniform(0, 0.7);
reject the pair and redraw both unless p >= 6.5 + 2e. 256 accepted.
Then 64 light seeds: b = exp(uniform(log 10, log 1000)).
Writes seeds.txt: 256 lines 'B <p> <e>' then 64 lines 'G <b>' (%.17g).
"""
import math, random

rng = random.Random(20260930)
bound = []
while len(bound) < 256:
    p = math.exp(rng.uniform(math.log(10.0), math.log(1000.0)))
    e = rng.uniform(0.0, 0.7)
    if p >= 6.5 + 2.0 * e:
        bound.append((p, e))
light = [math.exp(rng.uniform(math.log(10.0), math.log(1000.0))) for _ in range(64)]

with open("seeds.txt", "w") as f:
    for p, e in bound:
        f.write("B %.17g %.17g\n" % (p, e))
    for b in light:
        f.write("G %.17g\n" % (b,))
print("wrote seeds.txt: %d bound, %d light" % (len(bound), len(light)))
