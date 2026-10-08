#!/usr/bin/env python3
"""Second author on run 20261008-2113-scout-6652: the checker's named experiment.

The checker graded the travel-time-difference window silver and named three gaps:
(a) the radial never-fires routing in cert B2 was an unmargined 17-sample test that
    falsely routed 3/6 high-e sections while real encounters existed (F3x);
(b) the wide-crossing half of Kind::Wide (a crossing whose arc is long, pairs.rs:131)
    was never measured - the generator structurally makes merged arcs only;
(c) the >=10x cost claim rested on an unmeasured per-call ratio, evalsB counted
    B and B2 together, and the outside-window truth was asserted, not certified.

Starting from the run's own replica (tangency.py), dissection of the F3x miss found
the hole UNDER the checker's, and a second one beside it:

  HOLE 1 (under the checker's). The original admissibility filter
  "|Delta r(lambda)| < 2 rho at the common longitude" is unsound at high e: the two
  bodies meet at DIFFERENT longitudes (each within a rho-sweep of the meeting
  longitude lambda*), and dr/dlambda = r^2 e sin f / p is large at high e, so real
  meeting zones are excluded - the same hole as the false "never-fires" routes.
  Sound filter (cert B3): per apse-split segment, each body's achievable radius
  range over the segment extended by its sweep sw_k = rho / rmin_orbit_k
  (Lipschitz-inflated), admissible iff the pooled ranges overlap within rho.

  HOLE 2 (new). The replica's D(s) uses mod-TAU mean anomalies, so it is exactly
  lattice-periodic: D(s + k Ti + m Tj) = D(s). Cert A's numeric window is
  alias-complete (it crawls the whole cap domain); the travel-time window as
  originally derived covers ONE branch, and is complete only when the cap domain
  fits inside one lattice cell - true on F1/F2/F4 (domains ~5-11 vs periods ~12-17),
  false on F3x (domains ~20+). The two holes cancelled on the measured families:
  the family that would have exposed hole 2 was routed out by hole 1. The fix is
  alias completion: the window is the union of W_0 + {k Ti + m Tj} over the cap
  domain (returned as its hull, the crate's Section being one interval).

Also closed: the h margin now bounds |h'| per atomic (apse-split) segment by the
endpoint-range rectangle (the original's g-monotonicity assumption fails across
apse-straddling sample gaps and at interior sign changes of g); cert B's global
margin doubled to H*step (was H*step/2, unsound by 2x); the sweep tolerance c uses
orbit-wide extrema (the sweep may leave the arc).

Truth: certified hierarchical scan. Lipschitz confirm threshold
rho + Sigma*(h/2 + tstep/2) in both s and tau, refinement of fire-free violations
(depth <= 6), fires detected at every depth; windows containing a detected fire are
certified only to 2*h around it (disclosed; cert margins are O(rho) >> h).

F5: a wide-crossing family (cross=True, max(dm,dp) >= 0.2) plus a census of how
often wide-crossing arises among engineered tangencies.

Wall clock: per-call microbench mean_at_longitude vs state_at_mean, and end-to-end
per-section timings of cert A vs cert B3. evalsB and evalsB3 counted separately.

Families run in priority order: F3x (the kill), F5 (the unmeasured half), then
F1/F2/F4 regression. `python3 second.py` regenerates second-out.json (~5-8 min).
"""
import json, math, time
import numpy as np
import tangency as T
from tangency import (TAU, TICKS, RHO, Body, classify_arcs, eps_u, cert_A_wide,
                      signed_travel, states_at_mean_vec, make_pair)

K2 = 17
MAX_DEPTH = 3
rng2 = np.random.default_rng(20261009)

# ---------------- alias completion over the passage lattice ----------------

def alias_complete(win0, bi, bj, cap):
    """Union of win0 + {k Ti + m Tj} intersected with the cap domain, as its hull
    (the crate's Section is one interval) plus the component count. The replica's
    D(s) is exactly lattice-periodic, so every alias of a covered fire is covered."""
    a_dom, b_dom = -cap[0], cap[1]
    Ti, Tj = bi.period/TICKS, bj.period/TICKS
    reach = (b_dom - a_dom) + (win0[1] - win0[0])
    K = int(reach/Ti) + 1; M = int(reach/Tj) + 1
    ivs = []
    for k in range(-K, K+1):
        for m in range(-M, M+1):
            sh = k*Ti + m*Tj
            lo_ = max(a_dom, win0[0] + sh); hi_ = min(b_dom, win0[1] + sh)
            if hi_ > lo_: ivs.append((lo_, hi_))
    if not ivs: return None, 0
    ivs.sort()
    merged = [list(ivs[0])]
    for lo_, hi_ in ivs[1:]:
        if lo_ <= merged[-1][1]: merged[-1][1] = max(merged[-1][1], hi_)
        else: merged.append([lo_, hi_])
    return (merged[0][0], merged[-1][1]), len(merged)

def _caps(bi, bj, th, dm, dp):
    dj = (bj.travel(th-dm, th), bj.travel(th, th+dp))
    di = (bi.travel(th-dm, th), bi.travel(th, th+dp))
    return (dj[0]+di[1], dj[1]+di[0])

# ---------------- cert B (first cut), sound margin + alias completion ----------------

def cert_B_s(bi, bj, th, dm, dp, rho, evals):
    lam = [th - dm + (dp+dm)*q/(T.K_SAMPLE-1) for q in range(T.K_SAMPLE)]
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
    c = (2.0*rho/min(ri_min, rj_min)) * H
    margin = H * ((dm+dp)/(T.K_SAMPLE-1))       # sound: |h - nearest sample| <= H*step
    win0 = (-max(hvals) - c - margin, -min(hvals) + c + margin)
    win, _ = alias_complete(win0, bi, bj, _caps(bi, bj, th, dm, dp))
    return win, evals, "ok"

# ---------------- cert B3: sound travel-time-difference window ----------------

def _r_range(rp, rq, w_ext, e, p):
    """Sound (lo, hi) bound on r over an interval of half-width w_ext around the
    segment with endpoint radii rp, rq, given |dr/dlam| <= r^2 e / p: fixed point
    from below (monotone increasing), 5 steps + fudge."""
    base_lo, base_hi = min(rp, rq), max(rp, rq)
    lo, hi = base_lo, base_hi
    for _ in range(5):
        b = hi*hi*e/p
        lo = max(1e-12, base_lo - b*w_ext)
        hi = base_hi + b*w_ext
    hi *= 1.0 + 1e-9; lo = max(1e-12, lo*(1.0 - 1e-9))
    return lo, hi

def cert_B3(bi, bj, th, dm, dp, rho, evals):
    lo, hi = th - dm, th + dp
    if not hi > lo:
        return None, evals, "route:degenerate"
    step = (hi - lo)/(K2-1)
    sw_i = rho/max(bi.rmin(), 1e-9); sw_j = rho/max(bj.rmin(), 1e-9)
    if min(bi.rmin(), bj.rmin()) <= 4*rho:
        return None, evals, "route:rmin"
    rcache = {}
    def radii(x):
        if x not in rcache:
            rcache[x] = (1.0/bi.u_at(x), 1.0/bj.u_at(x))
        return rcache[x]
    for q in range(K2):
        radii(lo + step*q)
    evals[0] += 2*K2
    # apses of either body inside (lo, hi): owner radius closed form, other evaluated
    aps = []
    for kb, b in ((0, bi), (1, bj)):
        for base, is_peri in ((b.pom, True), (b.pom+math.pi, False)):
            k0 = math.ceil((lo - base)/TAU)
            for k in (k0, k0+1):
                e_ = base + k*TAU
                if lo < e_ < hi:
                    r_own = b.p/(1.0 + (b.e if is_peri else -b.e))
                    other = bj if kb == 0 else bi
                    evals[0] += 1
                    rcache[e_] = (r_own, 1.0/other.u_at(e_)) if kb == 0 else \
                                 (1.0/other.u_at(e_), r_own)
                    aps.append(e_)
    allb = sorted([(lo + step*q, True) for q in range(K2)] + [(e_, False) for e_ in aps])
    # admissibility (hole 1 fixed): pooled sweep-extended radius ranges overlap within rho
    def check(p, q, rip, rjp, riq, rjq):
        w_i = (q-p)/2 + sw_i; w_j = (q-p)/2 + sw_j
        li, hi_ = _r_range(rip, riq, w_i, bi.e, bi.p)
        lj, hj_ = _r_range(rjp, rjq, w_j, bj.e, bj.p)
        return max(li - hj_, lj - hi_)   # > rho: provably no meeting longitude here
    adm = []
    for (p, sp), (q, sq) in zip(allb[:-1], allb[1:]):
        if q <= p: continue
        rip, rjp = radii(p); riq, rjq = radii(q)
        gap = check(p, q, rip, rjp, riq, rjq)
        if gap > 6*rho: continue                 # far from admissible: excluded
        if gap <= rho:
            adm.append((p, q)); continue
        m = 0.5*(p+q)                            # near threshold: split once
        radii(m); evals[0] += 2
        rim, rjm = radii(m)
        if check(p, m, rip, rjp, rim, rjm) <= rho: adm.append((p, m))
        if check(m, q, rim, rjm, riq, rjq) <= rho: adm.append((m, q))
    if not adm:
        return None, evals, "route:noradial"      # provable: no meeting longitude
    lo_a = min(p for (p, q) in adm); hi_a = max(q for (p, q) in adm)
    slice_ = [x for (x, is_s) in allb if is_s and lo_a - step <= x <= hi_a + step]
    if len(slice_) < 2:
        return None, evals, "route:thin"
    sl0, sl1 = slice_[0], slice_[-1]
    inb = [x for (x, _) in allb if sl0 <= x <= sl1]
    # sweep tolerance: orbit-wide extrema (the sweep may leave the arc/slice)
    c = rho * (bi.rmax()**2/(math.sqrt(bi.p)*bi.rmin()) +
               bj.rmax()**2/(math.sqrt(bj.p)*bj.rmin()))
    # h on the slice and the sound per-segment |h'| rectangle margin
    hvals = []
    for x in inb:
        hvals.append(signed_travel(bi, th, x) - signed_travel(bj, th, x))
        evals[0] += 2
    margin_h = 0.0
    for p, q in zip(inb[:-1], inb[1:]):
        rip, rjp = radii(p); riq, rjq = radii(q)
        m_ip, m_iq = rip*rip/math.sqrt(bi.p), riq*riq/math.sqrt(bi.p)
        m_jp, m_jq = rjp*rjp/math.sqrt(bj.p), rjq*rjq/math.sqrt(bj.p)
        g = max(abs(max(m_ip, m_iq) - min(m_jp, m_jq)),
                abs(max(m_jp, m_jq) - min(m_ip, m_iq)))
        margin_h = max(margin_h, g*(q-p))
    win0 = (-max(hvals) - c - margin_h, -min(hvals) + c + margin_h)
    win, _ = alias_complete(win0, bi, bj, _caps(bi, bj, th, dm, dp))  # hole 2 fixed
    return win, evals, "ok"

# ---------------- certified truth: hierarchical scan + Lipschitz confirm ----------------

def _states_vec6(b, m):
    """positions only, 6 Newton iterations (truth grids; error << the rho-scale margins)"""
    m = np.asarray(m) % TAU
    e = b.e
    ea = m + e*np.sin(m)*(1.0 + e*np.cos(m))
    for _ in range(6):
        d = (ea - e*np.sin(ea) - m) / (1.0 - e*np.cos(ea))
        ea = ea - d
    se, ce = np.sin(ea), np.cos(ea)
    xp = b.a*(ce - e); yp = b.a*b.sq*se
    return np.stack([xp*b.cp - yp*b.sp, xp*b.sp + yp*b.cp])

def truth_v2(bi, bj, th, dj, cap, rho):
    """All s with D(s) < rho on (-cap0, cap1), certified hierarchically: at depth d,
    grid h_d = h0/8^d, tau grid 2048*4^d capped at 32768; D >= thr_d certifies
    no fire within h_d/2 (dist is Lipschitz Sigma in both s and tau). Fire-free
    violations are refined; windows containing a detected fire are certified only to
    2*h_d around it (disclosed). Certification floor: every unresolved window has
D_grid >= rho at cap resolution, hence D_true >= rho - Sigma*t_cap/2 there; a fire
with D_min <= rho - Sigma*t_cap/2 has width >= 2*(that slack)/Sigma > 2*h_max and is
detected. So: every fire deeper than ~4.5% is found; nothing else outside unresolved
windows. Returns (fires, unresolved)."""
    mi, mj = bi.mean_at_longitude(th), bj.mean_at_longitude(th)
    lo, hi = -dj[0], dj[1]
    Sig = (bi.vmax() + bj.vmax()) * 1.001
    a_dom, b_dom = -cap[0], cap[1]
    h0 = 16*rho/Sig
    grid = {}
    def grids(nt):
        if nt not in grid:
            t = np.linspace(lo, hi, max(nt, 2))
            grid[nt] = (t, _states_vec6(bj, mj + bj.n*t))
        return grid[nt]
    fires, unresolved = [], 0
    def D_of(svs, t, Sjj):
        out = np.empty(len(svs))
        for k in range(0, len(svs), 64):
            sv = svs[k:k+64]
            M = mi + bi.n*(t[None, :] - sv[:, None])
            Si = _states_vec6(bi, M.ravel()).reshape(2, len(sv), len(t))
            d = np.hypot(Si[0]-Sjj[0][None, :], Si[1]-Sjj[1][None, :])
            out[k:k+64] = d.min(axis=1)
        return out
    def scan(lo_s, hi_s, depth):
        nonlocal unresolved
        t, Sjj = grids(min(2048 * 4**depth, 32768))
        tstep = t[1]-t[0]
        hstep = h0 / 8**depth
        thr = rho + Sig*(hstep/2 + tstep/2)
        sv = np.arange(lo_s, hi_s, hstep)
        if len(sv) == 0: return
        dv = D_of(sv, t, Sjj)
        isfire = dv < rho
        fires.extend(sv[isfire].tolist())
        idx = np.where((dv < thr) & ~isfire)[0]   # refine only fire-free violations
        if len(idx) == 0: return
        splits = np.where(np.diff(idx) > 1)[0]
        for g0, g1 in zip(np.r_[0, splits+1], np.r_[splits, len(idx)-1]):
            wlo = sv[idx[g0]] - 2*hstep; whi = sv[idx[g1]] + 2*hstep
            if depth >= MAX_DEPTH:
                unresolved += 1; continue
            scan(max(lo_s, wlo), min(hi_s, whi), depth+1)
    scan(a_dom, b_dom, 0)
    return np.unique(np.round(fires, 10)), unresolved

# ---------------- F5: wide-crossing family ----------------

def make_pair_f5():
    """Crossing arcs with max(dm,dp) >= 0.2: Binet offset with |dU| < R - eps and
    R >~ 2 eps (the perpendicular offset clearly exceeds eps while the U offset stays
    inside). Accept-reject on the actual classifier."""
    for _ in range(400):
        a0 = rng2.uniform(1.5, 3.0)
        e = min(float(rng2.rayleigh(0.12)), 0.95)
        bj = Body.from_elements(a0, e, rng2.uniform(0, TAU), rng2.uniform(0, TAU))
        jb = np.array(bj.binet()); eps = eps_u(bj, bj, RHO)
        u = rng2.normal(size=3); u /= np.linalg.norm(u)
        up = math.hypot(u[1], u[2])
        if up < 0.2: continue
        R = rng2.uniform(1.6, 3.2) * eps
        mag = R / up
        dU = rng2.uniform(-0.85, 0.85) * R
        tgt = jb + np.array([dU, mag*u[1], mag*u[2]])
        if tgt[0] <= 0: continue
        bi = T.body_from_binet(tuple(tgt), rng2.uniform(0, TAU))
        if bi is None: continue
        arcs = classify_arcs(bi, bj, RHO)
        if not isinstance(arcs, list) or len(arcs) == 0: continue
        if not any(cross and max(dm, dp) >= 0.2 for (_, dm, dp, cross) in arcs): continue
        return bi, bj, arcs
    return None, None, None

# ---------------- census: which arc kinds arise among engineered tangencies ----------------

def census(n_try=500):
    tal = dict(tries=n_try, sections=0, wide_merged=0, wide_cross=0, cross_narrow=0,
               full=0, none=0, wide_emax=[], wide_cross_emax=[])
    for _ in range(n_try):
        a0 = rng2.uniform(1.5, 3.0)
        e = min(float(rng2.rayleigh(0.12)), 0.95)
        bj = Body.from_elements(a0, e, rng2.uniform(0, TAU), rng2.uniform(0, TAU))
        jb = np.array(bj.binet()); eps = eps_u(bj, bj, RHO)
        u = rng2.normal(size=3); u /= np.linalg.norm(u)
        mag = rng2.uniform(0.3, 3.0) * eps
        R = mag * math.hypot(u[1], u[2])
        dU = rng2.uniform(-1.2, 1.2) * R
        tgt = jb + np.array([dU, mag*u[1], mag*u[2]])
        if tgt[0] <= 0: tal["none"] += 1; continue
        bi = T.body_from_binet(tuple(tgt), rng2.uniform(0, TAU))
        if bi is None: tal["none"] += 1; continue
        arcs = classify_arcs(bi, bj, RHO)
        if arcs == "full": tal["full"] += 1; continue
        if not isinstance(arcs, list) or len(arcs) == 0: tal["none"] += 1; continue
        emax = max(bi.e, bj.e)
        for (_, dm, dp, cross) in arcs:
            tal["sections"] += 1
            wide = (not cross) or max(dm, dp) >= 0.2
            if wide and not cross:
                tal["wide_merged"] += 1; tal["wide_emax"].append(emax)
            elif wide:
                tal["wide_cross"] += 1; tal["wide_cross_emax"].append(emax)
            else:
                tal["cross_narrow"] += 1
    for k in ("wide_emax", "wide_cross_emax"):
        v = tal.pop(k)
        tal[k + "_med"] = float(np.median(v)) if v else None
        tal[k + "_hi"] = int(sum(1 for x in v if x > 0.6))
    return tal

# ---------------- wall clock ----------------

def microbench(reps=200000):
    ms = rng2.uniform(0, TAU, reps)
    ths = rng2.uniform(0, TAU, reps)
    es = [0.05, 0.12, 0.3, 0.6, 0.9]
    bodies = [Body.from_elements(2.0, e, 0.3, 0.0) for e in es]
    t0 = time.perf_counter()
    for k in range(reps): bodies[k % 5].state_at_mean(ms[k])
    t_state = (time.perf_counter()-t0)/reps
    t0 = time.perf_counter()
    for k in range(reps): bodies[k % 5].mean_at_longitude(ths[k])
    t_mean = (time.perf_counter()-t0)/reps
    return dict(state_at_mean_s=t_state, mean_at_long_s=t_mean,
                per_call_ratio=t_state/t_mean)

# ---------------- main ----------------

FAMS = ["F3x", "F5", "F1", "F2", "F4"]
NP = {"F3x": 8, "F5": 10, "F1": 10, "F2": 8, "F4": 4}

def run_section(bi, bj, th, dm, dp, cross):
    evalsA = [0]; evalsB = [0]; evalsB3 = [0]
    winA, cap, (di, dj) = cert_A_wide(bi, bj, th, dm, dp, RHO, evalsA)
    winB, _, flagB = cert_B_s(bi, bj, th, dm, dp, RHO, evalsB)
    winB3, _, flagB3 = cert_B3(bi, bj, th, dm, dp, RHO, evalsB3)
    fires, unresolved = truth_v2(bi, bj, th, dj, cap, RHO)
    missA = missB = missB3 = 0
    for s in fires:
        if isinstance(winA, tuple) and winA[0] != "cap":
            if not (winA[0] - 1e-9 <= s <= winA[1] + 1e-9): missA += 1
        if winB is not None and not (winB[0] - 1e-9 <= s <= winB[1] + 1e-9): missB += 1
        if winB3 is not None and not (winB3[0] - 1e-9 <= s <= winB3[1] + 1e-9): missB3 += 1
    bad_route = int(flagB3 != "ok" and len(fires) > 0)
    w = lambda v: (v[1]-v[0]) if v is not None else float("nan")
    wA = w(winA) if (isinstance(winA, tuple) and winA[0] != "cap") else float("nan")
    def timed(fn):
        best = float("inf")
        for _ in range(2):
            e2 = [0]; t0 = time.perf_counter(); fn(bi, bj, th, dm, dp, RHO, e2)
            best = min(best, time.perf_counter()-t0)
        return best
    tA = timed(cert_A_wide)
    tB3 = timed(cert_B3)
    return dict(e_i=round(bi.e,3), e_j=round(bj.e,3), dm=round(dm,3), dp=round(dp,3),
                cross=bool(cross), evalsA=evalsA[0], evalsB=evalsB[0], evalsB3=evalsB3[0],
                winA=("none" if winA is None else ("cap" if winA[0]=="cap" else "w")),
                wA=wA, wB=w(winB), wB3=w(winB3), flagB=flagB, flagB3=flagB3,
                nfire=int(len(fires)), missA=missA, missB=missB, missB3=missB3,
                bad_route=bad_route, unresolved=unresolved, tA=tA, tB3=tB3)

def main():
    t_start = time.perf_counter()
    out = dict(microbench=microbench(), census=census())
    results = {f: [] for f in FAMS}
    for fam in FAMS:
        k = 0; tries = 0
        while k < NP[fam] and tries < NP[fam]*8 and time.perf_counter() - t_start < 520:
            tries += 1
            if fam == "F5":
                bi, bj, arcs = make_pair_f5()
            else:
                bi, bj, arcs = make_pair(fam)
            if bi is None: continue
            for (c, dm, dp, cross) in arcs:
                th = c % TAU
                wide = (not cross) or max(dm, dp) >= 0.2
                if not wide: continue
                row = run_section(bi, bj, th, dm, dp, cross)
                row["fam"] = fam
                results[fam].append(row)
                wr = (row['wB3']/row['wA']) if (row['wA']==row['wA'] and row['wB3']==row['wB3']) else float('nan')
                print(f"[{fam} {k}] e=({row['e_i']},{row['e_j']}) cross={row['cross']} "
                      f"evalsA={row['evalsA']} evalsB3={row['evalsB3']} flag={row['flagB3']} "
                      f"fire={row['nfire']} missA={row['missA']} missB3={row['missB3']} "
                      f"unres={row['unresolved']} wB3/wA={wr:.2f} "
                      f"wallx={row['tA']/max(row['tB3'],1e-12):.1f}", flush=True)
                k += 1
                if k >= NP[fam]: break
    summ = {}
    for f in FAMS:
        rs = results[f]
        if not rs: summ[f] = "none"; continue
        ea = [r["evalsA"] for r in rs]; eb = [r["evalsB"] for r in rs]; eb3 = [r["evalsB3"] for r in rs]
        valid = [r for r in rs if r["winA"] == "w" and r["wA"] == r["wA"] and r["wB3"] == r["wB3"]]
        wB3r = [r["wB3"]/r["wA"] for r in valid]
        ratios = [(r["evalsA"]/max(r["evalsB3"], 1)) for r in valid]
        wallr = [(r["tA"]/max(r["tB3"], 1e-12)) for r in valid]
        summ[f] = dict(
            n_sections=len(rs),
            fire_total=sum(r["nfire"] for r in rs),
            missA=sum(r["missA"] for r in rs), missB=sum(r["missB"] for r in rs),
            missB3=sum(r["missB3"] for r in rs), bad_route=sum(r["bad_route"] for r in rs),
            unresolved=sum(r["unresolved"] for r in rs),
            routed_noradial=sum(1 for r in rs if r["flagB3"] == "route:noradial"),
            routed_other=sum(1 for r in rs if r["flagB3"] not in ("ok", "route:noradial")),
            evalsA_med=float(np.median(ea)), evalsA_p90=float(np.percentile(ea, 90)),
            evalsB_med=float(np.median(eb)), evalsB3_med=float(np.median(eb3)),
            evalsB3_max=int(max(eb3)),
            ratio_med=float(np.median(ratios)) if ratios else None,
            widthB3_ratio_med=float(np.median(wB3r)) if wB3r else None,
            widthB3_ratio_p90=float(np.percentile(wB3r, 90)) if wB3r else None,
            widthB3_ratio_max=float(max(wB3r)) if wB3r else None,
            wall_ratio_med=float(np.median(wallr)) if wallr else None,
            wall_ratio_min=float(min(wallr)) if wallr else None)
    out["summary"] = summ
    out["detail"] = {f: results[f][:8] for f in FAMS}
    with open(__file__.replace(".py", "-out.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(dict(microbench=out["microbench"], census=out["census"],
                          summary=summ), indent=1))
    print(f"wall total {time.perf_counter()-t_start:.1f}s")

if __name__ == "__main__":
    main()
