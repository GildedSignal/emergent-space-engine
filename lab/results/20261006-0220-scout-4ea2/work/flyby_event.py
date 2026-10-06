#!/usr/bin/env python3
"""B13 near-parabolic flybys: per-passage cadence vs the encounter-as-event (scout run 20261006-0220).

Scene and protocol transcribed exactly from xtask/src/behave/{restricted,assist}.rs:
star (1-mu) + planet mu on a circle, mu=1e-3, sep=5.27e8, R_p=4.84e4, units G=M_tot=1.
Judge: heliocentric dE, dL from t=0 (start 1.5*SOI inbound) to t_exit (first r>1.5*SOI
after entering SOI, within one planet period), gate 1% in both. Truth: DOP853 rtol 1e-12,
convergence checked against 1e-13 (the gate's own rule, 1e-4).

Laws (all answer the heliocentric state at the truth's t_exit):
  L1 starved cadence  : heliocentric DKD, H = 2^round(log2(T_pass/64)), T_pass = twice the
                        periapsis-to-start leg of the heliocentric conic (the plane's star-doll
                        rule, judged alone: no changeover, no doll).
  L2 one event        : patched conics (Öpik/Valsecchi): heliocentric Kepler outside a patch
                        sphere R_pch, one exact planetocentric hyperbola inside, analytic
                        entry/exit (root-finding on the two conics; no stepping).
  L3 event + interior : analytic entry as L2; inside, DKD with planetocentric Kepler drift and
                        star-tide kicks at H_in = 2^floor(log2(T_enc/64)) (the plane's own
                        in-doll rule); exit at the outward patch crossing; heliocentric Kepler
                        after. Events: 1 detection + <=~64 in-doll kicks + 1 exit + 1 rebind.
Floats explore; the structure is the claim. Nothing is tuned here.
"""
import json
import math

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

# ---------------------------------------------------------------- scene (restricted.rs)
MU = 1e-3
SEP = 5.27e8
R_PLANET = 4.84e4
OMEGA = SEP ** -1.5
PERIOD = 2 * math.pi * SEP ** 1.5
SOI = SEP * MU ** 0.4
START_SOI = 1.5
MU_STAR = 1.0 - MU


def planet_state(t):
    th = OMEGA * t
    c, s = math.cos(th), math.sin(th)
    r, v = SEP * (1 - MU), SEP * (1 - MU) * OMEGA
    return np.array([r * c, r * s]), np.array([-v * s, v * c])


def star_state(t):
    th = OMEGA * t
    c, s = math.cos(th), math.sin(th)
    r, v = SEP * MU, SEP * MU * OMEGA
    return np.array([-r * c, -r * s]), np.array([v * s, -v * c])


def ship_bary(q_rp, v_inf, psi):
    """assist.rs ship(): on the incoming hyperbola at 1.5*SOI, planet velocity added."""
    q = q_rp * R_PLANET
    e = 1.0 + q * v_inf * v_inf / MU
    p = q * (1.0 + e)
    r = START_SOI * SOI
    nu = -math.acos((p / r - 1.0) / e)
    angle = psi + math.acos(-1.0 / e) + nu
    h = math.sqrt(MU * p)
    radial, along = MU / h * e * math.sin(nu), h / r
    s, c = math.sin(angle), math.cos(angle)
    rel = np.array([r * c, r * s, radial * c - along * s, radial * s + along * c])
    pp, pv = planet_state(0.0)
    return rel + np.array([pp[0], pp[1], pv[0], pv[1]])


def helio_E_L(r, v):
    return (0.5 * v @ v - MU_STAR / math.hypot(r[0], r[1]), r[0] * v[1] - r[1] * v[0])


# ---------------------------------------------------------------- universal Kepler
def _C(z):
    if z > 1e-4:
        sz = math.sqrt(z)
        return (1 - math.cos(sz)) / z
    if z < -1e-4:
        x = math.sqrt(-z)
        h = math.sinh(0.5 * x)  # cosh(x)-1 = 2 sinh^2(x/2): exact, overflow-safe to x~700
        return 2 * h * h / (x * x)
    return 0.5 - z / 24.0 + z * z / 720.0


def _S(z):
    if z > 1e-4:
        sz = math.sqrt(z)
        return (sz - math.sin(sz)) / (z * sz)
    if z < -1e-4:
        x = math.sqrt(-z)
        return (math.sinh(x) - x) / (x * x * x)
    return 1.0 / 6.0 - z / 120.0 + z * z / 5040.0


def kepler_step(r0, v0, mu, dt):
    """Universal-variable Kepler propagation (Danby/Vallado). All conics, signed dt.
    t(chi) is monotone in chi, so the Newton solve is safeguarded by a bracket."""
    r0n = math.hypot(r0[0], r0[1])
    rdotv = r0 @ v0
    sqmu = math.sqrt(mu)
    alpha = 2.0 / r0n - (v0 @ v0) / mu  # 1/a

    def t_of(chi):
        z = alpha * chi * chi
        return ((rdotv / sqmu) * chi * chi * _C(z) + (1 - alpha * r0n) * chi ** 3 * _S(z)
                + r0n * chi) / sqmu

    adt = abs(dt)
    chi_hi = max(sqmu * adt / r0n, 1e-9)
    for _ in range(200):
        t_hi = t_of(chi_hi)
        if math.isinf(t_hi):
            raise OverflowError("kepler: bracket overflow")
        if t_hi >= adt:
            break
        chi_hi *= 2.0
    else:
        raise OverflowError("kepler: no bracket")
    lo, hi = 0.0, chi_hi
    chi = 0.5 * (lo + hi)
    for _ in range(200):
        z = alpha * chi * chi
        F = t_of(chi) - adt
        if F > 0.0:
            hi = chi
        else:
            lo = chi
        dF = ((rdotv / sqmu) * chi * (1 - z * _S(z)) + (1 - alpha * r0n) * chi * chi * _C(z)
              + r0n) / sqmu
        step = -F / dF
        nxt = chi + step
        if not (lo < nxt < hi) or not math.isfinite(nxt):
            nxt = 0.5 * (lo + hi)
        if abs(nxt - chi) <= 1e-14 * max(1.0, chi):
            chi = nxt
            break
        chi = nxt
    chi = math.copysign(chi, dt)  # t_of is odd in chi: the signed step is the mirrored solve
    z = alpha * chi * chi
    f = 1 - chi * chi / r0n * _C(z)
    g = dt - chi ** 3 / sqmu * _S(z)
    r = f * r0 + g * v0
    rn = math.hypot(r[0], r[1])
    fd = sqmu / (rn * r0n) * chi * (z * _S(z) - 1)
    gd = 1 - chi * chi / rn * _C(z)
    return r, fd * r0 + gd * v0


def conic_time_since_periapsis(r, v, mu):
    """(tau, a, e): tau is the time since periapsis (negative inbound)."""
    rn = math.hypot(r[0], r[1])
    v2 = v @ v
    evec = ((v2 - mu / rn) * r - (r @ v) * v) / mu
    e = math.hypot(evec[0], evec[1])
    nu = math.atan2((r[1] * evec[0] - r[0] * evec[1]) / max(e, 1e-300),
                    (r @ evec) / max(e, 1e-300))
    a = 1.0 / (2.0 / rn - v2 / mu)
    if e < 1.0:
        E = 2 * math.atan2(math.sqrt(1 - e) * math.sin(nu / 2), math.sqrt(1 + e) * math.cos(nu / 2))
        return (E - e * math.sin(E)) / math.sqrt(mu / a ** 3), a, e
    H = 2 * math.atanh(min(1 - 1e-15, math.sqrt((e - 1) / (e + 1)) * math.tan(nu / 2)))
    return (e * math.sinh(H) - H) / math.sqrt(mu / (-a) ** 3), a, e


# ---------------------------------------------------------------- truth (the judge's own frame)
def rhs(t, y):
    r = y[:2]
    rn = math.hypot(r[0], r[1])
    th = OMEGA * t
    u = np.array([math.cos(th), math.sin(th)])
    A = r + SEP * u
    tide = -MU_STAR * (A / math.hypot(A[0], A[1]) ** 3 - u / SEP ** 2)
    return np.concatenate([y[2:], -MU * r / rn ** 3 + tide])


def truth_flyby(bary0, rtol=1e-12):
    """(t_exit, dE, dL, closest) or an exclusion string. Planet-relative, Encke tide form."""
    pp, pv = planet_state(0.0)
    rel0 = np.concatenate([bary0[:2] - pp, bary0[2:] - pv])

    def run(t0, y0, level, direction):
        ev = lambda t, y: math.hypot(y[0], y[1]) - level
        ev.terminal = True
        ev.direction = direction
        return solve_ivp(rhs, (t0, PERIOD), y0, method="DOP853", rtol=rtol,
                         atol=[1e-6, 1e-6, 1e-17, 1e-17], events=ev, dense_output=True)

    s1 = run(0.0, rel0, SOI, -1.0)
    if len(s1.t_events[0]) == 0:
        return "never-in", None
    t_in = s1.t_events[0][0]
    s2 = run(t_in, s1.y_events[0][0], START_SOI * SOI, +1.0)
    if len(s2.t_events[0]) == 0:
        return "never-out", None
    t_exit = s2.t_events[0][0]

    # closest approach over [0, t_exit]: dense sample + golden-section refine
    ts1 = np.linspace(0.0, t_in, 2000)
    ts2 = np.linspace(t_in, t_exit, 2000)
    pts = [(t, math.hypot(*s1.sol(t)[:2])) for t in ts1] + [(t, math.hypot(*s2.sol(t)[:2])) for t in ts2]
    k = min(range(len(pts)), key=lambda i: pts[i][1])
    sol = s1 if k < len(ts1) else s2
    lo, hi = pts[max(0, k - 1)][0], pts[min(len(pts) - 1, k + 1)][0]
    for _ in range(70):
        m1, m2 = lo + 0.382 * (hi - lo), lo + 0.618 * (hi - lo)
        if math.hypot(*sol.sol(m1)[:2]) < math.hypot(*sol.sol(m2)[:2]):
            hi = m2
        else:
            lo = m1
    closest = math.hypot(*sol.sol(0.5 * (lo + hi))[:2])

    def helio(t, solx):
        ss, sv = star_state(t)
        pl, pv2 = planet_state(t)
        y = solx.sol(t)
        return helio_E_L(y[:2] + pl - ss, y[2:] + pv2 - sv)

    E0, L0 = helio(0.0, s1)
    E1, L1 = helio(t_exit, s2)
    return (t_exit, E1 - E0, L1 - L0, closest)


# ---------------------------------------------------------------- laws

def planet_helio(t):
    """The planet's position and velocity relative to the star at t."""
    pp, pv = planet_state(t)
    ss, sv = star_state(t)
    return pp - ss, pv - sv

def helio_of_bary(bary):
    ss, sv = star_state(0.0)
    return bary[:2] - ss, bary[2:] - sv


def law_L1(r0, v0, t_exit):
    """Starved cadence: heliocentric DKD, H = 2^round(log2(T_pass/64)), planet kick at midpoints."""
    tau, a, e = conic_time_since_periapsis(r0, v0, MU_STAR)
    T_pass = 2 * abs(tau)
    H = 2.0 ** round(math.log2(T_pass / 64.0))
    r, v = r0.copy(), v0.copy()
    t, kicks = 0.0, 0
    while t < t_exit:
        h = min(H, t_exit - t)
        r, v = kepler_step(r, v, MU_STAR, h / 2)
        rp, _ = planet_helio(t + h / 2)
        d = r - rp
        acc = -MU * (d / math.hypot(d[0], d[1]) ** 3 + rp / math.hypot(rp[0], rp[1]) ** 3)
        v = v + h * acc
        r, v = kepler_step(r, v, MU_STAR, h / 2)
        t += h
        kicks += 1
    return r, v, {"kicks": kicks, "H": H, "T_pass": T_pass}


def _analytic_entry(r0, v0, R_pch):
    """First t in (0, P) with |ship_helio_kepler(t) - planet(t)| = R_pch, downward. None: never."""
    def d(t):
        rs, _ = kepler_step(r0, v0, MU_STAR, t)
        rp, _ = planet_helio(t)
        return math.hypot(*(rs - rp))
    ts = np.linspace(1e-6, PERIOD, 3000)
    prev_t, prev_d = ts[0], d(ts[0])
    if prev_d < R_pch:
        return 0.0
    for k in range(1, len(ts)):
        dk = d(ts[k])
        if dk < R_pch < prev_d:
            return brentq(lambda t: d(t) - R_pch, prev_t, ts[k], xtol=1e-3)
        prev_t, prev_d = ts[k], dk
    return None


def _patch_state(r0, v0, t):
    rs, vs = kepler_step(r0, v0, MU_STAR, t)
    rp, vp = planet_helio(t)
    return rs - rp, vs - vp


def law_L2(r0, v0, R_pch):
    """One event: patched conics, the exact hyperbola leg inside R_pch (Öpik/Valsecchi form)."""
    t_in = 0.0 if R_pch >= START_SOI * SOI else _analytic_entry(r0, v0, R_pch)
    if t_in is None:
        return None
    if t_in == 0.0:
        pp, pv = planet_helio(0.0)
        rel, vrel = r0 - pp, v0 - pv  # the exact start state (the patch sphere holds it)
    else:
        rel, vrel = _patch_state(r0, v0, t_in)
    tau, a, e = conic_time_since_periapsis(rel, vrel, MU)
    if tau >= 0.0:
        return None  # already past periapsis at entry: the one-event form does not apply
    dt_leg = -2 * tau
    rel2, vrel2 = kepler_step(rel, vrel, MU, dt_leg)
    t_out = t_in + dt_leg
    rp, vp = planet_state(t_out)
    ss, sv = star_state(t_out)
    return t_out, rel2 + rp - ss, vrel2 + vp - sv, {"events": 1}


def law_L3(r0, v0, t_exit, R_pch):
    """Event + interior: entry at the patch sphere (analytic from the conics; exact at the
    start when the patch holds it), DKD in the planet frame (planetocentric Kepler drift,
    star-tide kicks, H_in = 2^floor(log2(T_enc/64))), exit at the outward patch crossing."""
    t_in = 0.0 if R_pch >= START_SOI * SOI else _analytic_entry(r0, v0, R_pch)
    if t_in is None:
        return None
    if t_in == 0.0:
        pp, pv = planet_helio(0.0)
        rel, vrel = r0 - pp, v0 - pv
    else:
        rel, vrel = _patch_state(r0, v0, t_in)
    tau, a, e = conic_time_since_periapsis(rel, vrel, MU)
    T_enc = 2 * abs(tau)
    H = 2.0 ** math.floor(math.log2(T_enc / 64.0))
    r, v = rel.copy(), vrel.copy()
    t, kicks = t_in, 0
    while math.hypot(r[0], r[1]) < R_pch or (r @ v) < 0.0:
        if t > t_exit:
            return None
        th = OMEGA * (t + H / 2)
        u = np.array([math.cos(th), math.sin(th)])
        r, v = kepler_step(r, v, MU, H / 2)
        A = r + SEP * u
        tide = -MU_STAR * (A / math.hypot(A[0], A[1]) ** 3 - u / SEP ** 2)
        v = v + H * tide
        r, v = kepler_step(r, v, MU, H / 2)
        t += H
        kicks += 1
    rp, vp = planet_state(t)
    ss, sv = star_state(t)
    return t, r + rp - ss, v + vp - sv, {"kicks": kicks, "H": H}


def finish_helio(r_h, v_h, t_from, t_to):
    if t_to > t_from:
        return kepler_step(r_h, v_h, MU_STAR, t_to - t_from)
    return r_h, v_h


# ---------------------------------------------------------------- seeds
def seeds():
    rng = np.random.default_rng(20261006)
    out = []
    for _ in range(48):  # A: matched to B13's distribution
        q = math.exp(rng.uniform(math.log(1.2), math.log(50.0)))
        out.append((q, rng.uniform(1.67e-5, 6.7e-5), rng.uniform(0, 2 * math.pi), "A"))
    best = []
    for _ in range(4000):  # B: the near-parabolic corner (smallest |e_h - 1|, both sides)
        q = math.exp(rng.uniform(math.log(1.2), math.log(50.0)))
        v = rng.uniform(4e-5, 6.7e-5)
        psi = rng.uniform(0, 2 * math.pi)
        r0h, v0h = helio_of_bary(ship_bary(q, v, psi))
        best.append((abs(conic_time_since_periapsis(r0h, v0h, MU_STAR)[2] - 1.0), q, v, psi))
    best.sort(key=lambda x: x[0])
    for _, q, v, psi in best[:16]:
        out.append((q, v, psi, "B"))
    for _ in range(8):  # C: fast and deep
        q = math.exp(rng.uniform(math.log(1.2), math.log(5.0)))
        out.append((q, 6.7e-5, rng.uniform(0, 2 * math.pi), "C"))
    return out


# ---------------------------------------------------------------- judge
def rel(a, b):
    return abs(a - b) / abs(b) if b != 0 else (0.0 if a == 0 else math.inf)


def main():
    rng = np.random.default_rng(11)
    worst = 0.0
    checked = 0
    # Forward accuracy vs DOP853 (every law here propagates forward only), including the
    # near-parabolic corner e = 1 +/- 1e-3 that killed the element route in m-meso-motion.
    for k in range(60):
        r = rng.normal(size=2)
        r = r / np.hypot(*r) * rng.uniform(1e4, 5e7)
        rn = np.hypot(*r)
        # a ~ r gives e within a few 1e-3 of 1 (the near-parabolic corner)
        a = rn / max(1e-9, (2.0 - 2.0 * rng.uniform(0.45, 0.55)))
        v = rng.normal(size=2)
        v = v / np.hypot(*v) * math.sqrt(MU * (2.0 / rn - 1.0 / a))
        dt = rng.uniform(1e6, 1e12)
        try:
            r2, v2 = kepler_step(r, v, MU, dt)
        except OverflowError:
            continue
        sol = solve_ivp(lambda t, y: np.concatenate([y[2:], -MU * y[:2] / np.hypot(y[0], y[1]) ** 3]),
                        [0, dt], np.concatenate([r, v]), method="DOP853", rtol=1e-13,
                        atol=[1e-8, 1e-8, 1e-20, 1e-20])
        rt = sol.y[:2, -1]
        if np.hypot(*rt) < 1e3:
            continue
        err = np.hypot(*(r2 - rt)) / np.hypot(*rt)
        worst = max(worst, err)
        checked += 1
    assert worst < 1e-9, worst
    print(f"selftest: Kepler forward vs DOP853 worst {worst:.2e} over {checked} conics")

    rows = []
    for q, v_inf, psi, tag in seeds():
        b = ship_bary(q, v_inf, psi)
        res = truth_flyby(b, 1e-12)
        if not isinstance(res, tuple):
            rows.append({"tag": tag, "q": q, "v_inf": v_inf, "psi": psi, "excluded": res})
            continue
        t_exit, dE, dL, closest = res
        fine = truth_flyby(b, 1e-13)
        if not isinstance(fine, tuple) or rel(fine[1], dE) > 1e-4 or rel(fine[2], dL) > 1e-4:
            rows.append({"tag": tag, "q": q, "v_inf": v_inf, "psi": psi, "excluded": "unconverged"})
            continue
        if closest < R_PLANET:
            rows.append({"tag": tag, "q": q, "v_inf": v_inf, "psi": psi, "excluded": "inside-planet",
                         "closest_rp": closest / R_PLANET})
            continue
        r0, v0 = helio_of_bary(b)
        E0, L0 = helio_E_L(r0, v0)
        _, _, e_h = conic_time_since_periapsis(r0, v0, MU_STAR)
        pp, pv = planet_state(0.0)
        tau_p, _, _ = conic_time_since_periapsis(b[:2] - pp, b[2:] - pv, MU)
        T_enc = 2 * abs(tau_p)
        row = {"tag": tag, "q_rp": q, "v_inf": v_inf, "e_h": e_h, "t_exit": t_exit,
               "dE_ref": dE, "dL_ref": dL, "T_enc": T_enc, "closest_rp": closest / R_PLANET}

        r1, v1, m1 = law_L1(r0, v0, t_exit)
        E1e, L1e = helio_E_L(r1, v1)
        row["L1"] = {"dE": rel(E1e - E0, dE), "dL": rel(L1e - L0, dL), **m1,
                     "kicks_in_enc": math.floor(T_enc / m1["H"])}

        for name, Rfrac in (("L2", 1.0), ("L2", 1.5), ("L3", 1.0), ("L3", 1.5)):
            fn = law_L2(r0, v0, Rfrac * SOI) if name == "L2" else law_L3(r0, v0, t_exit, Rfrac * SOI)
            key = f"{name}@{Rfrac}"
            if fn is None:
                row[key] = {"no_event": True}
                continue
            t_out, rh, vh, m = fn
            rh, vh = finish_helio(rh, vh, t_out, t_exit)
            E, L = helio_E_L(rh, vh)
            row[key] = {"dE": rel(E - E0, dE), "dL": rel(L - L0, dL), **m}
        rows.append(row)

    with open("flyby_event.json", "w") as f:
        json.dump(rows, f, indent=1)
    report(rows)


def report(rows):
    judged = [r for r in rows if "L1" in r]
    excl = [r for r in rows if "excluded" in r]
    print(f"{len(rows)} seeds, {len(judged)} judged, {len(excl)} excluded: "
          + ", ".join(sorted(set(str(r['excluded']) for r in excl))))
    for tag in ("A", "B", "C"):
        rs = [r for r in judged if r["tag"] == tag]
        if not rs:
            continue
        print(f"\nset {tag} ({len(rs)} judged, e_h-1 in [{min(r['e_h'] - 1 for r in rs):.2e}, "
              f"{max(r['e_h'] - 1 for r in rs):.2e}]):")
        for c in ("L1", "L2@1.0", "L2@1.5", "L3@1.0", "L3@1.5"):
            oks = [r[c].get("dE", math.inf) <= 1e-2 and r[c].get("dL", math.inf) <= 1e-2
                   and "no_event" not in r[c] for r in rs]
            worst = max(max(r[c].get("dE", math.inf), r[c].get("dL", math.inf)) for r in rs)
            evs = [r[c].get("kicks", r[c].get("events", 0)) for r in rs]
            nev = sum(1 for r in rs if "no_event" in r[c])
            print(f"  {c:8s} pass {sum(oks)}/{len(rs)}  worst {worst:9.2e}  events med "
                  f"{int(np.median(evs)) if evs else 0} max {max(evs) if evs else 0}  no-event {nev}")
    rs = [r for r in judged if r["tag"] == "B"]
    print("\nset B detail:")
    for r in sorted(rs, key=lambda r: r["e_h"]):
        l3 = r["L3@1.5"]
        print(f"  e-1={r['e_h'] - 1:8.2e} q={r['q_rp']:6.1f} vinf={r['v_inf']:.2e} "
              f"Tpass/Tenc={r['L1']['T_pass'] / r['T_enc']:8.1f} k_enc={r['L1']['kicks_in_enc']:5d} "
              f"L1({r['L1']['dE']:.1e}) L3@1.5({l3.get('dE', float('nan')):.1e},{l3.get('kicks', 0)}k)")


if __name__ == "__main__":
    main()
