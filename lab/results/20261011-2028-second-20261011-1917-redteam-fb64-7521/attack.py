#!/usr/bin/env python3
"""
Red-team 20261011-1917-fb64 — premise attack #5 (the view gathered at the past
light cone), as ordered by the lens (docs/lenses/redteam.md item 5).

PREMISE UNDER ATTACK (docs/representation.md §2, docs/law.md §Observation):
  "Positions are gathered at the observer's past light cone. Lensing takes
   deflection(b) from the doll's memo."
  + "Each visible tube crosses the observer's past light cone once; Newton's
     method finds the crossing, starting from the previous frame's."
The causal envelope is the flat c=1 min-plus lattice cone; the memo bends the
arrival DIRECTION. Nothing delays the arrival TIME (Shapiro). If the retarded
time is wrong by dt, a body moving at angular rate Omega is rendered at the
wrong phase: apparent-position error ~ Omega * dt.

ORACLE: exact equatorial Schwarzschild null geodesics (RK4 on the photon Binet
equation u'' + u = 3 M u^2), source on an exact circular geodesic
(Omega = sqrt(M/r^3)), static observer. Units M = 1, c = 1. All in float:
floats explore, they do not decide canonical outcomes (lab rule); this probe
only decides whether a premise is false.

VARIANTS (apparent sky direction at the observer, local static frame):
  design    as written: flat-cone retarded time t_e_flat + infinity deflection
            memo delta_inf(b) applied to the flat chord.
  phase     pure timing error: |angle(chord(t_e_flat), chord(t_e_true))|
            (equivalent to a design with a perfect bend memo).
  fix       delay-corrected crossing: solve t_obs - t_e = D_flat(t_e) + delay(b)
            with delay(b) the memoized geodesic delay (exact, from the table).
  nodefl    NEGATIVE: flat time, no bend at all.
  noretard  NEGATIVE: current position (no retardation) + delta_inf bend.

Also measures (lens item 5, second half): warm Newton convergence on the flat
cone for the orbit scenes and for uniform closing bodies up to beta = 0.999.

Modes:
  python3 attack.py calibrate   # weak-field scene r_e = 1e4 (conventions/tuning)
  python3 attack.py sweep       # held-out scenes r_e = 6..1000 (the decisive run)
  python3 attack.py newton      # uniform-body warm-Newton survivor test
Output: results-<mode>.json + stdout table.
"""
import json
import sys

import numpy as np

M = 1.0
TWO_PI = 2.0 * np.pi


# ----------------------------------------------------------------------------
# Photon tables. Rotational symmetry: the swept angle dphi and travel time dt
# from r_e to r_o depend only on (r_e, r_o, b) and the branch. Launch angle
# alpha is the local static-frame angle from the outward radial direction.
# ----------------------------------------------------------------------------

def photon_table(r_e, r_o, n_alpha=2000, dphi=3e-3, phi_max=14.0):
    """Integrate photons launched at r_e over alpha in (0, pi) (prograde
    tangential) until the first OUTBOUND crossing of r_o. Returns dict with
    per-alpha arrays; alpha = pi/2 splits the outward/inward launch families.
    """
    alpha = np.linspace(0.02, np.pi - 0.02, n_alpha)
    u_e, u_o = 1.0 / r_e, 1.0 / r_o
    b = r_e * np.sin(alpha) / np.sqrt(1.0 - 2.0 * M * u_e)
    disc0 = 1.0 / b**2 - u_e**2 + 2.0 * M * u_e**3
    u = np.full(n_alpha, u_e)
    # outward launch (alpha < pi/2): r grows => du/dphi < 0
    w = np.where(alpha < np.pi / 2, -np.sqrt(np.maximum(disc0, 0.0)),
                 np.sqrt(np.maximum(disc0, 0.0)))
    T = np.zeros(n_alpha)
    PHI = np.zeros(n_alpha)
    arrived = np.zeros(n_alpha, bool)
    A_phi = np.full(n_alpha, np.nan)
    A_t = np.full(n_alpha, np.nan)
    A_u = np.full(n_alpha, np.nan)
    A_w = np.full(n_alpha, np.nan)

    nsteps = int(phi_max / dphi)
    for _ in range(nsteps):
        live = ~arrived & (u < 0.5 - 1e-12) & (u > 0.0) & np.isfinite(u)
        if not live.any():
            break
        idx = np.nonzero(live)[0]  # integrate live columns only
        u0, w0, T0 = u[idx], w[idx], T[idx]
        bL = b[idx]

        def dL(u_, w_):
            den = bL * u_ * u_ * (1.0 - 2.0 * M * u_)
            den = np.where(np.abs(den) < 1e-300, 1e-300, den)
            return w_, 3.0 * u_ * u_ - u_, 1.0 / den

        k1u, k1w, k1t = dL(u0, w0)
        k2u, k2w, k2t = dL(u0 + 0.5 * dphi * k1u, w0 + 0.5 * dphi * k1w)
        k3u, k3w, k3t = dL(u0 + 0.5 * dphi * k2u, w0 + 0.5 * dphi * k2w)
        k4u, k4w, k4t = dL(u0 + dphi * k3u, w0 + dphi * k3w)
        uN = u0 + dphi / 6.0 * (k1u + 2 * k2u + 2 * k3u + k4u)
        wN = w0 + dphi / 6.0 * (k1w + 2 * k2w + 2 * k3w + k4w)
        tN = T0 + dphi / 6.0 * (k1t + 2 * k2t + 2 * k3t + k4t)
        u[idx], w[idx], T[idx] = uN, wN, tN
        PHI[live] += dphi
        crossL = (uN <= u_o) & (wN < 0.0)
        if crossL.any():
            f = (u0 - u_o) / np.where(u0 - uN != 0, u0 - uN, 1e-300)
            f = np.clip(f, 0.0, 1.0)
            cols = idx[crossL]
            A_phi[cols] = (PHI[cols] - dphi) + f[crossL] * dphi
            A_t[cols] = T0[crossL] + f[crossL] * (tN[crossL] - T0[crossL])
            A_u[cols] = u_o
            A_w[cols] = w0[crossL] + f[crossL] * (wN[crossL] - w0[crossL])
            arrived[cols] = True

    # conserved-quantity check AT ARRIVAL: w^2 + u^2 - 2u^3 == 1/b^2
    ok = arrived & np.isfinite(A_t)
    drift = np.abs((A_w[ok] ** 2 + A_u[ok] ** 2 - 2.0 * A_u[ok] ** 3)
                   * b[ok] ** 2 - 1.0)
    out = np.pi / 2
    return {
        "alpha": alpha, "b": b, "arrived": arrived, "A_phi": A_phi,
        "A_t": A_t, "b_drift_max": float(np.max(drift)) if ok.any() else np.nan,
        "out_mask": alpha < out, "in_mask": alpha > out,
    }


def delta_inf_table(b_grid, dphi=2e-3, u_start=1e-6):
    """Exact from-infinity-to-infinity deflection delta(b) = Phi_tot - pi,
    integrated on u'' + u = 3 M u^2 (both sides of the turning point)."""
    nb = len(b_grid)
    u = np.full(nb, u_start)
    w = np.sqrt(np.maximum(1.0 / b_grid**2 - u**2 + 2.0 * M * u**3, 0.0))
    PHI = np.zeros(nb)
    done = np.zeros(nb, bool)
    PHI_end = np.full(nb, np.nan)

    def dw(u_):
        return 3.0 * u_ * u_ - u_

    for _ in range(int(80.0 / dphi)):
        active = ~done & (u < 0.5 - 1e-12)
        if not active.any():
            break
        u0, w0, P0 = u, w, PHI
        k1u, k1w = w0, dw(u0)
        k2u, k2w = w0 + 0.5 * dphi * k1w, dw(u0 + 0.5 * dphi * k1u)
        k3u, k3w = w0 + 0.5 * dphi * k2w, dw(u0 + 0.5 * dphi * k2u)
        k4u, k4w = w0 + dphi * k3w, dw(u0 + dphi * k3u)
        u = u0 + dphi / 6.0 * (k1u + 2 * k2u + 2 * k3u + k4u)
        w = w0 + dphi / 6.0 * (k1w + 2 * k2w + 2 * k3w + k4w)
        PHI = P0 + dphi
        cross = active & (u <= u_start) & (w < 0.0)
        if cross.any():
            f = (u0 - u_start) / np.where(u0 - u != 0, u0 - u, 1e-300)
            f = np.clip(f, 0.0, 1.0)
            PHI_end[cross] = P0[cross] + f[cross] * dphi
            done[cross] = True
        plunge = active & (u >= 0.5)
        if plunge.any():
            done[plunge] = True  # no deflection: captured
    return PHI_end - np.pi + 2.0 * np.arcsin(np.clip(b_grid * u_start, 0, 1))
    # (the finite-u_start correction: a straight line from r=1/u_start sweeps
    # pi - 2*arcsin(b*u_start), not pi)
# ----------------------------------------------------------------------------
# Scene geometry and solvers.
# ----------------------------------------------------------------------------

def body_pos(phi0, omega, t, r_e):
    ph = phi0 + omega * t
    return np.array([r_e * np.cos(ph), r_e * np.sin(ph)]), ph


def flat_newton(phi0, omega, r_e, x_o, t_obs, seed):
    """The design's crossing solve: Newton on G(t_e) = t_obs - t_e - D_flat(t_e).
    Warm start from the previous frame's root (or the cold lag guess)."""

    def G(te):
        xb, _ = body_pos(phi0, omega, te, r_e)
        d = xb - x_o
        D = np.linalg.norm(d)
        return t_obs - te - D, d / max(D, 1e-300)

    def Gp(te):
        xb, ph = body_pos(phi0, omega, te, r_e)
        v = omega * r_e * np.array([-np.sin(ph), np.cos(ph)])
        d = xb - x_o
        D = np.linalg.norm(d)
        uhat = d / max(D, 1e-300)
        return -1.0 - float(uhat @ v)

    te = seed
    it = 0
    for it in range(1, 65):
        g, _ = G(te)
        if abs(g) < 1e-12 * max(1.0, abs(t_obs)):
            return te, it, True
        gp = Gp(te)
        if not np.isfinite(gp) or abs(gp) < 1e-14:
            return te, it, False
        step = g / gp
        if abs(step) > 1e6:
            return te, it, False
        te = te - step
        if te >= t_obs:
            te = t_obs - 1e-9  # clamp into the past cone; keep iterating
    g, _ = G(te)
    return te, it, abs(g) < 1e-9 * max(1.0, abs(t_obs))


def chord(phi0, omega, r_e, x_o, t_e):
    xb, _ = body_pos(phi0, omega, t_e, r_e)
    d = xb - x_o
    n = np.linalg.norm(d)
    return d / max(n, 1e-300), xb, n


def rot(v, ang):
    c, s = np.cos(ang), np.sin(ang)
    return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1]])


def ang_between(a, b):
    cr = a[0] * b[1] - a[1] * b[0]
    dt = max(-1.0, min(1.0, float(a @ b)))
    return abs(np.arctan2(cr, dt))


def signed_angle(a, b):
    cr = a[0] * b[1] - a[1] * b[0]
    dt = max(-1.0, min(1.0, float(a @ b)))
    return np.arctan2(cr, dt)


def scene_frames(r_e, r_o, table, dinf_b, dinf_v, n_frames=16, phi0=1.0):
    """Solve one scene over n_frames observation times spanning one orbit.
    Returns per-frame records."""
    omega = np.sqrt(M / r_e**3)
    period = TWO_PI / omega
    x_o = np.array([r_o, 0.0])
    recs = []
    seed = None
    for j in range(n_frames):
        t_obs = 0.35 * period + j * period / n_frames
        # --- design's flat-cone solve (warm Newton) ---
        if seed is None:
            xb, _ = body_pos(phi0, omega, t_obs, r_e)
            seed = t_obs - np.linalg.norm(xb - x_o)
        te_flat, iters, ok = flat_newton(phi0, omega, r_e, x_o, t_obs, seed)
        seed = te_flat
        d_flat, xb_flat, D_flat = chord(phi0, omega, r_e, x_o, te_flat)
        # impact parameter of the flat chord w.r.t. the hole
        b_flat = abs(x_o[0] * d_flat[1] - x_o[1] * d_flat[0])

        # --- true roots: scan (sigma, branch, winding k) ---
        roots = []
        for sigma in (+1.0, -1.0):
            for branch, mask in (("out", table["out_mask"]),
                                 ("in", table["in_mask"])):
                sel = mask & table["arrived"]
                if not sel.any():
                    continue
                a_g = table["alpha"][sel]
                b_g = table["b"][sel]
                ph_g = sigma * table["A_phi"][sel]
                t_g = table["A_t"][sel]
                # H(alpha) = phi0 + omega*(t_obs - dt) + sigma*dphi  (mod 2pi)
                H = phi0 + omega * (t_obs - t_g) + ph_g
                kmin = int(np.floor((H.min() - 1e-9) / TWO_PI))
                kmax = int(np.ceil((H.max() + 1e-9) / TWO_PI))
                for k in range(kmin, kmax + 1):
                    Hk = H - TWO_PI * k
                    s = np.sign(Hk)
                    idx = np.nonzero(np.diff(s) != 0)[0]
                    for i0 in idx:
                        a0, a1 = a_g[i0], a_g[i0 + 1]
                        for _ in range(60):  # bisection on piecewise-linear H
                            am = 0.5 * (a0 + a1)
                            Hm = (np.interp(am, a_g, H) - TWO_PI * k)
                            if np.sign(Hm) == np.sign(Hk[i0]):
                                a0 = am
                            else:
                                a1 = am
                        astar = 0.5 * (a0 + a1)
                        roots.append({
                            "sigma": sigma, "alpha": astar, "branch": branch,
                            "b": float(np.interp(astar, a_g, b_g)),
                            "dphi": float(sigma * np.interp(astar, a_g, ph_g)),
                            "dt": float(np.interp(astar, a_g, t_g)),
                        })
        if not roots:
            recs.append({"t_obs": t_obs, "roots": 0, "newton_fail": not ok,
                         "newton_iters": iters})
            continue
        # primary image: the root whose b is closest to the flat chord's b
        roots.sort(key=lambda R: abs(R["b"] - b_flat))
        R = roots[0]
        te_true = t_obs - R["dt"]
        d_true, xb_true, D_true_chord = chord(phi0, omega, r_e, x_o, te_true)
        delay = (t_obs - te_true) - D_true_chord  # Shapiro delay at the root

        # oracle apparent direction (local static frame at the observer,
        # phi_o = 0 => e_r = x, e_phi = y); arrival is outbound + sigma sense
        u_o = 1.0 / r_o
        sin_ao = R["b"] * u_o * np.sqrt(1.0 - 2.0 * M * u_o)
        sin_ao = min(1.0, abs(sin_ao))
        ao = np.arcsin(sin_ao)
        v_arr = np.array([np.cos(ao), R["sigma"] * np.sin(ao)])
        apparent_oracle = -v_arr

        # perfect bend of the true path (memo-free by construction)
        bend_true = signed_angle(d_true, apparent_oracle)

        # design as written: flat-cone retarded time + the doll's deflection
        # memo. The memo is the exact finite-path bend of the arrival family
        # (what a per-doll table compiled from light tubes would hold).
        bend_memo = bend_lookup(b_flat, table, R["sigma"], R["branch"],
                                r_e, r_o)
        design_dir = rot(d_flat, bend_memo)
        dinf = float(np.interp(b_flat, dinf_b, dinf_v))

        # pure timing error (perfect bend applied to both)
        err_phase = ang_between(d_flat, d_true)

        # delay-corrected crossing: t_obs - t_e = D_flat(t_e) + delay(b(t_e))
        te_fix = te_flat
        for _ in range(50):
            dtmp, _, Dtmp = chord(phi0, omega, r_e, x_o, te_fix)
            btmp = abs(x_o[0] * dtmp[1] - x_o[1] * dtmp[0])
            # delay memo on the primary root's arrival family: delay(b) =
            # geodesic travel time minus its own flat chord (per-doll table)
            dly = delay_lookup(btmp, table, R["sigma"], R["branch"], r_e, r_o)
            te_new = t_obs - Dtmp - dly
            if abs(te_new - te_fix) < 1e-13 * max(1.0, abs(t_obs)):
                te_fix = te_new
                break
            te_fix = te_new
        d_fix, _, _ = chord(phi0, omega, r_e, x_o, te_fix)
        err_fix = ang_between(d_fix, d_true)

        # negatives: no bend at all; no retardation (perfect memo kept)
        err_nodefl = ang_between(d_flat, apparent_oracle)
        d_now, _, _ = chord(phi0, omega, r_e, x_o, t_obs)
        noret_dir = rot(d_now, bend_memo)
        err_noretard = ang_between(noret_dir, apparent_oracle)

        err_design = ang_between(design_dir, apparent_oracle)

        recs.append({
            "t_obs": t_obs, "roots": len(roots), "b_flat": b_flat,
            "b_true": R["b"], "sigma_primary": R["sigma"],
            "newton_iters": iters, "newton_fail": not ok,
            "delay_M": delay, "travel_M": t_obs - te_true,
            "err_design": err_design, "err_phase": err_phase,
            "err_fix": err_fix, "err_nodefl": err_nodefl,
            "err_noretard": err_noretard, "dinf": dinf, "bend_true": bend_true,
            "te_flat": te_flat, "te_true": te_true, "te_fix": te_fix,
        })
    return recs


def delay_lookup(b_query, table, sigma, branch, r_e, r_o):
    """Per-doll delay memo on one arrival family: delay(b) = geodesic travel
    time dt(b) minus the flat chord length of the same swept angle."""
    mask = table["out_mask"] if branch == "out" else table["in_mask"]
    sel = mask & table["arrived"]
    if not sel.any():
        return 0.0
    b_g = table["b"][sel]
    t_g = table["A_t"][sel]
    ph_g = table["A_phi"][sel]  # >= 0, swept angle (sigma only mirrors)
    # emission point at angle -sigma*dphi from the observer (phi_o = 0)
    xe = r_e * np.cos(-sigma * ph_g)
    ye = r_e * np.sin(-sigma * ph_g)
    D = np.hypot(xe - r_o, ye)
    dly = t_g - D
    order = np.argsort(b_g)
    b_s, d_s = b_g[order], dly[order]
    keep = np.concatenate([[True], np.diff(b_s) > 0])
    b_s, d_s = b_s[keep], d_s[keep]
    if len(b_s) < 2:
        return 0.0
    return float(np.interp(b_query, b_s, d_s))


def bend_lookup(b_query, table, sigma, branch, r_e, r_o):
    """Per-doll deflection memo on one arrival family: bend(b) = signed angle
    from the family's flat chord to its true arrival direction. This is the
    most generous reading of 'deflection(b) from the doll's memo': a table the
    doll could compile exactly from its light tubes."""
    mask = table["out_mask"] if branch == "out" else table["in_mask"]
    sel = mask & table["arrived"]
    if not sel.any():
        return 0.0
    b_g = table["b"][sel]
    a_g = table["alpha"][sel]
    ph_g = table["A_phi"][sel]  # >= 0 swept angle
    # arrival local angle alpha_o(b): sin(a_o) = b u_o sqrt(1 - 2 M u_o)
    u_o = 1.0 / r_o
    sin_ao = np.clip(b_g * u_o * np.sqrt(1.0 - 2.0 * M * u_o), 0.0, 1.0)
    ao = np.arcsin(sin_ao)
    # flat chord direction at the observer (phi_o = 0, e_r = x, e_phi = y):
    # from observer to the emission point at angle -sigma*dphi
    xe = r_e * np.cos(-sigma * ph_g)
    ye = r_e * np.sin(-sigma * ph_g)
    chord = np.stack([xe - r_o, ye])
    chord = chord / np.linalg.norm(chord, axis=0)
    v_arr = np.stack([np.cos(ao), sigma * np.sin(ao)])
    apparent = -v_arr
    cr = chord[0] * apparent[1] - chord[1] * apparent[0]
    dt = np.clip(chord[0] * apparent[0] + chord[1] * apparent[1], -1.0, 1.0)
    bend = np.arctan2(cr, dt)
    order = np.argsort(b_g)
    b_s, bend_s = b_g[order], bend[order]
    keep = np.concatenate([[True], np.diff(b_s) > 0])
    b_s, bend_s = b_s[keep], bend_s[keep]
    if len(b_s) < 2:
        return 0.0
    return float(np.interp(b_query, b_s, bend_s))


def run_scenes(r_e_list, tag):
    dinf_b = np.geomspace(5.35, 5e4, 800)
    dinf_v = delta_inf_table(dinf_b)
    results = {"tag": tag, "M": M, "scenes": []}
    for r_e in r_e_list:
        r_o = 4.0 * r_e
        table = photon_table(r_e, r_o)
        recs = scene_frames(r_e, r_o, table, dinf_b, dinf_v)
        good = [r for r in recs if r.get("roots", 0) > 0]
        def med(k):
            return float(np.median([r[k] for r in good])) if good else None
        def mx(k):
            return float(np.max([r[k] for r in good])) if good else None
        sc = {
            "r_e": r_e, "r_o": r_o, "n_frames": len(recs),
            "frames_with_roots": len(good),
            "b_drift_max": table["b_drift_max"],
            "images_med": med("roots"), "images_max": mx("roots"),
            "delay_M_med": med("delay_M"), "travel_M_med": med("travel_M"),
            "err_design_med": med("err_design"), "err_design_max": mx("err_design"),
            "err_phase_med": med("err_phase"), "err_phase_max": mx("err_phase"),
            "err_fix_med": med("err_fix"), "err_fix_max": mx("err_fix"),
            "err_nodefl_med": med("err_nodefl"),
            "err_noretard_med": med("err_noretard"),
            "dinf_med": med("dinf"), "bend_true_med": med("bend_true"),
            "newton_iters_max": max((r.get("newton_iters", 0) for r in recs),
                                    default=0),
            "newton_fails": sum(1 for r in recs if r.get("newton_fail")),
            "frames": [{k: r.get(k) for k in
                        ("t_obs", "roots", "b_flat", "delay_M", "err_design",
                         "err_phase", "err_fix", "err_nodefl", "err_noretard",
                         "dinf", "newton_iters")}
                       for r in recs],
        }
        results["scenes"].append(sc)
        print(f"r_e={r_e:9.1f}  images med/max {sc['images_med']:.0f}/"
              f"{sc['images_max']:.0f}  delay {sc['delay_M_med']:.2f}M  "
              f"err_design {sc['err_design_med']:.2e}  err_phase "
              f"{sc['err_phase_med']:.2e}  err_fix {sc['err_fix_med']:.2e}  "
              f"nodefl {sc['err_nodefl_med']:.2e}  noretard "
              f"{sc['err_noretard_med']:.2e}  newton_max "
              f"{sc['newton_iters_max']} fails {sc['newton_fails']}")
    return results


# ----------------------------------------------------------------------------
# Survivor test: warm Newton on the flat cone for uniform closing bodies.
# ----------------------------------------------------------------------------

def newton_uniform():
    """Warm Newton on the flat cone for uniform closing bodies (the design's
    gather, item 5 second half). Correct derivative G' = -1 - u.v."""
    def run(beta, b_imp, deriv_sign=-1.0, frozen=False, label=None):
        x0 = np.array([10.0, b_imp])
        v = np.array([-beta, 0.0])
        dt = 1.0 / 60.0
        seed = None
        iters, fails = [], 0
        for k in range(1, 400):
            t_obs = k * dt
            if (x0 + v * t_obs)[0] < -12.0:
                break

            def G(te, t_obs=t_obs):
                d = x0 + v * te
                D = np.linalg.norm(d)
                return t_obs - te - D, d / D

            if seed is None:
                seed = t_obs - np.linalg.norm(x0 + v * t_obs)
            te, it, ok = seed, 0, False
            for it in range(1, 65):
                g, uhat = G(te)
                if abs(g) < 1e-12:
                    ok = True
                    break
                gp = -1.0 - float(uhat @ v) if deriv_sign < 0 else \
                    -1.0 + float(uhat @ v)
                if abs(gp) < 1e-14 or not np.isfinite(gp):
                    break
                te -= g / gp
                if not (t_obs - 1e4 < te < t_obs):
                    te = min(max(te, t_obs - 1e4), t_obs - 1e-12)
            if not ok:
                fails += 1
            iters.append(it)
            if not frozen:
                seed = te
        return {"beta": beta, "b_imp": b_imp, "frames": len(iters),
                "fails": fails, "iters_mean": float(np.mean(iters)),
                "iters_max": int(np.max(iters)), "note": label}

    out = []
    for beta in (0.1, 0.5, 0.9, 0.99, 0.999):
        for b_imp in (0.05, 0.5, 5.0):
            out.append(run(beta, b_imp))
    # negative controls at beta = 0.999: (a) planted wrong-derivative Newton
    # (the bug this run's own controls caught), (b) frozen seed
    out.append(run(0.999, 0.5, deriv_sign=+1.0,
                   label="negative control: wrong-derivative Newton"))
    out.append(run(0.999, 0.5, frozen=True,
                   label="negative control: frozen seed"))
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "sweep"
    if mode == "calibrate":
        res = run_scenes([1e4], "calibrate")
    elif mode == "sweep":
        res = run_scenes([6.0, 8.0, 20.0, 60.0, 200.0, 1000.0], "sweep")
    elif mode == "newton":
        res = {"tag": "newton", "uniform": newton_uniform()}
        for r in res["uniform"]:
            print(r)
    elif mode == "converge":
        # oracle self-convergence + image stability under refinement, r_e = 8
        dinf_b = np.geomspace(5.35, 5e4, 800)
        dinf_v = delta_inf_table(dinf_b)
        rows = []
        for r_e in (8.0, 60.0):
            r_o = 4.0 * r_e
            t1 = photon_table(r_e, r_o, n_alpha=2000, dphi=3e-3)
            t2 = photon_table(r_e, r_o, n_alpha=4000, dphi=1.5e-3,
                              phi_max=20.0)
            r1 = scene_frames(r_e, r_o, t1, dinf_b, dinf_v)
            r2 = scene_frames(r_e, r_o, t2, dinf_b, dinf_v)
            pairs = [(a, b) for a, b in zip(r1, r2)
                     if a.get("roots", 0) and b.get("roots", 0)]
            dif = [abs(a["err_phase"] - b["err_phase"]) for a, b in pairs]
            difd = [abs(a["err_design"] - b["err_design"]) for a, b in pairs]
            stable = [a["roots"] == b["roots"] and
                      a.get("sigma_primary") == b.get("sigma_primary")
                      for a, b in pairs]
            rows.append({
                "r_e": r_e, "pairs": len(pairs),
                "max_d_err_phase": max(dif) if dif else None,
                "median_d_err_phase": float(np.median(dif)) if dif else None,
                "max_d_err_design": max(difd) if difd else None,
                "stable_image_fraction": float(np.mean(stable)) if stable
                else None,
                "b_drift_coarse": t1["b_drift_max"],
                "b_drift_fine": t2["b_drift_max"],
            })
        res = {"tag": "converge", "rows": rows}
        print(json.dumps(res, indent=1, default=float))
    else:
        raise SystemExit("modes: calibrate | sweep | newton | converge")
    with open(f"results-{mode}.json", "w") as f:
        json.dump(res, f, indent=1, default=float)
    print(f"wrote results-{mode}.json")


if __name__ == "__main__":
    main()
