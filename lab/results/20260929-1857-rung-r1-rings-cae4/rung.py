"""Rung r1: orbits in rings around one mass — six configurations, frozen cases, metrics.

Rings (binet/river): edges at r = 2^(k/m); band k spans r in [2^(k/m), 2^((k+1)/m));
centre r_k = 2^((k+0.5)/m); u_k = 2^(-(k+0.5)/m) (geometric-centre value).

binet: in band k, u'' + (1-6u_k)u = 1/L^2 - 3u_k^2 (light: drop 1/L^2); exact band
solution (rotation if 1-6u_k>0, hyperbolic otherwise); u, u' continuous across bands.
dt per band = int E/(L u^2 (1-2u)) dphi over the traversed phi-interval, 16-pt GL.
Absorbed when u >= 1/2 (r <= 2).

river: in ring k flow beta_k = -sqrt(2/r_k) rhat; H = sqrt(1+|p|^2) + beta.p (light
|p| + beta.p), canonical p; H and L conserved at rings; no real root -> reflection.
Within-ring motion integrated in r by quadrature; A^2 = H^2 - (1-b^2)(1+L^2/r^2)
(massive) / H^2 - (1-b^2)L^2/r^2 (light); in-ring turning r_t where A = 0.

square (negative): dyadic squares, side 2^n, n = round(log2(r/16)) (side within
sqrt(2) of r/16); constant flow per cell (magnitude sqrt(2/r_c), pointing from the
cell centre to the mass); straight motion within a cell; H and L conserved at edges
(radial momentum solved about the mass; no real root -> reflection in the old cell).

tiltonly (negative): kick rotating v toward the mass, |v| kept: dalpha = |a x v|/v^2
dt with a = -rhat/r^2; drift-rotate-drift step, dt = T_kepler/256.

Sampler: random.Random(20260930); bound: p = 10**uniform(1,3), e = uniform(0,0.7),
redraw unless p >= 6.5+2e, 256 kept; light: b = 10**uniform(1,3), 64 draws.
"""
import json
import math
import random
import sys
import time

import numpy as np

from oracle import (PI, periapsis_elliptic, deflection_quadrature, bound_constants,
                    bound_period_quad, light_tail, gl)

TWOPI = 2.0 * np.pi
PERI, APO, CROSS, STOP = 0, 1, 2, 4

GL16 = gl(16)
GLX = np.array(GL16[0]); GLW = np.array(GL16[1])


# ---------------------------------------------------------------- seeds
def draw_seeds():
    rng = random.Random(20260930)
    bound = []
    while len(bound) < 256:
        p = 10.0 ** rng.uniform(1.0, 3.0)
        e = rng.uniform(0.0, 0.7)
        if p < 6.5 + 2.0 * e:
            continue
        bound.append((p, e))
    light = [10.0 ** rng.uniform(1.0, 3.0) for _ in range(64)]
    return bound, light


BOUND, LIGHT_B = draw_seeds()


def bound_EL(pe_list):
    p = np.array([a for a, _ in pe_list])
    e = np.array([b for _, b in pe_list])
    E, L = bound_constants(p, e)
    return p, e, E, L


def lcirc(r):
    return r / math.sqrt(r - 3.0)


def ecirc(r):
    return (1.0 - 2.0 / r) / math.sqrt(1.0 - 3.0 / r)


CAP_LT = [4.0 * v for v in (0.5, 0.9, 0.97, 1.03, 1.1, 1.5)]
CAP_PH = [3.0 * math.sqrt(3.0) * v for v in (0.9, 0.97, 1.03, 1.1)]
CAP_TRUTH = np.array([True] * 3 + [False] * 3 + [True] * 2 + [False] * 2)
U_LIGHT_START = 1e-4


# ================================================================ binet engine
def binet_run(u0, up0, E, L, m, light, ncyc, esc_u=None, phi_max=None,
              seq_cycles=2, trace_lanes=(), max_iter=30_000_000):
    """Vectorised over lanes. Returns per-cycle dphi/dt/nc/up/ua (kept cycles close at
    periapsis events), absorbed/escaped, first two cycles' band sequences, phi totals."""
    N = len(u0)
    u = np.array(u0, float)
    up = np.array(up0, float)
    E = np.broadcast_to(np.asarray(E, float), (N,)).copy()
    L = np.broadcast_to(np.asarray(L, float), (N,)).copy()
    kk = np.floor(-m * np.log2(u))
    Cmax = int(np.max(ncyc)) if np.ndim(ncyc) else int(ncyc)
    ncyc_a = (np.broadcast_to(np.asarray(ncyc), (N,)).astype(int) if np.ndim(ncyc)
              else np.full(N, int(ncyc)))
    out_dphi = np.full((N, Cmax), np.nan); out_dt = np.full((N, Cmax), np.nan)
    out_nc = np.zeros((N, Cmax)); out_up = np.full((N, Cmax), np.nan)
    out_ua = np.full((N, Cmax), np.nan)
    absorbed = np.zeros(N, bool); escaped = np.zeros(N, bool)
    cyc = np.zeros(N, int)
    phi_c = np.zeros(N); t_c = np.zeros(N); nc_c = np.zeros(N, int)
    ua_c = np.zeros(N); phi_tot = np.zeros(N)
    seqs = ([[] for _ in range(N)], [[] for _ in range(N)])
    trace = {i: [] for i in trace_lanes}
    active = np.ones(N, bool)
    esc_u = np.zeros(N) if esc_u is None else np.asarray(esc_u, float)
    phi_max = np.full(N, np.inf) if phi_max is None else np.asarray(phi_max, float)
    invL2 = (0.0 if light else 1.0) / L ** 2
    stop_lane = esc_u > 0.0
    it = 0
    while active.any():
        it += 1
        if it > max_iter:
            break
        uk = 2.0 ** (-(kk + 0.5) / m)
        w2 = 1.0 - 6.0 * uk
        osc = w2 > 0.0
        rhs = invL2 - 3.0 * uk * uk
        u_hi = 2.0 ** (-kk / m)
        u_lo = 2.0 ** (-(kk + 1.0) / m)
        with np.errstate(all="ignore"):
            om = np.sqrt(np.where(osc, w2, 1.0))
            C_ = np.where(osc, rhs / np.where(osc, w2, 1.0), 0.0)
            dc = u - C_
            th0 = np.arctan2(-up / om, dc)
            Q = np.hypot(dc, up / om)
            th_t = (np.floor(th0 / PI) + 1.0) * PI
            th_t = np.where(th_t <= th0 + 1e-13, th_t + PI, th_t)

            def osc_edge(u_e):
                g = (u_e - C_) / Q
                ok = (np.abs(g) <= 1.0) & osc & (Q > 0.0)
                a = np.arccos(np.clip(g, -1.0, 1.0))
                c1 = a + TWOPI * np.ceil((th0 - a) / TWOPI)
                c1 = np.where(c1 <= th0 + 1e-13, c1 + TWOPI, c1)
                c2 = -a + TWOPI * np.ceil((th0 + a) / TWOPI)
                c2 = np.where(c2 <= th0 + 1e-13, c2 + TWOPI, c2)
                the = np.minimum(c1, c2)
                return np.where(ok, (the - th0) / om, np.inf), the

            dphi_hi_o, th_hi = osc_edge(u_hi)
            dphi_lo_o, th_lo = osc_edge(u_lo)
            dphi_st_o, th_st = osc_edge(np.where(stop_lane, esc_u, u_lo))
            lam = np.sqrt(np.where(~osc, -w2, 1.0))
            Ch = np.where(~osc, rhs / np.where(~osc, w2, -1.0), 0.0)
            dch = u - Ch
            Hc = 0.5 * (dch + up / lam)
            Gc = 0.5 * (dch - up / lam)
            Hc_s = np.where(Hc == 0.0, 1e-300, Hc)
            ratio = Gc / Hc_s
            turn_h = (~osc) & (ratio > 1.0 + 1e-13)
            zt = np.sqrt(np.where(turn_h, ratio, 1.0))

            def hyp_edge(u_e):
                D = u_e - Ch
                disc = D * D - 4.0 * Hc * Gc
                ok = (~osc) & (disc >= 0.0)
                sq = np.sqrt(np.where(ok, disc, 0.0))
                z1 = np.where(ok & ((D - sq) / (2.0 * Hc_s) > 1.0 + 1e-13), (D - sq) / (2.0 * Hc_s), np.inf)
                z2 = np.where(ok & ((D + sq) / (2.0 * Hc_s) > 1.0 + 1e-13), (D + sq) / (2.0 * Hc_s), np.inf)
                ze = np.minimum(z1, z2)
                return np.where(np.isfinite(ze), np.log(ze) / lam, np.inf), ze

            dphi_hi_h, z_hi = hyp_edge(u_hi)
            dphi_lo_h, z_lo = hyp_edge(u_lo)
            dphi_st_h, z_st = hyp_edge(np.where(stop_lane, esc_u, u_lo))
            dphi_t = np.where(osc, np.where(osc, (th_t - th0) / om, np.inf),
                              np.where(turn_h, np.log(zt) / lam, np.inf))
            kind_t = np.where(osc,
                              np.where(np.mod(np.round(th_t / PI), 2.0) == 0.0, PERI, APO),
                              np.where(Hc_s < 0.0, PERI, APO))
            dphi_hi = np.where(osc, dphi_hi_o, dphi_hi_h)
            dphi_lo = np.where(osc, dphi_lo_o, dphi_lo_h)
            dphi_st = np.where(osc, dphi_st_o, dphi_st_h)
            dphi = np.minimum(dphi_t, np.minimum(dphi_hi, np.minimum(dphi_lo, dphi_st)))
            kind = np.where(dphi == dphi_t, kind_t,
                            np.where(dphi == dphi_hi, CROSS,
                                     np.where(dphi == dphi_lo, CROSS, STOP)))
            inward = dphi == dphi_hi
            th_sel = np.where(inward, th_hi, np.where(kind == STOP, th_st, th_lo))
            ze = np.where(inward, z_hi, np.where(kind == STOP, z_st, z_lo))
            up_ev = np.where(osc,
                             -Q * om * np.sin(th_sel),
                             lam * (Hc * ze - Gc / ze))
            u_ev = np.where(inward, u_hi,
                            np.where(kind == STOP, np.where(stop_lane, esc_u, u_lo), u_lo))
            is_turn = (kind == PERI) | (kind == APO)
            u_ev = np.where(is_turn,
                            np.where(osc, C_ + Q * np.cos(th_t), Ch + Hc * zt + Gc / zt),
                            u_ev)
            up_ev = np.where(is_turn, 0.0, up_ev)
            dphi = np.where(np.isfinite(dphi), dphi, 1e9)
            phj = 0.5 * dphi[:, None] * (1.0 + GLX)[None, :]
            uj_o = C_[:, None] + Q[:, None] * np.cos(th0[:, None] + om[:, None] * phj)
            zj = np.exp(lam[:, None] * phj)
            uj = np.where(osc[:, None], uj_o,
                          Ch[:, None] + Hc[:, None] * zj + Gc[:, None] / zj)
            uj = np.clip(uj, 1e-300, 0.5 - 1e-12)
            fj = E[:, None] / (L[:, None] * uj * uj * (1.0 - 2.0 * uj))
            dtev = 0.0 if light else 0.5 * dphi * (fj @ GLW)
        for i in trace:
            if active[i]:
                for j in range(16):
                    trace[i].append((phi_tot[i] + phj[i, j], float(uj[i, j])))
        dphi = np.where(active, dphi, 0.0)
        phi_c += dphi; phi_tot += dphi; t_c += np.where(active, dtev, 0.0)
        cross = (kind == CROSS) & active
        nc_c += cross
        ua_c = np.where(kind == APO, u_ev, ua_c)
        u = u_ev; up = up_ev
        kk = np.where(inward, kk - 1.0, np.where(cross, kk + 1.0, kk))
        absorb_ev = cross & inward & (u_ev >= 0.5 - 1e-12)
        absorb_ev &= active
        if seq_cycles > 0 and cross.any():
            idx = np.nonzero(cross & active & (cyc < seq_cycles))[0]
            for i in idx:
                seqs[cyc[i]][i].append(int(kk[i]))
        for i in np.nonzero((kind == PERI) & active & ~absorb_ev)[0]:
            c = cyc[i]
            if c < Cmax:
                out_dphi[i, c] = phi_c[i]; out_dt[i, c] = t_c[i]
                out_nc[i, c] = nc_c[i]; out_up[i, c] = u_ev[i]; out_ua[i, c] = ua_c[i]
            cyc[i] += 1
            phi_c[i] = 0.0; t_c[i] = 0.0; nc_c[i] = 0; ua_c[i] = 0.0
        esc_ev = (~absorb_ev) & (up_ev < 0) & (u_ev <= esc_u * (1.0 + 1e-15)) & active
        absorbed |= absorb_ev; escaped |= esc_ev
        active &= ~(absorb_ev | esc_ev | (cyc >= ncyc_a) | (phi_tot >= phi_max))
    return dict(dphi=out_dphi, dt=out_dt, nc=out_nc, up=out_up, ua=out_ua,
                absorbed=absorbed, escaped=escaped, seq=seqs, trace=trace,
                phi_tot=phi_tot)


# ================================================================ river engine
def river_run(r0, s0, H, L, m, light, ncyc, esc_r=None, phi_max=None,
              seq_cycles=2, trace_lanes=(), max_iter=30_000_000):
    N = len(r0)
    r = np.array(r0, float)
    s = np.array(s0, float)
    H = np.broadcast_to(np.asarray(H, float), (N,)).copy()
    L = np.broadcast_to(np.asarray(L, float), (N,)).copy()
    kk = np.floor(m * np.log2(r))
    b2 = 2.0 / 2.0 ** ((kk + 0.5) / m)
    one = 0.0 if light else 1.0
    A2_0 = H * H - (1.0 - b2) * (one + L * L / (r * r))
    with np.errstate(all="ignore"):
        rt0 = np.sqrt(np.where(light, (1.0 - b2) * L * L / (H * H),
                               (1.0 - b2) * L * L / np.maximum(H * H - (1.0 - b2), 1e-300)))
    r = np.where(A2_0 < 0, rt0, r)
    Cmax = int(np.max(ncyc)) if np.ndim(ncyc) else int(ncyc)
    ncyc_a = (np.broadcast_to(np.asarray(ncyc), (N,)).astype(int) if np.ndim(ncyc)
              else np.full(N, int(ncyc)))
    out_dphi = np.full((N, Cmax), np.nan); out_dt = np.full((N, Cmax), np.nan)
    out_nc = np.zeros((N, Cmax)); out_rp = np.full((N, Cmax), np.nan)
    out_ra = np.full((N, Cmax), np.nan)
    absorbed = np.zeros(N, bool); escaped = np.zeros(N, bool)
    cyc = np.zeros(N, int)
    phi_c = np.zeros(N); t_c = np.zeros(N); nc_c = np.zeros(N, int)
    ra_c = np.zeros(N); phi_tot = np.zeros(N)
    seqs = ([[] for _ in range(N)], [[] for _ in range(N)])
    trace = {i: [] for i in trace_lanes}
    active = np.ones(N, bool)
    esc_r = np.full(N, np.inf) if esc_r is None else np.asarray(esc_r, float)
    phi_max = np.full(N, np.inf) if phi_max is None else np.asarray(phi_max, float)
    it = 0
    while active.any():
        it += 1
        if it > max_iter:
            break
        k_lo = 2.0 ** (kk / m)
        k_hi = 2.0 ** ((kk + 1.0) / m)
        beta2 = 2.0 / 2.0 ** ((kk + 0.5) / m)
        with np.errstate(all="ignore"):
            rt = np.sqrt(np.where(light, (1.0 - beta2) * L * L / (H * H),
                                  (1.0 - beta2) * L * L
                                  / np.maximum(H * H - (1.0 - beta2), 1e-300)))
        rt_ok = np.where(light, np.isfinite(rt) & (rt > 0),
                         (H * H > (1.0 - beta2)) & (rt > 0))
        out_b = s > 0
        r_b = np.where(out_b, k_hi, k_lo)
        r_b = np.where(out_b & (esc_r < r_b) & (esc_r > r), esc_r, r_b)
        turn_exit = rt_ok & np.where(out_b, (r < rt) & (rt < r_b),
                                     (rt < r) & (rt > r_b))
        r_b = np.where(turn_exit, rt, r_b)
        kind = np.where(turn_exit, np.where(out_b, APO, PERI), CROSS)
        with np.errstate(all="ignore"):
            if turn_exit.any():
                side = np.where(out_b, -1.0, 1.0)  # r(q) = r_b + side*q^2, from r to r_b
                qmax = np.sqrt(np.abs(r - r_b))
                qj = 0.5 * qmax[:, None] * (1.0 + GLX)[None, :]
                rj = r_b[:, None] + side[:, None] * qj * qj
                wq = qj * qmax[:, None] * GLW[None, :]
            else:
                rj = r[:, None] + (r_b - r)[:, None] * (0.5 * (1.0 + GLX)[None, :])
                wq = 0.5 * np.abs(r_b - r)[:, None] * GLW[None, :]
            A2j = H[:, None] ** 2 - (1.0 - beta2)[:, None] * (one + L[:, None] ** 2 / rj ** 2)
            Aj = np.sqrt(np.maximum(A2j, 1e-300))
            dphi = (L[:, None] / (rj * rj * Aj) * wq).sum(axis=1)
            gam = (H[:, None] - s[:, None] * np.sqrt(beta2)[:, None] * Aj) / (1.0 - beta2)[:, None]
            dtev = 0.0 if light else (gam / Aj * wq).sum(axis=1)
        for i in trace:
            if active[i]:
                trace[i].append((phi_tot[i] + 0.5 * dphi[i], float(r[i])))
                trace[i].append((phi_tot[i] + dphi[i], float(r_b[i])))
        dphi = np.where(active, dphi, 0.0)
        dtev = np.where(active, dtev, 0.0)
        phi_c += dphi; phi_tot += dphi; t_c += dtev
        ra_c = np.maximum(ra_c, np.maximum(r, r_b))
        kk_try = np.where(out_b, kk + 1.0, kk - 1.0)
        beta2_try = 2.0 / 2.0 ** ((kk_try + 0.5) / m)
        A2_try = H * H - (1.0 - beta2_try) * (one + L * L / (r_b * r_b))
        absorb_ev = (kind == CROSS) & ~out_b & (kk <= m) & active
        enter = (kind == CROSS) & (A2_try >= 0) & ~absorb_ev
        reflect = (kind == CROSS) & ~enter & ~absorb_ev
        ra_c = np.where(reflect, np.maximum(ra_c, r_b), ra_c)
        kk = np.where(enter, kk_try, kk)
        s = np.where(enter, s, -s)
        r = r_b
        if seq_cycles > 0 and enter.any():
            idx = np.nonzero(enter & active & (cyc < seq_cycles))[0]
            for i in idx:
                seqs[cyc[i]][i].append(int(kk[i]))
        for i in np.nonzero((kind == PERI) & active & ~absorb_ev)[0]:
            c = cyc[i]
            if c < Cmax:
                out_dphi[i, c] = phi_c[i]; out_dt[i, c] = t_c[i]
                out_nc[i, c] = nc_c[i]; out_rp[i, c] = r_b[i]; out_ra[i, c] = ra_c[i]
            cyc[i] += 1
            phi_c[i] = 0.0; t_c[i] = 0.0; nc_c[i] = 0; ra_c[i] = 0.0
        esc_ev = (~absorb_ev) & (s > 0) & (r >= esc_r * (1.0 - 1e-9)) & active
        absorbed |= absorb_ev; escaped |= esc_ev
        active &= ~(absorb_ev | esc_ev | (cyc >= ncyc_a) | (phi_tot >= phi_max))
    return dict(dphi=out_dphi, dt=out_dt, nc=out_nc, rp=out_rp, ra=out_ra,
                absorbed=absorbed, escaped=escaped, seq=seqs, trace=trace,
                phi_tot=phi_tot)


# ================================================================ square engine
def square_flow(x, y):
    """Cell flow (bx, by) for the dyadic cell containing (x, y)."""
    r = np.maximum(np.hypot(x, y), 1e-12)
    n = np.clip(np.rint(np.log2(r / 16.0)), -40, 60)
    sn = 2.0 ** n
    i = np.floor(x / sn); j = np.floor(y / sn)
    cx = (i + 0.5) * sn; cy = (j + 0.5) * sn
    rc = np.maximum(np.hypot(cx, cy), 1e-300)
    bm = np.sqrt(2.0 / rc)
    return -bm * cx / rc, -bm * cy / rc, n, i, j, sn


def square_run(x0, y0, px0, py0, ncyc, esc_r=None, phi_max=None, light=False,
               seq_cycles=2, trace_lanes=(), max_iter=30_000_000):
    N = len(x0)
    x = np.array(x0, float); y = np.array(y0, float)
    px = np.array(px0, float); py = np.array(py0, float)
    Cmax = int(np.max(ncyc)) if np.ndim(ncyc) else int(ncyc)
    ncyc_a = (np.broadcast_to(np.asarray(ncyc), (N,)).astype(int) if np.ndim(ncyc)
              else np.full(N, int(ncyc)))
    out_dphi = np.full((N, Cmax), np.nan); out_dt = np.full((N, Cmax), np.nan)
    out_nc = np.zeros((N, Cmax)); out_rp = np.full((N, Cmax), np.nan)
    out_ra = np.full((N, Cmax), np.nan)
    absorbed = np.zeros(N, bool); escaped = np.zeros(N, bool)
    cyc = np.zeros(N, int)
    phi_c = np.zeros(N); t_c = np.zeros(N); nc_c = np.zeros(N, int)
    ra_c = np.hypot(x, y); phi_tot = np.zeros(N)
    seqs = ([[] for _ in range(N)], [[] for _ in range(N)])
    trace = {i: [] for i in trace_lanes}
    active = np.ones(N, bool)
    esc_r = np.full(N, np.inf) if esc_r is None else np.asarray(esc_r, float)
    phi_max = np.full(N, np.inf) if phi_max is None else np.asarray(phi_max, float)
    one = 0.0 if light else 1.0
    it = 0
    while active.any():
        it += 1
        if it > max_iter:
            break
        bx, by, n, ci, cj, sn = square_flow(x, y)
        gam = np.sqrt(one + px * px + py * py)
        Hv = gam + bx * px + by * py
        vx = px / gam + bx; vy = py / gam + by
        with np.errstate(divide="ignore", invalid="ignore"):
            tx = np.where(vx > 0, ((ci + 1.0) * sn - x) / vx,
                          np.where(vx < 0, (ci * sn - x) / vx, np.inf))
            ty = np.where(vy > 0, ((cj + 1.0) * sn - y) / vy,
                          np.where(vy < 0, (cj * sn - y) / vy, np.inf))
        te = np.minimum(tx, ty)
        # exit at the escape sphere exactly (scatter runs): ray-circle time
        v2_ = vx * vx + vy * vy
        rv = x * vx + y * vy
        r2_ = x * x + y * y
        disc_ = np.maximum(rv * rv - v2_ * (r2_ - esc_r * esc_r), 0.0)
        tR = np.where((esc_r < np.inf) & (v2_ > 0) & (rv > 0) & (r2_ < esc_r ** 2),
                      (np.sqrt(disc_) - rv) / v2_, np.inf)
        te = np.minimum(te, tR)
        stall = ~(te > 0)
        if stall.any():
            te = np.where(stall, np.maximum(np.hypot(x, y), 1.0) * 1e-15
                          / np.maximum(np.hypot(vx, vy), 1e-300), te)
        x1 = x + vx * te; y1 = y + vy * te
        r1 = np.hypot(x1, y1)
        tstar = -(x * vx + y * vy) / (vx * vx + vy * vy)
        has_foot = (tstar > 1e-15) & (tstar < te)
        xf = x + vx * np.where(has_foot, tstar, 0.0)
        yf = y + vy * np.where(has_foot, tstar, 0.0)
        ph0 = np.arctan2(y, x)
        phf = np.arctan2(yf, xf)
        ph1 = np.arctan2(y1, x1)

        def wrap(a, b):
            d = a - b
            return np.arctan2(np.sin(d), np.cos(d))

        dph_full = wrap(ph1, ph0)
        dph_f = wrap(phf, ph0)
        for i in trace:
            if active[i]:
                trace[i].append((float(x[i]), float(y[i])))
                trace[i].append((float(x1[i]), float(y1[i])))
        ra_c = np.maximum(ra_c, np.maximum(np.hypot(x, y), r1))
        actf = active.astype(float)
        phi_c += np.where(has_foot, dph_f, dph_full) * actf
        phi_tot += dph_full * actf
        t_c += np.where(has_foot, tstar, te) * actf
        nc_c += active
        for i in np.nonzero(has_foot & active)[0]:
            c = cyc[i]
            if c < Cmax:
                out_dphi[i, c] = phi_c[i]; out_dt[i, c] = t_c[i]
                out_nc[i, c] = nc_c[i]; out_rp[i, c] = np.hypot(xf[i], yf[i])
                out_ra[i, c] = ra_c[i]
            cyc[i] += 1
            phi_c[i] = dph_full[i] - dph_f[i]
            t_c[i] = te[i] - tstar[i]
            nc_c[i] = 1
            ra_c[i] = r1[i]
        absorb_ev = (r1 <= 2.0) & active
        esc_ev = (~absorb_ev) & (r1 >= esc_r) & ((x1 * vx + y1 * vy) > 0) & active
        # refraction at (x1, y1)
        r1s = np.maximum(r1, 1e-300)
        rhx, rhy = x1 / r1s, y1 / r1s
        thx, thy = -rhy, rhx
        Lnow = x1 * py - y1 * px
        pt = Lnow / r1s
        b1x, b1y, n1, i1, j1, _ = square_flow(x1, y1)
        pr_old = px * rhx + py * rhy

        def refract(bxv, byv, other=False):
            c1_ = bxv * rhx + byv * rhy
            c2_ = bxv * thx + byv * thy
            B = np.hypot(bxv, byv)
            a2 = 1.0 - (B * c1_) ** 2
            a1 = 2.0 * B * c1_ * (Hv - B * c2_ * pt)
            a0 = one + pt * pt - (Hv - B * c2_ * pt) ** 2
            disc = a1 * a1 - 4.0 * a2 * a0
            real = disc >= 0.0
            sq = np.sqrt(np.where(real, disc, 0.0))
            den = 2.0 * np.where(np.abs(a2) > 1e-300, a2, np.nan)
            z1 = (-a1 - sq) / den
            z2 = (-a1 + sq) / den
            if other:
                pr = np.where(np.abs(z1 - pr_old) >= np.abs(z2 - pr_old), z1, z2)
            else:
                pr = np.where(np.abs(z1 - pr_old) <= np.abs(z2 - pr_old), z1, z2)
            pr = np.where(np.isfinite(pr), pr, -a0 / np.where(np.abs(a1) > 1e-300, a1, np.nan))
            pr = np.where(np.isfinite(pr), pr, pr_old)
            pr = np.clip(pr, -1e6, 1e6)
            return real, pr

        real, pr_new = refract(b1x, b1y)
        do_reflect = (~real) & active & ~absorb_ev & ~esc_ev
        _, pr_refl = refract(bx, by, other=True)
        pr_new = np.where(do_reflect, pr_refl, pr_new)
        pxn = pr_new * rhx + pt * thx
        pyn = pr_new * rhy + pt * thy
        act2 = active & ~absorb_ev & ~esc_ev
        px = np.where(act2, pxn, px)
        py = np.where(act2, pyn, py)
        if seq_cycles > 0:
            for i in np.nonzero(act2)[0]:
                if cyc[i] < seq_cycles:
                    seqs[cyc[i]][i].append((int(n1[i]), int(i1[i]), int(j1[i])))
        x = x1; y = y1
        absorbed |= absorb_ev; escaped |= esc_ev
        active &= ~(absorb_ev | esc_ev | (cyc >= ncyc_a) | (phi_tot >= phi_max))
    return dict(dphi=out_dphi, dt=out_dt, nc=out_nc, rp=out_rp, ra=out_ra,
                absorbed=absorbed, escaped=escaped, seq=seqs, trace=trace,
                phi_tot=phi_tot)


# ================================================================ tiltonly engine
def tiltonly_run(x0, y0, vx0, vy0, dt, ncyc, esc_r=None, phi_max=None,
                 seq_cycles=2, trace_lanes=(), max_iter=4_000_000):
    N = len(x0)
    x = np.array(x0, float); y = np.array(y0, float)
    vx = np.array(vx0, float); vy = np.array(vy0, float)
    dt = np.broadcast_to(np.asarray(dt, float), (N,)).copy()
    Cmax = int(np.max(ncyc)) if np.ndim(ncyc) else int(ncyc)
    ncyc_a = (np.broadcast_to(np.asarray(ncyc), (N,)).astype(int) if np.ndim(ncyc)
              else np.full(N, int(ncyc)))
    out_dphi = np.full((N, Cmax), np.nan); out_dt = np.full((N, Cmax), np.nan)
    out_nc = np.zeros((N, Cmax)); out_rp = np.full((N, Cmax), np.nan)
    out_ra = np.full((N, Cmax), np.nan)
    absorbed = np.zeros(N, bool); escaped = np.zeros(N, bool)
    cyc = np.zeros(N, int)
    phi_c = np.zeros(N); t_c = np.zeros(N); nc_c = np.zeros(N, int)
    ra_c = np.hypot(x, y); phi_tot = np.zeros(N)
    trace = {i: [] for i in trace_lanes}
    active = np.ones(N, bool)
    esc_r = np.full(N, np.inf) if esc_r is None else np.asarray(esc_r, float)
    phi_max = np.full(N, np.inf) if phi_max is None else np.asarray(phi_max, float)
    it = 0
    while active.any():
        it += 1
        if it > max_iter:
            break
        x0s, y0s = x.copy(), y.copy()
        x = x + 0.5 * dt * vx; y = y + 0.5 * dt * vy
        r = np.maximum(np.hypot(x, y), 1e-9)
        ax, ay = -x / r ** 3, -y / r ** 3
        cr = ax * vy - ay * vx
        v2 = vx * vx + vy * vy
        da = np.abs(cr) / np.maximum(v2, 1e-300) * dt
        s_ = np.sin(da) * np.sign(cr)
        c_ = np.cos(da)
        vx, vy = vx * c_ - vy * s_, vx * s_ + vy * c_
        x = x + 0.5 * dt * vx; y = y + 0.5 * dt * vy
        r1 = np.maximum(np.hypot(x, y), 1e-9)
        ph0 = np.arctan2(y0s, x0s); ph1 = np.arctan2(y, x)
        d = ph1 - ph0
        dphi = np.arctan2(np.sin(d), np.cos(d))
        # foot of perpendicular from origin to the straight step segment
        ex, ey = x - x0s, y - y0s
        e2 = ex * ex + ey * ey
        tstar = np.where(e2 > 0, -(x0s * ex + y0s * ey) / np.maximum(e2, 1e-300), -1.0)
        has_foot = (tstar > 1e-15) & (tstar < 1.0)
        for i in trace:
            if active[i]:
                trace[i].append((float(x0s[i]), float(y0s[i])))
                trace[i].append((float(x[i]), float(y[i])))
        ra_c = np.maximum(ra_c, r1)
        dphi = np.where(active, dphi, 0.0)
        r0_ = np.hypot(x0s, y0s)
        vr_ = (x * vx + y * vy) / np.maximum(r1, 1e-300)
        cross_esc = (r1 >= esc_r) & (r0_ < esc_r) & (vr_ > 0)
        fr_esc = np.where(cross_esc,
                          np.maximum(esc_r - r0_, 0.0) / np.maximum(r1 - r0_, 1e-300), 1.0)
        dphi = dphi * fr_esc
        phi_c += dphi; phi_tot += dphi; t_c += dt * fr_esc; nc_c += 1
        for i in np.nonzero(has_foot & active)[0]:
            fr = tstar[i]
            xf = x0s[i] + fr * (x[i] - x0s[i]); yf = y0s[i] + fr * (y[i] - y0s[i])
            dphf = dphi[i] * fr
            c = cyc[i]
            if c < Cmax:
                out_dphi[i, c] = phi_c[i] - dphi[i] + dphf
                out_dt[i, c] = t_c[i] - dt[i] + fr * dt[i]
                out_nc[i, c] = nc_c[i]
                out_rp[i, c] = np.hypot(xf, yf)
                out_ra[i, c] = ra_c[i]
            cyc[i] += 1
            phi_c[i] = dphi[i] - dphf
            t_c[i] = dt[i] * (1.0 - fr)
            nc_c[i] = 1
            ra_c[i] = r1[i]
        absorb_ev = (r1 <= 2.0) & active
        esc_ev = (~absorb_ev) & (r1 >= esc_r) & ((x * vx + y * vy) > 0) & active
        absorbed |= absorb_ev; escaped |= esc_ev
        active &= ~(absorb_ev | esc_ev | (cyc >= ncyc_a) | (phi_tot >= phi_max))
    return dict(dphi=out_dphi, dt=out_dt, nc=out_nc, rp=out_rp, ra=out_ra,
                absorbed=absorbed, escaped=escaped, seq=seqs_placeholder(N),
                trace=trace, phi_tot=phi_tot)


def seqs_placeholder(N):
    return ([[] for _ in range(N)], [[] for _ in range(N)])


# ---------------------------------------------------------------- metrics assembly
def assemble(short, light_defl, cap_absorbed, isco_a_ok, isco_b_ok, long_r,
             seq_ok, name):
    dphi = short["dphi"][:, 1]
    dphi_gr = np.array([periapsis_elliptic(p, e) + TWOPI for p, e in BOUND])
    ok = np.isfinite(dphi)
    prec = ok & (np.abs(dphi - dphi_gr) <= 0.01 * np.abs(dphi_gr))
    prog = ok & (dphi > TWOPI)
    Tm = short["dt"][:, 1]
    To = np.array([bound_period_quad(p, e)[0] for p, e in BOUND])
    per = ok & (np.abs(Tm - To) / To <= 0.001)
    cross = float(np.median(short["nc"][ok, 1])) if ok.any() else 0.0
    d_or = np.array([deflection_quadrature(b) for b in LIGHT_B])
    dl = light_defl
    defl = np.isfinite(dl) & (np.abs(dl - d_or) <= 0.01 * np.abs(d_or))
    mis = int(np.sum(cap_absorbed != CAP_TRUTH))
    isco = int(isco_a_ok and isco_b_ok)
    rp, ra = long_r["rp"], long_r["ra"]
    with np.errstate(invalid="ignore"):
        shape_ok = ((np.abs(rp[:, 1:] / rp[:, [1]] - 1.0) <= 0.01).all(axis=1)
                    & (np.abs(ra[:, 1:] / ra[:, [1]] - 1.0) <= 0.01).all(axis=1)
                    & np.isfinite(rp[:, 1]))
    d1 = long_r["dphi"][:, 0]; t1 = long_r["dt"][:, 0]
    dl_, tl_ = long_r["dphi"], long_r["dt"]
    with np.errstate(invalid="ignore"):
        rep_num = ((np.abs(dl_[:, 1:] - d1[:, None]) <= 1e-12 * np.abs(d1[:, None])).all(axis=1)
                   & (np.abs(tl_[:, 1:] - t1[:, None]) <= 1e-12 * np.abs(t1[:, None])).all(axis=1)
                   & np.isfinite(d1) & (np.abs(d1) > 0))
    repeat = np.array(seq_ok, bool) & rep_num
    met = {"precession_pass_fraction": float(np.mean(prec)),
           "prograde_fraction": float(np.mean(prog)),
           "period_pass_fraction": float(np.mean(per)),
           "deflection_pass_fraction": float(np.mean(defl)),
           "capture_misclassified": mis,
           "isco_correct": isco,
           "shape_kept_fraction": float(np.mean(shape_ok)),
           "cycle_repeat_fraction": float(np.mean(repeat)),
           "crossings_per_cycle": cross}
    print(name, json.dumps(met, indent=1), flush=True)
    return met


def light_defl_from_phi(phi_tot, absorbed):
    tails = np.array([light_tail(b, U_LIGHT_START) for b in LIGHT_B])
    dl = phi_tot + 2.0 * tails - PI
    return np.where(absorbed, np.nan, dl)


def kepler_dt(rp, vt):
    v2 = vt * vt
    a = 1.0 / np.maximum(2.0 / rp - v2, 1e-9)
    return 2.0 * PI * a ** 1.5 / 256.0


# ================================================================ config drivers
def gr_speed_at_peri(p, e, E, L):
    """GR coordinate tangential speed r dphi/dt at periapsis (dr/dt = 0)."""
    rp = p / (1.0 + e)
    return L * (1.0 - 2.0 / rp) / (E * rp)


def binet_config(m):
    t0 = time.time()
    p, e, E, L = bound_EL(BOUND)
    u0 = (1.0 + e) / p
    short = binet_run(u0, np.zeros_like(u0), E, L, m, False, 4, seq_cycles=2)
    print(f"binet-m{m} short {time.time()-t0:.0f}s", flush=True)
    b = np.array(LIGHT_B)
    up0 = np.sqrt(1.0 / b ** 2 - U_LIGHT_START ** 2 + 2 * U_LIGHT_START ** 3)
    rl = binet_run(np.full(len(b), U_LIGHT_START), up0, np.ones(len(b)), b, m, True,
                   2, esc_u=np.full(len(b), U_LIGHT_START), seq_cycles=0, max_iter=10 ** 6)
    defl = light_defl_from_phi(rl["phi_tot"], rl["absorbed"])
    # capture
    Lt = np.array(CAP_LT); bp = np.array(CAP_PH)
    u0c = np.concatenate([np.full(len(Lt), 0.01), np.full(len(bp), U_LIGHT_START)])
    Lc = np.concatenate([Lt, bp])
    lightc = np.concatenate([np.zeros(len(Lt), bool), np.ones(len(bp), bool)])
    up0c = np.sqrt(np.maximum(0.0, 2.0 * u0c / Lc ** 2 - u0c ** 2 + 2 * u0c ** 3))
    # (E=1 for both; (E^2-1)/L^2 = 0)
    esc = np.concatenate([np.full(len(Lt), 0.01), np.full(len(bp), U_LIGHT_START)])
    rc_ = binet_run(u0c, up0c, np.ones(len(u0c)), Lc, m, False, 2, esc_u=esc,
                    seq_cycles=0, max_iter=10 ** 6)
    cap_abs = rc_["absorbed"]
    # isco
    out = []
    for (r0, f, plunge, cap) in ((7.0, 1.01, False, 100 * TWOPI), (5.5, 0.99, True, 50 * TWOPI)):
        rr = binet_run(np.array([1.0 / r0]), np.array([0.0]), np.array([ecirc(r0)]),
                       np.array([f * lcirc(r0)]), m, False, 2,
                       phi_max=np.array([cap]), seq_cycles=0, max_iter=10 ** 6)
        out.append(bool(rr["absorbed"][0]) if plunge else bool(~rr["absorbed"][0]))
    # trace: p=20, e=0.5, 5 cycles
    Et, Lt2 = bound_constants(20.0, 0.5)
    tr = binet_run(np.array([1.5 / 20.0]), np.array([0.0]), np.array([Et]),
                   np.array([Lt2]), m, False, 5, seq_cycles=0, trace_lanes=(0,))
    trace_xy = [[math.cos(ph) / uu, math.sin(ph) / uu] for ph, uu in tr["trace"][0]]
    # light trace for the picture (binet-m16 only)
    trace_lt = None
    if m == 16:
        bs = [10.0, 31.6, 100.0, 316.0, 1000.0]
        for bb in bs:
            upl = math.sqrt(1.0 / bb ** 2 - U_LIGHT_START ** 2 + 2 * U_LIGHT_START ** 3)
            tq = binet_run(np.array([U_LIGHT_START]), np.array([upl]), np.array([1.0]),
                           np.array([bb]), m, True, 2, esc_u=np.array([U_LIGHT_START]),
                           seq_cycles=0, trace_lanes=(0,), max_iter=10 ** 6)
            pts = [[math.cos(ph) / uu, math.sin(ph) / uu] for ph, uu in tq["trace"][0]]
            trace_lt = (pts if trace_lt is None else trace_lt)
            with open(f"light-binet-m16-{bb:g}.json", "w") as fh:
                json.dump(pts, fh)
    # long runs
    pl, el, El, Ll = bound_EL(BOUND[:32])
    long_r = binet_run((1.0 + el) / pl, np.zeros_like(pl), El, Ll, m, False,
                       10_002, seq_cycles=2)
    seq_ok = [long_r["seq"][0][i] == long_r["seq"][1][i] for i in range(32)]
    print(f"binet-m{m} long {time.time()-t0:.0f}s", flush=True)
    long_dict = dict(rp=1.0 / long_r["up"], ra=1.0 / long_r["ua"],
                     dphi=long_r["dphi"], dt=long_r["dt"])
    met = assemble(short, defl, cap_abs, out[0], out[1], long_dict, seq_ok, f"binet-m{m}")
    return met, trace_xy


def river_config(m):
    t0 = time.time()
    p, e, E, L = bound_EL(BOUND)
    rp0 = p / (1.0 + e)
    short = river_run(rp0, np.ones(len(p)), E, L, m, False, 4, seq_cycles=2)
    print(f"river-m{m} short {time.time()-t0:.0f}s", flush=True)
    b = np.array(LIGHT_B)
    rl = river_run(np.full(len(b), 1e4), -np.ones(len(b)), np.ones(len(b)), b, m, True,
                   2, esc_r=np.full(len(b), 1e4), seq_cycles=0, max_iter=10 ** 6)
    defl = light_defl_from_phi(rl["phi_tot"], rl["absorbed"])
    Lt = np.array(CAP_LT); bp = np.array(CAP_PH)
    r0c = np.concatenate([np.full(len(Lt), 100.0), np.full(len(bp), 1e4)])
    Lc = np.concatenate([Lt, bp])
    esc = np.concatenate([np.full(len(Lt), 100.0), np.full(len(bp), 1e4)])
    rc_ = river_run(r0c, -np.ones(len(r0c)), np.ones(len(r0c)), Lc, m, False, 2,
                    esc_r=esc, seq_cycles=0, max_iter=10 ** 6)
    cap_abs = rc_["absorbed"]
    out = []
    for (r0, f, plunge, cap) in ((7.0, 1.01, False, 100 * TWOPI), (5.5, 0.99, True, 50 * TWOPI)):
        rr = river_run(np.array([r0]), np.array([1.0]), np.array([ecirc(r0)]),
                       np.array([f * lcirc(r0)]), m, False, 2,
                       phi_max=np.array([cap]), seq_cycles=0, max_iter=10 ** 6)
        out.append(bool(rr["absorbed"][0]) if plunge else bool(~rr["absorbed"][0]))
    Et, Lt2 = bound_constants(20.0, 0.5)
    tr = river_run(np.array([20.0 / 1.5]), np.array([1.0]), np.array([Et]),
                   np.array([Lt2]), m, False, 5, seq_cycles=0, trace_lanes=(0,))
    trace_xy = [[math.cos(ph) * rr, math.sin(ph) * rr] for ph, rr in tr["trace"][0]]
    if m == 16:
        for bb in [10.0, 31.6, 100.0, 316.0, 1000.0]:
            tq = river_run(np.array([1e4]), np.array([-1.0]), np.array([1.0]),
                           np.array([bb]), m, True, 2, esc_r=np.array([1e4]),
                           seq_cycles=0, max_iter=10 ** 6)
            # trace not collected for light; rebuild sparse trace from phi_tot only
    pl, el, El, Ll = bound_EL(BOUND[:32])
    long_r = river_run(pl / (1.0 + el), np.ones(32), El, Ll, m, False, 10_002, seq_cycles=2)
    seq_ok = [long_r["seq"][0][i] == long_r["seq"][1][i] for i in range(32)]
    print(f"river-m{m} long {time.time()-t0:.0f}s", flush=True)
    long_dict = dict(rp=long_r["rp"], ra=long_r["ra"], dphi=long_r["dphi"], dt=long_r["dt"])
    met = assemble(short, defl, cap_abs, out[0], out[1], long_dict, seq_ok, f"river-m{m}")
    return met, trace_xy


def square_init(rp, pt, light=False):
    """Position (rp, 0), tangential canonical pt, radial p from dr/dt = 0."""
    bx, by, _, _, _, _ = square_flow(np.array([rp]), np.array([0.0]))
    br = bx[0]  # radial component at (rp, 0)
    one = 0.0 if light else 1.0
    pr = -br * math.sqrt((one + pt * pt) / (1.0 - br * br))
    return pr


def square_config():
    t0 = time.time()
    p, e, E, L = bound_EL(BOUND)
    rp0 = p / (1.0 + e)
    pr0 = np.array([square_init(r_, L_ / r_ * 0 + pt_ / 1.0) for r_, pt_
                    in zip(rp0, L / rp0)])
    short = square_run(rp0, np.zeros(len(p)), pr0, L / rp0, 4, seq_cycles=2)
    print(f"square short {time.time()-t0:.0f}s", flush=True)
    # light: 64 lanes, |p|=1, from (x, d) with v=(1,0); choose d so L/H = b
    b = np.array(LIGHT_B)
    xs, ys, ps = [], [], []
    for bb in b:
        d = bb
        for _ in range(4):
            x0 = -math.sqrt(max(1e8 - d * d, 0.0))
            bxf, byf, _, _, _, _ = square_flow(np.array([x0]), np.array([d]))
            H = 1.0 + bxf[0]  # |p|=1 moving +x
            d = bb * H
        xs.append(-math.sqrt(max(1e8 - d * d, 0.0))); ys.append(d)
    rl = square_run(np.array(xs), np.array(ys), np.ones(len(b)), np.zeros(len(b)), 2,
                    esc_r=np.full(len(b), 1e4), light=True, seq_cycles=0, max_iter=10 ** 6)
    defl = light_defl_from_phi(rl["phi_tot"], rl["absorbed"])
    # capture: timelike E=1 from r=100 at (0,-100) inward; photons from r=1e4
    Lt = np.array(CAP_LT); bp = np.array(CAP_PH)
    cap_abs = []
    for LL in Lt:
        bx, by, _, _, _, _ = square_flow(np.array([0.0]), np.array([-100.0]))
        # rhat=(0,-1), thetat=(1,0): p = pr*rhat + pt*thetat
        br = (bx * 0.0 + by * -1.0)[0]; bt = (bx * 1.0 + by * 0.0)[0]
        pt = LL / 100.0
        a2 = 1.0 - br * br; a1 = -2.0 * br * (1.0 - bt * pt)
        a0 = 1.0 + pt * pt - (1.0 - bt * pt) ** 2
        disc = a1 * a1 - 4 * a2 * a0
        sq = math.sqrt(max(disc, 0.0))
        z1 = (-a1 - sq) / (2 * a2); z2 = (-a1 + sq) / (2 * a2)
        gam1 = math.sqrt(1 + z1 * z1 + pt * pt)
        v1 = z1 / gam1 + br
        pr = z1 if v1 < 0 else z2
        rr = square_run(np.array([0.0]), np.array([-100.0]),
                        np.array([pr * 0.0 + pt * 1.0]), np.array([pr * -1.0 + pt * 0.0]),
                        2, esc_r=np.array([100.0]), seq_cycles=0, max_iter=10 ** 6)
        cap_abs.append(bool(rr["absorbed"][0]))
    for bb in bp:
        d = bb
        for _ in range(4):
            x0 = -math.sqrt(max(1e8 - d * d, 0.0))
            bxf, byf, _, _, _, _ = square_flow(np.array([x0]), np.array([d]))
            d = bb * (1.0 + bxf[0])
        rr = square_run(np.array([-math.sqrt(max(1e8 - d * d, 0.0))]), np.array([d]),
                        np.array([1.0]), np.array([0.0]), 2,
                        esc_r=np.array([1e4]), light=True, seq_cycles=0, max_iter=10 ** 6)
        cap_abs.append(bool(rr["absorbed"][0]))
    cap_abs = np.array(cap_abs)
    # isco
    out = []
    for (r0, f, plunge, cap) in ((7.0, 1.01, False, 100 * TWOPI), (5.5, 0.99, True, 50 * TWOPI)):
        pt = f * lcirc(r0) / r0
        pr = square_init(r0, pt)
        rr = square_run(np.array([r0]), np.array([0.0]), np.array([pr]), np.array([pt]),
                        2, phi_max=np.array([cap]), seq_cycles=0, max_iter=2 * 10 ** 6)
        out.append(bool(rr["absorbed"][0]) if plunge else bool(~rr["absorbed"][0]))
    Et, Lt2 = bound_constants(20.0, 0.5)
    pr = square_init(20.0 / 1.5, Lt2 / (20.0 / 1.5))
    tr = square_run(np.array([20.0 / 1.5]), np.array([0.0]), np.array([pr]),
                    np.array([Lt2 / (20.0 / 1.5)]), 5, seq_cycles=0, trace_lanes=(0,))
    trace_xy = [[float(a), float(c)] for a, c in tr["trace"][0]]
    pl, el, El, Ll = bound_EL(BOUND[:32])
    rpl = pl / (1.0 + el)
    prl = np.array([square_init(r_, L_ / r_) for r_, L_ in zip(rpl, Ll)])
    long_r = square_run(rpl, np.zeros(32), prl, Ll / rpl, 10_002, seq_cycles=2)
    seq_ok = [long_r["seq"][0][i] == long_r["seq"][1][i] for i in range(32)]
    print(f"square long {time.time()-t0:.0f}s", flush=True)
    long_dict = dict(rp=long_r["rp"], ra=long_r["ra"], dphi=long_r["dphi"], dt=long_r["dt"])
    met = assemble(short, defl, cap_abs, out[0], out[1], long_dict, seq_ok, "square")
    return met, trace_xy


def tiltonly_config():
    t0 = time.time()
    p, e, E, L = bound_EL(BOUND)
    rp0 = p / (1.0 + e)
    vt = gr_speed_at_peri(p, e, E, L)
    dtl = kepler_dt(rp0, vt)
    x0 = rp0.copy(); y0 = np.zeros(len(p)); vx0 = np.zeros(len(p)); vy0 = vt.copy()
    short = tiltonly_run(x0, y0, vx0, vy0, dtl, 4, seq_cycles=0)
    print(f"tiltonly short {time.time()-t0:.0f}s", flush=True)
    b = np.array(LIGHT_B)
    xs = -np.sqrt(np.maximum(1e8 - b ** 2, 0.0))
    rl = tiltonly_run(xs, b.copy(), np.ones(len(b)), np.zeros(len(b)), b / 50.0, 2,
                      esc_r=np.full(len(b), 1e4), seq_cycles=0, max_iter=10 ** 7)
    defl = light_defl_from_phi(rl["phi_tot"], rl["absorbed"])
    Lt = np.array(CAP_LT); bp = np.array(CAP_PH)
    cap_abs = []
    for LL in Lt:
        vt = LL * (1.0 - 0.02) / 100.0
        v = math.sqrt(2.0 / 100.0)
        vr = -math.sqrt(max(v * v - vt * vt, 0.0))
        rr = tiltonly_run(np.array([0.0]), np.array([-100.0]), np.array([vt]),
                          np.array([vr]), 0.02, 2, esc_r=np.array([100.0]),
                          seq_cycles=0, phi_max=np.array([80.0]), max_iter=4 * 10 ** 6)
        cap_abs.append(bool(rr["absorbed"][0]))
    for bb in bp:
        rr = tiltonly_run(np.array([-math.sqrt(1e8 - bb * bb)]), np.array([bb]),
                          np.array([1.0]), np.array([0.0]), bb / 50.0, 2,
                          esc_r=np.array([1e4]), seq_cycles=0, max_iter=10 ** 7)
        cap_abs.append(bool(rr["absorbed"][0]))
    cap_abs = np.array(cap_abs)
    out = []
    for (r0, f, plunge, cap) in ((7.0, 1.01, False, 100 * TWOPI), (5.5, 0.99, True, 50 * TWOPI)):
        LL = f * lcirc(r0)
        vt = LL * (1.0 - 2.0 / r0) / (ecirc(r0) * r0)
        rr = tiltonly_run(np.array([r0]), np.array([0.0]), np.array([0.0]),
                          np.array([vt]), kepler_dt(np.array([r0]), np.array([vt]))[0],
                          2, seq_cycles=0, phi_max=np.array([cap]), max_iter=4 * 10 ** 6)
        out.append(bool(rr["absorbed"][0]) if plunge else bool(~rr["absorbed"][0]))
    Et, Lt2 = bound_constants(20.0, 0.5)
    vtt = Lt2 * (1.0 - 2.0 / (20.0 / 1.5)) / (Et * (20.0 / 1.5))
    tr = tiltonly_run(np.array([20.0 / 1.5]), np.array([0.0]), np.array([0.0]),
                      np.array([vtt]), kepler_dt(np.array([20.0 / 1.5]), np.array([vtt]))[0],
                      5, seq_cycles=0, trace_lanes=(0,))
    trace_xy = [[float(a), float(c)] for a, c in tr["trace"][0]]
    pl, el, El, Ll = bound_EL(BOUND[:32])
    rpl = pl / (1.0 + el)
    vtl = gr_speed_at_peri(pl, el, El, Ll)
    long_r = tiltonly_run(rpl, np.zeros(32), np.zeros(32), vtl,
                          kepler_dt(rpl, vtl), 10_002, seq_cycles=0, max_iter=6 * 10 ** 6)
    seq_ok = [long_r["nc"][i, 0] == long_r["nc"][i, 1] for i in range(32)]
    print(f"tiltonly long {time.time()-t0:.0f}s", flush=True)
    long_dict = dict(rp=long_r["rp"], ra=long_r["ra"], dphi=long_r["dphi"], dt=long_r["dt"])
    met = assemble(short, defl, cap_abs, out[0], out[1], long_dict, seq_ok, "tiltonly")
    return met, trace_xy


CONFIGS = {
    "binet-m8": lambda: binet_config(8),
    "binet-m16": lambda: binet_config(16),
    "binet-m32": lambda: binet_config(32),
    "river-m16": lambda: river_config(16),
    "river-m32": lambda: river_config(32),
    "square": square_config,
    "tiltonly": tiltonly_config,
}

if __name__ == "__main__":
    cfg = sys.argv[1]
    t0 = time.time()
    met, trace_xy = CONFIGS[cfg]()
    with open(f"out-{cfg}.json", "w") as fh:
        json.dump({"metrics": met, "trace_orbit": trace_xy,
                   "seconds": time.time() - t0}, fh)
    print(f"done {cfg} in {time.time()-t0:.0f}s", flush=True)
