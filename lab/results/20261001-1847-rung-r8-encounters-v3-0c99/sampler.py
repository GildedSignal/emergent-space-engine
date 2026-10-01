"""rung r8 v3 — sampler (frozen): r8 v2's Python random.Random(20261008), extended.

Draw order (deterministic, one shared rng seeded 20261008):
  1. 16 belts: sigma_e log-uniform [1e-3, 3e-2] (v2's), rho log-uniform [1e-4, 1e-3] (v3's),
     N = 1000, a uniform [1, 1.5], 100 orbits at a = 1.
  2. Four adversarial belts (N = 1000, 100 orbits): narrow-a, co-orbital, equal-period (3 keys),
     hot (sigma_e = 0.1).
  3. Case (b): N = 3000, sigma_e = 1e-2, rho = 1e-4 (steady, 1e5 orbits).
  4. Case (c): N in {1000, 10000, 100000}, sigma_e = 1e-2, rho = 1e-4 * 1e4/N (rho ~ 1/N).
  5. Case (d): N = 10000, sigma_e = 1e-2, rho = 1e-4; then 100 kicks (index, sign).
Per body (v2's make_belt order): a, u (Rayleigh), pom, lam — 4 rng draws; e capped at 0.5.
Each belt -> <name>.bin (4*N f64 LE: a, e, pom, lam0) + belts.json (parameters).
"""
import json
import math
import random
import struct
import sys

TWOPI = 2.0 * math.pi
OUT = sys.argv[1] if len(sys.argv) > 1 else "."

rng = random.Random(20261008)
belts = []


def draw_belt(name, n, sigma_e, rho, orbits, a_lo=1.0, a_hi=1.5, keys=0):
    arr = bytearray()
    for _ in range(n):
        if keys > 1:
            k = rng.randrange(keys)
            a = a_lo + (a_hi - a_lo) * k / (keys - 1)
        else:
            a = a_lo + (a_hi - a_lo) * rng.random()
        u = rng.random()
        e = min(sigma_e * math.sqrt(-2.0 * math.log1p(-u)), 0.5)
        pom = TWOPI * rng.random()
        lam = TWOPI * rng.random()
        arr += struct.pack("<4d", a, e, pom, lam)
    with open(f"{OUT}/{name}.bin", "wb") as f:
        f.write(arr)
    belts.append(dict(name=name, n=n, sigma_e=sigma_e, rho=rho, orbits=orbits,
                      a_lo=a_lo, a_hi=a_hi, keys=keys, file=f"{name}.bin"))


# (a) 16 belts: sigma_e log-uniform [1e-3, 3e-2], rho log-uniform [1e-4, 1e-3]
for b in range(16):
    sigma_e = math.exp(rng.uniform(math.log(1e-3), math.log(3e-2)))
    rho = math.exp(rng.uniform(math.log(1e-4), math.log(1e-3)))
    draw_belt(f"a{b:02d}", 1000, sigma_e, rho, 100.0)

# (a) four adversarial belts
draw_belt("adv-narrow", 1000, 0.025, 1e-3, 100.0, 1.0, 1.0025)   # |dn|*T < 2pi for ~every pair
draw_belt("adv-coorbital", 1000, 3e-4, 1e-3, 100.0, 1.0, 1.0001)
draw_belt("adv-equalperiod", 1000, 1e-2, 1e-3, 100.0, 1.0, 1.001, keys=3)  # identical integer periods per key
draw_belt("adv-hot", 1000, 0.1, 1e-3, 100.0)

# (b) steady
draw_belt("b-steady", 3000, 1e-2, 1e-4, 1e5)
# (c) scaling, rho ~ 1/N
for n in (1000, 10000, 100000):
    draw_belt(f"c-n{n}", n, 1e-2, 1e-4 * 1e4 / n, 1000.0)
# (d) kicks
draw_belt("d-kick", 10000, 1e-2, 1e-4, 1000.0)
kicks = [dict(i=rng.randrange(10000), sign=1 if rng.random() < 0.5 else -1) for _ in range(100)]

with open(f"{OUT}/belts.tsv", "w") as f:
    for b in belts:
        f.write(f"{b['name']}\t{b['n']}\t{b['sigma_e']!r}\t{b['rho']!r}\t{b['orbits']!r}\n")
with open(f"{OUT}/kicks.tsv", "w") as f:
    for k in kicks:
        f.write(f"{k['i']}\t{k['sign']}\n")
with open(f"{OUT}/belts.json", "w") as f:
    json.dump(dict(belts=belts, kicks=kicks, seed=20261008), f, indent=1)
print(json.dumps([f"{b['name']} sig={b['sigma_e']:.4g} rho={b['rho']:.3g}" for b in belts[:16]], indent=0))
