"""Probe B: B12-like repeated crossings — Jacobi drift of the event law.

Scene: Sun (fixed) + Jupiter-mass planet, circular orbit at 5.2 AU.
16 seeds: ships on crossing orbits through the Hill zone (a within +-0.15 a_p
relative, small e).  Each seed runs until it has had >= NCROSS conjunctions
resolved as events (or hits the planet / escapes).

Metrics:
  - the LAW's own Jacobi drift |C_J(t)-C_J(0)|/|C_J(0)| after each event,
    its growth exponent vs event count;
  - truth (DOP853, restricted problem, Sun fixed) same diagnostic (control);
  - encounter statistics (b, U) map vs truth (chaotic: compare distributions).

Jacobi (heliocentric circular restricted, autonomous in the rotating frame):
  C_J = n^2 |r|^2 + 2(muS/r + muP/|r-rp|) - |v - i n r|^2
"""
import numpy as np, json, time, warnings
warnings.filterwarnings("ignore")
from scipy.integrate import solve_ivp
import conjlaws as C

MU_SUN = 4.0 * np.pi ** 2
MU_P = 9.5459e-4 * MU_SUN
A_P = 5.2
N_P = np.sqrt(MU_SUN / A_P ** 3)
R_H = A_P * (MU_P / (3.0 * MU_SUN)) ** (1.0 / 3.0)
R_P = 71492.0 / 1.496e8
KAP, LAM = 0.5, 15.0
B_ACT = 3.0 * R_H
NCROSS = 20


def planet_state(t):
    th = N_P * t
    return A_P * np.exp(1j * th), 1j * N_P * A_P * np.exp(1j * th)


def jacobi(r, v, rp):
    vrot = v - 1j * N_P * r
    return (N_P * np.abs(r)) ** 2 + 2.0 * (MU_SUN / np.abs(r) + MU_P / np.abs(r - rp)) \
        - (vrot * vrot.conj()).real


def mean_longitude(r, v, mu):
    h, e, ev, a, _ = C.elements(r, v, mu)
    f = np.angle(r * np.conj(ev))
    E = C._E_from_f(f, max(e, 1e-12))
    varpi = np.angle(ev) if e > 1e-8 else 0.0
    return (varpi + (E - e * np.sin(E))) % (2 * np.pi), np.sqrt(mu / abs(a) ** 3) * np.sign(a), a


def next_conjunction(r, v, t, lam_p):
    lam, n, a = mean_longitude(r, v, MU_SUN)
    d = (lam - lam_p) % (2 * np.pi)
    if n > N_P:
        dt = (2 * np.pi - d) / (n - N_P)
    else:
        dt = d / (N_P - n) if d > 1e-9 else 2 * np.pi / (N_P - n + 1e-12)
    return t + dt, abs(n - N_P)


def run_map(r0, v0, t0=0.0, nmax=NCROSS, collide=True):
    r, v, t = r0, v0, t0
    rp, vp = planet_state(t)
    CJ0 = jacobi(r, v, rp)
    log = []
    nres = 0
    guard = 0
    while nres < nmax and guard < 4000:
        guard += 1
        tc, w_syn = next_conjunction(r, v, t, N_P * t % (2 * np.pi))
        if not np.isfinite(tc) or tc <= t:
            break
        # advance to conjunction, refine closest approach
        rc, vc = C.propagate(r, v, MU_SUN, tc - t)
        t = tc
        w_s = 2 * np.pi / max(w_syn, 1e-9)
        tstar, rb, vb, rp_s, vp_s = C.closest_approach(rc, vc, *planet_state(t),
                                                       MU_SUN, t, w_s)
        d = rb - rp_s
        b = abs(d)
        if b > B_ACT:
            r, v = rc, vc
            continue
        U = abs(vb - vp_s)
        if b < R_P:
            return log, CJ0, "collision", t
        w = max(KAP * R_H, LAM * b) / max(U, 1e-9)
        # event input state at window start tstar-w
        r_in, v_in = C.propagate(rb, vb, MU_SUN, -w)
        rp_in, vp_in = planet_state(tstar - w)
        r_out, v_out = C.encounter_event(r_in, v_in, rp_in, vp_in, MU_P, MU_SUN, w)
        r, v, t = r_out, v_out, tstar + w
        nres += 1
        rp, _ = planet_state(t)
        log.append((t, jacobi(r, v, rp)))
    return log, CJ0, "ok", t


def run_truth(r0, v0, t_end, rtol=1e-11):
    def rhs(t, y):
        rr = y[0] + 1j * y[1]
        vv = y[2] + 1j * y[3]
        rp, _ = planet_state(t)
        acc = -MU_SUN * rr / abs(rr) ** 3 - MU_P * (rr - rp) / abs(rr - rp) ** 3
        return [vv.real, vv.imag, acc.real, acc.imag]
    t_eval = None
    sol = solve_ivp(rhs, [0, t_end], [r0.real, r0.imag, v0.real, v0.imag],
                    rtol=rtol, atol=1e-13, method="DOP853", dense_output=False)
    ts = sol.t
    r = sol.y[0] + 1j * sol.y[1]
    v = sol.y[2] + 1j * sol.y[3]
    # Jacobi along the way, sampled
    rp = A_P * np.exp(1j * N_P * ts)
    CJ = jacobi(r, v, rp)
    # min distance to planet over run (collision check)
    dmin = np.min(np.abs(r - rp))
    return ts, CJ, dmin


if __name__ == "__main__":
    import sys
    nseeds = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    rng = np.random.default_rng(23)
    print(f"seed  t_end(yr)  #events  CJ drift law   exponent   CJ drift truth  dmin/rP")
    out = []
    t00 = time.time()
    for s in range(nseeds):
        u = rng.uniform(-0.15, 0.15)
        a0 = A_P * (1 + u)
        e0 = rng.uniform(0.005, 0.05)
        lam0 = rng.uniform(0, 2 * np.pi)
        varpi0 = rng.uniform(0, 2 * np.pi)
        f0 = lam0 - varpi0
        p = a0 * (1 - e0 ** 2)
        rr = p / (1 + e0 * np.cos(f0))
        r0 = rr * np.exp(1j * (varpi0 + f0))
        hh = np.sqrt(MU_SUN * p)
        vr = MU_SUN / hh * e0 * np.sin(f0)
        vt = MU_SUN / hh * (1 + e0 * np.cos(f0))
        ur = np.exp(1j * (varpi0 + f0))
        v0 = vr * ur + vt * (1j * ur)
        log, CJ0, status, t_end = run_map(r0, v0)
        if status == "collision" or not log:
            print(f"{s:3d}  status={status}")
            continue
        drift = np.array([abs(c - CJ0) / abs(CJ0) for _, c in log])
        k = np.arange(1, len(drift) + 1)
        expon = np.polyfit(np.log(k), np.log(np.maximum(drift, 1e-18)), 1)[0]
        ts, CJt, dmin = run_truth(r0, v0, min(t_end, 6000.0))
        dtr = abs(CJt[-1] - CJt[0]) / abs(CJt[0])
        print(f"{s:3d}  {t_end:8.0f}  {len(log):3d}     {drift[-1]:.2e}      {expon:5.2f}      {dtr:.2e}    {dmin/R_P:8.1f}")
        out.append({"seed": s, "n": len(log), "drift_law": drift.tolist(),
                    "exponent": float(expon), "drift_truth": float(dtr), "t_end": float(t_end)})
    print(f"wall: {time.time()-t00:.0f} s")
    json.dump(out, open("probe_b.json", "w"), indent=1)
