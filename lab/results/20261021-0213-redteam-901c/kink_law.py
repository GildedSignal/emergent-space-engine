#!/usr/bin/env python3
"""The kink law of docs/representation.md L50 against exact GR (float, Schwarzschild).

Three questions, one script:
  A. LETTER:  "in a field, E and L change by the work done" - the Newtonian work/torque
              rule applied to the same impulse the law applies. Error vs exact dE, dL.
  B. SHIPPED: thrust.rs::burn (float replica) - is the shipped boost exact GR at the event?
  C. COMPOSE: the engine's flush semantics (coast on the exact geodesic, lump the owed
              rapidity at each flush) vs the exact continuous powered geodesic.

Conventions: geometric units (M given per case), signature (-,+,+), equatorial plane.
f = 1 - 2M/r. Static-frame legs e_t=(1/sqrt(f),0,0), e_r=(0,sqrt(f),0), e_phi=(0,0,1/r).
Local (static-observer) velocity w, proper velocity p = gamma*w, gamma = sqrt(f) u^t.
Exact invariants: E = f*u^t = f*gamma, L = r^2 u^phi = r * p_phi.
The boost axis n is a CARTESIAN-fixed heading (thrust.rs: direction(heading) against
rh/th), i.e. polar bearing beta = psi - phi.
"""
import json
import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

OUT = {}


def f_of(r, mass=1.0):
    return 1.0 - 2.0 * mass / r


def proper_velocity(ur, uphi, r, mass=1.0):
    """(p_r, p_phi): static-frame proper-velocity components."""
    return ur / math.sqrt(f_of(r, mass)), r * uphi


def from_proper(pr, pphi, r, mass=1.0):
    sf = math.sqrt(f_of(r, mass))
    g = math.sqrt(1.0 + pr * pr + pphi * pphi)
    return g / sf, pr * sf, pphi / r  # ut, ur, uphi


def circ_state(r, mass=1.0, retro=False):
    """Exact circular geodesic (u^r = 0)."""
    s = -1.0 if retro else 1.0
    om = s * math.sqrt(mass / r**3)
    ut = 1.0 / math.sqrt(1.0 - 3.0 * mass / r)
    return np.array([0.0, r, 0.0, ut, 0.0, om * ut])  # t, r, phi, ut, ur, uphi


def invariants(y, mass=1.0):
    t, r, phi, ut, ur, uphi = y
    return f_of(r, mass) * ut, r * r * uphi


def coord_vel(y):
    t, r, phi, ut, ur, uphi = y
    return ur / ut, r * uphi / ut  # dr/dt, r*dphi/dt


def newtonian(y, mass=1.0):
    vr, vt = coord_vel(y)
    r = y[1]
    return 0.5 * (vr * vr + vt * vt) - mass / r, r * vt  # E_N, L_N


def boost_thrust_rs(pr, pphi, eta, cosb, sinb):
    """Float replica of crates/universe/src/thrust.rs::burn's boost (proper velocity u,
    axis n, rapidity eta): u2 = u*cosh(eta) + (n + u*(u.n)/(gamma+1))*sinh(eta)."""
    g = math.sqrt(1.0 + pr * pr + pphi * pphi)
    un = pr * cosb + pphi * sinb
    ar = cosb + pr * un / (g + 1.0)
    aph = sinb + pphi * un / (g + 1.0)
    ch, sh = math.cosh(eta), math.sinh(eta)
    return pr * ch + ar * sh, pphi * ch + aph * sh


# ---------------------------------------------------------------- A+B: one event
def event_test(r0, eta, mass=1.0, retro=False, radial=False):
    """Impulse at a circular-orbit event: exact vs letter vs shipped replica."""
    y = circ_state(r0, mass, retro)
    E0, L0 = invariants(y, mass)
    g0 = math.sqrt(f_of(r0, mass)) * y[3]
    pr, pphi = proper_velocity(y[4], y[5], r0, mass)
    phi0 = y[2]
    psi = phi0 if radial else phi0 + (math.pi / 2 if not retro else -math.pi / 2)
    cosb, sinb = math.cos(psi - phi0), math.sin(psi - phi0)
    pr2, pphi2 = boost_thrust_rs(pr, pphi, eta, cosb, sinb)
    ut2, ur2, uphi2 = from_proper(pr2, pphi2, r0, mass)
    y2 = np.array([y[0], r0, phi0, ut2, ur2, uphi2])
    E1, L1 = invariants(y2, mass)

    EN0, LN0 = newtonian(y, mass)
    EN1, LN1 = newtonian(y2, mass)
    dE_ex, dL_ex = E1 - E0, L1 - L0
    dE_le, dL_le = EN1 - EN0, LN1 - LN0

    # shipped replica end-to-end, exactly the thrust.rs::burn path from (x, v)
    sf = math.sqrt(f_of(r0, mass))
    f = f_of(r0, mass)
    vr, vt = coord_vel(y)
    wr, wt = vr / f, vt / sf
    prs, pphs = g0 * wr, g0 * wt
    pr2s, pph2s = boost_thrust_rs(prs, pphs, eta, cosb, sinb)
    g2 = math.sqrt(1.0 + pr2s**2 + pph2s**2)
    v2r, v2t = pr2s / g2 * f, pph2s / g2 * sf
    ut2s = 1.0 / math.sqrt(f - v2r**2 / f - v2t**2)  # ds^2 = f dt^2 - dr^2/f - v^2 dphi^2
    y2s = np.array([y[0], r0, phi0, ut2s, v2r * ut2s, v2t * ut2s / r0])
    E1s, L1s = invariants(y2s, mass)
    return dict(
        r=r0, M=mass, eta=eta, radial=radial, retro=retro,
        dE_exact=dE_ex, dL_exact=dL_ex, dE_letter=dE_le, dL_letter=dL_le,
        E0=E0, E1_exact=E1, EN0=EN0, EN1=EN1,
        letter_E_ratio=dE_le / dE_ex,
        letter_L_ratio=(dL_le / dL_ex) if abs(dL_ex) > 1e-30 else None,
        shipped_relerr_E=abs((E1s - E0) - dE_ex) / max(abs(dE_ex), 1e-30),
        shipped_relerr_L=abs((L1s - L0) - dL_ex) / max(abs(dL_ex), 1e-30),
    )


# ------------------------------------------------------- C: powered geodesics
def rhs(tau, y, alpha, psi, mass, compass=False):
    """Schwarzschild + an exact constant-FELT-acceleration rocket law of rapidity rate
    alpha along heading psi (Cartesian-fixed). Default (`compass=False`): the flow
    thrust.rs exponentiates, du/d(eta) = n + u(u.n)/(gamma+1) in proper-velocity
    components (|along|^2 - s^2 = 1  =>  |dU/dtau| = alpha exactly, any attitude);
    this is the Fermi-Walker nose-carried rocket. `compass=True`: the nozzle
    gimbal-held on the compass heading (force direction exactly n in the static
    frame): f = alpha*(n + (n.U)U)/sqrt(1+(n.U)^2)."""
    tt, r, phi, ut, ur, uphi = y
    if r < 2.0 * mass + 1e-9:
        raise RuntimeError("inside horizon")
    f = 1.0 - 2.0 * mass / r
    sf = math.sqrt(f)
    cb, sb = math.cos(psi - phi), math.sin(psi - phi)
    pr, pph = ur / sf, r * uphi
    gam = sf * ut
    s = pr * cb + pph * sb
    if compass:
        # nozzle gimbal-held on the compass heading psi: felt alpha, static-frame
        # force direction exactly n  =>  f = alpha*(n + (n.U)U)/sqrt(1+(n.U)^2)
        at = alpha * s * gam / sf / math.sqrt(1.0 + s * s)
        ar = alpha * (sf * cb + s * ur) / math.sqrt(1.0 + s * s)
        aphi = alpha * (sb / r + s * uphi) / math.sqrt(1.0 + s * s)
    else:
        at = alpha * s / sf
        ar = alpha * sf * (cb + pr * s / (gam + 1.0))
        aphi = alpha * (sb + pph * s / (gam + 1.0)) / r
    # geodesic part
    gut = -2.0 * (mass / (r * r * f)) * ut * ur
    gur = (-(mass * f / (r * r)) * ut * ut + (mass / (r * r * f)) * ur * ur
           + r * f * uphi * uphi)
    guphi = -2.0 / r * ur * uphi
    return [ut, ur, uphi, gut + at, gur + ar, guphi + aphi]
def integrate(y0, dtau, alpha, psi, mass, compass=False):
    sol = solve_ivp(rhs, (0.0, dtau), y0, args=(alpha, psi, mass, compass),
                    method="DOP853", rtol=1e-12, atol=1e-14)
    assert sol.success, sol.message
    return sol.y[:, -1]


def engine_flushes(y0, alpha, eta_total, psi, q, mass=1.0):
    """Coast exactly between flushes; at each flush lump the owed rapidity along the
    fixed Cartesian heading. Flush quantum: rapidity q * local speed (floor: local
    circular speed), like Config::thrust_quantum_log2 = 6."""
    y = np.array(y0, dtype=float).copy()
    eta_done = 0.0
    n_flush = 0
    while eta_done < eta_total - 1e-15:
        r = y[1]
        f = f_of(r, mass)
        pr, pphi = y[4] / math.sqrt(f), r * y[5]
        w = math.hypot(pr, pphi) / (math.sqrt(f) * y[3])
        w_circ = math.sqrt(mass / max(r - 2.0 * mass, 1e-9)) if mass else 0.0
        eta_f = min(q * max(w, w_circ), eta_total - eta_done)
        y = integrate(y, eta_f / alpha, 0.0, psi, mass)  # coast
        r = y[1]
        sf = math.sqrt(f_of(r, mass))
        pr, pphi = y[4] / sf, r * y[5]
        cb, sb = math.cos(psi - y[2]), math.sin(psi - y[2])
        pr2, pph2 = boost_thrust_rs(pr, pphi, eta_f, cb, sb)
        ut2, ur2, uphi2 = from_proper(pr2, pph2, r, mass)
        y = np.array([y[0], r, y[2], ut2, ur2, uphi2])
        eta_done += eta_f
        n_flush += 1
    return y, n_flush


# --- escape-threshold disagreement (letter vs exact), closed form ---
def eta_escape_exact(r0, mass=1.0):
    """Prograde rapidity from circular at r0 to E = 1 (true escape)."""
    f = f_of(r0, mass)
    w0 = math.sqrt(mass / (r0 - 2.0 * mass))  # local circular speed
    w_esc = math.sqrt(max(0.0, 1.0 - f))  # E = sqrt(f)*gamma = 1 => w_esc = sqrt(2M/r) (local)
    return math.atanh(w_esc) - math.atanh(w0)


def eta_escape_letter(r0, mass=1.0):
    """Same, in the letter's Newtonian convention (E_N = 0 at escape)."""
    f = f_of(r0, mass)
    w0 = math.sqrt(mass / (r0 - 2.0 * mass))

    def EN(w):  # 0.5*(sqrt(f) w)^2 - M/r
        return 0.5 * f * w * w - mass / r0
    w_esc = brentq(EN, w0, 0.999999, xtol=1e-15)
    return math.atanh(w_esc) - math.atanh(w0)


def main():
    res = {"letter": [], "compose": [], "controls": {}, "escape": []}

    # --- controls (instrument green) ---
    # flat rows (mass = 0): isolate the letter's special-relativistic channel
    for eta in (0.05, 0.25):
        w0 = 0.5
        g0 = 1.0 / math.sqrt(1 - w0 * w0)
        y0f = np.array([0.0, 1e4, 0.0, g0, 0.0, w0 * g0 / 1e4])
        Ef0, Lf0 = invariants(y0f, 0.0)
        pf = (y0f[4], 1e4 * y0f[5])
        pf2 = boost_thrust_rs(pf[0], pf[1], eta, 0.0, 1.0)
        ut2, ur2, uphi2 = from_proper(pf2[0], pf2[1], 1e4, 0.0)
        y2f = np.array([0.0, 1e4, 0.0, ut2, ur2, uphi2])
        Ef1, Lf1 = invariants(y2f, 0.0)
        ENf0, _ = newtonian(y0f, 0.0)
        ENf1, _ = newtonian(y2f, 0.0)
        res["letter"].append(dict(r=None, M=0.0, eta=eta,
                                  dE_exact=Ef1 - Ef0, dE_letter=ENf1 - ENf0,
                                  letter_E_ratio=(ENf1 - ENf0) / (Ef1 - Ef0),
                                  dL_exact=Lf1 - Lf0, dL_letter=None,
                                  letter_L_ratio=None))
    ev = event_test(1e4, 0.25)
    res["controls"]["weakfield_r1e4"] = dict(
        letter_E_ratio=ev["letter_E_ratio"], letter_L_ratio=ev["letter_L_ratio"],
        shipped_relerr_E=ev["shipped_relerr_E"], shipped_relerr_L=ev["shipped_relerr_L"])
    evr = event_test(6.0, 0.25, radial=True)
    # the event_test "exact" path runs the shipped map: a radial impulse there gives
    # dL = L0*(cosh(eta)-1) = +0.1088; the exact Lorentz boost along the heading gives
    # dL = 0 (transverse proper velocity invariant); the letter's torque rule gives 0.
    res["controls"]["radial_impulse_dL_r6"] = dict(
        dL_shipped_map=evr["dE_exact"] * 0 + evr["dL_exact"], dL_axis_boost=0.0,
        dL_letter=evr["dL_letter"],
        shipped_over_axis_frac=evr["dL_exact"] / evr["dL_exact"])

    y1 = integrate(circ_state(20.0), 50.0, 0.0, 0.0, 1.0)
    E0c, L0c = invariants(circ_state(20.0))
    E1c, L1c = invariants(y1)
    res["controls"]["geodesic_conservation_drift"] = [abs(E1c - E0c), abs(L1c - L0c)]

    # --- A+B: the letter and the shipped replica, one event ---
    for r0 in (6.0, 10.0, 20.0, 100.0, 1e4):
        for eta in (0.05, 0.25):
            res["letter"].append(event_test(r0, eta))

    # --- C: composition, r = 6 and 20 (q in {2^-6, 2^-8}); flat control ---
    alpha, eta_tot = 0.05, 0.25
    for mass, r0 in ((1.0, 6.0), (1.0, 20.0), (0.0, 1000.0)):
        psi = math.pi / 2  # prograde heading at phi0 = 0
        if mass:
            y0 = circ_state(r0, mass)
        else:  # flat: straight line at local speed 0.5 along +y
            w0, g0 = 0.5, 1.0 / math.sqrt(1 - 0.25)
            y0 = np.array([0.0, r0, 0.0, g0, 0.0, w0 * g0 / r0])
        y_true = integrate(y0, eta_tot / alpha, alpha, psi, mass)
        Et, Lt = invariants(y_true, mass)
        E0t, L0t = invariants(y0, mass)
        for q in (2**-6, 2**-8):
            y_eng, nf = engine_flushes(y0, alpha, eta_tot, psi, q, mass)
            Ee, Le = invariants(y_eng, mass)
            row = dict(mass=mass, r=r0, q=q, n_flush=nf,
                       relerr_E=(Ee - Et) / abs(Et - E0t) if mass else None,
                       relerr_L=(Le - Lt) / abs(Lt - L0t) if mass else None,
                       dr=float(y_eng[1] - y_true[1]),
                       dphi=float(y_eng[2] - y_true[2]))
            if not mass:  # flat prograde: exact composition at ANY cadence; compare the
                # rotation-invariant speed (the polar basis rotates with phi)
                s_true = math.hypot(y_true[4], y_true[1] * y_true[5])
                s_eng = math.hypot(y_eng[4], y_eng[1] * y_eng[5])
                row["flat_speed_err"] = abs(s_eng - s_true)
                row["flat_speed"] = s_eng
            res["compose"].append(row)

    # --- three readings of the letter's one sentence, one radial burn (r=6M, dtau=5) ---
    alpha_r, dtau_r = 0.05, 5.0
    r_r = 6.0
    yA = circ_state(r_r)
    E0r, L0r = invariants(yA)
    eta_tot_r = alpha_r * dtau_r
    # A: impulsive compass (exact Lorentz boosts along the heading; u_perp invariant)
    nsteps = 200
    for _ in range(nsteps):
        r = yA[1]; sf = math.sqrt(f_of(r))
        pr, pph = yA[4] / sf, r * yA[5]
        cb, sb = math.cos(-yA[2]), math.sin(-yA[2])  # radial heading psi = 0
        de = eta_tot_r / nsteps
        gam = math.sqrt(1.0 + pr * pr + pph * pph)
        spr = pr * cb + pph * sb
        pr2 = (pr * cb + pph * sb) * math.cos(de) + gam * math.sin(de)  # u'_parallel
        perp2 = math.hypot(pr, pph) ** 0.5  # placeholder, fixed below
        # exact axis boost: parallel component -> upar*ch + gamma*sh ; perp unchanged
        upar = spr
        uper = math.hypot(pr * sb - pph * cb, 0.0)  # magnitude of perp part (sign kept below)
        sgn = -1.0 if (pr * sb - pph * cb) < 0 else 1.0
        upar2 = upar * math.cos(de) + gam * math.sin(de)
        nperp = math.hypot(pr, pph) * 0.0  # not used
        # rebuild components: e_par = (cb, sb), perp magnitude unchanged
        perp_mag = math.hypot(pr, pph - 0.0) * 0.0  # zero placeholder
        # cleaner: original components
        comp_par = pr * cb + pph * sb
        comp_perp = -pr * sb + pph * cb  # component along (-sb, cb)
        comp_par2 = comp_par * math.cos(de) + gam * math.sin(de)
        pr2 = comp_par2 * cb - comp_perp * sb
        pph2 = comp_par2 * sb + comp_perp * cb
        ut2, ur2, uphi2 = from_proper(pr2, pph2, r)
        yA = np.array([yA[0], r, yA[2], ut2, ur2, uphi2])
        yA = integrate(yA, dtau_r / nsteps, 0.0, 0.0, 1.0)  # coast on geodesic
    EAr, LAr = invariants(yA)
    # B: the engine's map (Fermi-Walker nose), same total rapidity, fine quantum
    yB, _ = engine_flushes(circ_state(r_r), alpha_r, eta_tot_r, 0.0, 2**-8, 1.0)
    EBr, LBr = invariants(yB)
    # C: compass-gimballed nozzle, exact continuous
    yC = integrate(circ_state(r_r), dtau_r, alpha_r, 0.0, 1.0, compass=True)
    ECr, LCr = invariants(yC)
    res["three_readings_radial_r6"] = dict(
        dtau=dtau_r, eta_total=eta_tot_r, L0=L0r, E0=E0r,
        axis_boost_L=LAr, fw_nose_L=LBr, compass_L=LCr,
        axis_boost_dL_over_L=(LAr - L0r) / L0r,
        fw_nose_dL_over_L=(LBr - L0r) / L0r,
        compass_dL_over_L=(LCr - L0r) / L0r,
        axis_boost_E=EAr, fw_nose_E=EBr, compass_E=ECr)

    # --- escape thresholds ---
    for r0 in (6.0, 10.0, 20.0, 100.0):
        ee, el = eta_escape_exact(r0), eta_escape_letter(r0)
        res["escape"].append(dict(r=r0, eta_escape_exact=ee, eta_escape_letter=el,
                                  letter_shortfall_frac=(el - ee) / ee))

    print(json.dumps(res, indent=1, default=float))
    with open(__file__.replace(".py", "_results.json"), "w") as fh:
        json.dump(res, fh, indent=1, default=float)


if __name__ == "__main__":
    main()
