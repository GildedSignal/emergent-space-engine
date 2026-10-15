#!/usr/bin/env python3
"""The flux accumulator's feedback loop, against a pairwise oracle.

Planar Kepler belt (G=1, star=1). Oracle: continuous pairwise transverse
impulses dv = 2 mu / (b v_rel), momentum-antisymmetric, detected on a theta-sort
grid. Arms (window = 1 mean orbit, zero pair tests):
  A     per-body VECTOR accumulator, local-density flux, golden-angle directions,
        quantum q kicks when |S| >= q, remainder carried (the proposal)
  A_glob A with global mean density (negative control)
  B     per-body Poisson sampling of physical encounters (control, must pass)
  C     scalar coherent accumulator (negative control, must fail)
Scenes: uniform (seeds), clump (200 co-orbital bodies held out).
Output: JSON rows (arm, scene, seed, q, window, mean_e, p99_e, heat_rate, kickstats).
"""
import json, sys, math
import numpy as np

RNG_PHI = 0.6180339887498949
B0 = 0.01          # detection / flux cut (impact parameter)
MU = 3e-8          # body mass (star = 1)
N = 2000
E0 = 0.02          # Rayleigh sigma at birth
A_LO, A_HI = 1.0, 1.6
STEPS_PER_ORBIT = 60
DT = 0.13 * STEPS_PER_ORBIT / STEPS_PER_ORBIT  # set below properly
W = STEPS_PER_ORBIT                       # window in steps
WINDOWS = 40
NSTEP = W * WINDOWS
DT = 2 * math.pi * 1.2 ** 1.5 / STEPS_PER_ORBIT  # mean orbit / 60

# ---------- Kepler helpers (e small; Newton on E) ----------
def states(a, e, w, M):
    E = M.copy()
    for _ in range(4):
        E -= (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    c, s = np.cos(E), np.sin(E)
    r = a * (1 - e * c)
    x = a * (c - e); y = a * math.sqrt(1 - e * e) * s
    ca, sa = np.cos(w), np.sin(w)
    rx = ca * x - sa * y; ry = sa * x + ca * y
    n = a ** -1.5
    vf = n * a / math.sqrt(1 - e * e) * (-s); vg = n * a / math.sqrt(1 - e * e) * (c - e)
    vx = ca * vf - sa * vg; vy = sa * vf + ca * vg
    return rx, ry, vx, vy

def rebind(rx, ry, vx, vy):
    """impulse applied; recompute (a, e, w, M) from state"""
    r2 = rx * rx + ry * ry; r = np.sqrt(r2)
    v2 = vx * vx + vy * vy
    a = 1.0 / (2.0 / r - v2)
    Lz = rx * vy - ry * vx
    # eccentricity vector: (v x L)/mu_star - r_hat , mu_star = 1
    ex = vy * Lz - rx / r; ey = -vx * Lz - ry / r
    e = np.hypot(ex, ey)
    w = np.arctan2(ey, ex)
    # true anomaly from dot(r, e)
    cosv = (rx * ex + ry * ey) / (r * np.maximum(e, 1e-12))
    cosv = np.clip(cosv, -1, 1)
    nu = np.sign(rx * vy - ry * vx - 0) * np.arccos(cosv)  # sign by angular order
    # sign of nu: cross(r, e_vec)? use cross(r, e) z: r x e
    crossz = rx * ey - ry * ex
    nu = np.where(crossz < 0, -nu, nu)
    E2 = 2 * np.arctan2(math.sqrt(1) * np.sin(nu / 2), np.sqrt(1) * np.cos(nu / 2) + 0)
    E2 = 2 * np.arctan2(np.sqrt(1 - e * e) * np.sin(nu), e + np.cos(nu)) / 1
    E2 = 2 * np.arctan2(np.sqrt(np.maximum(1 - e * e, 0)) * np.sin(nu), e + np.cos(nu))
    M = E2 - e * np.sin(E2)
    return a, e, w, M

def birth(seed, clump=False):
    rng = np.random.default_rng(seed)
    a = np.empty(N); e = np.empty(N); w = np.empty(N); M = np.empty(N)
    if clump:
        nc = 200
        a[:nc] = 1.29 + 0.02 * rng.random(nc)
        e[:nc] = np.abs(rng.rayleigh(0.01, nc))
        M[:nc] = rng.uniform(-0.15, 0.15, nc)
        w[:nc] = rng.uniform(0, 2 * math.pi, nc)
        rest = slice(nc, N)
    else:
        nc = 0; rest = slice(0, N)
    a[rest] = A_LO + (A_HI - A_LO) * rng.random(N - nc)
    e[rest] = np.abs(rng.rayleigh(E0, N - nc))
    M[rest] = rng.uniform(0, 2 * math.pi, N - nc)
    w[rest] = rng.uniform(0, 2 * math.pi, N - nc)
    return a, e, w, M

# ---------- oracle ----------
def oracle(seed, clump=False):
    a, e, w, M = birth(seed, clump)
    n = a ** -1.5
    rows = []
    kicks = 0; dv2_tot = 0.0; pair_sum = 0.0
    for step in range(NSTEP):
        M = (M + n * DT) % (2 * math.pi)
        rx, ry, vx, vy = states(a, e, w, M)
        th = np.arctan2(ry, rx) % (2 * math.pi)
        order = np.argsort(th)
        rxs = rx[order]; rys = ry[order]; vxs = vx[order]; vys = vy[order]
        th_s = th[order]
        for k in (1, 2, 3, 4):
            dth = np.diff(th_s, append=th_s[0] + 2 * math.pi)
            rmid = 0.5 * (np.hypot(rxs, rys) + np.hypot(np.roll(rxs, -1), np.roll(rys, -1)))
            arc = dth * rmid
            dr = np.hypot(np.roll(rxs, -1) - rxs, np.roll(rys, -1) - rys)
            sel = (arc < 1.5 * B0) & (dr < B0)
            i = np.nonzero(sel)[0]
            if i.size:
                j = (i + k) % N
                b = np.maximum(dr[i], 1e-9)
                dvx = vxs[j] - vxs[i]; dvy = vys[j] - vys[i]
                vrel = np.maximum(np.hypot(dvx, dvy), 1e-6)
                bmin = 4 * MU / (vrel * vrel)
                A = 2 * MU / (np.maximum(b, bmin) * vrel)
                # transverse unit to relative velocity
                mx = -dvy / vrel; my = dvx / vrel
                si = order[i]; sj = order[j]
                ei = np.arange(i.size)
                # apply antisymmetric impulse via rebind on the small arrays
                for (idx, sgn) in ((si, +1), (sj, -1)):
                    pass
                # vectorised rebind of both members
                na1, ne1, nw1, nm1 = rebind(rx[si] * 1, ry[si], vx[si] + sgn * 0, vy[si])
                # (placeholder replaced below)
                kick_i = np.stack([sgn * 0 for sgn in (1, 1)])  # noqa
                # real application:
                na_i, ne_i, nw_i, nm_i = rebind(rx[si], ry[si],
                                                vx[si] + A * mx * (+1), vy[si] + A * my * (+1))
                na_j, ne_j, nw_j, nm_j = rebind(rx[sj], ry[sj],
                                                vx[sj] - A * mx * (+1), vys[sj] - A * my * (+1))
                a[si] = na_i; e[si] = ne_i; w[si] = nw_i; M[si] = nm_i % (2 * math.pi)
                a[sj] = na_j; e[sj] = ne_j; w[sj] = nw_j; M[sj] = nm_j % (2 * math.pi)
                kicks += 2 * i.size; dv2_tot += float(np.sum(2 * A * A)); pair_sum += i.size
        if (step + 1) % W == 0:
            win = (step + 1) // W
            rows.append(dict(arm="oracle", seed=seed, scene="clump" if clump else "uniform",
                             q=0.0, window=win, mean_e=float(e.mean()),
                             p99_e=float(np.quantile(e, 0.99)),
                             heat=float((e * e).mean()), kicks_per_body=kicks / N,
                             dv2_per_body=dv2_tot / N))
    return rows

# ---------- accumulator arms ----------
NR, NTH = 6, 16
R_EDGES = np.linspace(0.8, 1.85, NR + 1)

def cell_rho(rx, ry):
    r = np.hypot(rx, ry); th = np.arctan2(ry, rx) % (2 * math.pi)
    ci = np.clip(np.digitize(r, R_EDGES) - 1, 0, NR - 1)
    cj = (th / (2 * math.pi) * NTH).astype(int) % NTH
    key = ci * NTH + cj
    cnt = np.bincount(key, minlength=NR * NTH).astype(float)
    # cell area = dr * r_mid * dth
    area = np.array([ (R_EDGES[i+1]-R_EDGES[i]) * 0.5*(R_EDGES[i+1]+R_EDGES[i]) * (2*math.pi/NTH)
                      for i in range(NR) ]).repeat(NTH)
    return cnt[key] / area[key], cnt[key]

def local_vrel(rx, ry, vx, vy):
    """speed dispersion about the circular shear flow, per cell (the honest local read)"""
    r = np.hypot(rx, ry); th = np.arctan2(ry, rx) % (2 * math.pi)
    ci = np.clip(np.digitize(r, R_EDGES) - 1, 0, NR - 1)
    cj = (th / (2 * math.pi) * NTH).astype(int) % NTH
    key = ci * NTH + cj
    vcirc = 1.0 / np.sqrt(np.maximum(r, 0.1))
    du = vx + vcirc * np.sin(th)   # deviation from circular flow (circular: v = vc*(-sin, cos))
    dv = vy - vcirc * np.cos(th)
    mean_u = np.bincount(key, weights=du, minlength=NR*NTH)
    mean_v = np.bincount(key, weights=dv, minlength=NR*NTH)
    cnt = np.maximum(np.bincount(key, minlength=NR*NTH), 1)
    sig = np.sqrt((mean_u/cnt)**2 + (mean_v/cnt)**2)  # placeholder; full var below
    var = np.bincount(key, weights=du*du+dv*dv, minlength=NR*NTH)/cnt - sig**2
    return np.sqrt(np.maximum(var[key], 1e-8))

def apply_dv(a, e, w, M, dvx, dvy):
    rx, ry, vx, vy = states(a, e, w, M)
    na, ne, nw, nm = rebind(rx, ry, vx + dvx, vy + dvy)
    return na, ne, nw, nm % (2 * math.pi)

def accumulator(seed, clump, arm, q, rng):
    a, e, w, M = birth(seed, clump)
    n = a ** -1.5
    Sx = np.zeros(N); Sy = np.zeros(N); c = np.zeros(N)
    gidx = np.arange(N); rot = (RNG_PHI * (gidx * 0.754977 + 1.0)) % 1.0
    rows = []; kicks = 0; dv2 = 0.0; apps = 0
    rho_glob = N / (math.pi * (1.75**2 - 0.85**2))
    dtw = DT * W
    for win in range(WINDOWS):
        M = (M + n * dtw) % (2 * math.pi)
        rx, ry, vx, vy = states(a, e, w, M)
        rho_loc, cnt = cell_rho(rx, ry)
        rho = rho_glob if arm == "A_glob" else rho_loc
        vrel = np.maximum(local_vrel(rx, ry, vx, vy), 5e-3)
        bmin = 4 * MU / vrel**2
        flux = 4 * MU * rho * np.log(B0 / bmin) * dtw   # |dv| flux per window (2-D law)
        if arm in ("A", "A_glob"):
            rot = (rot + RNG_PHI) % 1.0
            Sx += flux * np.cos(2*math.pi*rot); Sy += flux * np.sin(2*math.pi*rot)
            Sm = np.hypot(Sx, Sy)
            hit = Sm >= q
            if hit.any():
                ux = Sx[hit]/Sm[hit]; uy = Sy[hit]/Sm[hit]
                dvx = np.zeros(N); dvy = np.zeros(N)
                dvx[hit] = q*ux; dvy[hit] = q*uy
                a, e, w, M = apply_dv(a, e, w, M, dvx, dvy)
                Sx[hit] -= q*ux; Sy[hit] -= q*uy
                kicks += int(hit.sum()); dv2 += float(np.sum(dvx[dvx!=0]**2 + dvy[dvy!=0]**2)); apps += int(hit.sum())
        elif arm == "C":
            c += flux
            hit = c >= q
            if hit.any():
                rot = (rot + RNG_PHI) % 1.0
                dvx = np.zeros(N); dvy = np.zeros(N)
                dvx[hit] = q*np.cos(2*math.pi*rot[hit]); dvy[hit] = q*np.sin(2*math.pi*rot[hit])
                a, e, w, M = apply_dv(a, e, w, M, dvx, dvy)
                c[hit] -= q; kicks += int(hit.sum()); apps += int(hit.sum())
        elif arm == "B":
            lam = 2 * rho * vrel * B0 * dtw
            nk = rng.poisson(lam)
            tot = int(nk.sum())
            if tot:
                bi = np.repeat(np.arange(N), np.maximum(nk, 0))
                u = rng.random(tot)
                b = B0 * np.sqrt(u)
                A = np.minimum(2*MU/(np.maximum(b, bmin[bi]) * vrel[bi]), 0.5*vrel[bi])
                ang = rng.random(tot) * 2 * math.pi
                dvx = np.zeros(N); dvy = np.zeros(N)
                np.add.at(dvx, bi, A*np.cos(ang)); np.add.at(dvy, bi, A*np.sin(ang))
                a, e, w, M = apply_dv(a, e, w, M, dvx, dvy)
                kicks += tot; dv2 += float(np.sum(A*A))
        rows.append(dict(arm=arm, seed=seed, scene="clump" if clump else "uniform",
                         q=q, window=win+1, mean_e=float(e.mean()),
                         p99_e=float(np.quantile(e, 0.99)), heat=float((e*e).mean()),
                         kicks_per_body=kicks/N, dv2_per_body=dv2/N))
    return rows

def main():
    out = []
    seeds = [1, 2, 3, 4, 5]
    for s in seeds:
        out += oracle(s); print("oracle u", s, file=sys.stderr)
    out += oracle(11, clump=True); print("oracle c", file=sys.stderr)
    for s in seeds:
        for arm, qs in (("A", [3e-4, 1e-3, 3e-3, 1e-2]), ("B", [1e-3]), ("C", [1e-3]), ("A_glob", [1e-3])):
            for q in qs:
                out += accumulator(s, False, arm, q, np.random.default_rng(1000+s)); 
        print("arm u", s, file=sys.stderr)
    for arm, q in (("A", 1e-3), ("B", 1e-3), ("C", 1e-3), ("A_glob", 1e-3)):
        out += accumulator(11, True, arm, q, np.random.default_rng(1011))
    print("arm c", file=sys.stderr)
    json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "rows.json", "w"))

if __name__ == "__main__":
    main()
