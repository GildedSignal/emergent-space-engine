#!/usr/bin/env python3
"""Run 20261019-0628-redteam-638b (premise red-team): the composed strong-field view.

Question: does docs/representation.md L57's gather ("each visible tube crosses the
observer's past light cone once; Newton's method finds the crossing ... lensing adds
crossings, from each doll's memoized deflection(b)") and the measured occlusion cure
(22d1's per-row worldtube test) hold in the field of a black hole, the game's headline
object?

Oracle: exact Schwarzschild null geodesics in the 2D plane (the game's sky is S1, as
the view record's sky-cell census uses), M = 1, static observer at r_o.
  (du/dphi)^2 = 1/b^2 - u^2 (1 - 2u),   dt/dphi = 1 / (b u^2 (1 - 2u)),
  b = r_o sin(alpha) / sqrt(1 - 2/r_o)   (alpha: sky angle from the outward radial,
                                          CCW rays alpha in (0, pi); CW is the mirror).

Channels
  1. shadow:   exact capture arc (b < b_c, inward) vs the worldtube row (occluder =
               the 2M horizon tube) vs the b_c-tube cure; fabricated-visible fraction.
  2. images:   preimage census of the celestial circle at infinity (starfield) and a
               static beacon at r_s = 4M: count, 1D magnification |dPhi/dalpha| per
               image (flat = 1), CCW branch + its mirror.
  3. time:     retarded time along the true geodesic vs the flat row (Shapiro).

Controls (P5): weak-field deflection vs the 4/b + 15pi/4b^2 series; the capture
boundary b = 5.0 / 5.5 vs b_c = 3 sqrt(3); the ensemble shadow arc vs the closed
form; step-halving stability. Judged as behaviours, not continuum identity.
"""
import json
import math
import os
import subprocess
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BC = 3.0 * math.sqrt(3.0)  # photon critical impact parameter 5.19615...
U_CAP = 0.4995


def machine_state():
    out = {}
    for cmd in (["uptime"], ["nproc"]):
        try:
            out[cmd[0]] = subprocess.run(cmd, capture_output=True, text=True, timeout=5).stdout.strip()
        except Exception as e:  # noqa: BLE001
            out[cmd[0]] = f"unavailable: {e}"
    return out


def integrate(r_o, alphas, h=1e-3, max_phi=40.0, u_scr=1e-4, beacon_u=None):
    """Vectorised RK4 over the ray ensemble (CCW sense). Stops per ray at the screen
    (u_scr), the horizon (U_CAP) or max_phi ('stuck'). Optional beacon-radius crossing
    table: (ray index, phi, t, sgn at crossing)."""
    alphas = np.asarray(alphas, dtype=float)
    n = alphas.size
    b = np.maximum(r_o * np.sin(alphas) / math.sqrt(1.0 - 2.0 / r_o), 1e-3)
    u = np.full(n, 1.0 / r_o)
    t = np.zeros(n)
    sgn = np.where(np.cos(alphas) >= 0.0, -1.0, 1.0)
    phi = np.zeros(n)
    flips = np.zeros(n, dtype=int)
    # escape screen per ray: inside 4h/b one phi-step advances u by ~h/b, so the
    # discrete stages cannot resolve t (dt/dphi ~ 1/u^2): stop at u_c and add the
    # exact tail integral of du/(u^2 (1-2u)) = -1/u + 2 ln(u/(1-2u)) down to u_scr
    u_esc = np.maximum(u_scr, 4.0 * h / b)
    F = lambda uu: -1.0 / uu + 2.0 * np.log(uu) - 2.0 * np.log(np.maximum(1.0 - 2.0 * uu, 1e-300))
    status = np.zeros(n, dtype=int)  # 0 active, 1 escaped, 2 captured, 3 stuck
    Phi_out = np.full(n, np.nan)
    t_out = np.full(n, np.nan)
    beacon = []

    def Q(uu, bb):
        return 1.0 / bb**2 - uu * uu * (1.0 - 2.0 * uu)

    def deriv(uu, tt, sg, bb):
        du = sg * np.sqrt(np.maximum(Q(uu, bb), 0.0))
        uc = np.maximum(uu, 0.5 * u_scr)
        dt = 1.0 / (bb * uc * uc * (1.0 - 2.0 * np.maximum(uc, 0.0)))
        return du, dt

    steps = int(max_phi / h)
    for _ in range(steps):
        act_idx = np.nonzero(status == 0)[0]
        if act_idx.size == 0:
            break
        u0, t0, p0 = u[act_idx], t[act_idx], phi[act_idx]
        s0, b0 = sgn[act_idx], b[act_idx]
        k1u, k1t = deriv(u0, t0, s0, b0)
        k2u, k2t = deriv(u0 + 0.5 * h * k1u, t0 + 0.5 * h * k1t, s0, b0)
        k3u, k3t = deriv(u0 + 0.5 * h * k2u, t0 + 0.5 * h * k2t, s0, b0)
        k4u, k4t = deriv(u0 + h * k3u, t0 + h * k3t, s0, b0)
        u1 = u0 + (h / 6.0) * (k1u + 2 * k2u + 2 * k3u + k4u)
        t1 = t0 + (h / 6.0) * (k1t + 2 * k2t + 2 * k3t + k4t)
        p1 = p0 + h


        q1 = Q(u1, b0)
        turn = (q1 < 0.0) & (u1 < 0.5)
        if turn.any():
            for pos in np.nonzero(turn)[0]:
                q0 = Q(u0[pos], b0[pos])
                w = q0 / (q0 - q1[pos])  # linear interp to Q = 0
                i = act_idx[pos]
                # keep u at its pre-step value (Q > 0 there): parking exactly at
                # the root stalls (every probe reads Q <= 0 and flips forever)
                u[i] = u0[pos]
                t[i] = t0[pos] + w * (t1[pos] - t0[pos])
                phi[i] = p0[pos] + w * h
                sgn[i] = -s0[pos]
                flips[i] += 1
            continue  # the aborted step's beacon crossings are not committed

        if beacon_u is not None:  # committed steps only
            crossed = (u0 - beacon_u) * (u1 - beacon_u) < 0.0
            for pos in np.nonzero(crossed)[0]:
                w = (u0[pos] - beacon_u) / (u0[pos] - u1[pos])
                beacon.append((int(act_idx[pos]), p0[pos] + w * h,
                               t0[pos] + w * (t1[pos] - t0[pos]), float(s0[pos])))



        esc = u1 <= u_esc[act_idx]
        cap = u1 >= U_CAP
        u[act_idx] = u1
        t[act_idx] = t1
        phi[act_idx] = p1
        if esc.any():
            for pos in np.nonzero(esc)[0]:
                w = (u0[pos] - u_esc[act_idx[pos]]) / (u0[pos] - u1[pos])
                i = act_idx[pos]
                ue = u_esc[i]
                Phi_out[i] = p0[pos] + w * h + b[i] * (ue - u_scr)
                t_out[i] = (t0[pos] + w * (t1[pos] - t0[pos])
                            + (F(ue) - F(u_scr)))
                status[i] = 1
        for pos in np.nonzero(cap)[0]:
            status[act_idx[pos]] = 2
        status[act_idx[flips[act_idx] > 4]] = 3  # a null ray turns once; more is a stall
        status[act_idx[phi[act_idx] >= max_phi]] = 3
    return {"status": status, "Phi": Phi_out, "t": t_out, "b": b, "alpha": alphas,
            "beacon": beacon}


def alpha_for_b(r_o, b):
    s = b * math.sqrt(1.0 - 2.0 / r_o) / r_o
    return None if s >= 1.0 else math.pi - math.asin(s)  # inward-pointing ray


def shadow_closed_deg(r_o):
    x = BC * math.sqrt(1.0 - 2.0 / r_o) / r_o
    return 180.0 if x >= 1.0 else 2.0 * math.degrees(math.asin(x))


def straight_arc_deg(r_o, radius):
    """Apparent arc of a tube of given radius under the straight-row (worldtube) law."""
    x = radius / r_o
    return 180.0 if x >= 1.0 else 2.0 * math.degrees(math.asin(x))


def main():
    t0 = time.time()
    res = {"machine": machine_state(), "M": 1.0, "b_c": BC}

    # ---- controls ------------------------------------------------------------
    ctl = {}
    r_o = 6.0
    for b_try, expect in ((5.0, "captured"), (5.5, "escaped")):
        a = alpha_for_b(r_o, b_try)
        got = {1: "escaped", 2: "captured", 3: "stuck"}[integrate(r_o, np.array([a]), h=1e-3, max_phi=25.0)["status"][0]]
        ctl[f"b_{b_try}"] = {"expected": expect, "got": got, "pass": got == expect}
    a = alpha_for_b(1000.0, 100.0)
    flat_sweep = math.pi - math.asin(100.0 / 1000.0) - math.asin(100.0 / 1e4)
    d1 = integrate(1000.0, np.array([a]), h=1e-3, max_phi=6.0)["Phi"][0] - flat_sweep
    d2 = integrate(1000.0, np.array([a]), h=5e-4, max_phi=6.0)["Phi"][0] - flat_sweep
    series = 4.0 / 100.0 + 15.0 * math.pi / (4.0 * 100.0**2)
    ctl["deflection_b100"] = {"geodesic_h1": d1, "geodesic_h2": d2, "series": series,
                              "rel_series": abs(d1 - series) / series,
                              "step_ratio": d2 / d1,
                              "pass": abs(d1 - series) / series < 1.2e-2 and abs(d2 / d1 - 1.0) < 3e-3}
    alphas = np.linspace(1e-5, math.pi - 1e-5, 6000)
    for hh, key in ((1e-3, "h1"), (5e-4, "h2")):
        frac = float((integrate(r_o, alphas, h=hh, max_phi=60.0)["status"] == 2).mean())
        ctl[f"shadow_fraction_{key}"] = frac
    ctl["shadow_step_ratio"] = ctl["shadow_fraction_h2"] / ctl["shadow_fraction_h1"]
    ctl["shadow_closed_fraction"] = shadow_closed_deg(6.0) / 360.0
    ctl["shadow_ensemble_vs_closed_deg"] = abs(360.0 * ctl["shadow_fraction_h1"] - shadow_closed_deg(6.0))
    ctl["pass_all"] = all(v.get("pass", True) for v in ctl.values() if isinstance(v, dict)) and ctl["shadow_step_ratio"] < 1.002
    res["controls"] = ctl

    # ---- channel 1: shadow vs worldtube vs cure -------------------------------
    rows = []
    for r_o in (3.2, 3.5, 4.0, 6.0, 10.0, 20.0, 50.0):
        exact = shadow_closed_deg(r_o)
        tube = straight_arc_deg(r_o, 2.0)
        cure = straight_arc_deg(r_o, BC * math.sqrt(1.0 - 2.0 / r_o))
        ens = 360.0 * float((integrate(r_o, alphas, h=1e-3, max_phi=60.0)["status"] == 2).mean())
        rows.append({"r_o": r_o, "exact_arc_deg": exact, "ensemble_arc_deg": ens,
                     "worldtube_2M_arc_deg": tube,
                     "ratio_exact_over_tube": exact / tube if tube else None,
                     "cure_bc_arc_deg": cure, "cure_err_deg": abs(cure - exact),
                     "fabricated_visible_fraction": max(0.0, (exact - tube) / 360.0)})
    res["shadow_table"] = rows

    # ---- channels 2+3: fine map at r_o = 6 ------------------------------------
    r_o = 6.0
    alphas_f = np.linspace(1e-5, math.pi - 1e-5, 12000)
    out = integrate(r_o, alphas_f, h=1e-3, max_phi=45.0, beacon_u=0.25)
    esc = out["status"] == 1
    # Phi(alpha) is monotone increasing on the escaping set; sort by Phi and invert.
    # Rays with b below the floor pile (near-radial outward) carry garbage slopes:
    # excluded from the map (they are the primaries of sources within ~0.3 deg of
    # the observer's back direction, c ~ 0).
    okb = out["b"][esc] > 0.03
    P = out["Phi"][esc][okb]
    A = out["alpha"][esc][okb]
    T = out["t"][esc][okb]
    order = np.argsort(P)
    P_s, A_s, T_s = P[order], A[order], T[order]
    mu_at = np.gradient(A_s, P_s)          # 1D magnification |d alpha / d c| (flat = 1)
    p_max = float(P_s[-1])

    star_rows = []
    ghost5_angles = []
    for c_s in np.linspace(0.0, 2.0 * math.pi, 721)[:-1]:
        if math.degrees(min(c_s, 2.0 * math.pi - c_s)) < 1.0:
            continue
        mus = []
        # CCW images: Phi = c + 2 pi k; CW images: the mirror of the CCW preimages
        # of -c (a mirrored ray serves the source at -c, not the same one)
        for target in (c_s, -c_s):
            for k in range(0, 6):
                tgt = target + 2.0 * math.pi * k
                if tgt > p_max:
                    break
                j = np.searchsorted(P_s, tgt)
                if 1 <= j < len(P_s):
                    mus.append(abs(mu_at[j]))
        mus.sort(reverse=True)
        if mus:
            star_rows.append({"c_deg": math.degrees(c_s), "n": len(mus), "mu": mus[:4],
                              "ghost_ratio": mus[1] / mus[0] if len(mus) > 1 else 0.0})
            if len(mus) > 1 and mus[1] / mus[0] > 0.05:
                ghost5_angles.append(abs(((c_s + math.pi) % (2 * math.pi)) - math.pi))
    res["starfield"] = {
        "n_sources": len(star_rows),
        "min_images": min(r["n"] for r in star_rows),
        "max_images": max(r["n"] for r in star_rows),
        "ghost_gt5pct": sum(1 for r in star_rows if r["ghost_ratio"] > 0.05),
        "ghost_gt1pct": sum(1 for r in star_rows if r["ghost_ratio"] > 0.01),
        "max_ghost_ratio": max(r["ghost_ratio"] for r in star_rows),
        "ghost5_band_deg_either_side": math.degrees(max(ghost5_angles)) if ghost5_angles else 0.0,
        "sample_deg0": star_rows[0], "sample_deg90": star_rows[180],
        "sample_deg179_5": star_rows[359],
    }
    # magnification collapse next to the rim (Newton-seed tangent error): mu = dalpha/dc
    res["rim_magnification"] = {
        "min_mu_next_to_rim": float(np.min(mu_at[A_s > math.radians(134.0)])),
        "band_below_0p1_deg": float(2.0 * (135.0 - math.degrees(A_s[np.nonzero(mu_at < 0.1)[0][0]]))) if (mu_at < 0.1).any() else 0.0,
    }
    # Shapiro on star rays: t to the screen minus flat distance to the screen
    dt = T_s - (1e4 - r_o)
    res["shapiro_star"] = {"max_M": float(dt.max()),
                           "at_alpha_deg": float(math.degrees(A_s[int(np.argmax(dt))])),
                           "median_M": float(np.median(dt))}

    # beacon at r_s = 4M: preimages over ALL crossing branches (first crossings cover
    # only phi < ~1.53 rad; the rest live on second crossings and whirl wraps)
    r_s = 4.0
    # branches by within-ray crossing order (m = 0 first/inward, 1 outward, 2+ whirls);
    # phi-sorted crossings interleave branches, so monotonicity cannot recover them
    per_ray = {}
    for (i, p, tt, _sg) in out["beacon"]:
        per_ray.setdefault(int(i), []).append((p, tt))
    by_m = {}
    for i, lst in per_ray.items():
        for m, (p, tt) in enumerate(lst):
            by_m.setdefault(m, []).append((out["alpha"][i], p, tt))
    segs = []
    for m, mrows in sorted(by_m.items()):
        arr = np.array(sorted(mrows, key=lambda r: r[1]))
        if len(arr) > 16:
            segs.append(arr)

    def beacon_hits(phi_s):
        # images of the beacon at phi_s: CCW rays whose r_s crossing = phi_s + 2 pi j,
        # plus CW rays = the mirror of the CCW preimages of -phi_s (reflection maps
        # phi_s to -phi_s; doubling each hit would fabricate equal-flux pairs)
        hits = []
        for target, sense in ((phi_s, +1.0), (-phi_s, -1.0)):
            for j in range(0, 3):
                tgt = target + 2.0 * math.pi * j
                for sgm in segs:
                    p_b, a_b, t_b = sgm[:, 1], sgm[:, 0], sgm[:, 2]
                    if p_b[0] < tgt < p_b[-1]:
                        aa = np.interp(tgt, p_b, a_b)
                        tt = np.interp(tgt, p_b, t_b)
                        sl = np.interp(tgt, p_b, np.gradient(p_b, a_b))
                        hits.append({"alpha_deg": sense * math.degrees(aa), "t": float(tt),
                                     "mu": abs(1.0 / float(sl)) if sl != 0 else float("inf")})
        return hits

    beacon_rows = []
    for phi_s in np.linspace(0.05, 2.0 * math.pi, 24)[:-1]:
        imgs = [i for i in beacon_hits(phi_s) if math.isfinite(i["mu"])]
        mus = sorted((i["mu"] for i in imgs), reverse=True)
        ts = [i["t"] for i in imgs]
        t_flat = math.sqrt(r_o**2 + r_s**2 - 2 * r_o * r_s * math.cos(phi_s))
        beacon_rows.append({
            "phi_s_deg": math.degrees(phi_s), "n_images": len(imgs),
            "t_flat": t_flat, "t_geodesic_min": min(ts) if ts else None,
            "t_geodesic_max": max(ts) if ts else None,
            "shapiro_max_frac": (max(ts) / t_flat - 1.0) if ts else None,
            "mu_sorted": [round(m, 4) for m in mus[:4]],
            "ghost_ratio": (mus[1] / mus[0]) if len(mus) > 1 else 0.0,
            "alpha_degs": [round(i["alpha_deg"], 2) for i in imgs],
        })
    res["beacon"] = {
        "r_s": r_s, "rows": beacon_rows,
        "max_images": max(r["n_images"] for r in beacon_rows),
        "ghost_gt5pct_rows": sum(1 for r in beacon_rows if r["ghost_ratio"] > 0.05),
        "ghost_gt1pct_rows": sum(1 for r in beacon_rows if r["ghost_ratio"] > 0.01),
        "n_rows": len(beacon_rows),
        "max_shapiro_frac": max(r["shapiro_max_frac"] for r in beacon_rows if r["shapiro_max_frac"] is not None),
    }

    res["wall_s"] = time.time() - t0
    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(res, f, indent=1, default=float)
    print("controls:", json.dumps(ctl, indent=1, default=float))
    print("shadow:")
    for r in rows:
        print(f"  r_o={r['r_o']:>5}: exact {r['exact_arc_deg']:6.2f} (ens {r['ensemble_arc_deg']:6.2f}) "
              f"tube2M {r['worldtube_2M_arc_deg']:6.2f} ratio {r['ratio_exact_over_tube']:.3f} "
              f"cure_err {r['cure_err_deg']:.1e} fabricated {100*r['fabricated_visible_fraction']:.1f}%")
    print("starfield:", json.dumps(res["starfield"], default=float))
    print("rim:", res["rim_magnification"])
    print("shapiro:", res["shapiro_star"])
    print("beacon:", {k: v for k, v in res["beacon"].items() if k != "rows"})
    for r in beacon_rows[:6]:
        print("   ", r)
    print(f"wall {res['wall_s']:.1f}s")


if __name__ == "__main__":
    main()
