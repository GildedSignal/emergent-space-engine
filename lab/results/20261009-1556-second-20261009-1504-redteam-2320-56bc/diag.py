#!/usr/bin/env python3
"""Why did the generously handed strong branch die at frame 1 (eta 400->386.9)?
Replays the shipped continuation iteration by iteration for that one branch,
printing (theta, s, rmin) per iteration. Also tests the wrap seeds' fate under
the shipped scalar tracer (march cap) vs an extended march (mine, 40x longer,
same RK4/Binet law). Writes diag-out.json.
"""
import numpy as np, json
import falsifier as F

def extended_trace1(theta, L, Srel, rS, dphi=0.005, max_steps=44000):
    """F.trace1 with a longer march (winding rays need phi ~ pi + delta)."""
    obs_rel = F.O - L
    r0 = float(np.linalg.norm(obs_rel)); phi0 = float(np.arctan2(obs_rel[1], obs_rel[0]))
    er = obs_rel / r0; ephi = np.array([-er[1], er[0]])
    dv = (np.cos(theta), np.sin(theta))
    cospsi = dv[0]*er[0] + dv[1]*er[1]; sinpsi = dv[0]*ephi[0] + dv[1]*ephi[1]
    u = 1.0/r0; p = -u*cospsi/sinpsi
    sgn = 1.0 if sinpsi >= 0 else -1.0; hh = dphi*sgn
    phi = phi0; uc = 1.0/rS; u_stop = 1.0/12000.0
    rmin = np.inf; crossed = False; phi_c = 0.0
    for _ in range(max_steps):
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

def main():
    F.R_STAR = 3.0
    L0, Sr0, rS0 = F.geom(400.0)
    L1, Sr1, rS1 = F.geom(386.9)
    # seed = the strong root handed at frame 0
    th0 = 0.20648143268359595
    s0, rm0 = F.trace1(th0, L0, Sr0, rS0)
    trace = [dict(frame=0, theta=th0, s=s0, rmin=rm0)]
    # frame 1 iteration by iteration, mirroring F.continuation_frame
    t_seed, s_seed, t = th0, s0, th0
    for it in range(6):
        s, rm = F.trace1(t, L1, Sr1, rS1)
        trace.append(dict(frame=1, it=it+1, theta=t, s=s, rmin=rm))
        if s is None or rm < F.R_STAR:
            trace[-1]['dead'] = 'no-crossing/blocked'; break
        if abs(s) < 0.5:
            trace[-1]['converged'] = True; break
        if s_seed is None or abs(t - t_seed) < 1e-12:
            t_new = t - s/8000.0
        else:
            denom = (s - s_seed)
            t_new = t - s*(t - t_seed)/denom if abs(denom) > 1e-12 else t - s/8000.0
        if not np.isfinite(t_new) or abs(t_new - t) < 1e-12:
            t_new = t - s/8000.0
        t_seed, s_seed = t, s
        t = float(np.clip(t_new, -0.3, 0.3))
    # wrap seeds under shipped vs extended march
    wrap = {}
    for th in (0.19473328786987312, 0.20002099834882897):
        s_ship, rm_ship = F.trace1(th, L0, Sr0, rS0)
        s_ext, rm_ext = extended_trace1(th, L0, Sr0, rS0)
        wrap[round(th, 5)] = dict(shipped_s=s_ship, shipped_rmin=rm_ship,
                                  extended_s=s_ext, extended_rmin=rm_ext)
    out = dict(strong_branch_trace=trace, wrap_seeds=wrap)
    print(json.dumps(out, indent=1, default=float))
    with open('diag-out.json', 'w') as fh:
        json.dump(out, fh, default=float)

if __name__ == '__main__':
    main()
