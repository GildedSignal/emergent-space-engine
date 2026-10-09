#!/usr/bin/env python3
"""Falsifier for representation.md line 57 / law.md line 53:
"Each visible tube crosses the observer's past light cone once; Newton's
method finds the crossing, starting from the previous frame's [crossing]."

Units c = 1, seconds. Observer inertial at origin. Emitter approaches from +x,
worldline exists for t < 0 (chase already in progress at frame 0). Frames run
from t_o = 0 until the emitter's arrival. For an approach at beta the root
sits at t_e ~ (t_o - D0)/(1+beta) — up to 50,000 s in the past at
beta = 0.9999 ("you see the past").

Arms:
 (a) control: inertial smooth tubes (premise should hold: <= 2 iterations).
 (b) relativistic chase: hyperbolic (constant proper accel) approaching tube.
 (c) kinked tubes: piecewise-linear worldline, velocity jumps at kick step
     boundaries — the design's own tube shape (law.md line 33).

Solver is the doc's: Newton on f(t_e) = t_o - t_e - |x(t_e)|, f' = -1 - v(t_e),
started (i) literally from the previous frame's root, or (ii) from a
velocity-aware affine extrapolation te_prev + dt/(1+|v(te_prev)|) — the
charitable reading. Truth = bisection on an expanding bracket.
Cap 12 iterations, tol 1e-9*(1+|t|).
"""
import json
import sys
import numpy as np

CAP = 12
TOL = 1e-9
DT = 1.0 / 60.0


class Hyperbolic:
    """Constant proper acceleration alpha (alpha > 0 = approaching faster)."""

    def __init__(self, x0, beta0, alpha):
        self.x0, self.eta0, self.alpha = x0, np.arctanh(beta0), alpha

    def _t(self, tau):
        e0, a = self.eta0, self.alpha
        if a == 0.0:
            return tau
        return (np.sinh(e0) - np.sinh(e0 - a * tau)) / a

    def _x(self, tau):
        e0, a = self.eta0, self.alpha
        if a == 0.0:
            return self.x0 + np.tanh(e0) * tau
        return self.x0 + (np.cosh(e0) - np.cosh(e0 - a * tau)) / a

    def _tau_of_t(self, t):
        lo, hi = -1.0, 1.0
        while self._t(hi) < t:
            hi *= 2
        while self._t(lo) > t:
            lo *= 2
        for _ in range(70):
            mid = 0.5 * (lo + hi)
            if self._t(mid) < t:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    def x_of_t(self, t):
        return self._x(self._tau_of_t(t))

    def v_of_t(self, t):
        return np.tanh(self.eta0 - self.alpha * self._tau_of_t(t))

    def arrival_t(self):
        lo, hi = 0.0, 1.0
        while self.x_of_t(hi) > 0:
            hi *= 2
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            if self.x_of_t(mid) > 0:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)


class Kinked:
    """v constant between kick times (spacing dt_kick), jumping by +-dv."""

    def __init__(self, x0, beta, dv, dt_kick, t_back, t_fwd, seed):
        rng = np.random.default_rng(seed)
        n = int((t_back + t_fwd) / dt_kick)
        jumps = rng.choice([-1.0, 1.0], size=n) * dv
        v = beta + np.concatenate([[0.0], np.cumsum(jumps)])
        v = np.clip(v, -0.999999, -0.5)
        self.tk = np.linspace(-t_back, t_fwd, n + 1)
        self.v = v
        self.x = x0 + np.concatenate([[0.0], np.cumsum(v[:-1] * np.diff(self.tk))])

    def _seg(self, t):
        i = np.searchsorted(self.tk, t, side="right") - 1
        return max(0, min(i, len(self.v) - 1))

    def x_of_t(self, t):
        i = self._seg(t)
        return self.x[i] + self.v[i] * (t - self.tk[i])

    def v_of_t(self, t):
        return self.v[self._seg(t)]

    def arrival_t(self):
        lo, hi = 0.0, 1.0
        while self.x_of_t(hi) > 0:
            hi *= 2
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            if self.x_of_t(mid) > 0:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)


def f_of(wl, t_o, te):
    return t_o - te - abs(wl.x_of_t(te))


def bracket(wl, t_o, D0):
    """f decreasing; root in (lo, hi) iff f(lo) > 0 > f(hi). Expand left."""
    hi = t_o - 1e-12
    lo = min(2.0 * (t_o - D0), -1.0)
    while f_of(wl, t_o, lo) <= 0:
        lo *= 2
    return lo, hi


def bisect_root(wl, t_o, D0):
    lo, hi = bracket(wl, t_o, D0)
    for _ in range(120):
        mid = 0.5 * (lo + hi)
        if f_of(wl, t_o, lo) * f_of(wl, t_o, mid) <= 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def newton(wl, t_o, guess, lo):
    t = guess
    for it in range(1, CAP + 1):
        fv = f_of(wl, t_o, t)
        if abs(fv) < TOL * (1.0 + abs(t)):
            return t, it - 1, True
        t = t - fv / (-1.0 - wl.v_of_t(t))
        if t < lo:
            t = lo
    return t, CAP, False


def run_frames(wl, D0, n_frames, mode, label):
    te_prev, v_prev = None, None
    iters, stalls, pos_err = [], 0, []
    t_arrival = wl.arrival_t()
    n = min(n_frames, max(30, int((t_arrival - 0.02) / DT)))
    t_o = 0.0
    for _ in range(n):
        te_true = bisect_root(wl, t_o, D0)
        lo, _ = bracket(wl, t_o, D0)
        if te_prev is None:
            guess = te_true  # first frame: perfect init (charitable)
        elif mode == "prevroot":
            guess = te_prev
        else:  # velocity-aware affine extrapolation (dt_e = dt_o/(1+|v|))
            guess = te_prev + DT / max(1e-12, (1.0 + v_prev))
        te_n, it, ok = newton(wl, t_o, guess, lo)
        iters.append(it)
        stalls += 0 if ok else 1
        pos_err.append(abs(abs(wl.x_of_t(te_n)) - abs(wl.x_of_t(te_true))))
        te_prev, v_prev = te_true, wl.v_of_t(te_true)
        t_o += DT
    its, pe = np.array(iters), np.array(pos_err)
    return {
        "label": label, "frames": n,
        "mean_iter": float(its.mean()), "p99_iter": float(np.percentile(its, 99)),
        "max_iter": int(its.max()), "stall_rate": stalls / n,
        "max_pos_err": float(pe.max()), "mean_pos_err": float(pe.mean()),
    }


def main():
    out = {"arm_b": [], "arm_c": []}
    D0 = 5.0

    for beta in [0.9, 0.99, 0.999, 0.9999]:
        for alpha, aname in [(0.0, "coast"), (3.7e-4, "11561g")]:
            wl = Hyperbolic(D0, -abs(beta), alpha)
            for mode in ["extrap", "prevroot"]:
                r = run_frames(wl, D0, 300, mode,
                               f"b beta={beta} {aname} D={D0} {mode}")
                out["arm_b"].append(r)
                print(json.dumps(r), flush=True)

    for beta in [0.9, 0.999]:
        for dv in [1e-6, 1e-5, 1e-4]:
            for dtk, kname in [(0.05, "k20ps"), (0.5, "k2ps")]:
                wl = Kinked(D0, -abs(beta), dv, dtk,
                            2.5 * D0 / (1.0 - abs(beta)), 12.0, seed=42)
                r = run_frames(wl, D0, 2000, "extrap",
                               f"c beta={beta} dv={dv:g} {kname}")
                out["arm_c"].append(r)
                print(json.dumps(r), flush=True)

    with open(sys.argv[1] if len(sys.argv) > 1 else "gather-results.json", "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
