#!/usr/bin/env python3
"""The doll boundary rule, falsified on the CR3BP (run 20261017-1240-scout-f666).

Replays candidate handoff rules over the SAME true trajectory (no rule feedback);
measures the decision stream (event count, classification), not trajectory identity.
Rules: R0 shipped replica (per-tick r<R_H/2 ∧ E_p<0), R1 r-hysteresis, R2 dwell,
R3 per-cycle radial extent vs the empirical stability radius f(Λ)·R_H (continuous in
the synodic sense Λ, margin 0.05). All float — an instrument for the rule class,
not the integer law.
"""
import argparse, json, sys
import numpy as np
from scipy.integrate import solve_ivp

PRO = +1
RET = -1

def rhs(t, s, mu):
    x, y, vx, vy = s
    r1 = np.hypot(x + mu, y)
    r2 = np.hypot(x - 1.0 + mu, y)
    ax = 2.0 * vy + x - (1 - mu) * (x + mu) / r1**3 - mu * (x - 1 + mu) / r2**3
    ay = -2.0 * vx + y - (1 - mu) * y / r1**3 - mu * y / r2**3
    return [vx, vy, ax, ay]

def jacobi(s, mu):
    x, y, vx, vy = s
    r1 = np.hypot(x + mu, y)
    r2 = np.hypot(x - 1.0 + mu, y)
    return x*x + y*y + 2*(1-mu)/r1 + 2*mu/r2 - (vx*vx + vy*vy)

def integrate(mu, r0f, sense, nP, kick_t=None, kick_dv=0.0, rtol=1e-12):
    RH = (mu / 3.0) ** (1.0 / 3.0)
    r0 = r0f * RH
    th = np.pi / 2.0                       # launch direction: +y from planet
    # inertial
    px, py = (1 - mu) * np.cos(0.0), (1 - mu) * np.sin(0.0)
    pvx, pvy = (1 - mu) * -np.sin(0.0), (1 - mu) * np.cos(0.0)
    vc = np.sqrt(mu / r0)
    rx, ry = px + r0 * np.cos(th), py + r0 * np.sin(th)
    wx, wy = -np.sin(th), np.cos(th)
    vx, vy = pvx + sense * vc * wx, pvy + sense * vc * wy
    # to rotating (t=0): v_rot = v_in + (y, -x)
    s0 = [rx, ry, vx + ry, vy - rx]

    T = 2 * np.pi * nP
    t_events, s_events = [], []
    if kick_t is not None:
        t_events = [kick_t * 2 * np.pi]
        s_events = [None]  # filled after first leg

    def kick_state(t):
        sol = solve_ivp(rhs, [0, t], s0, args=(mu,), rtol=rtol, atol=rtol,
                        dense_output=False, method="DOP853")
        return sol.y[:, -1]

    if kick_t is not None:
        sk = kick_state(kick_t * 2 * np.pi)
        # radial (planetocentric) 3% boost
        dx, dy = sk[0] - (1 - mu), sk[1]
        r2 = np.hypot(dx, dy)
        sk = sk.copy()
        s_events = [sk + 0.0]
        s_events[0][2] += kick_dv * dx / r2
        s_events[0][3] += kick_dv * dy / r2
        sol1 = solve_ivp(rhs, [0, kick_t * 2 * np.pi], s0, args=(mu,), rtol=rtol,
                         atol=rtol, dense_output=True, method="DOP853")
        sol2 = solve_ivp(rhs, [kick_t * 2 * np.pi, T], s_events[0], args=(mu,),
                         rtol=rtol, atol=rtol, dense_output=True, method="DOP853")
        sols = [(0, sol1), (kick_t * 2 * np.pi, sol2)]
    else:
        sol = solve_ivp(rhs, [0, T], s0, args=(mu,), rtol=rtol, atol=rtol,
                        dense_output=True, method="DOP853")
        sols = [(0, sol)]

    Tm = 2 * np.pi * np.sqrt((r0f * RH) ** 3 / mu)   # moon period at r0
    dt = Tm / 200.0
    ts = np.arange(0.0, T - 1e-12, dt)
    S = np.zeros((len(ts), 4))
    for t0, s in sols:
        m = (ts >= t0 - 1e-12) & (ts <= s.t[-1] + 1e-12)
        S[m] = s.sol(ts[m]).T
    CJ = jacobi(S.T, mu)
    return ts, S, CJ, RH, Tm

def derived(ts, S, mu):
    """r2, planetocentric inertial velocity, E_p, h_z, per sample."""
    c, s_ = np.cos(ts), np.sin(ts)
    X, Y, VX, VY = S.T
    # rotating -> inertial
    xi = X * c - Y * s_
    yi = X * s_ + Y * c
    vxi = (VX - Y) * c - (VY + X) * s_
    vyi = (VX - Y) * s_ + (VY + X) * c
    # planet inertial pos/vel
    px, py = (1 - mu) * c, (1 - mu) * s_
    pvx, pvy = -(1 - mu) * s_, (1 - mu) * c
    dx, dy = xi - px, yi - py
    dvx, dvy = vxi - pvx, vyi - pvy
    r2 = np.hypot(dx, dy)
    v2 = dvx * dvx + dvy * dvy
    Ep = 0.5 * v2 - mu / r2
    hz = dx * dvy - dy * dvx
    return r2, Ep, hz

def apo_pass(ts, r2):
    """indices of local maxima of r2 (apoapsis passages)."""
    i = np.arange(1, len(r2) - 1)
    m = (r2[i] > r2[i - 1]) & (r2[i] > r2[i + 1])
    return i[m]

def f_stab(Lam):
    """empirical stability radius fraction, continuous in the synodic sense."""
    lam = np.clip(Lam, -1.0, 1.0)
    w = np.clip((0.25 - lam) / 0.5, 0.0, 1.0)   # 0 prograde -> 1 retrograde
    return 0.5 + 0.2 * w

def replay(ts, r2, Ep, hz, RH, rule, dt_scale=1.0):
    idx = np.arange(0, len(ts), max(1, int(round(dt_scale))))
    owner = "planet"     # born in the planet's doll (the moon test)
    n = 0
    times = []
    t_last = -1e9
    if rule in ("R0", "R1", "R2"):
        for i in idx:
            want = "planet"
            if rule == "R0" or rule == "R2":
                want = "planet" if (r2[i] < 0.5 * RH and Ep[i] < 0) else "star"
            elif rule == "R1":
                if owner == "planet":
                    want = "star" if (r2[i] > 0.65 * RH or Ep[i] > 0) else "planet"
                else:
                    want = "planet" if (r2[i] < 0.5 * RH and Ep[i] < 0) else "star"
            if want != owner:
                if rule == "R2" and ts[i] - t_last < 2 * np.pi:
                    continue
                owner = want
                n += 1
                times.append(ts[i])
                t_last = ts[i]
    elif rule == "R3":
        m = 0.05
        for i in apo_pass(ts, r2):
            ra = r2[i]
            Lam = hz[i] / max(ra * ra, 1e-12)
            f = f_stab(Lam)
            if owner == "planet":
                if ra > (f + m) * RH:
                    owner = "star"; n += 1; times.append(ts[i])
            else:
                if ra < (f - m) * RH and Ep[i] < 0:
                    owner = "planet"; n += 1; times.append(ts[i])
    else:
        raise ValueError(rule)
    return n, times

def classify(ts, r2, RH):
    """truth: retained iff never beyond 1.5 R_H."""
    return "retained" if r2.max() < 1.5 * RH else "ejected"

def run_case(mu, r0f, sense, nP, kick_t=None, kick_dv=0.0):
    ts, S, CJ, RH, Tm = integrate(mu, r0f, sense, nP, kick_t, kick_dv)
    r2, Ep, hz = derived(ts, S, mu)
    res = {
        "mu": mu, "r0f": r0f, "sense": "pro" if sense > 0 else "ret",
        "dC_J": float(abs(CJ.max() - CJ.min())),
        "truth": classify(ts, r2, RH),
        "max_r2_RH": float(r2.max() / RH),
        "n_apo": int(len(apo_pass(ts, r2))),
        "T_moon": float(Tm),
    }
    for rule in ("R0", "R0f", "R1", "R2", "R3"):
        sc = 2.0 if rule == "R0f" else 1.0
        n, times = replay(ts, r2, Ep, hz, RH, rule.rstrip("f"), dt_scale=sc)
        res[rule] = n
        res[rule + "_rate_per_orbit"] = round(n / max(res["n_apo"], 1), 4)
        res[rule + "_first"] = round(times[0], 3) if times else None
    return res

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mu", type=float, default=1e-3)
    ap.add_argument("--periods", type=float, default=20)
    ap.add_argument("--kick-t", type=float, default=None)
    ap.add_argument("--kick-dv", type=float, default=0.03)
    ap.add_argument("--json", type=str, default=None)
    A = ap.parse_args()
    cases = [(0.3, PRO), (0.3, RET), (0.49, RET), (0.5, PRO), (0.5, RET),
             (0.7, RET), (0.9, PRO), (0.9, RET)]
    out = []
    hdr = f"case(mu={A.mu}, {A.periods}P)      truth    dCJ      R0   R0f   R1   R2   R3   apo"
    print(hdr)
    for r0f, sense in cases:
        r = run_case(A.mu, r0f, sense, A.periods)
        out.append(r)
        print(f"({r0f:4.2f},{r['sense']})           "
              f"{r['truth']:8s} {r['dC_J']:.1e}  "
              f"{r['R0']:4d} {r['R0f']:4d} {r['R1']:4d} {r['R2']:4d} {r['R3']:4d}  {r['n_apo']}")
    if A.kick_t is not None:
        r = run_case(A.mu, 0.5, PRO, A.periods, kick_t=A.kick_t, kick_dv=A.kick_dv)
        out.append(r)
        print(f"(0.50,pro,kick {A.kick_dv:.0%})  {r['truth']:8s} {r['dC_J']:.1e}  "
              f"{r['R0']:4d} {r['R0f']:4d} {r['R1']:4d} {r['R2']:4d} {r['R3']:4d}  {r['n_apo']}")
    if A.json:
        with open(A.json, "w") as f:
            json.dump(out, f, indent=1)
    # summary lines the dossier quotes
    worst = max(out, key=lambda r: r["R0"])
    print(f"\nworst R0 chatter: ({worst['r0f']},{worst['sense']}) = {worst['R0']} "
          f"(R3 there = {worst['R3']})")
    mis = [r for r in out if r["R3"] > 0 and r["truth"] == "retained"]
    print(f"R3 releases on truth-retained cases: {[(x['r0f'], x['sense'], x['R3']) for x in mis]}")
    hold = [r for r in out if r["R3"] == 0 and r["truth"] == "ejected"]
    print(f"R3 retains-forever on truth-ejected cases: {[(x['r0f'], x['sense']) for x in hold]}")
    zeno = [r for r in out if r["R3_rate_per_orbit"] > 1.0]
    print(f"R3 >1/orbit anywhere: {[(x['r0f'], x['sense'], x['R3_rate_per_orbit']) for x in zeno]}")

if __name__ == "__main__":
    main()
