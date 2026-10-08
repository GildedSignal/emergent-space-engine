#!/usr/bin/env python3
"""News gravity: does cell-quantized arrival hold behaviour vs exact light cones?

Scene (law.md "Gravity travels at c" / the queued b-news-gravity build): a star
(mu=1), one planet (the changing source, mu_p=1e-3), a test receiver at
a=1.9, e=0.05 (16 phases). The planet's tube changes by impulsive dv events.
The receiver is pulled toward the source "as its past light cone last saw it"
(the seen tube extrapolated to now).

Laws (same integrator, same seeds; only the news model differs):
  instant : pull toward the true planet now (the plane today: no c at all)
  exact   : per-pair light cone: event e arrives when |x_r(t)-x_s(t_e)| <= c(t-t_e)
  cell    : arrival at t_e + lag(cell_s(t_e), cell_r(t_e)); lag = (sampled)
            min distance between the two lattice cells / c  (never early)
  laplace : control: pull toward the source's RETARDED POSITION (no tube) --
            must drift (Laplace). If it does not fail, the toy is void.

Cells: the doll's rings r0*2^(k/16), N=128 spokes (representation.md 1).
All source motion is analytic Kepler (universal variables; gdot = 1-chi^2 C/r,
fdot = (f*gdot-1)/g; energy exact to ~1e-14, RK4-verified). The receiver is
velocity-Verlet in the star's field + the source's pull.
"""
import numpy as np, json, sys, time

MU = 1.0
M_RING, N_SPOKE = 16, 128
R0 = 0.7  # doll inner edge (AU)
def _stumpff(z):
    """Branchless (vectorized): C(z), S(z) for z in [-50, 50]."""
    za = np.abs(z); rt = np.sqrt(za)
    with np.errstate(divide="ignore", invalid="ignore"):
        Cp = (1 - np.cos(rt)) / z
        Sp = (rt - np.sin(rt)) / z ** 1.5
        Cn = (np.cosh(rt) - 1) / (-z)
        Sn = (np.sinh(rt) - rt) / (-z) ** 1.5
    C = np.where(z >= 0, Cp, Cn); S = np.where(z >= 0, Sp, Sn)
    mid = za < 1e-8
    if mid.any():
        C[mid] = 0.5 - z[mid] / 24 + z[mid] ** 2 / 720
        S[mid] = 1 / 6 - z[mid] / 120 + z[mid] ** 2 / 5040
    return C, S

def kep_step(r, v, dt):
    """Advance (N,2) states by dt (scalar or per-row). Elliptic. Exact energy."""
    r0 = np.linalg.norm(r, axis=1); v2 = np.sum(v * v, axis=1)
    alpha = 2.0 / r0 - v2
    assert (alpha > 0).all(), "toy stays elliptic"
    P = 2 * np.pi / alpha ** 1.5
    dt_red = np.mod(dt, P)
    rv0 = np.sum(r * v, axis=1)
    sq = np.sqrt(MU); chi_hi = 2 * np.pi / np.sqrt(alpha)
    chi = (dt_red / P) * chi_hi
    A = rv0 / sq; B = 1 - alpha * r0
    for _ in range(8):
        z = alpha * chi ** 2; C, S = _stumpff(z)
        F = A * chi ** 2 * C + B * chi ** 3 * S + r0 * chi - sq * dt_red
        if np.max(np.abs(F / (1 + np.abs(dt_red) * sq))) < 1e-13: break
        dF = A * chi * (1 - z * S) + B * chi ** 2 * (1 - z * C) + r0
        chi = np.clip(chi - F / dF, 1e-12, chi_hi * (1 - 1e-12))
    z = alpha * chi ** 2; C, S = _stumpff(z)
    F = A * chi ** 2 * C + B * chi ** 3 * S + r0 * chi - sq * dt_red
    bad = np.abs(F) > 1e-11 * (1 + sq * np.abs(dt_red))
    if bad.any():
        idx = np.nonzero(bad)[0]
        lo = np.zeros(len(idx)); hi = np.full(len(idx), chi_hi[idx] * (1 - 1e-12))
        for _ in range(70):
            mid_ = 0.5 * (lo + hi); zm = alpha[idx] * mid_ ** 2
            Cm, Sm = _stumpff(zm)
            Fm = (A[idx] * mid_ ** 2 * Cm + B[idx] * mid_ ** 3 * Sm
                  + r0[idx] * mid_ - sq * dt_red[idx])
            m = Fm < 0; lo = np.where(m, mid_, lo); hi = np.where(m, hi, mid_)
        chi[idx] = 0.5 * (lo + hi)
        z = alpha * chi ** 2; C, S = _stumpff(z)
    f = 1 - chi ** 2 / r0 * C
    g = dt_red - chi ** 3 / sq * S
    rn = f[:, None] * r + g[:, None] * v
    r_nn = np.linalg.norm(rn, axis=1)
    gdot = 1 - chi ** 2 * C / r_nn
    fdot = (f * gdot - 1) / g
    vn = fdot[:, None] * r + gdot[:, None] * v
    return rn, vn

# ---------- lattice cells ----------
def cell_index(x):
    r = np.hypot(x[0], x[1]); th = np.arctan2(x[1], x[0]) % (2 * np.pi)
    return (int(np.floor(M_RING * np.log2(r / R0))),
            int(np.floor(th / (2 * np.pi / N_SPOKE))) % N_SPOKE)

def cell_corners(k, s):
    ra = R0 * 2 ** (k / M_RING); rb = R0 * 2 ** ((k + 1) / M_RING)
    t0 = s * 2 * np.pi / N_SPOKE; t1 = (s + 1) * 2 * np.pi / N_SPOKE
    th = np.linspace(t0, t1, 24)
    pts = [[ra * np.cos(t), ra * np.sin(t)] for t in th]
    pts += [[rb * np.cos(t), rb * np.sin(t)] for t in th]
    for rr in np.linspace(ra, rb, 8):
        pts += [[rr * np.cos(t0), rr * np.sin(t0)], [rr * np.cos(t1), rr * np.sin(t1)]]
    return np.array(pts)

_cellpts_cache = {}
def cell_lag_dist(c1, c2):
    """Max distance between two cells /c = causality-safe lag (never early).
    Sampled on boundaries (corners included): <= true max + O(r*1e-8)."""
    if c1 == c2: return 0.0
    p1 = _cellpts_cache.setdefault(c1, cell_corners(*c1))
    p2 = _cellpts_cache.setdefault(c2, cell_corners(*c2))
    return float(np.linalg.norm(p1[:, None, :] - p2[None, :, :], axis=2).max())

# ---------- the toy ----------
def osc_elems(x, v):
    r = np.linalg.norm(x, axis=1); v2 = np.sum(v * v, axis=1)
    a = -1.0 / (2 * (v2 / 2 - 1.0 / r))
    rv = np.sum(x * v, axis=1)
    return a, np.linalg.norm(((v2 - 1.0 / r)[:, None] * x - rv[:, None] * v), axis=1)

def run(law, c, events, seeds, a0=1.9, e0=0.05, dt=2e-3, t_end=16.0, mu_p=1e-3, rec_every=50):
    n = len(seeds)
    q = a0 * (1 - e0); vp = np.sqrt((1 + e0) / (a0 * (1 - e0)))
    ang = 2 * np.pi * seeds
    xr = np.stack([q * np.cos(ang), q * np.sin(ang)], 1)
    vr = np.stack([-vp * np.sin(ang), vp * np.cos(ang)], 1)
    # source truth replay: rows of `truth` are (t_e, r, v) AFTER each dv; row 0 is t=0
    truth = [(0.0, np.array([1.0, 0.0]), np.array([0.0, 1.0]))]
    ra, va, ta = np.array([1.0, 0.0]), np.array([0.0, 1.0]), 0.0
    for (t_e, dv) in events:
        ra2, va2 = kep_step(ra[None, :], va[None, :], t_e - ta)
        ra, va, ta = ra2[0], va2[0] + np.array(dv), t_e
        truth.append((t_e, ra.copy(), va.copy()))
    ne = len(events)
    # arrival times per seed/event. Receiver cell at t_e from its unperturbed
    # (star-only) Kepler: the lag needs only the occupied cell.
    pend_exact = np.full((n, ne), np.inf); pend_cell = np.full((n, ne), np.inf)
    xrU, vrU, tcur = xr.copy(), vr.copy(), 0.0
    for ei in range(ne):
        t_e, re_, ve_ = truth[ei + 1]
        xrU, vrU = kep_step(xrU, vrU, t_e - tcur); tcur = t_e
        for si in range(n):
            pend_exact[si, ei] = t_e + np.linalg.norm(xrU[si] - re_) / c
            lag = cell_lag_dist(cell_index(re_), cell_index(xrU[si])) / c
            pend_cell[si, ei] = t_e + lag
    pend_exact_0, pend_cell_0 = pend_exact.copy(), pend_cell.copy()
    tab = pend_exact if law == "exact" else (pend_cell if law == "cell" else None)
    # hot state: row 0 = true source, rows 1..n = per-seed ghosts (seen tubes)
    rs = np.vstack([truth[0][1]] + [truth[0][1]] * n)
    vs = np.vstack([truth[0][2]] + [truth[0][2]] * n)
    steps = int(round(t_end / dt))
    a_rec, e_rec, t_rec = [], [], []
    def accel(x, xg):
        d = xg - x; dn = np.linalg.norm(d, axis=1)
        return -x / np.linalg.norm(x, axis=1)[:, None] ** 3 + mu_p * d / dn[:, None] ** 3
    t = 0.0; acc = accel(xr, rs[1:])
    ei_true = 0
    for st in range(steps):
        t_new = t + dt
        rs, vs = kep_step(rs, vs, dt)
        while ei_true < ne and truth[ei_true + 1][0] <= t_new:
            ei_true += 1
            vs[0] = vs[0] + np.array(events[ei_true - 1][1])   # impulse lands within dt
        if law == "instant":
            rs[1:] = rs[0]
        if law in ("exact", "cell"):
            due = tab <= t_new
            for si in np.nonzero(due.any(1))[0]:
                eis = np.nonzero(due[si])[0]
                ei = eis[np.argmax([truth[j + 1][0] for j in eis])]
                t_e, re_, ve_ = truth[ei + 1]
                # seen tube := state right after event ei, propagated to t_new
                rs2, vs2 = kep_step(re_[None, :], ve_[None, :], t_new - t_e)
                rs[si + 1], vs[si + 1] = rs2[0], vs2[0]
                tab[si, : ei + 1] = np.inf
        # verlet on the receiver
        xr = xr + vr * dt + 0.5 * acc * dt * dt
        if law == "laplace":
            d = np.linalg.norm(xr - rs[0], axis=1)
            rret = rs[0]
            for _ in range(3):
                rret, _ = kep_step(np.vstack([rs[0]] * n), np.vstack([vs[0]] * n), -d / c)
                d = np.linalg.norm(xr - rret, axis=1)
            xg = rret
        else:
            xg = rs[1:]
        acc_new = accel(xr, xg)
        vr = vr + 0.5 * (acc + acc_new) * dt
        acc = acc_new; t = t_new
        if st % rec_every == 0:
            a_, e_ = osc_elems(xr, vr); a_rec.append(a_); e_rec.append(e_); t_rec.append(t)
    A = np.array(a_rec); E = np.array(e_rec)
    fin = np.isfinite(pend_exact_0)
    return dict(a=A.T, e=E.T, t=np.array(t_rec),
                pend_exact=pend_exact_0[fin], pend_cell=pend_cell_0[fin])

def fmt(x): return "0" if x == 0 else f"{x:.3e}"

def compare(R1, R2, label):
    da = np.abs(R1["a"] - R2["a"]) / R2["a"]; de = np.abs(R1["e"] - R2["e"])
    print(f"  {label}: max|da|/a={fmt(da.max())} med={fmt(np.median(da))}; "
          f"max|de|={fmt(de.max())} med={fmt(np.median(de))}")
    return dict(label=label, max_da=float(da.max()), med_da=float(np.median(da)),
                max_de=float(de.max()), med_de=float(np.median(de)))

def main(cfg="all"):
    seeds = np.linspace(0.017, 0.983, 16)
    out = {}
    t0 = time.time()
    jobs = []
    if cfg in ("all", "c30"): jobs.append(("impulsive_c30", 30.0, 12.0, [(5.0, (0.0, 0.03))]))
    if cfg in ("all", "c300"): jobs.append(("impulsive_c300", 300.0, 12.0, [(5.0, (0.0, 0.03))]))
    if cfg in ("all", "per"):
        ev, sgn, te = [], 1, 5.0
        while te < 7.0:
            ev.append((te, (0.0, 5e-4 * sgn))); sgn = -sgn; te += 0.01
        jobs.append(("periodic_c30", 30.0, 9.0, ev))
    for name, c, t_end, events in jobs:
        print(f"== {name}: c={c:g} AU/yr (beta_p={1/c:.3f}), 16 seeds, {t_end} yr, "
              f"{len(events)} event(s)", flush=True)
        R = {law: run(law, c, events, seeds, t_end=t_end) for law in
             ("instant", "exact", "cell", "laplace")}
        o = {}
        o["exact_vs_cell"] = compare(R["exact"], R["cell"], "exact vs cell  (the claim)")
        o["instant_vs_exact"] = compare(R["instant"], R["exact"], "instant vs exact (plane today)")
        o["laplace_vs_exact"] = compare(R["laplace"], R["exact"], "laplace vs exact (control)")
        darr = R["exact"]["pend_exact"] - R["cell"]["pend_cell"]
        o["arrival_delta"] = dict(med=float(np.median(darr)), max=float(darr.max()),
                                  min=float(darr.min()), n=int(len(darr)),
                                  never_early=bool((darr <= 0).all()))
        o["laplace_drift"] = float(np.median(np.abs(R["laplace"]["a"][:, -1] - R["laplace"]["a"][:, 0]) / R["laplace"]["a"][:, 0]))
        o["exact_drift"] = float(np.median(np.abs(R["exact"]["a"][:, -1] - R["exact"]["a"][:, 0]) / R["exact"]["a"][:, 0]))
        print(f"  arrival delta (exact-cell): med {fmt(np.median(darr))} yr, "
              f"max {fmt(darr.max())} yr, min {fmt(darr.min())} yr, never_early={o['arrival_delta']['never_early']}")
        print(f"  net |da|/a over window: laplace {fmt(o['laplace_drift'])}  exact {fmt(o['exact_drift'])}")
        out[name] = o
    out["elapsed_s"] = time.time() - t0
    fn = "toy_out.json" if cfg == "all" else f"toy_out_{cfg}.json"
    with open(fn, "w") as f: json.dump(out, f, indent=1, default=float)
    print(f"wrote {fn} ({out['elapsed_s']:.0f}s)")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "all")
