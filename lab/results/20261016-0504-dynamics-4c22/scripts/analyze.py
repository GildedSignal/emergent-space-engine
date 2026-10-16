#!/usr/bin/env python3
"""Analyse the batch's row files: the locals' comb structure and the two levers' effect.

A "storm" frame is one whose total events exceed 3x the median frame. For each file we report:
the train's peaks (frame, game-s, total, d2-attributable, composition), the peak spacing, the
height decay per period (the belt wave decays x0.72; a standing comb does not decay), the
d2-attributable max, and the totals (events summed over frames = work per game-second)."""
import pathlib
import re
import sys

D = pathlib.Path(__file__).resolve().parents[1] / "data"

ROW = re.compile(r"^row (\d+) ([\d.]+) ([\d.]+) (\d+) ([\d.]+)(?: (.*))?$")
DOLL = re.compile(r"(\d+):(\d+),(\d+),(\d+),(\d+)")


def load(name):
    rows = []
    for line in (D / f"{name}.txt").read_text().splitlines():
        m = ROW.match(line)
        if not m:
            continue
        att = {int(g[0]): [int(x) for x in g[1:]] for g in DOLL.findall(m.group(6) or "")}
        rows.append(dict(frame=int(m.group(1)), gs=float(m.group(2)), ms=float(m.group(3)),
                         ev=int(m.group(4)), lag=float(m.group(5)), att=att))
    return rows


def d2(r):
    a = r["att"].get(2, [0, 0, 0, 0])
    return sum(a)


def stats(name, warmup_frames=60):
    rows = [r for r in load(name) if r["frame"] >= warmup_frames]
    evs = sorted(r["ev"] for r in rows)
    med = evs[len(evs) // 2]
    storms = [r for r in rows if r["ev"] > 3 * max(med, 1)]
    # collapse adjacent storm frames into one peak each
    peaks = []
    for r in storms:
        if peaks and r["frame"] - peaks[-1]["frame"] <= 3:
            if r["ev"] > peaks[-1]["ev"]:
                peaks[-1] = r
        else:
            peaks.append(r)
    gaps = [b["gs"] - a["gs"] for a, b in zip(peaks, peaks[1:])]
    tot = sum(r["ev"] for r in rows)
    gs = rows[-1]["gs"] - rows[0]["gs"]
    print(f"== {name}: frames {len(rows)}, game-s {rows[0]['gs']:.0f}..{rows[-1]['gs']:.0f}")
    print(f"   events/frame med {med}, p99 {evs[int(0.99*(len(evs)-1))]}, max {evs[-1]}; "
          f"events/game-s {tot/gs:.1f}; ms p99 {sorted(r['ms'] for r in rows)[int(0.99*(len(rows)-1))]:.2f}, max {max(r['ms'] for r in rows):.2f}")
    if peaks:
        hs = [p["ev"] for p in peaks]
        print(f"   storms: {len(peaks)} peaks, heights {hs}")
        print(f"   first four: " + "; ".join(f"f{p['frame']} {p['gs']:.0f}gs ev{p['ev']} d2={d2(p)} {p['att'].get(2)}" for p in peaks[:4]))
        if gaps:
            print(f"   spacing game-s: {[round(g) for g in gaps[:10]]} (median {sorted(gaps)[len(gaps)//2]:.0f})")
        if len(hs) >= 6:
            import math
            # decay ratio per period from the first half to the last half medians
            h1 = sorted(hs[: len(hs) // 2])[len(hs) // 4]
            h2 = sorted(hs[len(hs) // 2 :])[len(hs) // 4]
            n = len(hs) // 2
            print(f"   height drift: median-of-first-half {h1} -> median-of-second-half {h2} "
                  f"({'standing' if h2 >= 0.9*h1 else 'decaying'}, per-period ratio {math.pow(h2/h1, 1/n):.3f})")
    return rows


if __name__ == "__main__":
    for name in sys.argv[1:]:
        stats(name)
