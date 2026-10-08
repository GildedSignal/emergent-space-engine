#!/usr/bin/env python3
"""Independent check of r6 (view at gamma). No code shared with r6_run.py.

Differences from the author's implementation, by design:
  - Truth roots: fixed-point contraction t' <- ta - |x_e(t') - x_o(ta)| (rate <= beta_o < 1),
    not bisection; convergence 1e-13 s doll-time, 200 iterations cap.
  - Solver replica: warm-started Newton written from the rung prose, own tolerance 1e-9 s.
  - Truth fluence: the author's closed form is validated three ways before being trusted:
      (a) brute dense midpoint quadrature (8192 nodes/window) on up to 300 sampled windows
          per case with orbits/frame <= 20;
      (b) exact periodicity: b and the k-weight are 2pi-periodic in the emission phase, so
          for high-k windows the closed form on the full window must equal dense quadrature
          on the TRIMMED window (span < 2pi) -- 64 sampled windows per high-k case;
      (c) the n ~ (-1, 0) approximation: dense quadrature with the exact line-of-sight
          n(t') and the linear arrival map, vs the closed form, on 40 windows per case at
          gamma <= 70.8 (the smallest D0, where R/D0 is worst).
  - Metrics recomputed from these; written as metrics-check.json. verdict.py compares
    pass/fail OUTCOMES, not values.

Usage: python3 r6_check.py            -> metrics-check.json, check-validation.json, log lines
"""
import json

import numpy as np

R = 0.2
N_EM = 32
N_FRAMES = 200
DTAU = 1.0 / 60.0
NEWTON_CAP = 32
PI = np.pi
WRAP = lambda a: (a + PI) % (2 * PI) - PI
PHI = np.linspace(0, 2 * PI, N_EM, endpoint=False)
CONFIGS = {"kavg": ("doll", "local"), "exact-exposure": ("truth", "local"),
           "instant": ("doll", "instant"), "raw-obs": ("raw", "local")}

OM = None
D0 = None


def ring_all(te):
    """All 32 emitters; te: (N_EM,) or (N_EM, Q)."""
    ang = OM * te + (PHI if np.ndim(te) == 1 else PHI[:, None])
    return (R * np.cos(ang), R * np.sin(ang), -R * OM * np.sin(ang), R * OM * np.cos(ang))


def ring_one(te, j):
    """Emitter j at doll times te (any shape)."""
    ang = OM * te + PHI[j]
    return R * np.cos(ang), R * np.sin(ang), -R * OM * np.sin(ang), R * OM * np.cos(ang)


def solve_case(beta, beta_o):
    gam = 1.0 / np.sqrt(1 - beta * beta)
    ta_Sp = gam * DTAU * np.arange(N_FRAMES)
    # truth roots by contraction: t' <- ta - dist(t'; ta), rate |n.v_e| <= beta_o < 1
    truth = np.zeros((N_FRAMES, N_EM))
    for i in range(N_FRAMES):
        ta = ta_Sp[i]
        t = np.full(N_EM, ta - (D0 - beta * ta))
        for _ in range(200):
            x, y, _, _ = ring_all(t)
            tn = ta - np.hypot(x - (D0 - beta * ta), y)
            step = np.max(np.abs(tn - t))
            t = tn
            if step < 1e-13:
                break
        truth[i] = t
    # warm-started Newton, doll-frame and raw observer-frame readings
    out = {}
    for name in ("doll", "raw"):
        prev = truth[0].copy()
        roots = np.zeros_like(truth)
        iters, fails, wrong = [], 0, 0
        for i in range(1, N_FRAMES):
            ta = ta_Sp[i] if name == "doll" else ta_Sp[i] / gam
            tol = max(1e-9, 4 * np.finfo(float).eps * (abs(ta) + D0))
            t = prev.copy()
            used = NEWTON_CAP
            for it in range(NEWTON_CAP):
                x, y, vx, vy = ring_all(t)
                if name == "doll":
                    dx = x - (D0 - beta * ta)
                    F = ta - t - np.hypot(dx, y)
                    dF = -1.0 - (dx * vx + y * vy) / np.hypot(dx, y)
                else:
                    tS = gam * (t + beta * x) - gam * beta * D0
                    xS = gam * (x + beta * t) - gam * D0
                    F = ta - tS - np.hypot(xS, y)
                    dF = -(gam * (1.0 + beta * vx)) - (xS * gam * (vx + beta) + y * vy) / np.hypot(xS, y)
                ok = np.abs(F) <= tol
                if np.all(ok):
                    used = it
                    break
                t = np.where(ok, t, t - F / dF)
            x, y, _, _ = ring_all(t)
            if name == "doll":
                F = ta - t - np.hypot(x - (D0 - beta * ta), y)
            else:
                tS = gam * (t + beta * x) - gam * beta * D0
                xS = gam * (x + beta * t) - gam * D0
                F = ta - tS - np.hypot(xS, y)
            ok = np.abs(F) <= tol
            fails += int(np.sum(~ok))
            wrong += int(np.sum(ok & (np.abs(t - truth[i]) > 1e-6 * np.maximum(1.0, np.abs(truth[i])))))
            t = np.where(ok, t, truth[i])
            roots[i] = t
            prev = t
            iters.append(used)
        roots[0] = truth[0]
        out[name] = dict(roots=roots, iters=float(np.mean(iters)),
                         fail=float(fails / ((N_FRAMES - 1) * N_EM)), wrong=wrong)
    out["truth"] = dict(roots=truth, iters=0.0, fail=0.0, wrong=0)
    return out, ta_Sp


def fluence_closed(truth, beta_o):
    th1 = OM * truth[:-1] + PHI[None, :]
    th2 = OM * truth[1:] + PHI[None, :]
    Th = th2 - th1
    s1, s2, c1, c2 = np.sin(th1), np.sin(th2), np.cos(th1), np.cos(th2)
    num = Th + (s2 - s1) + beta_o * ((c1 - c2) + 0.5 * (s2 * s2 - s1 * s1))
    den = Th + beta_o * (c1 - c2)
    out = np.full((N_FRAMES, N_EM), np.nan)
    out[1:] = num / den
    return out


def quad_fluence(t1, t2, j, beta_o, nodes=8192, exact_n=False, beta=0.0, ta1=0.0, ta2=1.0):
    """Dense midpoint quadrature of int b k dt' / int k dt' for one emitter's window.

    Default: the closed form's own weight k = 1 + beta_o sin(theta) (validations a, b).
    exact_n: k(t') = (1 + n.v_e)/(1 + n.v_o) with the true line of sight and the linear
    arrival map t_a(t') between the window's (ta1, ta2) (validation c).
    """
    u = (np.arange(nodes) + 0.5) / nodes
    te = t1 + (t2 - t1) * u
    th = OM * te + PHI[j]
    x, y, vx, vy = ring_one(te, j)
    if exact_n:
        ta = ta1 + (ta2 - ta1) * u
        xo = D0 - beta * ta
        dx, dy = x - xo, y
        r = np.hypot(dx, dy)
        k = (1.0 + (dx * vx + dy * vy) / r) / (1.0 - beta * dx / r)
    else:
        k = 1.0 + beta_o * np.sin(th)
    b = 1.0 + np.cos(th)
    return float(np.sum(b * k) / np.sum(k))


def main():
    gs = (1.0, 2.24, 22.4, 70.7, 125.0, 250.0, 255.0, 2e6)
    ladder = [(np.sqrt(1 - 1 / g**2), bo) for g in gs for bo in (0.05, 0.3)]
    acc = {c: dict(bright=[], wrong=0, fail=[], iters=[], pb=[]) for c in CONFIGS}
    val_report = []
    for beta, beta_o in ladder:
        global OM, D0
        gam = 1.0 / np.sqrt(1 - beta * beta)
        OM = beta_o / R
        D0 = 2.1 * gam * N_FRAMES * DTAU + 100.0
        T = 2 * PI * R / beta_o
        solved, ta_Sp = solve_case(beta, beta_o)
        tr = solved["truth"]["roots"]
        fl = fluence_closed(tr, beta_o)

        orb = (tr[1:] - tr[:-1]) / T
        pairs = lambda mask, n: (lambda idx: idx[np.linspace(0, len(idx) - 1,
                             min(len(idx), n)).astype(int)] if len(idx) else [])(np.argwhere(mask))
        # (a) dense quadrature on sampled low-k windows
        errs_a = [abs(quad_fluence(tr[i, j], tr[i + 1, j], j, beta_o) - fl[i + 1, j])
                  for i, j in pairs(orb <= 20.0, 300)]
        # (b) full-window dense quadrature on sampled high-k windows (the integrand has
        # harmonics 0..2 only, so >= 16 uniform nodes per orbit is machine-exact)
        errs_b = []
        for i, j in pairs(orb > 20.0, 8):
            n = int(min(max(16 * orb[i, j], 2048), 4_000_000))
            errs_b.append(abs(quad_fluence(tr[i, j], tr[i + 1, j], j, beta_o, nodes=n) - fl[i + 1, j]))
        # (c) exact line of sight at the smallest D0
        errs_c = []
        if gam <= 70.8:
            for i, j in pairs(np.ones_like(orb, bool), 40):
                qv = quad_fluence(tr[i, j], tr[i + 1, j], j, beta_o, exact_n=True,
                                  beta=beta, ta1=ta_Sp[i], ta2=ta_Sp[i + 1])
                errs_c.append(abs(qv - fl[i + 1, j]))
        val_report.append(dict(gamma=gam, beta_o=beta_o, D0=D0,
                               quad_lowk_max=max(errs_a) if errs_a else None,
                               quad_highk_max=max(errs_b) if errs_b else None,
                               exact_n_max=max(errs_c) if errs_c else None))

        dt_win = tr[2:] - tr[1:-1]
        below = dt_win / T < 0.45
        dphi_true = WRAP(OM * dt_win)
        for name, (slv, sprite) in CONFIGS.items():
            r = solved[slv]
            roots = r["roots"]
            acc[name]["wrong"] += r["wrong"]
            acc[name]["fail"].append(r["fail"])
            acc[name]["iters"].append(r["iters"])
            dt = np.diff(roots, axis=0)
            thm = OM * 0.5 * (roots[1:] + roots[:-1]) + PHI[None, :]
            ths = OM * roots[1:] + PHI[None, :]
            if sprite == "instant":
                render = 1.0 + np.cos(ths)
            else:
                x = OM * dt / 2.0
                render = 1.0 + np.sin(x) / x * np.cos(thm)
            acc[name]["bright"].append(np.abs(render - fl[1:]).ravel())
            thv = ths if sprite == "instant" else thm
            dth = WRAP(thv[1:] - thv[:-1])
            acc[name]["pb"].append(np.abs(WRAP(dth - dphi_true))[below].ravel())
    out = {}
    for name in CONFIGS:
        b = np.concatenate(acc[name]["bright"])
        pb = np.concatenate(acc[name]["pb"])
        out[name] = dict(iters_mean=float(np.mean(acc[name]["iters"])),
                         solver_fail_frac=float(np.mean(acc[name]["fail"])),
                         solver_wrong_roots=int(acc[name]["wrong"]),
                         bright_p99=float(np.percentile(b, 99)),
                         phase_below_p99=float(np.percentile(pb, 99)))
    with open("metrics-check.json", "w") as fh:
        json.dump(out, fh, indent=1)
    with open("check-validation.json", "w") as fh:
        json.dump(val_report, fh, indent=1)
    for c, v in out.items():
        print(f"chk {c:14s} it={v['iters_mean']:5.1f} fail={v['solver_fail_frac']*100:5.2f}% "
              f"wrong={v['solver_wrong_roots']:6d} bright_p99={v['bright_p99']:.4f} "
              f"phase_below={v['phase_below_p99']:.2e}", flush=True)
    vmax = {k: max((r[k] for r in val_report if r[k] is not None), default=None)
            for k in ("quad_lowk_max", "quad_highk_max", "exact_n_max")}
    print("validation maxima over cases:", vmax)


if __name__ == "__main__":
    main()
