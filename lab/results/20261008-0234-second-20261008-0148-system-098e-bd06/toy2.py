#!/usr/bin/env python3
"""toy2: the checker's named fixes, as runnable code.

1. SECOND-ORDER exact reference. The author's `exact` law solved arrival with
   the receiver's unperturbed position AT EVENT TIME (first order; error
   ~ beta_r * light-time). Here arrival solves the light cone
   |x_r(t_a) - x_s(t_e)| = c (t_a - t_e) by fixed point on the receiver's
   unperturbed Kepler (still analytic; the test body's mu_p coupling is
   second order in mu_p = 1e-3 and below the measured errors).
2. CELLINT: the shipped mechanism, not a float sample of it. One static
   per-doll INTEGER lag table (ring, ring, dspoke) -> ceil(max-distance / W0)
   quanta, where W0 = ring-0 radial width is the lattice's smallest cell
   width; the table entry is c-INDEPENDENT (a property of the doll alone:
   lag*W0/c). Receiver cell taken at ARRIVAL time (the engine's stated
   choice). ceil keeps it never early by construction.
3. The two regime gates the design needs, with numbers: c3 (beta_source
   = 0.33) and near (receiver a0 = 1.15, ~2-3 cell widths from the source).

Laws: instant | exact (2nd order) | cell (the author's float max-distance
lag, t_e cells, UNCHANGED for record continuity) | cellint (integer table,
arrival cell) | laplace (control: retarded position, must fail).
"""
import numpy as np, json, sys, time
from toy_news import (MU, M_RING, N_SPOKE, R0, kep_step, cell_index,
                      cell_lag_dist, osc_elems, fmt, compare)

W0 = R0 * (2 ** (1 / M_RING) - 1)   # ring-0 radial width (AU): lattice's smallest cell

_lagtab = {}
_tab_builds = 0
def lag_quanta(c1, c2):
    """Static per-doll integer lag table entry: ceil(dmax/W0) quanta."""
    global _tab_builds
    ds = (c2[1] - c1[1]) % N_SPOKE
    key = (c1[0], c2[0], ds)
    v = _lagtab.get(key)
    if v is None:
        v = int(np.ceil(cell_lag_dist(c1, c2) / W0 - 1e-9))
        _lagtab[key] = v; _tab_builds += 1
    return v

def run2(law, c, events, seeds, a0=1.9, e0=0.05, dt=2e-3, t_end=16.0,
         mu_p=1e-3, rec_every=50):
    n = len(seeds)
    q = a0 * (1 - e0); vp = np.sqrt((1 + e0) / (a0 * (1 - e0)))
    ang = 2 * np.pi * seeds
    xr = np.stack([q * np.cos(ang), q * np.sin(ang)], 1)
    vr = np.stack([-vp * np.sin(ang), vp * np.cos(ang)], 1)
    truth = [(0.0, np.array([1.0, 0.0]), np.array([0.0, 1.0]))]
    ra, va, ta = np.array([1.0, 0.0]), np.array([0.0, 1.0]), 0.0
    for (t_e, dv) in events:
        ra2, va2 = kep_step(ra[None, :], va[None, :], t_e - ta)
        ra, va, ta = ra2[0], va2[0] + np.array(dv), t_e
        truth.append((t_e, ra.copy(), va.copy()))
    ne = len(events)

    # ---- arrival tables ----
    # exact: light-cone fixed point on the receiver's unperturbed Kepler
    # cell:   float max-distance lag, receiver cell at t_e (author's, unchanged)
    # cellint: integer table quanta * W0/c, receiver cell at ARRIVAL time
    pend_exact = np.full((n, ne), np.inf)
    pend_cell = np.full((n, ne), np.inf)
    pend_int = np.full((n, ne), np.inf)
    xrU, vrU, tcur = xr.copy(), vr.copy(), 0.0
    for ei in range(ne):
        t_e, re_, ve_ = truth[ei + 1]
        xrU, vrU = kep_step(xrU, vrU, t_e - tcur); tcur = t_e
        # exact fixed point (second order)
        t_a = t_e + np.linalg.norm(xrU - re_, axis=1) / c
        for _ in range(12):
            xrA, _ = kep_step(xrU, vrU, t_a - t_e)
            t_a = t_e + np.linalg.norm(xrA - re_, axis=1) / c
        pend_exact[:, ei] = t_a
        cs = cell_index(re_)
        for si in range(n):
            cr = cell_index(xrU[si])
            pend_cell[si, ei] = t_e + cell_lag_dist(cs, cr) / c
            # cellint: receiver cell at arrival time (iterate)
            ta_i = pend_cell[si, ei]
            for _ in range(8):
                xrA, _ = kep_step(xrU[si][None, :], vrU[si][None, :], ta_i - t_e)
                cr2 = cell_index(xrA[0])
                ta_i = t_e + lag_quanta(cs, cr2) * W0 / c
            pend_int[si, ei] = ta_i
    pend_exact_0, pend_cell_0, pend_int_0 = (pend_exact.copy(), pend_cell.copy(),
                                             pend_int.copy())
    tab = {"exact": pend_exact, "cell": pend_cell, "cellint": pend_int}.get(law)

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
            vs[0] = vs[0] + np.array(events[ei_true - 1][1])
        if law == "instant":
            rs[1:] = rs[0]
        if tab is not None:
            due = tab <= t_new
            for si in np.nonzero(due.any(1))[0]:
                eis = np.nonzero(due[si])[0]
                ei = eis[np.argmax([truth[j + 1][0] for j in eis])]
                t_e, re_, ve_ = truth[ei + 1]
                rs2, vs2 = kep_step(re_[None, :], ve_[None, :], t_new - t_e)
                rs[si + 1], vs[si + 1] = rs2[0], vs2[0]
                tab[si, : ei + 1] = np.inf
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
                pend_exact=pend_exact_0[fin], pend_cell=pend_cell_0[fin],
                pend_int=pend_int_0[fin])

def adelta(R, key, label):
    darr = R["exact"]["pend_exact"] - R["exact"][key]
    ne = bool((darr <= 1e-12).all())
    print(f"  arrival delta exact-{label}: med {fmt(np.median(darr))} yr, "
          f"max {fmt(darr.max())}, min {fmt(darr.min())}, never_early={ne}")
    return dict(med=float(np.median(darr)), max=float(darr.max()),
                min=float(darr.min()), n=int(len(darr)), never_early=ne)

def one(name, c, t_end, events, a0=1.9):
    seeds = np.linspace(0.017, 0.983, 16)
    print(f"== {name}: c={c:g} AU/yr (beta_p={1/c:.3f}), a0={a0}, 16 seeds, "
          f"{t_end} yr, {len(events)} event(s)", flush=True)
    R = {law: run2(law, c, events, seeds, t_end=t_end, a0=a0) for law in
         ("instant", "exact", "cell", "cellint", "laplace")}
    o = {}
    o["exact2_vs_cell"] = compare(R["exact"], R["cell"], "exact(2nd) vs cell (record)")
    o["exact2_vs_cellint"] = compare(R["exact"], R["cellint"], "exact(2nd) vs cellint (claim)")
    o["instant_vs_exact2"] = compare(R["instant"], R["exact"], "instant vs exact2 (plane today)")
    o["laplace_vs_exact2"] = compare(R["laplace"], R["exact"], "laplace vs exact2 (control)")
    o["arr_cell"] = adelta(R, "pend_cell", "cell")
    o["arr_int"] = adelta(R, "pend_int", "cellint")
    return o

def main(cfg="all"):
    t0 = time.time()
    out = {}
    per = []
    te, sgn = 5.0, 1
    while te < 7.0:
        per.append((te, (0.0, 5e-4 * sgn))); sgn = -sgn; te += 0.01
    if cfg in ("all", "c30"):   out["impulsive_c30"] = one("impulsive_c30", 30.0, 12.0, [(5.0, (0.0, 0.03))])
    if cfg in ("all", "c300"):  out["impulsive_c300"] = one("impulsive_c300", 300.0, 12.0, [(5.0, (0.0, 0.03))])
    if cfg in ("all", "per"):   out["periodic_c30"] = one("periodic_c30", 30.0, 9.0, per)
    if cfg in ("all", "c3"):    out["impulsive_c3"] = one("impulsive_c3", 3.0, 12.0, [(5.0, (0.0, 0.03))])
    if cfg in ("all", "near"):  out["near_c30"] = one("near_c30", 30.0, 12.0, [(5.0, (0.0, 0.03))], a0=1.15)
    out["elapsed_s"] = time.time() - t0
    out["lagtab_entries_built"] = len(_lagtab)
    fn = "toy2_out.json" if cfg == "all" else f"toy2_out_{cfg}.json"
    with open(fn, "w") as f: json.dump(out, f, indent=1, default=float)
    print(f"wrote {fn} ({out['elapsed_s']:.0f}s, lag table entries built: {len(_lagtab)})")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "all")
