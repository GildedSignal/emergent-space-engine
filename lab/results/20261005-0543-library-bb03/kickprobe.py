"""Kick-schedule premise probe (library lens run 20261005-0543).

Structure under test (docs/law.md line 30): exact Kepler drift on the tube +
impulsive kicks at a FIXED step in the drift's phase. Question: at equal kick
budget (events per orbit), does magnitude-driven event scheduling beat uniform
cadence, and is the small-kick tail weightless (drop it) or load-bearing
(accumulate it below one quantum, principle 6)?

Schedules (all: impulse evaluated at end of its own interval, applied to v):
  S0  uniform in time            (the engine's fixed phase step)
  S1  uniform in eccentric anomaly (perihelion-weighted, Sundman dt/ds=r family)
  S2a threshold: on a fine micro-grid, DROP |dv| < Q          (pure deletion)
  S2b accumulate: pending += dv; fire when |pending| >= Q      ("below one
      quantum influences accumulate" -- principle 6)
Truth: scipy DOP853 rtol=1e-12 atol=1e-14 on the full perturbed problem.
Estimator (identical for truth and candidates): linear fit of osculating
varpi sampled 256x over 50 orbits -> precession rate; mean osculating e over
the last 10 orbits.
"""
import json
import sys
import numpy as np
from scipy.integrate import solve_ivp

MU = 1.0


def accel(x, y, vx, vy, t, case):
    r = np.hypot(x, y)
    ax = -MU * x / r**3
    ay = -MU * y / r**3
    if case["kind"] == "j2":
        j2 = case["j2"]  # = J2 * R^2
        c = -1.5 * MU * j2 / r**4
        ax += c * x / r
        ay += c * y / r
    elif case["kind"] == "3b":
        m2, R2 = case["m2"], case["R2"]
        n2 = np.sqrt(MU * (1 + m2) / R2**3)
        sx, sy = R2 * np.cos(n2 * t + case["phi2"]), R2 * np.sin(n2 * t + case["phi2"])
        dx, dy = sx - x, sy - y
        d3 = (dx * dx + dy * dy) ** 1.5
        s3 = R2**3
        ax += m2 * (dx / d3 - sx / s3)
        ay += m2 * (dy / d3 - sy / s3)
    return ax, ay


def accel_pert(x, y, vx, vy, t, case):
    """Perturbation only: the Kepler term is carried exactly by the drift."""
    ax, ay = accel(x, y, vx, vy, t, case)
    r = np.hypot(x, y)
    return ax + MU * x / r**3, ay + MU * y / r**3


def state_to_elems(x, y, vx, vy):
    r = np.hypot(x, y)
    v2 = vx * vx + vy * vy
    a = 1.0 / (2.0 / r - v2)
    rv = x * vx + y * vy
    ex = (v2 - 1.0 / r) * x - rv * vx
    ey = (v2 - 1.0 / r) * y - rv * vy
    e = np.hypot(ex, ey)
    varpi = np.arctan2(ey, ex)
    return a, e, varpi


def kepler_solve(M, e):
    E = M.copy()
    for _ in range(60):
        f = E - e * np.sin(E) - M
        fp = 1.0 - e * np.cos(E)
        d = f / fp
        E -= d
        if np.max(np.abs(d)) < 1e-15:
            break
    return E


def drift(x, y, vx, vy, dt):
    """Exact Kepler drift via classical elements (ellipse, e<1)."""
    a, e, _ = state_to_elems(x, y, vx, vy)
    r = np.hypot(x, y)
    rv = x * vx + y * vy
    # true anomaly & E from position
    ex_v = (vx * vx + vy * vy - 1.0 / r) * x - rv * vx
    ey_v = (vx * vx + vy * vy - 1.0 / r) * y - rv * vy
    varpi = np.arctan2(ey_v, ex_v)
    f = np.arctan2(y, x) - varpi
    E = 2.0 * np.arctan2(np.sqrt(1 - e) * np.sin(f / 2), np.sqrt(1 + e) * np.cos(f / 2))
    M = E - e * np.sin(E)
    n = a**-1.5
    M2 = M + n * dt
    # wrap to [0, 2pi) for the solver's benefit
    M2 = M2 % (2 * np.pi)
    E2 = kepler_solve(M2, e)
    f2 = 2.0 * np.arctan2(np.sqrt(1 + e) * np.sin(E2 / 2), np.sqrt(1 - e) * np.cos(E2 / 2))
    p = a * (1 - e * e)
    r2 = p / (1 + e * np.cos(f2))
    th = varpi + f2
    ct, st = np.cos(th), np.sin(th)
    h = np.sqrt(p)
    vr = MU / h * e * np.sin(f2)
    vt = MU / h * (1 + e * np.cos(f2))
    return r2 * ct, r2 * st, vr * ct - vt * st, vr * st + vt * ct


def run_candidate(case, s, y0, T, n_orb, n_per_orb):
    """s in {'S0','S1','S2a','S2b'}; returns (varpi samples, e samples, energy, n_kicks)."""
    x, y, vx, vy = y0
    micro = 1024  # micro-grid for S2 (evaluation per micro-step, events rarer)
    out_varpi, out_e, out_t = [], [], []
    if s in ("S0",):
        times = np.arange(1, n_orb * n_per_orb + 1) * (T / n_per_orb)
    elif s == "S1":
        # uniform eccentric anomaly: E_j spaced dE = 2pi/n; t from M(E)
        e0 = state_to_elems(x, y, vx, vy)[1]
        dE = 2 * np.pi / n_per_orb
        # starting E
        a0, e0, w0 = state_to_elems(x, y, vx, vy)
        r0 = np.hypot(x, y)
        rv0 = x * vx + y * vy
        f0 = np.arctan2(y, x) - w0
        E0 = 2 * np.arctan2(np.sqrt(1 - e0) * np.sin(f0 / 2), np.sqrt(1 + e0) * np.cos(f0 / 2))
        Egrid = E0 + dE * np.arange(1, n_orb * n_per_orb + 1)
        Mgrid = (Egrid - e0 * np.sin(Egrid)) % (2 * np.pi)
        M0 = E0 - e0 * np.sin(E0)
        # unwrap M relative to M0 (monotone in E)
        Mrel = Egrid - e0 * np.sin(Egrid) - M0
        times = Mrel * a0**1.5
    else:
        times = None  # micro-grid handled inline

    n_kicks = 0
    if s in ("S0", "S1"):
        t = 0.0
        sample_idx = set(np.linspace(0, len(times) - 1, 256).astype(int))
        for i, tk in enumerate(times):
            x, y, vx, vy = drift(x, y, vx, vy, tk - t)
            t = tk
            ax, ay = accel_pert(x, y, vx, vy, t, case)
            dt_int = times[i + 1] - tk if i + 1 < len(times) else T / n_per_orb
            vx += ax * dt_int
            vy += ay * dt_int
            n_kicks += 1
            if i in sample_idx:
                a_, e_, w_ = state_to_elems(x, y, vx, vy)
                out_varpi.append(w_)
                out_e.append(e_)
                out_t.append(t)
    else:
        Q = case["_Q"]
        dt_m = T / micro
        t = 0.0
        px = py = 0.0
        sample_every = max(1, (n_orb * micro) // 256)
        i_m = 0
        for j in range(n_orb * micro):
            x, y, vx, vy = drift(x, y, vx, vy, dt_m)
            t += dt_m
            ax, ay = accel_pert(x, y, vx, vy, t, case)
            dvx, dvy = ax * dt_m, ay * dt_m
            if s == "S2a":
                if np.hypot(dvx, dvy) >= Q:
                    vx += dvx
                    vy += dvy
                    n_kicks += 1
            else:  # S2b accumulate
                px += dvx
                py += dvy
                if np.hypot(px, py) >= Q:
                    vx += px
                    vy += py
                    px = py = 0.0
                    n_kicks += 1
            i_m += 1
            if i_m % sample_every == 0:
                a_, e_, w_ = state_to_elems(x, y, vx, vy)
                out_varpi.append(w_)
                out_e.append(e_)
                out_t.append(t)
    # unwrap varpi
    v = np.array(out_varpi)
    v = np.unwrap(v)
    t_arr = np.array(out_t)
    slope = np.polyfit(t_arr, v, 1)[0]
    e_mean = float(np.mean(out_e[-len(out_e) // 5 :]))
    return slope, e_mean, np.array([x, y, vx, vy]), n_kicks


def energy(x, y, vx, vy, case, t=None):
    r = np.hypot(x, y)
    E = 0.5 * (vx * vx + vy * vy) - MU / r
    if case["kind"] == "j2":
        E += -MU * case["j2"] / (2 * r**3)
    return E


def truth(case, y0, T, n_orb):
    def rhs(t, s):
        ax, ay = accel(s[0], s[1], s[2], s[3], t, case)
        return [s[2], s[3], ax, ay]

    t_end = n_orb * T
    sol = solve_ivp(rhs, [0, t_end], list(y0), method="DOP853", rtol=1e-12, atol=1e-14,
                    dense_output=True)
    ts = np.linspace(0, t_end, 2048)
    st = sol.sol(ts)
    varpis, es = [], []
    for i in range(len(ts)):
        a_, e_, w_ = state_to_elems(*st[:, i])
        varpis.append(w_)
        es.append(e_)
    v = np.unwrap(np.array(varpis))
    slope = np.polyfit(ts, v, 1)[0]
    e_mean = float(np.mean(es[-len(es) // 5 :]))
    return slope, e_mean, st[:, -1]


def initial_state(case):
    if case["kind"] == "j2":
        a0, e0 = case["a"], case["e0"]
    else:
        a0, e0 = case["a"], case["e0"]
    r0 = a0 * (1 - e0)  # start at periapsis
    v0 = np.sqrt(MU * (2 / r0 - 1 / a0))
    return [r0, 0.0, 0.0, v0]


def main():
    cases = {
        "C1-j2-e03": {"kind": "j2", "j2": 2e-3, "a": 1.0, "e0": 0.3},
        "C2-3b": {"kind": "3b", "m2": 1e-2, "R2": 3.0, "phi2": 0.0, "a": 1.0, "e0": 0.05},
        "C3-j2-e06": {"kind": "j2", "j2": 2e-3, "a": 1.0, "e0": 0.6},
    }
    n_orb = 50
    results = {}
    for name, case in cases.items():
        y0 = initial_state(case)
        a0 = case["a"]
        T = 2 * np.pi * a0**1.5
        sl_tr, e_tr, st_tr = truth(case, y0, T, n_orb)
        E0 = energy(*y0, case)
        Etr = energy(*st_tr, case) if case["kind"] == "j2" else None
        results[name] = {"truth": {"precession": sl_tr, "e": e_tr,
                                   "dE": (Etr - E0) / abs(E0) if Etr is not None else None},
                         "runs": []}
        print(f"{name}: truth precession {sl_tr:.6e} rad/time  e {e_tr:.6f}")
        for sched in ("S0", "S1", "S2a", "S2b"):
            for n in (2, 4, 8, 16, 32):
                case["_Q"] = None
                if sched.startswith("S2"):
                    # bisect quantum Q for target event count n/orbit
                    lo, hi = 1e-12, 1e-1
                    for _ in range(12):
                        mid = np.sqrt(lo * hi)
                        case["_Q"] = mid
                        _, _, _, nk = run_candidate(case, sched, y0, T, 3, n)
                        got = nk / 3
                        if got > n:
                            lo = mid
                        else:
                            hi = mid
                    case["_Q"] = np.sqrt(lo * hi)
                sl, em, st_end, nk = run_candidate(case, sched, y0, T, n_orb, n)
                dpre = (sl - sl_tr) / abs(sl_tr)
                de = (em - e_tr) / e_tr
                dE = (energy(*st_end, case) - E0) / abs(E0) if case["kind"] == "j2" else None
                results[name]["runs"].append({"sched": sched, "n": n, "kicks": nk,
                                              "per_orb": nk / n_orb,
                                              "dpre": dpre, "de": de, "dE": dE})
                print(f"  {sched} n={n:>2} ({nk/n_orb:5.1f}/orb): dpre {dpre:+.2e}  "
                      f"de {de:+.2e}" + (f"  dE {dE:+.2e}" if dE is not None else ""))
        # heavy-tail of |dv| mass on the micro-grid (first orbit)
        x, y, vx, vy = initial_state(case)
        dt_m = T / 1024
        dvs = []
        t = 0.0
        for j in range(1024):
            x, y, vx, vy = drift(x, y, vx, vy, dt_m)
            t += dt_m
            ax, ay = accel_pert(x, y, vx, vy, t, case)
            dvs.append(np.hypot(ax, ay) * dt_m)
        dvs = np.sort(dvs)[::-1]
        tot = dvs.sum()
        gini = 1 - 2 * np.trapezoid(np.cumsum(np.sort(dvs)) / tot, dx=1 / len(dvs))
        results[name]["tail"] = {"top10_share": float(dvs[: max(1, len(dvs) // 10)].sum() / tot),
                                 "gini": float(gini)}
        print(f"  |dv| mass: top decile share {dvs[:102].sum()/tot:.3f}, gini {gini:.3f}")
    with open(sys.argv[1] if len(sys.argv) > 1 else "results.json", "w") as f:
        json.dump(results, f, indent=1)


if __name__ == "__main__":
    main()
