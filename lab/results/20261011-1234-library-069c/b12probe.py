#!/usr/bin/env python3
"""B12 candidate statistic: classify residual-error growth class.

Tuned on models 1-3 (bounded, diffusive, ballistic) ONLY.
Models 4 (slow leak) and 5 (bounded+jumps) are held out: eval once.
Deterministic (seeded). Runtime target < 30 s.
"""
import numpy as np

Q = 1.0          # error quantum
T = 4096         # horizon in steps
NSEED = 100      # ensembles per model
SEED0 = 20261011


def series(kind, rng):
    """Residual (energy-error) series models. All start at 0."""
    t = np.arange(T)
    if kind == "bounded":
        # stationary AR(1) driven by +-q rounding noise (chaos-amplified rounding
        # stays stationary under a symplectic law: back-error analysis)
        e = rng.uniform(-Q, Q, T)
        x = np.zeros(T)
        for i in range(1, T):
            x[i] = 0.9 * x[i - 1] + e[i]
        return np.clip(x, -6 * Q, 6 * Q)
    if kind == "bounded_jumps":
        e = rng.uniform(-Q, Q, T)
        jp = rng.uniform(0, 1, T) < 0.005
        e = e + jp * rng.choice([-10 * Q, 10 * Q], T)
        x = np.zeros(T)
        for i in range(1, T):
            x[i] = 0.9 * x[i - 1] + e[i]
        return np.clip(x, -16 * Q, 16 * Q)
    if kind == "diffusive":
        return np.cumsum(rng.uniform(-Q, Q, T))
    if kind == "ballistic":
        return 0.01 * Q * t + rng.uniform(-Q, Q, T)
    if kind == "slow_leak":
        # step RMS ~ s^-0.25 -> Var(cumsum) ~ sqrt(t) -> RMS ~ t^0.25
        # (the recurrence ratio's killer case: sub-diffusive, NOT bounded)
        step = rng.uniform(-Q, Q, T) * (t + 1.0) ** -0.25
        return np.cumsum(step)
    raise ValueError(kind)


def classify(x, kseg=32):
    """Primary verdict: stationarity of the error distribution.
    F = var(segment means) / (var(adjacent-segment mean differences)/2).
    The blocked-difference denominator absorbs any autocorrelation shorter
    than a segment (chaos), so stationary -> F ~ 1; any compounding (leak,
    diffusion, drift) marches the means -> F >> 1. VOID (refuse) if the
    decorrelation time exceeds the segment length: the instrument cannot see.
    fcrit tuned on models 1-3 ONLY. Secondary: lag-MSD slope beta."""
    Tn = len(x)
    seg = np.array_split(x, kseg)
    means = np.array([s.mean() for s in seg])
    nseg = len(seg[0])
    denom = np.var(np.diff(means)) / 2.0
    F = np.var(means) / max(denom, 1e-15)

    # validity guard applies ONLY to a bounded verdict: marching means are
    # evidence of compounding at any tau; a flat F with tau longer than a
    # segment means the window cannot decorrelate -> refuse
    r = x - x.mean()
    rho1 = np.mean(r[:-1] * r[1:]) / max(np.mean(r * r), 1e-15)
    tau = (1.0 + rho1) / max(1.0 - rho1, 1e-9)

    fcrit = 3.5
    if F >= fcrit:
        verdict = "compounding"
    elif tau > 0.2 * nseg:
        verdict = "void"
    else:
        verdict = "bounded"

    lags = np.unique(np.round(np.geomspace(8, Tn // 8, 24)).astype(int))
    M = [np.mean((x[tau_] - x[:-tau_]) ** 2) for tau_ in lags]
    beta = max(np.polyfit(np.log(lags), np.log(np.maximum(M, 1e-12)), 1)[0], 0.0)
    if verdict == "bounded":
        sub = "bounded"
    elif beta > 1.4:
        sub = "ballistic"
    elif beta > 0.7:
        sub = "diffusive"
    elif beta > 0.3:
        sub = "leak"
    else:
        sub = "compounding-unresolved"
    return verdict, sub, [F, beta]


def run(Tn=T, seed0=SEED0):
    models = ["bounded", "diffusive", "ballistic", "slow_leak", "bounded_jumps"]
    truth = {"bounded": "bounded", "bounded_jumps": "bounded",
             "diffusive": "compounding", "ballistic": "compounding",
             "slow_leak": "compounding"}
    print(f"T={Tn} seeds={NSEED} seed0={seed0}")
    for m in models:
        ok, subs, Fs = 0, [], []
        for s in range(NSEED):
            rng = np.random.default_rng(seed0 + 1000 * s + sum(map(ord, m)))
            x = series(m, rng)
            verdict, sub, (F, beta) = classify(x)
            subs.append(sub)
            Fs.append(F)
            ok += verdict == truth[m]
        print(f"{m:14s} -> verdict pass {ok / NSEED:5.2f}  "
              f"F med={np.median(Fs):9.3g}  "
              f"subs={ {l: subs.count(l) for l in set(subs)} }")


if __name__ == "__main__":
    import sys
    run()
    if len(sys.argv) > 1 and sys.argv[1] == "short":
        T = 1024
        run(Tn=1024)
