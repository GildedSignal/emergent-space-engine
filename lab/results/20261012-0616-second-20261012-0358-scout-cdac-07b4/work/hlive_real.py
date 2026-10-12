#!/usr/bin/env python3
"""Second author: H_live on the design's real encounter path.

The scout run (20261012-0358) measured the live-memory law on a Poisson
rate-structure toy: uniform-b impulse kicks, independent random signs for
(da, de), no conjunction geometry, no kick recurrence, a clipped Gamma(e)
stirring coupling.  The checker held gold on exactly that gap.

This run replaces the rate structure with real belt dynamics and keeps the
accounting identical:

- Belt = crates/encounters' generator semantics: a ~ U[a_lo, a_lo+W],
  e ~ Rayleigh(sigma_e) capped 0.5, uniform angles (GM_star = 1 units).
- Real Kepler propagation (vectorised Newton on E); a body's state is its
  elements; kicks preserve the true anomaly (position-continuous).
- Conjunctions = every local minimum of the pair distance below B_DET,
  found like truth.rs: a pair is tracked while within B_DET and a kick
  fires at each d/dt(dr.dv) sign change - to +.  The minimum time t* is
  the vertex of the parabola through |dr|^2 at (t-dt, t-dt/2, t), all
  evaluated analytically from the elements; b, v_rel, the separation
  direction and both true anomalies are evaluated exactly at t*.
- Kick: impulse dv = 2 m / (b v_rel) along the separation at closest
  approach (capped at 0.5 v_rel where the straight-line formula leaves
  its small-angle domain; gravitational focusing negligible: 2m/v_rel^2
  << b at these masses), applied to both bodies with opposite signs and
  mapped to (da, de) by Gauss's planetary equations at the true anomaly.
  Contacts (b < 4 R_body) are counted and NOT kicked (lattice events).
- Stirring, kick recurrence and resonant concentration are native: kicks
  change e and a, which changes the crossing geometry.  No coupling is
  imposed anywhere.

Accounting is the scout's, replayed over the recorded kick stream at any
quantum eps: cell_a = eps*a_mid, cell_e = eps; distinguished iff current
cell != birth cell; R1/R2/R3 stores; joint cell entropy Hj; inflow
exponent; s_part = D / kick-applications (the toy kicked one body per
event, so its s_frac = D/(2*events) differs by a factor 2 in convention;
both are reported).  alpha_partial is fitted on the partial regime ONLY
(rows with D/N < 0.5), fixing the mislabelled field the checker found.

Deterministic (seeded), <2 GB, minutes per config.
"""
import json, math, os, subprocess, sys, time
import numpy as np

TAU = 2.0 * math.pi
YR_S = 3.156e7
RTF = 100.0
GS_PER_YR = YR_S / RTF
RHO_BODY = 2.5 / 1.989e33 * (1.496e13) ** 3   # M_sun/AU^3, rho=2.5 g/cc

# ---------------------------------------------------------------- kepler --

def kepler_E(M, e):
    M = np.mod(M, TAU)
    E = M + e * np.sin(M)
    for _ in range(12):
        dE = (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
        E = E - dE
        if np.max(np.abs(dE)) < 1e-14:
            break
    return E

def states(a, e, pom, M0, n, t):
    """Cartesian states at time t (GM = 1).  t may be scalar or array."""
    M = M0 + n * t
    E = kepler_E(M, e)
    cosE, sinE = np.cos(E), np.sin(E)
    r = a * (1.0 - e * cosE)
    f = 2.0 * np.arctan2(np.sqrt(1.0 + e) * sinE,
                         np.sqrt(1.0 - e) * (1.0 + cosE))
    th = pom + f
    p = a * (1.0 - e * e)
    h = np.sqrt(np.maximum(p, 1e-12))
    vr = (h / p) * e * np.sin(f)
    vt = h / r
    ct, st = np.cos(th), np.sin(th)
    return (r * ct, r * st, vr * ct - vt * st, vr * st + vt * ct, r, th, f)

def gauss(a, e, f, dvr, dvt):
    """(da, de) from a small kick (dvr, dvt) at true anomaly f."""
    p = a * (1.0 - e * e)
    h = np.sqrt(np.maximum(p, 1e-12))
    r = p / (1.0 + e * np.cos(f))
    da = (2.0 * a * a / h) * (e * np.sin(f) * dvr + (p / r) * dvt)
    de = (1.0 / h) * (p * np.sin(f) * dvr + ((p + r) * np.cos(f) + r * e) * dvt)
    return da, de

def M_from_f(f, e):
    E = 2.0 * np.arctan2(np.sqrt(1.0 - e) * np.sin(f * 0.5),
                         np.sqrt(1.0 + e) * np.cos(f * 0.5))
    return E - e * np.sin(E)

# ------------------------------------------------------------- propagation --

def propagate(N=1500, a_lo=1.0, W=0.05, sigma_e=0.05, m=1e-10, b_det=0.06,
              orbits=20, steps_per_orbit=256, seed=7, kick=True):
    rng = np.random.default_rng(seed)
    a = rng.uniform(a_lo, a_lo + W, N)
    e = np.minimum(rng.rayleigh(sigma_e, N), 0.5)
    pom = rng.uniform(0.0, TAU, N)
    M0 = rng.uniform(0.0, TAU, N)
    a0, e0 = a.copy(), e.copy()
    n = a ** -1.5
    a_mid = a_lo + W / 2.0
    dt = TAU / steps_per_orbit
    Rbody = (3.0 * m / (4.0 * math.pi * RHO_BODY)) ** (1.0 / 3.0)
    b_contact = 4.0 * Rbody
    steps = int(round(orbits * steps_per_orbit))
    KT, KI, KJ, KB, KV = [], [], [], [], []
    KDAI, KEI, KDAJ, KEJ = [], [], [], []
    pair_keys = []
    contacts = 0
    kicks_per_orbit = np.zeros(orbits + 1, dtype=np.int64)
    e_hist = [e.copy()]
    a_hist = [a.copy()]
    aI = np.empty(0, np.int64); aJ = np.empty(0, np.int64); aG = np.empty(0)
    for step in range(steps):
        t = step * dt
        x, y, vx, vy, r, th, f = states(a, e, pom, M0, n, t)
        # ---- near pairs: azimuth windows on the sorted circle ----
        order = np.argsort(th)
        th_s = th[order]
        w = b_det / max(float(np.min(r)), 0.3) + 0.02
        nxt = np.searchsorted(th_s, th_s + w, side="right")
        prv = np.searchsorted(th_s, th_s - w, side="left")
        cnt = nxt - prv - 1
        tot = int(cnt.sum())
        parts_i, parts_j = [], []
        if tot:
            off = np.concatenate([[0], np.cumsum(cnt)])
            base = np.repeat(off[:-1], cnt)
            within = np.arange(tot) - base
            kk = np.repeat(np.arange(N), cnt)          # owner (sorted pos)
            jpos = prv[kk] + within + (prv[kk] + within >= kk)
            ii = order[kk]; jj = order[jpos]
            d2 = (x[ii] - x[jj]) ** 2 + (y[ii] - y[jj]) ** 2
            sel = d2 < b_det * b_det
            parts_i.append(ii[sel]); parts_j.append(jj[sel])
        # wrap-around pairs (theta ~ 0 with theta ~ TAU), python-free core
        wK = int(np.searchsorted(th_s, 2.0 * w))
        if wK > 0:
            ext_i = order[:wK]
            th_e = th_s[:wK] + TAU
            lo = np.searchsorted(th_s, th_e - w, side="left")
            hi = np.searchsorted(th_s, th_e + w, side="right")
            for k in range(wK):
                js = order[lo[k]:hi[k]]
                ddx = x[ext_i[k]] - x[js]; ddy = y[ext_i[k]] - y[js]
                sel = ddx * ddx + ddy * ddy < b_det * b_det
                if sel.any():
                    parts_i.append(np.full(int(sel.sum()), ext_i[k]))
                    parts_j.append(js[sel])
        if parts_i:
            ni_ = np.concatenate(parts_i); nj_ = np.concatenate(parts_j)
            lo_ = np.minimum(ni_, nj_); hi_ = np.maximum(ni_, nj_)
            kd = np.unique(lo_ * N + hi_)
            near_ii, near_jj = kd // N, kd % N
        else:
            near_ii = near_jj = np.empty(0, dtype=np.int64)
        # ---- update active pairs ----
        if aI.size:
            dx = x[aI] - x[aJ]; dy = y[aI] - y[aJ]
            dvx = vx[aI] - vx[aJ]; dvy = vy[aI] - vy[aJ]
            ad2 = dx * dx + dy * dy
            g = dx * dvx + dy * dvy
            cross = (aG < 0.0) & (g >= 0.0)
            if cross.any() and kick:
                ci, cj = aI[cross], aJ[cross]
                # vertex of the parabola through |dr|^2 at t-dt, t-dt/2, t
                t0, t1, t2 = t - dt, t - 0.5 * dt, t
                d2s = np.empty((3, ci.size))
                for k, tk in enumerate((t0, t1, t2)):
                    xk, yk, _, _, _, _, _ = states(a, e, pom, M0, n, np.full(N, tk))
                    d2s[k] = (xk[ci] - xk[cj]) ** 2 + (yk[ci] - yk[cj]) ** 2
                L0 = 1.0 / ((t0 - t1) * (t0 - t2))
                L1 = 1.0 / ((t1 - t0) * (t1 - t2))
                L2 = 1.0 / ((t2 - t0) * (t2 - t1))
                A_ = d2s[0] * L0 + d2s[1] * L1 + d2s[2] * L2
                B_ = -(d2s[0] * (t1 + t2) * L0 + d2s[1] * (t0 + t2) * L1
                       + d2s[2] * (t0 + t1) * L2)
                safe = np.abs(A_) > 1e-300
                ts = np.where(safe, np.clip(-B_ / (2.0 * np.where(safe, A_, 1.0)),
                                            t0, t2), t1)
                # exact relative state at t* (gathered per-pair arrays)
                xi_s, yi_s, vxi_s, vyi_s, ri_s, thi_s, fi_s = states(
                    a[ci], e[ci], pom[ci], M0[ci], n[ci], ts)
                xj_s, yj_s, vxj_s, vyj_s, rj_s, thj_s, fj_s = states(
                    a[cj], e[cj], pom[cj], M0[cj], n[cj], ts)
                ddx = xi_s - xj_s; ddy = yi_s - yj_s
                dvx_ = vxi_s - vxj_s; dvy_ = vyi_s - vyj_s
                b = np.hypot(ddx, ddy)
                vrel = np.maximum(np.hypot(dvx_, dvy_), 1e-12)
                nrm = np.maximum(b, 1e-300)
                ux, uy = ddx / nrm, ddy / nrm
                fI, fJ = fi_s, fj_s
                thI, thJ = thi_s, thj_s
                contact = b < b_contact
                contacts += int(contact.sum())
                ok = ~contact
                if ok.any():
                    i2, j2 = ci[ok], cj[ok]
                    b2, v2 = b[ok], vrel[ok]
                    ts2 = ts[ok]
                    ux2, uy2 = ux[ok], uy[ok]
                    dv = np.minimum(2.0 * m / (b2 * v2), 0.5 * v2)
                    dvx, dvy = dv * ux2, dv * uy2
                    cth_i, sth_i = np.cos(thI[ok]), np.sin(thI[ok])
                    cth_j, sth_j = np.cos(thJ[ok]), np.sin(thJ[ok])
                    dvr_i = dvx * cth_i + dvy * sth_i
                    dvt_i = -dvx * sth_i + dvy * cth_i
                    dvr_j = -(dvx * cth_j + dvy * sth_j)
                    dvt_j = -(-dvx * sth_j + dvy * cth_j)
                    dai, dei = gauss(a[i2], e[i2], fI[ok], dvr_i, dvt_i)
                    daj, dej = gauss(a[j2], e[j2], fJ[ok], dvr_j, dvt_j)
                    np.add.at(a, i2, dai); np.add.at(e, i2, dei)
                    np.add.at(a, j2, daj); np.add.at(e, j2, dej)
                    e = np.clip(e, 0.0, 0.95)
                    a = np.maximum(a, 0.05)
                    n = a ** -1.5
                    # position-continuous mean anomaly at t* (last write on
                    # a double event in one step: one sub-quantum jump)
                    Mi = M_from_f(fI[ok], e[i2]); Mj = M_from_f(fJ[ok], e[j2])
                    M0[i2] = Mi - n[i2] * ts2
                    M0[j2] = Mj - n[j2] * ts2
                    KT.append(ts2.copy()); KI.append(i2); KJ.append(j2)
                    KB.append(b2.copy()); KV.append(v2.copy())
                    KDAI.append(dai.copy()); KEI.append(dei.copy())
                    KDAJ.append(daj.copy()); KEJ.append(dej.copy())
                    pair_keys.append(i2.astype(np.int64) * N + j2)
                    kicks_per_orbit[min(int(t // TAU), orbits)] += i2.size
            still = ad2 < b_det * b_det
            aI, aJ, aG = aI[still], aJ[still], g[still]
        # ---- add new near pairs ----
        if near_ii.size:
            keys = near_ii * N + near_jj
            if aI.size:
                asort = np.sort(aI * N + aJ)
                newm = ~np.isin(keys, asort)
            else:
                newm = np.ones(keys.size, dtype=bool)
            if newm.any():
                ni_, nj_ = near_ii[newm], near_jj[newm]
                g0 = ((x[ni_] - x[nj_]) * (vx[ni_] - vx[nj_])
                      + (y[ni_] - y[nj_]) * (vy[ni_] - vy[nj_]))
                aI = np.concatenate([aI, ni_]); aJ = np.concatenate([aJ, nj_])
                aG = np.concatenate([aG, g0])
        if (step + 1) % steps_per_orbit == 0:
            e_hist.append(e.copy())
            a_hist.append(a.copy())
    kick_t = np.concatenate(KT) if KT else np.empty(0)
    kick_i = (np.concatenate(KI) if KT else np.empty(0)).astype(np.int32)
    kick_j = (np.concatenate(KJ) if KT else np.empty(0)).astype(np.int32)
    pk = (np.concatenate(pair_keys) if pair_keys else np.empty(0, np.int64))
    return dict(N=N, W=W, sigma_e=sigma_e, m=m, b_det=b_det, orbits=orbits,
                steps_per_orbit=steps_per_orbit, a_mid=a_mid, seed=seed,
                contacts=contacts, kick_t=kick_t, kick_i=kick_i, kick_j=kick_j,
                kick_b=np.concatenate(KB) if KB else np.empty(0),
                kick_v=np.concatenate(KV) if KV else np.empty(0),
                dai=np.concatenate(KDAI) if KDAI else np.empty(0),
                dei=np.concatenate(KEI) if KEI else np.empty(0),
                daj=np.concatenate(KDAJ) if KDAJ else np.empty(0),
                dej=np.concatenate(KEJ) if KEJ else np.empty(0),
                a0=a0, e0=e0, e_hist=np.array(e_hist), a_hist=np.array(a_hist),
                kicks_per_orbit=kicks_per_orbit, pair_keys=pk)

# ----------------------------------------------------------------- replay --

def replay(run, eps_list):
    """Scout accounting replayed at each quantum eps over the kick stream."""
    N, a_mid = run["N"], run["a_mid"]
    a0, e0 = run["a0"], run["e0"]
    ki, kj, kt = run["kick_i"], run["kick_j"], run["kick_t"]
    crossings = ki.size
    kicks_app = 2 * crossings
    if kicks_app:
        rb = np.concatenate([ki, kj]).astype(np.int64)
        rt = np.concatenate([kt, kt])
        rda = np.concatenate([run["dai"], run["daj"]])
        rde = np.concatenate([run["dei"], run["dej"]])
        o = np.lexsort((rt, rb))
        rb, rt, rda, rde = rb[o], rt[o], rda[o], rde[o]
        csum_a = np.cumsum(rda); csum_e = np.cumsum(rde)
        gs = np.searchsorted(rb, np.arange(N), side="left")
        ge = np.searchsorted(rb, np.arange(N), side="right")
        pre_a = np.concatenate([[0.0], csum_a])[gs]
        pre_e = np.concatenate([[0.0], csum_e])[gs]
        a_at = a0[rb] + (csum_a - pre_a[rb])
        e_at = np.clip(e0[rb] + (csum_e - pre_e[rb]), 0.0, 0.95)
        chg = np.empty(rb.size, dtype=bool)
        chg[:-1] = rb[1:] != rb[:-1]
        chg[-1] = True
    else:
        rb = rt = a_at = e_at = chg = np.empty(0)
        gs = ge = np.zeros(N, dtype=np.int64)
    boundaries = np.arange(1, run["orbits"] + 1) * TAU
    out = {}
    for eps in eps_list:
        cell_a = eps * a_mid
        cell_e = eps
        ka0 = np.round(a0 / cell_a).astype(np.int64)
        ke0 = np.round(e0 / cell_e).astype(np.int64)
        if kicks_app:
            ka_at = np.round(a_at / cell_a).astype(np.int64)
            ke_at = np.round(e_at / cell_e).astype(np.int64)
            last = np.maximum(ge - 1, 0)
            has = ge > gs
            ka_fin = np.where(has, ka_at[last], ka0)
            ke_fin = np.where(has, ke_at[last], ke0)
        else:
            ka_fin, ke_fin = ka0.copy(), ke0.copy()
        dis = (ka_fin != ka0) | (ke_fin != ke0)
        D = int(dis.sum())

        def H(x):
            if x.size == 0: return 0.0
            _, c = np.unique(x, return_counts=True)
            p = c / c.sum()
            return float(-(p * np.log2(p)).sum())

        H_delta = H(ka_fin[dis] - ka0[dis]) + H(ke_fin[dis] - ke0[dis])
        id_bits = math.log2(N / max(D, 1))
        if D:
            _, cnt = np.unique(ka_fin[dis].astype(np.int64) * (1 << 24) + ke_fin[dis],
                               return_counts=True)
            cell_bits = math.log2(1 / eps) + 8
            shared = int((cnt >= 2).sum())
            R3_bits = float(np.sum(np.where(cnt >= 2, cell_bits + cnt * id_bits,
                                            cnt * (id_bits + H_delta / D))))
        else:
            cnt = np.empty(0); shared = 0; R3_bits = 0.0

        def Hj(kax, kex):
            _, c = np.unique(kax.astype(np.int64) * (1 << 24) + kex, return_counts=True)
            p = c / c.sum()
            return float(-(p * np.log2(p)).sum())

        Hj0, Hj1 = Hj(ka0, ke0), Hj(ka_fin, ke_fin)
        # D(t) from the live orbit-boundary snapshots (the kick stream is
        # grouped by body, so global time search on it is invalid; final
        # cells above come from the stream and match the snapshots exactly)
        ah, eh = run["a_hist"], run["e_hist"]
        Dt = []
        for k in range(1, len(ah)):
            ka_b = np.round(ah[k] / cell_a).astype(np.int64)
            ke_b = np.round(eh[k] / cell_e).astype(np.int64)
            Dt.append(int(((ka_b != ka0) | (ke_b != ke0)).sum()))
        # kicks before escape (the checker's instrument, native here)
        if kicks_app:
            crossed = (ka_at != ka0[rb]) | (ke_at != ke0[rb])
            wpos = np.arange(rb.size) - gs[rb]
            vals = np.where(crossed, wpos, 1 << 30)
            starts = np.where(ge > gs)[0]
            red_starts = gs[starts]
            firsts = np.minimum.reduceat(vals, red_starts) if red_starts.size else np.array([])
            esc_k = firsts[firsts < (1 << 30)] + 1
            esc_kicks_median = float(np.median(esc_k)) if esc_k.size else None
            esc_frac_multikick = float((esc_k >= 2).mean()) if esc_k.size else None
        else:
            esc_kicks_median = esc_frac_multikick = None
        t_orb = np.arange(1, len(Dt) + 1, dtype=float)
        Dv = np.array(Dt, float)
        sel = (Dv > 0) & (Dv < 0.05 * N) & (t_orb > 1)
        infl = (float(np.polyfit(np.log(t_orb[sel]), np.log(np.maximum(Dv[sel], 1)), 1)[0])
                if sel.sum() > 5 else None)
        selw = (Dv > 0) & (Dv < 0.3 * N) & (t_orb > 1)
        infl_wide = (float(np.polyfit(np.log(t_orb[selw]), np.log(np.maximum(Dv[selw], 1)), 1)[0])
                     if selw.sum() > 5 else None)
        out[f"{eps:g}"] = dict(
            eps=eps, D=D, D_over_N=D / N, crossings=crossings, kicks_app=kicks_app,
            s_part=D / max(kicks_app, 1), s_2event=D / max(2 * crossings, 1),
            R1_MB=D * 16 / 1e6, R2_MB=D * (id_bits + H_delta) / 8 / 1e6,
            R3_MB=R3_bits / 8 / 1e6, H_delta=H_delta, Hj0=Hj0, Hj1=Hj1,
            id_bits=id_bits, shared_frac=shared / max(len(cnt), 1),
            Dt=Dt, inflow_exp=infl, inflow_exp_wide=infl_wide,
            esc_kicks_median=esc_kicks_median,
            esc_frac_multikick=esc_frac_multikick)
    return out

def fit_power(x, y, ok=None):
    x, y = np.array(x, float), np.array(y, float)
    if ok is None:
        ok = np.isfinite(x) & np.isfinite(y) & (x > 0) & (y > 0)
    else:
        ok = np.asarray(ok, bool) & np.isfinite(y) & (y > 0)
    if ok.sum() < 3: return None
    return float(np.polyfit(np.log(x[ok]), np.log(y[ok]), 1)[0])

# ------------------------------------------------------------------- main --

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(here, "metrics-real.json")
    load = subprocess.run(["cat", "/proc/loadavg"], capture_output=True, text=True).stdout.split()
    R = {"machine": {"load1": load[0], "load5": load[1], "vcpu": 8}}
    print(f"machine: load1={load[0]} load5={load[1]} (8 vCPU, shared)", flush=True)

    # ---- positive control: no kicks -> exactly zero live bits ----
    c = propagate(N=300, orbits=3, kick=False)
    rc = replay(c, [1e-3])
    assert rc["0.001"]["D"] == 0 and rc["0.001"]["R2_MB"] == 0.0
    R["control_nokick"] = dict(D=0, R2_MB=0.0)
    print("control (kick=False): D=0, 0 live bits  PASS", flush=True)

    eps_sweep = [1e-2, 3e-3, 1e-3, 3e-4, 1e-4, 3e-5, 1e-5]

    def do(name, **kw):
        t0 = time.time()
        run = propagate(**kw)
        wall = time.time() - t0
        rep = replay(run, eps_sweep)
        kicks = run["kick_i"].size
        K_body_orbit = 2 * kicks / max(run["N"] * run["orbits"], 1)
        b = run["kick_b"]
        rho0 = 2.0 * np.count_nonzero(b < 0.01) / 0.01 / max(b.size, 1)
        pk = run["pair_keys"]
        if pk.size:
            _, pcnt = np.unique(pk, return_counts=True)
            repeat_frac = float(pcnt[pcnt >= 2].sum() / pcnt.sum())
            top_pair = int(pcnt.max())
        else:
            repeat_frac, top_pair = 0.0, 0
        if kicks:
            cntb = np.bincount(np.concatenate([run["kick_i"], run["kick_j"]]).astype(np.int64),
                               minlength=run["N"])
            disp = float(cntb.var() / max(cntb.mean(), 1e-9))
            bmed = float(np.median(b))
        else:
            disp, bmed = 0.0, None
        sig_e_t = [float(np.sqrt(np.mean(x ** 2))) for x in run["e_hist"]]
        d = dict(N=run["N"], W=run["W"], sigma_e=run["sigma_e"], m=run["m"],
                 b_det=run["b_det"], orbits=run["orbits"], seed=run["seed"],
                 contacts=run["contacts"], kicks=kicks, K_body_orbit=K_body_orbit,
                 wall_s=round(wall, 1), b_rho0=round(float(rho0), 1), b_median=bmed,
                 repeat_pair_kick_frac=repeat_frac, top_pair_kicks=top_pair,
                 kick_dispersion=disp, sigma_e_t=[round(s, 5) for s in sig_e_t],
                 eps=rep)
        R[name] = d
        print(f"{name}: kicks={kicks} K/body/orbit={K_body_orbit:.1f} wall={wall:.0f}s "
              f"rho_b0={rho0:.1f} repeat={repeat_frac:.3f} disp={disp:.2f} "
              f"sig_e {sig_e_t[0]:.4f}->{sig_e_t[-1]:.4f}", flush=True)
        for k, v in rep.items():
            print(f"   eps={k}: D={v['D']} D/N={v['D_over_N']:.4f} "
                  f"s_part={v['s_part']:.2e} inflow={v['inflow_exp']}", flush=True)
        return run, d

    # C1 baseline: toy's mass ladder, Sigma = N/W = 3e4/AU
    run1, d1 = do("C1_m1e-10", N=1500, W=0.05, sigma_e=0.05, m=1e-10, orbits=20, seed=7)
    # C2 mass lever x100
    do("C2_m1e-8", N=1500, W=0.05, sigma_e=0.05, m=1e-8, orbits=20, seed=7)
    # C3 saturation + real stirring: planetary-scale scatterer mass
    run3, d3 = do("C3_m1e-6", N=1500, W=0.05, sigma_e=0.05, m=1e-6, orbits=10, seed=7)
    # C4 surface density x3 (narrower belt, same N)
    do("C4_S9e4", N=1500, W=0.05 / 3.0, sigma_e=0.05, m=1e-10, orbits=10, seed=7)
    # C5 surface density /3, N/3
    do("C5_S1e4", N=500, W=0.05, sigma_e=0.05, m=1e-10, orbits=20, seed=7)
    # C6 seed robustness
    do("C6_seed2", N=1500, W=0.05, sigma_e=0.05, m=1e-10, orbits=10, seed=20261012)

    # ---- alpha on the partial regime only (per config) ----
    R["alpha_partial_real"] = {}
    for name in ("C1_m1e-10", "C2_m1e-8", "C3_m1e-6", "C4_S9e4", "C5_S1e4", "C6_seed2"):
        eps_rows = R[name]["eps"]
        xs = [v["eps"] for v in eps_rows.values()]
        ys = [v["s_part"] for v in eps_rows.values()]
        partial = np.array([v["D_over_N"] < 0.5 for v in eps_rows.values()])
        R["alpha_partial_real"][name] = dict(
            alpha_partial=fit_power(xs, ys, partial),
            n_partial_rows=int(partial.sum()),
            alpha_all=fit_power(xs, ys))
        print(f"alpha_partial[{name}] = {R['alpha_partial_real'][name]['alpha_partial']} "
              f"({int(partial.sum())}/{len(xs)} rows partial)", flush=True)

    # ---- corrected alpha_partial for the ORIGINAL toy metrics ----
    try:
        orig = json.load(open(os.path.join(here, "orig-metrics.json")))
        fix = {}
        for key, blk in orig.items():
            if not key.startswith("S2_m"): continue
            rows = blk["rows"]
            xs = [float(r[0]) for r in rows]
            ys = [float(r[1]) for r in rows]
            # partial regime = unsaturated rows; the toy's own rows show the
            # plateau (m>=1e-8 saturated at every eps).  Use eps in
            # [1e-2, 1e-4] for m=1e-10 (checker's refit window); report
            # None where no partial regime exists.
            if key == "S2_m1e-10":
                sel = np.array([1e-2 <= x <= 1e-4 for x in xs])
                fix[key] = dict(alpha_partial=fit_power(xs, ys, sel),
                                stored_mislabeled=blk["alpha_partial"],
                                n_rows=int(sel.sum()))
            else:
                fix[key] = dict(alpha_partial=None, saturated=True,
                                stored_mislabeled=blk["alpha_partial"])
        R["alpha_partial_toy_corrected"] = fix
        print("toy alpha corrected:", json.dumps(fix), flush=True)
    except Exception as ex:
        R["alpha_partial_toy_corrected"] = {"error": str(ex)}

    # ---- saturation store vs B18 (bytes per live body, reported at 1e9) ----
    v = R["C3_m1e-6"]["eps"]["0.001"]
    N = R["C3_m1e-6"]["N"]; D = v["D"]
    # Elias-Fano for the scarred set, plus per-scar delta at its entropy
    ef_bits = D * math.log2(N / max(D, 1)) + 2.0 * D if D < N else 2.0 * N
    store_bits = ef_bits + D * (v["id_bits"] + v["H_delta"])
    store_B_per_body = store_bits / N / 8.0
    floor_hist = v["Hj1"] / 8.0                        # histogram floor
    floor_prog = (0.126 + v["H_delta"] * D / N) / 8.0  # program + delta entropy
    R["B18_saturation_store"] = dict(
        config="C3_m1e-6", eps=1e-3, D=D, D_over_N=v["D_over_N"],
        H_delta_bits=v["H_delta"], Hj1=v["Hj1"],
        store_bytes_per_body=store_B_per_body,
        floor_hist_bytes=floor_hist, floor_prog_bytes=floor_prog,
        B18_hist_ok=bool(store_B_per_body <= 2 * floor_hist + 2),
        B18_prog_ok=bool(store_B_per_body <= 2 * floor_prog + 2),
        total_GB_at_1e9=store_B_per_body * 1e9 / 1e9)
    print("B18 saturation store:", json.dumps(R["B18_saturation_store"], indent=1), flush=True)

    # ---- 1e9 extrapolation at fixed surface density (rate per body fixed) ----
    P_gs = 1.0 * YR_S / RTF     # a=1 (GM=1) => P = 1 yr => 3.156e5 game-seconds
    extrap = {}
    for name in ("C1_m1e-10", "C4_S9e4", "C5_S1e4", "C2_m1e-8"):
        d = R[name]
        v = d["eps"]["0.001"]
        K = d["K_body_orbit"]
        ev_gs = 1e9 * K / P_gs                       # kick applications/gs
        mb_h_R1 = ev_gs * 3600 * v["s_part"] * 16 / 1e6
        sigma = d["N"] / d["W"]
        extrap[name] = dict(sigma_per_AU=sigma, K_body_orbit=K, s=v["s_part"],
                            D_over_N=v["D_over_N"], ev_per_gs=ev_gs,
                            MB_per_play_hour_R1=mb_h_R1)
    R["extrap_1e9_fixed_sigma"] = extrap
    print("1e9 fixed-sigma extrapolation:", json.dumps(extrap, indent=1), flush=True)

    # ---- toy at the real, measured rate (matched kicks/body/orbit) ----
    sys.path.insert(0, here)
    import hlive_scout as toy
    K_real = d1["K_body_orbit"]
    toy_rows = []
    for eps in eps_sweep:
        rr, _ = toy.run(N=1500, gamma0=K_real, sigma_e=0.05, m=1e-10, eps=eps,
                        steps=20 * 128, orbits=20, seed=7)
        toy_rows.append((eps, rr["D"], rr["events"], rr["s_frac"]))
        print(f"toy@K={K_real:.1f} eps={eps:g}: D={rr['D']} events={rr['events']} "
              f"s_part={rr['D'] / max(rr['events'], 1):.2e}", flush=True)
    R["toy_matched_rate"] = dict(
        K_body_orbit=K_real, N=1500, m=1e-10, orbits=20,
        rows=[(f"{a:g}", b, c, d) for a, b, c, d in toy_rows])

    json.dump(R, open(out_path, "w"), indent=1)
    print("wrote", out_path, flush=True)
