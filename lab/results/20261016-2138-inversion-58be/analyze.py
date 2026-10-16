#!/usr/bin/env python3
"""Summarize memwalk time series: the per-body plateau, its windows and slopes, the
catalogue, the dashboard ratio. Reads raw/*.txt written by the probe; prints one block
per arm and a summary line each (memsum: key=value)."""
import glob
import os
import re
import sys

ROW = re.compile(r"^mem: (.*)$")
KV = re.compile(r"(\w+)=(-?[\d.]+)")


def rows(path):
    out = []
    for line in open(path):
        m = ROW.match(line.strip())
        if not m:
            continue
        kv = dict(KV.findall(m.group(1)))
        out.append({k: float(v) for k, v in kv.items()})
    end = None
    for line in open(path):
        if line.startswith("end:"):
            end = dict(KV.findall(line))
            end = {k: float(v) for k, v in end.items()}
    return out, end


def slope(unit_rows, x, y, lo, hi):
    """Least-squares slope of y (B/body) per 10,000 units of x (game_s) in [lo, hi]."""
    pts = [(r[x], r[y]) for r in unit_rows if lo <= r[x] <= hi]
    if len(pts) < 3:
        return float("nan"), 0
    n = len(pts)
    mx = sum(p[0] for p in pts) / n
    my = sum(p[1] for p in pts) / n
    sxy = sum((p[0] - mx) * (p[1] - my) for p in pts)
    sxx = sum((p[0] - mx) ** 2 for p in pts)
    sl = sxy / sxx if sxx else float("nan")
    return sl * 10_000, n


here = os.path.dirname(os.path.abspath(__file__))
for path in sorted(glob.glob(os.path.join(here, "raw", "*.txt"))):
    name = os.path.basename(path).split(".")[0]
    rs, end = rows(path)
    if not rs:
        continue
    n_bodies = None
    head = next(l for l in open(path) if l.startswith("memwalk N="))
    hm = re.search(r"N=(\d+).*game_s=(\d+).*members=(\d+) seed=(\d+)", head)
    n_extra, game_target, members, seed = (int(hm.group(i)) for i in (1, 2, 3, 4)) if hm else (0, 0, 0, 0)
    bodies = int(re.search(r"(\d+) bodies", open(path).read()).group(1))
    pre = [r for r in rs if r["game_s"] < 12_000]
    # the wave: the largest rss jump between consecutive rows
    jumps = [(rs[i + 1]["rss_mb"] - rs[i]["rss_mb"], rs[i]["game_s"], rs[i + 1]["game_s"]) for i in range(len(rs) - 1)]
    jmax = max(jumps) if jumps else (0, 0, 0)
    post = [r for r in rs if r["game_s"] > jmax[2] and r["b_per_body"] > 0]
    if post:
        plat = sum(r["b_per_body"] for r in post) / len(post)
        drift = (max(r["b_per_body"] for r in post) - min(r["b_per_body"] for r in post)) / plat * 100
        lo, hi = post[0]["game_s"], post[-1]["game_s"]
        sl, cnt = slope(post, "game_s", "b_per_body", lo, hi)
    else:
        plat = drift = sl = float("nan")
        lo = hi = 0
    first, last = rs[0], rs[-1]
    dash_ratio = (last["b_per_body"] / last["dash"]) if last.get("dash") else float("nan")
    print(f"== {name}: N={n_extra} bodies={bodies} members={members} seed={seed} game_s={last['game_s']:.0f}")
    print(f"   build/pre-wave B/B {first['b_per_body']:.0f} -> {pre[-1]['b_per_body'] if pre else float('nan'):.0f}; wave at game_s [{jmax[1]:.0f},{jmax[2]:.0f}] (+{jmax[0]:.0f} MB)")
    print(f"   post-wave plateau {plat:.0f} B/B over [{lo:.0f},{hi:.0f}] game-s; drift {drift:.1f}%; slope {sl:+.1f} B/B per 10,000 game-s (n={cnt})")
    print(f"   catalogue {first['cat']:.0f} -> {last['cat']:.0f} (bodies {bodies}); dashboard {last['dash']:.0f} vs truth {last['b_per_body']:.0f} B/B = {dash_ratio:.1f}x")
    print(f"   kicks {last['kicks']:.0f} boundaries {last['boundaries']:.0f} lost {last['lost']:.0f} handoffs {last['handoffs']:.0f}; rss {first['rss_mb']:.1f} -> {last['rss_mb']:.1f} MB (hwm {end['hwm_mb'] if end else float('nan'):.1f})")
    if n_extra > 0:
        gs = last["game_s"]
        print(f"   memsum: arm={name} n={n_extra} seed={seed} members={members} game_s={gs:.0f} plateau_b={plat:.0f} slope_b_per_10k_gs={sl:+.1f} drift_pct={drift:.1f} cat_end={last['cat']:.0f} dash_ratio={dash_ratio:.2f} kick_per_b_gs={last['kicks'] / bodies / gs:.3e}")
    else:
        print(f"   memsum: arm={name} n=0 game_s={last['game_s']:.0f} rss_end_mb={last['rss_mb']:.1f} rss_start_mb={first['rss_mb']:.1f} cat_end={last['cat']:.0f}")
