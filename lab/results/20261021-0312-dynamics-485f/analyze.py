#!/usr/bin/env python3
"""Carry-ledger + rattle-structure analysis for 20261021-0312-dynamics-485f.
Reads the beltledger TSVs, prints a compact report, writes report.json."""
import json, math, sys, os
from collections import defaultdict

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "work")
OUT = {}

def load(tag, name):
    p = os.path.join(BASE, tag, name)
    if not os.path.exists(p):
        return None
    with open(p) as f:
        head = f.readline().rstrip("\n").split("\t")
        rows = [dict(zip(head, l.rstrip("\n").split("\t"))) for l in f if l.strip()]
    return rows

def fl(x):
    return float(x)

def fit_alpha(contacts, vals):
    """OLS slope of log10(val) vs log10(contacts), over rows with val>0."""
    xs, ys = [], []
    for c, v in zip(contacts, vals):
        if c > 0 and v > 0:
            xs.append(math.log10(c)); ys.append(math.log10(v))
    n = len(xs)
    if n < 4:
        return None, None
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    a = sxy / sxx if sxx > 0 else 0.0
    b = my - a * mx
    ssr = sum((y - (a * x + b)) ** 2 for x, y in zip(xs, ys))
    sst = sum((y - my) ** 2 for y in ys)
    r2 = 1 - ssr / sst if sst > 0 else 0.0
    return a, r2

for tag in sys.argv[1:]:
    rep = {}
    s = load(tag, "summary.tsv")
    if not s:
        continue
    for r in s:
        for k in ("t", "contacts", "c_win", "alive", "n_r10", "n_r3", "res_sum", "res_abs", "res_abs_alive", "res_max", "res_med", "res_p99", "car_abs", "car_max", "dead_new"):
            r[k] = int(r[k])
        r["ke_dev"] = fl(r["ke_dev"])
    # regime split: storm = up to the quench time (contacts-rate peak's half-decay), use t<=49152
    storm = [r for r in s if r["t"] <= 49152 and r["contacts"] > 0]
    late = [r for r in s if r["t"] > 49152 and r["contacts"] > 0]
    a_all, r2_all = fit_alpha([r["contacts"] for r in s], [r["res_abs"] for r in s])
    a_storm, r2_s = fit_alpha([r["contacts"] for r in storm], [r["res_abs"] for r in storm])
    a_late, r2_l = fit_alpha([r["contacts"] for r in late], [r["res_abs"] for r in late]) if late else (None, None)
    last = s[-1]
    mean_res = [(r["t"], r["res_abs_alive"] / max(r["alive"], 1)) for r in s]
    # P2: stationarity after 70k
    def mean_res_at(lo, hi):
        v = [m for t, m in mean_res if lo < t <= hi]
        return sum(v) / len(v) if v else 0
    m70 = mean_res_at(60000, 70000)
    mlast = mean_res_at(max(0, last["t"] - 16000), last["t"])
    # P3: bias
    biases = [abs(r["res_sum"]) / r["res_abs"] for r in s if r["res_abs"] > 0]
    # P5: headroom
    rep["walk"] = {
        "alpha_all": a_all, "r2_all": r2_all, "alpha_storm": a_storm, "r2_storm": r2_s,
        "alpha_late": a_late, "r2_late": r2_l,
        "res_abs_last": last["res_abs"], "contacts_last": last["contacts"],
        "alive_last": last["alive"],
        "mean_abs_res_60_70k": m70, "mean_abs_res_last16k": mlast,
        "station_ratio": (mlast / m70) if m70 else None,
        "res_max_last": last["res_max"], "car_max_last": last["car_max"],
        "headroom_energy_bits": 63 - last["res_max"].bit_length() if last["res_max"] > 0 else 63,
        "headroom_mom_bits": 63 - last["car_max"].bit_length() if last["car_max"] > 0 else 63,
        "max_bias_ratio": max(biases) if biases else None,
        "bias_last": biases[-1] if biases else None,
        "ke_dev_last": last["ke_dev"],
        "n_r3_last": last["n_r3"], "dead_total": sum(r["dead_new"] for r in s),
    }
    # rattle structure (winchron)
    w = load(tag, "winchron.tsv")
    if w:
        for r in w:
            for k in ("t", "contacts64", "distinct", "hot", "partner_med", "partner_max", "res_abs_hot"):
                r[k] = int(r[k])
            r["top_share"] = fl(r["top_share"])
        lastw = w[-6:]
        rep["rattle"] = {
            "windows": len(w),
            "c64_mean": sum(r["contacts64"] for r in w) / len(w),
            "hot_mean": sum(r["hot"] for r in w) / len(w),
            "pmed_max": max(r["partner_med"] for r in w),
            "pmed_last": sum(r["partner_med"] for r in lastw) / max(len(lastw), 1),
            "pmax_last": max(r["partner_max"] for r in lastw),
            "top_share_max": max(r["top_share"] for r in w),
            "contacts_per_hot_per_ch": (sum(r["contacts64"] for r in w) / len(w)) / max(sum(r["hot"] for r in w) / len(w), 1) / 64,
        }
    # pairs over the run
    p = load(tag, "pairs.tsv")
    if p:
        cnts = sorted((int(r["c_run"]) for r in p), reverse=True)
        tot = sum(cnts)
        by_body = defaultdict(set)
        for r in p:
            by_body[int(r["a"])].add(int(r["b"]))
            by_body[int(r["b"])].add(int(r["a"]))
        top10 = sum(cnts[:10]) / tot if tot else 0
        top1 = cnts[0] / tot if tot else 0
        # lifetime partner diversity of the 32 hottest bodies (final.tsv c_cum)
        f = load(tag, "final.tsv")
        hotids = sorted((int(r["id"]) for r in f), key=lambda i: -int(next(x for x in f if int(x["id"]) == i)["c_cum"]))[:32] if f else []
        div = [len(by_body.get(i, ())) for i in hotids]
        rep["pairs"] = {
            "distinct_pairs": len(cnts), "total": tot, "top1_share": top1, "top10_share": top10,
            "hot32_lifetime_partners_med": sorted(div)[len(div) // 2] if div else None,
            "hot32_lifetime_partners_min": min(div) if div else None,
        }
    # hot trace: per-body oscillation vs walk inside the window
    h = load(tag, "hottrace.tsv")
    if h:
        per = defaultdict(list)
        for r in h:
            per[int(r["id"])].append(int(r["res"]))
        stats = []
        for i, v in per.items():
            if len(v) < 64:
                continue
            rng = max(v) - min(v)
            med = sorted(v)[len(v) // 2]
            deltas = [v[k + 1] - v[k] for k in range(len(v) - 1)]
            # lag-1 autocorr of deltas
            n = len(deltas)
            md = sum(deltas) / n
            num = sum((deltas[k] - md) * (deltas[k + 1] - md) for k in range(n - 1))
            den = sum((d - md) ** 2 for d in deltas)
            ac = num / den if den > 0 else 0.0
            signs = sum(1 for k in range(n - 1) if deltas[k] * deltas[k + 1] < 0) / (n - 1)
            # first vs second half mean: drift within window?
            h1 = sum(v[: len(v) // 2]) / (len(v) // 2)
            h2 = sum(v[len(v) // 2 :]) / (len(v) - len(v) // 2)
            stats.append({"id": i, "range": rng, "med_abs": abs(med), "lag1_ac": ac, "sign_alt": signs, "half_drift": h2 - h1})
        if stats:
            stats.sort(key=lambda x: -x["range"])
            rep["hottrace"] = {
                "n": len(stats),
                "range_med": sorted(x["range"] for x in stats)[len(stats) // 2],
                "range_max": stats[0]["range"],
                "lag1_ac_med": sorted(x["lag1_ac"] for x in stats)[len(stats) // 2],
                "sign_alt_med": sorted(x["sign_alt"] for x in stats)[len(stats) // 2],
                "half_drift_over_range_med": sorted(abs(x["half_drift"]) / max(x["range"], 1) for x in stats)[len(stats) // 2],
                "worst": stats[0],
            }
    # per-body walk: consecutive-snapshot |dres| vs dcontacts for hot bodies
    sn = load(tag, "snapshots.tsv")
    if sn:
        for r in sn:
            r["t"] = int(r["t"]); r["id"] = int(r["id"]); r["res"] = int(r["res"]); r["c_cum"] = int(r["c_cum"])
        byid = defaultdict(list)
        for r in sn:
            byid[r["id"]].append(r)
        xs, ys = [], []
        ratios = []
        for i, rows in byid.items():
            rows.sort(key=lambda r: r["t"])
            for a, b in zip(rows, rows[1:]):
                dc = b["c_cum"] - a["c_cum"]
                dr = abs(b["res"] - a["res"])
                if dc >= 50 and dr > 0:
                    xs.append(math.log10(dc)); ys.append(math.log10(dr))
                    ratios.append(dr / math.sqrt(dc))
        if len(xs) > 20:
            n = len(xs)
            mx, my = sum(xs) / n, sum(ys) / n
            sxx = sum((x - mx) ** 2 for x in xs)
            sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
            a_pb = sxy / sxx if sxx > 0 else 0.0
            ssr = sum((y - (a_pb * x + (my - a_pb * mx))) ** 2 for x, y in zip(xs, ys))
            sst = sum((y - my) ** 2 for y in ys)
            rep["perbody_walk"] = {
                "n_intervals": n, "alpha": a_pb, "r2": 1 - ssr / sst if sst > 0 else 0,
                "dr_over_sqrt_dc_med": sorted(ratios)[len(ratios) // 2],
                "dr_over_sqrt_dc_p90": sorted(ratios)[int(len(ratios) * 0.9)],
            }
    OUT[tag] = rep

print(json.dumps(OUT, indent=1, default=str))
with open(os.path.join(BASE, "report.json"), "w") as f:
    json.dump(OUT, f, indent=1, default=str)
