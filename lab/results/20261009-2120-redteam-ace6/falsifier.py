#!/usr/bin/env python3
"""Falsifier: does the design's view gather select the right emission event?

Oracle: Schwarzschild equatorial null geodesics, M=1 (geometric units).
RK4 on  u'=w, w'=3u^2-u,  t'=1/(b u^2 (1-2u)),  s'=sqrt(u^2+w^2)/u^2
from a static observer at (r_o, phi=0), rays shot inward with impact
parameter b (plunging rays included; they can cross the emitter's orbit
inbound before they die). Every crossing of the level u=1/r_e (the emitter's
circular geodesic, Omega=r_e^-3/2, phi_e(t)=phi_e0+Omega t) is an image: the
ray meets the orbit at azimuth phi_c after coordinate time t_c and Euclidean
arc s_c. Image condition (t_obs=0):  phi_e0 - Omega*t_c(b) == phi_c(b) (mod 2pi).

Gathers compared on the same image:
  exact: t_e = -t_c                        (geodesic time transfer)
  flat : solves -t_e = D_flat(t_e), Euclidean chord (the conversation's t - d/c)
  bent : t_e = -s_c                        (deflection applied, flat speed along the arc)
Phase error = Omega*(t_e_gather - t_e_exact), degrees, on the sky the player is shown.
"""
import json, math, time, os
import numpy as np

TWO_PI = 2 * math.pi
LN2_16 = math.log(2) / 16  # ring cell relative width at m=16

def wrap(x):
    return (x + math.pi) % TWO_PI - math.pi

def integrate(b_in, r_o, u_c, dphi, phi_max):
    """Vectorized RK4 over rays b_in (sorted). Returns dict ray_id -> ordered
    crossings (phi_c, t_c, s_c, sign) at level u_c. Rays are compacted as they
    plunge (u>0.4995) or escape (u<u_o/3 outbound); phi_max caps windings."""
    ids = np.arange(b_in.size)
    b = b_in.copy()
    n = b.size
    u = np.full(n, 1.0 / r_o)
    w = np.sqrt(np.maximum((1.0/b)**2 - u*u + 2.0*u**3, 0.0))
    t = np.zeros(n); s = np.zeros(n)
    crossings = {int(i): [] for i in ids}
    phi = 0.0
    steps = int(phi_max / dphi)
    u_stop = (1.0 / r_o) / 3.0
    alive = np.ones(n, dtype=bool)
    for istep in range(steps):
        if not alive.any():
            break
        k1u = w
        k1w = 3*u*u - u
        k1t = 1.0 / (b*u*u*(1.0-2.0*u))
        k1s = np.sqrt(u*u + w*w) / (u*u)
        ua = u + 0.5*dphi*k1u; wa = w + 0.5*dphi*k1w
        k2u = wa; k2w = 3*ua*ua - ua
        k2t = 1.0 / (b*ua*ua*(1.0-2.0*ua))
        k2s = np.sqrt(ua*ua + wa*wa) / (ua*ua)
        ub = u + 0.5*dphi*k2u; wb = w + 0.5*dphi*k2w
        k3u = wb; k3w = 3*ub*ub - ub
        k3t = 1.0 / (b*ub*ub*(1.0-2.0*ub))
        k3s = np.sqrt(ub*ub + wb*wb) / (ub*ub)
        uc_ = u + dphi*k3u; wc_ = w + dphi*k3w
        k4u = wc_; k4w = 3*uc_*uc_ - uc_
        k4t = 1.0 / (b*uc_*uc_*(1.0-2.0*uc_))
        k4s = np.sqrt(uc_*uc_ + wc_*wc_) / (uc_*uc_)
        u_new = u + dphi/6.0*(k1u + 2*k2u + 2*k3u + k4u)
        w_new = w + dphi/6.0*(k1w + 2*k2w + 2*k3w + k4w)
        t_new = t + dphi/6.0*(k1t + 2*k2t + 2*k3t + k4t)
        s_new = s + dphi/6.0*(k1s + 2*k2s + 2*k3s + k4s)
        cross = ((u < u_c) & (u_new >= u_c)) | ((u > u_c) & (u_new <= u_c))
        if cross.any():
            idx = np.nonzero(cross)[0]
            du = u_new[idx] - u[idx]
            frac = np.where(np.abs(du) > 0, (u_c - u[idx]) / np.where(du != 0, du, 1.0), 0.0)
            phi_c = phi + frac*dphi
            t_c = t[idx] + frac*(t_new[idx]-t[idx])
            s_c = s[idx] + frac*(s_new[idx]-s[idx])
            for j in range(idx.size):
                crossings[int(ids[idx[j]])].append(
                    (float(phi_c[j]), float(t_c[j]), float(s_c[j]), 1 if du[j] > 0 else -1))
        # freeze dead rays, advance live ones
        dead = (u_new > 0.4995) | ((u_new < u_stop) & (w_new < 0))
        u = np.where(dead, u, u_new); w = np.where(dead, w, w_new)
        t = np.where(dead, t, t_new); s = np.where(dead, s, s_new)
        alive = alive & ~dead
        phi += dphi
        if (istep & 1023) == 1023 and (~alive).any():
            sel = alive
            ids, b, u, w, t, s, alive = ids[sel], b[sel], u[sel], w[sel], t[sel], s[sel], alive[sel]
    return crossings

def flat_gather(r_o, r_e, phi_e0, Omega):
    """Solve -t_e = D_flat(t_e) by bisection (G strictly decreasing: |dD/dt|<=v<1)."""
    lo, hi = -3.0*(r_o + r_e), 0.0
    def G(te):
        pe = phi_e0 + Omega*te
        D = math.sqrt(r_o*r_o + r_e*r_e - 2*r_o*r_e*math.cos(pe))
        return -te - D
    if G(lo) < 0 or G(hi) > 0:
        return None
    for _ in range(80):
        mid = 0.5*(lo+hi)
        if G(mid) > 0: lo = mid
        else: hi = mid
    return 0.5*(lo+hi)

def scene(r_e, r_o, phi_e0_list, dphi_c, dphi_f, nsweep=2500, bisect=22, label=""):
    u_c = 1.0/r_e
    Omega = r_e**-1.5
    b_graze = 1.0/(u_c*math.sqrt(1.0-2.0*u_c))
    b_hi = min(0.995*r_o/math.sqrt(1.0-2.0/r_o), 1.02*b_graze)
    b_sweep = np.geomspace(0.8, b_hi, nsweep)
    t0 = time.time()
    cross = integrate(b_sweep, r_o, u_c, dphi_c, TWO_PI*2)
    have = np.array([len(cross[i]) > 0 for i in range(nsweep)])
    maxk = max((len(c) for c in cross.values()), default=0)
    brackets = []
    for k in range(min(maxk, 6)):
        hk = np.array([len(cross[i]) > k for i in range(nsweep)])
        idx = np.nonzero(hk)[0]
        if idx.size < 8: continue
        runs = np.split(idx, np.nonzero(np.diff(idx) != 1)[0]+1)
        for run in runs:
            if run.size < 4: continue
            ph = np.array([cross[i][k][0] for i in run])
            tc = np.array([cross[i][k][1] for i in run])
            for pe0 in phi_e0_list:
                R = wrap(pe0 - Omega*tc - ph)
                sg = np.sign(R)
                chg = np.nonzero(sg[:-1]*sg[1:] < 0)[0]
                for i in chg[:6]:
                    brackets.append((k, b_sweep[run[i]], b_sweep[run[i+1]], pe0))
        if len(brackets) > 150: break
    if not brackets:
        return {"label": label, "roots": [], "n_brackets": 0, "t_sec": time.time()-t0}
    k_arr = np.array([br[0] for br in brackets]); pe_arr = np.array([br[3] for br in brackets])
    lo = np.array([br[1] for br in brackets]); hi = np.array([br[2] for br in brackets])
    def resid(bb):
        cr = integrate(bb, r_o, u_c, dphi_f, TWO_PI*2)
        R = np.full(bb.size, np.nan); pc = np.full(bb.size, np.nan)
        tc = np.full(bb.size, np.nan); sc = np.full(bb.size, np.nan)
        for i in range(bb.size):
            lst = cr.get(i, [])
            if len(lst) > k_arr[i]:
                pc[i], tc[i], sc[i], _ = lst[k_arr[i]]
                R[i] = wrap(pe_arr[i] - Omega*tc[i] - pc[i])
        return R, pc, tc, sc
    R_hi, _, _, _ = resid(hi)
    ok = np.isfinite(R_hi) & (R_hi != 0)
    lo, hi, k_arr, pe_arr, R_hi = lo[ok], hi[ok], k_arr[ok], pe_arr[ok], R_hi[ok]
    for _ in range(bisect):
        mid = 0.5*(lo+hi)
        Rm, _, _, _ = resid(mid)
        side = np.sign(Rm)*np.sign(R_hi) > 0
        lo = np.where(side, lo, mid)
        hi = np.where(side, mid, hi)
    b_root = 0.5*(lo+hi)
    Rr, pc, tc, sc = resid(b_root)
    roots = []
    for i in range(b_root.size):
        if not np.isfinite(Rr[i]) or abs(Rr[i]) > 2e-4:
            continue
        te_x = -tc[i]
        psi_x = (pe_arr[i] + Omega*te_x) % TWO_PI
        te_f = flat_gather(r_o, r_e, pe_arr[i], Omega)
        te_b = -sc[i]
        err_flat = math.degrees(wrap(Omega*(te_f - te_x))) if te_f is not None else float('nan')
        err_bent = math.degrees(wrap(Omega*(te_b - te_x)))
        D_flat_x = math.sqrt(r_o*r_o + r_e*r_e - 2*r_o*r_e*math.cos(psi_x))
        alpha = math.degrees(math.asin(min(1.0, b_root[i]*math.sqrt(1.0-2.0/r_o)/r_o)))
        roots.append(dict(b=float(b_root[i]), k=int(k_arr[i]), phi_e0=float(pe_arr[i]),
                          winding=int(pc[i]//TWO_PI), psi_exact_deg=math.degrees(psi_x),
                          alpha_deg=alpha, t_light=float(tc[i]), s_arc=float(sc[i]),
                          D_flat=float(D_flat_x),
                          shapiro_coord=float(tc[i]-sc[i]), geom_excess=float(sc[i]-D_flat_x),
                          err_flat_deg=err_flat, err_bent_deg=err_bent))
    return {"label": label, "roots": roots, "n_brackets": len(brackets), "t_sec": time.time()-t0}

def deflection_check(dphi):
    """Incoming ray from r=5000, b=20: total phi sweep - pi vs 4/b+15pi/4b^2."""
    r_o = 5000.0; b2 = 400.0
    u = 1.0/r_o; w = math.sqrt(1.0/b2 - u*u + 2.0*u**3)
    phi = 0.0; u_start = u
    while phi < 8.0:
        k1 = 3*u*u-u; wa = w+0.5*dphi*k1; ua = u+0.5*dphi*w
        k2 = 3*ua*ua-ua; wb = w+0.5*dphi*k2; ub = u+0.5*dphi*wa
        k3 = 3*ub*ub-ub; wc_ = w+dphi*k3; uc_ = u+0.5*dphi*wb
        k4 = 3*uc_*uc_-uc_
        u += dphi/6*(w + 2*wa + 2*wb + wc_)
        w += dphi/6*(k1 + 2*k2 + 2*k3 + k4)
        phi += dphi
        if phi > math.pi/2 and u < u_start:
            break
    return phi - math.pi

def main():
    t_start = time.time()
    state = dict(nproc=os.cpu_count(),
                 loadavg=open('/proc/loadavg').read().split()[:3],
                 meminfo_head=open('/proc/meminfo').readline().strip())
    out = {"machine": state, "scenes": []}
    phi_e0_list = [i*TWO_PI/12 for i in range(12)]
    for (re_, ro_) in [(8, 500), (7, 500), (10, 500), (20, 500), (50, 500),
                       (8, 5000), (20, 5000), (400, 5000)]:
        dphi_c = 1.25e-3 if ro_ <= 600 else 2.0e-3
        dphi_f = 1.0e-3 if ro_ <= 600 else 1.6e-3
        sc = scene(re_, ro_, phi_e0_list, dphi_c, dphi_f, label=f"r_e={re_}M r_o={ro_}M")
        roots = sc["roots"]
        prim = [r for r in roots if r["winding"] == 0]
        wind = [r for r in roots if r["winding"] >= 1]
        pf = [abs(r["err_flat_deg"]) for r in prim if r["err_flat_deg"] == r["err_flat_deg"]]
        pb = [abs(r["err_bent_deg"]) for r in prim]
        sh = [r["shapiro_coord"] for r in prim]
        q_lattice = ro_*LN2_16
        needed_1deg = (math.pi/180)/(re_**-1.5)
        sc["summary"] = dict(
            n_roots=len(roots), n_primary=len(prim), n_winding=len(wind),
            primary_err_flat_max_deg=max(pf, default=None),
            primary_err_flat_median_deg=float(np.median(pf)) if pf else None,
            primary_err_bent_max_deg=max(pb, default=None),
            shapiro_coord_minmax=[float(np.min(sh)), float(np.max(sh))] if sh else None,
            orbit_period=TWO_PI*re_**1.5,
            lattice_time_quantum=q_lattice, needed_1deg=needed_1deg,
            lattice_over_needed=q_lattice/needed_1deg,
            winding_extra_delay_max=(max([r["t_light"] for r in wind], default=None)),
        )
        out["scenes"].append(sc)
        print(f"[{sc['label']}] roots={len(roots)} prim={len(prim)} wind={len(wind)} "
              f"errflat_max={sc['summary']['primary_err_flat_max_deg']} errbent_max={sc['summary']['primary_err_bent_max_deg']} "
              f"shapiro={sc['summary']['shapiro_coord_minmax']} ({time.time()-t_start:.1f}s)", flush=True)
    d1 = deflection_check(5.0e-4); d2 = deflection_check(2.5e-4)
    out["controls"] = {"deflection_b20_5e-4": d1, "deflection_b20_2.5e-4": d2,
                       "series_4b_15pi4b2": 4/20 + 15*math.pi/(4*400)}
    sc_fine = scene(8, 500, phi_e0_list, 1.25e-3, 5.0e-4, label="r_e=8M r_o=500M fine")
    base = [s for s in out["scenes"] if s["label"] == "r_e=8M r_o=500M"][0]
    def keymap(sc_):
        return {(round(r["phi_e0"], 6), r["k"], r["winding"]): r for r in sc_["roots"]}
    km1, km2 = keymap(base), keymap(sc_fine)
    diffs = [abs(km1[key]["err_flat_deg"]-km2[key]["err_flat_deg"]) for key in km1
             if key in km2 and km1[key]["err_flat_deg"] == km1[key]["err_flat_deg"]]
    out["controls"]["convergence_max_abs_delta_err_deg"] = max(diffs, default=None)
    out["controls"]["n_convergence_pairs"] = len(diffs)
    with open("metrics.json", "w") as f:
        json.dump(out, f, indent=1)
    print("controls:", out["controls"])
    print(f"total {time.time()-t_start:.1f}s")

if __name__ == "__main__":
    main()
