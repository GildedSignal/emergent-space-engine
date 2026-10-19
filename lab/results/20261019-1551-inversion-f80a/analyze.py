#!/usr/bin/env python3
"""Parse the run's probe lines into the dossier's window table (20261019-1551-inversion-f80a)."""
import re, sys, pathlib

root = pathlib.Path(__file__).resolve().parent
LOGS = root / "work" / "logs"
PROBE = re.compile(
    r"probe gs=(\d+) rss_mb=(\d+) hwm_mb=(\d+) held=(\d+) mints=(\d+) answers=(\d+) "
    r"expired=(\d+) hist_gt1=(\d+) hist_total=(\d+) hist_max=(\d+)")
WINDOWS = [(0, 15e3), (15e3, 40e3), (40e3, 60e3), (60e3, 95e3), (95e3, 130e3),
           (130e3, 200e3), (200e3, 1e9)]

def parse(fn):
    rows = []
    for line in (LOGS / fn).read_text().splitlines():
        m = PROBE.search(line)
        if m:
            g = list(map(int, m.groups()))
            rows.append(dict(gs=g[0], rss=g[1], hwm=g[2], held=g[3], mints=g[4],
                             answers=g[5], expired=g[6], gt1=g[7], total=g[8], hmax=g[9]))
    tail = {}
    for line in (LOGS / fn).read_text().splitlines():
        if line.startswith(("game ", "scans:", "ladder:", "guard:", "memory:", "rung ")):
            tail[line.split(":")[0]] = line
    return rows, tail

def slope(rows, lo, hi, key):
    a = [r for r in rows if lo <= r["gs"] < hi]
    if len(a) < 2:
        return None
    dg = a[-1]["gs"] - a[0]["gs"]
    if dg <= 0:
        return None
    return (a[-1][key] - a[0][key]) * 1000.0 / dg

for fn, label in [("off_pruned.log", "OFF (TTL unset, prune restored = shipped)"),
                  ("on_ttl16.log", "ON (TTL=16, prune restored)")]:
    rows, tail = parse(fn)
    if not rows:
        print(f"== {label}: NO PROBES =="); continue
    print(f"== {label} ({len(rows)} probes, to gs {rows[-1]['gs']:,}) ==")
    print("  window gs        rss MB    MB/1k gs   held(max)  hist_total(end)  gt1(end)   +bindings/1k gs")
    for lo, hi in WINDOWS:
        w = [r for r in rows if lo <= r["gs"] < hi]
        if len(w) < 2:
            continue
        s_rss = slope(rows, lo, hi, "rss"); s_tot = slope(rows, lo, hi, "total")
        print(f"  {lo:>9.0f}-{hi if hi < 1e9 else rows[-1]['gs']:>9,.0f}  {w[-1]['rss']:>8}  "
              f"{s_rss if s_rss is not None else float('nan'):>8.2f}  {max(r['held'] for r in w):>6}  "
              f"{w[-1]['total']:>12,}  {w[-1]['gt1']:>8,}  {s_tot if s_tot is not None else float('nan'):>8.1f}")
    last = rows[-1]
    print(f"  end: gs={last['gs']:,} rss={last['rss']} hwm={last['hwm']} held={last['held']} "
          f"mints={last['mints']} answers={last['answers']} expired={last['expired']} "
          f"hist_total={last['total']:,} hist_gt1={last['gt1']:,} hist_max={last['hmax']} "
          f"({last['total']/30076:.2f} bindings/body)")
    for k in ("guard:", "scans:", "game ", "ladder:"):
        if k in tail:
            print("  " + tail[k][:400])
    print()
