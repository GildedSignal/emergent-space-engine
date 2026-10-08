#!/usr/bin/env python3
"""Falsifier for representation.md §2 Observables: 'Each visible tube crosses the
observer's past light cone once; Newton's method finds the crossing, starting from
the previous frame's.'  Plus the view's temporal sampling ('one sample per pixel').

Scene (the game's signature): the player coasts toward a system at closing speed
beta; 32 emitters hold a ring formation R = 0.2 light-s at orbital speed beta_o.
Frame rate 60/s of observer PROPER time, 200 frames. The doc's sentence names no
frame; both readings solve for the SAME emission event (same physical scene, same
tube parameter t' = system-frame time):
  A) observer-frame reading: F written in observer-frame quantities
     (observer static; system streams at beta; emitter worldline is the boosted
     ring; tS = g(t'+b x')-g b D0, xS = g(x'+b t')-g D0).
  B) doll-frame reading: F written in the system frame (clean circle; observer
     streams).  Slope of F in t' is O(1) here.
  C) control fix: rate-extrapolated guess (arrival-map slope at the previous
     root, one stored number), then Newton in the doll frame.
Truth: bisection on the doll-frame equation (F strictly monotone: |v_emitter| < c).

Units: c = 1, light-seconds, seconds. float64. Machine: Linux x86, 8 vCPU, idle.
"""
import json
import numpy as np

R = 0.2
N_EM = 32
N_FRAMES = 200
DTAU = 1.0 / 60.0
NEWTON_CAP = 32
TOL0 = 1e-9
WRAP = lambda a: (a + np.pi) % (2 * np.pi) - np.pi

def run_config(beta, beta_o, D0):
    gam = 1.0 / np.sqrt(1.0 - beta * beta)
    om = beta_o / R
    T = 2 * np.pi * R / beta_o if beta_o > 0 else np.inf
    phi = np.linspace(0, 2 * np.pi, N_EM, endpoint=False)
    k_dop = np.sqrt((1 + beta) / (1 - beta))
    dt_e_per_frame = k_dop * DTAU

    def emitter_Sp(te):
        ang = om * te + phi
        return (R * np.cos(ang), R * np.sin(ang),
                -R * om * np.sin(ang), R * om * np.cos(ang))
    def obs_Sp(ta): return D0 - beta * ta
    def F_Sp(te, ta):
        x, y, _, _ = emitter_Sp(te)
        return ta - te - np.hypot(x - obs_Sp(ta), y)
    def dF_Sp(te, ta):
        x, y, vx, vy = emitter_Sp(te)
        dx = x - obs_Sp(ta)
        r = np.hypot(dx, y)
        return -1.0 - (dx * vx + y * vy) / r
    def F_S(tp, ta):
        x, y, _, _ = emitter_Sp(tp)
        tS = gam * (tp + beta * x) - gam * beta * D0
        xS = gam * (x + beta * tp) - gam * D0
        return ta - tS - np.hypot(xS, y)
    def dF_S(tp, ta):
        x, y, vx, vy = emitter_Sp(tp)
        tS = gam * (tp + beta * x) - gam * beta * D0
        xS = gam * (x + beta * tp) - gam * D0
        r = np.hypot(xS, y)
        return -(gam * (1.0 + beta * vx)) - (xS * gam * (vx + beta) + y * vy) / r

    ta_S = DTAU * np.arange(N_FRAMES)          # observer-frame arrival times
    ta_Sp = gam * ta_S                         # same events, system-frame times
    tol = max(TOL0, 4 * np.finfo(float).eps * max(abs(ta_Sp[-1]), D0))

    def bisect_doll(ta):
        d_c = abs(obs_Sp(ta))
        lo = np.full(N_EM, ta - (d_c + 3 * R))
        hi = np.full(N_EM, ta - max(d_c - 3 * R, 1e-6))
        for _ in range(4):
            bad = ~(F_Sp(lo, ta) > 0); lo = np.where(bad, lo - (ta - lo), lo)
            bad = ~(F_Sp(hi, ta) < 0); hi = np.where(bad, hi - (ta - hi), hi)
        for _ in range(90):
            mid = 0.5 * (lo + hi)
            go_lo = F_Sp(mid, ta) > 0
            lo = np.where(go_lo, mid, lo)
            hi = np.where(go_lo, hi, mid)
        return 0.5 * (lo + hi)

    truth0 = bisect_doll(ta_Sp[0])
    res, phases = {}, None
    for name in ("A_obs", "B_doll", "C_rate"):
        Ff, dFf = (F_S, dF_S) if name == "A_obs" else (F_Sp, dF_Sp)
        prev_root = truth0.copy()
        iters = np.zeros((N_FRAMES, N_EM)); fails = np.zeros((N_FRAMES, N_EM), bool)
        wrong = 0
        ph = np.zeros(N_FRAMES)
        for i in range(1, N_FRAMES):
            ta = ta_S[i] if name == "A_obs" else ta_Sp[i]
            if name == "C_rate":
                x, y, vx, vy = emitter_Sp(prev_root)
                dx = x - obs_Sp(ta_Sp[i - 1])
                r = np.hypot(dx, y)
                s_fam = (1.0 + beta * dx / r) / (1.0 + (dx * vx + y * vy) / r)
                t = prev_root + (ta_Sp[i] - ta_Sp[i - 1]) * s_fam
            else:
                t = prev_root.copy()
            conv = np.full(N_EM, NEWTON_CAP)
            for it in range(NEWTON_CAP):
                f = Ff(t, ta)
                ok = np.abs(f) <= tol
                conv = np.where(ok & (conv == NEWTON_CAP), it, conv)
                if np.all(conv < NEWTON_CAP):
                    break
                t = np.where(ok, t, t - f / dFf(t, ta))
            ok = np.abs(Ff(t, ta)) <= tol
            iters[i] = np.where(conv < NEWTON_CAP, conv, NEWTON_CAP)
            fails[i] = ~ok
            truth = bisect_doll(ta_Sp[i])
            wrong += int(np.sum(ok & (np.abs(t - truth) > 1e-6 * np.maximum(1.0, np.abs(truth)))))
            t = np.where(ok, t, truth)
            prev_root = t
            if name == "B_doll":
                ang = om * t + phi
                ph[i] = np.median(np.arctan2(np.sin(ang), np.cos(ang)))
        if name == "B_doll" and beta_o > 0:
            dph = WRAP(np.diff(ph))
            true_rate = om * dt_e_per_frame
            res["alias"] = dict(
                dphi_per_frame=float(np.median(dph)),
                true_dphi_per_frame=float(WRAP(true_rate)),
                frac_retrograde=float(np.mean(dph < 0)),
                frac_frozen=float(np.mean(np.abs(dph) < 0.1 * np.abs(WRAP(true_rate)) + 1e-12)),
                orbits_per_frame=float(dt_e_per_frame / T),
            )
        res[name] = dict(
            mean_iters=float(np.mean(iters[1:])),
            p99_iters=float(np.percentile(iters[1:], 99)),
            fail=float(np.mean(fails[1:])),
            wrong_roots=wrong,
        )
    return dict(beta=beta, gamma=gam, beta_o=beta_o, D0=D0, T_orb=T,
                dt_e_per_frame=dt_e_per_frame, **res)

def main():
    configs = [(b, bo, 100.0) for b in (0.0, 0.9, 0.999, 0.9999)
               for bo in (0.0, 0.01, 0.05, 0.3)]
    gam = 2e6
    configs += [(np.sqrt(1 - 1 / gam**2), bo, 2e7) for bo in (0.01, 0.05, 0.3)]
    # aliasing sweep near the wagon-wheel boundary for beta_o = 0.3 (T = 4.19 s)
    for g in (125.0, 245.0, 250.0, 255.0, 300.0):
        configs.append((np.sqrt(1 - 1 / g**2), 0.3, 100.0))
    out = []
    for beta, beta_o, D0 in configs:
        r = run_config(beta, beta_o, D0)
        al = r.get("alias")
        als = (f"dphi={al['dphi_per_frame']:+.3f} true={al['true_dphi_per_frame']:+.3f} "
               f"retro={al['frac_retrograde']*100:4.0f}% frozen={al['frac_frozen']*100:4.0f}%"
               ) if al else "dphi=n/a"
        print(f"g={r['gamma']:8.3g} b_o={r['beta_o']:.2f} "
              f"orb/fr={r.get('alias', {}).get('orbits_per_frame', 0):8.3g} | "
              f"A it={r['A_obs']['mean_iters']:5.1f} fail={r['A_obs']['fail']*100:4.1f}% "
              f"wrong={r['A_obs']['wrong_roots']:4d} | "
              f"B it={r['B_doll']['mean_iters']:5.1f} fail={r['B_doll']['fail']*100:4.1f}% "
              f"wrong={r['B_doll']['wrong_roots']:4d} | "
              f"C it={r['C_rate']['mean_iters']:5.1f} fail={r['C_rate']['fail']*100:4.1f}% | "
              f"{als}", flush=True)
        out.append(r)
    with open("gather_results.json", "w") as fh:
        json.dump(out, fh, indent=1)

if __name__ == "__main__":
    main()
