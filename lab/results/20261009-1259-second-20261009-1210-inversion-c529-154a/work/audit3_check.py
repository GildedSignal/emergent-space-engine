#!/usr/bin/env python3
"""Independent population check of the Rust rank computation (run ...-154a).

Reimplements the generators (splitmix-style Rng from belt.rs + the fleet/ring recipes
published in the patches) in pure Python, computes mean longitude lam_k(t) = lam0_k
+ n_k t with n_k = a_k^-1.5 (crate: n = TAU*TICKS/period, rad per time unit), and
recounts the symmetric-min lambda-rank of the partner at the Rust event times.

Checks:
  G1c pair (89,107) at its two dumped event times  (Rust says rank_lam = 6)
  E1  pair (33,259) at its dumped event time       (Rust says rank_lam = 8)
Agreement => the Rust rank loop is faithful; disagreement => Rust bug.
"""
import json, math

TAU = 2 * math.pi
M64 = (1 << 64) - 1

class Rng:
    def __init__(self, s): self.s = s & M64
    def next_u64(self):
        self.s = (self.s + 0x9E3779B97F4A7C15) & M64
        z = self.s
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & M64
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M64
        return z ^ (z >> 31)
    def f64(self):
        return (self.next_u64() >> 11) / 9007199254740992.0

def fleet(nc, a_hw, sigma_e, e_cap, bunch, seed):
    rng = Rng(seed)
    pom0 = TAU * rng.f64()
    out = []
    for _ in range(nc):
        a = 1.0 + (2.0 * rng.f64() - 1.0) * a_hw
        u = rng.f64()
        e = min(sigma_e * math.sqrt(-2.0 * math.log(1.0 - u)), e_cap)
        pom = pom0 + (2.0 * rng.f64() - 1.0) * 0.1 if bunch else TAU * rng.f64()
        lam = TAU * rng.f64()
        out.append((a, e, pom, lam))
    return out

def ring(n, spread, sigma_e, equal, seed):
    rng = Rng(seed)
    out = []
    for _ in range(n):
        a = 1.0 + spread * rng.f64()
        u = rng.f64()
        e = min(sigma_e * math.sqrt(-2.0 * (1.0 - u).ln()) if False else sigma_e * math.sqrt(-2.0 * math.log(1.0 - u)), 0.5)
        pom = TAU * rng.f64()
        lam = TAU * rng.f64()
        out.append((a, e, pom, lam, equal))
    return out

def lam_of(body, t):
    a, e, pom, lam0 = body[:4]
    # crate: period = round(TAU a^1.5 2^32) ticks; n = TAU 2^32 / period; a' = n^-2/3
    period = round(TAU * a ** 1.5 * 2 ** 32)
    n = TAU * 2 ** 32 / period
    a2 = n ** (-2.0 / 3.0)
    n2 = 1.0 / a2 ** 1.5  # == n up to rounding of a2; use n directly
    return (lam0 + n * t) % TAU

def cd(x, y):
    d = (x - y) % TAU
    return min(d, TAU - d)

def rank_at(bodies, i, j, t):
    li, lj = lam_of(bodies[i], t), lam_of(bodies[j], t)
    g = cd(li, lj)
    ri = sum(1 for k in range(len(bodies)) if k not in (i, j) and cd(li, lam_of(bodies[k], t)) < g)
    rj = sum(1 for k in range(len(bodies)) if k not in (i, j) and cd(lj, lam_of(bodies[k], t)) < g)
    return 1 + min(ri, rj), g, g / (TAU / len(bodies))

seed = 0xC529
G1C = fleet(300, 1e-5, 1e-2, 0.05, True, seed + 12)  # G1c seed; +11 is G1b
# E1: ring(300, 0.0, 1e-2, true, seed+3) — equal periods: Body::with_period(p0,...) with
# p0 = round(TAU*1*TICKS); per-body draws identical to ring()
def ring_equalp(n, sigma_e, seed):
    rng = Rng(seed)
    p0 = round(TAU * 1.0 ** 1.5 * 2 ** 32)
    out = []
    for _ in range(n):
        a_draw = 1.0 + 0.0 * rng.f64()   # spread=0 still consumes a draw
        u = rng.f64()
        e = min(sigma_e * math.sqrt(-2.0 * math.log(1.0 - u)), 0.5)
        pom = TAU * rng.f64()
        lam = TAU * rng.f64()
        out.append((a_draw, e, pom, lam, True))
    return out

E1 = ring_equalp(300, 1e-2, seed + 3)

res = {}
# G1c worst events from refresh-b.jsonl (first draft used seed+11: wrong population, rank agreement was coincidence)
g1c = [json.loads(l) for l in open("refresh-b.jsonl") if "G1c" in l][0]
for w in g1c["worst"]:
    if {w["i"], w["j"]} == {89, 107}:
        r, g, gs = rank_at(G1C, w["i"], w["j"], w["t"])
        res[f"G1c 89/107 t={w['t']:.4f}"] = (r, round(gs, 2), w["rank_lam"])
# E1 worst event from refresh-a.jsonl
e1 = [json.loads(l) for l in open("refresh-a.jsonl") if "E1-" in l][0]
for w in e1["worst"]:
    if {w["i"], w["j"]} == {33, 259}:
        r, g, gs = rank_at(E1, w["i"], w["j"], w["t"])
        res[f"E1 33/259 t={w['t']:.4f}"] = (r, round(gs, 2), w["rank_lam"])

print(json.dumps({k: {"py_rank_lam": v[0], "gap_spacings": v[1], "rust_rank_lam": v[2]}
                  for k, v in res.items()}, indent=1))
