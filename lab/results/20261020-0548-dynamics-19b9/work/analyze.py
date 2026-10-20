#!/usr/bin/env python3
"""Analyze the beltledger flights: the carry ledger's attractor, walk, or drift.

Usage: python3 analyze.py <flights_dir> > analysis.json
Reads <arm>.global.tsv, <arm>.ledger.tsv, <arm>.epoch.tsv, <arm>.events.tsv per arm.
Pure python (no numpy): OLS, Spearman implemented inline.
"""
import gzip
import json
import math
import os
import sys
from collections import defaultdict


def open_maybe_gz(path):
    if os.path.exists(path):
        return open(path)
    gz = path + ".gz"
    if os.path.exists(gz):
        return gzip.open(gz, "rt")
    raise FileNotFoundError(path)

Q = 1 << 20
ENVELOPE_C = 16.0  # P1: maxAbsR < ENVELOPE_C*maxk + 32


def ols(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return sxy / sxx if sxx else 0.0


def spearman(xs, ys):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    return ols(ranks(xs), ranks(ys))


def load(path, cols):
    rows = []
    with open_maybe_gz(path) as f:
        for line in f:
            parts = line.split()
            if len(parts) >= cols:
                rows.append([int(p) for p in parts[:cols]])
    return rows


def analyze(dirpath, arm):
    g = load(os.path.join(dirpath, arm + ".global.tsv"), 10)
    # cols: t c esc n_live ke maxk sumR maxAbsR maxAbsC ops
    led = {r[0]: r for r in load(os.path.join(dirpath, arm + ".ledger.tsv"), 8)}
    out = {"n_ch": g[-1][0], "contacts": sum(r[1] for r in g), "esc_end": g[-1][2]}

    # P1: quantum envelope on every stride sample (maxk is running max already).
    p1_bad = []
    ratio_max = 0.0
    for r in g:
        t, mar, maxk = r[0], r[7], r[5]
        if t in led:
            env = ENVELOPE_C * maxk + 32
            if mar >= env:
                p1_bad.append((t, mar, maxk))
            if maxk > 0:
                ratio_max = max(ratio_max, mar / (2 * maxk))
    out["p1_envelope"] = {"ok": not p1_bad, "n_bad": len(p1_bad),
                          "worst": max(p1_bad, default=None),
                          "maxAbsR_over_2maxk": round(ratio_max, 3)}

    # P2b: |sumR| < 1e-4 * ke at every stride sample.
    p2b_bad = [(r[0], r[6], r[4]) for r in g if r[0] in led and abs(r[6]) >= 1e-4 * max(r[4], 1)]
    fr = [abs(r[6]) / max(r[4], 1) for r in g if r[0] in led]
    out["p2b_global_debt"] = {"ok": not p2b_bad, "n_bad": len(p2b_bad),
                              "max_frac": max(fr, default=0.0),
                              "sumR_final": g[-1][6]}

    # P6: headroom in bits.
    mar_all = max(r[7] for r in g)
    mac_all = max(r[8] for r in g)
    out["p6_headroom"] = {"maxAbsR": mar_all, "maxAbsC": mac_all,
                          "bits_R": 63 - mar_all.bit_length(),
                          "bits_C": 63 - mac_all.bit_length()}

    # Epochs: per-body walks. cols: t id ring ct cl R Cx Cy k2 r_q
    ep = defaultdict(list)
    for r in load(os.path.join(dirpath, arm + ".epoch.tsv"), 10):
        ep[r[0]].append(r)
    epochs = sorted(ep)
    if not epochs:
        return out
    fin = epochs[-1]
    live = [r for r in ep[fin]]
    contacted = [r for r in live if r[3] > 0]
    # P2: slope of log(1+|R|) on log(1+ct) at the final epoch.
    if contacted:
        xs = [math.log1p(r[3]) for r in contacted]
        ys = [math.log1p(abs(r[5])) for r in contacted]
        out["p2_walk_slope"] = round(ols(xs, ys), 4)
        out["p2_n"] = len(contacted)
        gross = sum(abs(r[5]) for r in live)
        net = sum(r[5] for r in live)
        out["gross_absR"] = gross
        out["net_R"] = net
        out["cancellation"] = round(1 - abs(net) / max(gross, 1), 4)
        # P4: lower-id flow.
        out["p4_spearman_id_R"] = round(spearman([r[1] for r in contacted], [r[5] for r in contacted]), 4)
        # |R| vs ct and vs k2 (which explains the ledger?).
        out["spearman_absR_ct"] = round(spearman([r[3] for r in contacted], [abs(r[5]) for r in contacted]), 4)
        out["spearman_absR_k2"] = round(spearman([r[8] for r in contacted], [abs(r[5]) for r in contacted]), 4)
        out["spearman_absR_absk"] = round(
            spearman([int(math.isqrt(r[8])) for r in contacted], [abs(r[5]) for r in contacted]), 4)
    # Per-epoch ledger shape.
    out["epochs"] = {}
    for e in epochs:
        rs = [abs(r[5]) for r in ep[e]]
        rs.sort()
        k2s = [r[8] for r in ep[e]]
        maxk2 = max(k2s, default=0)
        q = lambda f: rs[int(f * (len(rs) - 1))] if rs else 0
        out["epochs"][str(e)] = {
            "n_live": len(rs), "p50": q(0.5), "p99": q(0.99), "max": rs[-1] if rs else 0,
            "maxAbsR_over_2maxk": round(rs[-1] / (2 * math.isqrt(maxk2)), 3) if rs and maxk2 else None,
            "n_ct_gt0": sum(1 for r in ep[e] if r[3] > 0),
        }
    # Deaths (D lines) and the hazard tail, c644-comparable.
    ev = open(os.path.join(dirpath, arm + ".events.tsv")).read().splitlines()
    dts = [int(l.split()[1]) for l in ev if l.startswith("D")]
    out["n_dead"] = len(dts)
    if dts:
        dts.sort()
        # hazard in two halves, per chronon, per live body.
        h = dts[-1] - dts[0] if len(dts) > 1 else 1
        n0 = 800
        out["lambda_all"] = round(len(dts) / (n0 * dts[-1]), 8) if dts[-1] else None
        mid = dts[len(dts) // 2]
        out["deaths_first_half"] = sum(1 for t in dts if t <= mid)
        out["deaths_second_half"] = len(dts) - out["deaths_first_half"]
    return out


def identity_check(dirpath, arm):
    """E arm: ke_all + sumR must be constant to the unit every chronon (no tide/walls)."""
    g = load(os.path.join(dirpath, arm + ".global.tsv"), 11)
    base = g[0][9] - g[0][6]
    worst = max(abs((r[9] - r[6]) - base) for r in g)
    return {"identity_max_abs_dev": worst, "ok": worst == 0,
            "contacts": sum(r[1] for r in g), "maxAbsR": max(r[7] for r in g)}


def main():
    dirpath = sys.argv[1]
    res = {}
    for arm in ["B_cold_s1", "C_th_s2", "D_pass_s1", "E_notide_s1"]:
        p = os.path.join(dirpath, arm + ".global.tsv")
        if os.path.exists(p) or os.path.exists(p + ".gz"):
            res[arm] = analyze(dirpath, arm)
    if os.path.exists(os.path.join(dirpath, "E_notide_s1.global.tsv")) or os.path.exists(os.path.join(dirpath, "E_notide_s1.global.tsv.gz")):
        res["E_identity"] = identity_check(dirpath, "E_notide_s1")
    # D: R must be identically 0.
    if "D_pass_s1" in res:
        g = load(os.path.join(dirpath, "D_pass_s1.global.tsv"), 10)
        res["D_pass_zero"] = {"maxAbsR": max(r[7] for r in g), "maxAbsC": max(r[8] for r in g),
                              "ok": max(r[7] for r in g) == 0 and max(r[8] for r in g) == 0}
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
