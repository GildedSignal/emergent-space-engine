#!/usr/bin/env python3
"""Red-team falsifier: does the encounters crate's premise (closed ellipses, one-frequency
'integer circle rotation' timing, cone certificates valid until a kick) survive inside a GR
doll, where every orbit precesses by dw ~ 6*pi*M/p per radial period with (E, L) unchanged?

Truth: exact Schwarzschild timelike Binet law u'' + u = M/L^2 + 3*M*u^2 (the doll's own law,
law.md 'Motion in a doll'), integrated in t with RK4. Encounter = local minimum of pair
distance below rho, dip quantum 1e-6*rho (r8 v4's definition).

Crate emulator (pairs.rs logic) fed PERFECT inputs: osculating (p, e, om) from the truth's own
first radial cycle and T_r = the truth's exact GR radial period -> closed Kepler ellipses;
sections at longitude passages; a passage is checked iff the MODEL's min distance near the
passage is < rho*1.5 (generous superset of the crate's window*safety=1.5); the check evaluates
the TRUTH's min distance there; predicted encounter iff < rho. Cone-excluded pairs
(|dU| - R >= eps_u) are never checked (certificate valid until a kick; there are no kicks).

Usage: falsifier.py <p30gr|p30newt|p300gr|p300newt>
"""
import json, sys, time
import numpy as np

MODE = sys.argv[1]
M = 1.0
RNG = np.random.default_rng(20261008)

if MODE.startswith("p300"):
    P0, SPREAD, N_ORB, DT, STRIDE = 300.0, 0.015, 30, 1.0, 4
    MODEL_DT = 10.0
elif MODE.startswith("p30"):
    P0, SPREAD, N_ORB, DT, STRIDE = 30.0, 0.015, 50, 0.08, 4
    MODEL_DT = 0.35
GR = MODE.endswith("gr")
RHO_FRAC = 1e-3
ps = np.append(RNG.uniform(P0 * (1 - SPREAD), P0 * (1 + SPREAD), 60),
               [P0, 1.04 * P0])          # excluded pair: p2/p1 = 31.2/30 at P0=30
es = np.append(RNG.uniform(0.18, 0.22, 60), [0.20, 0.21])
oms = np.append(RNG.uniform(0, 2 * np.pi, 60), [0.0, 0.0])
NB = len(ps)
RHO = RHO_FRAC * P0

# ---- integrate the doll's law (RK4 in t) --------------------------------------------
L2 = M * ps
u0 = (1.0 + es) / ps
L = np.sqrt(L2)
E = np.sqrt((1 - 2 * M * u0) * (1 + L2 * u0 * u0)) if GR else np.ones(NB)
ML2 = M / L2

def rhs(u, up):
    if GR:
        w = L * u * u * (1 - 2 * M * u) / E
        f = ML2 + 3 * M * u * u - u
    else:
        w = L * u * u
        f = ML2 - u
    return up * w, f * w, w

u = u0.copy(); up = np.zeros(NB); phi = np.zeros(NB); t = 0.0
T_END = N_ORB * 2 * np.pi * np.sqrt((P0 / (1 - 0.2 ** 2)) ** 3 / M) * 1.15
NS = int(T_END / DT)
NS_S = NS // STRIDE
su = np.empty((NS_S, NB)); sphi = np.empty((NS_S, NB)); st = np.empty(NS_S)
ks = 0
t_start = time.time()
for k in range(NS):
    if k % STRIDE == 0 and ks < NS_S:
        su[ks] = u; sphi[ks] = phi; st[ks] = t; ks += 1
    k1 = rhs(u, up); k2 = rhs(u + 0.5 * DT * k1[0], up + 0.5 * DT * k1[1])
    k3 = rhs(u + 0.5 * DT * k2[0], up + 0.5 * DT * k2[1]); k4 = rhs(u + DT * k3[0], up + DT * k3[1])
    u += DT / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
    up += DT / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
    phi += DT / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])
    t += DT
integ_s = time.time() - t_start
DTS = DT * STRIDE
x_true = np.cos(sphi + oms) / su
y_true = np.sin(sphi + oms) / su

# ---- osculating elements and exact radial periods from the truth itself -------------
elem = []
for b in range(NB):
    ub = su[:, b]
    loc = np.where((ub[1:-1] > ub[:-2]) & (ub[1:-1] >= ub[2:]))[0] + 1
    per = loc[loc > 5]
    umax = ub[per[0]]
    umin = ub[per[0]:per[1]].min()
    # exact radial period: least-squares slope over ALL periapses (grid error / 50 orbits)
    kk = np.arange(len(per))
    Tr = float(np.linalg.lstsq(np.vstack([kk, np.ones_like(kk)]).T,
                               st[per], rcond=None)[0][0])
    # periapsis angle, parabolic-refined in phi (u is flat at the maximum)
    i0 = per[0]
    y0, y1, y2 = ub[i0 - 1], ub[i0], ub[i0 + 1]
    den = y0 - 2 * y1 + y2
    sh = np.clip(0.5 * (y0 - y2) / den, -1, 1) if den != 0 else 0.0
    om = (sphi[i0, b] + sh * (sphi[i0 + 1, b] - sphi[i0 - 1, b]) / 2 + oms[b]) % (2 * np.pi)
    elem.append(dict(p=(umax + umin) / (2 * umax * umin), e=(umax - umin) / (umax + umin),
                     om=om, Tr=Tr,
                     tp=0.0, umax=umax, umin=umin))
del su, sphi

def kepler_state(el, tq):
    n = 2 * np.pi / el["Tr"]
    l = n * (tq - el["tp"])
    Ee = l.copy()
    for _ in range(10):
        Ee -= (Ee - el["e"] * np.sin(Ee) - l) / (1 - el["e"] * np.cos(Ee))
    nu = 2 * np.arctan2(np.sqrt(1 + el["e"]) * np.sin(Ee / 2), np.sqrt(1 - el["e"]) * np.cos(Ee / 2))
    r = el["p"] / (1 + el["e"] * np.cos(nu))
    th = nu + el["om"]
    return r * np.cos(th), r * np.sin(th)

CAP = (3 * RHO / 2e-3 + 2) if P0 < 100 else (3 * RHO / 1.7e-3 + 5)

def dist_trace(i, j):
    return np.hypot(x_true[:, i] - x_true[:, j], y_true[:, i] - y_true[:, j])

def truth_encounters(d):
    idx = np.where((d[1:-1] < d[:-2]) & (d[1:-1] <= d[2:]) & (d[1:-1] < RHO))[0] + 1
    out = []
    for i0 in idx:
        a, b = max(0, i0 - 3), min(len(d) - 1, i0 + 3)
        if d[a] < d[i0] + 1e-6 * RHO or d[b] < d[i0] + 1e-6 * RHO:
            continue
        y0, y1, y2 = d[i0 - 1], d[i0], d[i0 + 1]
        den = y0 - 2 * y1 + y2
        sh = np.clip(0.5 * (y0 - y2) / den, -1, 1) if den != 0 else 0.0
        out.append((st[i0] + sh * DTS, y1 - 0.25 * (y0 - y2) * sh))
    return out

def truth_min(d, tc, cap):
    i0 = np.searchsorted(st, tc - cap); i1 = np.searchsorted(st, tc + cap)
    if i1 <= i0:
        return None, None
    k = i0 + int(np.argmin(d[i0:i1]))
    return float(d[k]), float(st[k])

def eps_u(ei, ej):
    rmin = min(1 / ei["umax"], 1 / ej["umax"]); rmax = max(1 / ei["umin"], 1 / ej["umin"])
    kappa = rmax * rmax * max(ei["e"], ej["e"]) / (min(ei["p"], ej["p"]) * rmin)
    return 1.5 * RHO * (1 + kappa) / (rmin * rmin)

res = dict(mode=MODE, gr=GR, P0=P0, rho=RHO, n_bodies=NB, n_orbits=N_ORB,
           truth_encounters=0, predicted_encounters=0, matched=0, false=0,
           missed_by_pair={}, excluded_pairs=[], excluded_with_truth=0,
           drift_worst5=[], integ_seconds=integ_s)

for i in range(NB):
    for j in range(i + 1, NB):
        ei, ej = elem[i], elem[j]
        if min(1 / ei["umin"], 1 / ej["umin"]) + RHO < max(1 / ei["umax"], 1 / ej["umax"]):
            continue
        d = dist_trace(i, j)
        tent = truth_encounters(d)
        Ui, Vi, Wi = 1 / ei["p"], ei["e"] * np.cos(ei["om"]) / ei["p"], ei["e"] * np.sin(ei["om"]) / ei["p"]
        Uj, Vj, Wj = 1 / ej["p"], ej["e"] * np.cos(ej["om"]) / ej["p"], ej["e"] * np.sin(ej["om"]) / ej["p"]
        dU, dV, dW = Ui - Uj, Vi - Vj, Wi - Wj
        R = float(np.hypot(dV, dW))
        pred = []
        if abs(dU) - R >= eps_u(ei, ej):
            res["excluded_pairs"].append([i, j])
            if tent:
                res["excluded_with_truth"] += len(tent)
                res["missed_by_pair"][f"{i},{j}"] = len(tent)
        else:
            # Superset of the crate's check set: EVERY conjunction dip of the closed-ellipse
            # model below 1.5*rho (the crate's windows are supersets of the model's <rho
            # passages by construction: cross windows x safety, numeric windows {D<1.05*rho},
            # full sections at every periapsis). Timing is the one-frequency model.
            tq = np.arange(0.0, st[-1], MODEL_DT)
            xi, yi = kepler_state(ei, tq); xj, yj = kepler_state(ej, tq)
            dm_ = np.hypot(xi - xj, yi - yj)
            ix = np.where((dm_[1:-1] < dm_[:-2]) & (dm_[1:-1] <= dm_[2:]) & (dm_[1:-1] < RHO * 1.5))[0] + 1
            pred = list(tq[ix])
        decided = []
        for tev in pred:
            dm2, tm2 = truth_min(d, tev, CAP)
            if dm2 is not None and dm2 < RHO:
                decided.append(tm2)
        res["truth_encounters"] += len(tent)
        res["predicted_encounters"] += len(decided)
        nm = sum(1 for (tm, dm) in tent if any(abs(tm - td) < CAP for td in decided))
        nf = sum(1 for td in decided if not any(abs(tm - td) < CAP for (tm, dm) in tent))
        res["matched"] += nm
        res["false"] += nf
        if len(tent) > nm:
            res["missed_by_pair"][f"{i},{j}"] = len(tent) - nm
        # conjunction timing drift: truth conjunctions vs best one-frequency (linear) fit
        idx = np.where((d[1:-1] < d[:-2]) & (d[1:-1] <= d[2:]))[0] + 1
        if len(idx) >= 4:
            tk = st[idx]; k = np.arange(len(idx))
            slope = np.linalg.lstsq(np.vstack([k, np.ones_like(k)]).T, tk, rcond=None)[0][0]
            drift = np.abs(tk - (tk[0] + slope * k))
            res["drift_worst5"].append(dict(pair=[i, j], n=len(idx), max_drift=float(drift.max()),
                                            last_drift=float(drift[-1]), Tsyn=float(slope)))
res["drift_worst5"] = sorted(res["drift_worst5"], key=lambda z: -z["max_drift"])[:5]
res["missed_fraction"] = (res["truth_encounters"] - res["matched"]) / max(1, res["truth_encounters"])
res["false_fraction"] = res["false"] / max(1, res["truth_encounters"] + res["false"])
with open(f"result_{MODE}.json", "w") as f:
    json.dump(res, f, indent=1)
print(MODE, "| truth:", res["truth_encounters"], "matched:", res["matched"], "false:", res["false"],
      "| missed_fraction:", round(res["missed_fraction"], 4),
      "| excluded_with_truth:", res["excluded_with_truth"],
      "| integ_s:", round(integ_s, 1), "| total_s:", round(time.time() - t_start, 1))
