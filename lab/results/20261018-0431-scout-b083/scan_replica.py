#!/usr/bin/env python3
"""Observer scan under co-orbital concentration: float replica of the shipped predicate.

Shipped semantics replicated verbatim (float instrument, canonical outcomes are the
integers' business — this run prices a representation, it does not change the law):

  crates/universe/src/encounter.rs::Scan::compute — for the player p and each candidate j
  at tick t with interval h:
      d = x_j(t) - x_p(t)            (current separation)
      w = (v_j(t) - v_p(t)) * h      (linear extrapolation over the interval)
      hit  <=>  dist(origin, segment [d, d+w]) <= near     (encounter tier)
      near = 2^ENCOUNTER_LOG2 * (r_a + r_b)               (ENCOUNTER_LOG2 = 10)
      contact tier: same with near' = (r_a + r_b)

  crates/universe/src/radial.rs::candidates — candidate window radius
      reach = ((r_p + radius_cap)*2^near_log2 + (|v_p| + speed_cap)*h) * 1.01 + r_p*1e-9
      read bodies whose radial range meets [r_p - reach, r_p + reach].

Units: r = 1 (the shared orbit's semi-major axis), circular speed 1, n = 1, P = 2*pi.
Dimensionless ship size rho = (r_a + r_b)/r.

Outputs: the five prediction blocks (P1..P5) with numbers; JSON to scan_replica.json.
"""
import json
import time

import numpy as np

K = 1_000_000          # fleet size for count/cost laws
KB = 40_000            # fleet size for brute-force controls
ENC = 2 ** 10          # ENCOUNTER_LOG2
RHOS = [1e-7, 1e-6, 1e-5]
OUT = {}

rng = np.random.default_rng(20261018)


def kepler(M, e):
    """Mean anomaly -> (x, y, vx, vy) on a=1, n=1 orbit of eccentricity e."""
    E = M.copy()
    for _ in range(60):                     # vectorised Newton; converges long before 60
        f = E - e * np.sin(E) - M
        E = E - f / (1 - e * np.cos(E))
    den = 1 - e * np.cos(E)
    x = np.cos(E) - e
    y = np.sqrt(1 - e * e) * np.sin(E)
    vx = -np.sin(E) / den
    vy = np.sqrt(1 - e * e) * np.cos(E) / den
    return x, y, vx, vy


def seg_dist(d, w):
    """dist(origin, segment [d, d+w]) — the shipped linear predicate's distance."""
    ww = np.einsum('ij,ij->i', w, w)
    s = np.clip(-np.einsum('ij,ij->i', d, w) / np.where(ww == 0, 1.0, ww), 0.0, 1.0)
    r = d + s[:, None] * w
    return np.sqrt(np.einsum('ij,ij->i', r, r))


def shipped_membership(dM, e, h, near, da=None, M0=0.0):
    """Brute force: exact Kepler states, shipped point-to-segment predicate.
    The player sits at mean anomaly M0; member j sits at M0 + dM (dM = the stored offset)."""
    M = M0 + dM
    xj, yj, vxj, vyj = kepler(M, e)
    if da is not None:
        # spread semi-major axes: state on orbit a_j = 1+da (n_j = a^-3/2)
        aj = 1.0 + da
        nj = aj ** -1.5
        Mj = M * (nj / 1.0)                 # same epoch phase offset in mean anomaly
        E = Mj.copy()
        for _ in range(60):
            f = E - e * np.sin(E) - Mj
            E = E - f / (1 - e * np.cos(E))
        den = 1 - e * np.cos(E)
        xj = aj * (np.cos(E) - e)
        yj = aj * np.sqrt(1 - e * e) * np.sin(E)
        vxj = -aj * nj * np.sin(E) / den
        vyj = aj * nj * np.sqrt(1 - e * e) * np.cos(E) / den
    xp, yp, vxp, vyp = kepler(np.array([M0]), e)
    d = np.stack([xj - xp[0], yj - yp[0]], axis=1)
    w = np.stack([(vxj - vxp[0]) * h, (vyj - vyp[0]) * h], axis=1)
    return seg_dist(d, w) <= near, d, w


# ---------------------------------------------------------------- P1: candidates
# Coast window (604c's measured constants): reach ~= 9*r; burn-class window W_b.
p1 = {}
for name in ["coast (reach~9r)", "burn-class (W=1e-3 r)"]:
    p1[name] = {"radial_filter_cut_fraction_on_ring": 0.0,
                "candidates_of_K": 1.0,
                "note": "co-orbital radial ranges == the player's; the radial representation "
                        "cannot exclude a ring member at any horizon"}
# replica check: every member's radius sits inside any window that contains the player
dM_chk = rng.uniform(0.0, 2 * np.pi, KB)
xj, yj, _, _ = kepler(dM_chk, 0.5)
p1["replica_radius_inside_player_window_fraction"] = float(np.mean(
    np.abs(np.sqrt(xj ** 2 + yj ** 2) - 1.0) <= 1e-3))
OUT["P1_candidates"] = p1

# ------------------------------------------------- P2: the answer tier (circular)
# Shared circular orbit: d.w == 0 exactly -> predicate distance == |d| == chord(2 sin(dM/2)).
p2 = {}
dM_uni = rng.uniform(0.0, 2 * np.pi, K)
dM_clu = rng.normal(0.0, 0.02, K)            # taleb-class clustered formation
h_coast = 9.0 / 1.0                          # any h: d.w=0 makes h irrelevant
ctrl = dM_uni[:KB]
_, d, w = shipped_membership(ctrl, 0.0, h_coast, 1.0)   # near=1: just to get d, w
dot = np.abs(np.einsum('ij,ij->i', d, w))
chord = 2 * np.abs(np.sin(ctrl / 2.0))
p2["d_dot_w_max"] = float(dot.max())
p2["closed_form_vs_brute_max_err"] = float(np.abs(seg_dist(d, w) - chord).max())
for rho in RHOS:
    near = ENC * rho
    half = 2 * np.arcsin(min(1.0, near / 2))
    uni_n = int(np.sum(2 * np.abs(np.sin(dM_uni / 2)) <= near))
    clu_n = int(np.sum(2 * np.abs(np.sin(dM_clu / 2)) <= near))
    p2[f"rho={rho:g}"] = {
        "near_set_uniform_per_1e6": uni_n,
        "near_set_clustered_sigma0.02_per_1e6": clu_n,
        "analytic_uniform": float(K * half / np.pi),
    }
OUT["P2_answer_tier_circular"] = p2

# ------------------------------------------- P3: eccentricity kills the naive form
p3 = {}
for e in [0.0, 0.2, 0.5]:
    rho = 1e-6
    near = ENC * rho
    h = 2 * np.pi / 10
    for nu_name, M0 in [("periapsis", 0.0), ("apoapsis", np.pi)]:
        dM = rng.normal(0.0, 0.02, KB)
        true_m, _, _ = shipped_membership(dM, e, h, near, M0=M0)
        naive = 2 * np.abs(np.sin(dM / 2)) <= near   # circular chord on the OFFSET
        row = p3.setdefault(f"e={e}_{nu_name}", {})
        row["naive_circular_chord_membership_error"] = float(np.mean(naive != true_m))
        # the general mechanism: a per-orbit-class capability curve C(offset; nu_p),
        # sampled once over the offset axis at this nu_p, applied to every member
        for gbits in (12, 14):
            n = 2 ** gbits
            grid = (np.arange(n) / n - 0.5) * 2 * np.pi     # offsets in [-pi, pi)
            g, _, _ = shipped_membership(grid, e, h, near, M0=M0)
            idx = np.mod(np.floor((dM / (2 * np.pi) + 0.5) * n).astype(int), n)
            from_curve = g[idx]
            row[f"curve_2^{gbits}_membership_error"] = float(np.mean(from_curve != true_m))
OUT["P3_eccentricity"] = p3

# --------------------------------------------------- P4: shear failure mode sweep
p4 = {}
rho, e, h = 1e-6, 0.0, 2 * np.pi / 10
near = ENC * rho
sigma_star = near / (1.5 * h)                # shear drift ~ reach threshold
for sig in np.logspace(-7, -3, 9):
    dM = rng.normal(0.0, 0.3, KB)
    da = rng.normal(0.0, sig, KB)
    true_m, _, _ = shipped_membership(dM, e, h, near, da=da)
    curve_m = 2 * np.abs(np.sin(dM / 2)) <= near      # phase-only (no shear term)
    disagree = int(np.sum(curve_m != true_m))
    unsound = int(np.sum(true_m & ~curve_m))          # the dangerous direction
    p4[f"sigma_a={sig:.1e}"] = {"disagree": disagree, "unsound_misses": unsound}
p4["predicted_sigma_star"] = float(sigma_star)
OUT["P4_shear"] = p4

# ------------------------------------------------------------- P5: the price
p5 = {}
t0 = time.perf_counter()
ans = 2 * np.abs(np.sin(dM_uni / 2)) <= ENC * 1e-6     # the whole per-member test
t1 = time.perf_counter()
sub = dM_uni[:100_000]
t2 = time.perf_counter()
acc = 0
for v in sub:
    if 2 * abs(np.sin(v / 2)) <= ENC * 1e-6:
        acc += 1
t3 = time.perf_counter()
near_n = p2["rho=1e-06"]["near_set_uniform_per_1e6"]
p5 = {
    "vectorised_per_member_ns": (t1 - t0) / K * 1e9,
    "python_scalar_loop_per_member_ns": (t3 - t2) / len(sub) * 1e9,
    "shipped_per_candidate_us_measured_604c": 4.4,
    "shipped_two_reads_per_candidate_us_7343": 7.1,
    "K": K,
    "exact_reads_needed_coast_rho1e-6": near_n,
    "shipped_answer_s_at_1e6": K * 4.4e-6,
    "offset_tier_s_at_1e6_at_10ns": K * 1e-8 + near_n * 7.1e-6,
}
OUT["P5_price"] = p5

# --------------------------------------------------------- negative control
# The shuffle control must run where answers are not ~all-constant: clustered, rho=1e-5.
# (On the uniform sparse fleet the answer is ~0.03% true — itself a finding: the shipped
#  per-candidate read buys <= ~1e-3 bits for 99.97% of members.)
neg_dM = rng.normal(0.0, 0.02, KB)
neg_true, _, _ = shipped_membership(neg_dM, 0.0, h, ENC * 1e-5)
table_ans = (2 * np.abs(np.sin(neg_dM / 2)) <= ENC * 1e-5)
shuffled = rng.permutation(table_ans)
uni_dM = rng.uniform(0, 2 * np.pi, KB)
uni_true, _, _ = shipped_membership(uni_dM, 0.0, h, ENC * 1e-6)
OUT["negative_control"] = {
    "clustered_rho1e-5_true_fraction": float(np.mean(neg_true)),
    "shuffled_disagreement": float(np.mean(shuffled != neg_true)),
    "unshuffled_disagreement": float(np.mean(table_ans != neg_true)),
    "uniform_rho1e-6_true_fraction": float(np.mean(uni_true)),
}

print(json.dumps(OUT, indent=1, sort_keys=True))
with open(__file__.replace(".py", ".json"), "w") as f:
    json.dump(OUT, f, indent=1, sort_keys=True)
