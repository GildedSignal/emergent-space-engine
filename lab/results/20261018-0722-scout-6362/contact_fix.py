#!/usr/bin/env python3
"""The contact skip's one-step integer fix, falsified in float.

Rule under test (contact-speed od 1's named open design question): a detected
crossed-in-bin pair (closest approach inside the detection chronon; 8144:
skip <=> tau* inside the bin) must exchange the exact v1-class impulse. The
shipped receding gate drops it (0 impulse). Candidate fix, from event-driven
MD / game-physics TOI: exchange along the CONTACT ROOT normal, which on the
lattice's own integer data (d, w, R quanta) decomposes as

    n*R = P - s*w ,  P_num = d*W2 - w*(d.w)  (integer, w.P_num == 0 EXACT),
    s = sqrt(D)/W2 , D = (d.w)^2 - W2*(|d|^2 - R^2)  (integer, D>=0 iff hit),
    w.n = -sqrt(D) exactly (w.P = 0),  |n| = R exactly,
    impulse dw = 2*sqrt(D)*P/R^2 - 2*D*w/(W2*R^2)     (closed form).

So the port needs ONE integer square root and ONE divide per component; no
irrational state is carried. The comparison operator (a reflection of the
relative velocity about the root normal) is shared between oracle and rule, so
the SR form of the shipped v1 operator cancels; the toy measures normal and
timing recovery, not the operator.

Arms: b_imp/R in {0, 1/4, 1/2, 39/40}, crossing depth rho=|w|/R in
{3, 30, 300, 512} (beta = rho*R/2^20, up to 1.0), tau*=1/2 (mid-bin).
Controls: miss b=1.5R must not fire (D<0). R=2048 quanta (1648's gas reach),
c = 2^20 quanta/chronon (8144's Q), k=20 fractional bits on the isqrt.
"""
import math

R = 2048
C = 1 << 20
K = 20
TICKS = 1 << K


def arm(b_imp, rho):
    W = int(round(rho * R))
    assert W % 2 == 0
    b = int(round(b_imp * R))
    return (W // 2, b), (-W, 0)


def ints(d, w):
    b_dot = d[0] * w[0] + d[1] * w[1]
    W2 = w[0] * w[0] + w[1] * w[1]
    c0 = d[0] * d[0] + d[1] * d[1] - R * R
    D = b_dot * b_dot - W2 * c0
    Pn = (d[0] * W2 - w[0] * b_dot, d[1] * W2 - w[1] * b_dot)
    return b_dot, W2, D, Pn


def exact(d, w):
    """Oracle: reflect w about the exact root normal; also tau- in chronons."""
    b_dot, W2, D, Pn = ints(d, w)
    if D < 0:
        return None
    sqD = math.sqrt(D)
    tau_m = (-b_dot - sqD) / W2
    P = (Pn[0] / W2, Pn[1] / W2)
    s = sqD / W2
    n = (P[0] - w[0] * s, P[1] - w[1] * s)     # |n| = R exactly
    nn = math.hypot(*n)
    nh = (n[0] / nn, n[1] / nn)
    wdn = w[0] * nh[0] + w[1] * nh[1]
    return (-2 * wdn * nh[0], -2 * wdn * nh[1]), tau_m, D, sqD


def integer_rule(d, w):
    """The fix: ONE isqrt (k frac bits) + ONE divide per component."""
    b_dot, W2, D, Pn = ints(d, w)
    if D < 0:
        return None                              # miss control: never fires
    S = math.isqrt(D << (2 * K))                 # ~ sqrt(D) * 2^K
    # dw = 2*sqrt(D)*P/R^2 - 2*D*w/(W2*R^2), P = Pn/W2:
    #   dw = (2*S*Pn - 2*D*w*2^K) / (2^K * W2 * R^2)  -- one divide/comp
    den = ((W2 * R * R) << K)
    nx = 2 * S * Pn[0] - ((2 * D * w[0]) << K)
    ny = 2 * S * Pn[1] - ((2 * D * w[1]) << K)
    dwx = (nx + den // 2) // den if nx >= 0 else -((-nx + den // 2) // den)
    dwy = (ny + den // 2) // den if ny >= 0 else -((-ny + den // 2) // den)
    # root tick: tau- * 2^K = (-b_dot*2^K - S)/W2 , ceiling
    tau_ticks = ((-b_dot << K) - S + W2 - 1) // W2
    return (dwx, dwy), tau_ticks


def check_identity(d, w):
    b_dot, W2, D, Pn = ints(d, w)
    return w[0] * Pn[0] + w[1] * Pn[1] == 0


def main():
    print(f"constants: R={R} quanta, c={C} quanta/chronon, k={K} bits, "
          f"ticks/chronon={TICKS}")
    arms = [(bi, r) for r in (3, 30, 300, 512)
            for bi in (0.0, 0.25, 0.5, 0.975)]
    print(f"{'b/R':>6} {'rho':>4} {'beta':>6} | {'ship':>5} {'int|dw|':>10} "
          f"{'ex|dw|':>10} {'rec%':>8} {'ang_err':>9} | {'w.P=0':>6} {'D>=0':>5} "
          f"| {'tau-_chr':>9} {'poserr_binend_q':>15} {'poserr_roottick_q':>18}")
    worst_rec, worst_ang = 1e9, 0.0
    for b_imp, rho in arms:
        d, w = arm(b_imp, rho)
        W2 = w[0] * w[0] + w[1] * w[1]
        beta = -w[0] / C
        ex = exact(d, w)
        assert ex is not None
        (ex_dw, tau_m, D, sqD) = ex
        ir = integer_rule(d, w)
        (dw, tau_ticks) = ir
        ex_len = math.hypot(*ex_dw)
        int_len = math.hypot(*dw)
        rec = int_len / ex_len
        ang = math.atan2(dw[0] * ex_dw[1] - dw[1] * ex_dw[0],
                         dw[0] * ex_dw[0] + dw[1] * ex_dw[1])
        pos_binend = (1 - tau_m) * ex_len
        pos_root = abs(tau_m - tau_ticks / TICKS) * ex_len
        worst_rec = min(worst_rec, rec)
        worst_ang = max(worst_ang, abs(ang))
        print(f"{b_imp:6.3f} {rho:4d} {beta:6.3f} | {'0':>5} {int_len:10.0f} "
              f"{ex_len:10.0f} {rec*100:8.4f} {ang:9.2e} | "
              f"{str(check_identity(d, w)):>6} {str(D >= 0):>5} | "
              f"{tau_m:9.5f} {pos_binend:15.1f} {pos_root:18.4f}")
    d, w = arm(1.5, 3)
    print(f"miss control (b=1.5R): fires = {integer_rule(d, w) is not None} "
          f"(must be False); w.P=0 exact = {check_identity(d, w)}")
    print(f"WORST integer recovery {worst_rec*100:.4f}%   "
          f"worst angle {worst_ang:.3e} rad   (shipped recovery on every arm: 0%)")
    random_sweep()


def random_sweep(n=200000, seed=6362):
    """Adversarial: random integer (d, w), arbitrary geometry/phase/sense,
    including already-inside (|d|<R), trailing and non-crossing pairs.
    Checks the integer identity, the miss never firing, and recovery/angle
    on every crossed-in-bin arm."""
    import random
    rnd = random.Random(seed)
    recs, angs, n_cross, n_miss, n_inside = [], [], 0, 0, 0
    for _ in range(n):
        w = (rnd.randint(-8 * R, 8 * R), rnd.randint(-8 * R, 8 * R))
        if w == (0, 0):
            continue
        d = (rnd.randint(-4 * R, 4 * R), rnd.randint(-4 * R, 4 * R))
        b_dot, W2, D, Pn = ints(d, w)
        assert w[0] * Pn[0] + w[1] * Pn[1] == 0
        ex = exact(d, w)
        if ex is None:
            n_miss += 1
            assert integer_rule(d, w) is None      # never fires on a miss
            continue
        n_inside += (d[0] ** 2 + d[1] ** 2 <= R * R)
        (ex_dw, tau_m, D_f, sqD) = ex
        if tau_m < 0 or tau_m > 1:
            continue                                 # not crossed-in-bin class
        n_cross += 1
        (dw, tau_ticks) = integer_rule(d, w)
        ex_len = math.hypot(*ex_dw)
        int_len = math.hypot(*dw)
        recs.append(int_len / ex_len)
        angs.append(abs(math.atan2(dw[0] * ex_dw[1] - dw[1] * ex_dw[0],
                                   dw[0] * ex_dw[0] + dw[1] * ex_dw[1])))
    recs.sort()
    angs.sort()
    print(f"random sweep n={n}: crossed-in-bin {n_cross}, miss {n_miss} "
          f"(never fired), inside-at-start {n_inside}; recovery "
          f"min {recs[0]*100:.4f}% / p1 {recs[len(recs)//100]*100:.4f}% / "
          f"median {recs[len(recs)//2]*100:.4f}%; angle max "
          f"{angs[-1]:.3e} rad / p99 {angs[len(angs)*99//100]:.3e}")


if __name__ == "__main__":
    main()
