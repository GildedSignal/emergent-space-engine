#!/usr/bin/env python3
"""Rung r8 v3 belts. Sampler: r8 v2's — one Python random.Random(20261008) stream, extended.

(a) 16 belts N=1000, a in [1,1.5], sigma_e log-uniform [1e-3,3e-2], rho log-uniform [1e-4,1e-3],
    100 orbits; then four adversarial belts: narrow-in-a, co-orbital, equal-period keys, hot.
(b) steady: N=3000, sigma_e=1e-2, rho=1e-4, 1e5 orbits.
(c) scaling: N in {1e3,1e4,1e5}, sigma_e=1e-2, rho=1e-4*(1e4/N) (rho ∝ 1/N: fixed per-body rate).
(d) kicks: N=1e4, sigma_e=1e-2, rho=1e-4.

Bodies: a uniform (or on `keys` discrete values), e Rayleigh (capped 0.5), pom, lam uniform.
Written as one binary file per belt (N*4 f64 LE: a, e, pom, lam) + belts.json index.
The bodies are fed to the code under test through Body::new(a, e, pom, lam), which rounds the
period to integer ticks (the law's clock) — both truth and methods see identical orbits.
"""
import json, math, random, struct, sys, os

TAU = 2.0 * math.pi
OUT = os.path.dirname(os.path.abspath(__file__))


def draw_belt(rng, name, n, sigma_e, rho, a_lo, a_hi, keys, orbits):
    bodies = []
    for _ in range(n):
        if keys > 1:
            k = rng.randrange(keys)
            a = a_lo + (a_hi - a_lo) * k / (keys - 1)
        else:
            a = a_lo + (a_hi - a_lo) * rng.random()
        u = rng.random()
        e = min(sigma_e * math.sqrt(-2.0 * math.log(1.0 - u)), 0.5)
        pom = TAU * rng.random()
        lam = TAU * rng.random()
        bodies.append((a, e, pom, lam))
    fn = f"belt-{name}.f64"
    with open(os.path.join(OUT, fn), "wb") as f:
        f.write(struct.pack(f"<{4*n}d", *[x for b in bodies for x in b]))
    return {"name": name, "n": n, "sigma_e": sigma_e, "rho": rho, "a_lo": a_lo, "a_hi": a_hi,
            "keys": keys, "orbits": orbits, "file": fn}


def main():
    rng = random.Random(20261008)  # the one stream, extended from r8 v2
    belts = []
    # (a) 16 belts
    for k in range(16):
        sigma_e = 10.0 ** rng.uniform(math.log10(1e-3), math.log10(3e-2))
        rho = 10.0 ** rng.uniform(math.log10(1e-4), math.log10(1e-3))
        belts.append(draw_belt(rng, f"a{k:02d}", 1000, sigma_e, rho, 1.0, 1.5, 0, 100.0))
    # four adversarial belts (parameters on the pattern of the crate's verify sets)
    belts.append(draw_belt(rng, "narrow", 400, 0.025, 3e-3, 1.0, 1.0025, 0, 20.0))     # |dn|*T < 2pi for every pair
    belts.append(draw_belt(rng, "coorbital", 300, 3e-4, 1e-3, 1.0, 1.0001, 0, 50.0))
    belts.append(draw_belt(rng, "equalkeys", 300, 1e-2, 1e-3, 1.0, 1.001, 3, 50.0))    # identical integer periods per key
    belts.append(draw_belt(rng, "hot", 500, 0.1, 1e-3, 1.0, 1.5, 0, 50.0))             # sigma_e = 0.1
    # (b) steady
    belts.append(draw_belt(rng, "steady", 3000, 1e-2, 1e-4, 1.0, 1.5, 0, 1e5))
    # (c) scaling
    for n in (1000, 10000, 100000):
        belts.append(draw_belt(rng, f"scale-n{n}", n, 1e-2, 1e-4 * 1e4 / n, 1.0, 1.5, 0, 100.0))
    # (d) kicks
    belts.append(draw_belt(rng, "kick", 10000, 1e-2, 1e-4, 1.0, 1.5, 0, 0.0))
    with open(os.path.join(OUT, "belts.json"), "w") as f:
        json.dump(belts, f, indent=1)
    for b in belts:
        print(f"{b['name']:14s} n={b['n']:6d} sigma_e={b['sigma_e']:.4g} rho={b['rho']:.3g} "
              f"a=[{b['a_lo']},{b['a_hi']}] keys={b['keys']} orbits={b['orbits']:.4g}")


if __name__ == "__main__":
    main()
