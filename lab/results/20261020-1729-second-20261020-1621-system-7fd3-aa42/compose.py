#!/usr/bin/env python3
"""Compose the adjudication (run aa42, second author on 7fd3): both metrics — 7fd3's
compile/rebind-wall and a765's compile/from_state-stages — on both scenes (a765's
kick-bench arm and 7fd3's belt arm), from the census logs in out/."""
import re, pathlib

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"

def parse(path):
    d = {}
    for line in open(path):
        m = re.search(r'census\[space\]: mints (\d+) compile_ms ([\d.]+) fit_ms ([\d.]+) fs_ms ([\d.]+) reads_state (\d+) reads_radius (\d+) mint_own (\d+)', line)
        if m:
            d.update(mints=int(m.group(1)), compile_ms=float(m.group(2)), fit_ms=float(m.group(3)),
                     fs_ms=float(m.group(4)), reads_state=int(m.group(5)), reads_radius=int(m.group(6)),
                     mint_own=int(m.group(7)))
        m = re.search(r'ucensus\[universe\]: kicks (\d+) kick_ms ([\d.]+) rebinds (\d+) rebind_ms ([\d.]+) hist_queries (\d+) hist_hits (\d+)', line)
        if m:
            d.update(kicks=int(m.group(1)), kick_ms=float(m.group(2)), rebinds=int(m.group(3)),
                     rebind_ms=float(m.group(4)), hist_q=int(m.group(5)), hist_hit=int(m.group(6)))
    return d

def row(name, d):
    n, rb = d['mints'], d['rebinds']
    wall_us = d['rebind_ms'] * 1e3 / rb
    fs_us = d['fs_ms'] * 1e3 / n
    outside_us = wall_us - d['fs_ms'] * 1e3 / rb
    print(f"{name}: mints {n} rebinds {rb}")
    print(f"  compile/rebind-WALL   {d['compile_ms']/d['rebind_ms']:.3f}   (7fd3's metric)")
    print(f"  compile/from_state    {d['compile_ms']/d['fs_ms']:.3f}   (a765's metric: compile/(fit+compile+tail))")
    print(f"  us/mint: compile {d['compile_ms']*1e3/n:6.2f}  fit_key {d['fit_ms']*1e3/n:5.2f}  "
          f"fs_tail {(d['fs_ms']-d['compile_ms']-d['fit_ms'])*1e3/n:5.2f}  fs_total {fs_us:6.2f}")
    print(f"  rebind wall {wall_us:6.2f} us  -> outside-from_state {outside_us:6.2f} us "
          f"({100*outside_us/wall_us:.1f}% of the wall)")
    ext = d['reads_state'] + d['reads_radius']
    print(f"  reads/mint {ext/n:6.2f}  history hits/mint {d['hist_hit']/n:.3f} "
          f"(hit rate {d['hist_hit']}/{d['hist_q']})")

for f in ("bench-s1.log", "bench-s42.log", "bench-s7.log", "bench-s1b.log", "belt-10000.log", "belt-30000.log"):
    p = OUT / f
    if p.exists():
        row(f, parse(p))
