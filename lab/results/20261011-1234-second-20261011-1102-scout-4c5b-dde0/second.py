#!/usr/bin/env python3
"""Second author's experiments on run 20261011-1102-scout-4c5b (fixed circ_L).

Modes (each writes its own JSON; `python3 second.py all` runs grid+conv+w2, the
fast ones; the from-1000M runs are separate because they take minutes):
  grid   B: pre-registered kill criterion on high-e births at the p=20M boundary
  m1000c C: circular  nu=0.25 from a0=1000M, measured re-keys (1% and 0.1% bars)
  m1000e C: eccentric nu=0.25 e0=0.3 from a0=1000M, measured re-keys
  conv   D1: handoff endpoint under step tightening (dt scale k in {1, 0.25})
  w2     D2: W2 relerr step-scaling (P/64 vs P/256)

run_eccentric_dt / run_circular_dt are verbatim copies of the shipped functions
with one multiplicative dt scale k (same RK4, same fluxes, same re-key logic,
same separatrix break) — the convergence knob the shipped code hardcodes.
"""
import json
import sys
import numpy as np
import inspiral as I

# ------------------------------------------------------- grid (kill line) ---
def grid():
    out = []
    cases = []
    for nu in (0.25, 0.01):
        for e0 in (0.5, 0.6, 0.65, 0.7, 0.75, 0.8, 0.9):
            cases.append((nu, 20.0 / (1.0 - e0 * e0), e0))   # p = 20M boundary
    cases.append((0.25, 110.0, 0.9))                          # checker's case
    for nu, a0, e0 in cases:
        r = I.run_eccentric(nu, a0, e0)
        w1 = r["walls"]["0.01"]
        ratio = (w1 / r["a_end"]) if (w1 is not None and r["a_end"]) else None
        out.append({"nu": nu, "a0": round(a0, 2), "e0": e0, "p0": round(a0 * (1 - e0 * e0), 2),
                    "orbits": r["orbits"], "a_end": r["a_end"], "e_end": r["e_end"],
                    "wall_1pct": w1, "wall_at_start": w1 is not None and w1 >= a0 * 0.999,
                    "ratio_wall_sep_1pct": ratio,
                    "kill_1pct": ratio is not None and ratio >= 5.0})
        print(f"  nu={nu:g} e0={e0:.2f} a0={a0:.1f} p0={a0*(1-e0*e0):.1f}: "
              f"orbits={r['orbits']:.0f} a_end={r['a_end']:.2f} e_end={r['e_end']:.3f} "
              f"wall1%={w1 and round(w1,1)} ratio={ratio and round(ratio,1)} kill={out[-1]['kill_1pct']}")
    return out

# ------------------------------------------ step-convergence of the handoff ---
def run_eccentric_dt(nu, a0, e0, k, eps_bars=(1e-2,)):
    E, L = I.EL_from_ae(a0, e0)
    u = I.roots_exact(E, L)
    ua, up, u3 = u[0], u[1], u[2]
    n_orb = 0.0
    max_e = 0.0
    a_end = e_end = None
    last_good = [None, None]

    def fluxes(E_, L_, ua_, up_):
        ua2, up2, u32, ok = I.roots_newton(E_, L_, ua_, up_)
        if not ok:
            u_ = I.roots_exact(E_, L_)
            if u_ is None:
                return None
            ua2, up2, u32 = u_
        a_, e_ = I.ae_from_u(ua2, up2)
        return (-I.flux_L(a_, e_, nu) / nu, -I.flux_G(a_, e_, nu) / nu,
                ua2, up2, u32, a_, e_)

    while True:
        f = fluxes(E, L, ua, up)
        if f is None:
            break
        dEdt, dLdt, ua, up, u3, a, e = f
        if u3 - up < 1e-6 * up:
            a_end, e_end = a, e
            break
        last_good = [a, e]
        max_e = max(max_e, e)
        P = 2.0 * np.pi * a**1.5
        da_orb = (64.0 / 5.0) * nu * I.peters_F(e) / a**3 * P
        dlnP = 1.5 * abs(da_orb) / a
        dt = k * P * min(0.5, 0.05 / max(dlnP, 1e-15))
        for _ in range(40):
            k1 = fluxes(E, L, ua, up)
            k2 = (None if k1 is None else
                  fluxes(E + .5 * dt * k1[0], L + .5 * dt * k1[1], k1[2], k1[3]))
            k3 = (None if k2 is None else
                  fluxes(E + .5 * dt * k2[0], L + .5 * dt * k2[1], k2[2], k2[3]))
            k4 = (None if k3 is None else
                  fluxes(E + dt * k3[0], L + dt * k3[1], k3[2], k3[3]))
            if None not in (k1, k2, k3, k4):
                break
            dt *= 0.5
        else:
            a_end, e_end = last_good
            break
        if None in (k1, k2, k3, k4):
            a_end, e_end = last_good
            break
        E += dt * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6.0
        L += dt * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6.0
        ua, up = k4[2], k4[3]
        n_orb += dt / P
    if a_end is None:
        u_ = I.roots_exact(E, L)
        if u_ is not None:
            a_end, e_end = I.ae_from_u(u_[0], u_[1])
        else:
            a_end, e_end = last_good
    return {"k": k, "orbits": n_orb, "a_end": a_end, "e_end": e_end, "max_e": max_e}

def conv():
    out = []
    for nu, a0, e0 in [(0.25, 100.0, 0.3), (0.25, 100.0, 0.6), (0.01, 100.0, 0.6)]:
        for k in (1.0, 0.25):
            r = run_eccentric_dt(nu, a0, e0, k)
            r.update({"nu": nu, "a0": a0, "e0": e0})
            out.append(r)
            print(f"  nu={nu:g} e0={e0} k={k}: a_end={r['a_end']:.3f} "
                  f"e_end={r['e_end']:.4f} orbits={r['orbits']:.0f}")
    return out

# ---------------------------------------------------------------- W2 scale ---
def w2_scaling():
    def run(ndt):
        dadt = lambda a: -(64.0 / 5.0) * 0.25 / a**3
        a, t = 100.0, 0.0
        while a > 6.0:
            P = 2.0 * np.pi * a**1.5
            dt = P / ndt
            k1 = dadt(a); k2 = dadt(a + .5 * dt * k1)
            k3 = dadt(a + .5 * dt * k2); k4 = dadt(a + dt * k3)
            a += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
            t += dt
        t_true = (5.0 / (256.0 * 0.25)) * (100.0**4 - 6.0**4)
        return abs(t / t_true - 1.0)
    r64, r256 = run(64), run(256)
    return {"relerr_P64": r64, "relerr_P256": r256, "factor": r64 / r256}

# ------------------------------------------------------------- from 1000M ---
def m1000(kind):
    if kind == "m1000c":
        r = I.run_circular(0.25, 1000.0, eps_bars=(1e-2, 1e-3))
        rate = {eb: r["rekeys_strong"][eb] / r["orbits"] for eb in ("0.01", "0.001")}
        out = {"kind": "circular", "nu": 0.25, "a0": 1000.0, "orbits": r["orbits"],
               "t_merge": r["t_merge"], "walls": r["walls"],
               "rekeys": r["rekeys_strong"], "rate_per_orbit": rate}
    else:
        r = I.run_eccentric(0.25, 1000.0, 0.3, eps_bars=(1e-2, 1e-3))
        rate = {eb: r["rekeys_strong"][eb] / r["orbits"] for eb in ("0.01", "0.001")}
        out = {"kind": "eccentric e0=0.3", "nu": 0.25, "a0": 1000.0, "orbits": r["orbits"],
               "a_end": r["a_end"], "e_end": r["e_end"], "max_e": r["max_e"],
               "walls": r["walls"], "rekeys": r["rekeys_strong"],
               "rate_per_orbit": rate}
    print(json.dumps(out, default=float))
    return out

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    res = {}
    if mode in ("grid", "all"):
        print("== B: kill grid at the p=20M boundary ==")
        res["grid"] = grid()
    if mode in ("conv", "all"):
        print("== D1: handoff under step tightening ==")
        res["conv"] = conv()
    if mode in ("w2", "all"):
        res["w2_scaling"] = w2_scaling()
        print(f"== D2: W2 relerr P/64={res['w2_scaling']['relerr_P64']:.2e} "
              f"P/256={res['w2_scaling']['relerr_P256']:.2e} "
              f"factor={res['w2_scaling']['factor']:.1f}x ==")
    if mode == "m1000c":
        res = m1000("m1000c")
    if mode == "m1000e":
        res = m1000("m1000e")
    with open(f"second-{mode}.json", "w") as f:
        json.dump(res, f, indent=1, default=float)
    print(f"wrote second-{mode}.json")
