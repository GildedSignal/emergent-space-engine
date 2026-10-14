#!/usr/bin/env python3
"""Verify the incomplete-Carlson readout against the shipped walk's dumped states.

For every dumped sample (u, psi, r, tau, adv):
  T = u * period / time_scale (dimensionless), time_scale = p^{3/2};
  invert the closed t(psi) by Newton -> psi_cf; compare psi, r, tau, adv.
Inbound half (T > t(pi)): solve on the reflected target Tt = 2*t(pi) - T (the walk
reflects exactly: here = 2*total - sum), then mirror tau/adv the same way.
"""
import mpmath as mp
import sys

mp.mp.dps = 30


def rf(x, y, z):
    return mp.elliprf(x, y, z)


def rd(x, y, z):
    return mp.elliprd(x, y, z)


def rj(x, y, z, p):
    return mp.elliprj(x, y, z, p)


def F(th, m):
    s, c = mp.sin(th), mp.cos(th)
    return s * rf(c * c, 1 - m * s * s, 1)


def E(th, m):
    s, c = mp.sin(th), mp.cos(th)
    return s * rf(c * c, 1 - m * s * s, 1) - (m * s**3 / 3) * rd(c * c, 1 - m * s * s, 1)


def Pi1(n, th, m):
    s, c = mp.sin(th), mp.cos(th)
    return s * rf(c * c, 1 - m * s * s, 1) + (n / 3) * s**3 * rj(c * c, 1 - m * s * s, 1, 1 - n * s * s)


def I2(n, th, m):
    """int_0^th dt/((1+n sin^2 t)^2 sqrt(1-m sin^2 t)) - Hermite reduction, sympy-solved."""
    D = (n + 1) * (m + n)
    b0 = (m * n + m + n * n / 2 + n) / D
    b1 = -m * n / D
    b2 = -m * n * n / (2 * D)
    q1 = b2 / n
    q0 = (b1 - q1) / n
    cc = b0 - q0
    A_alg = n * n / D
    s, c_, w = mp.sin(th), mp.cos(th), mp.sqrt(1 - m * mp.sin(th) ** 2)
    return (
        q1 * (F(th, m) - E(th, m)) / m
        + q0 * F(th, m)
        + cc * Pi1(-n, th, m)
        + 0.5 * A_alg * s * c_ * w / (1 + n * s * s)
    )


class Closed:
    def __init__(self, k, q):
        self.k, self.q = k, q
        eta = 1 - k
        self.a0 = 2 * k - 1
        self.e = 2 * eta
        self.A = 1 - q * (8 * k - 2)
        self.m = 4 * q * eta / self.A
        self.n3 = self.e  # a0 + e = 1 identically: x = 1 - n3 sin^2 u, u = psi/2
        beta = 1 - 2 * q  # 1 - 2q x at periapsis (x = 1)
        self.n4t = 2 * q * self.e / beta
        self.mg = -self.m / (1 - self.m)  # 1 - m cos^2 u = (1-m)(1 + N sin^2 u), mg = -N
        sq = mp.sqrt(self.A * (1 - self.m))
        tnum = mp.sqrt(k * (1 - 2 * q) * (1 + 2 * q * (1 - 2 * k)))
        taunum = mp.sqrt(k - q * (3 * k * k + eta * eta))
        self.pref_tau = 2 * taunum / sq
        self.pref_t = 2 * tnum / (beta * sq)
        self.pref_adv = 2 / sq
        self.t_num = tnum
        n3, n4 = self.n3, self.n4t
        # 1/((1-n3 v)^2 (1+n4 v)) = a3/(1-n3 v) + b3/(1-n3 v)^2 + c4/(1+n4 v), v = sin^2 u
        M = mp.matrix([[1, 1, 1], [n4 - n3, n4, -2 * n3], [-n3 * n4, 0, n3 * n3]])
        sol = mp.lu_solve(M, mp.matrix([1, 0, 0]))
        self.a3, self.b3, self.c4 = sol[0], sol[1], sol[2]

    def t(self, psi):
        u = mp.mpf(psi) / 2
        return self.pref_t * (
            self.a3 * Pi1(self.n3, u, self.mg)
            + self.b3 * I2(-self.n3, u, self.mg)
            + self.c4 * Pi1(-self.n4t, u, self.mg)
        )

    def tau(self, psi):
        return self.pref_tau * I2(-self.n3, mp.mpf(psi) / 2, self.mg)

    def adv(self, psi):
        return self.pref_adv * F(mp.mpf(psi) / 2, self.mg) - mp.mpf(psi)

    def dt(self, psi):
        k, q = self.k, self.q
        x = k + (1 - k) * mp.cos(psi)
        a = 2 * x + 4 * k
        g = 1 / mp.sqrt(1 - q * a)
        return self.t_num * g / (x * x * (1 - 2 * q * x))
    def invert_t(self, T, psi0):
        lo, hi = mp.mpf("1e-12"), mp.pi - mp.mpf("1e-12")
        psi = min(max(mp.mpf(psi0), lo), hi)
        for _ in range(80):
            step = (T - self.t(psi)) / self.dt(psi)
            if self.t(lo) > T or self.t(hi) < T:
                return None  # target outside the outbound half
            nxt = psi + step
            if not (lo < nxt < hi):
                nxt = (lo + hi) / 2
            if self.t(nxt) < T:
                lo = nxt
            else:
                hi = nxt
            if abs(nxt - psi) < mp.mpf("1e-18"):
                return nxt
            psi = nxt
        return psi

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "shipped_dump.txt"
    samples = {}
    for line in open(path):
        f = line.split()
        if not f:
            continue
        if f[0] == "KEY":
            d = dict(x.split("=") for x in f[1:])
            samples[(d["p"], d["e"])] = {"meta": d, "rows": []}
        elif f[0] == "S":
            d = dict(x.split("=") for x in f[1:])
            samples[(d["p"], d["e"])]["rows"].append(d)
    worst = {"psi": 0.0, "r": 0.0, "tau": 0.0, "adv": 0.0}
    worst_at = {}
    n_ok = n_tot = 0
    items = list(samples.items())
    for (p, e), blk in items[::3]:
        p, e = float(p), float(e)
        k = 1.0 / (1.0 + e)
        q = 1.0 / p
        c = Closed(mp.mpf(k), mp.mpf(q))
        period = mp.mpf(blk["meta"]["period"])
        ts = mp.mpf(p) ** 1.5
        pdim = period / ts
        t_half = c.t(mp.pi)
        for row in blk["rows"]:
            u = mp.mpf(row["u"])
            psi_w = mp.mpf(row["psi"])
            T = u * pdim
            outbound = T <= t_half
            Tt = T if outbound else 2 * t_half - T
            psi0 = min(max(mp.pi * Tt / t_half, mp.mpf("1e-9")), mp.pi - mp.mpf("1e-9"))
            psi_cf = c.invert_t(Tt, psi0)
            if psi_cf is None:
                n_tot += 1
                continue
            n_tot += 1
            if abs(psi_cf - psi_w) < mp.mpf("1e-6"):
                n_ok += 1
                s_tau = c.tau(psi_cf) if outbound else 2 * c.tau(mp.pi) - c.tau(psi_cf)
                s_adv = c.adv(psi_cf) if outbound else 2 * c.adv(mp.pi) - c.adv(psi_cf)
                for name, mine, theirs in [
                    ("psi", psi_cf, psi_w),
                    ("r", mp.mpf(p) / (k + (1 - k) * mp.cos(psi_cf)), mp.mpf(row["r"])),
                    ("tau", s_tau * ts, mp.mpf(row["tau"])),
                    ("adv", s_adv, mp.mpf(row["adv"])),
                ]:
                    rel = float(abs(mine - theirs) / max(abs(theirs), 1e-12))
                    if rel > worst[name]:
                        worst[name] = rel
                        worst_at[name] = (p, e, float(u))
            else:
                rel = float(abs(psi_cf - psi_w) / max(abs(psi_w), 1e-9))
                if rel > worst["psi"]:
                    worst["psi"] = rel
                    worst_at["psi"] = (p, e, float(u), "NEWTON-DIVERGED")
    print(f"converged-agreement: {n_ok}/{n_tot}")
    for name in ["psi", "r", "tau", "adv"]:
        print(f"worst rel err {name}: {worst[name]:.3e} at {worst_at.get(name)}")


if __name__ == "__main__":
    main()
