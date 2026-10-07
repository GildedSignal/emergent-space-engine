#!/usr/bin/env python3
"""Analysis for the second-author run: one brute-force truth, many certificate policies.

Policies against the SAME truth list (brute-force minima of the precessing pair):
  frozen  : single window cut at t=0 (the crate's static pom) — the author's run_case.
  theta   : piecewise-frozen; window w cut at t_w, elements frozen there, staleness
            |dOm|*(t-t_w) <= theta. A window cut at t_w is the pair P(delta) with the
            t=0 mean anomalies, rigidly advanced by t_w (exact translation), so its
            proposals are P(delta)'s frozen minima shifted by t_w — no extra brute force.
theta = |dOm|*Psyn is one refresh per synodic passage (the co-precessing O(1)-update limit).
Kick cadence K and theta are one parameter: a re-cut every K = theta/|dOm| leaves staleness
<= theta. The crossover theta* measures D_miss; K* = theta*/|dOm| is the shadowing cadence.
"""
import json
import math
import os

import numpy as np

from cert import TAU, body, fit_exp, machine

HERE = os.path.dirname(os.path.abspath(__file__))
TR = os.path.join(HERE, "truth")

RHO = 0.004
SAFETY = 1.2
MATCH = 0.4
nn = lambda a: a ** -1.5

G2 = (body(1.0, 0.30, 0.3, nn(1.0)), body(0.85, 0.40, 1.2, nn(0.85)))
G6 = (body(1.0, 0.30, 0.3, nn(1.0)), body(0.8, 0.30, 1.03, nn(0.8)))
G4N = (body(1.0, 0.30, 0.3, nn(1.0)), body(0.8, 0.30, 1.00, nn(0.8)))

PSYN_G6 = TAU / abs(G6[0]["n"] - G6[1]["n"])
PSYN_G2 = TAU / abs(G2[0]["n"] - G2[1]["n"])
PSYN_G4 = TAU / abs(G4N[0]["n"] - G4N[1]["n"])
P0 = TAU / G6[0]["n"]  # body-0 orbit = 2pi time units

OM_SWEEP = 3e-3          # rate for the theta-sweeps (G6 and G2)
D0 = 0.05                # staleness grid step (rad of differential rotation)
SUB4 = [0, 3, 6, 9]
THETAS = [(1, 0.05), (2, 0.1), (4, 0.2), (9, 0.45), (18, 0.9), (None, None)]  # (m, theta)


def load(key):
    with open(os.path.join(TR, key + ".json")) as f:
        return [(t, d) for (t, d) in json.load(f)["mins"]]


def eval_policy(true_m, windows, psyn):
    """windows: list of (t0, t1, [(t,d)]). MISS/waste as in the author's run_case."""
    events = [(t, d) for (t, d) in true_m if d < RHO]
    misses, first, missed = 0, None, []
    for (t, d) in events:
        w = next(((t0, t1, p) for (t0, t1, p) in windows if t0 <= t < t1), None)
        ok = w is not None and any(abs(tp - t) < MATCH * psyn for (tp, _) in w[2])
        if not ok:
            misses += 1
            missed.append((t, d))
            first = t if first is None else min(first, t)
    waste = 0
    nprop = 0
    for (_, _, props) in windows:
        for (tp, _) in props:
            nprop += 1
            if not any(d < RHO and abs(t - tp) < MATCH * psyn for (t, d) in events):
                waste += 1
    return dict(misses=misses, first=first, missed=missed[:6], waste=waste, props=nprop,
                n_events=len(events))


def frozen_windows(froz, T):
    props = [(t, d) for (t, d) in froz if d < SAFETY * RHO]
    return [(0.0, T, props)]


def theta_windows(plists, T, m, om, dstep=D0):
    """plists[j] = frozen minima at delta=j*dstep (j=0 is the frozen list). Windows every m
    steps; window w is cut at t_w = w*m*dstep/om, staleness <= m*dstep."""
    step = dstep / om
    wins = []
    w = 0
    while w * m * step < T:
        t0 = w * m * step
        j = min(w * m, len(plists) - 1)
        t1 = min((w + 1) * m * step, T) if j == w * m else T
        props = [(t0 + tau, d) for (tau, d) in plists[j]
                 if d < SAFETY * RHO and 0 <= tau and t0 + tau < t1]
        wins.append((t0, t1, props))
        w += 1
    return wins


def linfit(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    s, c = np.polyfit(x, y, 1)
    return dict(slope=round(float(s), 4), intercept=round(float(c), 2), n=len(x))


def main():
    out = dict(machine=machine(), rho=RHO, psyn_g6=round(PSYN_G6, 3), psyn_g2=round(PSYN_G2, 3))
    res = {}

    # ---------- control C0: instrument equivalence with the author's A2 at om=1e-3 ----------
    a2 = []
    for k in range(12):
        a2.append(eval_policy(load(f"g6r1_p{k}"),
                              frozen_windows(load(f"g6f_p{k}"), 1500.0), PSYN_G6))
    tot = dict(misses=sum(r["misses"] for r in a2), waste=sum(r["waste"] for r in a2),
               props=sum(r["props"] for r in a2),
               earliest=min((r["first"] for r in a2 if r["first"] is not None), default=None))
    res["C0_equivalence"] = dict(total=tot,
                                 ok=(tot["misses"] == 1 and tot["waste"] == 27
                                     and tot["props"] == 27
                                     and tot["earliest"] == 1458.6059965793488))
    print("C0 G6 frozen @1e-3 (author: m=1 w=27 p=27 e=1458.6059965793488):", tot,
          "ok=", res["C0_equivalence"]["ok"], flush=True)

    # ---------- control C1: kepler structural baseline (zero drift) ----------
    base = {}
    for g, psyn in (("g6", PSYN_G6), ("g2", PSYN_G2)):
        ks = range(12) if g == "g6" else SUB4
        rows = [eval_policy(load(f"{g}f_p{k}"),
                            frozen_windows(load(f"{g}f_p{k}"), 1500.0), psyn) for k in ks]
        base[g] = dict(misses=sum(r["misses"] for r in rows),
                       waste=sum(r["waste"] for r in rows),
                       props=sum(r["props"] for r in rows))
    res["C1_kepler_baseline"] = base
    print("C1 kepler baseline (frozen vs itself):", base, flush=True)

    # ---------- control C2: rigid rotation on G2 ----------
    froz = load("g2f_p0")
    true = load("g2rig_p0")
    r = eval_policy(true, frozen_windows(froz, 1500.0), PSYN_G2)
    m0t = min(d for (_, d) in true)
    m0f = min(d for (_, d) in froz)
    res["C2_rigid_G2"] = dict(misses=r["misses"], waste=r["waste"], m0_true=m0t,
                              m0_frozen=m0f, ok=(r["misses"] == 0 and r["waste"] == 0
                                                 and abs(m0t - m0f) < 1e-6))
    print("C2 rigid G2:", res["C2_rigid_G2"], flush=True)

    # ---------- E1: G6 first-miss scaling over rates ----------
    ens = []
    for omc in (1, 2, 3, 5, 10):
        om = omc * 1e-3
        rows = [eval_policy(load(f"g6r{omc}_p{k}"),
                            frozen_windows(load(f"g6f_p{k}"), 1500.0), PSYN_G6)
                for k in range(12)]
        fm = [r["first"] for r in rows if r["first"] is not None]
        ens.append(dict(om=om, misses=sum(r["misses"] for r in rows), n_ph_missing=len(fm),
                        first_times=fm, waste=sum(r["waste"] for r in rows),
                        earliest=min(fm) if fm else None,
                        median=sorted(fm)[len(fm) // 2] if fm else None,
                        D_earliest=round(om * min(fm), 4) if fm else None))
        print(f"E1 G6 om={om:.4g}: misses={ens[-1]['misses']} nph={len(fm)} "
              f"earliest={ens[-1]['earliest']} median={ens[-1]['median']} "
              f"D=om*earliest={ens[-1]['D_earliest']}", flush=True)
    okr = [e for e in ens if e["n_ph_missing"] >= 3]
    res["E1_scaling_G6"] = dict(
        ensemble=ens, n_rates_with_misses=len(okr),
        exp_earliest=fit_exp([e["om"] for e in okr], [e["earliest"] for e in okr]),
        exp_median=fit_exp([e["om"] for e in okr], [e["median"] for e in okr]))
    print("E1 fits:", res["E1_scaling_G6"]["exp_earliest"],
          res["E1_scaling_G6"]["exp_median"], flush=True)

    # ---------- E2: G4n safety-vs-realization split ----------
    pi_, pj_ = (b["a"] * (1 - b["e"] ** 2) for b in G4N)
    Vi, Vj = G4N[0]["e"] / pi_, G4N[1]["e"] / pj_
    dU = abs(1 / pi_ - 1 / pj_)
    dstar = math.acos((Vi * Vi + Vj * Vj - dU * dU) / (2 * Vi * Vj))
    dw0 = G4N[1]["pom"] - G4N[0]["pom"]
    travel_far = dw0 + dstar
    travel_near = dstar - dw0
    rows = []
    for omc in (1, 2, 3, 5):
        om = omc * 1e-3
        for k in range(6):
            true = load(f"g4r{omc}_p{k}")
            fb = next((t for (t, d) in true if d < RHO), None)
            rows.append(dict(om=om, phase=k, t_tang=travel_far / om, first=fb,
                             delay=(fb - travel_far / om) if fb is not None else None))
    realized = [r for r in rows if r["first"] is not None]
    before = [r for r in realized if r["first"] < r["t_tang"]]
    per_rate = []
    for om in (1e-3, 2e-3, 3e-3, 5e-3):
        rr = [r for r in realized if r["om"] == om]
        per_rate.append(dict(om=om, n=len(rr), t_tang=travel_far / om,
                             earliest_delay=(min(r["delay"] for r in rr) if rr else None),
                             median_delay=(sorted(r["delay"] for r in rr)[len(rr) // 2]
                                           if rr else None)))
    res["E2_G4n"] = dict(dstar=dstar, travel_far=travel_far, travel_near=travel_near,
                         rows=rows, n_realized=len(realized), n_before_tangency=len(before),
                         linfit_t_first_vs_inv_om=linfit([1 / r["om"] for r in realized],
                                                         [r["first"] for r in realized]),
                         linfit_earliest_vs_inv_om=linfit(
                             [1 / p["om"] for p in per_rate if p["earliest_delay"] is not None],
                             [p["t_tang"] + p["earliest_delay"] for p in per_rate
                              if p["earliest_delay"] is not None]),
                         per_rate=per_rate,
                         delays=[round(r["delay"], 1) for r in realized])
    print(f"E2 G4n: dstar={dstar:.6f} travel_far={travel_far:.4f} realized={len(realized)} "
          f"before={len(before)} minfit={res['E2_G4n']['linfit_earliest_vs_inv_om']}",
          flush=True)
    print("E2 per_rate:", per_rate, flush=True)

    # ---------- E3: theta-sweeps (fix + shadowing crossover) on G6 (12 phases) and G2 ----------
    for g, psyn in (("g6", PSYN_G6), ("g2", PSYN_G2)):
        ks = range(12) if g == "g6" else SUB4
        plists = {k: [load(f"{g}f_p{k}")] + [load(f"{g}P_p{k}_d{j}") for j in range(1, 92)]
                  for k in ks}
        sweep = []
        for m, th in THETAS:
            per = []
            for k in ks:
                wins = (frozen_windows(plists[k][0], 1500.0) if m is None
                        else theta_windows(plists[k], 1500.0, m, OM_SWEEP))
                key = f"g6r3_p{k}" if g == "g6" else f"g2r_p{k}"
                per.append((k, eval_policy(load(key), wins, psyn), len(wins)))
            sweep.append(dict(theta=th, m=m,
                              misses=sum(p[1]["misses"] for p in per),
                              waste=sum(p[1]["waste"] for p in per),
                              props=sum(p[1]["props"] for p in per),
                              rebuilds=max(p[2] for p in per),
                              n_ph_missing=sum(1 for p in per if p[1]["misses"]),
                              per_phase={str(k): p[1] for k, p in zip(ks, per)}))
            print(f"E3 {g} theta={th}: misses={sweep[-1]['misses']} waste={sweep[-1]['waste']} "
                  f"props={sweep[-1]['props']} rebuilds={sweep[-1]['rebuilds']}", flush=True)
        res[f"E3_theta_sweep_{g}"] = sweep

    # ---------- E4: G4n fix at theta=0.2 (never-pair coverage after tangency) ----------
    pl = [load("g4f")] + [load(f"g4fix_d{j}") for j in range(1, 15)]
    wins = theta_windows(pl, 3000.0, 1, 1e-3, dstep=0.2)  # window step 200 time = 0.2 rad
    true = load("g4r1_p0")
    r = eval_policy(true, wins, PSYN_G4)
    fb = next((t for (t, d) in true if d < RHO), None)
    res["E4_G4n_fix"] = dict(misses=r["misses"], waste=r["waste"], props=r["props"],
                             n_events=r["n_events"], first_true=fb, rebuilds=len(wins))
    print("E4 G4n fix theta=0.2:", res["E4_G4n_fix"], flush=True)

    # ---------- E5: regen verification of the author's results3 ----------
    orig = json.load(open(os.path.join(HERE, "results3.orig.json")))
    tags = {5e-4: "0.0005", 1e-3: "0.001", 2e-3: "0.002"}
    bad = []
    for (om, k, _t_cross_near, first) in orig:
        got = next((t for (t, d) in load(f"regen_{tags[om]}_k{k}") if d < RHO), None)
        if got != first:
            bad.append((om, k, first, got))
    res["E5_regen3"] = dict(n=len(orig), mismatches=bad,
                            corrected_t_tang={tags[om]: travel_far / om
                                              for om in (5e-4, 1e-3, 2e-3)})

    # ---------- E6: fold width — the staleness needed to certify a fold event ----------
    # Q(delta) = pair with pom_i shifted by delta and the t=0 mean anomalies: Q(delta(t))
    # evaluated at time t reproduces the true pair exactly (delta(t) = om*t on body i).
    from cert import d2_pair

    def min_d_near(bi, bj, tc, half=8.0):
        tau = np.arange(tc - half, tc + half, 0.002)
        d2 = d2_pair(bi, bj, tau)
        return float(np.sqrt(d2.min()))

    folds = []
    ev_list = [("g6", G6, 1, 667.4113902110225), ("g6", G6, 2, 917.1),
               ("g6", G6, 2, 1394.1), ("g6", G6, 6, 1086.5404245063),
               ("g6", G6, 10, 975.0), ("g2", G2, 3, 747.7958482618817)]
    for g, base, k, t_ev in ev_list:
        dstar_ev = OM_SWEEP * t_ev
        ph = k * TAU / 12
        bj0 = dict(base[1], M0=ph)
        row = dict(geometry=g, phase=k, t_event=t_ev, delta_event=round(dstar_ev, 5), scan=[])
        for off in (-0.01, -0.003, -0.001, -0.0003, 0.0, 0.0003, 0.001, 0.003, 0.01):
            bi = dict(base[0], pom=base[0]["pom"] + dstar_ev + off)
            md = min_d_near(bi, bj0, t_ev)
            row["scan"].append(dict(offset=off, min_d=round(md, 6)))
        res.setdefault("E6_fold_width", []).append(row)
        widths = [abs(sc["offset"]) for sc in row["scan"] if sc["min_d"] < 1.2 * RHO]
        row["width_below_1p2rho"] = max(widths) if widths else 0.0
        print(f"E6 {g} ph{k} t={t_ev:.1f}: d_event scan {row['scan']} "
              f"width<1.2rho={row['width_below_1p2rho']}", flush=True)
    print(f"E5 regen3: {len(orig)} rows, mismatches={bad}", flush=True)

    out["results"] = res
    with open(os.path.join(HERE, "results4.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("wrote results4.json", flush=True)


if __name__ == "__main__":
    main()
