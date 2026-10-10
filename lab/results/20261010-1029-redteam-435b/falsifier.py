#!/usr/bin/env python3
"""Red-team falsifier: the view's gather near a compact mass.

Premise under attack (docs/representation.md s2, law.md "Observation"):
  "Each visible tube crosses the observer's past light cone once; Newton's method finds the
   crossing, starting from the previous frame's. Lensing adds crossings, from each doll's
   memoized deflection(b)."

Truth: exact backward ray tracing of equatorial Schwarzschild null geodesics u'' + u = 3 M u^2
(the equation the law itself compiles: `Passage` in crates/space). "Memo gather": one bend
event of the exact tabulated deflection alpha_d(b) on the connecting straight line (generous:
the crate's per-passage deflection is exact), |b| < b_c = 3 sqrt(3) M => captured => no
crossing. Units M = 1, 2D plane (the game's plane), static observer and sources.

Scenes: A flat control (must pass), B weak-field control (must pass), C near a compact mass.
"""
import json, math, os, time
import numpy as np

T0 = time.time()
M = 1.0
GM = 3.0 * M                    # coefficient of u^2 in u'' = -u + GM u^2
BC = 3.0 * math.sqrt(3.0) * M   # critical impact parameter
U_H = 1.0 / (2.0 * M)

# ---------------------------------------------------------------- exact deflection table
_defl = {}

def trace_passage(b, h):
    """Asymptotic total bend of one passage with impact parameter b (far -> far).
    Window correction: subtract the flat window angle 2*asin(b*u0), so residual error is O(M/r0)."""
    u0 = 1.0 / 3.0e4
    d = math.sqrt(max(1.0 / b**2 - u0**2 + 2.0 * M * u0**3, 0.0))   # inbound: u increasing
    u, d, phi, turned = u0, d, 0.0, False
    flat_window = 2.0 * math.asin(min(b * u0, 1.0))
    while phi < 200.0:
        k1u, k1d = d, -u + GM * u * u
        u2, d2 = u + .5*h*k1u, d + .5*h*k1d
        k2u, k2d = d2, -u2 + GM*u2*u2
        u3, d3 = u + .5*h*k2u, d + .5*h*k2d
        k3u, k3d = d3, -u3 + GM*u3*u3
        u4, d4 = u + h*k3u, d + h*k3d
        k4u, k4d = d4, -u4 + GM*u4*u4
        u, d, phi = u + h*(k1u+2*k2u+2*k3u+k4u)/6, d + h*(k1d+2*k2d+2*k3d+k4d)/6, phi + h
        if u >= U_H:
            return None
        if d < 0:
            turned = True
        if turned and u <= u0 * 1.02:
            break
    return phi - math.pi + flat_window

def build_defl_table():
    bs = np.exp(np.linspace(math.log(BC*(1+2e-6)), math.log(300.0), 360))
    vs = np.empty_like(bs)
    for i, b in enumerate(bs):
        h = 2e-3 if b > 3*BC else 6e-4
        vs[i] = trace_passage(b, h) or 1e9
    return bs, vs

DEF_B, DEF_V = None, None

def alpha_d(b, weak_only=False):
    if weak_only:
        return 4.0*M/b + (15.0*math.pi/4.0)*(M/b)**2  # b-form (r0-form has -4)
    if b > 250.0:
        return 4.0*M/b + (15.0*math.pi/4.0)*(M/b)**2 + (128.0/3.0)*(M/b)**3
    return float(np.interp(b, DEF_B, DEF_V))

# ---------------------------------------------------------------- backward ray tracing
def trace_grid(r_o, r_s, alpha, gm=GM, phi_stop=None, h0=0.08, hmin=1.2e-3):
    """Backward rays from (r_o, phi=0) at look angles alpha (from +e_r toward +phi).
    Returns (phi_cross, captured): first outward crossing of r=r_s (continuous phi), inf if none."""
    u_o, u_s = 1.0/r_o, 1.0/r_s
    u = np.full(alpha.shape, u_o)
    d = -u_o/np.tan(alpha)
    phi = np.zeros_like(u)
    crossed = np.zeros(u.shape, bool)
    captured = np.zeros(u.shape, bool)
    phi_cross = np.full(u.shape, np.inf)
    stop = phi_stop if phi_stop is not None else (4.0*math.pi + 2.0)
    while phi[0] < stop and not (crossed | captured).all():
        act = ~(crossed | captured)
        umax = max(float(u[act].max()), 1e-3)
        h = min(h0, max(hmin, 0.05/(1.0+5.0*umax)))
        k1u, k1d = d, -u + gm*u*u
        u2, d2 = u+.5*h*k1u, d+.5*h*k1d
        k2u, k2d = d2, -u2 + gm*u2*u2
        u3, d3 = u+.5*h*k2u, d+.5*h*k2d
        k3u, k3d = d3, -u3 + gm*u3*u3
        u4, d4 = u+h*k3u, d+h*k3d
        k4u, k4d = d4, -u4 + gm*u4*u4
        un = u + h*(k1u+2*k2u+2*k3u+k4u)/6
        dn = d + h*(k1d+2*k2d+2*k3d+k4d)/6
        phin = phi + h
        captured |= act & (un >= U_H*(1.0 if gm else 0.0) if gm else False)
        if gm:
            hit = act & (~captured) & (u > u_s) & (un <= u_s)
        else:
            hit = act & (u > u_s) & (un <= u_s)
        if hit.any():
            frac = (u[hit]-u_s)/np.maximum(u[hit]-un[hit], 1e-300)
            phi_cross[hit] = phi[hit] + h*np.clip(frac, 0, 1)
            crossed |= hit
        u, d, phi = np.where(crossed|captured, u, un), np.where(crossed|captured, d, dn), phin
    return phi_cross, captured

def pc_at(r_o, r_s, a, target, gm=GM):
    pc, _ = trace_grid(r_o, r_s, np.array([a]), gm=gm, phi_stop=target+1.0)
    return float(pc[0])

def true_images_1side(r_o, r_s, dphi, nmax=2, n_grid=700, gm=GM):
    """Look angles alpha (upper side) with phi_cross(alpha) = dphi + 2 pi n, n <= nmax."""
    grid = np.linspace(0.55, math.pi-0.02, n_grid)
    pc, cap = trace_grid(r_o, r_s, grid, gm=gm,
                         phi_stop=dphi + 2*math.pi*(nmax+1) + 1.5)
    out = []
    da = grid[1]-grid[0]
    for n in range(nmax+1):
        tgt = dphi + 2*math.pi*n
        r_ = np.where(np.isfinite(pc) & ~cap, pc - tgt, np.nan)
        for i in range(n_grid-1):
            a, b_ = r_[i], r_[i+1]
            if not (np.isfinite(a) and np.isfinite(b_)):
                continue
            if a*b_ >= 0:
                continue
            lo, hi, flo = grid[i], grid[i+1], a
            for _ in range(18):
                mid = .5*(lo+hi)
                fm = pc_at(r_o, r_s, mid, tgt, gm=gm) - tgt
                if not np.isfinite(fm):
                    fm = 1e9*(1 if flo > 0 else -1)
                if (flo < 0) == (fm < 0):
                    lo, flo = mid, fm
                else:
                    hi = mid
            root = .5*(lo+hi)
            pm = pc_at(r_o, r_s, root, tgt, gm=gm)
            pp = pc_at(r_o, r_s, min(root+da, grid[-1]), tgt, gm=gm)
            slope = abs((pp-pm)/da) if np.isfinite(pp) and np.isfinite(pm) else np.inf
            if out and min(abs(root-o[0]) for o in out) < 1e-5:
                continue
            out.append((root, n, slope))
    out.sort()
    return out

def true_images(r_o, r_s, dphi, nmax=2, n_grid=700, gm=GM):
    """Both families: same side (sweep dphi + 2pi n) and opposite side (look 2pi - a,
    sweep (2pi - dphi) + 2pi n; mirror symmetry of the orbit equation)."""
    fam1 = true_images_1side(r_o, r_s, dphi, nmax, n_grid, gm)
    fam2 = [(2*math.pi - a, n, s) for a, n, s in
            true_images_1side(r_o, r_s, 2*math.pi - dphi, nmax, n_grid, gm)]
    all_ = sorted(fam1 + fam2)
    return all_

# ---------------------------------------------------------------- the memo gather
def memo_image(r_o, r_s, dphi, weak_only=False):
    xo = np.array([r_o, 0.0])
    xs = np.array([r_s*math.cos(dphi), r_s*math.sin(dphi)])
    dvec = xs - xo
    L = float(np.linalg.norm(dvec))
    t = float(np.clip(np.dot(-xo, dvec)/L**2, 0.0, 1.0))
    cp = xo + t*dvec
    b_line = float(np.linalg.norm(cp))
    if b_line < BC:
        return None, b_line
    delta = alpha_d(b_line, weak_only=weak_only)
    l2 = float(np.linalg.norm(xs - cp))
    ang_flat = math.atan2(dvec[1], dvec[0])
    ang_hole = math.atan2(0.0 - xo[1] if xo[1] != 0.0 else 0.0, -xo[0])
    sgn = 1.0 if ang_flat > ang_hole else -1.0
    return ang_flat + sgn*delta*(l2/L), b_line

# ---------------------------------------------------------------- scenes
def scene_A():
    """Flat control: gm=0 geometry exact; Newton on the retarded root (view.rs model)."""
    r_o, r_s, dphi = 10.0, 30.0, math.pi - 0.3
    imgs = true_images_1side(r_o, r_s, dphi, gm=0.0, n_grid=400)
    xo = np.array([r_o, 0.0])
    xs = np.array([r_s*math.cos(dphi), r_s*math.sin(dphi)])
    ang_flat = math.atan2(*(xs-xo)[::-1])
    def newton_iters(beta_o, beta_s, D=100.0, frames=40):
        worst, t_prev = 0, None
        for k in range(frames):
            t_obs = 50.0 + k/30.0
            xo_ = beta_o*t_obs
            def g(t):
                xs_ = D + beta_s*t
                return t + abs(xs_ - xo_) - t_obs
            def rate(t):
                xs_ = D + beta_s*t
                dd = xs_ - xo_
                return 1.0 + beta_s*math.copysign(1.0, dd) if True else 1
            t = t_prev if t_prev is not None else t_obs - D
            n = 0
            while abs(g(t)) > 1e-9 and n < 60:
                t -= g(t)/rate(t)
                n += 1
            worst = max(worst, n)
            # true root for next frame's guess
            lo, hi = 0.0, t_obs
            for _ in range(80):
                mid = .5*(lo+hi)
                if g(mid) < 0: lo = mid
                else: hi = mid
            t_prev = lo
        return worst
    return {"name": "A flat control", "n_roots_gm0": len(imgs),
            "root_minus_flat_rad": abs(imgs[0][0]-ang_flat) if imgs else None,
            "newton_worst_iters_beta0.5_src0": newton_iters(0.5, 0.0),
            "newton_worst_iters_beta0.999_src0": newton_iters(0.999, 0.0),
            "newton_worst_iters_beta0.5_src-0.9": newton_iters(0.5, -0.9),
            "newton_worst_iters_beta0.999_src-0.9": newton_iters(0.999, -0.9)}

def scene_B():
    r_o, r_s, dphi = 1e4, 3e4, math.pi - 0.1
    imgs = true_images(r_o, r_s, dphi)
    memo_ang, b_line = memo_image(r_o, r_s, dphi)
    xo = np.array([r_o, 0.0])
    xs = np.array([r_s*math.cos(dphi), r_s*math.sin(dphi)])
    ang_flat = math.atan2(*(xs-xo)[::-1])
    out = {"name": "B weak field", "b_line": b_line, "n_true": len(imgs), "memo_angle": memo_ang}
    if imgs:
        best = min(imgs, key=lambda t: abs(t[0]-memo_ang))
        err = abs(best[0]-memo_ang)
        bend_true = best[0]-ang_flat      # apparent - flat = bend seen at observer
        out.update(err_rad=err, bend_true=bend_true, bend_memo=memo_ang-ang_flat,
                   err_over_bend=err/abs(bend_true))
    return out

def scene_C(r_o, r_s, dphis):
    rows = []
    for dphi in dphis:
        imgs = true_images(r_o, r_s, dphi)
        memo_ang, b_line = memo_image(r_o, r_s, dphi)
        memo_wk, _ = memo_image(r_o, r_s, dphi, weak_only=True)
        keep = [(a, n, s) for a, n, s in imgs if np.isfinite(s)]
        if keep:
            mu = np.array([1.0/s for _, _, s in keep])
            kept = [k for k, m in zip(keep, mu) if m >= 0.01*mu.max()]
        else:
            kept = []
        err = err_w = None
        if memo_ang is not None and kept:
            err = math.degrees(min(abs(k[0]-memo_ang) for k in kept))
        if memo_wk is not None and kept:
            err_w = math.degrees(min(abs(k[0]-memo_wk) for k in kept))
        rows.append(dict(dphi=dphi, n_true=len(kept), n_all=len(imgs),
                         n_memo=0 if memo_ang is None else 1,
                         b_line=b_line, err_deg=err, err_weak_deg=err_w,
                         angles_deg=[math.degrees(a) for a, _, _ in kept]))
    return rows

def summarize(rows, r_o, r_s):
    n = len(rows)
    blind = sum(1 for r in rows if r["n_memo"] == 0)
    multi = sum(1 for r in rows if r["n_true"] >= 2)
    errs = [r["err_deg"] for r in rows if r["err_deg"] is not None]
    ew = [r["err_weak_deg"] for r in rows if r["err_weak_deg"] is not None]
    return dict(r_o=r_o, r_s=r_s, sources=n, blind_frac=blind/n, multi_frac=multi/n,
                err_max=max(errs) if errs else None,
                err_median=float(np.median(errs)) if errs else None,
                err_gt1deg=(sum(1 for e in errs if e > 1)/len(errs)) if errs else None,
                err_gt10deg=(sum(1 for e in errs if e > 10)/len(errs)) if errs else None,
                errweak_gt10deg=(sum(1 for e in ew if e > 10)/len(ew)) if ew else None)

def main():
    global DEF_B, DEF_V
    print(f"[{time.time()-T0:5.1f}s] deflection table...")
    DEF_B, DEF_V = build_defl_table()
    for b in (100.0, 30.0):
        w, e = alpha_d(b, True), alpha_d(b)
        print(f"  alpha_d(b={b}): exact {e:.6f}, weak {w:.6f}, rel {abs(e-w)/e:.1e}")
    A = scene_A(); print(f"[{time.time()-T0:5.1f}s] A:", json.dumps(A))
    B = scene_B(); print(f"[{time.time()-T0:5.1f}s] B:", json.dumps(B, default=float))
    results = {"A": A, "B": B, "C": []}
    for r_o, r_s in ((10.0, 30.0), (10.0, 20.0), (10.0, 50.0), (100.0, 1000.0)):
        step = 0.06 if r_o == 10 else 0.1
        dphis = [math.pi-d for d in np.arange(0.0, 0.601, step)]
        print(f"[{time.time()-T0:5.1f}s] C r_o={r_o} r_s={r_s} ({len(dphis)} sources)...")
        rows = scene_C(r_o, r_s, dphis)
        s = summarize(rows, r_o, r_s)
        results["C"].append({"summary": s, "rows": rows})
        print("  ", json.dumps(s, default=float))
    # C4: the gap width (memo-blind dphi interval), truth visibility
    g = results["C"][0]["rows"]
    sc_r = results["C"][0]["summary"]["r_o"]
    bd = [math.pi-r["dphi"] for r in g if r["n_memo"] == 0]
    results["C4"] = {"gap_width_rad": (max(bd)-min(bd))+2*(0.06 if sc_r == 10 else 0.1) if len(bd) > 1 else None,
                     "truth_min_images": min(r["n_true"] for r in g),
                     "truth_always_visible": all(r["n_true"] >= 1 for r in g)}
    # convergence check: one source at two grid sizes
    i1 = true_images(10.0, 30.0, math.pi-0.2, n_grid=700)
    i2 = true_images(10.0, 30.0, math.pi-0.2, n_grid=1400)
    results["convergence"] = {"n_roots_800": len(i1), "n_roots_1600": len(i2),
                              "max_root_shift": max(abs(a[0]-b[0]) for a, b in zip(i1, i2))
                              if len(i1) == len(i2) else None}
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "falsifier-out.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=1, default=float)
    print(f"[{time.time()-T0:5.1f}s] wrote {out}")
    print("convergence:", results["convergence"])
    with open("/proc/loadavg") as f:
        print("loadavg:", f.read().strip())

if __name__ == "__main__":
    main()
