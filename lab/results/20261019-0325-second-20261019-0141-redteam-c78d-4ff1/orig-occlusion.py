#!/usr/bin/env python3
"""The aggregate occlusion falsifier — representation.md L59 'Aggregates are one sample
each' under eclipse, the spatial-extent channel (1885's dispersion channel is orthogonal:
this fails at beta = 0 exactly).

Exact instrument, float64:
- static arms: uniform-disc fleets (N = 1e5, seed 20261019), exact behind-disc predicate,
  closed-form circle-circle overlap as cross-check (P9);
- one-sample rules: centre sample, and median over 20 random-member samples;
- pixel arm: the same L59 line's 'one sample per pixel' cap as the cure, priced;
- relativistic arm: beta 0.5 transverse behind the planet, exact per-ship retarded time
  (quadratic, past root) + segment-vs-disc predicate (22d1's law) + exact SR k^4 weights.

Occluded flux fraction f = (flux remaining)/(total flux). All lengths in R_p = 1.
"""
import json
import math
import sys

import numpy as np

R_P = 1.0
SEED = 20261019
N_STATIC = 100_000
N_BETA = 20_000


def fleet(n: int, r_f: float, rng: np.random.Generator) -> np.ndarray:
    """Uniform points in a disc of radius r_f (local frame)."""
    r = np.sqrt(rng.random(n)) * r_f
    a = rng.random(n) * 2.0 * np.pi
    return np.stack([r * np.cos(a), r * np.sin(a)], axis=1)


def overlap_area(d: float, r1: float, r2: float) -> float:
    """Circle-circle lens overlap area (exact closed form)."""
    if d >= r1 + r2:
        return 0.0
    if d <= abs(r1 - r2):
        return math.pi * min(r1, r2) ** 2
    t1 = (d * d + r1 * r1 - r2 * r2) / (2 * d * r1)
    t2 = (d * d + r2 * r2 - r1 * r1) / (2 * d * r2)
    t3 = (-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2)
    return r1 * r1 * math.acos(t1) + r2 * r2 * math.acos(t2) - 0.5 * math.sqrt(t3)


def static_arm(r_f: float, impact: float, label: str, out: dict) -> dict:
    """Fleet centre sweeps (u, impact); ships at local + centre; k = 1 (beta = 0)."""
    rng = np.random.default_rng(SEED)
    ships = fleet(N_STATIC, r_f, rng)
    span = R_P + r_f + 0.5 * R_P
    u = np.linspace(-span, span, 401)
    centre = np.stack([u, np.full_like(u, impact)], axis=1)
    # f_true per step: fraction of ships NOT behind the planet disc.
    abs_pos = ships[None, :, :] + centre[:, None, :]          # (T, N, 2)
    behind = np.hypot(abs_pos[..., 0], abs_pos[..., 1]) < R_P  # (T, N)
    f_true = 1.0 - behind.mean(axis=1)
    f_1c = 1.0 - (np.hypot(centre[:, 0], centre[:, 1]) < R_P).astype(float)
    # closed form cross-check (uniform disc): occluded fraction = overlap / fleet area.
    s = np.hypot(u, impact)
    f_cf = 1.0 - np.array([overlap_area(d, r_f, R_P) for d in s]) / (math.pi * r_f**2)
    cf_max_dev = float(np.max(np.abs(f_true - f_cf)))
    # random-member samples
    members = rng.choice(N_STATIC, size=20, replace=False)
    f_1m = 1.0 - behind[:, members].astype(float)              # (T, 20)
    err_m = np.abs(f_1m - f_true[:, None]).mean(axis=1)        # mean over draws, per step
    mid = int(np.argmin(np.hypot(centre[:, 0], centre[:, 1])))
    err_c = np.abs(f_1c - f_true)
    blink = (f_1c == 0.0) & (f_true > 0.5)
    row = {
        "config": label,
        "r_f_over_r_p": r_f,
        "impact": impact,
        "peak_err_centre": float(err_c.max()),
        "err_at_mid": float(err_c[mid]),
        "f1_at_mid": float(f_1c[mid]),
        "f_true_at_mid": float(f_true[mid]),
        "f_true_min": float(f_true.min()),
        "f1_min": float(f_1c.min()),
        "frac_time_err_gt5": float((err_c > 0.05).mean()),
        "frac_time_total_blink_true_gt_half": float(blink.mean()),
        "err_gt80_window_path": float(2 * span * (err_c > 0.80).mean()),
        "peak_err_randmember_meanpath": float(err_m.max()),
        "err_at_mid_randmember": float(np.median(np.abs(f_1m[mid] - f_true[mid]))),
        "cf_crosscheck_max_dev": cf_max_dev,
        "u": u.tolist(),
        "f_true": f_true.tolist(),
        "f_1c": f_1c.tolist(),
    }
    out["arms"].append(row)
    return row


def pixel_arm(r_f: float, h: float, label: str, out: dict) -> dict:
    """The same line's cure: one sample per PIXEL. Ship occluded iff its pixel's centre is
    behind the disc. Error vs exact; price = pixels covering the fleet."""
    rng = np.random.default_rng(SEED)
    ships = fleet(N_STATIC, r_f, rng)
    # local grid of pixel centres covering the fleet disc
    k = int(math.ceil(r_f / h))
    gx = np.arange(-k, k + 1) * h
    gy = np.arange(-k, k + 1) * h
    px, py = np.meshgrid(gx, gy)
    inside = px**2 + py**2 <= (r_f + h) ** 2
    centres = np.stack([px[inside], py[inside]], axis=1)
    idx_x = np.clip(np.round(ships[:, 0] / h).astype(int) + k, 0, 2 * k)
    idx_y = np.clip(np.round(ships[:, 1] / h).astype(int) + k, 0, 2 * k)
    ship_pixel = idx_y * (2 * k + 1) + idx_x
    pix_centre_of_ship = centres[ship_pixel] if len(centres) == (2 * k + 1) ** 2 else None
    # map each ship to the nearest grid centre explicitly (robust to the mask):
    ship_home = np.stack([idx_x * h - k * h, idx_y * h - k * h], axis=1)
    span = R_P + r_f + 0.5 * R_P
    u = np.linspace(-span, span, 401)
    impact = 0.0
    errs, nsamples = [], len(centres)
    for uu in u:
        c = np.array([uu, impact])
        behind_true = np.hypot(*(ships + c).T) < R_P
        behind_pix = np.hypot(*(ship_home + c).T) < R_P
        f_true = 1.0 - behind_true.mean()
        f_pix = 1.0 - behind_pix.mean()
        errs.append(abs(f_pix - f_true))
    row = {
        "config": label,
        "r_f_over_r_p": r_f,
        "pixel_h": h,
        "samples_paid": nsamples,
        "peak_err": float(max(errs)),
        "frac_time_err_gt5": float(np.mean(np.array(errs) > 0.05)),
    }
    out["pixel_arms"].append(row)
    return row



def beta_arm_skyplane(beta: float, r_f: float, label: str, out: dict) -> dict:
    """Sky-plane orientation: the fleet disc is perpendicular to the LOS (all ships at
    the same depth), spread in (x, z). 3D segment-vs-disc predicate."""
    gamma = 1.0 / math.sqrt(1.0 - beta * beta)
    y_fleet, C_Y = 25.0, 20.0
    rng = np.random.default_rng(SEED + 1)
    ships = fleet(N_BETA, r_f, rng)
    x_c0 = -(r_f + R_P + 14.0)
    t_mid = -x_c0 / beta
    W = (r_f + R_P) / beta + 14.0 + 1.5 * beta * (y_fleet + r_f)
    t_obs = np.linspace(t_mid - W, t_mid + W, 1201)
    f_true, f_1c = [], []
    for t in t_obs:
        x0 = ships[:, 0] + x_c0
        y0 = np.full(N_BETA, y_fleet)
        z0 = ships[:, 1]
        a = beta * beta - 1.0
        b = 2.0 * (beta * x0 + t)
        c = x0**2 + y0**2 + z0**2 - t * t
        disc = b * b - 4.0 * a * c
        sq = np.sqrt(np.maximum(disc, 0.0))
        r1 = (-b + sq) / (2 * a)
        r2 = (-b - sq) / (2 * a)
        guess = t - np.sqrt(x0**2 + y0**2 + z0**2)
        te = np.where(np.abs(r1 - guess) < np.abs(r2 - guess), r1, r2)
        prx, pry, prz = x0 + beta * te, y0, z0
        n2 = prx**2 + pry**2 + prz**2
        tt = np.clip(C_Y * pry / n2, 0.0, 1.0)
        dist = np.hypot(tt * prx, np.hypot(tt * pry - C_Y, tt * prz))
        behind = dist < R_P
        nrm = np.sqrt(n2)
        cosang = -(beta * prx) / nrm
        k = 1.0 / (gamma * (1.0 - beta * cosang))
        w = k**4
        f_true.append(float(1.0 - w[behind].sum() / w.sum()))
        # centre sample (z=0)
        bb = 2.0 * (beta * x_c0 + t)
        cc = x_c0**2 + y_fleet**2 - t * t
        dd = bb * bb - 4 * a * cc
        sqq = math.sqrt(max(dd, 0.0))
        rr1 = (-bb + sqq) / (2 * a)
        rr2 = (-bb - sqq) / (2 * a)
        gg = t - math.hypot(x_c0, y_fleet)
        tee = rr1 if abs(rr1 - gg) < abs(rr2 - gg) else rr2
        prx_c = x_c0 + beta * tee
        ttt = min(max(C_Y * y_fleet / (prx_c**2 + y_fleet**2), 0.0), 1.0)
        dd_ = math.hypot(ttt * prx_c, ttt * y_fleet - C_Y)
        f_1c.append(1.0 if dd_ >= R_P else 0.0)
    f_true = np.array(f_true)
    f_1c_arr = np.array(f_1c)
    err = np.abs(f_1c_arr - f_true)
    seen_mid = int(np.argmin(f_true))
    out["beta_arms"].append({
        "config": label, "beta": beta, "r_f_over_r_p": r_f,
        "peak_err_centre": float(err.max()),
        "err_at_mid": float(err[seen_mid]),
        "f1_at_mid": float(f_1c_arr[seen_mid]),
        "f_true_at_mid": float(f_true[seen_mid]),
        "f_true_min": float(f_true.min()),
        "frac_time_err_gt5": float((err > 0.05).mean()),
        "frac_time_total_blink_true_gt_half": float(((f_1c_arr == 0) & (f_true > 0.5)).mean()),
    })


def beta_arm(beta: float, r_f: float, label: str, out: dict) -> dict:
    """Exact: observer O=(0,0); planet C=(0,20) static R_p=1; fleet plane at y~25 moving
    in +x at beta (c=1). Per ship: retarded time (quadratic past root), then the
    segment(P_ret -> O) vs planet disc predicate, and the SR k^4 weight from the retarded
    photon direction. One-sample rule: the fleet centre's own predicate."""
    gamma = 1.0 / math.sqrt(1.0 - beta * beta)
    d_c, y_fleet = 20.0, 25.0
    rng = np.random.default_rng(SEED + 1)
    ships = fleet(N_BETA, r_f, rng)                            # local (x, y) at t=0
    x_c0 = -(r_f + R_P + 14.0)                                 # centre starts left
    t_mid = -x_c0 / beta
    W = (r_f + R_P) / beta + 14.0 + 1.5 * beta * (y_fleet + r_f)   # seen transit shifts ~ beta*d
    t_obs = np.linspace(t_mid - W, t_mid + W, 1201)
    f_true, f_1c = [], []
    for t in t_obs:
        x0 = ships[:, 0] + x_c0
        y0 = ships[:, 1] + y_fleet
        # retarded: (x0+beta te)^2 + y0^2 = (t - te)^2  ->  a te^2 + b te + c = 0
        a = beta * beta - 1.0
        b = 2.0 * (beta * x0 + t)
        c = x0**2 + y0**2 - t * t
        disc = b * b - 4.0 * a * c
        sq = np.sqrt(np.maximum(disc, 0.0))
        r1 = (-b + sq) / (2 * a)
        r2 = (-b - sq) / (2 * a)
        guess = t - np.hypot(x0, y0)
        te = np.where(np.abs(r1 - guess) < np.abs(r2 - guess), r1, r2)
        pr = np.stack([x0 + beta * te, y0], axis=1)            # retarded positions
        # segment pr -> O(0,0) vs disc at C=(0,20), radius 1: closest point parameter
        tt = np.clip((C_Y := 20.0) * pr[:, 1] / (pr[:, 0] ** 2 + pr[:, 1] ** 2), 0.0, 1.0)
        closest = tt[:, None] * pr
        dist = np.hypot(closest[:, 0], closest[:, 1] - C_Y)
        behind = dist < R_P
        # SR k^4 weight: photon direction n = -pr/|pr| (emitter -> observer)
        nrm = np.hypot(pr[:, 0], pr[:, 1])
        cosang = -(beta * pr[:, 0]) / nrm                       # v . n, v = (beta, 0)
        k = 1.0 / (gamma * (1.0 - beta * cosang))
        w = k**4
        f_true.append(float(1.0 - w[behind].sum() / w.sum()))
        # the centre sample: same exact predicate on the centre worldline
        for f1_list, (cx, cy) in ((f_1c, (x_c0, y_fleet)),):
            bb = 2.0 * (beta * cx + t)
            cc = cx**2 + cy**2 - t * t
            dd = bb * bb - 4 * a * cc
            sqq = math.sqrt(max(dd, 0.0))
            rr1 = (-bb + sqq) / (2 * a)
            rr2 = (-bb - sqq) / (2 * a)
            gg = t - math.hypot(cx, cy)
            tee = rr1 if abs(rr1 - gg) < abs(rr2 - gg) else rr2
            prx, pry = cx + beta * tee, cy
            ttt = min(max(C_Y * pry / (prx**2 + pry**2), 0.0), 1.0)
            dd_ = math.hypot(ttt * prx, ttt * pry - C_Y)
            f1_list.append(1.0 if dd_ >= R_P else 0.0)
    f_true = np.array(f_true)
    f_1c_arr = np.array(f_1c)
    err = np.abs(f_1c_arr - f_true)
    seen_mid = int(np.argmin(f_true))                          # the SEEN eclipse centre
    row = {
        "config": label,
        "beta": beta,
        "r_f_over_r_p": r_f,
        "peak_err_centre": float(err.max()),
        "err_at_mid": float(err[seen_mid]),
        "f1_at_mid": float(f_1c_arr[seen_mid]),
        "f_true_at_mid": float(f_true[seen_mid]),
        "f_true_min": float(f_true.min()),
        "frac_time_err_gt5": float((err > 0.05).mean()),
        "frac_time_total_blink_true_gt_half": float(((f_1c_arr == 0) & (f_true > 0.5)).mean()),
    }
    out["beta_arms"].append(row)
    return row


def main() -> None:
    out = {"arms": [], "pixel_arms": [], "beta_arms": [], "controls": {}}
    # P1 control: single-member aggregate.
    rng = np.random.default_rng(SEED)
    ships1 = fleet(1, 0.0, rng)  # degenerate: the one ship at the centre
    u = np.linspace(-2.5, 2.5, 101)
    err1 = []
    for uu in u:
        behind = math.hypot(uu, 0.0) < R_P
        f_t = 0.0 if behind else 1.0
        f_1 = 0.0 if behind else 1.0
        err1.append(abs(f_1 - f_t))
    out["controls"]["single_member_max_err"] = float(max(err1))

    static_arm(0.01, 0.0, "rf0.01_impact0", out)              # P2 safe regime
    static_arm(1.0, 0.0, "rf1_impact0", out)                  # P5
    static_arm(3.0, 0.0, "rf3_impact0", out)                  # P3 headline
    static_arm(10.0, 0.0, "rf10_impact0", out)                # P4
    static_arm(3.0, 0.7 * (3.0 + 1.0), "rf3_impact2.8_grazing", out)  # P10 held-out
    pixel_arm(3.0, 0.5, "pix_h0.5_rf3", out)                  # P7
    pixel_arm(3.0, 0.125, "pix_h0.125_rf3", out)              # P7
    beta_arm(0.5, 3.0, "beta0.5_rf3_transitplane", out)        # P8
    beta_arm_skyplane(0.5, 3.0, "beta0.5_rf3_skyplane", out)      # P8b

    with open("results.json", "w") as fh:
        json.dump(out, fh, indent=1)

    print(f"control single-member max err: {out['controls']['single_member_max_err']}")
    print(f"{'config':28s} {'peak':>7s} {'err@mid':>8s} {'f1@mid':>7s} {'ftrue@mid':>10s} "
          f"{'ftrue_min':>9s} {'t>5%':>6s} {'blink':>6s} {'cf_dev':>7s}")
    for r in out["arms"]:
        print(f"{r['config']:28s} {r['peak_err_centre']:7.3f} {r['err_at_mid']:8.3f} "
              f"{r['f1_at_mid']:7.2f} {r['f_true_at_mid']:10.3f} {r['f_true_min']:9.3f} "
              f"{r['frac_time_err_gt5']:6.2f} {r['frac_time_total_blink_true_gt_half']:6.2f} "
              f"{r['cf_crosscheck_max_dev']:7.4f}")
    print("pixel arms:")
    for r in out["pixel_arms"]:
        print(f"  {r['config']:24s} samples {r['samples_paid']:5d} peak {r['peak_err']:.4f} "
              f"t>5% {r['frac_time_err_gt5']:.3f}")
    print("beta arms:")
    for r in out["beta_arms"]:
        print(f"  {r['config']:16s} peak {r['peak_err_centre']:.3f} err@seenmid {r['err_at_mid']:.3f} "
              f"f1@seenmid {r['f1_at_mid']:.2f} ftrue@seenmid {r['f_true_at_mid']:.3f} "
              f"ftrue_min {r['f_true_min']:.3f} t>5% {r['frac_time_err_gt5']:.2f} "
              f"blink {r['frac_time_total_blink_true_gt_half']:.2f}")
    # extra P3 diagnostics
    r3 = next(r for r in out["arms"] if r["config"] == "rf3_impact0")
    print(f"rf3: err>80% window path = {r3['err_gt80_window_path']:.2f} R_p "
          f"(sample eclipse width 2 R_p; fleet transit 2*(R_p+R_f) = 8 R_p)")
    print(f"rf3: rand-member err@mid median {r3['err_at_mid_randmember']:.3f}, "
          f"mean-path peak {r3['peak_err_randmember_meanpath']:.3f}")


if __name__ == "__main__":
    sys.exit(main())
