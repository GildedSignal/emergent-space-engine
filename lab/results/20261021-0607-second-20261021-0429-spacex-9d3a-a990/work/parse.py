#!/usr/bin/env python3
"""Pull run 20261021-0607's numbers out of the arm logs (rows vs oracle vs none, 1e5-3e5)."""
import re, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent.parent
args = [HERE / "work"]
rows = {}
for p in args:
    for f in sorted(p.glob("arm_*.txt")):
        blob = f.read_text()
        key = f.name
        rows.setdefault(key, []).append(blob)
        rows[key] = blob

def g(blob, pat):
    m = re.search(pat, blob)
    return m.groups() if m else None

print(f"{'arm':<28}{'bodies':>8}{'0postB':>10}{'live@1f/1s/5s/20s/cap':>26}{'reb@60/300/1200/cap':>24}{'viewR':>10}{'engR':>10}")
for key, blob in sorted(rows.items()):
    n = g(blob, r"rcensus: n=(\d+) ")
    if not n:
        continue
    zp = g(blob, r"zero_post_build=(\d+) build_born=(\d+)")
    live = g(blob, r"rcensus live fraction.*?: ([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+)")
    rb = g(blob, r"rebuilds by slack \[[^\]]*\]: build_born=(\d+)_(\d+)_(\d+)_(\d+)_(\d+)")
    rd = g(blob, r"orbit_view=(\d+) readout_engine=(\d+) readout_view=(\d+)")
    zpb, bb = int(zp[0]), int(zp[1])
    lv = "/".join(f"{float(x):.3f}" for x in live) if live else "-"
    rbs = "/".join(rb[i] for i in (1, 2, 3, 4)) if rb else "-"
    print(f"{key:<28}{int(n[0]):>8}{zpb:>7}/{bb:<7}{lv:>26}{rbs:>24}{int(rd[0]) + int(rd[2]):>10}{rd[1]:>10}")

print()
# The demotion arithmetic (the gold number): returns per build-born body per wall-second, and the
# 1e9 core bill at the compile cost the rung priced (4.4 us, c4d3), against the oracle's ~440.
for key, blob in sorted(rows.items()):
    if "rows" not in key:
        continue
    fr = g(blob, r"frames=(\d+)")
    rb = g(blob, r"rebuilds by slack \[[^\]]*\]: build_born=(\d+)_(\d+)_(\d+)_(\d+)_(\d+)")
    bb = g(blob, r"build_born=(\d+)")
    if not (fr and rb and bb):
        continue
    fr, bb = int(fr[0]), int(bb[0])
    wall_s = fr / 60.0
    for slack, cnt in zip(("60", "300", "1200", "16384"), rb[1:5]):
        rate = int(cnt) / bb / wall_s
        print(f"{key}: slack {slack:>5}f -> {rate:.5f} returns/body/wall-s -> {rate * 1e9 * 4.4e-6:7.1f} cores at 1e9 (compile 4.4 us)")
    print()
