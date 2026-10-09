#!/usr/bin/env python3
"""Premise red-team: representation.md §2 gather premise.

"Each visible tube crosses the observer's past light cone once; Newton's method
finds the crossing, starting from the previous frame's. Lensing adds crossings,
from each doll's memoized deflection(b)."

The first sentence is implemented as written: a per-image warm-started root
finder on the arrival angle (secant with the previous frame's point — Newton
with a finite-difference slope, generous). The design names no mechanism that
*finds* the added crossings. Test: a lens star transits the observer-source
line; truth = backward ray tracing on the design's own photon law
(Binet u'' + u = 3Mu^2, M=1); compare image sets per frame.

2D, geometric units. All under 60 s.
"""
import numpy as np, json, time

M = 1.0
R_STAR = 50.0            # lens star radius (blocks rays)
D_OL = 2000.0            # observer-lens distance along x
D_OS = 10000.0           # observer-source distance
O = np.array([0.0, 0.0])
S = np.array([D_OS, 0.0])

def geom(eta):
    L = np.array([D_OL, eta]); Srel = S - L
    return L, Srel, float(np.linalg.norm(Srel))

# ---------- vectorized truth tracer over a grid of departure angles ----------
def trace_grid(thetas, L, Srel, rS, dphi=0.005, max_steps=None):
    if max_steps is None: max_steps = int(7.0/dphi) + 200
    obs_rel = O - L
    r0 = float(np.linalg.norm(obs_rel)); phi0 = float(np.arctan2(obs_rel[1], obs_rel[0]))
    er = obs_rel / r0; ephi = np.array([-er[1], er[0]])
    d = np.stack([np.cos(thetas), np.sin(thetas)], 1)
    cospsi = d @ er; sinpsi = d @ ephi
    u0 = 1.0 / r0
    duphi0 = -u0 * cospsi / sinpsi
    sigma = np.where(sinpsi >= 0.0, 1.0, -1.0); h = dphi * sigma
    n = thetas.size
    phi = np.full(n, phi0); u = np.full(n, u0); p = duphi0.copy()
    active = np.ones(n, bool); rmin = np.full(n, np.inf)
    crossed = np.zeros(n, bool); phi_c = np.zeros(n)
    uc = 1.0 / rS; u_stop = 1.0 / 12000.0
    for _ in range(max_steps):
        if not active.any(): break
        pu, pp, pphi = u[active], p[active], phi[active]; hh = h[active]
        k1u = pp;                     k1p = 3.0*pu*pu - pu
        uu = pu + 0.5*hh*k1u;         f1 = 3.0*uu*uu - uu
        k2u = pp + 0.5*hh*k1p;        k2p = f1
        uu = pu + 0.5*hh*k2u;         f2 = 3.0*uu*uu - uu
        k3u = pp + 0.5*hh*k2p;        k3p = f2
        uu = pu + hh*k3u;             f3 = 3.0*uu*uu - uu
        k4u = pp + hh*k3p;            k4p = f3
        nu = pu + hh/6.0*(k1u + 2*k2u + 2*k3u + k4u)
        np_ = pp + hh/6.0*(k1p + 2*k2p + 2*k3p + k4p)
        nphi = pphi + hh
        new_cross = (~crossed[active]) & (pu > uc) & (nu <= uc)
        t = np.where(pu != nu, (pu - uc)/np.maximum(np.abs(pu - nu), 1e-300), 0.0)
        phi_c[active] = np.where(new_cross, pphi + t*hh, phi_c[active])
        crossed[active] = crossed[active] | new_cross
        rmin[active] = np.minimum(rmin[active], 1.0/np.maximum(nu, 1e-9))
        u[active], p[active], phi[active] = nu, np_, nphi
        active[active] &= ~((nu <= u_stop) | (nu >= 0.5))
    # arrival at the source sphere
    x = rS*np.cos(phi_c); y = rS*np.sin(phi_c)
    rp = -p/np.maximum(u*u, 1e-18)                      # dr/dφ at crossing
    tx = -rS*np.sin(phi_c) + rp*np.cos(phi_c); ty = rS*np.cos(phi_c) + rp*np.sin(phi_c)
    tx = tx*sigma; ty = ty*sigma                        # march direction
    tn = np.sqrt(tx*tx + ty*ty); tx /= tn; ty /= tn
    s = tx*(Srel[1] - y) - ty*(Srel[0] - x)             # signed miss at source
    blocked = rmin < R_STAR
    ok = crossed & ~blocked
    return s, ok, rmin

def truth_images(thetas, L, Srel, rS, dphi=0.005):
    s, ok, rmin = trace_grid(thetas, L, Srel, rS, dphi)
    sv = np.where(ok, s, np.nan)
    roots = []
    for i in range(thetas.size - 1):
        a, b = sv[i], sv[i+1]
        if np.isnan(a) or np.isnan(b): continue
        if a == 0.0: roots.append((thetas[i], 0.0)); continue
        if a*b < 0.0:
            t = thetas[i] + (thetas[i+1]-thetas[i])*a/(a-b)
            iu = min(i+2, thetas.size-1); il = max(i-1, 0)
            slope = (sv[iu] - sv[il])/(thetas[iu]-thetas[il])
            roots.append((float(t), float(abs(slope))))
    out = []
    for t, sl in sorted(roots):
        if out and abs(t - out[-1][0]) < 3e-4:
            out[-1] = (out[-1][0], min(out[-1][1], sl)); continue
        out.append((t, sl))
    return out, s, ok

# ---------- scalar tracer for the continuation gather ----------
def trace1(theta, L, Srel, rS, dphi=0.005):
    obs_rel = O - L
    r0 = float(np.linalg.norm(obs_rel)); phi0 = float(np.arctan2(obs_rel[1], obs_rel[0]))
    er = obs_rel / r0; ephi = np.array([-er[1], er[0]])
    dv = (np.cos(theta), np.sin(theta))
    cospsi = dv[0]*er[0] + dv[1]*er[1]; sinpsi = dv[0]*ephi[0] + dv[1]*ephi[1]
    u = 1.0/r0; p = -u*cospsi/sinpsi
    sgn = 1.0 if sinpsi >= 0 else -1.0; hh = dphi*sgn
    phi = phi0; uc = 1.0/rS; u_stop = 1.0/12000.0
    rmin = np.inf; crossed = False; phi_c = 0.0
    for _ in range(1100):
        pu, pp = u, p
        k1u = pp; k1p = 3.0*pu*pu - pu
        uu = pu + 0.5*hh*k1u; k2u = pp + 0.5*hh*k1p; k2p = 3.0*uu*uu - uu
        uu = pu + 0.5*hh*k2u; k3u = pp + 0.5*hh*k2p; k3p = 3.0*uu*uu - uu
        uu = pu + hh*k3u;     k4u = pp + hh*k3p;     k4p = 3.0*uu*uu - uu
        u = pu + hh/6.0*(k1u + 2*k2u + 2*k3u + k4u)
        p = pp + hh/6.0*(k1p + 2*k2p + 2*k3p + k4p)
        phi += hh
        if (not crossed) and pu > uc >= u:
            t = (pu - uc)/(pu - u); phi_c = (phi - hh) + t*hh; crossed = True
        rmin = min(rmin, 1.0/max(u, 1e-9))
        if u <= u_stop or u >= 0.5: break
    if not crossed: return None, rmin
    x = rS*np.cos(phi_c); y = rS*np.sin(phi_c)
    rp = -p/(u*u)
    tx = (-rS*np.sin(phi_c) + rp*np.cos(phi_c))*sgn; ty = (rS*np.cos(phi_c) + rp*np.sin(phi_c))*sgn
    tn = np.hypot(tx, ty); tx /= tn; ty /= tn
    s = tx*(Srel[1] - y) - ty*(Srel[0] - x)
    return float(s), float(rmin)

def continuation_frame(tracked, L, Srel, rS, tol=0.5, maxit=6, dom=0.3):
    out = []
    for (th, s_prev, _iters_prev) in tracked:
        t_seed, s_seed = th, s_prev
        t = th; conv = False; its = 0; rmin = None; s = None
        for it in range(maxit):
            s, rm = trace1(t, L, Srel, rS)
            if s is None or rm < R_STAR: break
            its = it + 1
            if abs(s) < tol: conv = True; rmin = rm; break
            if s_seed is None or abs(t - t_seed) < 1e-12:
                t_new = t - s/8000.0               # ds/dθ ≈ source distance
            else:
                denom = (s - s_seed)
                if abs(denom) < 1e-12: break
                t_new = t - s*(t - t_seed)/denom
            if not np.isfinite(t_new) or abs(t_new - t) < 1e-12:
                t_new = t - s/8000.0
            t_seed, s_seed = t, s
            t = float(np.clip(t_new, -dom, dom))
        if conv: out.append(dict(theta=t, s=s, iters=its, rmin=rmin))
    return out

def main():
    t0 = time.time()
    etas = np.concatenate([np.linspace(400, 20, 30), np.linspace(20, 400, 30)[1:]])
    thetas = np.linspace(-0.25, 0.25, 2001)
    frames = []
    tracked = None
    for k, eta in enumerate(etas):
        L, Srel, rS = geom(eta)
        roots, sv, ok = truth_images(thetas, L, Srel, rS)
        thetas_true = [t for t, _ in roots]
        mags = [1.0/sl if sl > 0 else np.inf for _, sl in roots]
        if tracked is None:
            # seed continuation with the truth at frame 0 (generous), each with
            # its own trace so the secant has a real second point
            tracked = []
            for t in thetas_true:
                s0, _ = trace1(t, L, Srel, rS)
                tracked.append((t, s0, 0))
        cont = continuation_frame(tracked, L, Srel, rS)
        ct = [c['theta'] for c in cont]
        latched = [(i, j) for i in range(len(ct)) for j in range(len(ct))
                   if i != j and abs(ct[i] - ct[j]) < 6e-4]
        frames.append(dict(k=int(k), eta=float(eta),
                           n_truth=len(thetas_true), thetas_true=thetas_true,
                           mags=mags,
                           n_cont=len(cont), thetas_cont=ct,
                           iters=[c['iters'] for c in cont],
                           missed=[t for t in thetas_true
                                   if not any(abs(t - c) < 6e-4 for c in ct)],
                           latched=latched))
        tracked = [(c['theta'], c['s'], c['iters']) for c in cont]
    # ---- caustic boundary by bisection (truth only) ----
    def n_truth(eta):
        L, Srel, rS = geom(eta)
        return len(truth_images(thetas, L, Srel, rS)[0])
    lo, hi = 20.0, 120.0            # n_truth: 2 at lo, 1 at hi
    for _ in range(18):
        mid = 0.5*(lo + hi)
        if n_truth(mid) >= 2: lo = mid
        else: hi = mid
    eta_crit = 0.5*(lo + hi)
    # ---- instrument checks ----
    L, Srel, rS = geom(60.0)
    g = np.linspace(-0.25, 0.25, 4001)
    r5, _, _ = truth_images(g, L, Srel, rS, dphi=0.005)
    r25, _, _ = truth_images(g, L, Srel, rS, dphi=0.00125)
    shift = (max(abs(a - b) for (a, _), (b, _) in zip(r5, r25))
             if len(r5) == len(r25) else None)
    sa, oka, _rma = trace_grid(g[::8], L, Srel, rS, dphi=0.005)
    maxdiff = max(abs(trace1(tt, L, Srel, rS)[0] - ss)
                  for tt, ss, o in zip(g[::8], sa, oka) if o)
    # ---- summary ----
    inside = [f for f in frames if f['n_truth'] == 2]
    miss_frames = [f for f in frames if f['missed']]
    k_birth = next((f['k'] for f in frames if f['n_truth'] == 2), None)
    out = dict(
        wall_s=round(time.time() - t0, 1),
        frames_total=len(frames),
        frames_two_images=len(inside),
        eta_crit_bisected=round(eta_crit, 1),
        eta_crit_small_angle_pred=round(4*M*8000.0/(D_OS*R_STAR)*D_OL, 1),
        frames_with_missed_images=len(miss_frames),
        miss_fraction_inside=round(len([f for f in miss_frames if f['n_truth'] == 2])/max(len(inside), 1), 3),
        first_missed_frame=(miss_frames[0]['k'] if miss_frames else None),
        missed_image_separation_rad=[round(abs(f['missed'][0] - f['thetas_cont'][0]), 4)
                                      for f in miss_frames[:5] if f['thetas_cont'] and f['missed']],
        truth_pair_separation_range_rad=[round(min(abs(f['thetas_true'][1]-f['thetas_true'][0]) for f in inside), 4),
                                         round(max(abs(f['thetas_true'][1]-f['thetas_true'][0]) for f in inside), 4)] if inside else None,
        rel_mag_image2_at_birth_plus=[round(frames[k_birth+i]['mags'][1]/frames[k_birth+i]['mags'][0], 3)
                                      for i in (0, 2, 5, 10) if k_birth is not None and len(frames[k_birth+i]['mags']) == 2],
        max_iters_persistent=max([max(f['iters']) for f in frames if f['iters']] or [0]),
        frames_doubletracked=sum(1 for f in frames if f['latched']),
        dphi_halving_max_root_shift_rad=shift,
        scalar_vs_grid_max_s_diff=round(maxdiff, 6),
        control_outside_ok=all(f['n_truth'] == f['n_cont'] == 1 and not f['missed'] for f in frames[:6]),
        control_outside_frames=[f['k'] for f in frames[:6]],
        tracker_never_had_secondary=all(f['n_cont'] == 1 for f in inside),
        truth_counts_by_eta=[(round(f['eta'], 1), f['n_truth'], f['n_cont']) for f in frames[::4]],
    )
    print(json.dumps(out, indent=1))
    with open('falsifier-out.json', 'w') as fh:
        json.dump(dict(summary=out, frames=frames), fh, default=float)

if __name__ == '__main__':
    main()
