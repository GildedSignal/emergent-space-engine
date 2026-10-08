#!/usr/bin/env python3
"""Stress test for the phase-rank co-orbital certificate (run 20261007-2344-taleb-6f01).

Gold 20261006-0346-taleb-09b5: under a formation, every real encounter lies within
partner rank 4 along the orbit, so a phase-neighbour certificate at O(n*k) replaces the
quadratic window tier. This script measures that claim's valid domain.

Model: N bodies on Kepler orbits (GM=1, a~1). A belt is "concentrated" (the trigger case)
when the a-spread is tiny (da=1e-4), like a fleet. Formation scatter is added in the
eccentricity vector: pure orientation spread dppx (fixed e0, pericentre spread D) or
Gaussian e-vector scatter dvec (station-keeping model).

Truth contacts: per grid time, sort by true longitude lambda; adjacent pairs within
theta_c become candidates; each candidate pair's distance is minimized on the full grid,
local minima refined densely; contact event = min distance < rho. Independence check:
a random subsample of pairs is brute-forced on a denser grid with no lambda logic.

Certificate under test: partner rank in mean-anomaly order (M-sort) and in true-longitude
order (lambda-sort), measured at window open (t=0) and at the encounter (nearest grid
time). Miss fraction at rank k is the silent-drop rate of an O(n*k) tier.

Kepler propagation is exact to Newton convergence; all comparisons are geometric.
"""
import json
import sys
import time

import numpy as np

TAU = 2.0 * np.pi


def wrap(x):
    return (x + np.pi) % TAU - np.pi


def make_belt(N, da, e0, dppx=0.0, dvec=0.0, seed=1):
    rng = np.random.default_rng(seed)
    a = 1.0 + da * rng.random(N)
    if dppx > 0.0:
        th = dppx * rng.random(N)  # orientation spread at fixed e0 (extent D)
        P = e0 * np.cos(th)
        Q = e0 * np.sin(th)
    else:
        P = e0 + dvec * rng.standard_normal(N)
        Q = dvec * rng.standard_normal(N)
    e = np.hypot(P, Q)
    wx = np.arctan2(Q, P)
    wx = np.where(e < 1e-14, TAU * rng.random(N), wx)
    M0 = TAU * rng.random(N)
    n = a ** -1.5
    return dict(a=a, e=e, wx=wx, M0=M0, n=n, N=N)


def elem_M(el, t):
    return wrap(el["M0"] + el["n"] * t)


def kepler_solve(M, e):
    E = M.copy()
    for _ in range(10):
        den = 1.0 - e * np.cos(E)
        E = E - (E - e * np.sin(E) - M) / den
    return E


def from_E(el, E):
    c, s = np.cos(E), np.sin(E)
    r = el["a"] * (1.0 - el["e"] * c)
    f = np.arctan2(np.sqrt(np.maximum(0.0, 1.0 - el["e"] ** 2)) * s, c - el["e"])
    return r, wrap(el["wx"] + f)


def body_state(el, t):
    """(r, lam, M) at time t (scalar or array) for all bodies."""
    M = elem_M(el, t)
    return (*from_E(el, kepler_solve(M, el["e"])), M)


def grid_states(el, T, G):
    ts = np.linspace(0.0, T, G, endpoint=False)
    lamg = np.empty((G, el["N"]))
    xg = np.empty((G, el["N"]))
    yg = np.empty((G, el["N"]))
    for gi, t in enumerate(ts):
        r, lam, _ = body_state(el, t)
        lamg[gi] = lam
        xg[gi] = r * np.cos(lam)
        yg[gi] = r * np.sin(lam)
    return ts, xg, yg, lamg


def candidate_pairs(lamg, theta_c=0.06):
    """Pairs ever adjacent in true longitude with |dlam| < theta_c."""
    G, N = lamg.shape
    cand = set()
    for gi in range(G):
        order = np.argsort(lamg[gi])
        lam_s = lamg[gi][order]
        d = np.abs(wrap(np.diff(lam_s)))
        for k in np.where(d < theta_c)[0]:
            cand.add((int(order[k]), int(order[k + 1])))
        if abs(wrap(lam_s[0] - lam_s[-1])) < theta_c:
            cand.add((int(order[0]), int(order[-1])))
    return sorted(cand)


def pair_events(el, i, j, ts, xg, yg, rho, dense=512, span=2.0):
    """Refined (t*, dmin) contact events (dmin < rho) for one candidate pair."""
    G = len(ts)
    dt = ts[1] - ts[0]
    dg = np.hypot(xg[:, i] - xg[:, j], yg[:, i] - yg[:, j])
    if dg.min() > 20.0 * rho:
        return []
    k = np.arange(1, G - 1)
    loc = k[(dg[k] <= dg[k - 1]) & (dg[k] < dg[k + 1])]
    if dg[0] < dg[1]:
        loc = np.append(0, loc)
    if dg[-1] < dg[-2]:
        loc = np.append(loc, G - 1)
    sub = {kk: el[kk][i : i + 1] for kk in ("a", "e", "wx", "M0", "n")}
    sub2 = {kk: el[kk][j : j + 1] for kk in ("a", "e", "wx", "M0", "n")}
    out = []
    for gi in loc:
        if dg[gi] > 5.0 * rho + 0.05:
            continue
        td = (ts[gi] - span * dt) + (2.0 * span * dt) * np.arange(dense) / (dense - 1)
        xa, ya = [], []
        for s in (sub, sub2):
            r, lam, _ = body_state(s, td)
            xa.append(r * np.cos(lam))
            ya.append(r * np.sin(lam))
        dd = np.hypot(xa[0] - xa[1], ya[0] - ya[1])
        m = int(np.argmin(dd))
        if dd[m] < rho:
            out.append((float(td[m]), float(dd[m])))
    out.sort()
    ded = []
    for t, d in out:
        if not ded or t - ded[-1][0] > 2.0 * dt:
            ded.append((t, d))
    return ded


def brute_pairs(el, pairs, T, rho, G=4096):
    """No-lambda-logic brute force on given pairs (independence check)."""
    ts = np.linspace(0.0, T, G, endpoint=False)
    found = set()
    for (i, j) in pairs:
        dists = []
        for idx in (i, j):
            s = {kk: el[kk][idx : idx + 1] for kk in ("a", "e", "wx", "M0", "n")}
            r, lam, _ = body_state(s, ts)
            dists.append((r * np.cos(lam), r * np.sin(lam)))
        dg = np.hypot(dists[0][0] - dists[1][0], dists[0][1] - dists[1][1])
        if dg.min() < rho:
            found.add((i, j))
    return found


def orders_at(el, t):
    """Rank positions of every body in M-order and lambda-order at time t."""
    _, lam, M = body_state(el, t)
    posM = np.empty(el["N"], dtype=int)
    posM[np.argsort(M)] = np.arange(el["N"])
    posL = np.empty(el["N"], dtype=int)
    posL[np.argsort(lam)] = np.arange(el["N"])
    return posM, posL


def gap(pos, i, j, N):
    g = abs(int(pos[i]) - int(pos[j]))
    return min(g, N - g)


def triggers(el):
    n = el["n"]
    p = el["a"] * (1.0 - el["e"] ** 2)
    U, V, W = 1.0 / p, el["e"] * np.cos(el["wx"]) / p, el["e"] * np.sin(el["wx"]) / p
    c = (U.mean(), V.mean(), W.mean())
    r_binet = float(np.max(np.hypot(np.hypot(U - c[0], V - c[1]), W - c[2])))
    return {
        "dn_rel": float(n.max() - n.min()),
        "phase_density_per_rad": el["N"] / TAU,
        "binet_radius": r_binet,
    }


def analyze(name, N=300, da=1e-4, e0=3e-4, dppx=0.0, dvec=0.0, T=30 * TAU,
            rho=1e-3, G=1024, seed=1, brute_n=0, k=4, tag=""):
    t_start = time.time()
    el = make_belt(N, da, e0, dppx, dvec, seed)
    ts, xg, yg, lamg = grid_states(el, T, G)
    cand = candidate_pairs(lamg)
    events = []
    for (i, j) in cand:
        events.extend((i, j, tm, dm) for (tm, dm) in pair_events(el, i, j, ts, xg, yg, rho))
    dt = ts[1] - ts[0]
    posM0, posL0 = orders_at(el, 0.0)
    cache = {}

    def ranks_at(tq):
        key = int(round(tq / dt))
        if key not in cache:
            cache[key] = orders_at(el, key * dt)
        return cache[key]

    r0 = {"M": [], "lam": []}
    rE = {"M": [], "lam": []}
    pair0 = {}
    for i, j, tm, dm in events:
        gM, gL = gap(posM0, i, j, N), gap(posL0, i, j, N)
        r0["M"].append(gM)
        r0["lam"].append(gL)
        pM, pL = ranks_at(tm)
        rE["M"].append(gap(pM, i, j, N))
        rE["lam"].append(gap(pL, i, j, N))
        if (i, j) not in pair0:
            pair0[(i, j)] = (gM, gL)
    from collections import Counter
    ev_per_pair = Counter((i, j) for i, j, _, _ in events)
    def miss(v):
        return float(np.mean(np.asarray(v) > k)) if len(v) else None

    def q(v, p):
        return float(np.quantile(np.asarray(v), p)) if len(v) else None

    D_or = dppx if dppx > 0 else min(TAU, 4.0 * dvec)
    res = {
        "name": name, "tag": tag, "N": N, "da": da, "e0": e0, "dppx": dppx,
        "dvec": dvec, "T_orbits": T / TAU, "rho": rho, "k": k, "seed": seed,
        "contacts": len(events),
        "contact_pairs": len(pair0),
        "max_events_per_pair": max(ev_per_pair.values()) if ev_per_pair else 0,
        "miss_M_open": miss(r0["M"]), "miss_lam_open": miss(r0["lam"]),
        "miss_M_enc": miss(rE["M"]), "miss_lam_enc": miss(rE["lam"]),
        "miss_M_pairs": miss([gM for gM, _ in pair0.values()]),
        "miss_lam_pairs": miss([gL for _, gL in pair0.values()]),
        "rankM_open_p50": q(r0["M"], 0.5), "rankM_open_p95": q(r0["M"], 0.95),
        "ranklam_open_p95": q(r0["lam"], 0.95),
        "ranklam_open_max": max(r0["lam"]) if r0["lam"] else None,
        "cand_pairs": len(cand), "triggers": triggers(el),
        "S_M_pred": N * D_or / TAU,
        "S_lam_pred": N * (1.5 * da * (T / TAU) * TAU + 2.0 * dvec) / TAU,
        "seconds": round(time.time() - t_start, 2),
    }
    if brute_n:
        rng = np.random.default_rng(seed + 777)
        all_pairs = [(i, j) for i in range(N) for j in range(i + 1, N)]
        sel = set(all_pairs[x] for x in rng.choice(len(all_pairs), size=brute_n, replace=False))
        bf = brute_pairs(el, sorted(sel), T, rho)
        truth_sel = {(i, j) for (i, j, _, _) in events} & sel
        res.update({
            "brute_checked": brute_n,
            "brute_found": len(bf),
            "truth_in_subsample": len(truth_sel),
            "brute_extra": sorted(bf - truth_sel),
            "brute_agree": bf == truth_sel,
        })
    return res


def run(tag, cases, fname):
    out = []
    for c in cases:
        r = analyze(**c)
        out.append(r)
        print(json.dumps(r), flush=True)
    with open(fname, "w") as f:
        json.dump(out, f, indent=1)
    print(f"wrote {fname}", flush=True)


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "pilot"
    if which == "pilot":
        run("pilot", [
            dict(name="aligned-gold", tag="control+", N=300, da=1e-4, e0=3e-4,
                 dppx=0.0, dvec=0.0, seed=11, brute_n=150),
        ], "pilot.json")
    elif which == "wscan":
        cs = [dict(name=f"ppi-D{D:g}", tag="wscan", N=300, dppx=D, seed=21)
              for D in (0.05, 0.2, 0.5, 1.0, np.pi)]
        cs += [dict(name=f"N{N}-D0.5", tag="wscan", N=N, dppx=0.5, seed=31)
               for N in (150, 600)]
        cs += [dict(name="wide-belt", tag="control-", N=300, da=0.1, dppx=np.pi, seed=41)]
        cs += [dict(name="D0.5-rho3e-4", tag="rho", N=300, dppx=0.5, rho=3e-4, seed=21),
               dict(name="D0.5-rho3e-3", tag="rho", N=300, dppx=0.5, rho=3e-3, seed=21)]
        run("wscan", cs, "wscan.json")
    elif which == "escan":
        cs = [dict(name=f"evec-{dv:g}", tag="escan", N=300, dvec=dv, seed=51)
              for dv in (1e-4, 1e-3, 3e-3)]
        cs += [dict(name="lamcrack-N600-e02-d02", tag="escan", N=600, e0=0.02, dvec=0.02, seed=61),
               dict(name="lamsafe-N600-e02-d005", tag="escan", N=600, e0=0.02, dvec=0.005, seed=62),
               dict(name="lamcrack-N300-e02-d02", tag="escan", N=300, e0=0.02, dvec=0.02, seed=63)]
        run("escan", cs, "escan.json")
    else:
        print(__doc__)
