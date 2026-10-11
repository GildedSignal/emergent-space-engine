#!/usr/bin/env python3
"""Second-author run on 20261011-1917-redteam-fb64 (silver).

The checker's named experiment, done:
1. `quad`    — the arrival-time oracle converged (substep re-integration of
               the arrival step) and validated at EVERY sampled b against an
               independent u-space Gauss-Legendre quadrature (sin^2(psi)
               substitution kills both the turning-point and grazing-launch
               endpoint singularities). Also regenerates the checker's finding
               against the ORIGINAL linear-interpolation table.
2. `sweep2`  — the silver sweep rerun on the fixed oracle (same scene code,
               attack.scene_frames, unchanged); P8 re-derived.
3. `imgmemo` — the image-resolved delay memo prototyped at r_e in
               {6, 8, 20} (+ 60 as single-image control): travel time dt(b)
               keyed per image (arrival family + winding segment + local
               alpha window), crossing solved as te = t_obs - dt_img(b(te))
               with b from the bent arrival direction; per-family memo and an
               unbent ablation computed on the same tracked image.

attack.py (the silver run's shipped script) is untouched; this file imports
its scene machinery so the corrected sweep differs from the silver record by
exactly one change: the table.
"""
import json
import sys
import time

import numpy as np

import attack
from attack import (M, TWO_PI, ang_between, body_pos, chord, delta_inf_table,
                    flat_newton, rot, scene_frames, signed_angle)

SCENES = [6.0, 8.0, 20.0, 60.0, 200.0, 1000.0]
DEC_DPHI = 7.5e-4  # decisive tables: checker-prescribed finer dphi + substeps
PIXEL = 1.45e-3  # one pixel, 1080p over 90 deg FOV (vertical convention)


# ----------------------------------------------------------------------------
# Fixed oracle: identical to attack.photon_table except the arrival step is
# re-integrated with n_sub RK4 substeps and the crossing is interpolated
# within a substep (step-limited final-step interpolation), instead of linear
# interpolation across the whole coarse step.
# ----------------------------------------------------------------------------

def photon_table_fixed(r_e, r_o, n_alpha=2000, dphi=3e-3, phi_max=14.0,
                       n_sub=128):
    alpha = np.linspace(0.02, np.pi - 0.02, n_alpha)
    u_e, u_o = 1.0 / r_e, 1.0 / r_o
    b = r_e * np.sin(alpha) / np.sqrt(1.0 - 2.0 * M * u_e)
    disc0 = 1.0 / b**2 - u_e**2 + 2.0 * M * u_e**3
    u = np.full(n_alpha, u_e)
    w = np.where(alpha < np.pi / 2, -np.sqrt(np.maximum(disc0, 0.0)),
                 np.sqrt(np.maximum(disc0, 0.0)))
    T = np.zeros(n_alpha)
    PHI = np.zeros(n_alpha)
    arrived = np.zeros(n_alpha, bool)
    A_phi = np.full(n_alpha, np.nan)
    A_t = np.full(n_alpha, np.nan)
    A_u = np.full(n_alpha, np.nan)
    A_w = np.full(n_alpha, np.nan)
    fallbacks = 0

    def dL(u_, w_, b_):
        den = b_ * u_ * u_ * (1.0 - 2.0 * M * u_)
        den = np.where(np.abs(den) < 1e-300, 1e-300, den)
        return w_, 3.0 * u_ * u_ - u_, 1.0 / den

    nsteps = int(phi_max / dphi)
    for _ in range(nsteps):
        live = ~arrived & (u < 0.5 - 1e-12) & (u > 0.0) & np.isfinite(u)
        if not live.any():
            break
        idx = np.nonzero(live)[0]
        u0, w0, T0 = u[idx], w[idx], T[idx]
        bL = b[idx]

        k1u, k1w, k1t = dL(u0, w0, bL)
        k2u, k2w, k2t = dL(u0 + 0.5 * dphi * k1u, w0 + 0.5 * dphi * k1w, bL)
        k3u, k3w, k3t = dL(u0 + 0.5 * dphi * k2u, w0 + 0.5 * dphi * k2w, bL)
        k4u, k4w, k4t = dL(u0 + dphi * k3u, w0 + dphi * k3w, bL)
        uN = u0 + dphi / 6.0 * (k1u + 2 * k2u + 2 * k3u + k4u)
        wN = w0 + dphi / 6.0 * (k1w + 2 * k2w + 2 * k3w + k4w)
        tN = T0 + dphi / 6.0 * (k1t + 2 * k2t + 2 * k3t + k4t)
        u[idx], w[idx], T[idx] = uN, wN, tN
        PHI[live] += dphi
        crossL = (uN <= u_o) & (wN < 0.0)
        if crossL.any():
            cols = idx[crossL]
            arrived[cols] = True
            # --- the fix: re-walk this step for the crossing columns with
            # n_sub substeps of the same RK4, then interpolate in-substep.
            h = dphi / n_sub
            bcols = b[cols]
            us, ws, Ts = u0[crossL].copy(), w0[crossL].copy(), T0[crossL].copy()
            ph_start = PHI[cols] - dphi
            hit = np.zeros(cols.size, bool)
            for j in range(n_sub):
                act = np.nonzero(~hit)[0]
                if act.size == 0:
                    break
                u0s, w0s, T0s = us[act], ws[act], Ts[act]
                bA = bcols[act]
                s1u, s1w, s1t = dL(u0s, w0s, bA)
                s2u, s2w, s2t = dL(u0s + 0.5 * h * s1u, w0s + 0.5 * h * s1w, bA)
                s3u, s3w, s3t = dL(u0s + 0.5 * h * s2u, w0s + 0.5 * h * s2w, bA)
                s4u, s4w, s4t = dL(u0s + h * s3u, w0s + h * s3w, bA)
                uNs = u0s + h / 6.0 * (s1u + 2 * s2u + 2 * s3u + s4u)
                wNs = w0s + h / 6.0 * (s1w + 2 * s2w + 2 * s3w + s4w)
                tNs = T0s + h / 6.0 * (s1t + 2 * s2t + 2 * s3t + s4t)
                cr = (uNs <= u_o) & (wNs < 0.0)
                nc = ~cr
                us[act[nc]], ws[act[nc]], Ts[act[nc]] = uNs[nc], wNs[nc], tNs[nc]
                if cr.any():
                    c2 = act[cr]
                    f = ((u0s[cr] - u_o)
                         / np.where(u0s[cr] - uNs[cr] != 0,
                                    u0s[cr] - uNs[cr], 1e-300))
                    f = np.clip(f, 0.0, 1.0)
                    A_phi[cols[c2]] = ph_start[c2] + (j + f) * h
                    A_t[cols[c2]] = T0s[cr] + f * (tNs[cr] - T0s[cr])
                    A_u[cols[c2]] = u_o
                    A_w[cols[c2]] = w0s[cr] + f * (wNs[cr] - w0s[cr])
                    hit[c2] = True
            if (~hit).any():  # defensive: coarse fallback, as the original
                fallbacks += int((~hit).sum())
                miss = cols[~hit]
                sel = np.searchsorted(idx, miss)
                f = ((u0[sel] - u_o)
                     / np.where(u0[sel] - uN[sel] != 0, u0[sel] - uN[sel],
                                1e-300))
                f = np.clip(f, 0.0, 1.0)
                A_phi[miss] = (PHI[miss] - dphi) + f * dphi
                A_t[miss] = T0[sel] + f * (tN[sel] - T0[sel])
                A_u[miss] = u_o
                A_w[miss] = w0[sel] + f * (wN[sel] - w0[sel])
                arrived[miss] = True

    ok = arrived & np.isfinite(A_t)
    drift = np.abs((A_w[ok] ** 2 + A_u[ok] ** 2 - 2.0 * A_u[ok] ** 3)
                   * b[ok] ** 2 - 1.0)
    return {
        "alpha": alpha, "b": b, "arrived": arrived, "A_phi": A_phi,
        "A_t": A_t, "b_drift_max": float(np.max(drift)) if ok.any() else np.nan,
        "out_mask": alpha < np.pi / 2, "in_mask": alpha > np.pi / 2,
        "n_sub": n_sub, "fallbacks": fallbacks,
    }


# ----------------------------------------------------------------------------
# Independent quadrature: u-space Gauss-Legendre with the sin^2(psi)
# substitution anchored at each segment's zero of w (turning point or grazing
# launch), which makes every integrand analytic on the closed panel.
# ----------------------------------------------------------------------------

_GLX, _GLW = np.polynomial.legendre.leggauss(24)
_PAN = 40
_PSI_EDGES = np.linspace(0.0, np.pi / 2, _PAN + 1)
_PSI_NODES = np.concatenate([
    0.5 * (_PSI_EDGES[k] + _PSI_EDGES[k + 1])
    + 0.5 * (_PSI_EDGES[k + 1] - _PSI_EDGES[k]) * _GLX
    for k in range(_PAN)])
_PSI_WEIGHTS = np.concatenate([
    0.5 * (_PSI_EDGES[k + 1] - _PSI_EDGES[k]) * _GLW for k in range(_PAN)])


def _seg_int(kind, b_sub, z, o):
    """Integral of dt/du or dphi/du over u in [min(z,o), max(z,o)] for each
    column of b_sub, where w may vanish at endpoint z; u(psi) = z - (z-o)
    sin^2(psi) makes the integrand analytic (GL16 x 8 panels in psi)."""
    invb2 = (1.0 / b_sub**2)[:, None]
    bs = b_sub[:, None]
    c = (z - o)[:, None]
    s2 = np.sin(_PSI_NODES)[None, :] ** 2
    uu = z[:, None] - c * s2
    jac = (np.abs(2.0 * c) * np.sin(_PSI_NODES)[None, :]
           * np.cos(_PSI_NODES)[None, :])
    w = np.sqrt(np.maximum(invb2 - uu**2 + 2.0 * uu**3, 1e-300))
    if kind == "dt":
        F = 1.0 / (bs * uu**2 * (1.0 - 2.0 * uu) * w)
    else:
        F = 1.0 / w
    return np.sum(F * jac * _PSI_WEIGHTS[None, :], axis=1)


def quad_travel(b_col, u_e, u_o, out_mask):
    """dt and dphi by the independent quadrature, per column. out_mask True =
    outbound monotone segment [u_o, u_e]; else in-branch with turning point."""
    n = b_col.size
    dt = np.zeros(n)
    ph = np.zeros(n)
    if out_mask.any():
        rows = np.nonzero(out_mask)[0]
        bs = b_col[rows]
        z = np.full(rows.size, u_e)   # anchor at u_e (grazing launch zero)
        o = np.full(rows.size, u_o)
        dt[rows] = _seg_int("dt", bs, z, o)
        ph[rows] = _seg_int("phi", bs, z, o)
    if (~out_mask).any():
        rows = np.nonzero(~out_mask)[0]
        bs = b_col[rows]
        invb2 = 1.0 / bs**2
        lo = np.full(rows.size, u_e)
        hi = np.full(rows.size, 1.0 / 3.0)
        fhi = invb2 - hi**2 + 2 * hi**3
        valid = fhi <= 0.0
        for _ in range(90):
            mid = 0.5 * (lo + hi)
            fm = invb2 - mid**2 + 2 * mid**3
            down = fm > 0.0
            lo = np.where(down, mid, lo)
            hi = np.where(down, hi, mid)
        u_t = 0.5 * (lo + hi)
        zt = u_t.copy()
        dt_up = _seg_int("dt", bs, zt, np.full(rows.size, u_e))
        dt_dn = _seg_int("dt", bs, zt, np.full(rows.size, u_o))
        ph_up = _seg_int("phi", bs, zt, np.full(rows.size, u_e))
        ph_dn = _seg_int("phi", bs, zt, np.full(rows.size, u_o))
        dt[rows] = np.where(valid, dt_up + dt_dn, np.nan)
        ph[rows] = np.where(valid, ph_up + ph_dn, np.nan)
    return dt, ph

def mode_quad():
    """Validate A_t/A_phi of (a) the silver run's shipped table and (b) the
    decisive fixed table (dphi=7.5e-4 + substep arrival) against the
    independent quadrature, at EVERY arrived column of every scene."""
    out = {"note": "A_t/A_phi vs independent u-space GL24x40(sin^2 psi)",
           "dphi_fixed": DEC_DPHI, "scenes": []}
    for r_e in SCENES:
        r_o = 4.0 * r_e
        u_e, u_o = 1.0 / r_e, 1.0 / r_o
        tabs = {"original": attack.photon_table(r_e, r_o),
                "fixed": photon_table_fixed(r_e, r_o, dphi=DEC_DPHI)}
        arr = tabs["original"]["arrived"]
        dt_q = np.full(arr.size, np.nan)
        ph_q = np.full_like(dt_q, np.nan)
        for name in ("out", "in"):
            mask = (tabs["original"]["out_mask"] if name == "out"
                    else tabs["original"]["in_mask"]) & arr
            if not mask.any():
                continue
            dt, ph = quad_travel(tabs["original"]["b"][mask], u_e, u_o,
                                 np.ones(int(mask.sum()), bool) if name == "out"
                                 else np.zeros(int(mask.sum()), bool))
            dt_q[mask] = dt
            ph_q[mask] = ph
        sc = {"r_e": r_e, "r_o": r_o, "n_arrived": int(arr.sum()),
              "n_quad_nan": int((arr & ~np.isfinite(dt_q)).sum())}
        small = tabs["original"]["out_mask"] & arr & (
            tabs["original"]["b"] < 0.15 * r_e)
        for tag in ("original", "fixed"):
            t = tabs[tag]
            ok = arr & np.isfinite(dt_q) & np.isfinite(t["A_t"])
            relt = np.abs(t["A_t"][ok] - dt_q[ok]) / dt_q[ok]
            absphi = np.abs(t["A_phi"][ok] - ph_q[ok])
            i = int(np.argmax(relt))
            bb = t["b"][ok][i]
            ok_small = small & np.isfinite(dt_q) & np.isfinite(t["A_t"])
            relt_small = (np.abs(t["A_t"][ok_small] - dt_q[ok_small])
                          / dt_q[ok_small])
            j = int(np.argmax(relt_small))
            sc[tag] = {
                "A_t_relerr_max": float(relt.max()),
                "A_t_abserr_max_M": float(np.abs(t["A_t"][ok]
                                                 - dt_q[ok]).max()),
                "A_t_relerr_max_at_b": float(bb),
                "A_t_relerr_median": float(np.median(relt)),
                "A_phi_abserr_max": float(absphi.max()),
                "smallb_out": {
                    "n": int(ok_small.sum()),
                    "A_t_abserr_max_M": float(np.abs(
                        t["A_t"][ok_small] - dt_q[ok_small]).max()),
                    "at_b": float(t["b"][ok_small][j]),
                },
                "b_drift_max": t["b_drift_max"],
            }
        sc["fixed"]["fallbacks"] = tabs["fixed"]["fallbacks"]
        out["scenes"].append(sc)
        o, f = sc["original"], sc["fixed"]
        print(f"r_e={r_e:9.1f}  orig: rel {o['A_t_relerr_max']:.2e} "
              f"(abs {o['A_t_abserr_max_M']:.2f} M at b~"
              f"{o['smallb_out']['at_b']:.1f})  fixed: rel "
              f"{f['A_t_relerr_max']:.2e} abs {f['A_t_abserr_max_M']:.2e} M  "
              f"dphi {f['A_phi_abserr_max']:.2e}")
    with open("results-quad.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote results-quad.json")


# ----------------------------------------------------------------------------
# Corrected sweep: attack.scene_frames on the fixed table, same aggregation.
# ----------------------------------------------------------------------------

def run_scenes_fixed(r_e_list, tag):
    dinf_b = np.geomspace(5.35, 5e4, 800)
    dinf_v = delta_inf_table(dinf_b)
    results = {"tag": tag, "M": M, "oracle": "fixed-substep-n128",
               "dphi": DEC_DPHI, "scenes": []}
    for r_e in r_e_list:
        r_o = 4.0 * r_e
        table = photon_table_fixed(r_e, r_o, dphi=DEC_DPHI)
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
            "err_fix_ratio": (med("err_fix") / med("err_phase")
                              if good else None),
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
              f"{sc['err_phase_med']:.2e}  err_fix {sc['err_fix_med']:.2e} "
              f"(ratio {sc['err_fix_ratio']:.3f})  nodefl "
              f"{sc['err_nodefl_med']:.2e}  noretard {sc['err_noretard_med']:.2e}"
              f"  newton_max {sc['newton_iters_max']} fails "
              f"{sc['newton_fails']}")
    return results


def mode_sweep2():
    res = run_scenes_fixed(SCENES, "sweep2")
    with open("results-sweep2.json", "w") as fh:
        json.dump(res, fh, indent=1)
    # P8 re-derivation
    print("\nP8 re-derived (converged oracle):")
    for sc in res["scenes"]:
        r = sc["r_e"]
        c1 = sc["err_fix_med"] < 1e-4
        c2 = sc["err_fix_med"] < sc["err_phase_med"] / 10.0
        p8 = (c1 if r >= 20 else c2)
        print(f"  r_e={r:7.1f}: err_fix {sc['err_fix_med']:.2e}  "
              f"{'PASS' if p8 else 'FAIL'}  "
              f"({'<1e-4' if r >= 20 else '<phase/10'})")
    print("wrote results-sweep2.json")


# ----------------------------------------------------------------------------
# Image-resolved delay memo prototype.
# ----------------------------------------------------------------------------

def _bend_curve(table, sigma, sel, r_e, r_o):
    """bend(b) over selected columns of one arrival family (attack's formula)."""
    b_g = table["b"][sel]
    ph_g = table["A_phi"][sel]
    u_o = 1.0 / r_o
    sin_ao = np.clip(b_g * u_o * np.sqrt(1.0 - 2.0 * M * u_o), 0.0, 1.0)
    ao = np.arcsin(sin_ao)
    xe = r_e * np.cos(-sigma * ph_g)
    ye = r_e * np.sin(-sigma * ph_g)
    ch = np.stack([xe - r_o, ye])
    ch = ch / np.linalg.norm(ch, axis=0)
    ap = np.stack([-np.cos(ao), -sigma * np.sin(ao)])
    cr = ch[0] * ap[1] - ch[1] * ap[0]
    dt_ = np.clip(ch[0] * ap[0] + ch[1] * ap[1], -1.0, 1.0)
    bend = np.arctan2(cr, dt_)
    order = np.argsort(b_g)
    b_s, v_s = b_g[order], bend[order]
    keep = np.concatenate([[True], np.diff(b_s) > 0])
    return b_s[keep], v_s[keep]


def scene_imgmemo(r_e, r_o, table, n_frames=16, phi0=1.0, alpha_win=0.35):
    omega = np.sqrt(M / r_e**3)
    period = TWO_PI / omega
    x_o = np.array([r_o, 0.0])
    u_o = 1.0 / r_o
    sin_den = u_o * np.sqrt(1.0 - 2.0 * M * u_o)
    prev_roots = None
    hero_prev_idx = None
    prev_te = None
    recs = []
    seed = None
    for j in range(n_frames):
        t_obs = 0.35 * period + j * period / n_frames
        if seed is None:
            xb, _ = body_pos(phi0, omega, t_obs, r_e)
            seed = t_obs - np.linalg.norm(xb - x_o)
        te_flat, iters, ok = flat_newton(phi0, omega, r_e, x_o, t_obs, seed)
        seed = te_flat
        d_flat, xb_flat, D_flat = chord(phi0, omega, r_e, x_o, te_flat)
        b_flat = abs(x_o[0] * d_flat[1] - x_o[1] * d_flat[0])
        # ---- root scan (as attack.scene_frames) ----
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
                H = phi0 + omega * (t_obs - t_g) + ph_g
                kmin = int(np.floor((H.min() - 1e-9) / TWO_PI))
                kmax = int(np.ceil((H.max() + 1e-9) / TWO_PI))
                for k in range(kmin, kmax + 1):
                    Hk = H - TWO_PI * k
                    s = np.sign(Hk)
                    idx0 = np.nonzero(np.diff(s) != 0)[0]
                    for i0 in idx0:
                        a0, a1 = a_g[i0], a_g[i0 + 1]
                        for _ in range(60):
                            am = 0.5 * (a0 + a1)
                            Hm = (np.interp(am, a_g, H) - TWO_PI * k)
                            if np.sign(Hm) == np.sign(Hk[i0]):
                                a0 = am
                            else:
                                a1 = am
                        astar = 0.5 * (a0 + a1)
                        roots.append({
                            "sigma": sigma, "alpha": astar, "branch": branch,
                            "k": k,
                            "b": float(np.interp(astar, a_g, b_g)),
                            "dphi": float(sigma * np.interp(astar, a_g,
                                                            table["A_phi"][sel])),
                            "dt": float(np.interp(astar, a_g, t_g)),
                        })
        if not roots:
            recs.append({"t_obs": t_obs, "roots": 0})
            continue
        roots.sort(key=lambda R: abs(R["b"] - b_flat))
        # ---- tracking: match current roots to prev by (sigma, branch, alpha)
        jump = True
        hero = roots[0]
        if prev_roots is not None and hero_prev_idx is not None:
            hp = prev_roots[hero_prev_idx]
            best, bd = None, alpha_win
            for i, R in enumerate(roots):
                if R["sigma"] == hp["sigma"] and R["branch"] == hp["branch"]:
                    d = abs(R["alpha"] - hp["alpha"])
                    if d < bd:
                        best, bd = i, d
            if best is not None:
                hero, jump = roots[best], False
        hero_idx = roots.index(hero)
        te_true = t_obs - hero["dt"]
        d_true, _, _ = chord(phi0, omega, r_e, x_o, te_true)
        # ---- image-local memo: family + winding segment + alpha window
        fam = (table["out_mask"] if hero["branch"] == "out"
               else table["in_mask"]) & table["arrived"]
        a_f = table["alpha"][fam]
        seg_root = int(np.floor(np.interp(hero["alpha"], a_f,
                                          table["A_phi"][fam]) / TWO_PI))
        seg = np.floor(table["A_phi"][fam] / TWO_PI).astype(int)
        sel = np.zeros_like(fam)
        sel[np.nonzero(fam)[0]] = ((np.abs(table["alpha"][fam]
                                           - hero["alpha"]) <= alpha_win)
                                   & (seg == seg_root))
        n_img = int(sel.sum())
        b_all = table["b"][sel]
        order = np.argsort(b_all)
        b_img = b_all[order]
        keep = np.concatenate([[True], np.diff(b_img) > 0])
        b_img = b_img[keep]
        t_img = table["A_t"][sel][order][keep]
        # image-local bend(b) and flat-chord D(b) curves
        u_oq = 1.0 / r_o
        sin_ao = np.clip(b_img * u_oq * np.sqrt(1.0 - 2.0 * M * u_oq), 0.0, 1.0)
        ao = np.arcsin(sin_ao)
        ph_sel = table["A_phi"][sel][order][keep]
        xe = r_e * np.cos(-hero["sigma"] * ph_sel)
        ye = r_e * np.sin(-hero["sigma"] * ph_sel)
        ch = np.stack([xe - r_o, ye])
        ch = ch / np.linalg.norm(ch, axis=0)
        ap = np.stack([-np.cos(ao), -hero["sigma"] * np.sin(ao)])
        cr = ch[0] * ap[1] - ch[1] * ap[0]
        dtq = np.clip(ch[0] * ap[0] + ch[1] * ap[1], -1.0, 1.0)
        bend_img = np.arctan2(cr, dtq)
        D_img = np.hypot(xe - r_o, ye)
        # alpha-parametrized curves (the tube memo's native coordinates:
        # A_phi is monotone in alpha per branch, so angular closure inverts
        # without folds; b-parametrized curves fold near the photon ring).
        a_sel = table["alpha"][sel]
        aph_a = table["A_phi"][sel]
        dt_a = table["A_t"][sel]
        oA = np.argsort(aph_a)
        aph_s, alpha_s, dt_s = aph_a[oA], a_sel[oA], dt_a[oA]
        ph_e_s = -hero["sigma"] * aph_s
        D_s = np.hypot(r_e * np.cos(ph_e_s) - r_o, r_e * np.sin(ph_e_s))
        # ---- three crossing solves, same target d_true. All keep the
        # shipped contractive structure te = t_obs - D(te) - dly. Seeds: the
        # tracked image is solved WARM from the previous frame's converged
        # time for that image (the design's own previous-frame seed); on a
        # tracking jump every solve restarts cold from te_flat.
        seed_warm = (prev_te["img"] if (prev_te and not jump) else te_flat)
        seed_warm_fam = (prev_te["family"] if (prev_te and not jump)
                         else te_flat)
        solves = {}
        # (a) per-family (shipped): te = t_obs - D(te) - delay_family(b(te))
        te = seed_warm_fam
        for _ in range(80):
            dtmp, _, Dtmp = chord(phi0, omega, r_e, x_o, te)
            btmp = abs(x_o[0] * dtmp[1] - x_o[1] * dtmp[0])
            dly = attack.delay_lookup(btmp, table, hero["sigma"],
                                      hero["branch"], r_e, r_o)
            te_new = t_obs - Dtmp - dly
            if abs(te_new - te) < 1e-13 * max(1.0, abs(t_obs)):
                te = te_new
                break
            te = te_new
        solves["family"] = ang_between(chord(phi0, omega, r_e, x_o, te)[0],
                                       d_true)
        te_fam_out = te
        # (b/c) image-resolved: dly_img(b) = dt_img(b) - D_img(b), the travel
        # time and flat chord of the image's own light-tube columns.
        clamps_flat = clamps_bent = 0

        def solve_img(use_bent, te_seed):
            """Bracketed bisection on G(te) = te + D(te) + dly_img(b(te))
            - t_obs (the checker's own bracket prescription). The fixed-point
            iteration is not contractible near the photon ring (dly'(b)
            diverges); G is continuous with a bracketed unique root near the
            warm seed."""
            cl = 0

            def G(tev):
                dtmp, _, Dtmp = chord(phi0, omega, r_e, x_o, tev)
                bfl = abs(x_o[0] * dtmp[1] - x_o[1] * dtmp[0])
                if use_bent:
                    # self-consistent impact parameter: the bend memo is
                    # keyed by b, and b follows from the bent ray, so solve
                    # the inner contractive fixed point b = F(b) over the
                    # image window (bend varies slowly in b: |F'| << 1).
                    bq = min(max(bfl, b_img[0]), b_img[-1])
                    for _ in range(40):
                        bend = float(np.interp(bq, b_img, bend_img))
                        v = -rot(dtmp, bend)
                        ao_s = np.arctan2(v[1], v[0])
                        bn = float(np.sin(abs(ao_s)) / sin_den)
                        if abs(bn - bq) < 1e-12:
                            bq = bn
                            break
                        bq = bn
                    bq = min(max(bq, b_img[0]), b_img[-1])
                else:
                    bq = bfl
                if bq < b_img[0] or bq > b_img[-1]:
                    nonlocal cl
                    cl += 1
                dly = (float(np.interp(bq, b_img, t_img))
                       - float(np.interp(bq, b_img, D_img)))
                return tev + Dtmp + dly - t_obs

            w = 8.0
            lo, hi = te_seed - w, te_seed + w
            glo, ghi = G(lo), G(hi)
            for _ in range(6):
                if glo == 0.0 or ghi == 0.0 or (glo < 0) != (ghi < 0):
                    break
                w *= 2.0
                lo, hi = te_seed - w, te_seed + w
                glo, ghi = G(lo), G(hi)
            if (glo < 0) == (ghi < 0):
                return te_seed, cl  # no bracket found: report seed
            for _ in range(100):
                mid = 0.5 * (lo + hi)
                gm = G(mid)
                if gm == 0.0 or (hi - lo) < 1e-13 * max(1.0, abs(t_obs)):
                    break
                if (gm < 0) == (glo < 0):
                    lo, glo = mid, gm
                else:
                    hi, ghi = mid, gm
            return 0.5 * (lo + hi), cl

        te_a, clamps_flat = solve_img(False, seed_warm)
        solves["img_flat"] = ang_between(
            chord(phi0, omega, r_e, x_o, te_a)[0], d_true)
        te_c, clamps_bent = solve_img(True, seed_warm)
        solves["img_bent"] = ang_between(
            chord(phi0, omega, r_e, x_o, te_c)[0], d_true)

        # (d) image-resolved, alpha closure: the tube that closes the angles
        # for emission at te is alpha(te) = A_phi^{-1}(2 pi k - phi0 -
        # omega te); its travel time and chord come from the same columns.
        # G(te*) = te* + dt* + (D(te*) - D_tube(alpha*)) - t_obs = 0 exactly.
        k_img = hero["k"]

        def G_alpha(tev):
            # sigma*A_phi(alpha) = 2 pi k - phi0 - omega*te, so the
            # A_phi value to invert is sigma * (that), since sigma^2 = 1.
            target = hero["sigma"] * (TWO_PI * k_img - phi0 - omega * tev)
            if target < aph_s[0] or target > aph_s[-1]:
                target = np.clip(target, aph_s[0], aph_s[-1])
            av = float(np.interp(target, aph_s, alpha_s))
            dtv = float(np.interp(target, aph_s, dt_s))
            Dv = float(np.interp(target, aph_s, D_s))
            _, _, Dte = chord(phi0, omega, r_e, x_o, tev)
            return tev + dtv + (Dte - Dv) - t_obs

        w = 8.0
        lo, hi = seed_warm - w, seed_warm + w
        glo, ghi = G_alpha(lo), G_alpha(hi)
        for _ in range(6):
            if (glo < 0) != (ghi < 0):
                break
            w *= 2.0
            lo, hi = seed_warm - w, seed_warm + w
            glo, ghi = G_alpha(lo), G_alpha(hi)
        if (glo < 0) != (ghi < 0):
            for _ in range(100):
                mid = 0.5 * (lo + hi)
                gm = G_alpha(mid)
                if gm == 0.0 or (hi - lo) < 1e-13 * max(1.0, abs(t_obs)):
                    break
                if (gm < 0) == (glo < 0):
                    lo, glo = mid, gm
                else:
                    hi, ghi = mid, gm
            te_d = 0.5 * (lo + hi)
        else:
            te_d = seed_warm
        solves["img_alpha"] = ang_between(
            chord(phi0, omega, r_e, x_o, te_d)[0], d_true)
        prev_te = {"img": te_d, "family": te_fam_out}
        recs.append({
            "t_obs": t_obs, "roots": len(roots), "jump": jump,
            "hero": f"{hero['sigma']:+.0f}/{hero['branch']}/k{hero['k']}",
            "alpha_hero": hero["alpha"], "b_true": hero["b"],
            "te_true": te_true, "te_flat": te_flat,
            "n_img_columns": n_img, "b_img_lo": float(b_img[0]),
            "b_img_hi": float(b_img[-1]),
            "clamps_flat": clamps_flat, "clamps_bent": clamps_bent,
            "err_family": solves["family"], "err_img_flat": solves["img_flat"],
            "err_img_bent": solves["img_bent"], "err_img_alpha": solves["img_alpha"],
            "newton_iters": iters, "newton_fail": not ok,
        })
        prev_roots, hero_prev_idx = roots, hero_idx
    return recs

def mode_imgmemo():
    out = {"pixel_floor": PIXEL, "scenes": []}
    for r_e in [6.0, 8.0, 20.0, 60.0]:
        r_o = 4.0 * r_e
        table = photon_table_fixed(r_e, r_o, dphi=DEC_DPHI)
        recs = scene_imgmemo(r_e, r_o, table)
        good = [r for r in recs if r.get("roots", 0) > 0]

        def med(k):
            return float(np.median([r[k] for r in good])) if good else None

        def mx(k):
            return float(np.max([r[k] for r in good])) if good else None

        sc = {
            "r_e": r_e, "r_o": r_o, "n_frames": len(recs),
            "images_med": med("roots"),
            "jumps": sum(1 for r in good if r["jump"]),
            "err_family_med": med("err_family"), "err_family_max": mx("err_family"),
            "err_img_flat_med": med("err_img_flat"), "err_img_flat_max": mx("err_img_flat"),
            "err_img_bent_med": med("err_img_bent"), "err_img_bent_max": mx("err_img_bent"),
            "err_img_alpha_med": med("err_img_alpha"), "err_img_alpha_max": mx("err_img_alpha"),
            "frac_img_bent_below_floor": (
                float(np.mean([r["err_img_bent"] <= PIXEL for r in good]))),
            "frac_img_alpha_below_floor": (
                float(np.mean([r["err_img_alpha"] <= PIXEL for r in good]))),
            "clamps_total": sum(r["clamps_flat"] + r["clamps_bent"]
                                for r in good),
            "frames": good,
        }
        nj = [r for r in good if not r["jump"]]
        sc["err_img_bent_med_nojump"] = (float(np.median(
            [r["err_img_bent"] for r in nj])) if nj else None)
        sc["err_img_alpha_med_nojump"] = (float(np.median(
            [r["err_img_alpha"] for r in nj])) if nj else None)
        sc["err_img_alpha_max_nojump"] = (float(np.max(
            [r["err_img_alpha"] for r in nj])) if nj else None)
        sc["frac_img_alpha_below_floor_nojump"] = (
            float(np.mean([r["err_img_alpha"] <= PIXEL for r in nj]))
            if nj else None)
        sc["err_img_bent_max_nojump"] = (float(np.max(
            [r["err_img_bent"] for r in nj])) if nj else None)
        sc["frac_img_bent_below_floor_nojump"] = (
            float(np.mean([r["err_img_bent"] <= PIXEL for r in nj]))
            if nj else None)
        out["scenes"].append(sc)
        print(f"r_e={r_e:6.1f}  images med {sc['images_med']:.0f}  jumps "
              f"{sc['jumps']}/{len(good)}  family {sc['err_family_med']:.2e}"
              f"/{sc['err_family_max']:.2e}  img_flat "
              f"{sc['err_img_flat_med']:.2e}/{sc['err_img_flat_max']:.2e}  "
              f"img_bent {sc['err_img_bent_med']:.2e}/"
              f"{sc['err_img_bent_max']:.2e}  <=floor "
              f"{sc['frac_img_bent_below_floor']*100:.0f}%  nojump med "
              f"{sc['err_img_bent_med_nojump']:.2e} (<=floor "
              f"{sc['frac_img_bent_below_floor_nojump']*100:.0f}%)  alpha "
              f"{sc['err_img_alpha_med']:.2e}/{sc['err_img_alpha_max']:.2e} "
              f"<=floor {sc['frac_img_alpha_below_floor']*100:.0f}%  nojump "
              f"med {sc['err_img_alpha_med_nojump']:.2e} (<=floor "
              f"{sc['frac_img_alpha_below_floor_nojump']*100:.0f}%)  clamps "
              f"{sc['clamps_total']}")
    with open("results-imgmemo.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote results-imgmemo.json")


def mode_calibrate2():
    res = run_scenes_fixed([10000.0], "calibrate2")
    with open("results-calibrate2.json", "w") as fh:
        json.dump(res, fh, indent=1)
    print("wrote results-calibrate2.json")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "sweep2"
    t0 = time.time()
    {"quad": mode_quad, "sweep2": mode_sweep2, "imgmemo": mode_imgmemo,
     "calibrate2": mode_calibrate2}[mode]()
    print(f"[{mode}] {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main()
