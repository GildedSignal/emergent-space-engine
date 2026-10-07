#!/usr/bin/env python3
"""Cadence analysis: N_min per case vs gate stand-ins (B14 precession/classification,
B17 pump/libration/regime, B5-style bounded residual). Reference = same scheme, n=256."""
import numpy as np, sys, glob, os, gzip

NV = [1, 2, 4, 8, 16, 32, 64, 128]
REF = 512
CTRL = 256
D = os.path.dirname(os.path.abspath(__file__))

def unwrap(x, period=2 * np.pi):
    x = np.array(x, float)
    out = x.copy()
    for i in range(1, len(x)):
        d = x[i] - x[i - 1]
        if d > period / 2: out[i:] -= period
        elif d < -period / 2: out[i:] += period
    return out

def load(case, n, seed):
    rows = []
    import gzip as _g
    op = _g.open if os.path.exists(f"{D}/csv_{case}.csv.gz") else open
    with op(f"{D}/csv_{case}.csv" + (".gz" if os.path.exists(f"{D}/csv_{case}.csv.gz") else ""), "rt") as f:
        for line in f:
            p = line.split(",")
            if p[0] != case or int(p[1]) != n or int(p[2]) != seed: continue
            if float(p[5]) < 0: continue  # escape marker row
            rows.append([float(x) for x in p[3:]])
    t = np.array([r[1] for r in rows]); a = np.array([r[2] for r in rows])
    e = np.array([r[3] for r in rows]); w = np.array([r[4] for r in rows]); lam = np.array([r[5] for r in rows])
    esc = np.any(a < 0)
    tesc = t[np.argmin(a)] if esc else np.nan
    return t, a, e, w, lam, esc, tesc

def presrate(t, w, a):
    if len(t) < 50: return np.nan
    wu = unwrap(w)
    ok = (t >= 0.15 * t[-1]) & (t <= 0.9 * t[-1]) & (a > 0)
    if ok.sum() < 40: return np.nan
    c = np.polyfit(t[ok], wu[ok], 1)
    resid = wu[ok] - np.polyval(c, t[ok])
    return c[0], np.std(resid)

def analyze(case, n_p, res_j=None, horizon=None):
    gz = os.path.exists(f"{D}/csv_{case}.csv.gz")
    _op = gzip.open if gz else open
    seeds = sorted({int(l.split(",")[2]) for l in _op(f"{D}/csv_{case}.csv" + (".gz" if gz else ""), "rt") if l.startswith(case)})
    per_n = {}
    for n in NV + [REF, CTRL]:
        rows = {}
        for s in seeds:
            t, a, e, w, lam, esc, tesc = load(case, n, s)
            rows[s] = dict(t=t, a=a, e=e, w=w, lam=lam, esc=esc)
        per_n[n] = rows
    # significance of reference precession signal
    ref_pr = {}
    for s in seeds:
        pr = presrate(per_n[REF][s]["t"], per_n[REF][s]["w"], per_n[REF][s]["a"])
        ref_pr[s] = pr
    # 512 control on convergence
    ctrl = []
    for s in seeds:
        pr512 = presrate(per_n[CTRL][s]["t"], per_n[CTRL][s]["w"], per_n[CTRL][s]["a"])
        if not (isinstance(pr512, tuple) and isinstance(ref_pr[s], tuple)):
            c = np.nan
        else:
            c = abs(pr512[0] - ref_pr[s][0]) / abs(ref_pr[s][0]) if abs(ref_pr[s][0]) > 0 else np.nan
        ctrl.append(c)
    # resonant reference regime (per seed) from REF series
    def res_angle(s, n):
        r = per_n[n][s]
        phi = unwrap(2 * n_p * r["t"] - unwrap(r["lam"]) - unwrap(r["w"]))
        return phi
    out = {"ctrl512": ctrl, "rows": []}
    for n in NV:
        for s in seeds:
            r, rf = per_n[n][s], per_n[REF][s]
            # classification: escape match
            cls_ok = (r["esc"] == rf["esc"])
            # precession
            pr = presrate(r["t"], r["w"], r["a"])
            if isinstance(ref_pr[s], tuple) and isinstance(pr, tuple):
                relerr = abs(pr[0] - ref_pr[s][0]) / abs(ref_pr[s][0])
                sig = abs(ref_pr[s][0]) * (rf["t"][-1] - rf["t"][0])
            else:
                relerr, sig = np.nan, 0.0
            # residual walk exponent vs ref
            wu = unwrap(r["w"]); wu_r = unwrap(rf["w"])
            tt = r["t"]; ok = tt <= rf["t"][-1]
            res = wu[: ok.sum()] - np.interp(tt[ok], rf["t"], wu_r)
            if len(res) > 60 and np.max(np.abs(res)) > 1e-9:
                tq = tt[ok][len(res) // 2:]
                rq = np.abs(res[len(res) // 2:])
                good = np.isfinite(rq) & (tq > 0) & (rq > 0)
                t2, r2 = tq[good], rq[good]
                ex = np.polyfit(np.log(t2), np.log(np.maximum(r2, 1e-300)), 1)[0]
            else:
                ex = 0.0
            # resonant bars
            pump, libr_ratio, regime_ok = np.nan, np.nan, True
            if res_j is not None:
                phi = res_angle(s, n); phi_r = res_angle(s, REF)
                def librange(phi, t):
                    m = t >= 0.2 * t[-1]
                    u = phi[m]
                    return (u.max() - u.min())
                lr, lrr = librange(phi, r["t"]), librange(phi_r, rf["t"])
                regime_ok = (lr < 2 * np.pi * 0.95) == (lrr < 2 * np.pi * 0.95)
                if lrr < 2 * np.pi * 0.95:
                    libr_ratio = lr / lrr if lrr > 1e-6 else np.nan
                    m = rf["t"] >= 0.9 * rf["t"][-1]
                    e_end_ref = np.mean(rf["e"][m])
                    m2 = r["t"] >= 0.9 * r["t"][-1]
                    e_end = np.mean(r["e"][m2]) if m2.sum() else np.nan
                    e0 = rf["e"][0]
                    pump = (e_end - e0) / (e_end_ref - e0) if abs(e_end_ref - e0) > 1e-4 else np.nan
            out["rows"].append(dict(n=n, s=s, cls_ok=cls_ok, relerr=relerr, sig=sig, walk_ex=ex,
                                    pump=pump, libr=libr_ratio, regime=regime_ok,
                                    esc=r["esc"], esc_ref=rf["esc"]))
    return out

def nmin(case, res):
    seeds = sorted({r["s"] for r in res["rows"]})
    per_seed = {}
    for s in seeds:
        rr = [r for r in res["rows"] if r["s"] == s]
        n_s = None
        for r in sorted(rr, key=lambda r: r["n"]):
            ok = r["cls_ok"] and r["regime"]
            if r["sig"] > 0.05:
                if not np.isfinite(r["relerr"]) or r["relerr"] > 0.10: ok = False
            if np.isfinite(r["pump"]) and not (0.8 <= r["pump"] <= 1.25): ok = False
            if np.isfinite(r["libr"]) and r["libr"] < 0.8: ok = False
            if r["walk_ex"] > 0.2: ok = False
            if ok: n_s = r["n"]; break
        per_seed[s] = n_s
    vals = [v for v in per_seed.values() if v is not None]
    med = int(np.median(vals)) if vals else None
    worst = max(vals) if vals else None
    nfail = sum(1 for v in per_seed.values() if v is None)
    return med, worst, nfail, per_seed

CASES = {
    "M1": (1000.0005, None), "M2": (1000.0005, None), "M3": (1000.0005, None),
    "M4": (1000.0005, None), "M5": (1000.0005, None), "M6": (316.2295, None),
    "B1": (1.0005, None), "B2": (1.0005, None),
    "B3": (1.0005, "j2"), "B4": (1.0005, "j2"), "B5": (1.0005, "j32"), "B6": (1.0005, "j2"),
}
if __name__ == "__main__":
    print(f"{'case':4} {'N_med':>6} {'N_worst':>7} {'noN':>4}  ctrl512   relerr@8  relerr@16  notes")
    for case, (n_p, rj) in CASES.items():
        res = analyze(case, n_p, res_j=rj)
        med, worst, nfail, per_seed = nmin(case, res)
        def rel_at(n):
            v = [r["relerr"] for r in res["rows"] if r["n"] == n and np.isfinite(r["relerr"]) and r["sig"] > 0.05]
            return f"{np.median(v):8.3g}" if v else "     n/a"
        ctrl = [c for c in res["ctrl512"] if np.isfinite(c)]
        print(f"{case:4} {str(med):>6} {str(worst):>7} {nfail:>4}  "
              f"{(f'{np.median(ctrl):.1e}' if ctrl else 'n/a'):>8}  {rel_at(8)} {rel_at(16)}  {per_seed}")
