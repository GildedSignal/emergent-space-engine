#!/usr/bin/env python3
"""Re-run the scar physics with the wall-free level instrument per epoch.

Physics is scars.py verbatim (same seed, same kick law, same KDK, same
channel definitions); only the measurement differs. Modes:
  long  : N=1e4, 45000 kicks — model-coded level per epoch, raw and with the
          shipped secular program (per-body linear rates fitted on the first
          30%), plus plug-in totals to show where the wall sits.
  bign  : N=3e5, 4500 kicks  — same-seed superset of main (first 1e4 bodies
          asserted identical to the stored main npz); plug-in vs model level;
          held-out coding (table fitted on the first 1e4 bodies, 2.9e5 coded).
"""
import json
import sys
import time

import numpy as np

from level import (CHANNELS, CIRCLE, channel_levels, level_bits_1d,
                   level_bits_2d, plugin_bits, heldout_bits_1d, wrap)
from scars import elements_from_state, jupiter, pos_vel_from_M

TAU = 2.0 * np.pi
Q = 1e-6


def run(nsteps=45000, N=10000, muJ=9.5459e-4, steps_per_PJ=150,
        seed=20261008, tag="long"):
    rng = np.random.default_rng(seed)
    PJ = TAU * np.sqrt(5.2 ** 3)
    dt = PJ / steps_per_PJ

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
        ax = muJ * (-dx / d3 - xJ / rJ3)
        ay = muJ * (-dy / d3 - yJ / rJ3)
        VX += 0.5 * dt * ax
        VY += 0.5 * dt * ay
        a, e, varpi, M = elements_from_state(X, Y, VX, VY)
        M = wrap(M + dt * a ** -1.5)
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
            print(f"  step {step}/{nsteps} t={t:7.1f}yr "
                  f"elapsed={time.time()-start:4.0f}s", file=sys.stderr)

    result = {"tag": tag, "N": N, "nsteps": nsteps, "q": Q, "epochs": []}

    if tag == "long":
        # secular program exactly as shipped: rates fitted on first 30%
        fit = [s for s in snaps if s["step"] <= 0.3 * nsteps]
        ts = np.array([s["t_yr"] for s in fit])
        Vp = np.unwrap(np.array([s["dvarpi"] for s in fit]), axis=0)
        Lm = np.unwrap(np.array([s["dlambda"] for s in fit]), axis=0)
        A = np.vstack([ts, np.ones_like(ts)]).T
        g_slope = np.linalg.lstsq(A, Vp, rcond=None)[0][0]
        l_slope = np.linalg.lstsq(A, Lm, rcond=None)[0][0]

    for s in snaps:
        row = {"step": s["step"], "t_yr": round(s["t_yr"], 2)}
        lv = channel_levels(s, Q)
        row["level"] = {k2: round(v, 3) for k2, v in lv.items()}
        row["level_total"] = round(sum(lv[c] for c in CHANNELS), 3)
        row["level_joint_total"] = round(
            lv["da_rel"] + lv["joint_hk"] + lv["dvarpi"] + lv["dlambda"], 3)
        row["plugin_total"] = round(
            sum(plugin_bits(s[c], Q) for c in CHANNELS), 3)
        row["wall_total"] = round(5 * np.log2(N), 3)
        if tag == "long":
            sec = {}
            sec_v = {}
            for ch in CHANNELS:
                v2 = s[ch]
                if ch == "dvarpi":
                    v2 = wrap(v2 - g_slope * s["t_yr"])
                elif ch == "dlambda":
                    v2 = wrap(v2 - l_slope * s["t_yr"])
                elif ch in ("dh", "dk"):
                    gt = g_slope * s["t_yr"]
                    hr = h0 * np.cos(gt) - k0 * np.sin(gt)
                    kr = h0 * np.sin(gt) + k0 * np.cos(gt)
                    v2 = (v2 + (h0 if ch == "dh" else k0)) - \
                        (hr if ch == "dh" else kr)
                sec_v[ch] = v2
                sec[ch] = level_bits_1d(v2, Q, 256, CIRCLE.get(ch, False))[0]
            row["level_sec"] = {c: round(sec[c], 3) for c in CHANNELS}
            row["level_sec_total"] = round(sum(sec[c] for c in CHANNELS), 3)
            row["level_sec_joint_total"] = round(
                sec["da_rel"] + level_bits_2d(sec_v["dh"], sec_v["dk"], Q)
                + sec["dvarpi"] + sec["dlambda"], 3)
        result["epochs"].append(row)

    if tag == "long":
        fin = {ch: snaps[-1][ch] for ch in CHANNELS}
        fin["a0"] = a0
        np.savez_compressed(f"scars2-{tag}-final.npz", **fin)
        ref = np.load("work/orig/scars-long-final.npz")
        result["final_matches_stored_long"] = {
            ch: bool((fin[ch] == ref[ch]).all()) for ch in CHANNELS}

    if tag == "bign":
        ref = np.load("scars-main-final.npz")
        same = {ch: bool((fin[ch][:10000] == ref[ch]).all())
                for ch in CHANNELS}
        result["prefix_identical_to_main"] = same
        row = {"step": nsteps}
        row["plugin_final"] = {ch: round(plugin_bits(fin[ch], Q), 3)
                               for ch in CHANNELS}
        row["plugin_final_total"] = round(
            sum(row["plugin_final"].values()), 3)
        row["level_final"] = {k2: round(v, 3)
                              for k2, v in channel_levels(fin, Q).items()}
        row["level_final_total"] = round(
            sum(row["level_final"][c] for c in CHANNELS), 3)
        row["wall_total"] = round(5 * np.log2(N), 3)
        ho = {}
        for ch in CHANNELS:
            b, frac = heldout_bits_1d(fin[ch][:10000], fin[ch][10000:], Q,
                                      256, CIRCLE.get(ch, False))
            ins = level_bits_1d(fin[ch][:10000], Q, 256,
                                CIRCLE.get(ch, False))[0]
            ho[ch] = {"insample_1e4": round(ins, 3),
                      "heldout_2.9e5": round(b, 3),
                      "excess": round(b - ins, 3), "escape_frac": frac}
        result["heldout"] = ho

    out = f"scars2-{tag}.json"
    with open(out, "w") as f:
        json.dump(result, f, indent=1)
    print("wrote", out)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "long"
    if mode == "bign":
        run(N=300000, nsteps=4500, tag="bign")
    else:
        run(nsteps=45000, tag="long")
