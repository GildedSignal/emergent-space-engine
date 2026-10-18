#!/usr/bin/env python3
"""Eclipse parity at game velocities — SECOND-AUTHOR FIX (run ...-9ffc).

Base: 20261018-0035-redteam-22d1's eclipse_parity.py (silver; the checker found the
W2/W2p ONSET instrument broken). This file keeps every wiring, arm and number of the
original, fixes exactly the two named defects, and certifies the fix:

FIX 1 (W2 sprite, onset scan): the retarded-time quadratic now uses the worldline's
  perpendicular offset d_perp (anchored at the perpendicular foot, P.v = 0), not the
  occluder's *current* distance |occ(t)| — the original was exact only at t_O = 0
  (where the Jaccard table sits, so that table was and stays exact).
FIX 2 (W2p per-row, onset scan): the row offset now uses the constant letter distance
  d_perp, not the time-varying |occ(t)|.

CERTIFICATES (independent of the fixed code path — closed-form algebra + bisection):
  C1  t_ret: quadratic vs 100-step bisection on |X(tau)| = t_O - tau over whole grids.
  C2  onsets: sub-grid bisection vs closed forms (centre row, transverse, exact):
        W1  = -R/beta
        W3  = d - R*sqrt(1+beta^2)/beta
        W2  = sqrt(d^2+R^2) - R/beta     -> W2-W3 -> (R/beta)(sqrt(1+beta^2)-1)
        W2p = d - R/beta                  (the letter: constant d)
  C3  arcs (t_O = 0, per row, transverse and oblique): each wiring's segment predicate
      equals the closed-form predicate row for row:
        W1  |sin(psi)| < R/d
        W3  sin(psi) in ( [-b(d^2-R^2) -+ R*sqrt(d^2-b^2(d^2-R^2))]/d^2 )  [transverse;
            general: d_perp^2 (sin(psi)+v_y)^2 < R^2 (1+beta^2+2 v.Ehat(psi))]
        W2  |sin(psi - psi_s)| < R/(gamma*d_perp), psi_s = bearing of X(-gamma*d_perp)
      half-angle(W2)/half-angle(W3) -> 1/gamma; centres -> -asin(beta);
      Jaccard(W2,W3) -> sqrt(1-beta^2).
  C4  the artifact: the original buggy W2 onset column is recomputed alongside and
      reported (it converged with W2p at 100R beta 0.9 — the tell).

Deterministic; ~20 s.
"""
import json
import math
import time as wall

import numpy as np

N = 10_000
WIRINGS = ("W1", "W2", "W2p", "W3")
OUT = {}


def perp_foot(occ0, v):
    """Foot of the perpendicular from the observer (origin) to the worldline, and d_perp."""
    occ0 = np.asarray(occ0, float)
    b2 = float(v @ v)
    if b2 == 0.0:
        return occ0, float(np.hypot(*occ0))
    p = occ0 - v * (float(occ0 @ v) / b2)
    return p, float(np.hypot(*p))


def lookback_quad(P, v):
    """Exact lookback time(s) tau <= 0 solving |P + v*tau| = -tau, where P is the
    occluder's position at the ARRIVAL time t_O (any P on the line; no foot needed).
    Returns tau = t_ret - t_O, vectorised over rows of P (M,2)."""
    P = np.atleast_2d(np.asarray(P, float))
    b2 = float(v @ v)
    if b2 == 0.0:
        return -np.hypot(P[:, 0], P[:, 1])
    pv = P @ v
    p2 = np.einsum("ij,ij->i", P, P)
    # roots of (b2-1) t^2 + 2 pv t + p2 = 0; disc = pv^2 + (1-b2) p2 >= 0 always.
    # retarded root (t <= 0 since sqrt >= |pv|):
    return (pv - np.sqrt(pv * pv + (1.0 - b2) * p2)) / (1.0 - b2)


def lookback_bisect(P, v, iters=100):
    """Independent solve of |P + v*tau| = -tau by bisection (vectorised over rows)."""
    P = np.atleast_2d(np.asarray(P, float))
    b = math.sqrt(float(v @ v))
    one_minus_b = max(1.0 - b, 1e-9)
    pn = np.hypot(P[:, 0], P[:, 1])
    # K with g(-K) = |P - v K| - K <= pn + b K - K < 0 strictly
    K = pn / one_minus_b + 10.0
    lo = -K
    hi = 0.0 * K
    glo = np.hypot(P[:, 0] - v[0] * K, P[:, 1] - v[1] * K) - K   # < 0
    ghi = pn                                                  # > 0 (d > 0)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        g = np.hypot(P[:, 0] + v[0] * mid, P[:, 1] + v[1] * mid) + mid
        neg = g < 0.0
        lo = np.where(neg, mid, lo)
        hi = np.where(neg, hi, mid)
    return 0.5 * (lo + hi), bool(np.all(glo < 0) and np.all(ghi >= 0))


def min_dist(L, psi, t_O, occ_t, v, wiring):
    """Min distance from each emitter's retarded null segment to the occluder, exact.
    Segment: u*E (u=1 at the observer), light time t = t_O - u L."""
    E = L * np.stack([np.cos(psi), np.sin(psi)], axis=-1)           # (n,2)
    if wiring == "W3":
        anchor, vv = np.asarray(occ_t).reshape(1, 2), v
    elif wiring == "W1":
        anchor, vv = np.asarray(occ_t).reshape(1, 2), np.zeros(2)
    elif wiring == "W2":
        # exact sprite: retarded point of the worldline through occ_t (FIX 1: exact
        # general quadratic in lookback time, any line direction, any t_O)
        P = np.asarray(occ_t, float).reshape(1, 2)
        tr = float(lookback_quad(P, v)[0])
        anchor = P + v * tr
        vv = np.zeros(2)
    elif wiring == "W2p":
        p, d_perp = perp_foot(occ_t, v)
        anchor = np.asarray(occ_t) - np.outer(d_perp * np.cos(psi), v)  # letter: const d
        vv = np.zeros(2)
    else:
        raise ValueError(wiring)
    A = E + L * vv                                                   # (n,2)
    B = np.broadcast_to(anchor, (len(psi), 2))
    aa = np.einsum("ij,ij->i", A, A)
    ab = np.einsum("ij,ij->i", A, B)
    u = np.clip(ab / aa, 0.0, 1.0)
    diff = u[:, None] * A - B
    return np.sqrt(np.einsum("ij,ij->i", diff, diff))


def min_dist_vs_t(L, psi, t_grid, occ_path, v, wiring, d_perp=None):
    """min_dist over a time grid for a small psi set, vectorised over t."""
    occ = np.array([occ_path(t) for t in t_grid])                   # (M,2)
    E = L * np.stack([np.cos(psi), np.sin(psi)], axis=-1)           # (P,2)
    if d_perp is None:
        _, d_perp = perp_foot(occ[0], v)
    if wiring == "W3":
        anchor, vv = occ[:, None, :], v
    elif wiring == "W1":
        anchor, vv = occ[:, None, :], np.zeros(2)
    elif wiring == "W2":
        lb = lookback_quad(occ, v)                                  # (M,) FIX 1
        anchor = (occ + lb[:, None] * v[None, :])[:, None, :]
        vv = np.zeros(2)
    elif wiring == "W2p":
        dt = d_perp * np.cos(psi)[None, :]                          # (M,P) FIX 2: const d
        anchor = occ[:, None, :] - dt[:, :, None] * v[None, None, :]
        vv = np.zeros(2)
    else:
        raise ValueError(wiring)
    A = E + L * vv                                                  # (P,2)
    aa = np.einsum("pj,pj->p", A, A)
    ab = np.einsum("mpj,pj->mp", anchor, A)
    u = np.clip(ab / aa[None, :], 0.0, 1.0)
    diff = u[:, :, None] * A[None, :, :] - anchor
    return np.sqrt(np.einsum("mpj,mpj->mp", diff, diff))


def jaccard(a, b):
    union = np.logical_or(a, b).sum()
    return 1.0 if union == 0 else np.logical_and(a, b).sum() / union


def onset(tgrid, mind, R):
    idx = np.nonzero(mind < R)[0]
    return float(tgrid[idx[0]]) if len(idx) else None


def onset_refined(L, psi0, tgrid, occ_path, v, wiring, R, d_perp):
    """Sub-grid onset by bisection on the wiring's own min-dist (60 iterations)."""
    one = np.array([psi0])

    def f(t):
        return float(min_dist_vs_t(L, one, np.array([t]), occ_path, v, wiring,
                                   d_perp=d_perp)[0, 0])
    md = min_dist_vs_t(L, one, tgrid, occ_path, v, wiring, d_perp=d_perp)[:, 0]
    idx = np.nonzero(md < R)[0]
    if len(idx) == 0:
        return None
    k = idx[0]
    if k == 0:
        return float(tgrid[0])
    lo, hi = float(tgrid[k - 1]), float(tgrid[k])   # f(lo) >= R > f(hi)
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if f(mid) < R:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def arm_a():
    print("=== Arm A: moving occluder, no mass (transverse) — FIXED onset instrument ===")
    L_E = 1e4
    psi = np.arange(N) * (2 * math.pi / N)
    rows, cert = [], []
    for d_over_R in (2.0, 10.0, 100.0):
        R, d = 1.0, d_over_R
        for beta in (1e-4, 0.1, 0.5, 0.9):
            v = np.array([0.0, beta])
            occ = lambda t: (d, beta * t)
            ver = {w: min_dist(L_E, psi, 0.0, occ(0.0), v, w) < R for w in WIRINGS}
            n3 = int(ver["W3"].sum())
            row = dict(d_over_R=d_over_R, beta=beta, n_occ_W3=n3, frac_W3=n3 / N,
                       jac_W1=jaccard(ver["W1"], ver["W3"]),
                       jac_W2=jaccard(ver["W2"], ver["W3"]),
                       jac_W2p=jaccard(ver["W2p"], ver["W3"]),
                       n_flip_W1=int((ver["W1"] != ver["W3"]).sum()))
            span = max(8.0 * R / max(beta, 1e-6) + 4.0 * d + 50.0, 20.0)
            tgrid = np.linspace(-span, span, 200_001)
            p, d_perp = perp_foot(occ(0.0), v)
            on, onr = {}, {}
            for w in WIRINGS:
                mdt = min_dist_vs_t(L_E, np.array([0.0]), tgrid, occ, v, w,
                                    d_perp=d_perp)[:, 0]
                on[w] = onset(tgrid, mdt, R)
                onr[w] = onset_refined(L_E, 0.0, tgrid, occ, v, w, R, d_perp)
            # C4: the artifact column — the ORIGINAL buggy W2 (current-distance quad,
            # expressed in lookback time: |occ(t)|^2 where d_perp^2 belongs)
            b2 = float(v @ v)
            tO2 = tgrid * tgrid
            r2 = d * d + b2 * tO2                       # |occ(t)|^2 along the path
            # faithful replication of the original onset wiring (grid quadratic):
            t_ret_bug = (tgrid - np.sqrt(b2 * tO2 + (1 - b2) * r2)) / (1 - b2) \
                if b2 > 0 else tgrid - d
            A = np.array([L_E, 0.0])
            anchor = np.stack([d + v[0] * t_ret_bug, v[1] * t_ret_bug], -1)
            ab = anchor @ A
            u = np.clip(ab / float(A @ A), 0.0, 1.0)
            diff = u[:, None] * A[None, :] - anchor
            md_bug = np.sqrt(np.einsum("ij,ij->i", diff, diff))
            on_bug = onset(tgrid, md_bug, R)
            # C1: quad vs bisection over the whole grid (lookback, per grid row)
            occ_arr = np.array([occ(t) for t in tgrid])
            tr_q = lookback_quad(occ_arr, v)
            tr_b, bracket_ok = lookback_bisect(occ_arr, v)
            c1 = float(np.max(np.abs(tr_q - tr_b)))
            # C2: refined onsets vs closed forms
            cf = {"W1": -R / beta,
                  "W3": d - R * math.sqrt(1 + beta * beta) / beta,
                  "W2": math.sqrt(d * d + R * R) - R / beta,
                  "W2p": d - R / beta}
            row.update({f"on_{w}": on[w] for w in WIRINGS},
                       on_W2_buggy=on_bug,
                       dt_on_W1=on["W1"] - on["W3"],
                       dt_on_W2=on["W2"] - on["W3"],
                       dt_on_W2p=on["W2p"] - on["W3"],
                       dt_on_W2_refined=onr["W2"] - onr["W3"],
                       dt_on_W2p_refined=onr["W2p"] - onr["W3"],
                       artifact_W2_bug_minus_fix=on_bug - onr["W2"],
                       artifact_W2_bug_vs_W3=on_bug - onr["W3"])
            rows.append(row)
            cert.append(dict(d_over_R=d_over_R, beta=beta, c1_quad_vs_bisect=c1,
                             bracket_ok=bracket_ok,
                             c2_onset_minus_closed={w: onr[w] - cf[w] for w in WIRINGS}))
            fmt = lambda x: f"{x:+10.4f}s"
            print(f"d={d_over_R:6.0f}R beta={beta:7.4f}  nOcc(W3)={n3:5d} ({n3/N:6.2%})  "
                  f"Jac W1={row['jac_W1']:.3f} W2={row['jac_W2']:.3f} "
                  f"W2p={row['jac_W2p']:.4f}  dOnset W1={fmt(row['dt_on_W1'])} "
                  f"W2={fmt(row['dt_on_W2'])} W2p={fmt(row['dt_on_W2p'])}  "
                  f"buggyW2={fmt(on_bug - onr['W3'])}  c1={c1:.1e}")
    rim = {}
    for d_over_R in (2.0, 10.0):
        R, d, beta = 1.0, d_over_R, 0.5
        v = np.array([0.0, beta])
        psi_r = math.asin(R / d)
        span = 6.0 * R / beta + 2.0 * d + 10.0
        tgrid = np.linspace(-span, span, 200_001)
        p, d_perp = perp_foot((d, 0.0), v)
        ons = {}
        for w in WIRINGS:
            mdt = min_dist_vs_t(L_E, np.array([psi_r]), tgrid,
                                lambda t: (d, beta * t), v, w, d_perp=d_perp)[:, 0]
            ons[w] = onset(tgrid, mdt, R)
        rim[f"{d_over_R:.0f}R"] = {w: ons[w] - ons["W3"] for w in WIRINGS}
        print(f"  d={d_over_R:3.0f}R psi_rim={math.degrees(psi_r):5.2f}deg  rim onset err: "
              f"W1={ons['W1']-ons['W3']:+9.4f}s W2={ons['W2']-ons['W3']:+8.4f}s "
              f"W2p={ons['W2p']-ons['W3']:+.4f}s   (W2 centre-row bound "
              f"{(R/beta)*(math.sqrt(1+beta*beta)-1):.3f}s)")
    print("-- oblique arm (45 deg, held out), d=10R, now with the FIXED W2 --")
    obl = []
    for beta in (0.1, 0.5):
        R, d = 1.0, 10.0
        v = beta * np.array([math.cos(math.pi / 4), math.sin(math.pi / 4)])
        occ = lambda t: (d + v[0] * t, v[1] * t)  # centre crosses (d, 0) at t = 0
        ver = {w: min_dist(L_E, psi, 0.0, occ(0.0), v, w) < R for w in WIRINGS}
        obl.append(dict(beta=beta, n_occ=int(ver["W3"].sum()),
                        jac_W1=jaccard(ver["W1"], ver["W3"]),
                        jac_W2=jaccard(ver["W2"], ver["W3"]),
                        jac_W2p=jaccard(ver["W2p"], ver["W3"])))
        print(f"  beta={beta}: nOcc(W3)={int(ver['W3'].sum())}  Jac W1="
              f"{jaccard(ver['W1'], ver['W3']):.3f}  W2={jaccard(ver['W2'], ver['W3']):.4f}"
              f"  W2p={jaccard(ver['W2p'], ver['W3']):.4f}")
    return dict(L_E=L_E, rows=rows, rim=rim, oblique=obl, certificates=cert)


def arm_arc():
    """Certificate C3: the t_O = 0 arcs vs closed forms, per row (transverse + oblique)."""
    print("=== Arm ARC: arc geometry vs closed form; the 1/gamma mechanism ===")
    L_E = 1e4
    psi = np.arange(N) * (2 * math.pi / N)
    s = np.sin(psi)
    out = []
    for d_over_R in (2.0, 10.0, 100.0):
        R, d = 1.0, d_over_R
        for beta in (0.1, 0.5, 0.9):
            v = np.array([0.0, beta])
            occ0 = (d, 0.0)
            # closed forms (exact, transverse)
            disc = d * d - beta * beta * (d * d - R * R)
            lo3 = (-beta * (d * d - R * R) - R * math.sqrt(disc)) / (d * d)
            hi3 = (-beta * (d * d - R * R) + R * math.sqrt(disc)) / (d * d)
            # one-sided: the segment points at the +x half-plane (cos(psi) >= 0);
            # the bare sin-intervals are the infinite-line (two-sided) tests
            cos_pos = np.cos(psi) >= 0.0
            cf3 = (s > lo3) & (s < hi3) & cos_pos
            cf1 = (np.abs(s) < R / d) & (np.cos(psi) >= 0.0)
            gam = 1.0 / math.sqrt(1 - beta * beta)
            psi_s = -math.asin(beta)
            cf2 = (np.abs(np.sin(psi - psi_s)) < R / (gam * d)) & (np.cos(psi - psi_s) >= 0)
            code = {w: min_dist(L_E, psi, 0.0, occ0, v, w) < R for w in WIRINGS}
            mism = {w: int((code[w] != cf).sum()) for w, cf in
                    (("W1", cf1), ("W2", cf2), ("W3", cf3))}

            def arc_geo(mask):
                """wrap-safe centre and half-width (deg) of a contiguous arc < 180 deg."""
                idx = np.nonzero(mask)[0]
                a = psi[idx]
                z = np.exp(1j * a).mean()
                centre = math.atan2(z.imag, z.real)
                dev = (a - centre + math.pi) % (2 * math.pi) - math.pi
                return (math.degrees(centre),
                        0.5 * math.degrees(dev.max() - dev.min()),
                        dev.max() - dev.min())

            c1d, w1h, _ = arc_geo(code["W1"])
            c3d, w3h, _ = arc_geo(code["W3"])
            c2d, w2h, _ = arc_geo(code["W2"])
            row = dict(d_over_R=d_over_R, beta=beta, mismatches=mism,
                       centre_W1_deg=c1d, centre_W3_deg=c3d, centre_W2_deg=c2d,
                       minus_asinbeta_deg=-math.degrees(math.asin(beta)),
                       half_W1=w1h, half_W2=w2h, half_W3=w3h,
                       one_over_gamma=1 / gam,
                       jac_W2=jaccard(code["W2"], code["W3"]),
                       jac_W1=jaccard(code["W1"], code["W3"]),
                       sqrt_1_minus_beta2=math.sqrt(1 - beta * beta),
                       n_W3=int(code["W3"].sum()), n_W2=int(code["W2"].sum()))
            row["ratio_W2_W3"] = row["half_W2"] / row["half_W3"]
            out.append(row)
            print(f"d={d_over_R:3.0f}R beta={beta:.1f}: mismatch rows {mism['W1']}/"
                  f"{mism['W2']}/{mism['W3']}  centre W3={c3d:+7.3f} "
                  f"W2={c2d:+7.3f} (-asin b={-math.degrees(math.asin(beta)):+.3f})"
                  f"  half W3={w3h:.3f} W2={w2h:.3f}  ratio={row['ratio_W2_W3']:.4f}"
                  f"  1/gamma={1/gam:.4f}  Jac(W2,W3)={row['jac_W2']:.4f}  "
                  f"sqrt(1-b^2)={row['sqrt_1_minus_beta2']:.4f}")
    print("-- oblique closed-form certificate (45 deg, d=10R) --")
    oblo = []
    for beta in (0.1, 0.5):
        R, d = 1.0, 10.0
        v = beta * np.array([math.cos(math.pi / 4), math.sin(math.pi / 4)])
        occ0 = (d, 0.0)
        p, d_perp = perp_foot(occ0, v)
        Ehat = np.stack([np.cos(psi), np.sin(psi)], -1)
        # exact W3 predicate: D2(w) = |w(Ehat+v) - occ0|^2 (the occluder at time -w is
        # occ0 - w v), so the anchor is occ0 at its frame-time distance d, NOT the
        # perpendicular foot: occluded iff d^2 (sin(psi)+v_y)^2 < R^2 (1+beta^2+2 v.Ehat)
        # one-sided: the grazing point is on the ray iff (Ehat+v).occ0 >= 0, i.e.
        # cos(psi)+v_x >= 0
        cos_pos = np.cos(psi) + v[0] >= 0.0
        cf3 = (d ** 2 * (s + v[1]) ** 2
               < R ** 2 * (1 + float(v @ v) + 2 * (Ehat @ v))) & cos_pos
        gam = 1.0 / math.sqrt(1 - beta * beta)
        lb0 = float(lookback_quad(np.asarray(occ0, float).reshape(1, 2), v)[0])
        A_s = np.asarray(occ0, float) + v * lb0
        d_s = float(np.hypot(*A_s))          # = -lb0 exactly (light time = distance)
        psi_s = math.atan2(A_s[1], A_s[0])
        cf2 = (np.abs(np.sin(psi - psi_s)) < R / d_s) & (np.cos(psi - psi_s) >= 0)
        cf1 = (np.abs(s) < R / d) & (np.cos(psi) >= 0.0)
        code = {w: min_dist(L_E, psi, 0.0, occ0, v, w) < R for w in WIRINGS}
        mism = {w: int((code[w] != cf).sum()) for w, cf in
                (("W1", cf1), ("W2", cf2), ("W3", cf3))}
        oblo.append(dict(beta=beta, d_perp=d_perp, sprite_dist=d_s,
                         sprite_lighttime=-lb0, gamma_d_perp=gam * d_perp,
                         psi_s_deg=math.degrees(psi_s), mismatches=mism,
                         jac_W1=jaccard(code["W1"], code["W3"]),
                         jac_W2=jaccard(code["W2"], code["W3"]),
                         jac_W2p=jaccard(code["W2p"], code["W3"])))
        print(f"  beta={beta}: d_perp={d_perp:.4f}  sprite dist={d_s:.4f} "
              f"(gamma*d_perp={gam*d_perp:.4f})  mismatches {mism['W1']}/{mism['W2']}/"
              f"{mism['W3']}  Jac W2={jaccard(code['W2'], code['W3']):.4f}")
    return dict(transverse=out, oblique=oblo)


def arm_observer():
    """Observer at beta_O = 0.5: aberrated arcs and coordinate-arc parity error."""
    print("=== Arm O: observer beta_O = 0.5, d = 2R, occluder static ===")
    L_E = 1e4
    R, d = 1.0, 2.0
    psi = np.arange(N) * (2 * math.pi / N)
    out = {}
    for label, bO in (("approach(+x toward occluder)", +0.5), ("recede", -0.5)):
        E = L_E * np.stack([np.cos(psi), np.sin(psi)], axis=-1)
        look = E / np.linalg.norm(E, axis=-1)[:, None]
        occ_xy = np.array([d, 0.0])
        aa = np.einsum("ij,ij->i", E, E)
        ab = np.einsum("ij,ij->i", E, np.broadcast_to(occ_xy, (N, 2)))
        u = np.clip(ab / aa, 0.0, 1.0)
        diff = u[:, None] * E - occ_xy
        occ_true = np.linalg.norm(diff, axis=-1) < R
        ang_coord = np.degrees(np.arctan2(look[:, 1], look[:, 0])) % 360.0
        g = 1.0 / math.sqrt(1 - bO * bO)
        nx, ny = look[:, 0], look[:, 1]
        npx = (nx + bO) / (1.0 + bO * nx)            # look dir into the +bO x frame
        npy = ny / (g * (1.0 + bO * nx))
        ang_obs = np.degrees(np.arctan2(npy, npx)) % 360.0

        def halfarc(ang, mask):
            a = ang[mask]
            z = np.exp(1j * np.radians(a)).mean()
            centre = math.degrees(math.atan2(z.imag, z.real)) % 360.0
            dev = (a - centre + 180.0) % 360.0 - 180.0
            return 0.5 * (dev.max() - dev.min()), centre
        h_obs, _ = halfarc(ang_obs, occ_true)
        h_coord, c_coord = halfarc(ang_coord, occ_true)
        occ_wrong = np.abs((ang_coord - c_coord + 180.0) % 360.0 - 180.0) < h_coord
        mis = int((occ_wrong != occ_true).sum())
        arc_err = abs(h_obs - 30.0) / 30.0
        out[label] = dict(half_arc_obs_deg=h_obs, half_arc_coord_deg=h_coord,
                          arc_size_error=arc_err, misclassified=mis, frac=mis / N,
                          n_occ=int(occ_true.sum()))
        print(f"  {label}: half-arc observer-frame {h_obs:.2f} deg, coordinate-frame "
              f"{h_coord:.2f} deg (static 30.00; arc-size error {arc_err:.1%}); "
              f"coordinate-arc row parity misclassifies {mis} rows ({mis/N:.3%})")
    return out


def shapiro(b, r_E, r_O, M):
    return 2.0 * M * math.log(4.0 * r_E * r_O / (b * b))


def arm_b():
    print("=== Arm B: differential Shapiro delay across a strong-field transit ===")
    M = 1.0
    r_O, R_p = 20.0 * M, 1.0 * M
    E = 100.0 * M * np.array([math.cos(2.5), math.sin(2.5)])
    Opos = np.array([r_O, 0.0])
    seg = Opos - E
    Lseg = float(np.linalg.norm(seg))
    udir = seg / Lseg
    b_ray = abs(float(np.cross(E, udir)))
    r_E = float(np.linalg.norm(E))
    s = np.linspace(0.0, Lseg, 2_000_001)
    pts = E[None, :] + s[:, None] * udir[None, :]
    r = np.linalg.norm(pts, axis=1)
    quad = 2.0 * M * float(np.sum(1.0 / r)) * (Lseg / (len(s) - 1))
    logf = shapiro(b_ray, r_E, r_O, M)
    exact = 2.0 * M * math.log(((r_E + math.sqrt(r_E ** 2 - b_ray ** 2))
                                * (r_O + math.sqrt(r_O ** 2 - b_ray ** 2))) / b_ray ** 2)
    print(f"  b_ray={b_ray:.2f}M: delay quad={quad:.4f}s  log={logf:.4f}s  "
          f"exact={exact:.4f}s  (log vs quad {abs(logf-quad)/quad:.2%})")
    diff_limb = (shapiro(b_ray + R_p, r_E, r_O, M) - shapiro(b_ray - R_p, r_E, r_O, M))
    rows = {}
    for beta in (1e-4, 0.5):
        dur = 2.0 * R_p / beta
        rows[f"beta{beta}"] = dict(duration=dur, diff_limb=abs(diff_limb),
                                   rel=abs(diff_limb) / dur, w1_error=2.0 * R_p,
                                   naive=logf)
        print(f"  beta={beta:7.4f}: transit {dur:10.2f}s | sprite-consistent differential "
              f"{abs(diff_limb):.4f}s ({abs(diff_limb)/dur:.3%}) | W1 error d/c = "
              f"{2.0*R_p:.1f}s | naive no-cancel delay {logf:.2f}s (not the observable)")
    return dict(M=M, r_O=r_O, R_p=R_p, b_ray=b_ray, shapiro_quad=quad, shapiro_log=logf,
                shapiro_exact=exact, rel_err_log_vs_quad=abs(logf - quad) / quad,
                diff_limb=abs(diff_limb), rows=rows)


def price():
    print("=== Price: exact W3 per row (vectorised; order of magnitude, shared x86) ===")
    L_E = 1e4
    psi = np.arange(100_000) * (2 * math.pi / 100_000)
    v = np.array([0.0, 0.5])
    reps = 20
    t0 = wall.perf_counter()
    for _ in range(reps):
        min_dist(L_E, psi, 0.0, (10.0, 0.0), v, "W3")
    dt = (wall.perf_counter() - t0) / reps
    print(f"  100k rows: {dt*1e3:.2f} ms/pass -> {dt*1e9/100_000:.0f} ns/row "
          f"(numpy one-off overhead included)")
    return dict(ms_per_100k=dt * 1e3, ns_per_row=dt * 1e9 / 100_000)


def main():
    OUT["arm_a"] = arm_a()
    OUT["arm_arc"] = arm_arc()
    OUT["arm_observer"] = arm_observer()
    OUT["arm_b"] = arm_b()
    OUT["price"] = price()
    with open(__file__.replace(".py", "-out.json"), "w") as f:
        json.dump(OUT, f, indent=1)
    print("wrote", __file__.replace(".py", "-out.json"))


if __name__ == "__main__":
    main()
