#!/usr/bin/env python3
"""r6 (view at gamma): the checker's named experiment for 20261008-1947-redteam-efb2.

Question: at closing gamma in {1 ... 2e6}, does the view's "one sample per pixel"
(representation.md s2) render what the observer receives from a periodic emitter,
and does the k-averaged sprite law (the dossier's proposed fix, in the doc's own
"type x log k table" form) render it instead?  Flyby-free scenes (D0 scaled with
gamma so the observer never passes the system: every frame approaches), per-emitter
circular statistics, truth = the k-weighted average of the emission over the light
actually received during each frame (what a 1/60 s exposure records), with k the
LOCAL arrival slope dt_a/dt_e from the crossing geometry, never a constant.

Scene (doll/system frame S', c = 1, light-seconds): 32 emitters on a ring
R = 0.2 ls at orbital speed beta_o; each is a lighthouse b_j(t') = 1 + cos(w t' + phi_j).
Observer coasts toward the system at closing beta; frames are 1/60 s of observer
proper time; 200 frames; D0 = 2.1*gamma*N*DTAU + 100 ls.

Solvers (the design sentence, both readings, same emission event):
  doll : Newton on F' = ta - te - |x_e(te) - x_o(ta)| in the doll frame, warm-started
         from the previous frame's root (the doc's mechanism).
  raw  : Newton on the same event written in raw observer-frame magnitudes
         (boosted emitter worldline), warm-started the same way.
Truth roots: bisection on the doll-frame F' (strictly monotone: |v_e| < c).

Render laws (per frame i >= 1, emitter j; window = the received interval
[t'_{i-1}, t'_i] of that emitter):
  instant    : 1 + cos(w t'_i + phi_j)                  -- one sample per pixel
  kavg       : 1 + sinc(x) cos(w (t'_i + t'_{i-1})/2 + phi_j),  x = w (t'_i - t'_{i-1})/2
               (sinc(x) = sin(x)/x; the memo sprite keyed by log k; k enters only
               through the two crossings the engine already solves)
  kavg-global: same sprite but x = w k_glob DTAU / 2 with k_glob = sqrt((1+b)/(1-b))
               (the approaching-only constant, not local geometry)
  raw-obs    : kavg rendered on the raw-solver roots (number-form control)
Truth brightness: fluence = int b k dt' / int k dt' over the TRUE window, midpoint
rule, 2048 nodes; k(t') = (1 + n.v_e)/(1 + n.v_o) with n from the linear arrival map.

Usage: python3 r6_run.py [pilot]   -> metrics.json (+ r6_results.json, log lines)
"""
import json
import sys

import numpy as np

R = 0.2
N_EM = 32
N_FRAMES = 200
DTAU = 1.0 / 60.0
NEWTON_CAP = 32
TOL0 = 1e-9
WRAP = lambda a: (a + np.pi) % (2 * np.pi) - np.pi
PI = np.pi


def emitter(te):
    """Ring emitters in the doll frame: positions and velocities at system time te.
    te: (N_EM,) or (N_EM, Q)."""
    ang = OM * te + (PHI if te.ndim == 1 else PHI[:, None])
    x = R * np.cos(ang)
    y = R * np.sin(ang)
    vx = -R * OM * np.sin(ang)
    vy = R * OM * np.cos(ang)
    return x, y, vx, vy


def run_case(beta, beta_o, truth_roots, ta_Sp):
    """One (beta, beta_o) case. Returns per-solver arrays and per-render arrays."""
    gam = 1.0 / np.sqrt(1.0 - beta * beta)
    T = 2 * PI * R / beta_o
    tol = max(TOL0, 4 * np.finfo(float).eps * max(abs(ta_Sp[-1]), D0))

    def obs(ta):
        return D0 - beta * ta

    def F_doll(te, ta):
        x, y, _, _ = emitter(te)
        return ta - te - np.hypot(x - obs(ta), y)

    def dF_doll(te, ta):
        x, y, vx, vy = emitter(te)
        dx = x - obs(ta)
        return -1.0 - (dx * vx + y * vy) / np.hypot(dx, y)

    def F_raw(tp, ta):
        """Same emission event, raw observer-frame magnitudes (boosted worldline)."""
        x, y, _, _ = emitter(tp)
        tS = gam * (tp + beta * x) - gam * beta * D0
        xS = gam * (x + beta * tp) - gam * D0
        return ta - tS - np.hypot(xS, y)

    def dF_raw(tp, ta):
        x, y, vx, vy = emitter(tp)
        xS = gam * (x + beta * tp) - gam * D0
        return -(gam * (1.0 + beta * vx)) - (xS * gam * (vx + beta) + y * vy) / np.hypot(xS, y)

    # ---- solvers: warm-started Newton, doll and raw; truth roots given (bisection) ----
    solved = {}
    for name, Ff, dFf in (("doll", F_doll, dF_doll), ("raw", F_raw, dF_raw)):
        prev = truth_roots[0].copy()
        roots = np.zeros_like(truth_roots)
        iters = np.zeros(N_FRAMES)
        fails = np.zeros(N_FRAMES)
        wrong = 0
        for i in range(1, N_FRAMES):
            ta = ta_Sp[i] if name == "doll" else ta_Sp[i] / gam  # raw solves in tau
            t = prev.copy()
            conv = np.full(N_EM, NEWTON_CAP)
            for it in range(NEWTON_CAP):
                f = Ff(t, ta)
                ok = np.abs(f) <= tol
                conv = np.where(ok & (conv == NEWTON_CAP), it, conv)
                if np.all(conv < NEWTON_CAP):
                    break
                t = np.where(ok, t, t - f / dFf(t, ta))
            ok = np.abs(Ff(t, ta)) <= tol
            iters[i] = np.mean(np.where(conv < NEWTON_CAP, conv, NEWTON_CAP))
            fails[i] = np.mean(~ok)
            wrong += int(np.sum(ok & (np.abs(t - truth_roots[i]) > 1e-6 * np.maximum(1.0, np.abs(truth_roots[i])))))
            t = np.where(ok, t, truth_roots[i])
            roots[i] = t
            prev = t
        roots[0] = truth_roots[0]
        solved[name] = dict(roots=roots, iters=float(np.mean(iters[1:])),
                            fail=float(np.mean(fails[1:])), wrong=wrong)
    return solved, T, tol


def fluence_truth(truth_roots, beta_o):
    """Received (exposure) average of b over each true window, per (frame i >= 1, em).

    A frame's exposure records the light received during it: the k-weighted average
    of the emission over the window, k = dt_a/dt_e = (1 + n.v_e)/(1 + n.v_o).  To
    leading order in R/D0 the line of sight is n = (-1, 0) through the window, so
    k ~ kbar * (1 + beta_o sin(theta)) and the integral is closed-form in the edge
    phases (kbar cancels in the ratio); neglected terms are O(R/D0) <= 2e-3.
    Independent of every solver; no quadrature (which would alias at high k).
    """
    th1 = OM * truth_roots[:-1] + PHI[None, :]
    th2 = OM * truth_roots[1:] + PHI[None, :]
    Th = th2 - th1
    s1, s2 = np.sin(th1), np.sin(th2)
    c1, c2 = np.cos(th1), np.cos(th2)
    num = Th + (s2 - s1) + beta_o * ((c1 - c2) + 0.5 * (s2 * s2 - s1 * s1))
    den = Th + beta_o * (c1 - c2)
    out = np.full((N_FRAMES, N_EM), np.nan)
    out[1:] = num / den
    return out


PHI = None
OM = None
D0 = None


def metrics_for(configs, ladder):
    """configs: dict name->render spec; ladder: list of (beta, beta_o). Returns metrics dict."""
    global PHI, OM, D0
    acc = {c: dict(bright=[], phase_below=[], wrong=0, fail=[], iters=[], frozen_above=[],
                   true_above=[]) for c in configs}
    detail = []
    for beta, beta_o in ladder:
        gam = 1.0 / np.sqrt(1.0 - beta * beta)
        OM = beta_o / R
        PHI = np.linspace(0, 2 * PI, N_EM, endpoint=False)
        D0 = 2.1 * gam * N_FRAMES * DTAU + 100.0
        ta_S = DTAU * np.arange(N_FRAMES)
        ta_Sp = gam * ta_S
        T = 2 * PI * R / beta_o

        # truth roots: bisection in the doll frame (monotone F)
        truth = np.zeros((N_FRAMES, N_EM))
        for i in range(N_FRAMES):
            ta = ta_Sp[i]
            d_c = abs(D0 - beta * ta)
            lo = np.full(N_EM, ta - (d_c + 3 * R))
            hi = np.full(N_EM, ta - max(d_c - 3 * R, 1e-6))

            def Fs(te):
                x, y, _, _ = emitter(np.full(N_EM, te) if np.isscalar(te) else te)
                return ta - te - np.hypot(x - (D0 - beta * ta), y)

            for _ in range(4):
                bad = ~(Fs(lo) > 0); lo = np.where(bad, lo - (ta - lo), lo)
                bad = ~(Fs(hi) < 0); hi = np.where(bad, hi - (ta - hi), hi)
            for _ in range(90):
                mid = 0.5 * (lo + hi)
                go_lo = Fs(mid) > 0
                lo, hi = np.where(go_lo, mid, lo), np.where(go_lo, hi, mid)
            truth[i] = 0.5 * (lo + hi)

        solved, _, _ = run_case(beta, beta_o, truth, ta_Sp)
        solved["truth"] = dict(roots=truth, iters=0.0, fail=0.0, wrong=0)
        fl = fluence_truth(truth, beta_o)

        dt_win = truth[2:] - truth[1:-1]                # window w_i = [t'_{i-1}, t'_i], i >= 2
        orb_fr = dt_win / T
        below = orb_fr < 0.45
        dphi_true = WRAP(OM * dt_win)
        k_glob = np.sqrt((1 + beta) / (1 - beta))

        for name, (use_solver, sprite) in configs.items():
            roots = solved[use_solver]["roots"]
            r = solved[use_solver]
            acc[name]["wrong"] += r["wrong"]
            acc[name]["fail"].append(r["fail"])
            acc[name]["iters"].append(r["iters"])
            dt = np.diff(roots, axis=0)
            x_loc = OM * dt / 2.0
            x_glob = OM * k_glob * DTAU / 2.0
            mid = 0.5 * (roots[1:] + roots[:-1])
            th_mid = OM * mid + PHI[None, :]
            th_smp = OM * roots[1:] + PHI[None, :]
            if sprite == "instant":
                render = 1.0 + np.cos(th_smp)
            else:
                x = x_glob if sprite == "global" else x_loc
                render = 1.0 + np.sinc(x / PI) * np.cos(th_mid)   # np.sinc(v)=sin(pi v)/(pi v)
            err = np.abs(render - fl[1:])
            acc[name]["bright"].append(err.ravel())
            # per-emitter phase honesty below Nyquist: advance at frame i vs window w_i
            th_var = th_smp if sprite == "instant" else th_mid
            dth = WRAP(th_var[1:] - th_var[:-1])
            pe = np.abs(WRAP(dth - dphi_true))[below]
            acc[name]["phase_below"].append(pe.ravel())
            # frozen diagnostic above the wagon-wheel boundary (per emitter, local truth)
            above = orb_fr >= 0.5
            if above.any():
                froz = np.abs(dth) < 0.05
                acc[name]["frozen_above"].append(froz[above].ravel())
                acc[name]["true_above"].append(dphi_true[above].ravel())
            detail.append(dict(gamma=gam, beta_o=beta_o, D0=D0, config=name,
                               bright_p99=float(np.percentile(err, 99)),
                               bright_max=float(err.max()),
                               orb_per_frame_med=float(np.median(orb_fr)),
                               frozen_frac_above=float(np.mean(acc[name]["frozen_above"][-1]))
                               if above.any() else None))
    out = {}
    for name in configs:
        b = np.concatenate(acc[name]["bright"])
        pb = np.concatenate(acc[name]["phase_below"])
        fa = np.concatenate(acc[name]["frozen_above"]) if acc[name]["frozen_above"] else np.array([])
        out[name] = dict(
            iters_mean=float(np.mean(acc[name]["iters"])),
            solver_fail_frac=float(np.mean(acc[name]["fail"])),
            solver_wrong_roots=int(acc[name]["wrong"]),
            bright_p99=float(np.percentile(b, 99)),
            bright_max=float(b.max()),
            phase_below_p99=(float(np.percentile(pb, 99)) if pb.size else -1.0),
            frozen_frac_above=float(np.mean(fa)) if fa.size else None,
        )
    return out, detail


CONFIGS = {  # formal: kavg candidate, exact-exposure positive, instant/raw-obs negative
    "kavg": ("doll", "local"),
    "exact-exposure": ("truth", "local"),
    "instant": ("doll", "instant"),
    "raw-obs": ("raw", "local"),
    "kavg-global": ("doll", "global"),  # diagnostic only: not in the rung's configs block
}


def main():
    pilot = len(sys.argv) > 1 and sys.argv[1] == "pilot"
    if pilot:
        ladder = [(np.sqrt(1 - 1 / g**2), 0.3) for g in (70.7, 125.0, 250.0)] + \
                 [(np.sqrt(1 - 1 / 4e12), 0.05), (0.0, 0.3)]
    else:
        gs = (1.0, 2.24, 22.4, 70.7, 125.0, 250.0, 255.0, 2e6)
        ladder = [(np.sqrt(1 - 1 / g**2), bo) for g in gs for bo in (0.05, 0.3)]
    m, detail = metrics_for(CONFIGS, ladder)
    with open("metrics-pilot.json" if pilot else "metrics.json", "w") as fh:
        json.dump(m, fh, indent=1)
    with open("r6_results.json", "w") as fh:
        json.dump(dict(metrics=m, detail=detail), fh, indent=1)
    for c, v in m.items():
        print(f"{c:12s} iters={v['iters_mean']:5.1f} fail={v['solver_fail_frac']*100:4.1f}% "
              f"wrong={v['solver_wrong_roots']:5d} bright_p99={v['bright_p99']:.3f} "
              f"max={v['bright_max']:.3f} phase_below_p99={v['phase_below_p99']:.2e} "
              f"frozen_above={v['frozen_frac_above']}", flush=True)


if __name__ == "__main__":
    main()
