#!/usr/bin/env python3
"""Red-team falsifier for representation.md's view-gather premise (run 20261011-0614).

Premise under attack (docs/representation.md, section 2):
  "Each visible tube crosses the observer's past light cone once; Newton's
   method finds the crossing, starting from the previous frame's. Lensing adds
   crossings, from each doll's memoized deflection(b)."

Parts:
  A. controls (flat space, deflection, capture, step size)
  B. one star behind a Schwarzschild BH, observer orbiting at r_o in
     {6.5, 10, 20, 40} M: true image count per frame (brute-force scan of the
     emission circle) vs a previous-frame Newton tracker seeded with ALL true
     images at frame 0 (generous: the design specifies no seeding at all).
     Newton evaluates Phi(alpha) on the frame's own Phi-table (a perfect
     per-direction oracle: strictly more generous than re-tracing rays).
     An image's identity is its direction; the winding label follows by
     continuity (it drifts by 1 per orbit as the star sweeps the sky).
  C. flat space, observer thrusting to beta 0.998, 200 drifting emitters:
     Newton iterations and wrong roots (premise-survival check).
  D. doc check: closed-form banding error of the Minsky/Binet band tangent
     (representation.md section 1 "primary in-cell solution") for circular
     orbits, plus analytic in-band spot checks.

Float64 throughout. GR is the oracle; the attack is about the gather mechanism.
"""
import json
import math
import numpy as np

M = 1.0
BC = 3.0 * math.sqrt(3.0)          # photon critical impact parameter
TWO_PI = 2.0 * math.pi
OUT = {}


# ---------------------------------------------------------------- photon rays
def integrate_rays(r_o, alphas, dphi=0.03, phi_cap=4.0 * math.pi, u_fin=1.0 / 500.0):
    """Photon Binet u'' = 3 u^2 - u (M=1) from an observer at (r_o, phi=0).

    alphas: emission angle from the outward radial, CCW positive (static frame).
    Returns (Phi, b): Phi = signed accumulated angle when the ray crosses
    r = 1/u_fin outbound; nan if captured (r <= 2M) or lost (wind > cap).
    """
    alphas = np.atleast_1d(np.asarray(alphas, dtype=float))
    sin = np.sin(alphas)
    cos = np.cos(alphas)
    s = np.where(sin >= 0.0, 1.0, -1.0)
    sa = np.maximum(np.abs(sin), 1e-12)
    f = math.sqrt(1.0 - 2.0 * M / r_o)
    b = r_o * sin / f
    u = np.full(alphas.size, 1.0 / r_o)
    up = -cos * f / (r_o * sa)          # mirrored so integration runs in +|phi|
    phi = np.zeros(alphas.size)
    Phi = np.full(alphas.size, np.nan)
    alive = np.ones(alphas.size, dtype=bool)
    nsteps = int(math.ceil(phi_cap / dphi))

    def acc(u_):
        return 3.0 * u_ * u_ - u_

    for _ in range(nsteps):
        if not alive.any():
            break
        k1u = up
        k1a = acc(u)
        k2u = up + 0.5 * dphi * k1a
        k2a = acc(u + 0.5 * dphi * k1u)
        k3u = up + 0.5 * dphi * k2a
        k3a = acc(u + 0.5 * dphi * k2u)
        k4u = up + dphi * k3a
        k4a = acc(u + dphi * k3u)
        u_new = u + dphi / 6.0 * (k1u + 2 * k2u + 2 * k3u + k4u)
        up_new = up + dphi / 6.0 * (k1a + 2 * k2a + 2 * k3a + k4a)

        act = alive & (u_new >= 0.5)                     # captured
        if act.any():
            alive[act] = False
        fin = alive & (u_new <= u_fin)                   # exited outbound
        if fin.any():
            t = (u[fin] - u_fin) / (u[fin] - u_new[fin])
            Phi[fin] = s[fin] * (phi[fin] + t * dphi)
            alive[fin] = False
        mv = alive
        u[mv] = u_new[mv]
        up[mv] = up_new[mv]
        phi[mv] += dphi
        # rays still alive past the cap were near-critical: dropped (nan)
    return Phi, b


def truth_roots(Phi, alphas, phi_rel):
    """All emission angles whose ray reaches the star (r=500, angle phi_rel),
    as (alpha, winding n) pairs, by level-crossing of H = Phi - phi_rel.
    The wrap interval [last, first+2pi] is included."""
    H = Phi - phi_rel
    ok = ~np.isnan(H)
    roots = []
    xs = np.concatenate([alphas, alphas[:1] + TWO_PI])
    Hs = np.concatenate([H, H[:1]])
    oks = np.concatenate([ok, ok[:1]])
    for i in np.nonzero(oks[:-1] & oks[1:])[0]:
        h1, h2 = Hs[i], Hs[i + 1]
        lo, hi = (h1, h2) if h1 <= h2 else (h2, h1)
        n_lo = int(math.ceil(lo / TWO_PI - 1e-9))
        n_hi = int(math.floor(hi / TWO_PI + 1e-9))
        for k in range(n_lo, n_hi + 1):
            tgt = TWO_PI * k
            a = xs[i] + (xs[i + 1] - xs[i]) * (h1 - tgt) / (h1 - h2)
            roots.append((float(a % TWO_PI), k))
    return roots


# ---------------------------------------------------------------- part A: controls
def controls():
    rep = {}

    def flat_phi(r_o, alpha, R=500.0):
        # straight ray from (r_o,0), direction (cos a, sin a), to radius R
        P = np.array([r_o, 0.0])
        d = np.array([math.cos(alpha), math.sin(alpha)])
        pd = P @ d
        s = -pd + math.sqrt(pd * pd - (P @ P) + R * R)
        X = P + s * d
        return math.atan2(X[1], X[0])

    def integrate_flat(r_o, alphas, dphi=0.005, u_fin=1.0 / 500.0):
        # RK4 on u'' = -u (flat photon), same IC mapping, validates the mapping
        alphas = np.atleast_1d(np.asarray(alphas, float))
        sin = np.sin(alphas); cos = np.cos(alphas)
        s = np.where(sin >= 0, 1.0, -1.0)
        sa = np.maximum(np.abs(sin), 1e-12)
        u = np.full(alphas.size, 1.0 / r_o)
        up = -cos / (r_o * sa)
        phi = np.zeros(alphas.size)
        Phi = np.full(alphas.size, np.nan)
        alive = np.ones(alphas.size, bool)
        for _ in range(400000):
            if not alive.any():
                break
            k1u, k1a = up, -u
            k2u, k2a = up + 0.5 * dphi * k1a, -(u + 0.5 * dphi * k1u)
            k3u, k3a = up + 0.5 * dphi * k2a, -(u + 0.5 * dphi * k2u)
            k4u, k4a = up + dphi * k3a, -(u + dphi * k3u)
            u_new = u + dphi / 6 * (k1u + 2 * k2u + 2 * k3u + k4u)
            up_new = up + dphi / 6 * (k1a + 2 * k2a + 2 * k3a + k4a)
            fin = alive & (u_new <= u_fin)
            if fin.any():
                t = (u[fin] - u_fin) / (u[fin] - u_new[fin])
                Phi[fin] = s[fin] * (phi[fin] + t * dphi)
                alive[fin] = False
            mv = alive
            u[mv] = u_new[mv]; up[mv] = up_new[mv]; phi[mv] += dphi
        return Phi

    for r_o in (10.0, 40.0):
        errs = []
        for alpha in np.linspace(0.05, TWO_PI - 0.05, 60):
            Phi = integrate_flat(r_o, [alpha])
            errs.append(abs(Phi[0] - flat_phi(r_o, alpha)))
        rep[f"flat_max_phi_err_r{r_o}"] = float(max(errs))
    # deflection: b=20 from r_o=30, inward; delta = Phi - flat Phi
    r_o = 30.0
    f = math.sqrt(1 - 2.0 / r_o)
    alpha = math.pi - math.asin(20.0 * f / r_o)   # inward, b=+20
    Phi, b = integrate_rays(r_o, [alpha], dphi=0.01)
    delta = Phi[0] - flat_phi(r_o, alpha)
    rep["deflection_b20"] = float(delta)
    rep["deflection_b20_expected_band"] = [0.20, 0.24]   # 4/b .. 4/b+(15pi/4)/b^2
    # capture threshold at r_o=10, inward rays
    r_o = 10.0
    f = math.sqrt(1 - 2.0 / r_o)
    res = {}
    for name, bb in (("below", BC - 0.02), ("above", BC + 0.02)):
        alpha = math.pi - math.asin(min(1.0, bb * f / r_o))
        Phi, _ = integrate_rays(r_o, [alpha], dphi=0.01, phi_cap=8 * math.pi)
        res[name] = bool(np.isnan(Phi[0]))
    rep["capture_below_crit_captured"] = res["below"]
    rep["capture_above_crit_escapes"] = not res["above"]
    # step-size sensitivity of the truth grid
    r_o = 10.0
    alphas = (np.arange(3600) + 0.5) / 3600.0 * TWO_PI
    P1, _ = integrate_rays(r_o, alphas, dphi=0.03)
    P2, _ = integrate_rays(r_o, alphas, dphi=0.0075)
    d = np.abs(P1 - P2)
    d = d[~np.isnan(d)]
    rep["dphi03_vs_dphi0075_max"] = float(d.max())
    rep["dphi03_vs_dphi0075_p99"] = float(np.percentile(d, 99))
    return rep


# ---------------------------------------------------------------- part B: the gather
def gather_scan(r_o, frames=32, nalpha=3600):
    alphas = (np.arange(nalpha) + 0.5) / nalpha * TWO_PI
    f = math.sqrt(1.0 - 2.0 * M / r_o)
    shadow_deg = math.degrees(math.asin(min(1.0, BC * f / r_o)))
    per_frame = []
    track = None
    for fr in range(frames):
        phi_rel = (-TWO_PI * fr / frames) % TWO_PI
        Phi, b = integrate_rays(r_o, alphas, dphi=0.03)
        roots = truth_roots(Phi, alphas, phi_rel)
        rec = {"frame": fr, "true_count": len(roots),
               "roots": [(round(a, 5), n) for a, n in roots]}
        # ---- the design's mechanism: Newton from the previous frame's root.
        # Phi(alpha) evaluated on this frame's own Phi table (perfect oracle).
        # The image's identity is its direction; the winding label follows.
        if track is None:
            track = [list(r) for r in roots]      # generous seeding
        else:
            xs = np.concatenate([alphas - TWO_PI, alphas, alphas + TWO_PI])
            ys = np.concatenate([Phi, Phi, Phi])

            def phi_of(a):
                return np.interp(a, xs, ys)

            keep = []
            collapsed = 0
            for a_prev, _ in track:
                a = a_prev
                n0 = round(float(phi_of(a) - phi_rel) / TWO_PI)   # continuity
                ok = False
                for _ in range(6):
                    g = phi_of(a) - phi_rel - TWO_PI * n0
                    if abs(g) < 1e-9:
                        ok = True
                        break
                    h = 1e-5
                    dg = (phi_of(a + h) - phi_of(a)) / h
                    if not np.isfinite(dg) or abs(dg) < 1e-9:
                        break
                    a = a - g / dg
                    if not (-TWO_PI <= a < 2 * TWO_PI):
                        break
                circ = abs(((a - a_prev) + math.pi) % TWO_PI - math.pi)
                if ok and -TWO_PI <= a < 2 * TWO_PI and circ < math.radians(30.0):
                    keep.append([float(a % TWO_PI), n0])
            keep.sort(key=lambda t: t[0])
            dedup = []
            i = 0
            while i < len(keep):
                j = i
                while j + 1 < len(keep) and abs(keep[j + 1][0] - keep[i][0]) < 2e-4:
                    j += 1
                if j > i:
                    collapsed += j - i
                dedup.append(keep[i])
                i = j + 1
            track = dedup
            rec["tracked_count"] = len(track)
            rec["collapsed_pairs"] = collapsed
            tol = math.radians(0.15)
            matched = 0
            ghosts = 0
            for t in track:
                if not any(abs(((t[0] - a) + math.pi) % TWO_PI - math.pi) < tol for a, _ in roots):
                    ghosts += 1
            missed = []
            for a, n in roots:
                if any(abs(((a - t[0]) + math.pi) % TWO_PI - math.pi) < tol for t in track):
                    matched += 1
                else:
                    bb = r_o * math.sin(a) / f
                    missed.append((round(a, 4), round(float(abs(bb)), 3)))
            rec["matched"] = matched
            rec["ghosts"] = ghosts
            rec["missed"] = missed
        per_frame.append(rec)
    counts = [r["true_count"] for r in per_frame]
    events = sum(1 for i in range(1, len(counts)) if counts[i] != counts[i - 1])
    tracked = [r.get("tracked_count") for r in per_frame[1:]]
    matched = [r.get("matched") for r in per_frame[1:]]
    ghosts = [r.get("ghosts", 0) for r in per_frame[1:]]
    true_c = counts[1:]
    miss_b = [bb for r in per_frame[1:] for (_, bb) in r.get("missed", [])]
    miss_a = [a for r in per_frame[1:] for (a, _) in r.get("missed", [])]
    shadow_a = math.radians(shadow_deg)
    dist_edge = []
    for a in miss_a:
        d = min(abs(((a - (math.pi + shadow_a)) + math.pi) % TWO_PI - math.pi),
                abs(((a - (math.pi - shadow_a)) + math.pi) % TWO_PI - math.pi))
        dist_edge.append(math.degrees(d))
    wrong = [1 for tc, m, g in zip(true_c, matched, ghosts) if m < tc or g > 0]
    summary = {
        "r_o": r_o,
        "shadow_half_angle_deg": round(shadow_deg, 2),
        "true_count_min_max": [int(min(counts)), int(max(counts))],
        "count_changes_per_orbit": events,
        "frames_undercount_or_ghost": int(sum(wrong)),
        "frames_total_after_first": len(tracked),
        "mean_missing_when_wrong": round(float(np.mean([tc - m for tc, m in zip(true_c, matched) if m < tc])), 2)
        if wrong else 0.0,
        "max_missing": int(max((tc - m for tc, m in zip(true_c, matched)), default=0)),
        "total_ghost_instances": int(sum(ghosts)),
        "missed_image_b_stats": (round(float(np.min(miss_b)), 3), round(float(np.median(miss_b)), 3),
                                 round(float(np.max(miss_b)), 3)) if miss_b else None,
        "missed_b_below_crit_plus_1": (int(sum(1 for x in miss_b if x < BC + 1.0)), len(miss_b)) if miss_b else None,
        "missed_dist_to_shadow_deg_median": round(float(np.median(dist_edge)), 2) if dist_edge else None,
        "collapse_events": int(sum(r.get("collapsed_pairs", 0) for r in per_frame)),
        "per_frame_counts": counts,
    }
    return summary, per_frame


# ---------------------------------------------------------------- part C: flat, high beta
def flat_gather():
    rng = np.random.RandomState(7)
    N = 200
    pos = np.column_stack([rng.uniform(-45, 45, N), rng.uniform(-30, 30, N)])
    dirn = rng.normal(size=(N, 2))
    dirn /= np.linalg.norm(dirn, axis=1, keepdims=True)
    spd = rng.uniform(0.0, 0.01, N)
    vel = dirn * spd[:, None]
    frames = 120
    dt = 1.0 / 60.0
    tau_prev = None
    iters_all, fails, wrong = [], 0, 0
    for fr in range(frames):
        t = fr * dt
        x_o = np.array([math.log(math.cosh(1.5 + t)) - math.log(math.cosh(1.5)), 0.0])
        if fr == 0:
            tau_prev = t - np.linalg.norm(pos - x_o[None, :], axis=1)
            continue
        # truth by bisection on tau in [t-100, t]
        lo = np.full(N, t - 100.0)
        hi = np.full(N, t)

        def fl(tau):
            return np.linalg.norm(x_o[None, :] - (pos + vel * tau[:, None]), axis=1) - (t - tau)

        for _ in range(80):
            mid = 0.5 * (lo + hi)
            fm = fl(mid)
            lo = np.where(fm < 0, mid, lo)
            hi = np.where(fm >= 0, mid, hi)
        tau_true = 0.5 * (lo + hi)
        # Newton from previous frame
        tau = tau_prev.copy()
        used = np.zeros(N, int)
        ok = np.zeros(N, bool)
        for _ in range(12):
            xe = pos + vel * tau[:, None]
            d = x_o[None, :] - xe
            r = np.linalg.norm(d, axis=1)
            fv = r - (t - tau)
            nhat = d / r[:, None]
            dfv = -(nhat * vel).sum(1) + 1.0
            tau = tau - fv / dfv
            used += 1
            ok = np.abs(fv) < 1e-9
            if ok.all():
                break
        iters_all.extend(used.tolist())
        fails += int((~ok).sum())
        wrong += int((np.abs(tau - tau_true) > 1e-6).sum())
        tau_prev = tau.copy()
    beta0, beta1 = math.tanh(1.5), math.tanh(3.5)
    return {"beta_range": [round(beta0, 4), round(beta1, 4)],
            "frames": frames - 1, "emitters": N,
            "max_newton_iters": int(max(iters_all)),
            "mean_newton_iters": round(float(np.mean(iters_all)), 3),
            "nonconverged": fails, "wrong_roots": wrong}


# ---------------------------------------------------------------- part D: doc check
def band_banding(m=16):
    u0 = 2.0 ** (-2000.0 / m)          # arbitrary band-origin anchor
    rel_err = []
    for p in np.geomspace(20.0, 80.0, 200):
        u = 1.0 / p
        k = math.floor(math.log(u / u0) / math.log(2.0 ** (1.0 / m)))
        band_lo = u0 * 2.0 ** (k / m)
        band_hi = u0 * 2.0 ** ((k + 1) / m)
        u_k = math.sqrt(band_lo * band_hi)          # geometric centre
        g = lambda x: (1.0 - 6.0 * x) ** -0.5 - 1.0
        rel_err.append((g(u_k) - g(u)) / g(u))
    rel_err = np.array(rel_err)
    # analytic in-band spot checks at p=33 (circular orbit, M=1)
    spots = []
    p = 33.0
    u = 1.0 / p
    k = math.floor(math.log(u / u0) / math.log(2.0 ** (1.0 / m)))
    band_lo = u0 * 2.0 ** (k / m)
    band_hi = u0 * 2.0 ** ((k + 1) / m)
    invL2 = (p - 3.0) / (p * p)                    # circular: L^2 = p^2/(p-3)
    band_width = band_hi - band_lo
    for frac in (0.15, 0.5, 0.9):
        u_k = band_lo * (band_hi / band_lo) ** frac
        w2 = 1.0 - 6.0 * u_k
        u_c = (invL2 - 3.0 * u_k * u_k) / w2       # band centre of oscillation
        amp = abs(u - u_c)
        closed = ((1 - 6 * u_k) ** -0.5 - 1) / ((1 - 6 * u) ** -0.5 - 1) - 1
        spots.append({"band_frac": frac,
                      "u_k_over_u": round(u_k / u, 5),
                      "closed_form_rel_err": round(closed, 5),
                      "osc_amplitude_over_bandwidth": round(amp / band_width, 6)})
    return {"m": m,
            "sawtooth_min": round(float(rel_err.min()), 5),
            "sawtooth_max": round(float(rel_err.max()), 5),
            "predicted_amplitude": round(2.0 ** (1.0 / (2 * m)) - 1.0, 5),
            "spots": spots}


if __name__ == "__main__":
    print("== A controls ==")
    OUT["controls"] = controls()
    print(json.dumps(OUT["controls"], indent=1))
    print("== B gather scan ==")
    OUT["gather"] = []
    for r_o in (6.5, 10.0, 20.0, 40.0):
        s, frames = gather_scan(r_o)
        OUT["gather"].append(s)
        print(json.dumps({k: v for k, v in s.items() if k != "per_frame_counts"}, indent=1))
        print("counts:", s["per_frame_counts"])
    print("== C flat high-beta ==")
    OUT["flat_high_beta"] = flat_gather()
    print(json.dumps(OUT["flat_high_beta"], indent=1))
    print("== D band doc check ==")
    OUT["band_doc_check"] = band_banding()
    print(json.dumps(OUT["band_doc_check"], indent=1))
    with open("falsifier-results.json", "w") as fh:
        json.dump(OUT, fh, indent=1)
    print("saved falsifier-results.json")
