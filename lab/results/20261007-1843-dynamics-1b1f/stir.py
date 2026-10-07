#!/usr/bin/env python3
"""Self-stirring belt: exact planar Kepler motion around M*=1, elastic hyperbolic
deflection at each conjunction (b < R_kick). Event map, vectorized in numpy.

Encounter = conjunction with miss distance b < R_cap (game-scale capture radius).
We log every kick (b < R_kick) and every encounter (b < R_cap). Behaviour, not
trajectory fidelity (PRINCIPLES 2, 20).
"""
import json, sys, time
import numpy as np

TAU = 2 * np.pi

def kepler_solve(M, e, it=5):
    E = M + e * np.sin(M)
    for _ in range(it):
        f = E - e * np.sin(E) - M
        fp = 1 - e * np.cos(E)
        E = E - f / fp
    return E

def elements_to_state(a, e, w, M):
    """Planar Kepler, G*M*=1. Returns position and velocity."""
    E = kepler_solve(M, e)
    cE, sE = np.cos(E), np.sin(E)
    r = a * (1 - e * cE)
    x = a * (cE - e);  y = a * np.sqrt(np.maximum(0.0, 1 - e * e)) * sE
    ca, sa = np.cos(w), np.sin(w)
    X = ca * x - sa * y; Y = sa * x + ca * y
    n = a ** -1.5
    Edot = n / (1 - e * cE)
    vx = -a * sE * Edot; vy = a * np.sqrt(np.maximum(0.0, 1 - e * e)) * cE * Edot
    VX = ca * vx - sa * vy; VY = sa * vx + ca * vy
    return X, Y, VX, VY

def state_to_elements(X, Y, VX, VY):
    r = np.hypot(X, Y); v2 = VX * VX + VY * VY
    eps = v2 / 2 - 1.0 / r
    h = X * VY - Y * VX
    a = -1.0 / (2 * eps)
    rx = (v2 - 1.0 / r) * X - (X * VX + Y * VY) * VX
    ry = (v2 - 1.0 / r) * Y - (X * VX + Y * VY) * VY
    e = np.hypot(rx, ry)
    w = np.arctan2(ry, rx)
    cosnu = (rx * X + ry * Y) / np.maximum(e * r, 1e-300)
    cosnu = np.clip(cosnu, -1, 1)
    nu = np.arccos(cosnu) * np.where(X * VX + Y * VY >= 0, 1, -1)
    E = 2 * np.arctan2(np.sqrt(np.maximum(0, 1 - e)) * np.sin(nu / 2),
                       np.sqrt(np.maximum(0, 1 + e)) * np.cos(nu / 2))
    M = E - e * np.sin(E)
    return a, np.clip(e, 0, 0.97), w, M % TAU

def run(n=300, W=0.08, sig_e=0.05, m=1e-4, R_cap=3e-3, R_kick=None,
        T=400, steps_per_orbit=48, K=8, seed=1, kicks=True, tag=""):
    rng = np.random.default_rng(seed)
    a = 1 - W / 2 + W * rng.random(n)
    e = rng.rayleigh(sig_e, n).clip(1e-4, 0.6)
    w = TAU * rng.random(n)
    M0 = TAU * rng.random(n)
    if R_kick is None:
        R_kick = 10 * R_cap
    dt_orb = TAU / steps_per_orbit
    nsteps = int(T * steps_per_orbit)
    nn = a ** -1.5

    enc = []       # (t, b, chi, dv) for b < R_cap
    kicks_log = []
    ejected = 0
    e_snap = []    # (orbit, e_p50, e_p90, e_p99, a_std, mean_e)
    rate_bins = np.zeros(T + 1, dtype=np.int64)   # encounters per orbit index
    next_ok = {}   # pair -> next allowed conjunction time

    for step in range(nsteps):
        t = step * dt_orb
        M = M0 + nn * t
        # mean longitude (2nd order eq. of center) for detection only
        lam = (M + w + (2 * e - 0.25 * e ** 3) * np.sin(M) + 1.25 * e * e * np.sin(2 * M)) % TAU
        order = np.argsort(lam)
        ls = lam[order]
        pairs = []
        for k in range(1, K + 1):
            dl = ls[k:] - ls[:-k]
            dl = (dl + np.pi) % TAU - np.pi          # wrap to (-pi_, pi_]
            i = order[:-k]; j = order[k:]
            # radial feasibility: bands overlap within R_kick
            feas = np.abs(a[i] - a[j]) < (a[i] * (e[i] + e[j])) + R_kick
            # conjunction if within relative angular motion of this step
            srel = np.abs(nn[i] - nn[j]) + (e[i] + e[j]) * 0.5 * (nn[i] + nn[j])
            hit = feas & (np.abs(dl) < srel * dt_orb)
            for I, J in zip(i[hit], j[hit]):
                key = (int(I), int(J)) if I < J else (int(J), int(I))
                if next_ok.get(key, -1.0) < t:
                    pairs.append(key)
                    next_ok[key] = t + 3 * dt_orb
        if not pairs:
            continue
        pi_ = np.array([p[0] for p in pairs]); pj_ = np.array([p[1] for p in pairs])
        allb = np.concatenate([pi_, pj_])
        Mt = M0[allb] + nn[allb] * t
        X, Y, VX, VY = elements_to_state(a[allb], e[allb], w[allb], Mt)
        Xd = {int(b): k for k, b in enumerate(allb)}
        ii = np.array([Xd[int(x)] for x in pi_]); jj = np.array([Xd[int(x)] for x in pj_])
        bx = X[ii] - X[jj]; by = Y[ii] - Y[jj]
        b = np.hypot(bx, by)
        dvx = VX[ii] - VX[jj]; dvy = VY[ii] - VY[jj]
        v2 = dvx * dvx + dvy * dvy
        v = np.sqrt(v2 + 1e-300)
        mu = 2 * m
        chi = 2 * np.arctan(mu / (b * np.maximum(v2, 1e-12)))
        sel = b < R_kick
        for q in np.nonzero(sel)[0]:
            if b[q] < R_cap:
                enc.append((t, float(b[q]), float(chi[q]), 0.0))
                rate_bins[int(t / TAU)] += 1
            if not kicks:
                continue
            bhat_x = bx[q] / b[q]; bhat_y = by[q] / b[q]
            c = bhat_x * dvy[q] - bhat_y * dvx[q]     # z of b x v
            eps_ = 1.0 if c >= 0 else -1.0
            ang = -eps_ * chi[q]
            ca, sa = np.cos(ang), np.sin(ang)
            ox = ca * dvx[q] - sa * dvy[q]; oy = sa * dvx[q] + ca * dvy[q]
            dvx_r = ox - dvx[q]; dvy_r = oy - dvy[q]  # change of relative velocity
            I_, J_ = int(pi_[q]), int(pj_[q])
            xi, yi, vxi, vyi = X[ii[q]], Y[ii[q]], VX[ii[q]], VY[ii[q]]
            xj, yj, vxj, vyj = X[jj[q]], Y[jj[q]], VX[jj[q]], VY[jj[q]]
            vxi2 = vxi + 0.5 * dvx_r; vyi2 = vyi + 0.5 * dvy_r
            vxj2 = vxj - 0.5 * dvx_r; vyj2 = vyj - 0.5 * dvy_r
            aI, eI, wI, MI = state_to_elements(xi, yi, vxi2, vyi2)
            aJ, eJ, wJ, MJ = state_to_elements(xj, yj, vxj2, vyj2)
            dv_mag = np.hypot(dvx_r, dvy_r)
            kicks_log.append((t, b[q], chi[q], dv_mag))
            if aI > 0 and eI < 0.95:
                a[I_] = aI; e[I_] = eI; w[I_] = wI % TAU; M0[I_] = MI
            else:
                ejected += 1; a[I_] = 50.0; e[I_] = 0.01
            if aJ > 0 and eJ < 0.95:
                a[J_] = aJ; e[J_] = eJ; w[J_] = wJ % TAU; M0[J_] = MJ
            else:
                ejected += 1; a[J_] = 50.0; e[J_] = 0.01
        if step % steps_per_orbit == 0:
            o = step // steps_per_orbit
            e_snap.append((o, *np.percentile(e, [50, 90, 99]), float(a.std()), float(e.mean())))
    return dict(enc=enc, kicks=kicks_log, e_snap=e_snap, rate=rate_bins,
                ejected=ejected, n=n, T=T)

if __name__ == "__main__":
    t0 = time.time()
    cfg = json.loads(sys.argv[1])
    out = run(**cfg)
    cfg2 = {k: v for k, v in cfg.items()}
    np.save(f"raw_{cfg.get('tag','x')}.npy",
            np.array([(round(t, 3), round(b, 6), round(c, 4), round(d, 8)) for t, b, c, d in out["enc"]],
                     dtype=np.float64), allow_pickle=True)
    snaps = out["e_snap"]
    res = dict(tag=cfg.get("tag", ""), cfg=cfg2,
               n_enc=len(out["enc"]), n_kicks=len(out["kicks"]), ejected=out["ejected"],
               wall_s=round(time.time() - t0, 1),
               e_snap=[(o, round(p50, 4), round(p90, 4), round(p99, 4), round(sd, 4), round(me, 4))
                       for o, p50, p90, p99, sd, me in snaps],
               rate_per_orbit=[int(x) for x in out["rate"]])
    with open(f"res_{cfg.get('tag','x')}.json", "w") as f:
        json.dump(res, f)
    print(cfg.get("tag"), "encounters", res["n_enc"], "kicks", res["n_kicks"],
          "wall", res["wall_s"])
