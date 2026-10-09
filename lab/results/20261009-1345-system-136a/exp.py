#!/usr/bin/env python3
"""Run 20261009-1345-system-136a (system lens): is the cycle-memo key space the encounter
candidate index?

  A. The bucket tier (dyadic buckets of the memo key's own quantization: relative width 2^-11 in
     periapsis r_p and in k = 1/(1+e)) with a conservative Binet envelope contains 100% of the
     exact cone candidates (crates/encounters/src/pairs.rs is_candidate), at a bounded superset.
  B. Under belt secular drift, per-pair section caches keyed by (bucket_i, bucket_j, Dw-band)
     invalidate at a rate compared against kick cadence: the amortization of r8 v3's open
     per-element-change setup cost.

Floats explore; every reported outcome is a count or ratio of counts on fixed seeds.
Reproduce: python3 exp.py            (numpy only; ~10 s, <500 MB)
"""
import json
import numpy as np

TAU = 2.0 * np.pi
RHO = 1e-4                 # encounter radius, belt units (a ~ 1)
W = np.log1p(2.0**-11)     # bucket relative width in ln(r_p) and ln(k); memo uses 11-12 bits
PAD = 1e-12                # conservative envelope pad (last-ulp log/exp roundoff)
OUT = {}

# ---------------------------------------------------------------- elements ---
def make_belt(n, a_lo=0.9, a_hi=1.1, sig_e=0.1, keys=0, seed=1):
    r = np.random.default_rng(seed)
    a = r.uniform(a_lo, a_hi, n) if keys <= 1 else a_lo + (a_hi-a_lo)*(r.integers(0, keys, n))/(keys-1)
    e = np.minimum(sig_e*np.sqrt(-2.0*np.log1p(-r.random(n))), 0.5)
    pom = TAU*r.random(n)
    return a, e, pom

def make_formation(n=512):
    return np.full(n, 1.0), np.full(n, 0.05), np.full(n, 0.3)

def binet(a, e, pom):
    p = a*(1.0-e*e)
    return 1.0/p, e*np.cos(pom)/p, e*np.sin(pom)/p

def eps_u(a1, e1, a2, e2, rho=RHO):
    """pairs.rs eps_u, vectorized."""
    rmin = np.minimum(a1*(1-e1), a2*(1-e2))
    rmax = np.maximum(a1*(1+e1), a2*(1+e2))
    emax = np.maximum(e1, e2)
    pmin = np.minimum(a1*(1-e1**2), a2*(1-e2**2))
    kappa = rmax*rmax*emax/(pmin*rmin)
    return 1.5*rho*(1.0+kappa)/(rmin*rmin)

def bucket_ids(a, e):
    return np.floor(np.log(a*(1.0-e))/W).astype(np.int64), np.floor(np.log(1.0/(1.0+e))/W).astype(np.int64)


# ------------------------------------------------------- bucket tier (A) -----
def exact_candidates(a, e, pom, chunk=256):
    """All pairs with cone_gap < eps_u (the crate's candidate predicate), as (i, j) arrays."""
    U, V, Wv = binet(a, e, pom)
    n = len(a)
    ii, jj = [], []
    for lo in range(0, n, chunk):
        hi = min(lo+chunk, n)
        I, J = np.meshgrid(np.arange(lo, hi), np.arange(lo, n), indexing="ij")
        dU = np.abs(U[I]-U[J]); R = np.hypot(V[I]-V[J], Wv[I]-Wv[J])
        ok = (dU - R) < eps_u(a[I], e[I], a[J], e[J])
        ok &= J > I                                  # unordered pairs once, incl same chunk
        m = np.nonzero(ok)
        ii.append(I[m]); jj.append(J[m])
    return np.concatenate(ii), np.concatenate(jj)

def bucket_tier(a, e, pom):
    """Conservative bucket-envelope tier. A bucket pair is allowed iff the worst case over the
    two bucket boxes (U-interval gap vs R1max+R2max at Dpom = pi, with the bucket-wide eps_u
    bound) can still satisfy the cone predicate."""
    n = len(a)
    b_rp, b_k = bucket_ids(a, e)
    U, V, Wv = binet(a, e, pom)
    R = np.hypot(V, Wv)
    bid = {}
    for i in range(n):
        bid.setdefault((int(b_rp[i]), int(b_k[i])), []).append(i)
    keys = sorted(bid)
    nb = len(keys)
    bidx = np.empty(n, dtype=np.int64)
    for x, key in enumerate(keys):
        bidx[np.array(bid[key])] = x

    env = {}
    for key in keys:
        rp0, k0 = key
        rp = np.exp((rp0+np.linspace(0, 1, 9))*W)
        kk = np.exp((k0+np.linspace(0, 1, 9))*W)
        RP, KK = np.meshgrid(rp, kk)
        EE = 1.0/KK - 1.0
        uu = 1.0/(RP*(1.0+EE))       # U = 1/p = 1/(rp(1+e))
        rr = EE*uu                   # R = e/p
        e_hi = 1.0/np.exp(k0*W) - 1.0
        e_lo = 1.0/np.exp((k0+1)*W) - 1.0
        rp_a, rp_b = np.exp(rp0*W), np.exp((rp0+1)*W)
        a_lo, a_hi = rp_a/(1.0-e_hi), rp_b/(1.0-e_lo)
        env[key] = dict(u0=float(uu.min())*(1-PAD), u1=float(uu.max())*(1+PAD),
                        r1=float(rr.max())*(1+PAD),
                        rmin=float(a_lo*(1-e_hi)), rmax=float(a_hi*(1+e_hi)),
                        emax=float(e_hi), pmin=float(a_lo*(1-e_hi**2)))

    # instrument check: the sampled envelope covers every actual member (with pad)
    env_ok = all(U[np.array(bid[k])].min() >= env[k]["u0"] and U[np.array(bid[k])].max() <= env[k]["u1"]
                 and R[np.array(bid[k])].max() <= env[k]["r1"] for k in keys)

    ua = np.array([env[k]["u0"] for k in keys]); ub = np.array([env[k]["u1"] for k in keys])
    rb = np.array([env[k]["r1"] for k in keys])
    rmn = np.array([env[k]["rmin"] for k in keys]); rmx = np.array([env[k]["rmax"] for k in keys])
    emx = np.array([env[k]["emax"] for k in keys]); pmn = np.array([env[k]["pmin"] for k in keys])
    cnt = np.array([len(bid[k]) for k in keys], dtype=np.int64)

    M = np.zeros((nb, nb), dtype=bool)
    tri = np.arange(nb)[None, :]
    CH = 256
    for lo in range(0, nb, CH):
        hi = min(lo+CH, nb)
        rows = np.arange(lo, hi)[:, None]
        rmin_w = np.minimum.outer(rmn[lo:hi], rmn)
        rmax_w = np.maximum.outer(rmx[lo:hi], rmx)
        emax_w = np.maximum.outer(emx[lo:hi], emx)
        pmin_w = np.minimum.outer(pmn[lo:hi], pmn)
        kap = rmax_w*rmax_w*emax_w/(pmin_w*rmin_w)
        eps_w = 1.5*RHO*(1.0+kap)/(rmin_w*rmin_w)
        ugap = np.maximum(0.0, np.maximum(ua[lo:hi, None]-ub[None, :], ua[None, :]-ub[lo:hi, None]))
        ok = (ugap - (rb[lo:hi, None]+rb[None, :])) < eps_w
        ok &= rows <= tri                              # upper triangle incl diagonal
        M[lo:hi] = ok
    npairs_bp = int(np.count_nonzero(M))               # bucket pairs, once each
    M |= M.T                                           # symmetrize for pair lookups
    # unordered tier-2 body pairs: (b^T M b - sum of diag-allowed bucket counts) / 2
    tier2_count = int((int(cnt @ M @ cnt) - int(cnt[np.diag(M)].sum())) // 2)
    return M, bidx, tier2_count, npairs_bp, env_ok, nb

def part_a(name, a, e, pom):
    ei, ej = exact_candidates(a, e, pom)
    M, bidx, tier2_count, npairs_bp, env_ok, nb = bucket_tier(a, e, pom)
    misses = int(np.count_nonzero(~M[bidx[ei], bidx[ej]]))
    cands = np.zeros(len(a), int)
    np.add.at(cands, ei, 1); np.add.at(cands, ej, 1)
    row = dict(n=int(len(a)), exact_pairs=int(len(ei)), tier2_pairs=tier2_count,
               misses=misses, superset=round(tier2_count/max(1, len(ei)), 2),
               cands_per_body_med=float(np.median(cands)),
               occupied_buckets=int(nb), bodies_per_bucket=round(len(a)/nb, 2),
               bucket_pairs=npairs_bp, envelope_covers_members=bool(env_ok))
    OUT.setdefault("A", {})[name] = row
    print(f"[A] {name:10s} n={row['n']:5d} exact={row['exact_pairs']:8d} tier2={row['tier2_pairs']:8d} "
          f"misses={row['misses']} superset=x{row['superset']} cand/body~{row['cands_per_body_med']:.0f} "
          f"buckets={row['occupied_buckets']} ({row['bodies_per_bucket']}/bkt) bpairs={row['bucket_pairs']} "
          f"env_ok={row['envelope_covers_members']}")
    return ei, ej

def corners_workload():
    """Adversarial: pairs at bucket corners with cone_gap - eps_u straddling the boundary."""
    A, E, POM = [], [], []
    r = np.random.default_rng(99)
    for _ in range(300):
        e1 = r.uniform(0.02, 0.4)
        rp1 = r.uniform(0.8, 1.2)
        k2c = (np.floor(np.log(1.0/(1.0+e1))/W)+1.0)*W       # low edge of the adjacent k-bucket
        e2s = np.linspace(1.0/np.exp(k2c+W)-1.0, 1.0/np.exp(k2c)-1.0, 400)
        rp2s = np.full_like(e2s, np.exp((np.floor(np.log(rp1)/W)+1)*W))  # adjacent rp-bucket edge
        pom1, dpom = TAU*r.random(), np.pi*r.random()
        a1s, a2s = np.full_like(e2s, rp1/(1-e1)), rp2s/(1.0-e2s)
        U1 = np.array(binet(rp1/(1-e1), e1, pom1))[:, None]
        U2 = np.array(binet(a2s, e2s, pom1+dpom))
        gaps = np.abs(U1[0]-U2[0]) - np.hypot(U1[1]-U2[1], U1[2]-U2[2])
        d = gaps - eps_u(a1s, np.full_like(e2s, e1), a2s, e2s)
        k = int(np.argmin(np.abs(d)))                        # nearest the candidate boundary
        for kk in (k-1, k, k+1):
            if 0 <= kk < len(e2s):
                A.append(float(a1s[kk])); E.append(e1); POM.append(pom1)
                A.append(float(a2s[kk])); E.append(float(e2s[kk])); POM.append(pom1+dpom)
    return np.array(A), np.array(E), np.array(POM)

# ------------------------------------------------------- drift study (B) -----
def part_b(a, e, pom, exact):
    """Secular drift of a Jupiter analog (mu=1e-3, circular, a_j=2.08) over the belt."""
    MU, AJ = 1e-3, 2.08
    al = np.clip(a/AJ, 0, 0.99)
    b1 = 3*al*(1+al**2)                       # b_{3/2}^{(1)} leading terms (alpha ~ 0.5)
    n = a**-1.5
    A = 0.75*n*MU*al*b1                       # apsidal rate, rad per time unit
    dpre = A*TAU/n                            # absolute rad per orbit
    e_f = 1.25*MU*al*b1                       # forced e (order), per body

    ii, jj = exact
    dw = np.abs(A[ii]-A[jj])*TAU/((n[ii]+n[jj])/2.0)          # differential rad per orbit
    res_band = {str(b): float(np.median(b/np.maximum(dw, 1e-18))) for b in (2.4e-4, 1.5e-2)}

    # radial residence: e_vec(t) = e0 e^{iAt} + e_f vec, a fixed (secular); count grid transitions
    T, dt = 2000.0, 0.25
    tvec = np.arange(int(T/dt))*dt
    phi0 = np.arctan2(np.sin(pom), np.cos(pom))
    evec = e[:, None]*np.exp(1j*(phi0[:, None]+A[:, None]*tvec[None, :])) + e_f[:, None]
    et = np.abs(evec)
    at = a[:, None]*np.ones_like(et)
    tk = int(np.count_nonzero(np.diff(np.floor(np.log(1.0/(1.0+et))/W), axis=1) != 0))
    tr = int(np.count_nonzero(np.diff(np.floor(np.log(at*(1.0-et))/W), axis=1) != 0))
    radial_res = float(len(a)*T/max(min(tk, tr), 1))

    OUT["B"] = dict(abs_precess_rad_per_orbit_med=float(np.median(dpre)),
                    diff_precess_rad_per_orbit_med=float(np.median(dw)),
                    diff_over_abs=float(np.median(dw)/np.median(dpre)),
                    band_residence_orbits={k: round(v, 1) for k, v in res_band.items()},
                    radial_residence_orbits=round(radial_res, 1),
                    forced_e_med=float(np.median(e_f)))
    b = OUT["B"]
    for band_tag, cadence, tag in (("0.00024", 0.3, "avg"), ("0.00024", 32.0, "unavg"),
                                   ("0.015", 0.3, "avg"), ("0.015", 32.0, "unavg")):
        inv = max(1.0/res_band[band_tag], 1.0/radial_res)
        b[f"savings_{tag}_{band_tag}"] = round(cadence/inv)
    print(f"[B] |dw|/orbit={b['abs_precess_rad_per_orbit_med']:.2e} d(dw)/orbit={b['diff_precess_rad_per_orbit_med']:.2e} "
          f"({b['diff_over_abs']:.1%}) band(2.4e-4) res={b['band_residence_orbits']['0.00024']:.0f} orb "
          f"band(1.5e-2) res={b['band_residence_orbits']['0.015']:.0f} orb "
          f"radial res={b['radial_residence_orbits']:.0f} orb")
    print(f"[B] savings: avg x{b['savings_avg_0.00024']} / x{b['savings_avg_0.015']}; "
          f"unavg x{b['savings_unavg_0.00024']} / x{b['savings_unavg_0.015']}")

def part_b_resonant():
    """r4 v3 2:1 pump scale: de/orbit = 5e-5."""
    de = 5e-5
    res = float(np.log1p(2.0**-11)/de)
    OUT["B_resonant"] = dict(de_per_orbit=de, k_residence_orbits=round(res, 1),
                             savings_avg=round(0.3*res), savings_unavg=round(32.0*res))
    print(f"[B-res] de/orbit={de:.0e} -> k residence={res:.0f} orbits; savings "
          f"x{OUT['B_resonant']['savings_avg']} (avg) x{OUT['B_resonant']['savings_unavg']} (unavg)")

if __name__ == "__main__":
    for name, gen in [("belt", lambda: make_belt(4096, seed=1)),
                      ("belt64", lambda: make_belt(4096, keys=64, seed=2)),
                      ("formation", make_formation),
                      ("corners", corners_workload)]:
        a, e, pom = gen()
        exact = part_a(name, a, e, pom)
        if name == "belt":
            part_b(a, e, pom, exact)
    part_b_resonant()
    with open("metrics.json", "w") as f:
        json.dump(OUT, f, indent=1)
    print("wrote metrics.json")
