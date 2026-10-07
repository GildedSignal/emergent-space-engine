#!/usr/bin/env python3
"""Second-author run on 20261007-0528-fermi-aab3: pin the impulse accounting on the real
population by integrating the exact restricted three-body problem (Sun + perturber on a
circular orbit + massless belt-0 rock), then recompute the 8 GB gate with an explicit
perturber-mass bound instead of a free f_emb.

Units: G = M_star = 1, AU, time such that a=1 orbit = 2*pi. v_K(a=1) = 1.
Belt-0 geometry (crates/encounters/src/belt.rs): a ~ U[1, 1.5], e ~ Rayleigh(sigma_e) capped
0.5, random periapsis and phase, coplanar. sigma_e = 0.01 (the author's assumption; the r8
rung draws it log-uniform — handled in r8check.py).

Stages (each cached to enc3-out.json):
  1. integrate: per-conjunction net element kick vs measured closest approach b, for
     perturber mass 1e22 / 1e24 / 1e26 kg, plus mu=0 numerical controls.
  2. kick law: median kick(b) vs b, against the author's 2*mu/b (v = v_K), the checker's
     2*mu/(0.0175 b), the shear law (4/3) mu / b^2, and the local impulse 2*mu/(b*v_rel).
  3. rates: per-body per-orbit conjunction rate R(b) at belt-0 local density, extended to
     b = 0.3 AU (the author's curve sampled only rho <= 1e-3).
  4. gate: creation rate and tube materialization vs total perturber mass M_pert (the f_emb
     x mu degeneracy removed), vs the tube-filling floor.
"""
import json
import numpy as np
from scipy.integrate import solve_ivp

RNG = np.random.default_rng(20261007)
MSUN = 1.989e30
YR_S = 3.156e7
Q_QUANTUM = 1e-6          # program element quantum (relative), the author's 1-bit threshold
TUBE_BYTES = 16
N_BELT0 = 10_000          # belt-0 local density: N bodies in a in [1, 1.5]
OUT = {}

# ---------------------------------------------------------------- Kepler machinery
def kepler_E(M, e):
    E = M.copy()
    for _ in range(60):
        f = E - e * np.sin(E) - M
        fp = 1 - e * np.cos(E)
        d = f / fp
        E = E - np.clip(d, -0.7, 0.7)
        if np.max(np.abs(d)) < 1e-14:
            break
    return E

def elements_to_state(a, e, w, M0, t):
    """Heliocentric 2D state at time t from osculating elements (GM=1)."""
    n = a ** -1.5
    M = M0 + n * t
    E = kepler_E(np.mod(M, 2 * np.pi), e)
    cE, sE = np.cos(E), np.sin(E)
    r = a * (1 - e * cE)
    xf = a * (cE - e); yf = a * np.sqrt(1 - e * e) * sE
    nf = n / (1 - e * cE)
    vxf = -a * nf * sE; vyf = a * nf * np.sqrt(1 - e * e) * cE
    cw, sw = np.cos(w), np.sin(w)
    return np.stack([xf * cw - yf * sw, xf * sw + yf * cw,
                     vxf * cw - vyf * sw, vxf * sw + vyf * cw])

def state_to_elements(x, y, vx, vy):
    r = np.hypot(x, y); v2 = vx * vx + vy * vy
    a = 1.0 / (2.0 / r - v2)
    h = x * vy - y * vx
    evec = ((v2 - 1.0 / r) * np.array([x, y]) - (x * vx + y * vy) * np.array([vx, vy]))
    e = np.hypot(*evec)
    return a, e

def perturber_state(a_p, lam_p0, t):
    n_p = a_p ** -1.5
    th = lam_p0 + n_p * t
    return np.array([a_p * np.cos(th), a_p * np.sin(th)]), \
           np.array([-n_p * a_p * np.sin(th), n_p * a_p * np.cos(th)])

# ---------------------------------------------------------------- one encounter
def first_conjunction(a, e, w, M0, a_p, lam_p0):
    """Time of first lambda-conjunction and the synodic rate."""
    n = a ** -1.5; n_p = a_p ** -1.5
    dn = n - n_p
    if abs(dn) < 1e-4:
        return None, None
    T_syn = 2 * np.pi / abs(dn)
    ts = np.linspace(0.0, T_syn, 721)
    def g(t):
        st = elements_to_state(a, e, w, M0, t)
        rp, _ = perturber_state(a_p, lam_p0, t)
        lam_r = np.arctan2(st[1], st[0])
        lam_p = np.arctan2(rp[1], rp[0])
        return (lam_r - lam_p + np.pi) % (2 * np.pi) - np.pi
    gs = np.array([g(t) for t in ts])
    sgn = np.sign(gs)
    idx = np.nonzero(np.diff(sgn) != 0)[0]
    if idx.size == 0:
        return None, None
    for i in idx:                      # a wrapped-angle sign change is also hit at opposition
        lo, hi = ts[i], ts[i + 1]
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            if np.sign(g(mid)) == np.sign(g(lo)):
                lo = mid
            else:
                hi = mid
        t_c = 0.5 * (lo + hi)
        if abs(g(t_c)) < 0.2:          # true conjunction (wrapped angle through 0), not pi
            return t_c, T_syn
    return None, None

def one_encounter(args):
    (a, e, w, M0, a_p, lam_p0, mu) = args
    t_c, T_syn = first_conjunction(a, e, w, M0, a_p, lam_p0)
    if t_c is None:
        return None
    st0 = elements_to_state(a, e, w, M0, t_c)
    rp0, vp0 = perturber_state(a_p, lam_p0, t_c)
    b0 = np.hypot(st0[0] - rp0[0], st0[1] - rp0[1])
    vrel0 = np.hypot(st0[2] - vp0[0], st0[3] - vp0[1])
    W = min(T_syn / 4.0, max(6.0 * b0 / max(vrel0, 1e-9), 0.02))
    t0, t1 = t_c - W, t_c + W

    y0 = elements_to_state(a, e, w, M0, t0)
    def rhs(t, y):
        r = np.hypot(y[0], y[1])
        rp, _ = perturber_state(a_p, lam_p0, t)
        dx, dy = y[0] - rp[0], y[1] - rp[1]
        d = np.hypot(dx, dy)
        ax = -y[0] / r**3 - mu * (dx / d**3 + rp[0] / a_p**3)
        ay = -y[1] / r**3 - mu * (dy / d**3 + rp[1] / a_p**3)
        return [y[2], y[3], ax, ay]

    sol = solve_ivp(rhs, (t0, t1), y0, method="DOP853", rtol=1e-12, atol=1e-14,
                    dense_output=True)
    if not sol.success:
        return None
    ts = np.linspace(t0, t1, 2001)
    zz = sol.sol(ts)
    rp_ts = perturber_state(a_p, lam_p0, ts)[0]
    bmin = float(np.min(np.hypot(zz[0] - rp_ts[0], zz[1] - rp_ts[1])))
    i_bm = int(np.argmin(np.hypot(zz[0] - rp_ts[0], zz[1] - rp_ts[1])))
    vp_ts = perturber_state(a_p, lam_p0, ts)[1]
    vrel_bm = float(np.hypot(zz[2, i_bm] - vp_ts[0, i_bm], zz[3, i_bm] - vp_ts[1, i_bm]))
    yf = zz[:, -1]
    a1, e1 = state_to_elements(*yf)
    da_rel = abs(a1 - a) / a
    de = abs(e1 - e)
    dv_v = float(np.hypot(de, 0.5 * da_rel))       # velocity-equivalent kick
    return dict(b=bmin, vrel=vrel_bm, dv_v=dv_v, da_rel=float(da_rel), de=float(de),
                mu=mu, W=float(W))

# ---------------------------------------------------------------- stage 1+2: integrate
def draw_encounters(n, mu):
    """Belt-0 rock + circular perturber embedded in the belt."""
    out = []
    while len(out) < n:
        a = RNG.uniform(1.0, 1.5); e = min(0.01 * np.sqrt(-2 * np.log(1 - RNG.random())), 0.5)
        w = RNG.uniform(0, 2 * np.pi); M0 = RNG.uniform(0, 2 * np.pi)
        a_p = RNG.uniform(1.05, 1.45); lam_p0 = RNG.uniform(0, 2 * np.pi)
        out.append((a, e, w, M0, a_p, lam_p0, mu))
    return out

def integrate_all():
    import concurrent.futures as cf
    import os
    masses = {"1e22": 1e22, "1e24": 1e24, "1e26": 1e26}
    n_draws = {"1e22": 1100, "1e24": 1100, "1e26": 700}
    res = {}
    for name, m in masses.items():
        cache = f"enc3-raw-{name}.json"
        mu = m / MSUN
        if os.path.exists(cache):
            got = json.load(open(cache))
            ctl_max = json.load(open(cache.replace("raw", "ctl")))
        else:
            jobs = draw_encounters(n_draws[name], mu)
            with cf.ProcessPoolExecutor(max_workers=8) as ex:
                got = [r for r in ex.map(one_encounter, jobs, chunksize=4) if r is not None]
            # numerical control: same geometry, mu = 0
            with cf.ProcessPoolExecutor(max_workers=8) as ex:
                ctl = [r for r in ex.map(one_encounter,
                                         [(a, e, w, M0, a_p, l0, 0.0)
                                          for (a, e, w, M0, a_p, l0, _) in jobs[:80]],
                                         chunksize=4) if r is not None]
            ctl_max = float(max(r["dv_v"] for r in ctl))
            json.dump(got, open(cache, "w"))
            json.dump(ctl_max, open(cache.replace("raw", "ctl"), "w"))
        res[name] = dict(encounters=got, control_max_dv=ctl_max, mass_kg=m, mu=mu)
        print(f"  {name} kg: {len(got)} encounters, control drift {ctl_max:.2e}", flush=True)
    return res

def bin_kicks(res):
    """Median kick vs b, in log bins; compare against the candidate laws."""
    edges = np.logspace(-4, np.log10(0.25), 19)
    out = {}
    for name, d in res.items():
        mu = d["mu"]
        b = np.array([r["b"] for r in d["encounters"]])
        dv = np.array([r["dv_v"] for r in d["encounters"]])
        vr = np.array([r["vrel"] for r in d["encounters"]])
        rows = []
        for i in range(len(edges) - 1):
            m = (b >= edges[i]) & (b < edges[i + 1])
            if m.sum() >= 8:
                bm, dm, vm_ = np.median(b[m]), np.median(dv[m]), np.median(vr[m])
                rows.append(dict(
                    b=bm, n=int(m.sum()), dv_v=dm,
                    dv_author=2 * mu / bm,                    # author: v = v_K = 1
                    dv_checker=2 * mu / (0.0175 * bm),        # checker: v_rel = 0.0175
                    dv_shear=(4.0 / 3.0) * mu / bm**2,        # shear-dominated law
                    dv_localimp=2 * mu / (bm * vm_),          # impulse with true local v_rel
                ))
        out[name] = rows
    return out

# ---------------------------------------------------------------- stage 3: rate curve
def rate_curve():
    """Per-body per-orbit conjunction rate with closest approach < b, belt-0 local density
    (N = 1e4, a in [1,1.5], sigma_e = 0.01). Extended to b = 0.3 (author sampled <= 1e-3)."""
    n = 2_000_000
    a1 = RNG.uniform(1, 1.5, n); a2 = RNG.uniform(1, 1.5, n)
    e1 = np.minimum(0.01 * np.sqrt(-2 * np.log(1 - RNG.random(n))), 0.5)
    e2 = np.minimum(0.01 * np.sqrt(-2 * np.log(1 - RNG.random(n))), 0.5)
    w1 = RNG.uniform(0, 2 * np.pi, n); w2 = RNG.uniform(0, 2 * np.pi, n)
    th = RNG.uniform(0, 2 * np.pi, n)
    p1 = a1 * (1 - e1**2); p2 = a2 * (1 - e2**2)
    f1 = th - w1; f2 = th - w2
    c1 = 1 + e1 * np.cos(f1); c2 = 1 + e2 * np.cos(f2)
    r1 = p1 / c1; r2 = p2 / c2
    h1 = np.sqrt(p1); h2 = np.sqrt(p2)
    dvr = e1 * np.sin(f1) / h1 - e2 * np.sin(f2) / h2
    dvt = c1 / h1 - c2 / h2
    v = np.hypot(dvr, dvt)
    bmin = np.abs(r1 - r2) * np.abs(dvt) / np.maximum(v, 1e-30)
    dn = np.abs(a1**-1.5 - a2**-1.5)
    # per body per orbit: each partner contributes dn conjunctions per 2*pi time = dn per orbit
    grid = np.logspace(-6, np.log10(0.3), 25)
    rate = [float(np.mean(dn * (bmin < g)) * N_BELT0) for g in grid]
    return grid, rate

# ---------------------------------------------------------------- stage 4: gate
def b_crossing(rows, level):
    """b where median dv_v crosses `level`, log-interpolated."""
    bs = np.array([r["b"] for r in rows]); dvs = np.array([r["dv_v"] for r in rows])
    for i in range(len(dvs) - 1):
        if dvs[i] >= level > dvs[i + 1]:
            t = np.log(level / dvs[i]) / np.log(dvs[i + 1] / dvs[i])
            return float(np.exp(np.log(bs[i]) + t * (np.log(bs[i + 1]) - np.log(bs[i]))))
    return None

def gate(kicks, grid, rate):
    """Creation rate and materialization vs TOTAL perturber mass in the belt (M_pert in
    M_star units). Shear-regime scaling: R(b_bits) ~ b_bits^2 ~ mu, so C ~ mu * f_emb =
    M_pert / (M_star * N_rock): the split cancels. Verified numerically per mass."""
    T_orb_s = 2 * np.pi * 1.25**1.5 / (2 * np.pi) * YR_S      # a = 1.25 orbit in seconds
    def R_at(b):
        return float(10 ** np.interp(np.log10(b), np.log10(grid), np.log10(rate)))
    rows = {}
    floor_tubes = 0.375e9 / (3.6e7)   # tubes/s filling the 6 GB share over 3.6e7 game-s (rtf 100, 100 h) = 10.4/s
    for name, rl in kicks.items():
        mu = {"1e22": 1e22 / MSUN, "1e24": 1e24 / MSUN, "1e26": 1e26 / MSUN}[name]
        b_bits = b_crossing(rl, Q_QUANTUM)
        b_strong = b_crossing(rl, 1e-3)
        if b_bits is None:
            continue
        r_bits = R_at(b_bits); r_strong = R_at(b_strong) if b_strong else 0.0
        rows[name] = dict(
            b_bits_AU=b_bits, b_strong_AU=b_strong,
            r_H_AU=(mu / 3)**(1.0 / 3.0) * 1.25,
            rate_bits_per_orbit=r_bits, rate_strong_per_orbit=r_strong,
            # per-rock rate = R * f_emb, f_emb = M_pert/(mu*N_rock); total = R*M_pert/mu (N cancels)
            creation_bits_per_s_per_Mpert=r_bits * (1.0 / mu) * 2.0 / T_orb_s,
            materialize_per_s_per_Mpert=r_strong * (1.0 / mu) / T_orb_s,
        )
    # table at named M_pert points (M_sun units), using each mass row (split-independence test)
    table = {}
    for Mp_name, Mp in [("stated_1e25kg_5e-6Msun", 5.0e-6), ("heavy_disk_1e-4", 1e-4),
                        ("max_disk_1e-3", 1e-3), ("absurd_1e-2", 1e-2)]:
        table[Mp_name] = {k: {"creation_bits_s": v["creation_bits_per_s_per_Mpert"] * Mp,
                              "tubes_s": v["materialize_per_s_per_Mpert"] * Mp,
                              "tube_fill_game_years_at_0.375e9":
                                  0.375e9 / max(v["materialize_per_s_per_Mpert"] * Mp, 1e-30)
                                  / 3.156e7}
                          for k, v in rows.items()}
    return dict(T_orb_s=T_orb_s, floor_tubes_per_s=floor_tubes, per_mass=rows,
                vs_Mpert=table)

# ---------------------------------------------------------------- r8 honest check
def r8_check():
    """Frozen N = 1e4 (r8 v2 rung). (sigma_e, rho) log-uniform in the rung bands."""
    n = 1_000_000
    def model(sigma_e, rho, n_pairs=n):
        rng = np.random.default_rng(int(sigma_e * 1e6) + 7)
        a1 = rng.uniform(1, 1.5, n_pairs); a2 = rng.uniform(1, 1.5, n_pairs)
        e1 = np.minimum(sigma_e * np.sqrt(-2 * np.log(1 - rng.random(n_pairs))), 0.5)
        e2 = np.minimum(sigma_e * np.sqrt(-2 * np.log(1 - rng.random(n_pairs))), 0.5)
        w1 = rng.uniform(0, 2 * np.pi, n_pairs); w2 = rng.uniform(0, 2 * np.pi, n_pairs)
        cross = np.abs(a1 - a2) < (a1 * e1 + a2 * e2) + rho
        xfrac = cross.mean()
        cands = xfrac * 1e4 * 9999 / 2
        a1, e1, w1, a2, e2, w2 = a1[cross], e1[cross], w1[cross], a2[cross], e2[cross], w2[cross]
        th = rng.uniform(0, 2 * np.pi, a1.size)
        p1 = a1 * (1 - e1**2); p2 = a2 * (1 - e2**2)
        f1 = th - w1; f2 = th - w2
        c1 = 1 + e1 * np.cos(f1); c2 = 1 + e2 * np.cos(f2)
        h1 = np.sqrt(p1); h2 = np.sqrt(p2)
        dvr = e1 * np.sin(f1) / h1 - e2 * np.sin(f2) / h2
        dvt = c1 / h1 - c2 / h2
        v = np.hypot(dvr, dvt)
        bmin = np.abs(p1 / c1 - p2 / c2) * np.abs(dvt) / np.maximum(v, 1e-30)
        dn = np.abs(a1**-1.5 - a2**-1.5)
        enc20 = float(np.mean(dn * (bmin < rho)) * cands * 20 * 2 * np.pi / (2 * np.pi))
        return cands, enc20
    out = {}
    N, T20 = 10_000, 20.0
    for se in [1e-3, 3e-3, 1e-2, 3e-2]:
        for rho in [1e-5, 3e-5, 1e-4, 3e-4]:
            c, e = model(se, rho)
            out[f"se={se:g},rho={rho:g}"] = dict(
                candidates=c, factor_cands=c / 1.7e6,
                enc20=e, factor_enc=e / 427.0)
    return out

# ---------------------------------------------------------------- main
def main():
    res = integrate_all()
    OUT["integrations"] = {k: dict(mass_kg=v["mass_kg"], mu=v["mu"],
                                   control=v["control_max_dv"],
                                   n=len(v["encounters"])) for k, v in res.items()}
    kicks = bin_kicks(res)
    OUT["kick_law"] = kicks
    grid, rate = rate_curve()
    OUT["rate_curve"] = dict(b_grid=grid.tolist(), per_body_per_orbit=rate)
    OUT["gate"] = gate(kicks, grid, rate)
    OUT["r8_check_frozenN1e4"] = r8_check()
    with open("enc3-out.json", "w") as f:
        json.dump(OUT, f, indent=1)
    # raw encounters kept separately (size)
    with open("enc3-raw.json", "w") as f:
        json.dump({k: v["encounters"] for k, v in res.items()}, f)
    print("wrote enc3-out.json, enc3-raw.json")

if __name__ == "__main__":
    main()
