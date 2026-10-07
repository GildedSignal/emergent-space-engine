#!/usr/bin/env python3
"""Certificate horizon under apsidal precession (lab run 20261007-1550-dynamics-71a5).

Truth: each body on a uniformly precessing conic (the tube's float form: radial cycle exact,
period P = 2*pi/n, apsidal advance dper per orbit). Certificate: the same pair frozen at
t=0 (crates/encounters models fixed pom, no precession). Proposal = frozen local minimum
< safety*rho (the crate's safety-scaled window). MISS = true minimum < rho with no proposal
within 0.4 synodic spacings.

Two horizons are separated:
  t_cross  (safety): when differential precession first makes the pair's Binet geometry
           crossing (cone gap < 0) or shifts the arcs past the frozen window — the
           certificate is wrong from here, whether or not an encounter realizes.
  t_realize: first brute-force sub-rho event = t_cross + conjunction-sampling waiting
           W ~ P_syn/p_arc (a geometry constant, independent of the drift rate).
"""
import json, math, os, platform, time
import numpy as np

TAU = 2.0 * np.pi
GOLD = (math.sqrt(5.0) - 1.0) / 2.0


def body(a, e, pom, n, M0=0.0, dper=0.0):
    return dict(a=a, e=e, pom=pom, n=n, M0=M0, Om=dper * n / TAU)


def lam_r(b, t):
    e = b["e"]
    M = (b["M0"] + b["n"] * t) % TAU
    E = np.full_like(M, np.pi, dtype=float) if e > 0.75 else M.astype(float)
    for _ in range(12):
        E -= (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    nu = 2.0 * np.arctan2(np.sqrt(1 + e) * np.sin(0.5 * E), np.sqrt(1.0 - e) * np.cos(0.5 * E))
    r = b["a"] * (1.0 - e * np.cos(E))
    return b["pom"] + b["Om"] * t + nu, r


def d2_pair(bi, bj, t):
    li, ri = lam_r(bi, t)
    lj, rj = lam_r(bj, t)
    dx = ri * np.cos(li) - rj * np.cos(lj)
    dy = ri * np.sin(li) - rj * np.sin(lj)
    return dx * dx + dy * dy


def d2_scalar(bi, bj, t):
    return float(d2_pair(bi, bj, np.array([t]))[0])


def pair_minima(bi, bj, T, N, dmax, chunk=1 << 21):
    """All local minima of the distance below dmax on [0,T), golden-refined."""
    step = T / N
    out = []
    prev_d = None
    for c0 in range(0, N, chunk):
        c1 = min(c0 + chunk, N)
        t = np.arange(c0, c1, dtype=np.int64) * step
        d2 = d2_pair(bi, bj, t)
        d2f = d2 if prev_d is None else np.concatenate(([prev_d], d2))
        thr = dmax * dmax
        k = np.nonzero((d2f[1:-1] < d2f[:-2]) & (d2f[1:-1] <= d2f[2:]) & (d2f[1:-1] < thr))[0]
        for i in k:
            # d2f[1:-1][i] is d2f index i+1: t index i+1 (first chunk) or c0+i (stitched)
            j = (i + 1) if c0 == 0 else (c0 + i)
            if j < 1:
                continue
            a_, b_ = (j - 1) * step, (j + 1) * step
            c_, d_ = b_ - GOLD * (b_ - a_), a_ + GOLD * (b_ - a_)
            fc, fd = d2_scalar(bi, bj, c_), d2_scalar(bi, bj, d_)
            for _ in range(60):
                if fc < fd:
                    b_, d_, fd = d_, c_, fc
                    c_ = b_ - GOLD * (b_ - a_)
                    fc = d2_scalar(bi, bj, c_)
                else:
                    a_, c_, fc = c_, d_, fd
                    d_ = a_ + GOLD * (b_ - a_)
                    fd = d2_scalar(bi, bj, d_)
            tm = 0.5 * (a_ + b_)
            out.append((tm, math.sqrt(d2_scalar(bi, bj, tm))))
        prev_d = float(d2[-1])
    out.sort()
    return out


def frozen(b):
    return dict(b, Om=0.0)


def run_case(name, bi, bj, rho, T, N, froz, safety=1.2, dmax=0.05):
    Psyn = TAU / abs(bi["n"] - bj["n"])
    true_m = pair_minima(bi, bj, T, N, dmax)
    prop = [(t, d) for (t, d) in froz if d < safety * rho]
    misses, first, missed_list = 0, None, []
    for (t, d) in true_m:
        if d < rho:
            if not any(abs(tp - t) < 0.4 * Psyn for (tp, dp) in prop):
                misses += 1
                missed_list.append((t, d))
                if first is None:
                    first = t
    waste = sum(1 for (tp, dp) in prop
                if not any(d < rho and abs(t - tp) < 0.4 * Psyn for (t, d) in true_m))
    m0 = min((d for (_, d) in froz), default=float("nan"))
    mt = min((d for (_, d) in true_m), default=float("nan"))
    ser = []
    ci = 0
    for (t, d) in true_m:
        while ci + 1 < len(froz) and froz[ci + 1][0] < t:
            ci += 1
        cands = froz[max(0, ci - 1): ci + 2]
        if cands:
            best = min(cands, key=lambda p: abs(p[0] - t))
            if abs(best[0] - t) < 0.45 * Psyn:
                ser.append((t, d - best[1]))
    return dict(name=name, rho=rho, T=T, Psyn=Psyn, n_true=len(true_m), n_prop=len(prop),
                misses=misses, first_miss=first, waste=waste, m0_frozen=m0, m0_true=mt,
                first_prop=(prop[0][0] if prop else None),
                drift_t=[p[0] for p in ser], drift_dd=[p[1] for p in ser],
                missed_events=missed_list[:8])


def first_below(ms, rho):
    for (t, d) in ms:
        if d < rho:
            return t
    return None


def fit_exp(xs, ys, floor=0.0):
    x = np.array([float(v) for v in xs if v is not None and v > 0])
    y = np.array([float(v) for v in ys if v is not None])
    if len(x) < 3:
        return None
    lx, ly = np.log(x), np.log(np.maximum(np.abs(y), floor if floor > 0 else 1e-300))
    A = np.vstack([lx, np.ones_like(lx)]).T
    (slope, itc), *_ = np.linalg.lstsq(A, ly, rcond=None)
    return dict(slope=round(float(slope), 4), intercept=round(float(itc), 4), n=len(x))


def binet(b):
    p = b["a"] * (1 - b["e"] ** 2)
    u = 1 / p
    return u, b["e"] * u * math.cos(b["pom"]), b["e"] * u * math.sin(b["pom"])


def cone_gap(bi, bj):
    Ui, Vi, Wi = binet(bi)
    Uj, Vj, Wj = binet(bj)
    return abs(Ui - Uj) - math.hypot(Vi - Vj, Wi - Wj)


def R_of(bi, bj):
    _, Vi, Wi = binet(bi)
    _, Vj, Wj = binet(bj)
    return math.hypot(Vi - Vj, Wi - Wj)


def machine():
    load = open("/proc/loadavg").read().split()
    free = [l.split(": ")[1].strip() for l in open("/proc/meminfo").read().splitlines()
            if l.startswith(("MemTotal", "MemAvailable"))]
    return dict(host=platform.node(), cpu=platform.machine(), nproc=os.cpu_count(),
                loadavg1=load[0], mem=free, time=time.strftime("%Y-%m-%dT%H:%M:%S"))


def main():
    T, N = 2500.0, 1 << 22
    results = dict(machine=machine(), params=dict(T=T, N=N), cases=[], fits={})
    nn = lambda a: a ** -1.5
    G2 = (body(1.0, 0.30, 0.3, nn(1.0)), body(0.85, 0.40, 1.2, nn(0.85)))
    G4 = (body(1.0, 0.30, 0.3, nn(1.0), 0.0), body(0.8, 0.30, 1.02, nn(0.8), 0.7))
    RHO = 0.004

    froz = {"G2": pair_minima(frozen(G2[0]), frozen(G2[1]), T, N, 0.05),
            "G4": pair_minima(frozen(G4[0]), frozen(G4[1]), T, N, 0.05)}
    results["fits"]["calib"] = {
        g: dict(rho=RHO, m0_frozen=min(d for _, d in froz[g]), cone_gap=cone_gap(*gg),
                first_frozen_sub_rho=first_below(froz[g], RHO))
        for g, gg in (("G2", G2), ("G4", G4))}
    for g in ("G2", "G4"):
        c = results["fits"]["calib"][g]
        print(f"calib {g}: m0={c['m0_frozen']:.5f} cone_gap={c['cone_gap']:+.5f} "
              f"first_frozen_sub_rho={c['first_frozen_sub_rho']}", flush=True)

    # --- controls (prediction 1) ---
    for g, gg in (("G2", G2), ("G4", G4)):
        for tag, dpi, dpj in (("kepler", 0.0, 0.0), ("coprec", 0.3, 0.3)):
            bi = dict(gg[0], Om=dpi * gg[0]["n"] / TAU)
            bj = dict(gg[1], Om=dpj * gg[1]["n"] / TAU)
            r = run_case(f"control-{g}-{tag}", bi, bj, RHO, T, N, froz[g])
            results["cases"].append(r)
            print(f"control {g} {tag}: misses={r['misses']} m0_true={r['m0_true']:.6f} "
                  f"vs frozen {r['m0_frozen']:.6f}", flush=True)

    # --- sweep A: active section (G2, crossing at t=0), first MISS vs drift rate ---
    dps = np.logspace(-4.5, -3.0, 7)  # rad per unit time on body i; j stays fixed
    HA = []
    for dp in dps:
        bi = dict(G2[0], Om=dp)
        r = run_case(f"A-G2-om{dp:.4g}", bi, G2[1], RHO, T, N, froz["G2"])
        results["cases"].append(r)
        HA.append(r["first_miss"])
        print(f"A G2 Om={dp:.3g}: first_miss={r['first_miss']} misses={r['misses']} "
              f"n_true={r['n_true']} n_prop={r['n_prop']} waste={r['waste']}", flush=True)
    ok = [(w, h) for w, h in zip(dps, HA) if h is not None]
    results["fits"]["A_G2"] = dict(om=[float(x) for x in dps],
                                   H=[None if h is None else float(h) for h in HA],
                                   exp=fit_exp([w for w, _ in ok], [h for _, h in ok]))
    print("A_G2 fit:", results["fits"]["A_G2"]["exp"], flush=True)

    # --- drift linearity (prediction 2) ---
    for dp in (1e-4, 3e-4):
        bi = dict(G2[0], Om=dp)
        r = run_case(f"drift-G2-om{dp:.4g}", bi, G2[1], RHO, T, N, froz["G2"])
        results["cases"].append(r)
        t = np.array(r["drift_t"]); dd = np.abs(np.array(r["drift_dd"]))
        sel = (t > 0.25 * T) & (dd > 0)
        f = fit_exp(t[sel], dd[sel], floor=1e-13)
        amp = float(np.median(dd[sel] / t[sel]))
        results["fits"][f"drift_om{dp:.4g}"] = dict(exp=f, amp_per_t=amp, n=int(sel.sum()))
        print(f"drift Om={dp:.3g}: |dd| ~ t^{f['slope']} amp/t={amp:.3e} n={sel.sum()}", flush=True)

    # --- sweep B: 'None' pair (G4, cone gap > 0 at t=0, near-tangent) ---
    h = 1e-4
    R0 = R_of(G4[0], G4[1])
    Rp = R_of(G4[0], dict(G4[1], pom=G4[1]["pom"] - h))
    dRdvar = (R0 - Rp) / h
    gap0 = cone_gap(*G4)
    tc_const = abs(gap0) / dRdvar if dRdvar > 0 else None  # t_cross = tc_const / Om
    results["fits"]["B_G4"] = dict(cone_gap0=gap0, dR_dvar=dRdvar, t_cross_const_per_om=tc_const)
    print(f"B G4: gap0={gap0:+.5f} dR/dvar={dRdvar:.4f} t_cross = {tc_const:.4f}/Om", flush=True)
    HB = []
    dpsB = np.logspace(-5.0, -3.0, 8)
    for dp in dpsB:
        bj = dict(G4[1], Om=-dp)
        tm_all = pair_minima(G4[0], bj, T, N, 0.05)
        fb = first_below(tm_all, RHO)
        r = run_case(f"B-G4-om{dp:.4g}", G4[0], bj, RHO, T, N, froz["G4"])
        r["first_true_below"] = fb
        results["cases"].append(r)
        HB.append(fb)
        print(f"B G4 Om={dp:.3g}: first_sub_rho={fb} "
              f"t_cross={tc_const/dp:.1f} (misses={r['misses']})", flush=True)
    okB = [(w, hb) for w, hb in zip(dpsB, HB) if hb is not None]
    results["fits"]["B_G4"].update(om=[float(x) for x in dpsB],
                                   first_sub_rho=[None if v is None else float(v) for v in HB],
                                   exp=fit_exp([w for w, _ in okB], [v for _, v in okB]))
    print("B_G4 fit:", results["fits"]["B_G4"]["exp"], flush=True)

    # --- mechanism constant: m0 vs rigid relative rotation of pom_j ---
    md = {}
    for dlt in (0.0, +0.02, -0.02):
        bj = dict(G2[1], pom=G2[1]["pom"] + dlt)
        md[f"{dlt:+.2f}"] = min(d for (_, d) in pair_minima(frozen(G2[0]), frozen(bj), T, N, 0.05))
    results["fits"]["m_of_dpom"] = md
    results["fits"]["m_of_dpom"]["dm0_dpom"] = (md["+0.02"] - md["-0.02"]) / 0.04
    print(f"m0(dpom): {md}", flush=True)

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json"), "w") as f:
        json.dump(results, f, indent=1)
    print("wrote results.json")


if __name__ == "__main__":
    main()
