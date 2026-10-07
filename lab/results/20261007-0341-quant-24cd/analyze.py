#!/usr/bin/env python3
"""Per-frame analysis of the plane bench dumps (run 20261007-0341-quant-24cd).

Reads frames-<tag>.csv written by the patched xtask (PLANE_FRAME_DUMP) and prints:
- tail shape of engine_ms (p50/p99/p99.9/max) and frame_ms;
- burn vs coast engine cost (burn: nominal frame n with n % 240 < 20, the script's windows);
- worst frames and whether they sit in a burn window or at run start (warmup).

Usage: analyze.py tag [tag ...]
"""
import sys
import statistics as st


def pct(xs, q):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int((len(xs) - 1) * q + 0.5))]


for tag in sys.argv[1:]:
    rows = []
    with open(f"frames-{tag}.csv") as f:
        next(f)
        for line in f:
            n, wall, cpu, eng, view, js, wire, rtf = line.split(",")
            rows.append(dict(n=int(n), wall=float(wall), cpu=float(cpu), eng=float(eng),
                             view=float(view), frame=float(wall), rtf=float(rtf)))
    if not rows:
        print(f"{tag}: empty"); continue
    # warmup: first 30 frames excluded from tail stats (scene build, first gather)
    body = rows[30:]
    eng = [r["eng"] for r in body]
    burn = [r["eng"] for r in body if r["n"] % 240 < 20]
    coast = [r["eng"] for r in body if r["n"] % 240 >= 20]
    worst = sorted(rows, key=lambda r: -r["eng"])[:8]
    print(f"== {tag}  frames={len(rows)}")
    print(f"  engine_ms p50={pct(eng,0.5):.3f} p99={pct(eng,0.99):.3f} p999={pct(eng,0.999):.3f} max={max(eng):.3f}")
    print(f"  frame_ms p50={pct([r['frame'] for r in body],0.5):.3f} p99={pct([r['frame'] for r in body],0.99):.3f} max={max(r['frame'] for r in body):.3f}")
    if burn:
        print(f"  burn  n={len(burn):3d} p50={pct(burn,0.5):.3f} p99={pct(burn,0.99):.3f} max={max(burn):.3f}")
        print(f"  coast n={len(coast):3d} p50={pct(coast,0.5):.3f} p99={pct(coast,0.99):.3f} max={max(coast):.3f}")
        if coast and pct(coast, 0.99) > 0:
            print(f"  burn/coast p99 ratio = {pct(burn,0.99)/pct(coast,0.99):.2f}")
    print("  worst engine frames: " + ", ".join(f"#{r['n']}({r['eng']:.1f}ms{'B' if r['n']%240<20 else ''})" for r in worst))
