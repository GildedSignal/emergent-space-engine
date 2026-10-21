#!/usr/bin/env python3
"""Arrival time of light at a rotating doll: exact Kerr equatorial null geodesics
vs the view letter's chi-blind delay(b) column (representation.md L57 gather;
5977/9f4a/fb64's cure spec; 8be2's "Shapiro unmemoized").

M = 1, E = 1, L = signed impact parameter b (prograde > 0 when a > 0), Q = 0.
  Delta = r^2 - 2r + a^2 ;  P = (r^2 + a^2) - a L ;  R = P^2 - Delta (L - a)^2
  r^2 dt/dlam = a(L-a) + (r^2+a^2) P / Delta ;  dr/dlam = +/- sqrt(R)/r^2

Direct (primary) image only: photon emitted at r_e on the outward branch,
R > 0 on the whole path [r_e, r_o]; its closest approach is r_e itself.
Geometry note (found by the instrument, pre-decisive): at r_e an outward photon
obeys |b| <= b_max(r_e) = r_e / sqrt(1 - 2 r_e^-1) at a = 0 (7.348 at r_e = 6),
so the strong-field scene flies b <= 7 and fb64's b >= 8 regime moves to r_e = 20.
"""
import math

SCENES = {"A_r6": (6.0, (5.0, 6.0, 7.0)), "B_r20": (20.0, (8.0, 8.5, 12.0, 20.0))}
CHIS = (0.5, 0.9, 0.998)


def Delta(r, a):   return r * r - 2.0 * r + a * a
def bigP(r, a, L): return (r * r + a * a) - a * L
def bigR(r, a, L):
    P = bigP(r, a, L)
    return P * P - Delta(r, a) * (L - a) * (L - a)


def integrand(r, a, L):
    P = bigP(r, a, L)
    return (a * (L - a) + (r * r + a * a) * P / Delta(r, a)) / math.sqrt(bigR(r, a, L))


def path_ok(r_e, r_o, a, L):
    n = 4000
    for i in range(n + 1):
        r = r_e + (r_o - r_e) * i / n
        if bigR(r, a, L) <= 1e-9 * max(1.0, r ** 4):
            return False
    return True


def gl_nodes(n):
    xs, ws = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        dp = 1.0
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1.0)
            dx = -p1 / dp
            x += dx
            if abs(dx) < 1e-15:
                break
        xs.append(x); ws.append(2.0 / ((1 - x * x) * dp * dp))
    return xs, ws


GL10 = gl_nodes(10)


def t_quad(r_e, r_o, a, L, panels=8000):
    xs, ws = GL10
    total = 0.0
    for i in range(panels):
        r0 = r_e + (r_o - r_e) * i / panels
        h = (r_o - r_e) / panels / 2.0
        c = r0 + h
        s = 0.0
        for x, w in zip(xs, ws):
            s += w * integrand(c + h * x, a, L)
        total += h * s
    return total


def t_rk4(r_e, r_o, a, L, n=2_000_000):
    """Independent scheme: classical RK4 in the independent variable r."""
    def dtdr(r):  return integrand(r, a, L)
    h = (r_o - r_e) / n
    r, t = r_e, 0.0
    while r < r_o - 1e-12:
        hh = min(h, r_o - r)
        k1 = dtdr(r); k2 = dtdr(r + hh / 2); k3 = dtdr(r + hh / 2); k4 = dtdr(r + hh)
        t += hh * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        r += hh
    return t


def flat_time(r_e, r_o, b):
    return math.sqrt(r_o * r_o - b * b) + math.sqrt(r_e * r_e - b * b)


def main():
    r_o = 100.0

    print("== C+ instrument: RK4(in r) vs Gauss-Legendre, a = 0 (both scenes) ==")
    worst = 0.0
    for name, (r_e, bs) in SCENES.items():
        for b in bs:
            tq, tr = t_quad(r_e, r_o, 0.0, b), t_rk4(r_e, r_o, 0.0, b)
            worst = max(worst, abs(tq - tr))
            print(f"  {name} b={b:5.1f}  quad={tq:.9f}  rk4={tr:.9f}  |d|={abs(tq-tr):.2e}")
    print(f"  worst |quad-rk4| = {worst:.2e}  -> {'PASS' if worst < 1e-6 else 'FAIL'}")

    print("== C+ physics: Shapiro log coefficient at a = 0, r_e = 20 (dt = c*ln(4 r_o r_e/b^2)) ==")
    for b in (8.0, 12.0, 20.0):
        dt = t_quad(20.0, r_o, 0.0, b) - flat_time(20.0, r_o, b)
        c = dt / math.log(4 * r_o * 20.0 / (b * b))
        print(f"  b={b:5.1f}  dt_Schw={dt:8.4f} M  c_fit={c:.4f}")

    print("== C- instrument: sense symmetry t(a=0.9, retro b) = t(a=-0.9, pro |b|), r_e=20 ==")
    t1, t2 = t_quad(20.0, r_o, 0.9, -12.0), t_quad(20.0, r_o, -0.9, 12.0)
    print(f"  {t1:.12f} vs {t2:.12f}  |d|={abs(t1-t2):.2e} -> {'PASS' if abs(t1-t2) < 1e-9 else 'FAIL'}")
    print("== C- instrument: step halving (panels 8000 -> 16000), chi=0.998 pro b=6 r_e=6 ==")
    t1 = t_quad(6.0, r_o, 0.998, 6.0); t2 = t_quad(6.0, r_o, 0.998, 6.0, panels=16000)
    print(f"  {t1:.12f} vs {t2:.12f}  |d|={abs(t1-t2):.2e} -> {'PASS' if abs(t1-t2) < 1e-9 else 'FAIL'}")

    for name, (r_e, bs) in SCENES.items():
        print(f"\n== {name}: chi-blind delay(b) error  (err = t_exact - t_static, M units) ==")
        t_static = {b: t_quad(r_e, r_o, 0.0, b) for b in bs}
        print(f"  {'chi':>5} {'sense':>5} {'b':>5} {'t_exact':>10} {'err':>9} {'dSchw':>8} {'err/d':>7} {'ph_deg':>7}")
        for chi in CHIS:
            for sense in ("pro", "retro"):
                sgn = 1.0 if sense == "pro" else -1.0
                for b in bs:
                    L = sgn * b
                    if not path_ok(r_e, r_o, chi, L):
                        print(f"  {chi:5.3f} {sense:>5} {b:5.1f}   (no direct outward branch)")
                        continue
                    te = t_quad(r_e, r_o, chi, L)
                    err = te - t_static[b]
                    dts = t_static[b] - flat_time(r_e, r_o, b)
                    om = 1.0 / (r_e ** 1.5 + chi)
                    ph = math.degrees(om * abs(err))
                    print(f"  {chi:5.3f} {sense:>5} {b:5.1f} {te:10.4f} {err:+9.4f} {dts:8.4f} {err/dts:+7.3f} {ph:7.1f}")

    print("\n== P2: sense split at same |b| (chi=0.998, b=8.5, r_e=20) ==")
    tp, tr = t_quad(20.0, r_o, 0.998, 8.5), t_quad(20.0, r_o, 0.998, -8.5)
    dts = t_quad(20.0, r_o, 0.0, 8.5) - flat_time(20.0, r_o, 8.5)
    print(f"  |pro-retro| = {abs(tp-tr):.4f} M   vs delay_Schw = {dts:.4f} M   ratio = {abs(tp-tr)/dts:.3f}")

    print("\n== P3: linearity in a (r_e=20, b=12, pro) ==")
    t0 = t_quad(20.0, r_o, 0.0, 12.0)
    t25 = t_quad(20.0, r_o, 0.25, 12.0); t50 = t_quad(20.0, r_o, 0.5, 12.0)
    print(f"  [t(0.5)-t(0)]/[t(0.25)-t(0)] = {(t50-t0)/(t25-t0):.4f}")

    print("\n== P5: weak-field edge (r_e=20, b=20, chi=0.5) ==")
    te = t_quad(20.0, r_o, 0.5, 20.0)
    dts = t_quad(20.0, r_o, 0.0, 20.0) - flat_time(20.0, r_o, 20.0)
    err = te - t_quad(20.0, r_o, 0.0, 20.0)
    print(f"  err = {err:+.4f} M  ({err/dts:+.5f} of delay_Schw = {dts:.4f} M)")


if __name__ == "__main__":
    main()
