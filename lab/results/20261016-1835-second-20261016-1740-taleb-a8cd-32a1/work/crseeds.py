#!/usr/bin/env python3
"""Correctly-rounded (CR) rebuild of the B12 corpus seed path (run 20261016-1835-...-32a1).

The parent run (20261016-1740-taleb-a8cd) measured the disease: the frozen corpus is
libm-conditional because `handoff::ship` builds its f64 seed through non-CR libm calls
(`cbrt` inside `Restricted::hill`, `powf(r,-0.5)`, `cos`, `sin`).  The checker's named
missing experiment: would a CR-only seed path give back a stable corpus ("judged 16/16")?

This script recomputes the *draws* exactly (SplitMix64, all CR arithmetic) and then every
non-CR call at 60 decimal digits with mpmath, rounding each f64 op individually, and writes
the CR seed table the Rust probe (`lab_corpus_cr_seeds`, via patch.diff) consumes.

Each f64 op of the seed path is simulated: mpmath carries exact operands (f64 -> mpf is
exact) at dps=60 (~199 bits), so the final float() rounding is the correctly-rounded f64
of the exact operation (ties are measure-zero; a tie would still land within 1 ulp).
"""
import struct
import mpmath as mp

mp.mp.dps = 60

HANDOFF_SEED = 20261002
MASK = (1 << 64) - 1
MU = 1e-3
SEP = 5.27e8
KEPT = [32, 39, 53, 57, 70, 72, 78, 83, 85, 88, 101, 106, 138, 142, 148, 159]
RAD = float(mp.pi / 180)  # the f64 nearest pi/180, same constant Rust's to_radians uses


class Rng:
    def __init__(self, s):
        self.s = s & MASK

    def next(self):
        self.s = (self.s + 0x9E3779B97F4A7C15) & MASK
        z = self.s
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK
        return z ^ (z >> 31)

    def unit(self):
        return float(mp.mpf(self.next() >> 11) / mp.mpf(1 << 53))  # exact, then round


def fl(x):
    return float(x)


def draws(n):
    rng = Rng(HANDOFF_SEED)
    out = []
    for _ in range(n):
        side = 1.0 if (rng.next() >> 63) == 1 else -1.0
        k = fl(1.5 + fl(1.5 * rng.unit()))
        alpha = fl(fl(30.0 + fl(300.0 * rng.unit())) * RAD)
        out.append((side, k, alpha))
    return out


def cr_seed(side, k, alpha):
    # Restricted::hill: sep * (mu/3).cbrt(), each step CR
    mu3 = fl(mp.mpf(MU) / 3)
    hill = fl(mp.mpf(SEP) * mp.root(mp.mpf(mu3), 3))
    # ship(): r = sep * (1 + side * hill / sep * k), each step CR, left-to-right
    t1 = fl(mp.mpf(side) * mp.mpf(hill))
    t2 = fl(t1 / mp.mpf(SEP))
    t3 = fl(mp.mpf(t2) * mp.mpf(k))
    t4 = fl(1.0 + mp.mpf(t3))
    r = fl(mp.mpf(SEP) * mp.mpf(t4))
    v = fl(mp.power(mp.mpf(r), mp.mpf(-1) / 2))
    c = fl(mp.cos(mp.mpf(alpha)))
    s = fl(mp.sin(mp.mpf(alpha)))
    x = fl(mp.mpf(r) * mp.mpf(c))
    y = fl(mp.mpf(r) * mp.mpf(s))
    vx = fl(mp.mpf(-v) * mp.mpf(s))
    vy = fl(mp.mpf(v) * mp.mpf(c))
    return r, v, c, s, x, y, vx, vy


def bits(x):
    return "{:016x}".format(struct.unpack("<Q", struct.pack("<d", x))[0])


def main():
    ds = draws(max(KEPT) + 1)
    lines = []
    for i in KEPT:
        side, k, alpha = ds[i]
        r, v, c, s, x, y, vx, vy = cr_seed(side, k, alpha)
        lines.append(
            f"{i} {int(side)} {bits(k)} {bits(alpha)} "
            f"{bits(r)} {bits(v)} {bits(c)} {bits(s)} {bits(x)} {bits(y)} {bits(vx)} {bits(vy)}"
        )
    print("\n".join(lines))


if __name__ == "__main__":
    main()
