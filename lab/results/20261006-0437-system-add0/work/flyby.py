#!/usr/bin/env python3
"""B13 flyby replica (float, Newtonian, 2D): does the epoch rule decide the gate?

Scene = the plane's star doll: Sun fixed at the origin, Jupiter on an exact circular
heliocentric tube, one ship. Truth = adaptive RKF45 on the heliocentric equation

    r'' = -mu_S r/|r|^3 + mu_J [(r_J - r)/|r_J - r|^3 - r_J/|r_J|^3]

(CR3BP in the non-rotating frame; the bracket's second term is the origin's fall,
force.rs's indirect term). Metric = B13's: the change of the ship's heliocentric
orbital energy E and angular momentum L across the encounter window (from 2.5 R_edge
before to 2.5 R_edge after), vs the truth's change, in relative error.

The candidates share every component: the WH split (drift = exact two-body Kepler
about the doll's centre in force), the SyMBA telescoping changeover (each level l
applies its own share W_l(r) of Jupiter's pull at its own cadence H/4^l; `engaged`
(force.rs) decides when a finer level must be scheduled), the handoff at R_edge/4 in
and R_edge out (4:1 hysteresis), and the full differential solar tide inside
Jupiter's doll. Only the EPOCH RULE differs:

  A 'phase'  : the plane's rule - H = radial period / 64 in the star doll (clamped
               to hmax_star) and H = passage duration / 64 in Jupiter's doll
               (crates/universe/src/step.rs::step_for).
  B 'events' : H = (time to the next tube event)/4 - the events are the crossings of
               the shell ladder and the periapsis of the current conic: the exact
               quantity that A's `engaged` certificate only guards as a boolean.
  C 'fine'   : A with H = r_p/(64 v_p) inside Jupiter's doll (an oracle cadence that
               knows the answer; the positive control).

Float replica: it tests the CONFIGURATION (the epoch rule), not the integer law.
"""
import json
import math
import sys

MU_S = 4.0 * math.pi * math.pi
MU_J = MU_S / 1047.06
A_J = 5.2
R_J = 71492.0 / 1.495978707e8
R_EDGE = A_J * (1.0 / 1047.06) ** 0.4
V_JUP = math.sqrt(MU_S / A_J)
KMS = 3.1558149e7 / 1.495978707e8
LEVELS = 3
HMIN = 1.0e-6

NORM = lambda p: math.hypot(p[0], p[1])
DOT = lambda a, b: a[0] * b[0] + a[1] * b[1]
ADD = lambda a, b: (a[0] + b[0], a[1] + b[1])
SUB = lambda a, b: (a[0] - b[0], a[1] - b[1])
MUL = lambda a, s: (a[0] * s, a[1] * s)


def jupiter(t):
    th = t * V_JUP / A_J
    return (A_J * math.cos(th), A_J * math.sin(th)), (-V_JUP * math.sin(th), V_JUP * math.cos(th))


# ------------------------------------------------------- universal Kepler drift
def _stumpff(z):
    if z > 1e-8:
        s = math.sqrt(z)
        return (1.0 - math.cos(s)) / z, (s - math.sin(s)) / (s * s * s)
    if z < -1e-8:
        s = min(math.sqrt(-z), 600.0)
        return (math.cosh(s) - 1.0) / (-z), (math.sinh(s) - s) / (-z) ** 1.5
    C = 0.5 - z / 24.0 + z * z / 720.0 - z ** 3 / 40320.0
    S = 1.0 / 6.0 - z / 120.0 + z * z / 5040.0 - z ** 3 / 362880.0
    return C, S


def drift(r, v, mu, dt):
    if dt == 0.0:
        return r, v
    r0, v0 = NORM(r), NORM(v)
    rdv = DOT(r, v)
    alpha = 2.0 / r0 - v0 * v0 / mu
    sq = math.sqrt(mu)
    chi = sq * dt * alpha if alpha > 1e-12 else sq * dt / r0
    for _ in range(60):
        z = alpha * chi * chi
        C, S = _stumpff(z)
        F = (rdv / sq) * chi * chi * C + (1.0 - alpha * r0) * chi ** 3 * S + r0 * chi - sq * dt
        dF = (rdv / sq) * chi * (1.0 - z * S) + (1.0 - alpha * r0) * chi * chi * C + r0
        d = F / dF
        chi -= d
        if abs(d) < 1e-12 * max(1.0, abs(chi)):
            break
    z = alpha * chi * chi
    C, S = _stumpff(z)
    f = 1.0 - chi * chi / r0 * C
    g = dt - chi ** 3 / sq * S
    rn = (f * r[0] + g * v[0], f * r[1] + g * v[1])
    rn2 = DOT(rn, rn)
    fd = sq / (r0 * math.sqrt(rn2)) * chi * (z * S - 1.0)
    gd = 1.0 - chi * chi / math.sqrt(rn2) * C
    vn = (fd * r[0] + gd * v[0], fd * r[1] + gd * v[1])
    return rn, vn


def conic_period(r, v, mu):
    r0, v0 = NORM(r), NORM(v)
    a = 1.0 / (2.0 / r0 - v0 * v0 / mu)
    return 2.0 * math.pi * math.sqrt(a * a * a / mu) if a > 0.0 else float("inf")


def conic_elems(rho, u, mu):
    En = 0.5 * DOT(u, u) - mu / NORM(rho)
    L = rho[0] * u[1] - rho[1] * u[0]
    e = math.sqrt(max(1.0 + 2.0 * En * L * L / (mu * mu), 0.0))
    a = -mu / (2.0 * En)
    rp = abs(a) * abs(1.0 - e)
    vp = math.sqrt(max(2.0 * (En + mu / max(rp, 1e-12)), 1e-12))
    return a, e, rp, vp


def leg_to_edge(a, e):
    """Hyperbolic time from periapsis to r = R_EDGE, from elements (step_for's leg)."""
    try:
        He = math.acosh(max(1.0, (1.0 - R_EDGE / a) / e))
        M = e * math.sinh(He) - He
        return math.sqrt((-a) ** 3 / MU_J) * M
    except (ValueError, ZeroDivisionError, OverflowError):
        return None


# ------------------------------------------------------------------- truth
_A = [None, [1 / 4, 1 / 4], [3 / 8, 3 / 32, 9 / 32],
      [12 / 13, 1932 / 2197, -7200 / 2197, 7296 / 2197],
      [1, 439 / 216, -8, 3680 / 513, -845 / 4104],
      [1 / 2, -8 / 27, 2, -3544 / 2565, 1859 / 4104, -11 / 40]]
_B4 = [25 / 216, 0, 1408 / 2565, 2197 / 4104, -1 / 5]
_B5 = [16 / 135, 0, 6656 / 12825, 28561 / 56430, -9 / 50, 2 / 55]


def _accel_true(t, y):
    r = (y[0], y[1])
    rJ, _ = jupiter(t)
    d = SUB(rJ, r)
    g1 = -MU_S / NORM(r) ** 3
    g2 = MU_J / NORM(d) ** 3
    g3 = -MU_J / A_J ** 3
    return (y[2], y[3], g1 * r[0] + g2 * d[0] + g3 * rJ[0], g1 * r[1] + g2 * d[1] + g3 * rJ[1])


def truth_pass(r0, v0, tmax=6.0, tol=1e-12):
    """Adaptive RKF45; stops at the first 'beyond 2.5 R_edge and receding'.

    Returns (t_exit, final position, final velocity, closest approach to Jupiter)."""
    y = [r0[0], r0[1], v0[0], v0[1]]
    t = 0.0
    h = 1e-4
    ca = 1e9
    while t < tmax:
        rJ, vJ = jupiter(t)
        d = SUB((y[0], y[1]), rJ)
        if t > 0.0 and NORM(d) > 1.3 * R_EDGE and DOT(d, SUB((y[2], y[3]), vJ)) > 0.0:
            return t, (y[0], y[1]), (y[2], y[3]), ca
        k = [_accel_true(t, y)]
        for i in range(1, 6):
            yy = [y[j] + h * sum(_A[i][m] * k[m - 1][j] for m in range(1, i + 1)) for j in range(4)]
            k.append(_accel_true(t + _A[i][0] * h, yy))
        y5 = [y[j] + h * sum(b * k[m][j] for m, b in enumerate(_B5)) for j in range(4)]
        err = max(abs(y[j] + h * sum(b * k[m][j] for m, b in enumerate(_B4)) - y5[j]) for j in range(4))
        sc = tol * max(1.0, max(abs(x) for x in y))
        if err <= sc:
            t += h
            y = y5
            rJ, _ = jupiter(t)
            ca = min(ca, NORM(SUB((y[0], y[1]), rJ)))
        fac = (sc / max(err, 1e-300)) ** 0.25 if err > sc else 1.6
        h = max(1e-9, min(0.05, h * max(0.15, min(3.0, fac))))
    return tmax, (y[0], y[1]), (y[2], y[3]), ca


# --------------------------------------------------- tube events (the exact times)
def _prop_rel(r, v, t, dt, centre_jup):
    if centre_jup:
        rJ, vJ = jupiter(t)
        rho, u = drift(SUB(r, rJ), SUB(v, vJ), MU_J, dt)
        rJ2, vJ2 = jupiter(t + dt)
        return ADD(rho, rJ2), ADD(u, vJ2)
    return drift(r, v, MU_S, dt)


def _root(fn, t, tmax, g0, tau0=1e-7):
    """First zero of fn(t+tau) for tau in (0, tmax): scan (growth 1.3) + bisection.

    The first sample is scaled to the local crossing time so a fast encounter's
    dip-and-return is never jumped over."""
    tau = tau0
    n = 0
    while tau < tmax and n < 400:
        g1 = fn(t + tau)
        if g0 * g1 <= 0.0:
            lo, hi = tau / 1.3, tau
            for _ in range(70):
                mid = 0.5 * (lo + hi)
                if fn(t + mid) * g0 > 0.0:
                    lo = mid
                else:
                    hi = mid
            return 0.5 * (lo + hi)
        g0 = g1
        tau *= 1.3
        n += 1
    return None


def next_crossing(r, v, t, R, centre_jup, tmax=4.0):
    def gap(tt):
        rr, _ = _prop_rel(r, v, t, tt - t, centre_jup)
        return NORM(SUB(rr, jupiter(tt)[0])) - R
    rJ, vJ = jupiter(t)
    speed = NORM(SUB(v, vJ))
    tau0 = max(1e-9, min(1e-7, abs(gap(t + 1e-12)) / (speed + 1e-9) / 4.0))
    return _root(gap, t, tmax, gap(t + 1e-12), tau0)


def next_periapsis(r, v, t, centre_jup, tmax=1.0):
    def rdv(tt):
        rr, vv = _prop_rel(r, v, t, tt - t, centre_jup)
        if centre_jup:
            rJ, vJ = jupiter(tt)
            rr, vv = SUB(rr, rJ), SUB(vv, vJ)
        return DOT(rr, vv)
    g0 = rdv(t + 1e-12)
    if g0 > 0.0:            # already receding: no periapsis ahead on this conic
        return None
    return _root(rdv, t, tmax, g0)


# ------------------------------------------------------------ the candidates
def smooth(y):
    y = max(0.0, min(1.0, y))
    return y * y * (3.0 - 2.0 * y)


def shell_R(l):
    return R_EDGE * 2.0 ** (1 - l)


def boundary(r, big_r):
    return smooth((r - big_r / 2.0) / (big_r / 2.0))


def weight(l, r):
    w = 1.0
    for i in range(l):
        w *= 1.0 - boundary(r, shell_R(i))
    if l < LEVELS:
        w *= boundary(r, shell_R(l))
    return w


def engaged(l, r, speed, h):
    return r - 1.25 * speed * h < shell_R(l)


class Handoff(Exception):
    def __init__(self, t):
        self.t = t


def run_candidate(r0, v0, t1, mode, hmax_star=0.5):
    """State: (r, v) heliocentric in the star doll; (rho, u) planetocentric in Jupiter's."""
    r = v = None
    rho = u = None
    t = 0.0
    in_jup = False
    r, v = r0, v0
    kicks = 0
    guard = 0

    def star_walk(t, h, l):
        """Telescoping SyMBA: level l applies W_l over [t, t+h]; finer levels inside."""
        nonlocal r, v, kicks
        rJ, vJ = jupiter(t)
        dn = NORM(SUB(r, rJ))
        speed = NORM(SUB(v, vJ))
        if l < LEVELS and engaged(l, dn, speed, h):
            q = h / 4.0
            star_walk(t, q, l + 1)
            star_walk(t + q, q, l + 1)
            # level-l share at the interval midpoint (state is there now)
            apply_star_kick(t + h / 2.0, l, h)
            star_walk(t + h / 2.0, q, l + 1)
            star_walk(t + 3 * q, q, l + 1)
        else:
            rm, vm = drift(r, v, MU_S, 0.5 * h)
            r, v = rm, vm
            apply_star_kick(t + 0.5 * h, l, h)
            r, v = drift(r, v, MU_S, 0.5 * h)

    def apply_star_kick(tm, l, h):
        nonlocal r, v, kicks
        rJm, _ = jupiter(tm)
        d = SUB(rJm, r)
        dn = NORM(d)
        a = MUL(d, MU_J / dn ** 3 * weight(l, dn))
        if l == 0:
            a = SUB(a, MUL(rJm, MU_J / A_J ** 3))
        v = (v[0] + a[0] * h, v[1] + a[1] * h)
        kicks += 1
        if not in_jup and NORM(SUB(r, jupiter(tm)[0])) < R_EDGE / 4.0:
            raise Handoff(tm)

    def jup_step(t, h):
        nonlocal rho, u, kicks
        rJ, _ = jupiter(t)
        rhom, um = drift(rho, u, MU_J, 0.5 * h)
        rr = ADD(rJ, rhom)
        a = SUB(MUL(rr, -MU_S / NORM(rr) ** 3), MUL(rJ, -MU_S / A_J ** 3))
        um = (um[0] + a[0] * h, um[1] + a[1] * h)
        kicks += 1
        rho, u = drift(rhom, um, MU_J, 0.5 * h)

    while t < t1 - 1e-12:
        guard += 1
        if guard > 2_000_000:
            raise RuntimeError("step guard")
        if in_jup:
            rJ, vJ = jupiter(t)
            if NORM(rho) > R_EDGE:
                in_jup = False
                r, v = ADD(rJ, rho), ADD(vJ, u)
                rho = u = None
        if not in_jup:
            if mode in ("A", "C"):
                h = min(conic_period(r, v, MU_S) / 64.0, hmax_star)
            else:
                evs = [next_crossing(r, v, t, R, False) for R in (2.0 * R_EDGE, R_EDGE, R_EDGE / 2.0, R_EDGE / 4.0)]
                p = next_periapsis(r, v, t, False, tmax=4.0)
                if p is not None:
                    evs.append(p)
                te = min([e for e in evs if e is not None], default=1.0)
                h = min(conic_period(r, v, MU_S) / 64.0, te * (1.0 + 1e-9), hmax_star)
            h = max(min(h, t1 - t), HMIN)
            try:
                star_walk(t, h, 0)
                t += h
            except Handoff as ho:
                t = ho.t
                rJ, vJ = jupiter(t)
                in_jup = True
                rho, u = SUB(r, rJ), SUB(v, vJ)
                r = v = None
        else:
            _, _, rp, vp = conic_elems(rho, u, MU_J)
            if mode == "A":
                leg = leg_to_edge(*conic_elems(rho, u, MU_J)[:2])
                h = (2.0 * leg if leg else 2.0 * rp / vp) / 64.0
            elif mode == "C":
                h = rp / (64.0 * vp)
            else:
                evs = []
                R = R_EDGE
                rJ, vJ = jupiter(t)
                while R > max(1.5 * rp, 1e-9):
                    c = next_crossing(ADD(rJ, rho), ADD(vJ, u), t, R, True, tmax=1.0)
                    if c is not None:
                        evs.append(c)
                    R *= 0.5
                p = next_periapsis(ADD(rJ, rho), ADD(vJ, u), t, True)
                if p is not None:
                    evs.append(p)
                te = min(evs) if evs else 0.25
                h = max(te * (1.0 + 1e-9), HMIN)
            h = max(min(h, t1 - t), HMIN)
            jup_step(t, h)
            t += h
    if in_jup:
        rJ, vJ = jupiter(t1)
        r, v = ADD(rJ, rho), ADD(vJ, u)
    return r, v, kicks


# ------------------------------------------------------------------- seeds
def seed_from_b(vinf, w, n, b):
    d0 = 1.3 * R_EDGE
    L = math.sqrt(max(d0 * d0 - b * b, 1e-12))
    rJ, vJ = jupiter(0.0)
    r = ADD(SUB(rJ, MUL(w, L)), MUL(n, b))
    v = ADD(vJ, MUL(w, vinf))
    return r, v


def make_seed(vinf_kms, rp_target, phi_deg, side, refine=True):
    """Aim for periapsis ~ rp_target; refine b against the truth (solar bending)."""
    vinf = vinf_kms * KMS
    rp = rp_target * R_J
    b = rp * math.sqrt(1.0 + 2.0 * MU_J / (rp * vinf * vinf))
    phi = math.radians(phi_deg)
    w = (-math.cos(phi), -math.sin(phi))
    n = (-w[1] * side, w[0] * side)
    r0, v0 = seed_from_b(vinf, w, n, b)
    if not refine:
        return r0, v0
    ca = target = None
    for _ in range(3):
        _, _, _, ca = truth_pass(r0, v0)
        if ca > 0.3 * R_J and abs(ca - rp) < 0.25 * rp:
            break
        if ca < 1e-6:
            ca = 1e-6
        b *= math.sqrt(rp / ca)          # b ~ rp sqrt(1 + 2mu/(rp vinf^2)): mild rescale
        r0, v0 = seed_from_b(vinf, w, n, b)
    return r0, v0


def helio_e(r, v):
    En = 0.5 * DOT(v, v) - MU_S / NORM(r)
    L = r[0] * v[1] - r[1] * v[0]
    return math.sqrt(max(1.0 + 2.0 * En * L * L / (MU_S * MU_S), 0.0))


def energy_l(r, v):
    return 0.5 * DOT(v, v) - MU_S / NORM(r), r[0] * v[1] - r[1] * v[0]


def para_phi(vinf_kms):
    """Relative-velocity angle that makes the heliocentric orbit near-parabolic."""
    vinf = vinf_kms * KMS
    vesc = math.sqrt(2.0 * MU_S / A_J)
    c = (vesc * vesc - V_JUP * V_JUP - vinf * vinf) / (2.0 * V_JUP * vinf)
    if not -1.0 <= c <= 1.0:
        return None
    psi = math.acos(c)
    return math.degrees(math.atan2(-math.sin(psi), -math.cos(psi)))


def main():
    seeds = []
    for vinf in (5.0, 8.0, 12.0, 16.0, 20.0):
        phis = [-35.0, 25.0]
        pp = para_phi(vinf)
        if pp is not None:
            phis.append(pp)
        for rp in (1.2, 3.0, 10.0, 30.0, 50.0):
            for phi in phis:
                side = 1 if phi == phis[0] else -1
                seeds.append((vinf, rp, phi, side))
    rows = []
    for idx, (vinf, rp, phi, side) in enumerate(seeds):
        r0, v0 = make_seed(vinf, rp, phi, side)
        t1, rft, vft, ca = truth_pass(r0, v0)
        E0, L0 = energy_l(r0, v0)
        E1t, L1t = energy_l(rft, vft)
        dEt, dLt = E1t - E0, L1t - L0
        row = {"i": idx, "vinf": vinf, "rp_t": rp, "phi": phi, "e": round(helio_e(r0, v0), 4),
               "ca_RJ": round(ca / R_J, 2), "t1": round(t1, 3),
               "dEt": dEt, "dLt": dLt}
        configs = [("A", 0.5), ("A2", 2.0), ("A01", 0.1), ("A002", 0.02), ("B", 0.5), ("C", 0.5)]
        for mode, hm in configs:
            rf, vf, kk = run_candidate(r0, v0, t1, mode[-1] if mode[0] == "A" else mode, hmax_star=hm)
            E1, L1 = energy_l(rf, vf)
            row[f"{mode}_errE"] = abs(E1 - E0 - dEt) / max(abs(dEt), 1e-14)
            row[f"{mode}_errL"] = abs(L1 - L0 - dLt) / max(abs(dLt), 1e-14)
            row[f"{mode}_kicks"] = kk
            okL = row[f"{mode}_errL"] <= 0.01 or abs(dLt) < 1e-4   # degenerate dL: not judged
            row[f"{mode}_pass"] = row[f"{mode}_errE"] <= 0.01 and okL
        rows.append(row)
        print(json.dumps(row), flush=True)
    out = sys.argv[1] if len(sys.argv) > 1 else "rows.json"
    with open(out, "w") as f:
        json.dump(rows, f, indent=1)
    for mode in ("A", "A2", "A01", "A002", "B", "C"):
        n = sum(1 for x in rows if x[f"{mode}_pass"])
        worst = max(max(x[f"{mode}_errE"], x[f"{mode}_errL"]) for x in rows)
        kicks = sum(x[f"{mode}_kicks"] for x in rows)
        print(f"{mode}: {n}/{len(rows)} pass, worst rel err {worst:.3g}, total kicks {kicks}", file=sys.stderr)


if __name__ == "__main__":
    main()
