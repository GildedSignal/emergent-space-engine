#!/usr/bin/env python3
"""Second-author run on 20261008-1419-system-2f89: the usable-root census for the SEM step.

The checker's gold recipe, executed: freeze a usability band, sweep scenes, probe the
structural prediction (K(start)=0 => K(end(alpha)) = alpha^2 C2 ds^2 + alpha^3 C3 ds^3 has
no nonzero root except where the cubic competes), and make every number regenerate from
this folder. p8.py is the author's shipped script, imported unmodified.

FROZEN before the decisive runs (see predictions.md):
  grid      : 37 log points on [1/64, 64] (3 per octave; 1, 2, 4, 8, ... are grid points)
  usable    : a root alpha* in [1/2, 2] (bisection, 42 iterations)
  sens band : any root in [1/4, 4]       (band-edge sensitivity, reported separately)
  runaway   : a root outside the usable band; disclosed with the |K| scale at alpha = 1,
              2, 8, 64 so runaway roots can be read against the nominal residual scale
  variants  : P = plain v2 states (natural shadow offset);
              Z = same states, p_t reset so K(start) = 0 (the manifold a successful SEM
                  step lands on; the drift time tau1 changes with p_t, so the whole
                  alpha-family is the SEM one, not just a shifted offset);
              best = a full trajectory whose every step is solved on the usable band
                  (root when one exists, else argmin |K| in band) -- the most
                  root-favourable SEM trajectory that can be flown.
  scenes    : base (B12 ships, e 0-0.3, seed 4), seed99, ecc (e 0.5-0.85, seed 5),
              two (2nd planet 0.4 mu at 9.5, phase 2.1 rad, generic Omega),
              flyby (B13 hyperbolic passes, seed 7; encounter-dominant)

Subcommands (all <= ~90 s):
  census.py controls|noether
  census.py census <scene> <k> <plain|zero> [steps]
  census.py best   <scene> <k> [periods]
  census.py summary
"""
import glob
import json
import os
import sys

import numpy as np

import p8
from p8 import (C_CLOCK, MU, OMEGA, P_PLANET, R_H, R_PLANET_SHRUNK, R_PLANET_TRUE,
                SEP, b12_ships, fprime, init_p_t, kepler_drift, k_residual,
                planet, step_plain, up_field)

HERE = os.path.dirname(os.path.abspath(__file__))

A_MIN, A_MAX = 1.0 / 64.0, 64.0
GRID = np.exp(np.linspace(np.log(A_MIN), np.log(A_MAX), 37))  # 3 per octave
LO, HI = 0.5, 2.0                 # usable band (frozen)
S_LO, S_HI = 0.25, 4.0            # sensitivity band (frozen)
BESTGRID = np.exp(np.linspace(np.log(LO), np.log(HI), 25))
NBISECT = 42
IDX1 = int(np.argmin(np.abs(GRID - 1.0)))


# ------------------------------------------------------------------ two-planet scene
P2 = ((MU, SEP, 0.0), (0.4 * MU, 9.5, 2.1))   # (mass, separation, phase)


def up2_field(x, t):
    """Total planetary U, grad, and the per-planet pieces (for the exact Noether p_t)."""
    u = np.zeros(x.shape[:-1] + (1,))
    gu = np.zeros_like(x)
    parts = []
    for (mi, si, phi) in P2:
        om = np.sqrt(1.0 + mi) / si ** 1.5
        ang = np.asarray(om * t + phi, dtype=float).ravel()   # (m,)
        xp = si * np.stack([np.cos(ang), np.sin(ang)], axis=-1)
        vp = om * si * np.stack([-np.sin(ang), np.cos(ang)], axis=-1)
        d = x - xp
        r12 = np.linalg.norm(d, axis=-1, keepdims=True)
        u = u + mi / r12 - mi * np.sum(x * xp, axis=-1, keepdims=True) / si ** 3
        gui = -mi * d / r12 ** 3 - mi * xp / si ** 3
        gu = gu + gui
        parts.append((om, gui, vp, xp))
    return u, gu, parts


def hd_of(x, v):
    return 0.5 * np.sum(v * v, axis=-1, keepdims=True) - 1.0 / np.linalg.norm(x, axis=-1, keepdims=True)


def kres2(x, v, p_t, t):
    return hd_of(x, v) - up2_field(x, t)[0] + p_t


def step2(x, v, p_t, t, ds, a=1.0):
    a = np.asarray(a, dtype=float).reshape(-1, 1) if np.ndim(a) else a
    tau1 = a * (0.5 * ds) * fprime(hd_of(x, v) + p_t + C_CLOCK)
    x1, v1 = kepler_drift(x, v, tau1)
    t1 = t + tau1
    u1, gu1, parts = up2_field(x1, t1)
    w = a * ds * fprime(u1 + C_CLOCK)
    dv = w * gu1
    dp_t = sum(-om * np.cross(x1, w * gui)[..., None] for (om, gui, _, _) in parts)
    v1 = v1 + dv
    p1 = p_t + dp_t
    tau2 = a * (0.5 * ds) * fprime(hd_of(x1, v1) + p1 + C_CLOCK)
    x2, v2 = kepler_drift(x1, v1, tau2)
    return x2, v2, p1, t1 + tau2


def step1(x, v, p_t, t, ds, a=1.0):
    return step_plain(x, v, p_t, t, ds, alpha_mul=a)


# ------------------------------------------------------------------ scenes
def ecc_ships(n, seed):
    rng = np.random.default_rng(seed)
    a = SEP * rng.uniform(0.75, 1.35, n)
    e = rng.uniform(0.5, 0.85, n)
    ang = rng.uniform(0, 2 * np.pi, n)
    nu = rng.uniform(0, 2 * np.pi, n)
    r = a * (1 - e ** 2) / (1 + e * np.cos(nu))
    x = np.stack([r * np.cos(nu + ang), r * np.sin(nu + ang)], axis=1)
    h_circ = np.sqrt(np.maximum(a * (1 - e ** 2), 1e-9))
    vv = h_circ / r
    v = np.stack([-vv * np.sin(nu + ang), vv * np.cos(nu + ang)], axis=1)
    return x, v


def flyby_ships(n, seed):
    """B13's encounter-dominant hyperbolic passes, batched (copied from p8.run_b13 setup)."""
    rng = np.random.default_rng(seed)
    kms = 29.78
    q_r = rng.uniform(1.2, 50.0, n) * R_PLANET_TRUE
    vinf = rng.uniform(5.0, 20.0, n) / kms
    r_start = 0.5 * R_H
    e_h = 1.0 + vinf ** 2 * q_r / MU
    cosnu = ((q_r * (1 + e_h)) / r_start - 1.0) / e_h
    nu0 = -np.arccos(np.clip(cosnu, -1, 1))
    v_peri = np.sqrt(vinf ** 2 + 2.0 * MU / q_r)
    b_ang, phi = rng.uniform(0, 2 * np.pi, n), rng.uniform(0, 2 * np.pi, n)
    ed = np.stack([np.cos(b_ang), np.sin(b_ang)], axis=1)
    td = np.stack([-ed[:, 1], ed[:, 0]], axis=1)
    r_dir = np.cos(nu0)[:, None] * ed + np.sin(nu0)[:, None] * td
    t_dir = -np.sin(nu0)[:, None] * ed + np.cos(nu0)[:, None] * td
    h_p = q_r * v_peri
    v_rad = -np.sqrt(np.maximum(vinf ** 2 + 2.0 * MU / r_start - h_p ** 2 / r_start ** 2, 0.0))
    v_rel = v_rad[:, None] * r_dir + (h_p / r_start)[:, None] * t_dir
    ang = phi
    xp0 = SEP * np.stack([np.cos(ang), np.sin(ang)], axis=1)
    vp0 = OMEGA * SEP * np.stack([-np.sin(ang), np.cos(ang)], axis=1)
    return xp0 + r_start * r_dir, vp0 + v_rel


def scene(name, k, n_ships=8):
    ds = (P_PLANET / 2 ** k) / fprime(C_CLOCK)
    if name == "base":
        x, v = b12_ships(n_ships, 4)
    elif name == "seed99":
        x, v = b12_ships(n_ships, 99)
    elif name == "ecc":
        x, v = ecc_ships(n_ships, 5)
    elif name == "two":
        x, v = b12_ships(n_ships, 4)
    elif name == "flyby":
        x, v = flyby_ships(n_ships, 7)
    else:
        raise SystemExit("unknown scene " + name)
    p_t = init_p_t(x, v)
    if name == "two":
        return x, v, p_t, step2, kres2, ds, lambda x, t: up2_field(x, t)[0]
    return x, v, p_t, step1, k_residual, ds, lambda x, t: up_field(x, t)[0]


# ------------------------------------------------------------------ root finding
def k_family(stepf, kres, x, v, p_t, t, ds, grid):
    Ks = np.empty((len(grid),) + x.shape[:-1] + (1,))
    for i, a in enumerate(grid):
        x2, v2, p1, t2 = stepf(x, v, p_t, t, ds, a)
        Ks[i] = kres(x2, v2, p1, t2)
    return Ks[:, :, 0]  # (ngrid, nship)


def bisect_batched(stepf, kres, x, v, p_t, t, ds, js, alo, ahi, klo, khi):
    """js maps each bracket to its ship; states are indexed, alpha is per-bracket."""
    alo = alo.copy(); ahi = ahi.copy(); klo = klo.copy(); khi = khi.copy()
    xb, vb, pb = x[js], v[js], p_t[js]
    tb = np.asarray(t)
    if tb.ndim > 0 and tb.shape[0] == x.shape[0]:
        tb = tb[js]
    for _ in range(NBISECT):
        amid = 0.5 * (alo + ahi)
        x2, v2, p1, t2 = stepf(xb, vb, pb, tb, ds, amid[:, None])
        km = kres(x2, v2, p1, t2)[:, 0]
        same = np.sign(km) == np.sign(klo)
        alo_n = np.where(same, amid, alo)
        khi_n = np.where(same, khi, km)
        ahi_n = np.where(same, ahi, amid)
        klo_n = np.where(same, km, klo)
        alo, ahi, klo, khi = alo_n, ahi_n, klo_n, khi_n
    return 0.5 * (alo + ahi)


def roots_of_state(stepf, kres, x, v, p_t, t, ds):
    """All grid-bracket roots for each ship. Returns list over ships of root-alpha arrays."""
    K = k_family(stepf, kres, x, v, p_t, t, ds, GRID)
    n = K.shape[1]
    finite = np.all(np.isfinite(K), axis=0)
    sgn = np.sign(K)
    js, ils = [], []
    for j in range(n):
        if not finite[j]:
            continue
        idx = np.where(sgn[:-1, j] * sgn[1:, j] < 0)[0]
        for i in idx:
            js.append(j); ils.append(i)
    roots = [[] for _ in range(n)]
    if js:
        js_a = np.array(js); ils_a = np.array(ils)
        rs = bisect_batched(stepf, kres, x, v, p_t, t, ds, js_a,
                            GRID[ils_a], GRID[ils_a + 1],
                            K[ils_a, js_a], K[ils_a + 1, js_a])
        for r, j in zip(rs, js_a):
            roots[j].append(r)
    return roots, K, finite
# ------------------------------------------------------------------ census
def run_census(name, k, variant, n_steps=200, seed=None):
    x, v, p_t, stepf, kres, ds, uof = scene(name, k)
    n = x.shape[0]
    t = 0.0
    alive = np.ones(n, dtype=bool)
    rec = dict(n=0, usable=0, sens=0, runaway_only=0, onesigned=0, nan=0)
    k1_list, k2_list, k8_list, k64_list = [], [], [], []
    run_root_alpha, run_k_ratio = [], []
    rm_usable, rm_one = [], []
    for _ in range(n_steps):
        # census the CURRENT state (the state SEM would face), then advance plain
        p_eval = p_t.copy()
        if variant == "zero":
            p_eval = -hd_of(x, v) + uof(x, t)      # K(start) = 0 exactly
        roots, K, finite = roots_of_state(stepf, kres, x, v, p_eval, t, ds)
        xp, _ = planet(t)
        rmin = np.linalg.norm(x - xp.reshape(-1, 2), axis=1)
        if name == "two":
            for (mi, si, phi) in P2:
                om = np.sqrt(1.0 + mi) / si ** 1.5
                ang = np.asarray(om * t + phi, dtype=float).ravel()
                xpi = si * np.stack([np.cos(ang), np.sin(ang)], axis=-1)
                rmin = np.minimum(rmin, np.linalg.norm(x - xpi, axis=1))
        for j in range(n):
            if not alive[j]:
                continue
            if rmin[j] <= R_PLANET_SHRUNK:
                alive[j] = False
                continue
            if not finite[j]:
                rec["nan"] += 1
                continue
            rec["n"] += 1
            k1_list.append(abs(K[IDX1, j]))
            k2_list.append(abs(K[IDX1 + 3, j]))
            k8_list.append(abs(K[IDX1 + 9, j]))
            k64_list.append(abs(K[-1, j]))
            r = np.array(roots[j])
            if len(r) == 0:
                rec["onesigned"] += 1
                rm_one.append(rmin[j])
            else:
                if np.any((r >= LO) & (r <= HI)):
                    rec["usable"] += 1
                    rm_usable.append(rmin[j])
                elif np.any((r >= S_LO) & (r <= S_HI)):
                    rec["sens"] += 1
                else:
                    rec["runaway_only"] += 1
                    run_root_alpha.append(float(np.min(np.abs(np.log(r)))))
                    run_k_ratio.append(float(k8_list[-1] / max(k1_list[-1], 1e-300)))
        x, v, p_t, t = stepf(x, v, p_t, t, ds)
    out = dict(scene=name, k=k, variant=variant, steps=n_steps, ships=int(n),
               lost=int(n - np.sum(alive)))
    for key in ("n", "usable", "sens", "runaway_only", "onesigned", "nan"):
        out[key] = int(rec[key])
    out["frac_usable"] = rec["usable"] / max(rec["n"], 1)
    out["frac_onesigned_fullgrid"] = rec["onesigned"] / max(rec["n"], 1)
    out["median_absK1"] = float(np.median(k1_list)) if k1_list else None
    out["median_absK2"] = float(np.median(k2_list)) if k2_list else None
    out["median_absK8"] = float(np.median(k8_list)) if k8_list else None
    out["median_absK64"] = float(np.median(k64_list)) if k64_list else None
    out["median_rmin_usable"] = float(np.median(rm_usable)) if rm_usable else None
    out["median_rmin_onesigned"] = float(np.median(rm_one)) if rm_one else None
    if run_root_alpha:
        out["runaway_median_root_alpha"] = float(np.exp(np.median(run_root_alpha)))
        out["runaway_median_K8_over_K1"] = float(np.median(run_k_ratio))
    fn = os.path.join(HERE, "census-%s-k%d-%s.json" % (name, k, variant))
    with open(fn, "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))
    return out


# ------------------------------------------------------------------ SEM-best trajectory
def run_best(name, k, periods=2.0, cap=6000):
    x, v, p_t, stepf, kres, ds, uof = scene(name, k)
    n = x.shape[0]
    t = np.zeros((n, 1))
    t_end = periods * P_PLANET
    alive = np.ones(n, dtype=bool)
    steps = usable = nan = 0
    kend_abs = []
    prev_root = np.zeros(n, dtype=bool)
    trans = {"rr": [0, 0], "nr": [0, 0]}   # (count, usable_count) by prev_root
    i = 0
    while np.min(t[alive]) < t_end and i < cap:
        K = k_family(stepf, kres, x, v, p_t, t, ds, BESTGRID)
        finite = np.all(np.isfinite(K), axis=0)
        sgn = np.sign(K)
        js, ils = [], []
        for j in range(n):
            if not (alive[j] and finite[j]):
                continue
            idx = np.where(sgn[:-1, j] * sgn[1:, j] < 0)[0]
            for q in idx:
                js.append(j); ils.append(q)
        alpha = np.empty(n)
        has_root = np.zeros(n, dtype=bool)
        for j in range(n):
            if not (alive[j] and finite[j]):
                alpha[j] = 1.0
                continue
            alpha[j] = BESTGRID[np.argmin(np.abs(K[:, j]))]   # no-root fallback: argmin |K| in band
            if np.any(K[:, j] == 0.0):                          # exact grid-point zero
                has_root[j] = True
        if js:
            js_a, ils_a = np.array(js), np.array(ils)
            rs = bisect_batched(stepf, kres, x, v, p_t, t, ds, js_a,
                                BESTGRID[ils_a], BESTGRID[ils_a + 1],
                                K[ils_a, js_a], K[ils_a + 1, js_a])
            for r, j in zip(rs, js_a):
                if not has_root[j] or abs(np.log(r)) < abs(np.log(alpha[j])):
                    alpha[j] = r
                has_root[j] = True
        for j in range(n):
            if not (alive[j] and finite[j]):
                continue
            steps += 1
            if has_root[j]:
                usable += 1
            pr = prev_root[j]
            key = "rr" if pr else "nr"
            trans[key][0] += 1
            trans[key][1] += int(has_root[j])
            prev_root[j] = has_root[j]
            if not finite[j]:
                nan += 1
        x2, v2, p1, t2 = stepf(x, v, p_t, t, ds, alpha[:, None])
        kend_abs.append(np.abs(kres(x2, v2, p1, t2)[alive, 0]))
        x, v, p_t, t = x2, v2, p1, t2
        xp, _ = planet(t)
        alive &= np.linalg.norm(x - xp.reshape(-1, 2), axis=1) > R_PLANET_SHRUNK
        i += 1
    kend = np.concatenate(kend_abs) if kend_abs else np.array([np.nan])
    out = dict(scene=name, k=k, variant="best", periods=periods, steps_taken=i,
               records=int(steps), usable=int(usable),
               frac_usable=usable / max(steps, 1),
               frac_usable_after_root=trans["rr"][1] / max(trans["rr"][0], 1),
               frac_usable_after_noroot=trans["nr"][1] / max(trans["nr"][0], 1),
               median_absK_end=float(np.median(kend)),
               worst_absK_end=float(np.max(kend)),
               lost=int(n - np.sum(alive)), nan=int(nan))
    fn = os.path.join(HERE, "best-%s-k%d.json" % (name, k))
    with open(fn, "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))
    return out



# ------------------------------------------------------------------ controls / noether
def cmd_controls():
    """Instrument controls (run before the decisive census; see predictions.md)."""
    out = {}
    # (a) roots the census finds are true zeros of K(end(alpha)): residual + sign flip
    x, v = b12_ships(8, 3)
    p_t = init_p_t(x, v)
    worst_abs, flip_ok, flip_fail, eligible, nroot = 0.0, 0, 0, 0, 0
    eps = np.finfo(float).eps
    t, ds = 0.0, (P_PLANET / 2 ** 8) / fprime(C_CLOCK)
    for _ in range(40):
        roots, K, finite = roots_of_state(step1, k_residual, x, v, p_t, t, ds)
        scale = max(np.median(np.abs(K)), 1e-300)
        for j in range(x.shape[0]):
            tj = float(np.asarray(t).reshape(-1)[j]) if np.ndim(t) else float(t)
            floor = eps * float(np.median(np.abs(hd_of(x, v)) + np.abs(up_field(x, tj)[0]) + np.abs(p_t)))
            for r in roots[j]:
                nroot += 1
                pk = step1(x[j:j + 1], v[j:j + 1], p_t[j:j + 1], tj, ds, np.array([[r]]))
                kstar = float(k_residual(*pk)[0, 0])
                worst_abs = max(worst_abs, abs(kstar))
                km = k_residual(*step1(x[j:j + 1], v[j:j + 1], p_t[j:j + 1], tj, ds, np.array([[r * (1 - 1e-3)]])))[0, 0]
                kp = k_residual(*step1(x[j:j + 1], v[j:j + 1], p_t[j:j + 1], tj, ds, np.array([[r * (1 + 1e-3)]])))[0, 0]
                if min(abs(km), abs(kp)) > 5.0 * floor:
                    eligible += 1
                    if km * kp < 0:
                        flip_ok += 1
                    else:
                        flip_fail += 1
        x, v, p_t, t = step1(x, v, p_t, t, ds)
    out["roots_checked"] = nroot
    out["worst_abs_K_at_root"] = worst_abs
    out["root_residual_over_floor"] = worst_abs / max(floor, 1e-300)
    out["flip_eligible"] = eligible
    out["flip_fail"] = flip_fail
    # (b) negative: Kepler-only (no planets) must give a flat, root-free K family
    def stepk(x, v, p_t, t, ds, a=1.0):
        x2, v2 = kepler_drift(x, v, np.asarray(a) * ds)
        return x2, v2, p_t, t + np.asarray(a) * ds

    def kresk(x, v, p_t, t):
        return hd_of(x, v) + p_t

    p_off = -hd_of(x, v) + 0.7   # K(start) = 0.7 != 0
    K = k_family(stepk, kresk, x, v, p_off, 0.0, ds, GRID)
    roots, K2, _ = roots_of_state(stepk, kresk, x, v, p_off, 0.0, ds)
    out["neg_roots"] = int(sum(len(r) for r in roots))
    out["neg_max_spread"] = float(np.max(np.abs(K)) - np.min(np.abs(K)))
    print(json.dumps(out, indent=1))
    with open(os.path.join(HERE, "controls.json"), "w") as f:
        json.dump(out, f, indent=1)


def cmd_noether():
    """The discrete-Noether identity the author cited but did not ship; both fields."""
    rng = np.random.default_rng(11)
    x = np.stack([rng.uniform(2, 8, 64), rng.uniform(-2, 2, 64)], axis=1)
    t = rng.uniform(0, 50, 1)[0]
    u, gu, du = up_field(x, t)
    lhs = du[:, 0]
    rhs = -OMEGA * np.cross(x, gu)
    rel1 = float(np.max(np.abs(lhs - rhs) / np.maximum(np.abs(lhs), 1e-300)))
    u2, gu2, parts = up2_field(x, t)
    lhs2 = sum(-om * np.cross(x, gui) for (om, gui, _, _) in parts)
    # exact dU/dt by finite difference on the rigid rotation
    dt = 1e-4
    fd = (up2_field(x, t + dt)[0][:, 0] - up2_field(x, t - dt)[0][:, 0]) / (2 * dt)
    relfd = float(np.max(np.abs(fd - lhs2) / np.maximum(np.abs(lhs2), 1e-300)))
    out = dict(one_planet_max_rel=rel1, two_planet_noether_vs_finite_diff=relfd)
    print(json.dumps(out, indent=1))
    with open(os.path.join(HERE, "noether.json"), "w") as f:
        json.dump(out, f, indent=1)


def cmd_summary():
    rows = []
    for fn in sorted(glob.glob(os.path.join(HERE, "census-*.json")) + glob.glob(os.path.join(HERE, "best-*.json"))):
        with open(fn) as f:
            d = json.load(f)
        rows.append(d)
    print("%-8s %2s %-6s %9s %9s %11s %11s" % ("scene", "k", "var", "usable", "1signed", "afterR", "afterNR"))
    for d in rows:
        print("%-8s %2d %-6s %9.4f %9s %11s %11s" % (
            d["scene"], d["k"], d["variant"], d.get("frac_usable", float("nan")),
            ("%.4f" % d["frac_onesigned_fullgrid"]) if "frac_onesigned_fullgrid" in d else "-",
            ("%.4f" % d["frac_usable_after_root"]) if "frac_usable_after_root" in d else "-",
            ("%.4f" % d["frac_usable_after_noroot"]) if "frac_usable_after_noroot" in d else "-"))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "summary"
    if cmd == "controls":
        cmd_controls()
    elif cmd == "noether":
        cmd_noether()
    elif cmd == "census":
        run_census(sys.argv[2], int(sys.argv[3]), sys.argv[4],
                   int(sys.argv[5]) if len(sys.argv) > 5 else 200)
    elif cmd == "best":
        run_best(sys.argv[2], int(sys.argv[3]),
                 float(sys.argv[4]) if len(sys.argv) > 4 else 2.0)
    elif cmd == "summary":
        cmd_summary()
    else:
        raise SystemExit("unknown command " + cmd)
