#!/usr/bin/env python3
"""Kick-cadence phase boundary for the averaged-kick layer (dynamics lens, run 20261009-1936-dynamics-5030).

Secular model: double-averaged quadrupole tide (Kozai-Lidov test particle, circular outer
perturber) = H0190 K2's family. Canonical pair (j = sqrt(1-e^2), omega), j_z conserved.
E(j, w) = 1 + 3/2*(1-j^2) - 3*(1 - jz^2/j^2)*P,  P = (1/2 + 2(1-j^2)) sin^2 w + (j^2/2) cos^2 w.
flow = (-dE/dw, +dE/dj) * eps  (verified against finite differences).
Truth: RK4 on the same flow, dt = 0.004/eps, E drift asserted < 1e-5.
Map: kicks at interval h orbits (cadence = 1/h kicks/orbit), shear order (kick j, then
advance w at the NEW j — the WH-like order) and naive explicit Euler. Shadow pair -> Lyapunov.

Modes: sanity | tlib | sweep | analyze
"""
import json, math, sys
import numpy as np

# ---------- Hamiltonian and flow ----------

def energy(j, w, jz):
    s2 = np.sin(w) ** 2
    u = 1.0 - j * j
    P = (0.5 + 2.0 * u) * s2 + 0.5 * (1.0 - u) * (1.0 - s2)
    return 1.0 + 1.5 * u - 3.0 * (1.0 - jz * jz / (j * j)) * P

def flow(j, w, jz, eps):
    s2 = np.sin(w) ** 2
    j2 = j * j
    u = 1.0 - j2
    Q = 1.0 - (jz * jz) / j2
    P = (0.5 + 2.0 * u) * s2 + 0.5 * j2 * (1.0 - s2)
    dj = 7.5 * Q * u * np.sin(2.0 * w)
    dw = -3.0 * j - 6.0 * (jz * jz / (j * j2)) * P - 3.0 * Q * j * (1.0 - 5.0 * s2)
    return eps * dj, eps * dw

def rk4_step(j, w, jz, eps, dt):
    a1, b1 = flow(j, w, jz, eps)
    a2, b2 = flow(j + 0.5 * dt * a1, w + 0.5 * dt * b1, jz, eps)
    a3, b3 = flow(j + 0.5 * dt * a2, w + 0.5 * dt * b2, jz, eps)
    a4, b4 = flow(j + dt * a3, w + dt * b3, jz, eps)
    return j + dt / 6.0 * (a1 + 2 * a2 + 2 * a3 + a4), w + dt / 6.0 * (b1 + 2 * b2 + 2 * b3 + b4)

# ---------- cases ----------

def fixed_point_j(jz):
    f = lambda j: flow(np.array([j]), np.array([math.pi / 2]), jz, 1.0)[1][0]
    lo, hi = abs(jz) + 1e-6, 1 - 1e-6
    if f(lo) * f(hi) > 0:
        return None
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)

def make_cases():
    jz_c2 = 0.45
    jstar = fixed_point_j(jz_c2)
    return [
        ("C1-deep-kl",      0.30,  0.995, math.radians(45)),
        ("C2-near-centre",  jz_c2, min(0.999, jstar + 0.004), math.pi / 2 - 0.02),
        ("C3-near-sep",     0.74,  0.99,  math.radians(80)),
        ("C4-pro-circ",     0.90,  0.95,  math.radians(30)),
        ("C5-retro-circ",  -0.50,  0.90,  math.radians(30)),
        ("C6-e09-heldout",  0.20,  0.436, math.pi / 2),
    ]

EPS_LIST = [0.3, 0.1, 0.03, 0.01]

# ---------- shared lockstep integrator (truth or map) ----------

def lockstep(run_state, step_fn, T_end, store_max=4096, renorm=256):
    """run_state: dict of arrays j, w, jz, eps (and optional h, shear flag in closure via step_fn).
    Steps all runs until each reaches T_end (time per run advanced by its own dt/h).
    Returns metrics."""
    W = len(run_state["j"])
    j = run_state["j"].copy(); w = run_state["w"].copy()
    jz = run_state["jz"]; eps = run_state["eps"]; dt = run_state["dt"]
    jlo = np.abs(jz) + 1e-12
    jhi = np.full(W, 1.0 - 1e-12)
    js_ = j + 1e-9; ws_ = w.copy()
    grow = np.zeros(W); last_d = np.full(W, 1e-9)
    done = np.zeros(W, bool); viol = np.zeros(W, bool)
    emax = np.full(W, -1.0); dw_tot = np.zeros(W)
    E0 = energy(j, w, jz); Emax = np.zeros(W)
    steps_max = int(np.ceil(np.max(T_end / dt)))
    dec = max(1, steps_max // store_max)
    e_store = np.full((store_max + 2, W), np.nan)
    t_store = np.zeros((store_max + 2, W))
    e_store[0] = np.sqrt(np.maximum(0, 1 - j * j)); t_store[0] = 0.0
    hn = 1
    dlog = []  # (t, running max E drift) snapshots for exponent
    snap_t, snap_m = [], []
    t_now = np.zeros(W)
    for it in range(1, steps_max + 1):
        act = ~done
        if not act.any():
            break
        idx = np.nonzero(act)[0]
        jj, ww = j[idx], w[idx]
        jn, wn = step_fn(jj, ww, jz[idx], eps[idx], dt[idx])
        # shadow
        sj, sw = js_[idx], ws_[idx]
        sjn, swn = step_fn(sj, sw, jz[idx], eps[idx], dt[idx])
        if it % renorm == 0:
            dist = np.hypot(sjn - jn, swn - wn)
            dist = np.maximum(dist, 1e-300)
            grow[idx] += np.log(dist / last_d[idx])
            ratio = 1e-9 / dist
            sjn = jn + (sjn - jn) * ratio
            swn = wn + (swn - wn) * ratio
            last_d[idx] = 1e-9
        bad = (jn < jlo[idx]) | (jn > jhi[idx])
        viol[idx] |= bad
        j[idx] = np.clip(jn, jlo[idx], jhi[idx]); w[idx] = wn
        js_[idx] = np.clip(sjn, jlo[idx], jhi[idx]); ws_[idx] = swn
        t_now[idx] += dt[idx]
        dw_tot[idx] += (wn - ww)
        e_now = np.sqrt(np.maximum(0, 1 - j * j))
        emax[idx] = np.maximum(emax[idx], e_now[idx])
        Ed = np.abs(energy(j[idx], w[idx], jz[idx]) - E0[idx])
        Emax[idx] = np.maximum(Emax[idx], Ed)
        if it % dec == 0 and hn <= store_max:
            e_store[hn] = e_now; t_store[hn] = t_now; hn += 1
        if it % (renorm * 4) == 0:
            snap_t.append(t_now.copy()); snap_m.append(Emax.copy())
        done[idx] = t_now[idx] >= T_end[idx] - 1e-12
    lam = np.where(T_end > 0, grow / np.maximum(T_end, 1e-9), 0.0)
    return dict(j=j, w=w, dw_tot=dw_tot, emax=emax, viol=viol, Emax=Emax,
                lam=lam, e_store=e_store[:hn], t_store=t_store[:hn],
                snap_t=np.array(snap_t), snap_m=np.array(snap_m), steps_max=steps_max)

def step_truth(j, w, jz, eps, dt):
    return rk4_step(j, w, jz, eps, dt)

def make_step_map(shear):
    if shear:
        def st(j, w, jz, eps, h):
            djm, _ = flow(j, w, jz, eps)
            jn = j + h * djm
            _, dwm = flow(jn, w, jz, eps)
            return jn, w + h * dwm
    else:
        def st(j, w, jz, eps, h):
            djm, dwm = flow(j, w, jz, eps)
            return j + h * djm, w + h * dwm
    return st

# ---------- behaviour metrics from stores ----------

def behaviour(dw_tot, e_store, t_store, T_win):
    cls = "circ" if abs(dw_tot) > 1.5 * 2 * math.pi else "lib"
    emax = float(np.nanmax(e_store))
    if cls == "circ":
        per = 2 * math.pi * T_win / max(abs(dw_tot), 1e-12)
    else:
        e = np.nanmean(e_store, axis=1)  # across runs; callers use single-run slices
        per = float("nan")
    return cls, emax, per

def libration_period(t, e):
    idx = [i for i in range(1, len(e) - 1) if e[i] >= e[i - 1] and e[i] > e[i + 1] and not math.isnan(e[i])]
    if len(idx) < 3:
        return float("nan")
    gaps = np.diff(np.array(t)[idx])
    gaps = gaps[gaps > 0]
    return float(np.median(gaps))  # one e-maximum per libration period (verified against omega crossings)


# ---------- modes ----------

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "sanity"
    cases = make_cases()

    if mode == "sanity":
        rng = np.random.default_rng(1)
        j = rng.uniform(0.3, 0.999, 1000); w = rng.uniform(0, 2 * np.pi, 1000); jz = rng.uniform(-0.8, 0.8, 1000)
        dj, dw = flow(j, w, jz, 1.0)
        d = 1e-6
        Ew = (energy(j, w + d, jz) - energy(j, w - d, jz)) / (2 * d)
        Ej = (energy(j + d, w, jz) - energy(j - d, w, jz)) / (2 * d)
        assert np.max(np.abs(dj + Ew)) < 1e-6 and np.max(np.abs(dw - Ej)) < 1e-6, "flow not canonical"
        for ci in (0.7754, 0.7745):
            f = flow(np.array([0.999999]), np.array([math.pi / 2]), np.array([ci]), 1.0)[1][0]
            print(f"f_w(e~0, w=90, cos i={ci}) = {f:+.4f}")
        # truth E conservation, worst case
        st = dict(j=np.array([0.995]), w=np.array([0.8]), jz=np.array([0.3]), eps=np.array([0.1]), dt=np.array([0.004 / 0.1]))
        m = lockstep(st, step_truth, np.array([600.0]))
        print("truth E drift:", m["Emax"][0])
        # linearized libration frequency at C2 centre vs measured period
        jstar = fixed_point_j(0.45)
        d2 = 1e-5
        Ejj = (energy(jstar + d2, math.pi / 2, 0.45) - 2 * energy(jstar, math.pi / 2, 0.45) + energy(jstar - d2, math.pi / 2, 0.45)) / d2 ** 2
        Eww = (energy(jstar, math.pi / 2 + d2, 0.45) - 2 * energy(jstar, math.pi / 2, 0.45) + energy(jstar, math.pi / 2 - d2, 0.45)) / d2 ** 2
        wlib = math.sqrt(abs(Ejj * Eww)) * 0.1
        print("C2 jstar:", round(jstar, 4), "linear T_lib:", round(2 * math.pi / wlib, 1))
        return

    if mode == "tlib":
        # measure T_lib per case/eps from truth (vectorized lockstep)
        rows = []
        for name, jz, j0, w0 in cases:
            for eps in EPS_LIST:
                rows.append((name, jz, j0, w0, eps))
        st = dict(j=np.array([r[2] for r in rows]), w=np.array([r[3] for r in rows]),
                  jz=np.array([r[1] for r in rows]), eps=np.array([r[4] for r in rows]),
                  dt=np.array([0.004 / r[4] for r in rows]))
        T_probe = np.array([150.0 / r[4] for r in rows])  # 150 secular-time units
        m = lockstep(st, step_truth, T_probe)
        out = {}
        for k, r in enumerate(rows):
            name, jz, j0, w0, eps = r
            t = m["t_store"][:, k]; e = m["e_store"][:, k]
            if abs(m["dw_tot"][k]) > 1.5 * 2 * math.pi:
                per = 2 * math.pi * T_probe[k] / abs(m["dw_tot"][k]); cls = "circ"
            else:
                per = libration_period(t, e); cls = "lib"
            out[f"{name}|{eps}"] = dict(cls=cls, T_lib=per, emax=float(m["emax"][k]),
                                        E_drift=float(m["Emax"][k]))
            print(f"{name} eps={eps}: {cls} T_lib={per:.1f} emax={m['emax'][k]:.4f} Edrift={m['Emax'][k]:.2e}")
        json.dump(out, open("tlib.json", "w"), indent=1)
        return

    if mode == "sweep":
        tlib = json.load(open("tlib.json"))
        hs = [1 / 128, 1 / 64, 1 / 32, 1 / 16, 1 / 8, 1 / 4, 0.5, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
        win_libs = 20.0
        runs = []
        for name, jz, j0, w0 in cases:
            for eps in EPS_LIST:
                info = tlib[f"{name}|{eps}"]
                Tl = info["T_lib"]; cls = info["cls"]
                for h in hs:
                    N_lib = Tl / h
                    if not (3.0 <= N_lib <= 3000.0):
                        continue
                    if win_libs * N_lib > 200000:
                        continue
                    for v in ("shear", "euler"):
                        runs.append(dict(case=name, eps=eps, h=h, variant=v, N_lib=N_lib,
                                         T_win=win_libs * Tl, cls_truth=cls))
        W = len(runs)
        print("map runs:", W)
        # one lockstep per variant
        for variant in ("shear", "euler"):
            sel = [r for r in runs if r["variant"] == variant]
            st = dict(j=np.array([dict((c[0], c) for c in cases)[r["case"]][2] for r in sel]),
                      w=np.array([dict((c[0], c) for c in cases)[r["case"]][3] for r in sel]),
                      jz=np.array([dict((c[0], c) for c in cases)[r["case"]][1] for r in sel]),
                      eps=np.array([r["eps"] for r in sel]),
                      dt=np.array([r["h"] for r in sel]))
            m = lockstep(st, make_step_map(variant == "shear"), np.array([r["T_win"] for r in sel]))
            for k, r in enumerate(sel):
                t = m["t_store"][:, k]; e = m["e_store"][:, k]
                if abs(m["dw_tot"][k]) > 1.5 * 2 * math.pi:
                    cls_r = "circ"; per = 2 * math.pi * r["T_win"] / abs(m["dw_tot"][k])
                else:
                    cls_r = "lib"; per = libration_period(t, e)
                # E drift exponent from snapshots
                mt = m["snap_t"][:, k]; mm = m["snap_m"][:, k]
                ok = (mt > 0) & (mm > 1e-14)
                if ok.sum() >= 4:
                    expo = float(np.polyfit(np.log(mt[ok]), np.log(mm[ok]), 1)[0])
                else:
                    expo = float("nan")
                r.update(cls_map=cls_r, emax_map=float(m["emax"][k]),
                         lam=float(m["lam"][k]), viol=bool(m["viol"][k]),
                         Emax=float(m["Emax"][k]), E_expo=expo, period_map=per)
            print("variant done:", variant, "steps_max:", m["steps_max"])
        # truth metrics on the same windows
        trows = []
        for name, jz, j0, w0 in cases:
            for eps in EPS_LIST:
                trows.append((name, eps, jz, j0, w0))
        st = dict(j=np.array([r[3] for r in trows]), w=np.array([r[4] for r in trows]),
                  jz=np.array([r[2] for r in trows]), eps=np.array([r[1] for r in trows]),
                  dt=np.array([0.004 / r[1] for r in trows]))
        T_win = np.array([win_libs * tlib[f"{r[0]}|{r[1]}"]["T_lib"] for r in trows])
        m = lockstep(st, step_truth, T_win)
        truth = {}
        for k, r in enumerate(trows):
            t = m["t_store"][:, k]; e = m["e_store"][:, k]
            if abs(m["dw_tot"][k]) > 1.5 * 2 * math.pi:
                cls_r = "circ"; per = 2 * math.pi * T_win[k] / abs(m["dw_tot"][k])
            else:
                cls_r = "lib"; per = libration_period(t, e)
            truth[f"{r[0]}|{r[1]}"] = dict(cls=cls_r, T_lib=per, emax=float(m["emax"][k]),
                                           E_drift=float(m["Emax"][k]))
            print(f"truth {r[0]} eps={r[1]}: {cls_r} T={per:.1f} emax={m['emax'][k]:.4f} Edrift={m['Emax'][k]:.1e}")
        json.dump(dict(runs=runs, truth=truth, tlib=tlib, win_libs=win_libs),
                  open("results.json", "w"), indent=1)
        print("wrote results.json")
        return

    if mode == "analyze":
        res = json.load(open("results.json"))
        runs = res["runs"]; truth = res["truth"]
        for r in runs:
            tr = truth[f"{r['case']}|{r['eps']}"]
            r["emax_err"] = abs(r["emax_map"] - tr["emax"]) / max(tr["emax"], 1e-6)
            r["per_err"] = abs(r["period_map"] - tr["T_lib"]) / max(abs(tr["T_lib"]), 1e-6) if not math.isnan(r["period_map"]) else float("nan")
            r["cls_ok"] = r["cls_map"] == tr["cls"]
            r["lam_Tlib"] = r["lam"] * res["tlib"][f"{r['case']}|{r['eps']}"]["T_lib"]
            r["ok"] = r["cls_ok"] and r["emax_err"] <= 0.1 and r["lam_Tlib"] <= 0.5 and not r["viol"]
            r["ok_strict"] = r["ok"] and (r["per_err"] != r["per_err"] or r["per_err"] <= 0.1)
        # boundary per (case, eps, variant): min N_lib among ok runs (ascending)
        print(f"{'case':16s} {'eps':>5s} {'variant':7s} {'loose':>7s} {'strict':>7s} {'onset-lam':>9s}")
        coll_loose, coll_strict = [], []
        for variant in ("shear", "euler"):
            for name, jz, j0, w0 in make_cases():
                for eps in EPS_LIST:
                    asc = sorted([r for r in runs if r["case"] == name and r["eps"] == eps and r["variant"] == variant], key=lambda r: r["N_lib"])
                    oks = next((r["N_lib"] for r in asc if r["ok"]), None)
                    okss = next((r["N_lib"] for r in asc if r["ok_strict"]), None)
                    lamon = next((r["N_lib"] for r in asc if r["lam_Tlib"] > 0.5), None)
                    print(f"{name:16s} {eps:5.2f} {variant:7s} {str(('%.0f'%oks) if oks else 'None'):>7s} {str(('%.0f'%okss) if okss else 'None'):>7s} {str(('%.0f'%lamon) if lamon else 'None'):>9s}")
                    if variant == "shear":
                        if oks: coll_loose.append((name, eps, oks))
                        if okss: coll_strict.append(okss)
        for lab, coll in (("loose", coll_loose), ("strict", coll_strict)):
            if coll:
                vals = [c[2] for c in coll]
                print("shear %s boundary N_lib*: min %.1f max %.1f" % (lab, min(vals), max(vals)))
        byc = {}
        for name, eps, oks in coll_loose:
            byc.setdefault(name, []).append(oks)
        for name, v in sorted(byc.items()):
            print("  collapse %s: N_lib* = %s (factor %.1f)" % (name, ["%.1f" % x for x in v], max(v) / min(v)))
        # plateau
        plat = [r for r in runs if r["variant"] == "shear" and r["N_lib"] >= 20]
        bad = [r for r in plat if not r["ok"]]
        print("shear plateau N_lib>=20: runs", len(plat), "bad", len(bad))
        for r in bad[:10]:
            print("  BAD:", r["case"], r["eps"], "h=%.2f" % r["h"], "N_lib=%.0f" % r["N_lib"],
                  "emax_err=%.3g" % r["emax_err"], "per_err=%.3g" % r["per_err"],
                  "cls", r["cls_map"], "lamT=%.2f" % r["lam_Tlib"], "viol", r["viol"])
        json.dump(runs, open("rows.json", "w"), indent=1)
        return

if __name__ == "__main__":
    main()
