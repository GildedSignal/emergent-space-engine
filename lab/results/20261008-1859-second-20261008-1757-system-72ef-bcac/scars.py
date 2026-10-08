#!/usr/bin/env python3
"""Scar growth of a belt under the design's own path (Kepler drift + Jupiter kicks).

Question: does the per-body stored difference from the genesis program ("scar")
grow without bound in bits (the H_live fear: distinctions per game-second decide
whether 1e9 fit in 8 GB), or does it saturate / grow only as log(#kicks)?

Design's path (docs/law.md): drift = exact Kepler (the compiled tube), kicks =
the secondary's pull at a fixed step in the drift's phase. KDK per step, Jupiter
on its exact Kepler tube (its own drift is free). Elements are derived, never
stepped; we quantize element differences current - genesis at log-spaced epochs.
"""
import json
import sys
import time

import numpy as np

TAU = 2.0 * np.pi


def wrap(x):
    return (x + np.pi) % TAU - np.pi


def pos_vel_from_M(a, e, varpi, M):
    E = M.copy()
    for _ in range(8):
        E -= (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    cE, sE = np.cos(E), np.sin(E)
    fac = np.sqrt(1.0 - e * e)
    xo = a * (cE - e)
    yo = a * fac * sE
    den = 1.0 - e * cE
    n = a ** -1.5
    vxo = -a * n * sE / den
    vyo = a * n * fac * cE / den
    cv, sv = np.cos(varpi), np.sin(varpi)
    return (xo * cv - yo * sv, xo * sv + yo * cv,
            vxo * cv - vyo * sv, vxo * sv + vyo * cv)


def elements_from_state(X, Y, VX, VY):
    r = np.sqrt(X * X + Y * Y)
    v2 = VX * VX + VY * VY
    a = 1.0 / (2.0 / r - v2)          # GM = 1
    hz = X * VY - Y * VX
    ex = VY * hz - X / r
    ey = -VX * hz - Y / r
    e = np.sqrt(ex * ex + ey * ey)
    varpi = np.arctan2(ey, ex)
    rdotv = X * VX + Y * VY
    # true anomaly from the eccentricity vector (e cancels in the atan2)
    f = np.arctan2(ex * Y - ey * X, ex * X + ey * Y)
    # eccentric anomaly: tan(E/2) = sqrt((1-e)/(1+e)) tan(f/2)
    half = np.clip(np.sqrt((1.0 - e) / (1.0 + e)) * np.tan(f / 2.0), -1e6, 1e6)
    E = 2.0 * np.arctan(half)
    M = wrap(E - e * np.sin(E))
    return a, e, wrap(varpi), M


def jupiter(t, aJ=5.2, eJ=0.048, lJ0=0.6):
    MJ = wrap(lJ0 + t * aJ ** -1.5)
    EJ = MJ
    for _ in range(60):
        EJ -= (EJ - eJ * np.sin(EJ) - MJ) / (1.0 - eJ * np.cos(EJ))
    fac = np.sqrt(1.0 - eJ * eJ)
    nJ = aJ ** -1.5
    den = 1.0 - eJ * np.cos(EJ)
    return (aJ * (np.cos(EJ) - eJ), aJ * fac * np.sin(EJ),
            -aJ * nJ * np.sin(EJ) / den, aJ * nJ * fac * np.cos(EJ) / den)


def entropy_bits(v, q):
    codes = np.round(v / q).astype(np.int64)
    _, cnt = np.unique(codes, return_counts=True)
    p = cnt / cnt.sum()
    return float(-(p * np.log2(p)).sum())


def run(muJ=9.5459e-4, N=10000, nsteps=4500, steps_per_PJ=150, seed=20261008,
        q=1e-6, control=False, tag="main"):
    rng = np.random.default_rng(seed)
    PJ = TAU * np.sqrt(5.2 ** 3)
    dt = PJ / steps_per_PJ
    if control:
        muJ = 0.0

    a0 = rng.uniform(2.1, 3.3, N)
    e0 = np.minimum(rng.rayleigh(0.05, N), 0.6)
    varpi0 = rng.uniform(0, TAU, N)
    M0 = rng.uniform(0, TAU, N)
    h0 = e0 * np.cos(varpi0)
    k0 = e0 * np.sin(varpi0)

    a, e, varpi, M = a0.copy(), e0.copy(), varpi0.copy(), M0.copy()
    X, Y, VX, VY = pos_vel_from_M(a, e, varpi, M)

    epochs = np.unique(np.round(np.logspace(0, np.log10(nsteps), 24)).astype(int))
    t = 0.0
    start = time.time()
    snaps = []
    for step in range(1, nsteps + 1):
        tmid = t + 0.5 * dt
        xJ, yJ, _, _ = jupiter(tmid)
        dx, dy = X - xJ, Y - yJ
        d3 = (dx * dx + dy * dy) ** 1.5
        rJ3 = (xJ * xJ + yJ * yJ) ** 1.5
        ax = muJ * (-dx / d3 - xJ / rJ3)   # direct + indirect term
        ay = muJ * (-dy / d3 - yJ / rJ3)
        VX += 0.5 * dt * ax                # half kick
        VY += 0.5 * dt * ay
        a, e, varpi, M = elements_from_state(X, Y, VX, VY)  # kicked state
        M = wrap(M + dt * a ** -1.5)       # exact Kepler drift
        X, Y, VX, VY = pos_vel_from_M(a, e, varpi, M)
        xJ, yJ, _, _ = jupiter(tmid)
        dx, dy = X - xJ, Y - yJ
        d3 = (dx * dx + dy * dy) ** 1.5
        VX += 0.5 * dt * muJ * (-dx / d3 - xJ / rJ3)
        VY += 0.5 * dt * muJ * (-dy / d3 - yJ / rJ3)
        t += dt
        if step in epochs or step == nsteps:
            aa, ee, vv, MM = elements_from_state(X, Y, VX, VY)
            h = ee * np.cos(vv)
            k = ee * np.sin(vv)
            snaps.append({
                "step": step, "t_yr": t,
                "da_rel": (aa - a0) / a0,
                "dh": h - h0,
                "dk": k - k0,
                "dvarpi": wrap(vv - varpi0),
                "dlambda": wrap(MM + vv - M0 - varpi0 - t * a0 ** -1.5),
            })
            print(f"  step {step}/{nsteps} t={t:7.1f}yr elapsed={time.time()-start:4.0f}s",
                  file=sys.stderr)

    # secular program: per-body linear drift of dvarpi and dlambda fitted on
    # the first 30% of the horizon (rates are smooth in a; a program carries
    fit = [s for s in snaps if s["step"] <= 0.3 * nsteps]
    ts = np.array([s["t_yr"] for s in fit])
    Vp = np.unwrap(np.array([s["dvarpi"] for s in fit]), axis=0)   # (T_fit, N)
    Lm = np.unwrap(np.array([s["dlambda"] for s in fit]), axis=0)
    A = np.vstack([ts, np.ones_like(ts)]).T
    g_slope = np.linalg.lstsq(A, Vp, rcond=None)[0][0]
    l_slope = np.linalg.lstsq(A, Lm, rcond=None)[0][0]

    result = {"tag": tag, "muJ": muJ, "N": N, "nsteps": nsteps, "q": q,
              "control": bool(control), "epochs": []}
    for s in snaps:
        row = {"step": s["step"], "t_yr": round(s["t_yr"], 2), "channels": {}}
        tot_raw, tot_sec = 0.0, 0.0
        for ch in ("da_rel", "dh", "dk", "dvarpi", "dlambda"):
            v = s[ch]
            mag = np.abs(v)
            Hb = entropy_bits(v, q)
            row["channels"][ch] = {
                "H_bits": round(Hb, 3),
                "p50": float(np.median(mag)),
                "p99": float(np.quantile(mag, 0.99)),
                "zero_frac": round(float((np.round(v / q) == 0).mean()), 5),
            }
            tot_raw += Hb
            v2 = v
            if ch == "dvarpi":
                v2 = wrap(v - g_slope * s["t_yr"])
            elif ch == "dlambda":
                v2 = wrap(v - l_slope * s["t_yr"])
            elif ch in ("dh", "dk"):
                gt = g_slope * s["t_yr"]
                hr = h0 * np.cos(gt) - k0 * np.sin(gt)
                kr = h0 * np.sin(gt) + k0 * np.cos(gt)
                v2 = (v + (h0 if ch == "dh" else k0)) - (hr if ch == "dh" else kr)
            Hb2 = entropy_bits(v2, q)
            row["channels"][ch]["H_sec"] = round(Hb2, 3)
            tot_sec += Hb2
        row["H_total"] = round(tot_raw, 3)
        row["H_total_sec"] = round(tot_sec, 3)
        result["epochs"].append(row)

    # diagnostics from the final snapshot: resonance concentration and
    # quantum sensitivity of the saturation level
    fin = snaps[-1]
    near = np.abs(a0 - 3.276) / 3.276 < 0.01
    result["resonance"] = {
        "frac_near_21": round(float(near.mean()), 4),
        "da_p99_near": float(np.quantile(np.abs(fin["da_rel"][near]), 0.99)),
        "da_p99_far": float(np.quantile(np.abs(fin["da_rel"][~near]), 0.99)),
        "dh_p99_near": float(np.quantile(np.abs(fin["dh"][near]), 0.99)),
        "dh_p99_far": float(np.quantile(np.abs(fin["dh"][~near]), 0.99)),
    }
    result["q_sensitivity"] = {}
    for qq in (1e-5, 1e-6, 1e-7):
        result["q_sensitivity"][str(qq)] = round(
            sum(entropy_bits(fin[ch], qq) for ch in
                ("da_rel", "dh", "dk", "dvarpi", "dlambda")), 2)
    np.savez_compressed(f"scars-{tag}-final.npz", a0=a0,
                        **{ch: fin[ch] for ch in
                           ("da_rel", "dh", "dk", "dvarpi", "dlambda")})

    out = f"scars-{tag}.json"
    with open(out, "w") as f:
        json.dump(result, f, indent=1)
    print("wrote", out)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "main"
    if mode == "control":
        run(control=True, N=2000, nsteps=300, tag="control")
    elif mode == "long":
        run(nsteps=45000, tag="long")
    else:
        run()
