#!/usr/bin/env python3
"""Tangency windows: numeric_window (crate replica, cert A) vs travel-time-difference
windows (cert B: global worst-case bounds; cert B2: sub-arc + per-interval bounds),
against a dense s-domain firing-set truth. Run 20261008-2113-scout-6652.
Faithful port of crates/encounters/src/{kepler,pairs}.rs for the Wide-section path;
float replica (scout falsifier). Disclosed deviations: passage ticks not rounded;
refine() counted as 6 evals + golden section; numeric_window capped at MAXD d_of_s
calls per side; truth grids as stated in truth_s_domain.
"""
import json, math, time
import numpy as np

TAU = 2.0 * math.pi
TICKS = 4294967296.0
RHO = 8e-3
K_SAMPLE = 5    # B: h samples across the arc
K2 = 17         # B2: radial-grid samples across the arc
MAXD = 300      # d_of_s cap per side for cert A
rng = np.random.default_rng(20261008)

class Body:
    __slots__ = ("a","e","pom","n","p","sq","cp","sp","period","tp")
    def __init__(self, period, e, pom, lam0):
        n = TAU * TICKS / period
        a = n ** (-2.0/3.0)
        pom = pom % TAU
        m0 = (lam0 - pom) % TAU
        tpf = (-(m0 / TAU) * period) % period
        self.a, self.e, self.pom, self.n = a, e, pom, n
        self.p = a * (1.0 - e*e); self.sq = math.sqrt(1.0 - e*e)
        self.cp, self.sp = math.cos(pom), math.sin(pom)
        self.period = period; self.tp = int(round(tpf)) % period
    @staticmethod
    def from_elements(a0, e, pom, lam0):
        return Body(round(TAU * a0**1.5 * TICKS), e, pom, lam0)
    def rmin(self): return self.a * (1.0 - self.e)
    def rmax(self): return self.a * (1.0 + self.e)
    def binet(self):
        u = 1.0 / self.p
        return (u, self.e*self.cp*u, self.e*self.sp*u)
    def vmax(self): return (1.0 + self.e) / math.sqrt(self.p)
    def u_at(self, x):
        U, V, W = self.binet()
        return U + V*math.cos(x) + W*math.sin(x)
    def mean_at_longitude(self, th):
        f = th - self.pom
        ea = 2.0 * math.atan2(math.sqrt(1.0-self.e)*math.sin(0.5*f),
                              math.sqrt(1.0+self.e)*math.cos(0.5*f))
        return (ea - self.e*math.sin(ea)) % TAU
    def travel(self, th0, th1):
        return ((self.mean_at_longitude(th1) - self.mean_at_longitude(th0)) % TAU) / self.n
    def t_pass(self, th):
        return (self.tp + (self.mean_at_longitude(th) / TAU) * self.period) / TICKS
    def state_at_mean(self, m):
        e = self.e; m = m % TAU
        ea = m + e*math.sin(m)*(1.0 + e*math.cos(m))
        for _ in range(12):
            d = (ea - e*math.sin(ea) - m) / (1.0 - e*math.cos(ea))
            ea -= d
            if abs(d) < 1e-15: break
        se, ce = math.sin(ea), math.cos(ea)
        xp = self.a * (ce - e); yp = self.a * self.sq * se
        edot = self.n / (1.0 - e*ce)
        vxp = -self.a * se * edot; vyp = self.a * self.sq * ce * edot
        return (xp*self.cp - yp*self.sp, xp*self.sp + yp*self.cp,
                vxp*self.cp - vyp*self.sp, vxp*self.sp + vyp*self.cp)

def states_at_mean_vec(b, m):
    m = np.asarray(m) % TAU
    e = b.e
    U, V, W = b.binet()
    ea = m + e*np.sin(m)*(1.0 + e*np.cos(m))
    for _ in range(12):
        d = (ea - e*np.sin(ea) - m) / (1.0 - e*np.cos(ea))
        ea = ea - d
    se, ce = np.sin(ea), np.cos(ea)
    xp = b.a*(ce - e); yp = b.a*b.sq*se
    edot = b.n/(1.0 - e*ce)
    vxp = -b.a*se*edot; vyp = b.a*b.sq*ce*edot
    return (np.stack([xp*b.cp - yp*b.sp, xp*b.sp + yp*b.cp]),
            np.stack([vxp*b.cp - vyp*b.sp, vxp*b.sp + vyp*b.cp]))

# ---------------- crate replica: sections and windows ----------------

def eps_u(bi, bj, rho):
    rmin = min(bi.rmin(), bj.rmin()); rmax = max(bi.rmax(), bj.rmax())
    kappa = rmax*rmax*max(bi.e, bj.e) / (min(bi.p, bj.p) * rmin)
    return 1.5 * rho * (1.0 + kappa) / (rmin*rmin)

def classify_arcs(bi, bj, rho):
    """Port of sections() arc classification -> list of (c, dm, dp, cross) or 'full' or []."""
    a, b = bi.binet(), bj.binet()
    du, dv, dw = a[0]-b[0], a[1]-b[1], a[2]-b[2]
    r = math.hypot(dv, dw); eps = eps_u(bi, bj, rho)
    if abs(du) - r >= eps: return []
    if r < 1e-300: return "full"
    th0 = math.atan2(dw, dv)
    c_lo, c_hi = (-eps - du)/r, (eps - du)/r
    merged0, merged_pi = c_hi >= 1.0, c_lo <= -1.0
    phi1 = math.acos(min(1.0, c_hi)); phi2 = math.acos(max(-1.0, c_lo))
    if merged0 and merged_pi: return "full"
    if merged0: return [(th0, phi2, phi2, False)]
    if merged_pi: return [(th0+math.pi, math.pi - phi1, math.pi - phi1, False)]
    phx = math.acos(max(-1.0, min(1.0, -du/r)))
    return [(th0+phx, phx-phi1, phi2-phx, True),
            (th0-phx, phi2-phx, phx-phi1, True)]

def rel_state(bi, bj, mi, mj, tau, s):
    si = bi.state_at_mean(mi + bi.n*(tau - s))
    sj = bj.state_at_mean(mj + bj.n*tau)
    return ((si[0]-sj[0], si[1]-sj[1]), (si[2]-sj[2], si[3]-sj[3]))

def dist_at(bi, bj, mi, mj, tau, s):
    (dx, dy), _ = rel_state(bi, bj, mi, mj, tau, s)
    return math.hypot(dx, dy)

def d_of_s(bi, bj, th, dj, s, evals):
    """D(s): min distance while j crosses the arc; k=32 samples, dr.dv brackets refined.
    Faithful replica of pairs.rs::d_of_s (refine counted as 6 evals + golden section)."""
    mi, mj = bi.mean_at_longitude(th), bj.mean_at_longitude(th)
    lo, hi = -dj[0], dj[1]
    k = 32; h = (hi - lo) / k
    (r0x, r0y), (v0x, v0y) = rel_state(bi, bj, mi, mj, lo, s)
    evals[0] += 1
    best = math.hypot(r0x, r0y)
    gp = r0x*v0x + r0y*v0y
    for q in range(1, k+1):
        t = lo + h*q
        (rx, ry), (vx, vy) = rel_state(bi, bj, mi, mj, t, s)
        evals[0] += 1
        best = min(best, math.hypot(rx, ry))
        g = rx*vx + ry*vy
        if gp < 0.0 <= g:
            evals[0] += 6   # refine() cost
            a_, b_ = t-h, t
            for _ in range(24):
                m1 = a_ + 0.382*(b_-a_); m2 = a_ + 0.618*(b_-a_)
                if dist_at(bi, bj, mi, mj, m1, s) < dist_at(bi, bj, mi, mj, m2, s): b_ = m2
                else: a_ = m1
            best = min(best, dist_at(bi, bj, mi, mj, 0.5*(a_+b_), s))
        gp = g
    return best

def numeric_window(bi, bj, th, dj, ab, rho, evals):
    """Cert A: conservative advancement in s (crate replica). (l, r) | None | ("cap",a,b)."""
    lip = bi.vmax() * 1.001; stop = rho * 1.05
    a, b = ab
    s = a; cnt = 0
    while True:
        if s > b: return None
        d = d_of_s(bi, bj, th, dj, s, evals)
        if d < stop: break
        s += (d - rho) / lip; cnt += 1
        if cnt > MAXD: return ("cap", a, b)
    left = s
    s = b; cnt = 0
    while True:
        d = d_of_s(bi, bj, th, dj, s, evals)
        if d < stop or s <= left: break
        s -= (d - rho) / lip; cnt += 1
        if cnt > MAXD: return ("cap", a, b)
    return (left, max(s, left))

def cert_A_wide(bi, bj, th, dm, dp, rho, evals):
    dj = (bj.travel(th-dm, th), bj.travel(th, th+dp))
    di = (bi.travel(th-dm, th), bi.travel(th, th+dp))
    cap = (dj[0]+di[1], dj[1]+di[0])
    return numeric_window(bi, bj, th, dj, (-cap[0], cap[1]), rho, evals), cap, (di, dj)

# ---------------- cert B and B2: travel-time-difference windows ----------------

def signed_travel(b, th, x):
    return b.travel(th, x) if x >= th else -b.travel(x, th)

def cert_B(bi, bj, th, dm, dp, rho, evals):
    """W = [-max h - c - m, -min h + c + m]; global worst-case bounds (first cut)."""
    lam = [th - dm + (dp+dm)*q/(K_SAMPLE-1) for q in range(K_SAMPLE)]
    hvals = []
    for x in lam:
        hvals.append(signed_travel(bi, th, x) - signed_travel(bj, th, x))
        evals[0] += 2
    us_i = [bi.u_at(x) for x in lam]; us_j = [bj.u_at(x) for x in lam]
    ri_min, ri_max = 1.0/max(us_i), 1.0/min(us_i)
    rj_min, rj_max = 1.0/max(us_j), 1.0/min(us_j)
    if min(ri_min, rj_min) <= 4*rho:
        return None, evals, "route:rmin"
    H = ri_max**2/math.sqrt(bi.p) + rj_max**2/math.sqrt(bj.p)
    rmin_arc = min(ri_min, rj_min)
    c = (2.0*rho/rmin_arc) * (ri_max**2/math.sqrt(bi.p) + rj_max**2/math.sqrt(bj.p))
    margin = H * ((dm+dp)/(K_SAMPLE-1)) * 0.5
    return (-max(hvals) - c - margin, -min(hvals) + c + margin), evals, "ok"

def cert_B2(bi, bj, th, dm, dp, rho, evals):
    """Tight variant: encounters require radial separation < rho, confining the meeting
    longitude to a sub-arc; h' bounded per sub-interval as the difference of two monotone
    functions (r^2/L is monotone in longitude between apses); tolerance from the sub-arc."""
    lam_all = [th - dm + (dp+dm)*q/(K2-1) for q in range(K2)]
    rad = [abs(1.0/bi.u_at(x) - 1.0/bj.u_at(x)) for x in lam_all]
    evals[0] += 2*K2
    ok = [k for k in range(K2) if rad[k] < 2.0*rho]
    if not ok:
        return None, evals, "route:noradial"
    lam = lam_all[max(ok[0]-1,0):min(ok[-1]+2, K2)]
    if len(lam) < 2:
        return None, evals, "route:thin"
    hvals, gvals, rads = [], [], []
    for x in lam:
        hvals.append(signed_travel(bi, th, x) - signed_travel(bj, th, x))
        ri, rj = 1.0/bi.u_at(x), 1.0/bj.u_at(x)
        rads.extend([ri, rj])
        gvals.append(ri*ri/math.sqrt(bi.p) - rj*rj/math.sqrt(bj.p))
        evals[0] += 4
    breaks = set(range(len(lam)))
    for b in (bi, bj):
        for ext in (b.pom, b.pom+math.pi):
            for k in range(-2, 3):
                e_ = ext + k*TAU
                if lam[0] < e_ < lam[-1]:
                    breaks.add(sum(1 for x in lam if x < e_))
    ivs = sorted(breaks)
    margin = 0.0
    for a_, b_ in zip(ivs[:-1], ivs[1:]):
        if b_ - a_ >= 1:
            gb = max(abs(gvals[a_]), abs(gvals[b_]))
            margin = max(margin, gb*(lam[b_]-lam[a_])*0.5)
    rmax_sa = max(rads); rmin_sa = min(rads)
    if rmin_sa <= 4*rho:
        return None, evals, "route:rmin"
    c = (2.0*rho/rmin_sa) * (rmax_sa**2/math.sqrt(bi.p) + rmax_sa**2/math.sqrt(bj.p))
    return (-max(hvals) - c - margin, -min(hvals) + c + margin), evals, "ok"

# ---------------- truth: firing set in s-space ----------------

def D_grid(bi, bj, th, dj, svals):
    """Vectorized D(s) = min over tau in the arc of |r_i - r_j|."""
    mi, mj = bi.mean_at_longitude(th), bj.mean_at_longitude(th)
    taus = np.linspace(-dj[0], dj[1], 768)
    out = np.empty(len(svals))
    for k, s in enumerate(svals):
        Si, _ = states_at_mean_vec(bi, mi + bi.n*(taus - s))
        Sj, _ = states_at_mean_vec(bj, mj + bj.n*taus)
        out[k] = np.hypot(Si[0]-Sj[0], Si[1]-Sj[1]).min()
    return out

def truth_s_domain(bi, bj, th, dj, winB2, cap, rho):
    """All s with D(s) < rho: fine scan over B2's window widened 3x, coarse Lipschitz-safe
    scan of the rest at rho/(4 lip). Returns (fires, outside_count)."""
    lip = bi.vmax() * 1.001
    a_dom, b_dom = -cap[0], cap[1]
    fires = []; outside = 0
    if winB2 is not None:
        widen = 3.0*(winB2[1]-winB2[0])
        wlo, whi = max(a_dom, winB2[0]-widen), min(b_dom, winB2[1]+widen)
        if whi > wlo:
            sv = np.arange(wlo, whi, rho/(2.0*(bi.vmax()+bj.vmax())))
            dvals = D_grid(bi, bj, th, dj, sv)
            fires.extend(sv[dvals < rho].tolist())
        segs = [(a_dom, min(winB2[0]-widen, b_dom)),
                (max(winB2[1]+widen, a_dom), b_dom)]
    else:
        segs = [(a_dom, b_dom)]
    for (lo, hi) in segs:
        if hi <= lo: continue
        sv = np.arange(lo, hi, rho/(4.0*lip))
        if len(sv):
            dvals = D_grid(bi, bj, th, dj, sv)
            outside += int((dvals < rho).sum())
            fires.extend(sv[dvals < rho].tolist())
    return np.array(fires), outside

# ---------------- pair generation ----------------

def body_from_binet(target, lam0):
    U, V, W = target
    p = 1.0/U; e = math.hypot(V, W)/U
    if e > 0.97 or e < 1e-6: return None
    pom = math.atan2(W, V)
    return Body.from_elements(p/(1.0-e*e), e, pom, lam0)

def make_pair(fam):
    """Wide/merged arcs arise when the two Binet points sit within ~eps_u of each other.
    F1 barely-crossing (gap<0), F2 one-sided (gap>0), F4 near-identical, F3x high-e mix."""
    for _ in range(300):
        a0 = rng.uniform(1.5, 3.0)
        e = rng.uniform(0.6, 0.95) if fam == "F3x" else min(float(rng.rayleigh(0.12)), 0.95)
        bj = Body.from_elements(a0, e, rng.uniform(0, TAU), rng.uniform(0, TAU))
        jb = np.array(bj.binet()); eps = eps_u(bj, bj, RHO)
        mag = rng.uniform(0.3, 3.0) * eps
        u = rng.normal(size=3); u /= np.linalg.norm(u)
        R = mag * math.hypot(u[1], u[2])
        if fam == "F4":
            dU = mag * u[0]
        elif fam == "F2":
            dU = (1.0 if u[0] >= 0 else -1.0) * (R + rng.uniform(0.05, 0.9) * eps)
        elif fam == "F3x":
            dU = (1.0 if u[0] >= 0 else -1.0) * (R + rng.uniform(-0.9, 0.9) * eps)
        else:
            dU = (1.0 if u[0] >= 0 else -1.0) * (R + rng.uniform(-0.9, -0.05) * eps)
        tgt = jb + np.array([dU, mag*u[1], mag*u[2]])
        if tgt[0] <= 0: continue
        bi = body_from_binet(tuple(tgt), rng.uniform(0, TAU))
        if bi is None: continue
        arcs = classify_arcs(bi, bj, RHO)
        if not isinstance(arcs, list) or len(arcs) == 0: continue
        return bi, bj, arcs
    return None, None, None

# ---------------- main ----------------

def main():
    t_start = time.perf_counter()
    fams = ["F1", "F2", "F4", "F3x"]
    NP = 30
    results = {f: [] for f in fams}
    for fam in fams:
        k = 0; tries = 0
        while k < NP and tries < NP*3 and time.perf_counter() - t_start < 300:
            tries += 1
            bi, bj, arcs = make_pair(fam)
            if bi is None: continue
            k += 1
            for (c, dm, dp, cross) in arcs:
                th = c % TAU
                wide = (not cross) or max(dm, dp) >= 0.2
                if not wide: continue
                evalsA = [0]; evalsB = [0]
                winA, cap, (di, dj) = cert_A_wide(bi, bj, th, dm, dp, RHO, evalsA)
                winB, _, flagB = cert_B(bi, bj, th, dm, dp, RHO, evalsB)
                winB2, _, flagB2 = cert_B2(bi, bj, th, dm, dp, RHO, evalsB)
                fires, outside = truth_s_domain(bi, bj, th, dj, winB2, cap, RHO)
                missA = missB = missB2 = 0
                for s in fires:
                    if isinstance(winA, tuple) and winA[0] != "cap":
                        if not (winA[0] - 1e-9 <= s <= winA[1] + 1e-9): missA += 1
                    if winB is not None and not (winB[0] - 1e-9 <= s <= winB[1] + 1e-9): missB += 1
                    if winB2 is not None and not (winB2[0] - 1e-9 <= s <= winB2[1] + 1e-9): missB2 += 1
                w = lambda v: (v[1]-v[0]) if v is not None else float("nan")
                wA = w(winA) if (isinstance(winA, tuple) and winA[0] != "cap") else float("nan")
                results[fam].append(dict(
                    e_i=round(bi.e,3), e_j=round(bj.e,3), dm=round(dm,3), dp=round(dp,3),
                    cross=bool(cross), evalsA=evalsA[0], evalsB=evalsB[0],
                    winA=("none" if winA is None else ("cap" if winA[0]=="cap" else "w")),
                    wA=wA, wB=w(winB), wB2=w(winB2), flagB=flagB, flagB2=flagB2,
                    nfire=len(fires), missA=missA, missB=missB, missB2=missB2,
                    outside=outside))
    summ = {}
    for f in fams:
        rs = results[f]
        if not rs: summ[f] = "none"; continue
        ea = [r["evalsA"] for r in rs]; eb = [r["evalsB"] for r in rs]
        valid = [r for r in rs if isinstance(r["winA"], str) and r["winA"] == "w" and r["wA"]==r["wA"]]
        ratios = [(r["evalsA"]/max(r["evalsB"],1)) for r in valid]
        wB2r = [r["wB2"]/r["wA"] for r in valid if r["wB2"]==r["wB2"]]
        wBr = [r["wB"]/r["wA"] for r in valid if r["wB"]==r["wB"]]
        summ[f] = dict(
            n_sections=len(rs),
            evalsA_med=float(np.median(ea)), evalsA_p90=float(np.percentile(ea,90)),
            evalsB_med=float(np.median(eb)), evalsB_max=int(max(eb)),
            ratio_med=float(np.median(ratios)) if ratios else None,
            ratio_min=float(min(ratios)) if ratios else None,
            widthB_ratio_med=float(np.median(wBr)) if wBr else None,
            widthB2_ratio_med=float(np.median(wB2r)) if wB2r else None,
            widthB2_ratio_p90=float(np.percentile(wB2r,90)) if wB2r else None,
            A_none=sum(1 for r in rs if r["winA"] is None),
            B_route=sum(1 for r in rs if r["flagB"] != "ok"),
            B2_route=sum(1 for r in rs if r["flagB2"] != "ok"),
            missA=sum(r["missA"] for r in rs), missB=sum(r["missB"] for r in rs),
            missB2=sum(r["missB2"] for r in rs), outside_fires=sum(r["outside"] for r in rs),
            fire_total=sum(r["nfire"] for r in rs),
            sections_fired=sum(1 for r in rs if r["nfire"] > 0))
    with open(__file__.replace(".py", "-out.json"), "w") as fh:
        json.dump(dict(summary=summ, detail={f: results[f][:8] for f in fams}), fh, indent=1)
    print(json.dumps(summ, indent=1))
    print(f"wall {time.perf_counter()-t_start:.1f}s")

if __name__ == "__main__":
    main()
