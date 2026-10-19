#!/usr/bin/env python3
"""r11 eclipse-aggregate rung instrument (fresh code, second author on c78d).

The exact law (22d1): observer O at origin; planet disc centre C, R_p = 1, static;
rigid fleet behind it at depth ~25 moving +x at beta (c = 1). Per sample point: past
light-cone root -> retarded position -> segment(retarded -> O) vs disc predicate ->
SR k^4 weight.  f = 1 - sum(w * occluded)/sum(w).

Readouts judged against the exact truth:
  one-sample  the letter L59 first clause: the representative point's own predicate;
  pixel-h*    the letter's second clause as cure: the same exact law evaluated once per
              pixel of a pitch-h grid covering the fleet support (pixel weight x k^4);
  overlap     circle-circle lens closed form (uniform disc, beta = 0 only).

Note (disclosed instrument fix): c78d's beta arm weights k^4 = 1/(gamma(1 + beta^2
px/q)) — a doppler with beta counted twice; exact SR is k = 1/(gamma(1 - v.n)) =
1/(gamma(1 + beta px/q)), used on BOTH paths here. Beta-arm minima move ~1pp
(sky 0.8150 -> 0.7999); every c78d conclusion is geometric and unaffected.
Two independent code paths:
  author  quadratic light-cone root + clipped-parameter segment distance (inline);
  check   monotone bisection on phi(te) = t - te - |P(te)| + a 3-case segment distance
          (endpoint / endpoint / perpendicular), gamma-beta k^4 by explicit dot product.

Usage:
  eclipse_rung.py <config>            one JSON line: the config's five rung metrics
  eclipse_rung.py --check             metrics-check.json (bisection path, all configs)
  eclipse_rung.py --diagnostics       diagnostics.json (beta 0.9, R_f 10/30, arc shape)

No code reused from c78d's occlusion.py; the physics is shared by definition.
Deterministic: seed 20261019. float64. O(points) memory per step.
"""
import json
import math
import sys

import numpy as np

RP = 1.0
CY = 20.0          # planet centre distance (transit: (0, CY); sky: (0, CY, 0))
DEPTH = 25.0       # fleet plane depth
SEED = 20261019
N_TRUTH_BETA = 20_000
N_TRUTH_STATIC = 100_000
BETA = 0.5         # the frozen criteria case ("player beta" per the page's fix)
RF = 3.0           # frozen fleet radius (R_p units)
TSTEPS = 1201
USTEPS = 401


# ---------------------------------------------------------------- fleet point sets

def disc_points(n, r, rng):
    ang = rng.uniform(-np.pi, np.pi, n)
    rad = np.sqrt(rng.uniform(0.0, 1.0, n)) * r
    return np.column_stack((rad * np.cos(ang), rad * np.sin(ang)))


def arc_points(n, rng, r_arc=3.0, half_ang=np.pi / 6, half_w=0.15):
    """taleb-09b5's formation: n ships on a 60-degree arc at radius 3, radial width 0.3."""
    th = rng.uniform(-half_ang, half_ang, n)
    rr = r_arc + rng.uniform(-half_w, half_w, n)
    return np.column_stack((rr * np.cos(th), rr * np.sin(th)))


# ---------------------------------------------------------------- the exact law, author path

def retarded_quad(x0, y0, z0, t, beta):
    """Past root of |P(te)| = t - te via the quadratic."""
    a = beta * beta - 1.0
    b = 2.0 * (beta * x0 + t)
    c = x0 * x0 + y0 * y0 + z0 * z0 - t * t
    sq = np.sqrt(np.maximum(b * b - 4.0 * a * c, 0.0))
    lo, hi = (-b - sq) / (2.0 * a), (-b + sq) / (2.0 * a)
    near = t - np.sqrt(x0 * x0 + y0 * y0 + z0 * z0)
    return np.where(np.abs(lo - near) < np.abs(hi - near), lo, hi)


def behind_clip(px, py, pz):
    """Segment(P -> O) vs disc(C, RP): closest-point parameter clipped (author path)."""
    u = np.clip((py * CY) / (px * px + py * py + pz * pz), 0.0, 1.0)
    d = np.sqrt((u * px) ** 2 + (u * py - CY) ** 2 + (u * pz) ** 2)
    return d < RP


def beta_fs_author(x0, y0, z0, ts, beta):
    gam = 1.0 / math.sqrt(1.0 - beta * beta)
    fs = np.empty(len(ts))
    for i, t in enumerate(ts):
        te = retarded_quad(x0, y0, z0, t, beta)
        px, py, pz = x0 + beta * te, y0, z0
        occl = behind_clip(px, py, pz)
        q = np.sqrt(px * px + py * py + pz * pz)
        w = (1.0 / (gam * (1.0 + beta * px / q))) ** 4   # SR doppler: 1/(g(1 - v.n)), v.n = -beta*px/q
        fs[i] = 1.0 - w[occl].sum() / w.sum()
    return fs


# ---------------------------------------------------------------- the exact law, check path

def retarded_bisect(x0, y0, z0, t, beta, iters=44):
    """phi(te) = t - te - |P(te)| is strictly decreasing (d phi/d te in (-1-beta, -1+beta)
    < 0 for beta < 1), so the past root is unique; bisect [t - D, t] with phi > 0 at the
    left end, D chosen so D(1-beta) > |x0|+|y0|+|z0| + beta|t| + 1 (guaranteed)."""
    D = (np.abs(x0) + np.abs(y0) + np.abs(z0) + beta * abs(t) + 2.0) / (1.0 - beta)
    lo, hi = t - D, t + 0.0
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        pm = np.sqrt((x0 + beta * mid) ** 2 + y0 * y0 + z0 * z0)
        left = (t - mid) - pm > 0.0
        lo, hi = np.where(left, mid, lo), np.where(left, hi, mid)
    return 0.5 * (lo + hi)


def behind_cases(px, py, pz):
    """Same predicate by explicit 3-case split: s* = (P.C)/|P|^2 in [0,1] is the foot;
    s* <= 0 -> nearest endpoint O (d = |C|); s* >= 1 -> nearest endpoint P; else the
    perpendicular distance sqrt(|C|^2 - (P.C)^2/|P|^2)."""
    q2 = px * px + py * py + pz * pz
    pc = py * CY
    s = pc / q2
    dO = CY                       # |C - O|
    dP = np.sqrt(px * px + (py - CY) ** 2 + pz * pz)
    dperp = np.sqrt(np.maximum(CY * CY - pc * pc / q2, 0.0))
    d = np.where(s <= 0.0, dO, np.where(s >= 1.0, dP, dperp))
    return d < RP


def beta_fs_check(x0, y0, z0, ts, beta):
    gam = 1.0 / math.sqrt(1.0 - beta * beta)
    fs = np.empty(len(ts))
    for i, t in enumerate(ts):
        te = retarded_bisect(x0, y0, z0, t, beta)
        px, py, pz = x0 + beta * te, y0, z0
        occl = behind_cases(px, py, pz)
        q = np.sqrt(px * px + py * py + pz * pz)
        vdotn = beta * (-px) / q          # v = (+beta x), n = -P/|P| (emitter -> observer)
        k = 1.0 / (gam * (1.0 - vdotn))
        w = k ** 4
        fs[i] = 1.0 - w[occl].sum() / w.sum()
    return fs


# ---------------------------------------------------------------- case plumbing (shared)

def worldlines(points2d, orientation):
    """Local fleet coords -> worldline offsets. transit: local (x, y) in the motion
    plane at depth DEPTH; sky: local (x, z), all at depth DEPTH."""
    x_c0 = -(RF + RP + 14.0)
    if orientation == "transit":
        return points2d[:, 0] + x_c0, points2d[:, 1] + DEPTH, np.zeros(len(points2d))
    return points2d[:, 0] + x_c0, np.full(len(points2d), DEPTH), points2d[:, 1].copy()


def seen_grid(beta):
    t_mid = (RF + RP + 14.0) / beta
    W = (RF + RP) / beta + 14.0 + 1.5 * beta * (DEPTH + RF)
    return np.linspace(t_mid - W, t_mid + W, TSTEPS)


def beta_fs(points2d, orientation, beta, path="author"):
    x0, y0, z0 = worldlines(points2d, orientation)
    ts = seen_grid(beta)
    fs = beta_fs_author(x0, y0, z0, ts, beta) if path == "author" else beta_fs_check(x0, y0, z0, ts, beta)
    return ts, fs


def static_truth_f(points2d, r_f, impact=0.0):
    """beta = 0: fleet swept along x behind the disc at the origin; exact per-ship truth."""
    span = RP + r_f + 0.5 * RP
    us = np.linspace(-span, span, USTEPS)
    fs = np.empty(USTEPS)
    for i, u in enumerate(us):
        fs[i] = 1.0 - (np.hypot(points2d[:, 0] + u, points2d[:, 1] + impact) < RP).mean()
    return us, fs


def lens_area(d, r1, r2):
    if d >= r1 + r2:
        return 0.0
    if d <= abs(r1 - r2):
        return math.pi * min(r1, r2) ** 2
    a1 = math.acos((d * d + r1 * r1 - r2 * r2) / (2 * d * r1))
    a2 = math.acos((d * d + r2 * r2 - r1 * r1) / (2 * d * r2))
    s = (-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2)
    return r1 * r1 * a1 + r2 * r2 * a2 - 0.5 * math.sqrt(s)


# ---------------------------------------------------------------- readouts / metrics

def pixel_support(r_f, h, shape="disc"):
    k = int(math.ceil(r_f / h)) + 1
    g = np.arange(-k, k + 1) * h
    mx, my = np.meshgrid(g, g)
    if shape == "disc":
        inside = mx * mx + my * my <= r_f * r_f
    else:  # the arc band: |rho - 3| <= 0.15, |theta| <= 30 deg
        inside = (np.abs(np.hypot(mx, my) - 3.0) <= 0.15) & (np.abs(np.arctan2(my, mx)) <= np.pi / 6)
    return np.column_stack((mx[inside], my[inside]))


def metrics_for(err, f_r, f_e, samples, r_f, h):
    return {
        "flux_err_p99": float(np.percentile(err, 99)),
        "fmin_abs_dev": float(abs(f_r.min() - f_e.min())),
        "false_blink_frac": float(((f_r <= 0.0) & (f_e > 0.5)).mean()),
        "samples": int(samples),
        "samples_over_bound": float(samples / (math.pi * (r_f / h) ** 2)),
    }


def worst(a, b):
    return {k: (max(a[k], b[k]) if isinstance(a[k], (int, float)) else a[k]) for k in a}


def run_config(name, path="author"):
    ships = disc_points(N_TRUTH_BETA, RF, np.random.default_rng(SEED))
    if name in ("pixel-h2", "pixel-h1"):
        h = 0.5 if name == "pixel-h2" else 1.0
        px = pixel_support(RF, h)
        ms = []
        for orient in ("transit", "sky"):
            _, f_e = beta_fs(ships, orient, BETA, path)
            _, f_r = beta_fs(px, orient, BETA, path)
            ms.append(metrics_for(np.abs(f_r - f_e), f_r, f_e, len(px), RF, h))
        return worst(*ms)
    if name == "one-sample":
        centre = np.zeros((1, 2))
        ms = []
        for orient in ("transit", "sky"):
            _, f_e = beta_fs(ships, orient, BETA, path)
            _, f_r = beta_fs(centre, orient, BETA, path)
            ms.append(metrics_for(np.abs(f_r - f_e), f_r, f_e, 1, RF, RF))
        return worst(*ms)
    if name == "overlap-disc":
        stat = disc_points(N_TRUTH_STATIC, RF, np.random.default_rng(SEED))
        us, f_e = static_truth_f(stat, RF)
        f_r = np.array([1.0 - lens_area(abs(u), RF, RP) / (math.pi * RF * RF) for u in us])
        return metrics_for(np.abs(f_r - f_e), f_r, f_e, 1, RF, RF)
    raise SystemExit(f"unknown config {name}")


# ---------------------------------------------------------------- diagnostics

def diagnostics():
    d = {"beta_arms": [], "static_scaling": [], "arc": {}}
    ships = disc_points(N_TRUTH_BETA, RF, np.random.default_rng(SEED))
    px = pixel_support(RF, 0.5)
    for beta in (0.5, 0.9):
        for orient in ("transit", "sky"):
            _, f_e = beta_fs(ships, orient, beta)
            _, f_r = beta_fs(px, orient, beta)
            _, f_1 = beta_fs(np.zeros((1, 2)), orient, beta)
            e1, er = np.abs(f_1 - f_e), np.abs(f_r - f_e)
            d["beta_arms"].append({
                "beta": beta, "orient": orient, "f_true_min": round(float(f_e.min()), 4),
                "onesample_peak_err": round(float(e1.max()), 4),
                "onesample_p99": round(float(np.percentile(e1, 99)), 4),
                "pixel_h2_p99": round(float(np.percentile(er, 99)), 4),
                "pixel_h2_fmin_dev": round(float(abs(f_r.min() - f_e.min())), 4),
                "pixel_h2_blink_frac": round(float(((f_r <= 0.0) & (f_e > 0.5)).mean()), 4),
            })
    for r_f in (3.0, 10.0, 30.0):
        stat = disc_points(N_TRUTH_STATIC, r_f, np.random.default_rng(SEED))
        us, f_e = static_truth_f(stat, r_f)
        pxa = pixel_support(r_f, 0.5)
        errs = [abs((1.0 - (np.hypot(pxa[:, 0] + u, pxa[:, 1]) < RP).mean()) - f_e[i])
                for i, u in enumerate(us)]
        d["static_scaling"].append({
            "r_f": r_f, "samples": int(len(pxa)),
            "bound_pi_rf2_over_h2": round(math.pi * (r_f / 0.5) ** 2, 1),
            "ratio": round(len(pxa) / (math.pi * (r_f / 0.5) ** 2), 3),
            "pixel_h2_p99": round(float(np.percentile(errs, 99)), 4),
            "pixel_h2_peak": round(float(np.max(errs)), 4),
        })
    arc = arc_points(400, np.random.default_rng(SEED))
    us = np.linspace(-4.5, 4.5, USTEPS)
    f_e = np.array([1.0 - (np.hypot(arc[:, 0] + u, arc[:, 1]) < RP).mean() for u in us])
    f_1 = np.array([0.0 if abs(u) < RP else 1.0 for u in us])
    d["arc"] = {
        "n_ships": 400,
        "f_true_min": round(float(f_e.min()), 4),
        "onesample_peak_err": round(float(np.abs(f_1 - f_e).max()), 4),
        "onesample_p99": round(float(np.percentile(np.abs(f_1 - f_e), 99)), 4),
        "readouts": [],
    }
    for h in (0.5, 0.15, 0.075):
        pxa = pixel_support(3.0, h, shape="arc")
        errs = [abs((1.0 - (np.hypot(pxa[:, 0] + u, pxa[:, 1]) < RP).mean()) - f_e[i])
                for i, u in enumerate(us)]
        d["arc"]["readouts"].append({
            "h": h, "samples": int(len(pxa)),
            "pixel_p99": round(float(np.percentile(errs, 99)), 4),
            "pixel_peak": round(float(np.max(errs)), 4),
        })
    return d


def main(argv):
    if "--diagnostics" in argv:
        json.dump(diagnostics(), open("diagnostics.json", "w"), indent=1)
        print("diagnostics.json written")
        return 0
    if "--check" in argv:
        out = {c: run_config(c, path="check") for c in ("pixel-h2", "pixel-h1", "one-sample", "overlap-disc")}
        json.dump(out, open("metrics-check.json", "w"), indent=1)
        print(json.dumps(out))
        return 0
    print(json.dumps({argv[0]: run_config(argv[0])}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
