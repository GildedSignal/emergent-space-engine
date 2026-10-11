#!/usr/bin/env python3
"""B12's error series read as an attractor: persistence of the Jacobi error's increments.

Scene: CR3BP in units sep = 1 (Jupiter: mu 1e-3, R_SOI = mu^0.4, R_H = (mu/3)^(1/3),
R_p = 4.84e4/5.27e8), integrated in the rotating frame (autonomous rhs, no phase error).
The judge series is the gate's own: e_j = |C(t_j) - C(0)|/|C(0)| on the law's states,
t_j = j*P/8, j = 0..1600 (200 planet periods).

Statistics:
  EXP: faithful port of xtask/src/behave/fit.rs growth_exponent (the frozen statistic).
  VR(tau) = Var(e_{t+tau}-e_t)/(tau*Var(de_t)): the persistent share of the error's
  increments (Lo-MacKinlay variance ratio). Bounded attractor -> 0 at large tau,
  random walk -> 1, drift -> rises with tau. Decision at tau* = 200 = T/8, threshold
  1/2 (midpoint of the two model values; nothing fitted).

One run prints every table; the same command regenerates metrics.json.
"""
import json
import math
import sys

import numpy as np
from scipy.integrate import solve_ivp

# ---------------------------------------------------------------- scene (sep = 1)
MU = 1e-3
R_SOI = MU ** 0.4
R_HILL = (MU / 3.0) ** (1.0 / 3.0)
R_PLANET = 4.84e4 / 5.27e8
TWO_PI = 2.0 * math.pi
PERIODS = 200
COARSE = 8
TIMES = np.arange(PERIODS * COARSE + 1) * TWO_PI / COARSE  # 1601 samples
T = len(TIMES)
TAU_STAR = T // 8  # 200
TAUS = [4, 8, 16, 32, 64, 100, 128, 200, 320]
KEEP = 12
NTRIED_MAX = 80
HITS_MIN = 8

STAR = np.array([-MU, 0.0])  # rotating frame: star and planet fixed


def rhs(t, s):
    x, y, vx, vy = s
    r1 = math.hypot(x - STAR[0], y - STAR[1])
    r2 = math.hypot(x - (1.0 - MU), y)
    c1 = -(1.0 - MU) / (r1 * r1 * r1)
    c2 = -MU / (r2 * r2 * r2)
    return (
        vx,
        vy,
        2.0 * vy + x + c1 * (x - STAR[0]) + c2 * (x - 1.0 + MU),
        -2.0 * vx + y + c1 * y + c2 * y,
    )


def jacobi(s):
    x, y, vx, vy = s
    r1 = math.hypot(x - STAR[0], y - STAR[1])
    r2 = math.hypot(x - (1.0 - MU), y)
    return x * x + y * y + 2.0 * (1.0 - MU) / r1 + 2.0 * MU / r2 - (vx * vx + vy * vy)


def run(s0, rtol):
    sol = solve_ivp(rhs, (0.0, TIMES[-1]), s0, method="DOP853", rtol=rtol,
                    atol=rtol * 0.1, t_eval=TIMES)
    if not sol.success or sol.y.shape[1] != T:
        return None
    return sol.y.T  # (1601, 4)


def star_axis(states):
    """Semimajor axis about the star, in separations, capped at 10 (unbound)."""
    x, y, vx, vy = states.T
    vix, viy = vx - y, vy + x  # inertial velocity: v_rot + (Omega x r)
    r1 = np.hypot(x - STAR[0], y - STAR[1])
    e = 0.5 * (vix * vix + viy * viy) - (1.0 - MU) / r1
    a = (1.0 - MU) / (-2.0 * e)
    return np.minimum(a, 10.0)


def planet_r2(states):
    return np.hypot(states[:, 0] - (1.0 - MU), states[:, 1])

# ---------------------------------------------------------------- ships
def candidate(rng):
    k = rng.uniform(1.5, 3.0)
    side = 1.0 if rng.random() < 0.5 else -1.0
    r = 1.0 + side * k * R_HILL
    alpha = math.radians(rng.uniform(30.0, 330.0))
    # barycentric circular, CCW; rotating frame aligned with inertial at t = 0
    x, y = r * math.cos(alpha), r * math.sin(alpha)
    v = 1.0 / math.sqrt(r)
    vx, vy = -v * math.sin(alpha), v * math.cos(alpha)
    return np.array([x, y, vx + y, vy - x])


def ships(seed=20261011, nudge=0.0):
    """The first KEEP candidates that cross R_SOI often, stay off the planet, are
    converged (rtol 1e-13 vs 1e-11 agree on C to 1e-8 relative) and stay bound."""
    try:
        z = np.load("ships%s.npz" % ("nudged" if nudge else "base"))
        return [{"s0": z["s0"][i], "truth": z["truth"][i], "C": z["C"][i],
                 "soi_hits": int(h), "min_r2": float(m)}
                for i, (h, m) in enumerate(zip(z["hits"], z["minr2"]))]
    except OSError:
        pass
    rng = np.random.default_rng(seed)
    kept = []
    for _ in range(NTRIED_MAX):
        s0 = candidate(rng)
        if nudge:
            s0 = s0 * (1.0 + nudge)
        fine = run(s0, 1e-13)
        if fine is None:
            continue
        r2 = planet_r2(fine)
        hits = int((r2 < R_SOI).sum())
        if hits < HITS_MIN or r2.min() < 2.0 * R_PLANET or np.hypot(fine[:, 0], fine[:, 1]).max() > 3.0:
            continue
        c = np.array([jacobi(s) for s in fine])
        coarse = run(s0, 1e-11)
        if coarse is None:
            continue
        cc = np.array([jacobi(s) for s in coarse])
        if np.abs(cc - c).max() / abs(c[0]) > 1e-8:
            continue  # chaotic: this box cannot hold it, like the gate's unconverged
        kept.append({"s0": s0, "truth": fine, "C": c, "soi_hits": hits, "min_r2": float(r2.min())})
        if len(kept) == KEEP:
            break
    np.savez("ships%s.npz" % ("nudged" if nudge else "base"),
             s0=np.array([k["s0"] for k in kept]), truth=np.array([k["truth"] for k in kept]),
             C=np.array([k["C"] for k in kept]), hits=[k["soi_hits"] for k in kept],
             minr2=[k["min_r2"] for k in kept])
    return kept


# ---------------------------------------------------------------- the laws (error series)
def series_laws(ship, seed):
    truth, C = ship["truth"], ship["C"]
    c0 = abs(C[0])
    r2 = planet_r2(truth)
    e = {}
    e["echo-conserving"] = np.zeros(T)  # the gate's echo holds C exactly
    e["echo-float13"] = np.abs(C - C[0]) / c0  # the finest float path's own drift
    for rtol, name in ((1e-12, "float12"), (1e-11, "float11")):
        states = run(ship["s0"], rtol)
        c = np.array([jacobi(s) for s in states])
        e[name] = np.abs(c - c[0]) / abs(c[0])
    # planted-bounded: state-only, 1e-7 per unit of (a - a0)/R_H
    a = star_axis(truth)
    e["planted-bounded"] = 1e-7 * np.abs(a - a[0]) / R_HILL
    # planted-compound: 1e-7 x sum of one unit step per 3-R_H entry
    inside = r2 < 3.0 * R_HILL
    entries = np.flatnonzero(inside[1:] & ~inside[:-1]) + 1
    rng = np.random.default_rng(seed)
    steps = np.zeros(T)
    steps[entries] = rng.standard_normal(len(entries))
    e["planted-compound"] = 1e-7 * np.abs(np.cumsum(steps))
    # planted-kick: planetocentric velocity x1.001 per R_SOI entry; dC = -2 v.dv - |dv|^2
    kinside = r2 < R_SOI
    kentries = np.flatnonzero(kinside[1:] & ~kinside[:-1]) + 1
    dc = np.zeros(T)
    for j in kentries:
        x, y, vx, vy = truth[j]
        ux, uy = vx - y, vy + x - (1.0 - MU)  # planetocentric, inertial axes
        dv = 1e-3 * np.array([ux, uy])
        dc[j] = -2.0 * (vx * dv[0] + vy * dv[1]) - (dv[0] ** 2 + dv[1] ** 2)
    e["planted-kick"] = np.abs(np.cumsum(dc)) / c0
    # drifts and noises (independent of the trajectory)
    j = np.arange(T)
    e["planted-drift"] = 1e-10 * j / (T - 1)
    e["leak-1e-12/period"] = 1e-12 * j / COARSE
    rng = np.random.default_rng(seed + 1)
    e["noise-1e-11"] = np.abs(rng.normal(0.0, 1e-11, T))
    shape = np.abs(a - a[0]) / max(1e-300, np.abs(a - a[0]).max())
    e["scaled-1e-11"] = 1e-11 * shape
    return e


def leak_sweep(seed):
    """Drift rate sweep on a bounded background of amplitude 1e-11 (control version)."""
    out = {}
    j = np.arange(T)
    for amp in (1e-11, 2e-11):
        for per_period in (1e-13, 3e-13, 1e-12, 3e-12, 1e-11):
            rng = np.random.default_rng(seed + 77)
            laws = [np.abs(rng.normal(0.0, amp, T)) + per_period * j / COARSE for _ in range(KEEP)]
            out[f"leak {per_period:.0e}/period on {amp:.0e}"] = laws
    return out


# ---------------------------------------------------------------- statistics
def growth_exponent(err):
    """Port of xtask/src/behave/fit.rs (16 windows, first 10% dropped, window max)."""
    n = len(err)
    first = max(n // 10, 1)
    if n <= first or any(not math.isfinite(x) for x in err):
        return float("nan")
    W = 16

    def edge(j):
        return n if j == W else round(first * (n / first) ** (j / W))

    pts, used = [], 0
    for j in range(W):
        a, b = edge(j), edge(j + 1)
        if b <= a:
            continue
        used += 1
        top = max(abs(x) for x in err[a:b])
        if top > 0.0:
            pts.append((math.log(math.sqrt(a * (b - 1))), math.log(top)))
    if used < W // 2:
        return float("nan")
    if not pts:
        return 0.0
    if len(pts) < 3:
        return float("nan")
    mx = sum(p[0] for p in pts) / len(pts)
    my = sum(p[1] for p in pts) / len(pts)
    return (sum((p[0] - mx) * (p[1] - my) for p in pts)
            / sum((p[0] - mx) ** 2 for p in pts))


def vr(err, tau):
    e = np.asarray(err, dtype=float)
    v = np.diff(e).var()
    if v <= 0.0:
        return 0.0
    return (e[tau:] - e[:-tau]).var() / (tau * v)


def pooled(laws, tau):
    xs = np.array([vr(l, tau) for l in laws])
    med = float(np.median(xs))
    mad = np.median(np.abs(xs - med)) * 1.4826
    se = max(mad / math.sqrt(len(xs)), 1e-12)
    return med, float(se), xs


def trend(laws, lags=50):
    """Drift test: OLS slope of e on t with Newey-West (HAC) standard errors.
    VR is invariant to a deterministic ramp (a variance drops constants), so drift
    is the other half of compounding: mean persistence. The floor is the noise
    amplitude over sqrt(T) (an amplitude/horizon floor), not a memory floor."""
    ts, bs, ses = [], [], []
    n = len(laws[0])
    t = np.arange(n) - (n - 1) / 2.0
    for e in laws:
        e = np.asarray(e, float)
        b = float((t * (e - e.mean())).sum() / (t * t).sum())
        r = e - e.mean() - b * t  # residuals
        g = [np.cov(r[:-k], r[k:])[0, 1] if k else np.var(r) for k in range(lags + 1)]
        s2 = g[0] + 2.0 * sum((1.0 - k / (lags + 1)) * g[k] for k in range(1, lags + 1))
        # HAC se of the slope: s2 / sum((t - tbar)^2)
        ses.append(math.sqrt(max(s2, 0.0) / (t * t).sum()))
        bs.append(b)
        ts.append(abs(b) / ses[-1] if ses[-1] > 0 else 0.0)
    return float(np.median(bs)), float(np.median(ses)), float(np.median(ts))


def verdict(med, se, half=0.5, k=3.0):
    if med - k * se > half:
        return "FAIL"
    if med + k * se < half:
        return "PASS"
    return "INDETERMINATE"


# ---------------------------------------------------------------- run
def main():
    print("scene: mu %.0e  R_SOI %.4f  R_HILL %.4f  T %d  tau* %d" % (MU, R_SOI, R_HILL, T, TAU_STAR))
    base = ships()
    print("kept %d/%d tried; soi coarse hits %s" % (len(base), NTRIED_MAX,
          sorted(s["soi_hits"] for s in base)))
    if len(base) < 8:
        print("TOO FEW SHIPS: %d" % len(base))
        return 1
    laws = {}
    for i, ship in enumerate(base):
        for name, e in series_laws(ship, seed=1000 + i).items():
            laws.setdefault(name, []).append(e)

    sweep = leak_sweep(seed=5000)
    allsets = dict(laws)
    allsets.update(sweep)

    table = []
    for name, series in allsets.items():
        exps = [growth_exponent(e) for e in series]
        exp_med = float(np.nanmedian(exps))
        med, se, xs = pooled(series, TAU_STAR)
        vr100, _, _ = pooled(series, 100)
        vr320, _, _ = pooled(series, 320)
        tr, trse, trt = trend(series)
        tdrift = trt - 3.0
        table.append({
            "law": name, "exp_median": exp_med,
            "exp_pass_0.2": bool(exp_med <= 0.2),
            "vr_tau*": med, "vr_se": se,
            "vr_100": vr100, "vr_320": vr320,
            "vr_verdict": verdict(med, se),
            "trend": tr, "trend_se": trse, "trend_t": trt,
            "trend_verdict": "FAIL" if tdrift > 0 else "PASS",
            "class": "",
            "max_err": float(max(np.nanmax(e) for e in series)),
        })

    # positive-control null spread of VR (for the derived threshold's sigma)
    noise_se = [t for t in table if t["law"] == "noise-1e-11"][0]["vr_se"]
    bounded_se = [t for t in table if t["law"] == "planted-bounded"][0]["vr_se"]
    se_null = max(noise_se, bounded_se)

    def cls(t):
        if t["law"] in ("echo-conserving", "planted-bounded", "noise-1e-11", "scaled-1e-11",
                        "leak-1e-12/period") and t["law"] != "leak-1e-12/period":
            return "positive"
        return ""
    print("\n%-34s %9s %5s %7s %6s %7s %7s %+7s %9s %9s %6s" %
          ("law", "EXP", "pass", "VR(200)", "se", "VR(100)", "VR(320)", "margin",
           "VR verdict", "trend t", "tr-verdict"))
    for t in table:
        margin = (0.5 - t["vr_tau*"]) / (se_null if se_null > 0 else 1)
        print("%-34s %9.3f %5s %7.3f %6.3f %7.3f %7.3f %+7.1f %9s %9.1f %6s" %
              (t["law"], t["exp_median"], str(t["exp_pass_0.2"]), t["vr_tau*"], t["vr_se"],
               t["vr_100"], t["vr_320"], margin, t["vr_verdict"], t["trend_t"], t["trend_verdict"]))
    print("\nse_null (max of noise, planted-bounded across-ship): %.3f" % se_null)
    print("pooled separation of planted-bounded vs planted-compound, in se_null: %.1f" %
          ((dict((t["law"], t["vr_tau*"]) for t in table)["planted-compound"]
            - dict((t["law"], t["vr_tau*"]) for t in table)["planted-bounded"]) / se_null))

    # ulp-nudge stability of every verdict
    nudged = ships(seed=20261011, nudge=2 ** -52)
    flips = []
    if len(nudged) == KEEP:
        nlaws = {}
        for i, ship in enumerate(nudged):
            for name, e in series_laws(ship, seed=1000 + i).items():
                nlaws.setdefault(name, []).append(e)
        for name in laws:
            m0, s0, _ = pooled(laws[name], TAU_STAR)
            m1, s1, _ = pooled(nlaws[name], TAU_STAR)
            v0, v1 = verdict(m0, s0), verdict(m1, s1)
            if v0 != v1:
                flips.append((name, v0, v1, m0, m1))
        print("ulp-nudge verdict flips: %s" % (flips if flips else "none"))
    else:
        print("ulp-nudge: kept %d ships (chaotic selection moved); flips not compared" % len(nudged))

    json.dump({"table": table, "se_null": se_null, "flips": flips,
               "ships": [{"soi_hits": s["soi_hits"], "min_r2": s["min_r2"]} for s in base]},
              open(sys.argv[1] if len(sys.argv) > 1 else "metrics.json", "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
