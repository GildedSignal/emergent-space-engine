#!/usr/bin/env python3
"""Decompose the 10^5 rung's memory wall into channels, from the run's probe lines.

Channels at each probe: rss (VmRSS), store_mb (sum of per-body bytes_of: compiled
orbits, live bindings, history), scan_mb (held scans' candidate vecs at 224 B/cand),
hist_total (retired binding segments). The 'machinery' of 3eb3 is the subtraction
(rss - base - 2.1KB*hist)/kicks; ours removes store and scan first.

Usage: analyze.py <log> [<log> ...]   (one table per log, plus the regression)
"""
import re
import sys

BASE_MB = None  # per-log: rss at the first probe past the build


def load(path):
    global BASE_MB
    rows = []
    base = None
    for line in open(path):
        if not line.startswith(("probe:", "guard:")):
            continue
        d = dict(kv.split("=") for kv in line.split()[1:] if "=" in kv)
        r = {k: float(v) for k, v in d.items()}
        if base is None:
            base = r["rss_mb"]
        r["base_mb"] = base
        r["kind"] = line.split(":")[0]
        rows.append(r)
    return rows


def regress(ys, xs):
    n = len(xs)
    if n < 2:
        return 0.0, 0.0
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    slope = sxy / sxx if sxx else 0.0
    return slope, my - slope * mx


for path in sys.argv[1:]:
    rows = load(path)
    if not rows:
        print(f"{path}: no probe lines")
        continue
    print(f"== {path} ({len(rows)} probes, base {rows[0]['base_mb']:.0f} MB)")
    print("gs      rss   Δrss  store  scan  held  cand_max  hist_t  kicks   mint  exp  resid  KB/kick(sub3eb3)")
    for r in rows:
        drss = r["rss_mb"] - r["base_mb"]
        # 3eb3's subtraction: rss - base - 2.1KB*hist_total, over kicks
        sub = (r["rss_mb"] - r["base_mb"]) - 2.1e-6 * r["hist_total"] * 1e3 / 1e3 * 1.0
        sub = (r["rss_mb"] - r["base_mb"]) - (r["hist_total"] * 2.1 / 1024.0)
        kb_kick = sub * 1024.0 / r["kicks"] if r["kicks"] else 0.0
        resid = drss - (r["store_mb"] - rows[0]["store_mb"]) - r["scan_mb"]
        mark = ">" if r["kind"] == "guard" else " "
        print(f"{r['gs']:>7.0f} {r['rss_mb']:>6.0f} {drss:>6.0f} {r['store_mb']:>6.0f} {r['scan_mb']:>5.0f} {r['held']:>5.0f}"
              f" {r['scan_cand_max']:>9.0f} {r['hist_total']:>7.0f} {r['kicks']:>8.0f} {r['mints']:>6.0f} {r['expired']:>4.0f}"
              f" {resid:>6.0f} {kb_kick:>8.1f}{mark}")
    # regressions on the tail (last 2/3 of probes)
    tail = rows[len(rows) // 3 :]
    if len(tail) >= 3:
        kicks = [r["kicks"] for r in tail]
        resid = [r["rss_mb"] - r["base_mb"] - (r["store_mb"] - rows[0]["store_mb"]) - r["scan_mb"] for r in tail]
        s, c = regress(resid, kicks)
        print(f"residual slope: {s * 1024:.2f} KB per kick (intercept {c:.0f} MB, n={len(tail)})")
        mints = [r["mints"] for r in tail]
        s2, _ = regress(resid, mints)
        print(f"residual slope: {s2 * 1024:.1f} KB per mint (n={len(tail)})")
        rss_s, _ = regress([r["rss_mb"] for r in tail], [r["gs"] for r in tail])
        print(f"rss slope: {rss_s * 1000:.3f} MB per 1k gs (n={len(tail)})")
        scan_s, _ = regress([r["scan_mb"] for r in tail], [r["gs"] for r in tail])
        store_s, _ = regress([r["store_mb"] for r in tail], [r["gs"] for r in tail])
        print(f"scan slope: {scan_s * 1000:.3f} MB/1k gs; store slope: {store_s * 1000:.3f} MB/1k gs")
