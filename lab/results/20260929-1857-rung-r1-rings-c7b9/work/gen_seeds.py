#!/usr/bin/env python3
"""Rung r1 sampler: Python random.Random(20260930), drawn in this order.
Bound seeds first (with rejection), then light seeds. Long runs = first 32 bound seeds."""
import random, math, json

rng = random.Random(20260930)
bound = []
while len(bound) < 256:
    p = math.exp(rng.uniform(math.log(10), math.log(1000)))
    e = rng.uniform(0, 0.7)
    if p < 6.5 + 2 * e:
        continue
    bound.append((p, e))
light = []
while len(light) < 64:
    b = math.exp(rng.uniform(math.log(10), math.log(1000)))
    light.append(b)

with open("seeds.json", "w") as f:
    json.dump({"bound": bound, "light": light}, f, indent=0)
print(f"bound={len(bound)} light={len(light)} first32_longruns p[0]={bound[0][0]:.3f} e[0]={bound[0][1]:.3f}")
