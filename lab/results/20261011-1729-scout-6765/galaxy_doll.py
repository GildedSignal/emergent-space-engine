#!/usr/bin/env python3
"""Galaxy-doll falsifier (scout lens, run 20261011-1729-scout-6765).

Question: does the law's own compiled-cycle mechanism (compile from (E, L) by
turning-point panel quadrature, advance by additions, everything else kicks)
hold the smooth galactic field at the plane's cost and error type, and where
does galactic-scale dynamics even exist at playable horizons?

Units: G = 1, disc circular speed v0 = 1, core rc, galaxy edge Rg.
Potential: Phi(r) = 0.5*v0^2*ln(1+(r/rc)^2)   r <= Rg
           Kepler-matched (C^1) outside: -GMg/r + C, Mg = v0^2*Rg^3/(Rg^2+rc^2).
Optional central nucleus: -Mbh/r added inside r < Rn (smoothed at rnuc for the
force only via a softening epsilon; Phi stays -Mbh/sqrt(r^2+eps^2) so the
potential is finite and smooth at 0).

Modes:
  python3 galaxy_doll.py calibrate   # tuning cases only (A, core control)
  python3 galaxy_doll.py full        # everything, writes galaxy-out.json
"""
import json
import math
import os
import sys
import time

# ---------------------------------------------------------------- potential
V0 = 1.0
RC = 0.05
RG = 8.0
MG = V0 * V0 * RG**3 / (RG * RG + RC * RC)          # enclosed mass at Rg
PHI_RG = 0.5 * V0 * V0 * math.log(1 + (RG / RC) ** 2)
KEP_C = PHI_RG + MG / RG                            # C^1 match at Rg
MBH = 0.0                                           # set per case
EPS_BH = 1e-4                                       # nucleus softening

def phi(r, mbh=MBH):
    if r <= RG:
        p = 0.5 * V0 * V0 * math.log(1.0 + (r / RC) ** 2)
    else:
        p = -MG / r + KEP_C
    if mbh > 0.0:
        p -= mbh / math.sqrt(r * r + EPS_BH * EPS_BH)
    return p

def dphi(r, mbh=MBH):
    if r <= RG:
        d = V0 * V0 * r / (r * r + RC * RC)
    else:
        d = MG / (r * r)
    if mbh > 0.0:
        d += mbh * r / (r * r + EPS_BH * EPS_BH) ** 1.5
    return d

def phi_eff(r, L, mbh=MBH):
    return phi(r, mbh) + 0.5 * L * L / (r * r)

# ---------------------------------------------------------------- quadrature
GL4_X = (-0.8611363115940526, -0.3399810435848563,
         0.3399810435848563, 0.8611363115940526)
GL4_W = (0.34785484513745385, 0.6521451548625461,
         0.6521451548625461, 0.34785484513745385)

def panels_ab(a, b, npan):
    """Yield (x, w) samples of composite 4-pt GL on [a,b] split into npan panels."""
    h = (b - a) / npan
    for i in range(npan):
        x0 = a + i * h
        for xi, wi in zip(GL4_X, GL4_W):
            yield x0 + 0.5 * h * (xi + 1.0), 0.5 * h * wi

def compile_cycle(rp, ra, L, mbh, npan, cuts=()):
    """Radial cycle apo->peri->apo.  r = c + A cos(psi), psi in (0, pi).
    Returns (dphi, dt) for the FULL cycle (mirror-doubled).  Panel edges at
    the psi values where r crosses any radius in `cuts` (band edges)."""
    c = 0.5 * (ra + rp)
    A = 0.5 * (ra - rp)
    E = phi_eff(rp, L, mbh)   # == phi_eff(ra, L, mbh) by construction
    # psi cuts: psi = acos((r_cut - c)/A) for cuts inside (rp, ra)
    psis = [0.0, math.pi]
    for rc_ in cuts:
        s = (rc_ - c) / A
        if -1.0 < s < 1.0:
            psis.append(math.acos(s))
    psis.sort()
    dphi = 0.0
    dt = 0.0
    for a_, b_ in zip(psis[:-1], psis[1:]):
        nloc = max(1, int(round(npan * (b_ - a_) / math.pi)))
        for x, w in panels_ab(a_, b_, nloc):
            r = c + A * math.cos(x)
            s = math.sin(x)
            den = 2.0 * (E - phi(r, mbh)) - L * L / (r * r)
            if den <= 0.0:
                den = 1e-300
            sq = math.sqrt(den)
            dphi += w * (L / (r * r)) * A * s / sq
            dt += w * A * s / sq
    return 2.0 * dphi, 2.0 * dt

def compile_scatter(rp, R0, L, E, mbh, npan):
    """Transit r=R0 (inbound) -> rp -> R0 (outbound).  r = rp + (R0-rp) sin^2(th),
    th in (0, pi/2); endpoint singularity at rp removed by sin(th)."""
    dphi = 0.0
    dt = 0.0
    # cut at Rg if inside
    ths = [0.0, 0.5 * math.pi]
    if rp < RG < R0:
        frac = (RG - rp) / (R0 - rp)
        ths.append(math.asin(math.sqrt(frac)))
    ths.sort()
    for a_, b_ in zip(ths[:-1], ths[1:]):
        nloc = max(1, int(round(npan * (b_ - a_) / (0.5 * math.pi))))
        for x, w in panels_ab(a_, b_, nloc):
            r = rp + (R0 - rp) * math.sin(x) ** 2
            drdth = (R0 - rp) * math.sin(2.0 * x)   # = 2(R0-rp) sin cos
            den = 2.0 * (E - phi(r, mbh)) - L * L / (r * r)
            if den <= 0.0:
                den = 1e-300
            sq = math.sqrt(den)
            dphi += w * (L / (r * r)) * drdth / sq
            dt += w * drdth / sq
    return 2.0 * dphi, 2.0 * dt

# ---------------------------------------------------------------- truth: leapfrog KDK
def accel(x, y, mbh):
    r = math.hypot(x, y)
    a = -dphi(r, mbh)
    return a * x / r, a * y / r

def leapfrog_orbit(rp, ra, L, mbh, ncycles, steps_per_cycle, phi0=0.0):
    """Start at apoapsis, tangential velocity; integrate ncycles radial cycles."""
    E = phi_eff(rp, L, mbh)
    r = ra
    x, y = ra * math.cos(phi0), ra * math.sin(phi0)
    vt = L / ra
    vx, vy = -vt * math.sin(phi0), vt * math.cos(phi0)
    # period estimate from a first coarse compile
    _, T = compile_cycle(rp, ra, L, mbh, 64)
    dt = T / steps_per_cycle
    ax, ay = accel(x, y, mbh)
    t = 0.0
    n_steps = int(ncycles * steps_per_cycle)
    for _ in range(n_steps):
        vx += 0.5 * dt * ax
        vy += 0.5 * dt * ay
        x += dt * vx
        y += dt * vy
        ax, ay = accel(x, y, mbh)
        vx += 0.5 * dt * ax
        vy += 0.5 * dt * ay
        t += dt
    return x, y, vx, vy, t

def leapfrog_transit(b, vinf, mbh, nsteps, R0):
    """Start at r~R0 inbound with speed vinf, impact parameter b; run to r>R0 outbound."""
    x = -math.sqrt(max(R0 * R0 - b * b, 1e-12))
    y = b
    vx, vy = vinf, 0.0
    E = 0.5 * vinf * vinf + phi(R0, mbh)
    # time scale: crossing time ~ 2 R0 / vinf
    dt = (2.0 * R0 / vinf) / nsteps
    ax, ay = accel(x, y, mbh)
    t = 0.0
    for _ in range(10 * nsteps):
        vx += 0.5 * dt * ax
        vy += 0.5 * dt * ay
        x += dt * vx
        y += dt * vy
        ax, ay = accel(x, y, mbh)
        vx += 0.5 * dt * ax
        vy += 0.5 * dt * ay
        t += dt
        r = math.hypot(x, y)
        if r > R0 and x > 0:
            break
    return x, y, vx, vy, t

# ---------------------------------------------------------------- turning points
def orbit_from_rp_ra(rp, ra, mbh):
    L2 = 2.0 * (phi(ra, mbh) - phi(rp, mbh)) / (1.0 / (rp * rp) - 1.0 / (ra * ra))
    L = math.sqrt(L2)
    E = phi_eff(rp, L, mbh)
    return E, L

def scatter_rp(b, vinf, mbh, R0):
    """periapsis of the transit by bisection on dPhi_eff."""
    E = 0.5 * vinf * vinf + phi(R0, mbh)
    L = b * vinf
    def g(r):
        return 2.0 * (E - phi(r, mbh)) - L * L / (r * r)
    lo, hi = 1e-6, R0
    if g(hi) < 0.0:
        return None, E, L   # no turning point inside R0
    while hi - lo > 1e-14 * hi:
        mid = 0.5 * (lo + hi)
        if g(mid) > 0.0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi), E, L

# ---------------------------------------------------------------- experiments
def err_vs_panels(rp, ra, mbh, label, cuts):
    E, L = orbit_from_rp_ra(rp, ra, mbh)
    ref = compile_cycle(rp, ra, L, mbh, 512, cuts)
    rows = {}
    for P in (2, 4, 8, 16, 32, 64):
        d, t = compile_cycle(rp, ra, L, mbh, P, cuts)
        rows[P] = {
            "dphi": d, "dt": t,
            "err_dphi": abs(d - ref[0]) / ref[0],
            "err_dt": abs(t - ref[1]) / ref[1],
        }
    return {"label": label, "rp": rp, "ra": ra, "mbh": mbh, "E": E, "L": L,
            "dphi_ref": ref[0], "dt_ref": ref[1], "panels": rows}

def case_mpiratio(rp, ra, mbh, label, cuts):
    """Ratio of apoapsis to periapsis motion: check analytic controls."""
    E, L = orbit_from_rp_ra(rp, ra, mbh)
    d, t = compile_cycle(rp, ra, L, mbh, 256, cuts)
    return {"label": label, "dphi": d, "dt": t, "dphi_over_pi": d / math.pi}

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    out = {"mode": mode, "loadavg_start": open("/proc/loadavg").read().split()[:3]}
    cuts_rg = (RG,)   # band edge at the galaxy edge

    if mode == "calibrate":
        # tuning case A (mid-disc rosette) and the harmonic-core control
        A = err_vs_panels(1.0, 2.0, 0.0, "A_mid_disc_calib", ())
        core = case_mpiratio(0.005, 0.02, 0.0, "core_harmonic", ())
        flat = case_mpiratio(1.0, 2.0, 0.0, "A_mid_flat", ())
        out["calibrate"] = {"A": A, "core": core, "flat": flat}
        print(json.dumps(out, indent=1))
        return

    # ---------------- E1/E2: held-out rosettes, error vs panels
    cases = [
        (0.4, 3.0, 0.0, "B_eccentric", ()),
        (5.0, 11.0, 0.0, "D_outer_crossing_Rg", cuts_rg),
        (5.0, 11.0, 0.0, "D_outer_nocut_negative", ()),
        (0.02, 0.5, 0.05, "E_nucleus_mixed", ()),
        (0.0006, 0.0024, 0.0, "C_core_harmonic_control", ()),
        (1.0, 2.0, 0.0, "A_mid_flat_calib", ()),
    ]
    out["rosettes"] = [err_vs_panels(*c) for c in cases]

    # analytic controls: harmonic core -> dphi = pi;  mid-flat -> sqrt(2)*pi
    out["controls"] = {
        "harmonic_core_dphi_pi": out["rosettes"][4]["dphi_ref"] / math.pi,
        "mid_flat_dphi_sqrtpi": out["rosettes"][5]["dphi_ref"] / (math.sqrt(2) * math.pi),
    }

    # ---------------- E2b: cost per compile (order of magnitude, cloud x86)
    E, L = orbit_from_rp_ra(0.4, 3.0, 0.0)
    t0 = time.perf_counter()
    NREP = 200
    for _ in range(NREP):
        compile_cycle(0.4, 3.0, L, 0.0, 32)
    out["compile_cost_us_32pan"] = (time.perf_counter() - t0) / NREP * 1e6

    # ---------------- E-advance: linear error accumulation, 10^4 cycles
    E, L = orbit_from_rp_ra(0.4, 3.0, 0.0)
    d32, t32 = compile_cycle(0.4, 3.0, L, 0.0, 32)
    dref, tref = compile_cycle(0.4, 3.0, L, 0.0, 512)
    err1 = d32 - dref
    NCYC = 10000
    phiN_direct = NCYC * d32
    phiN_seq = 0.0
    for _ in range(NCYC):
        phiN_seq += d32       # pure additions, the tube's advance
    out["advance"] = {
        "err_per_cycle_rad": err1,
        "err_1e4_cycles_rad": NCYC * err1,
        "linear_residual": abs(phiN_seq - phiN_direct),
        "rekey_cycles_for_1e-4rad": (1e-4 / abs(err1)) if err1 != 0 else None,
    }

    # ---------------- independent truth: leapfrog on case B
    E, L = orbit_from_rp_ra(0.4, 3.0, 0.0)
    x, y, vx, vy, t = leapfrog_orbit(0.4, 3.0, L, 0.0, 30, 4000)
    x2, y2, vx2, vy2, t2 = leapfrog_orbit(0.4, 3.0, L, 0.0, 30, 8000)
    # phase after 30 cycles: compare against compiled advance
    # leapfrog 30 cycles ~ 30*T; compiled: 30*dphi.  Compare swept angle & time.
    def swept(x, y):
        return math.atan2(y, x)
    out["leapfrog_truth_B"] = {
        "swept_4000": swept(x, y), "swept_8000": swept(x2, y2),
        "t_4000": t, "t_8000": t2,
        "compiled_30cyc_dphi": 30 * dref, "compiled_30cyc_t": 30 * tref,
        "lf_dt_conv_swept": abs(swept(x, y) - swept(x2, y2)),
        "lf_dt_conv_t": abs(t - t2),
    }

    # ---------------- E5: scatter transits (fast coasts)
    R0 = 60.0
    scat = []
    for b, vinf, cname in ((0.5, 9.0, "beta0p9_b0.5"), (2.0, 9.0, "beta0p9_b2.0"),
                           (0.5, 3.0, "beta0p3_b0.5"), (0.05, 1.0, "slow_b0.05")):
        rp, E, Lm = scatter_rp(b, vinf, 0.0, R0)
        Ls = -b * vinf                      # physical (clockwise) angular momentum
        d, tt = compile_scatter(rp, R0, Ls, E, 0.0, 64)   # d is signed (<0)
        xf, yf, vxf, vyf, tlf = leapfrog_transit(b, vinf, 0.0, 40000, R0)
        xf2, yf2, vxf2, vyf2, tlf2 = leapfrog_transit(b, vinf, 0.0, 80000, R0)
        defl_lf = math.atan2(vyf, vxf)      # initial velocity azimuth is 0 (+x)
        defl_lf2 = math.atan2(vyf2, vxf2)
        phi0 = math.atan2(b, -math.sqrt(R0 * R0 - b * b))
        phif = phi0 + d                     # signed sweep
        # position-angle check (no velocity reconstruction): leapfrog end azimuth
        pos_ang_lf = math.atan2(yf, xf)
        pos_err = math.atan2(math.sin(pos_ang_lf - phif), math.cos(pos_ang_lf - phif))
        vr_out = math.sqrt(max(2.0 * (E - phi(R0, 0.0)) - Ls * Ls / (R0 * R0), 0.0))
        vphi_out = Ls / R0
        alpha = math.atan2(vphi_out, vr_out)
        defl_comp = phif + alpha            # final velocity azimuth; initial is 0
        defl_comp = math.atan2(math.sin(defl_comp), math.cos(defl_comp))
        scat.append({
            "case": cname, "b": b, "vinf": vinf, "rp": rp,
            "compiled_dphi_swept": d, "compiled_dt": tt,
            "leapfrog_dt": tlf, "leapfrog_dt_half": tlf2,
            "deflection_compiled": defl_comp, "deflection_leapfrog": defl_lf,
            "deflection_err": abs(defl_comp - defl_lf),
            "position_angle_err": abs(pos_err),
            "lf_dt_conv_defl": abs(defl_lf - defl_lf2),
            "t_err_rel": abs(tt - tlf) / tt,
        })
    out["scatter"] = scat

    # ---------------- E3: GR seam arithmetic (physical anchors)
    G_SI = 6.674e-11
    C_SI = 2.998e8
    MSUN = 1.989e30
    PC = 3.086e16
    def seam(Mbh_kg, v0_ms, horizon_s, theta_rad):
        # accumulated GR apse drift N(r)*6pi*rs/p >= theta, Kepler T(r), p~r
        rs = 2 * G_SI * Mbh_kg / C_SI**2
        def acc(r):
            T = 2 * math.pi * math.sqrt(r**3 / (G_SI * Mbh_kg))
            N = horizon_s / T
            return N * 6 * math.pi * rs / r
        lo, hi = 10 * rs, 1e6 * rs
        if acc(lo) < theta_rad:
            return 0.0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if acc(mid) > theta_rad:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)
    seams = []
    for name, Mbh_msun, v0_kms in (("SgrA_like", 4e6, 220.0), ("game_nucleus_1e8", 1e8, 220.0)):
        Mbh = Mbh_msun * MSUN
        v0 = v0_kms * 1e3
        r_soi = G_SI * Mbh / v0**2
        row = {"name": name, "M_msun": Mbh_msun, "r_soi_pc": r_soi / PC,
               "r_soi_rs": r_soi / (2 * G_SI * Mbh / C_SI**2)}
        for H in (1e5, 1e7, 1e9, 1e11):
            row[f"seam_H{H:.0e}_th1e-3_rs"] = seam(Mbh, v0, H, 1e-3) / (2 * G_SI * Mbh / C_SI**2)
        seams.append(row)
    out["gr_seam"] = seams

    # ---------------- disc-frozen arithmetic
    Tdisc_s = 2 * math.pi * (8e3 * PC) / (220e3)      # 8 kpc, 220 km/s
    frozen = []
    for rtf in (1e2, 1e4, 1e6, 1e8):
        game_s = 100 * 3600 * rtf                     # 100 h session
        frozen.append({"rtf": rtf, "game_years": game_s / 3.156e7,
                       "disc_orbits_per_session": game_s / Tdisc_s})
    out["disc_frozen"] = {"T_disc_years": Tdisc_s / 3.156e7, "rows": frozen}

    # ---------------- resonance radii from compiled epicyclic ratio
    res = []
    for r0 in (0.5, 1.0, 2.0, 3.0, 4.0):
        E, L = orbit_from_rp_ra(0.99 * r0, 1.01 * r0, 0.0)
        d, t = compile_cycle(0.99 * r0, 1.01 * r0, L, 0.0, 256)
        Om = math.sqrt(dphi(r0, 0.0) / r0)            # v_c/r
        kap = 2 * math.pi * Om / d                    # dphi = 2 pi Om/kap
        res.append({"r": r0, "Omega": Om, "kappa": kap, "kap_over_om": kap / Om,
                    "dphi_near_circ_over_pi": d / math.pi})
    out["epicyclic"] = res

    out["loadavg_end"] = open("/proc/loadavg").read().split()[:3]
    with open("galaxy-out.json", "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
