#!/usr/bin/env python3
"""
H_live probe: the rate of live distinctions (quantum-crossing encounter kicks) per
belt body per unit simulated time, measured from belt encounter physics directly.

Scene (spec of this run, r8-flavoured, planar):
  star M*=1, G=1 (units: a=1, orbit = 2*pi, v_K = 1 at a=1)
  belt: a in [1, 1+W] uniform, W = 0.02; e ~ Rayleigh(sigma_e);
  varpi, mean anomaly uniform. N reference = 1e4 (rate is linear in N at fixed
  geometry: test-particle assumption, flagged).
  Belt total mass M_belt in {1e-7, 1e-5} M*; per-body mass m = M_belt / N.

Truth measurement (no candidate logic): stratified Monte Carlo over radial
separations delta_a (log bins). For each sampled pair: exact Keplerian states,
one synodic period, conjunction-centred sampling (mean-longitude conjunction
solved exactly) + vectorised zoom refinement of the distance minimum -> b_min
and v_rel there. P(b_min < rho | delta_a) per bin; encounter rate per body per
orbit  Lambda(rho) = 2 * int n_1D(delta_a) |delta_n| P(delta_a, rho) d(delta_a),
with n_1D = N/W (uniform belt) and |delta_n| = 1.5*delta_a (n = a^-1.5).

Cross-checks / controls:
  positive: analytic estimates (planar shear  Lambda = 1.5 N rho^2 / W for a cold
            belt; kinematic Lambda = 2 n_2D <v_rel> 2 rho for a hot belt) within 3x.
  negative: widest bins must return P ~ 0 (an instrument that cannot say zero is
            broken); a planted broken sampler (uniform-in-time, no conjunction
            centre) must UNDERCOUNT and be caught.

Outputs: JSON with Lambda(rho, sigma_e), b_min distribution, delta-v spectrum,
then (in post) the design table: crossing rates at a quantum grid, scar bits per
body per hour at rtf grid for the plane's belt scenes, regime boundaries.
"""
import json
import sys
import numpy as np

RNG_SEED = 20261010

# ------------------------------------------------------- Kepler propagation
# planar; state in inertial frame, angles = true longitude


def kepler_xy(a, e, lam, M0, t):
    t = np.asarray(t)
    if t.ndim == 2:
        a = a[:, None]; e = e[:, None]; lam = lam[:, None]; M0 = M0[:, None]
    n_ = a ** -1.5
    M = np.mod(M0 + n_ * t, 2.0 * np.pi)
    E = M + e * np.sin(M)
    for _ in range(10):
        E = E - (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    cosE, sinE = np.cos(E), np.sin(E)
    # true anomaly and radius
    r = a * (1.0 - e * cosE)
    nu = np.arctan2(np.sqrt(1.0 - e * e) * sinE, cosE - e)
    th = lam + nu
    c, s = np.cos(th), np.sin(th)
    x, y = r * c, r * s
    # velocity (mu* = 1)
    k = np.sqrt((1.0 + e) / (a * (1.0 - e)))
    vr = k * e * np.sin(nu)
    vt = k * (1.0 + e * np.cos(nu))
    vx = vr * c - vt * s
    vy = vr * s + vt * c
    return x, y, vx, vy


def pair_min_distance(a1, e1, l1, M01, a2, e2, l2, M02, n_coarse=128,
                      n_zoom_pts=12, zoom_rounds=4, zoom_shrink=0.15):
    """Minimum distance over one synodic period, conjunction-centred + zoom.

    Returns b_min (n,), v_rel (n,) at the minimum.
    """
    n1 = a1 ** -1.5
    n2 = a2 ** -1.5
    dn = n1 - n2
    P_syn = 2.0 * np.pi / np.abs(dn)
    # mean-longitude conjunction: lam1 + n1 t = lam2 + n2 t (mod 2pi)
    # relative mean longitude at t=0 (approx: use varpi + M0)
    L1 = l1 + M01
    L2 = l2 + M02
    dL = np.mod(L1 - L2, 2.0 * np.pi)
    # solve dn * t = -dL (mod 2pi): t_c = (2pi - dL)/dn mod P_syn
    with np.errstate(divide="ignore", invalid="ignore"):
        t_c = np.mod((2.0 * np.pi - dL) / np.where(dn == 0, 1.0, dn), P_syn)
    t_c = np.where(dn == 0, 0.0, t_c)

    # coarse: window +/-0.25 P_syn (covers e-driven offsets up to ~0.4 rad)
    half = 0.25 * P_syn
    S = n_coarse
    idx = np.arange(S)[None, :]
    t = t_c[:, None] - half[:, None] + (2 * half[:, None]) * (idx / (S - 1))
    d = _dist(a1, e1, l1, M01, a2, e2, l2, M02, t)
    best = d.min(axis=1)
    best_t = t[np.arange(d.shape[0]), d.argmin(axis=1)]

    # zoom: shrink window around best
    spacing = (2 * half) / (S - 1)
    w = spacing.copy()
    for _ in range(zoom_rounds):
        idx = np.arange(n_zoom_pts)[None, :]
        t = best_t[:, None] - w[:, None] + (2 * w[:, None]) * (idx / (n_zoom_pts - 1))
        d = _dist(a1, e1, l1, M01, a2, e2, l2, M02, t)
        j = d.argmin(axis=1)
        rows = np.arange(d.shape[0])
        cand = d[rows, j]
        upd = cand < best
        best = np.where(upd, cand, best)
        best_t = np.where(upd, t[rows, j], best_t)
        w = w * zoom_shrink

    # relative speed at the refined minimum
    x1, y1, vx1, vy1 = kepler_xy(a1, e1, l1, M01, best_t)
    x2, y2, vx2, vy2 = kepler_xy(a2, e2, l2, M02, best_t)
    v_rel = np.hypot(vx1 - vx2, vy1 - vy2)
    return best, v_rel

def pair_min_distance_blunt(a1, e1, l1, M01, a2, e2, l2, M02, S=128):
    """Planted broken instrument: uniform in time over one synodic period, no
    conjunction centre, no zoom. Must UNDERCOUNT close pairs (dips are far
    narrower than the spacing)."""
    dn = a1 ** -1.5 - a2 ** -1.5
    P_syn = 2.0 * np.pi / np.abs(dn)
    t = np.linspace(0, 1, S)[None, :] * P_syn[:, None]
    d = _dist(a1, e1, l1, M01, a2, e2, l2, M02, t)
    return d.min(axis=1)


def _dist(a1, e1, l1, M01, a2, e2, l2, M02, t):
    x1, y1, _, _ = kepler_xy(a1, e1, l1, M01, t)
    x2, y2, _, _ = kepler_xy(a2, e2, l2, M02, t)
    return np.hypot(x1 - x2, y1 - y2)


# ------------------------------------------------------------------ the probe


def measure(W, sigma_e, N, bins=22, pairs_per_bin=900, seed=RNG_SEED,
            rhos=(1e-4, 1e-3)):
    rng = np.random.default_rng(seed)
    # stratified delta_a bins (log), radial reach capped by 2*W (belt) + ecc
    da_max = 1.2 * (W + 4 * sigma_e)
    edges = np.geomspace(1e-5, da_max, bins + 1)
    out = {"edges": edges, "P": np.zeros((bins, len(rhos))),
           "bmin": np.zeros((bins, pairs_per_bin)),
           "vrel": np.zeros((bins, pairs_per_bin)),
           "pairs_da": np.zeros((bins, pairs_per_bin)),
           "weight": np.zeros(bins)}
    for i in range(bins):
        lo, hi = edges[i], edges[i + 1]
        da = np.exp(rng.uniform(np.log(lo), np.log(hi), pairs_per_bin))
        # draw two bodies with this radial offset; pairs falling outside the
        # belt are dropped and the bin's weight shrinks by the same fraction
        a1 = 1.0 + W * rng.random(pairs_per_bin)
        a2 = a1 + da
        keep = a2 <= 1.0 + W
        out["weight"][i] = np.mean(keep)
        a1, a2, da = a1[keep], a2[keep], da[keep]
        m = len(a1)
        e1 = sigma_e * np.sqrt(-2.0 * np.log(1.0 - rng.random(m)))
        e2 = sigma_e * np.sqrt(-2.0 * np.log(1.0 - rng.random(m)))
        l1 = 2 * np.pi * rng.random(m)
        l2 = 2 * np.pi * rng.random(m)
        M01 = 2 * np.pi * rng.random(m)
        M02 = 2 * np.pi * rng.random(m)
        bmin, vrel = pair_min_distance(a1, e1, l1, M01, a2, e2, l2, M02)
        out["bmin"][i, :m] = bmin
        out["vrel"][i, :m] = vrel
        out["pairs_da"][i, :m] = da
        for k, rho in enumerate(rhos):
            out["P"][i, k] = np.mean(bmin < rho) if m else 0.0
    return out


def rate_from_P(edges, P, N, W, weight=None):
    """Lambda per body per orbit = 2 * int n1D |dn| P da, summed over bins."""
    n1D = N / W
    centers = np.sqrt(edges[:-1] * edges[1:])
    widths = np.diff(edges)
    w = np.ones(len(centers)) if weight is None else weight
    Lam = 2.0 * n1D * np.sum(P * w * (1.5 * centers) * widths)
    return Lam


def blunt_control(seed=RNG_SEED + 1, n=4000):
    """Negative control: the planted blunt sampler on the tightest bin
    (delta_a in [1e-5, 2e-5]) must undercount P(b<1e-4) against the zoomed
    truth on the same pairs."""
    rng = np.random.default_rng(seed)
    da = np.exp(rng.uniform(np.log(1e-5), np.log(2e-5), n))
    a1 = 1.0 + 0.02 * rng.random(n)
    a2 = a1 + da
    e1 = 0.01 * np.sqrt(-2.0 * np.log(1.0 - rng.random(n)))
    e2 = 0.01 * np.sqrt(-2.0 * np.log(1.0 - rng.random(n)))
    l1, l2 = 2 * np.pi * rng.random(n), 2 * np.pi * rng.random(n)
    M01, M02 = 2 * np.pi * rng.random(n), 2 * np.pi * rng.random(n)
    b_true, _ = pair_min_distance(a1, e1, l1, M01, a2, e2, l2, M02)
    b_blunt = pair_min_distance_blunt(a1, e1, l1, M01, a2, e2, l2, M02)
    return {"truth_P": float(np.mean(b_true < 1e-4)),
            "blunt_P": float(np.mean(b_blunt < 1e-4))}


def main():
    res = {}
    for sigma_e, tag in ((0.01, "cold"), (0.1, "hot")):
        out = measure(W=0.02, sigma_e=sigma_e, N=1e4)
        r = {}
        for k, rho in enumerate((1e-4, 1e-3)):
            r[str(rho)] = rate_from_P(out["edges"], out["P"][:, k], 1e4, 0.02,
                                      weight=out["weight"])
        # widest-bin control: P must be ~0 in the last two bins
        widest_zero = float(np.max(out["P"][-2:, :]))
        res[tag] = {
            "Lambda": r,
            "widest_bin_maxP": widest_zero,
            "edges": out["edges"].tolist(),
            "P": out["P"].tolist(),
            "bmin_flat": out["bmin"].ravel().tolist(),
            "vrel_flat": out["vrel"].ravel().tolist(),
            "weight": out["weight"].tolist(),
        }
        print(f"[{tag}] Lambda(1e-4)={r[str(1e-4)]:.4g}  Lambda(1e-3)={r[str(1e-3)]:.4g}"
              f"  widest-bin max P = {widest_zero:.3g}", flush=True)
    res["blunt_control"] = blunt_control()
    print("[control] blunt undercount:",
          f"truth P={res['blunt_control']['truth_P']:.4f}"
          f" blunt P={res['blunt_control']['blunt_P']:.4f}", flush=True)
    with open(sys.argv[1] if len(sys.argv) > 1 else "hlive_raw.json", "w") as f:
        json.dump(res, f)


if __name__ == "__main__":
    main()
