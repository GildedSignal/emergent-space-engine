#!/usr/bin/env python3
"""Scout falsifier 20261006-1135-scout-7a46.

Question: on the conic's singular set (L=0, no turning point, near-radial,
plunge), does a square-root (Levi-Civita) generator serve the encounter at
zero per-step cost where the stepping fallback pays diverging work?

Scene: the planet's doll. Planet mu at origin (planetocentric, non-rotating);
parent M=1 on a circular orbit R=1, n=1; r_H=0.03; r_in=0.4 r_H is the doll's
edge; entry r0 = 0.98 r_in.

Schemes:
  C     exact LC drift (z=u^2, dt=|u|^2 dtau, u''=(E/2)u) + tide kicks only,
        Strang D(dtau/2) K D(dtau/2), K kicks per encounter.
  A-rt  velocity Verlet on planet monopole + tide, dt = min(cap, alpha*r).
  A-fix velocity Verlet, constant dt.

Truth: DOP853 rtol 1e-12 on the same inertial ODE.
Cost unit: events (A: steps; C: kicks). C's drift evaluates no forces.
"""
import json
import math
import sys

M, RORB, NORB = 1.0, 1.0, 1.0
RH = 0.03
MU = 3.0 * RH**3
R_IN = 0.4 * RH
R_START = 0.98 * R_IN
R_SURF = 1e-4 * RH
V_H = NORB * RH
THETA0 = 3.0 * math.pi / 4.0
STEPCAP = 500_000
KICKS_DEFAULT = 8


def star(t):
    return complex(math.cos(NORB * t), math.sin(NORB * t))


def f_tide(z, t):
    xs = star(t)
    d = z - xs
    return -d / (abs(d)**3) - xs / RORB**3


def f_total(z, t):
    return -MU * z / (abs(z)**3) + f_tide(z, t)


# ------------------------------------------------------------- truth
def truth(state0, kind, r_exit, rtol=1e-12, tide=True):
    from scipy.integrate import solve_ivp
    y0 = [state0[0].real, state0[0].imag, state0[1].real, state0[1].imag]

    def rhs(t, y):
        f = f_total(complex(y[0], y[1]), t) if tide else -MU * complex(y[0], y[1]) / (math.hypot(y[0], y[1])**3)
        return (y[2], y[3], f.real, f.imag)

    def ev(t, y):
        return math.hypot(y[0], y[1]) - r_exit
    ev.terminal = True
    ev.direction = -1.0 if kind == "hit" else 1.0
    tmax = 100.0
    sol = solve_ivp(rhs, (0.0, tmax), y0, method="DOP853", rtol=rtol,
                    atol=1e-15, events=[ev])
    if not sol.t_events[0].size:
        return None
    ye = sol.y_events[0][0]
    return complex(ye[0], ye[1]), complex(ye[2], ye[3]), sol.t_events[0][0]


def truth_radial_notide(state0, kind, r_exit):
    """Exact two-body truth for L=0 cases by mirror symmetry; time by quad.
    (DOP853 cannot integrate through the r=0 singularity; LC can.)"""
    from scipy.integrate import quad
    z0, zd0 = state0
    r0, v0 = abs(z0), abs(zd0)
    E = 0.5 * v0**2 - MU / r0

    def t_of_r(r):
        return quad(lambda rr: 1.0 / math.sqrt(2.0 * (E + MU / rr)),
                    r_exit, r0, limit=400)[0]
    v_e = math.sqrt(2.0 * (E + MU / r_exit))
    def i_of(r):
        return quad(lambda rr: 1.0 / math.sqrt(2.0 * (E + MU / rr)),
                    0.0, r, limit=400)[0]
    if kind == "hit":
        return z0 * (r_exit / r0), zd0 / v0 * v_e, t_of_r(r_exit)
    # outbound exit on the far side, after passing r = 0
    return z0 * (r_exit / r0), -zd0 / v0 * v_e, i_of(r0) + i_of(r_exit)


# ------------------------------------------------------- LC machinery
def csqrt(z):
    return complex(math.sqrt((abs(z) + z.real) / 2.0),
                   math.copysign(math.sqrt((abs(z) - z.real) / 2.0), z.imag))


def seg_fns(u0, up0, kap):
    """Closed-form LC drift segment starting at (u0, up0) with u''=kap*u.
    Returns (u_of, up_of, t_of) as functions of segment phase th."""
    if kap < 0.0:
        nu = math.sqrt(-kap)
        a, b = u0, up0 / nu
        A = (abs(a)**2 + abs(b)**2) / 2.0
        B = (abs(a)**2 - abs(b)**2) / 2.0
        C = (a * b.conjugate()).real
        return (lambda th: a * math.cos(th) + b * math.sin(th),
                lambda th: nu * (-a * math.sin(th) + b * math.cos(th)),
                lambda th: (A * th + 0.5 * B * math.sin(2 * th)
                + 0.5 * C * (1.0 - math.cos(2 * th))) / nu)
    if kap > 0.0:
        nu = math.sqrt(kap)
        a, b = u0, up0 / nu
        A = (abs(a)**2 + abs(b)**2) / 2.0
        B = (abs(a)**2 - abs(b)**2) / 2.0
        C = (a * b.conjugate()).real
        return (lambda th: a * math.cosh(th) + b * math.sinh(th),
                lambda th: nu * (a * math.sinh(th) + b * math.cosh(th)),
                lambda th: (0.5 * A * math.sinh(2 * th) + B * th
                + 0.5 * C * (math.cosh(2 * th) - 1.0)) / nu)
    a, b = u0, up0
    return (lambda th: a + b * th,
            lambda th: b,
            lambda th: abs(a)**2 * th + (a * b.conjugate()).real * th**2
            + abs(b)**2 * th**3 / 3.0)


def nu_of(kap):
    return 1.0 if kap == 0.0 else math.sqrt(abs(kap))


def find_crossing(u0, up0, kap, th_lim, r_t, direction, ns=96):
    """First phase th in (0, th_lim] where |u|^2 (= physical r) crosses r_t
    with the given direction (+1: from below to >=; -1: from above to <=), or
    None. For kap >= 0, |u|^2 is unimodal with an analytic vertex, so narrow
    dips (hit radii) are bracketed exactly instead of sampled."""
    u_of, _, _ = seg_fns(u0, up0, kap)
    g0 = abs(u0)**2 - r_t
    if kap >= 0.0 and th_lim > 0.0:
        nu = nu_of(kap)
        if kap == 0.0:
            ab2 = abs(up0)**2
            th_star = -(u0 * up0.conjugate()).real / ab2 if ab2 > 0.0 else 0.0
        else:
            a, b = u0, up0 / math.sqrt(kap)
            A = (abs(a)**2 + abs(b)**2) / 2.0
            C = (a * b.conjugate()).real
            th_star = 0.25 * math.log((A - C) / (A + C)) if A + C != 0.0 \
                else 0.0
        th_star = min(max(th_star, 0.0), th_lim)
        inside = abs(u_of(th_star))**2 < r_t
        if direction > 0:
            if g0 < 0.0 or inside:
                lo, hi = max(th_star, 1e-15), th_lim
                if abs(u_of(hi))**2 < r_t:
                    return None
                for _ in range(80):
                    mid = 0.5 * (lo + hi)
                    if abs(u_of(mid))**2 >= r_t:
                        hi = mid
                    else:
                        lo = mid
                return hi if hi > 1e-15 else None
            return None
        if direction < 0:
            if g0 <= 0.0 or not inside:
                return None
            lo, hi = 0.0, th_star
            for _ in range(80):
                mid = 0.5 * (lo + hi)
                if abs(u_of(mid))**2 <= r_t:
                    hi = mid
                else:
                    lo = mid
            return hi if hi > 1e-15 else None
    prev_th, prev_g = 0.0, g0
    prev_th, prev_g = 0.0, g0
    for i in range(1, ns + 1):
        th = th_lim * i / ns
        g = abs(u_of(th))**2 - r_t
        hit = (direction > 0 and prev_g < 0.0 <= g) or \
              (direction < 0 and prev_g > 0.0 >= g)
        if hit:
            lo, hi = prev_th, th
            for _ in range(80):
                mid = 0.5 * (lo + hi)
                gm = abs(u_of(mid))**2 - r_t
                if (direction > 0 and gm >= 0.0) or (direction < 0 and gm <= 0.0):
                    hi = mid
                else:
                    lo = mid
            return hi
        prev_th, prev_g = th, g
    return None


def lc_run(state0, kind, r_exit, kicks=KICKS_DEFAULT, tide=True):
    """Scheme C. Returns dict or None."""
    z, zd = state0
    t = 0.0
    u = csqrt(z)
    up = zd * u.conjugate() / 2.0
    E = 0.5 * abs(zd)**2 - MU / abs(z)
    direction = -1.0 if kind == "hit" else 1.0

    # pre-pass: drift-only phase length to the exit, to space the kicks
    kap = E / 2.0
    nu = nu_of(kap)
    th_win = (64.0 if kap > 0 else 24.0 * math.pi) * max(1.0, nu)
    th_x = find_crossing(u, up, kap, th_win, r_exit, direction, ns=2048)
    if th_x is None:
        return None
    tau_x = th_x / nu
    dtau = tau_x / kicks

    nkicks = 0
    narith = 0

    def exit_or_drift(u, up, t, kap, th_half):
        """Drift one half chunk; return (exited, u, up, t)."""
        th_e = find_crossing(u, up, kap, th_half * 1.001 + 1e-15, r_exit,
                             direction)
        u_of, up_of, t_of = seg_fns(u, up, kap)
        if th_e is not None:
            return True, u_of(th_e), up_of(th_e), t + t_of(th_e)
        return False, u_of(th_half), up_of(th_half), t + t_of(th_half)

    def state_z(u, up):
        r2 = u.real**2 + u.imag**2
        return u * u, 2.0 * u * up / r2

    for _ in range(6 * kicks + 16):
        kap = E / 2.0
        th_half = 0.5 * dtau * nu_of(kap)
        ex, u, up, t = exit_or_drift(u, up, t, kap, th_half)
        narith += 200
        if ex:
            z, zd = state_z(u, up)
            return dict(z=z, zd=zd, t=t, kicks=nkicks, narith=narith)
        if tide:
            # kick at the chunk midpoint (v2's w = ds * f'(U) at the state)
            z, zd = state_z(u, up)
            dt_k = (u.real**2 + u.imag**2) * dtau
            dz = f_tide(z, t) * dt_k
            E += (zd * dz.conjugate()).real + 0.5 * abs(dz)**2
            zd = zd + dz
            up = zd * u.conjugate() / 2.0
            nkicks += 1
        kap = E / 2.0
        th_half = 0.5 * dtau * nu_of(kap)
        ex, u, up, t = exit_or_drift(u, up, t, kap, th_half)
        narith += 200
        if ex:
            z, zd = state_z(u, up)
            return dict(z=z, zd=zd, t=t, kicks=nkicks, narith=narith)
    return None


# ------------------------------------------------------------- scheme A
def verlet(state0, kind, r_exit, rule):
    mode, p, cap = rule  # ('rt', alpha, dtcap) or ('fix', dt, None)
    z, zd = state0
    t = 0.0
    f = f_total(z, t)
    evals = 1
    for step in range(STEPCAP + 1):
        r = abs(z)
        dt = min(cap, p * r) if mode == "rt" else p
        if dt <= 0.0:
            dt = 1e-18
        z_new = z + zd * dt + 0.5 * f * dt * dt
        t_new = t + dt
        f_new = f_total(z_new, t_new)
        evals += 1
        zd_new = zd + 0.5 * (f + f_new) * dt
        # crossing?
        r_new = abs(z_new)
        crossed = False
        if kind == "hit":
            crossed = r_new <= r_exit
        else:
            vr_out = (z_new * zd_new.conjugate()).real > 0.0
            crossed = r_new >= r_exit and vr_out and (r >= r_exit or step > 0)
        if crossed:
            lo, hi = 0.0, dt
            for _ in range(60):
                s = 0.5 * (lo + hi)
                zs = z + zd * s + 0.5 * f * s * s
                zds = zd + 0.5 * (f + f_total(zs, t + s)) * s
                evals += 1
                rs = abs(zs)
                c = (rs <= r_exit) if kind == "hit" else \
                    (rs >= r_exit and (zs * zds.conjugate()).real > 0.0)
                if c:
                    hi = s
                else:
                    lo = s
            s = hi
            z_out = z + zd * s + 0.5 * f * s * s
            zd_out = zd + 0.5 * (f + f_total(z_out, t + s)) * s
            evals += 1
            return dict(z=z_out, zd=zd_out, t=t + s, steps=step + 1,
                        evals=evals, capped=False)
        z, zd, t, f = z_new, zd_new, t_new, f_new
    return dict(z=z, zd=zd, t=t, steps=STEPCAP, evals=evals, capped=True)


# ------------------------------------------------------------- cases
def entry_state(kind, q=None, vinf=None, Lfrac=None, Esign=None):
    z0 = R_START * complex(math.cos(THETA0), math.sin(THETA0))
    e_th = complex(math.cos(THETA0), math.sin(THETA0))
    if kind in ("exit", "hit"):
        v = math.sqrt(vinf**2 + 2.0 * MU / R_START)
        if kind == "hit":
            vr, vt = -v, 0.0
        elif Lfrac is not None:
            L = Lfrac
            vt = L / R_START
            vr = -math.sqrt(max(v**2 - vt**2, 0.0))
        else:
            L = (MU / vinf) * math.sqrt((1.0 + q * vinf**2 / MU)**2 - 1.0)
            vt = L / R_START
            vr = -math.sqrt(max(v**2 - vt**2, 0.0))
        zd = vr * e_th + vt * 1j * e_th
        return z0, zd
    if kind == "thru":  # bound radial fall, passes r=0, exits at 0.95 R_START
        vr = -0.7 * math.sqrt(2.0 * MU / R_START)
        return z0, vr * e_th
    if kind == "par":  # exact parabolic radial fall, E = 0
        vr = -math.sqrt(2.0 * MU / R_START)
        return z0, vr * e_th
    raise ValueError(kind)


def r_exit_of(kind):
    if kind == "hit":
        return R_SURF
    if kind == "thru":
        return 0.95 * R_START
    return R_IN


def err_rel(res, tr):
    dz = abs(res["z"] - tr[0]) / max(abs(tr[0]), 1e-30)
    dv = abs(res["zd"] - tr[1]) / max(abs(tr[1]), 1e-30)
    dt = abs(res["t"] - tr[2]) / max(abs(tr[2]), 1e-30)
    return math.hypot(math.hypot(dz, dv), dt)


def main():
    out = {"units": dict(MU=MU, RH=RH, R_IN=R_IN, R_START=R_START,
                         R_SURF=R_SURF, V_H=V_H)}
    cases = []
    for vinf_f in (0.3, 0.7):
        for q_f in (0.3, 0.1, 0.03, 0.01, 0.003):
            cases.append(dict(name=f"q{q_f:g}_v{vinf_f:g}", kind="exit",
                              q=q_f * RH, vinf=vinf_f * V_H))
    cases.append(dict(name="thru", kind="thru"))
    cases.append(dict(name="par", kind="par"))
    cases.append(dict(name="hit_v0.3", kind="hit", vinf=0.3 * V_H))
    cases.append(dict(name="nr_q3e-6", kind="exit", vinf=0.3 * V_H,
                      Lfrac=math.sqrt(2 * MU * 3e-6)))
    rows = []
    # calibration case
    cal = next(c for c in cases if c["name"] == "q0.1_v0.7")
    st0 = entry_state(cal["kind"], q=cal.get("q"), vinf=cal.get("vinf"),
                      Lfrac=cal.get("Lfrac"))
    tr = truth(st0, cal["kind"], r_exit_of(cal["kind"]))
    cals = {}
    for K in (4, 8, 16, 32):
        r = lc_run(st0, cal["kind"], r_exit_of(cal["kind"]), kicks=K)
        cals[f"C_K{K}"] = err_rel(r, tr)
    for a in (0.4, 0.2, 0.1, 0.05, 0.025):
        r = verlet(st0, cal["kind"], r_exit_of(cal["kind"]), ("rt", a, 2e-3))
        cals[f"A_a{a:g}"] = (err_rel(r, tr), r["evals"])
    print("CALIBRATION", json.dumps(cals, indent=1))
    out["calibration"] = {k: (v if not isinstance(v, tuple) else list(v))
                          for k, v in cals.items()}
    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.2
    dt_fix = alpha * 0.1 * RH
    out["locked"] = dict(alpha=alpha, dt_fix=dt_fix, K=KICKS_DEFAULT)
    print(f"locked alpha={alpha} dt_fix={dt_fix:.3e}")

    for c in cases:
        st0 = entry_state(c["kind"], q=c.get("q"), vinf=c.get("vinf"),
                          Lfrac=c.get("Lfrac"))
        rx = r_exit_of(c["kind"])
        tr = truth(st0, c["kind"], rx)
        row = dict(case=c["name"], kind=c["kind"])
        if c.get("q"):
            row["q_over_rh"] = c["q"] / RH
        if c.get("vinf"):
            row["vinf_over_vh"] = c["vinf"] / V_H
        if c.get("Lfrac"):
            row["L"] = c["Lfrac"]
        # truth-quality check on singular cases
        if c["name"] in ("thru", "par", "nr_q3e-6", "hit_v0.3"):
            tr2 = truth(st0, c["kind"], rx, rtol=1e-14)
            row["truth_agreement"] = err_rel(
                dict(z=tr2[0], zd=tr2[1], t=tr2[2]), tr)
        if c["kind"] in ("thru", "par", "hit"):
            tr0 = truth_radial_notide(st0, c["kind"], rx)
        else:
            tr0 = truth(st0, c["kind"], rx, tide=False)
        Cn = lc_run(st0, c["kind"], rx, kicks=KICKS_DEFAULT, tide=False)
        row["C_notide_err"] = err_rel(Cn, tr0) if Cn else None
        for K in (4, 8, 16):
            r = lc_run(st0, c["kind"], rx, kicks=K)
            if r:
                row[f"C_K{K}"] = dict(err=err_rel(r, tr), kicks=r["kicks"],
                                      t=r["t"])
        for am in (1.0, 0.25, 0.0625):
            r = verlet(st0, c["kind"], rx, ("rt", alpha * am, 2e-3))
            row[f"A_rt_a{am:g}"] = dict(err=err_rel(r, tr), evals=r["evals"],
                                        capped=r["capped"])
        r = verlet(st0, c["kind"], rx, ("fix", dt_fix, None))
        row["A_fix"] = dict(err=err_rel(r, tr), evals=r["evals"],
                            capped=r["capped"])
        rows.append(row)
        print(c["name"], "C_notide", row["C_notide_err"], "C_K8",
              row.get("C_K8"), "A_rt", row.get("A_rt_a1"))
    out["rows"] = rows
    import pathlib
    pathlib.Path(__file__).parent.joinpath("results.json").write_text(
        json.dumps(out, indent=1))
    print("wrote results.json")


if __name__ == "__main__":
    main()
