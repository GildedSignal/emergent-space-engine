#!/usr/bin/env python3
"""Scorecard: parse the two arm files, recompute every derived number in the dossier."""
import re

def ladder(path):
    line = [l for l in open(path) if l.startswith("ladder: ")][-1]
    return {k: (float(v) if "." in v or "-" in v and not v.lstrip("-").isdigit() else int(v))
            for k, v in re.findall(r"(\w+)=([-\d.e+]+)", line)}

def txt(path):
    return open(path).read()

def worst_events(path):
    """(worst-frame events, median events/frame, over-frames inside the wave >= 400 / printed)."""
    t = txt(path)
    m = re.search(r"events/frame p50 (\d+) p99 (\d+) max (\d+)", t)
    med = int(m.group(1))
    wf = re.search(r"worst frames.*?:\s*(.*)", t).group(1)
    worst = max(int(e) for _, _, e, _ in re.findall(r"\((\d+), ([\d.]+), (\d+), ([\d.]+)\)", wf))
    ov = [int(f) for f in re.findall(r"-?\d+", re.search(r"frames over the budget \(first 12\): \[(.*?)\]", t).group(1))]
    in_wave = sum(1 for f in ov if f >= 400)
    return worst, med, in_wave, len(ov)

a1, a2 = ladder("arm_1e5.txt"), ladder("arm_2e5.txt")
w1, m1, c1, t1 = worst_events("arm_1e5.txt")
w2, m2, c2, t2 = worst_events("arm_2e5.txt")
print(f"10^5   : p50 {a1['p50_ms']:.3f} ms  p99 {a1['p99_ms']:.3f}  max {a1['max_ms']:.1f}  "
      f"over {a1['over']}/{a1['frames']} ({100*a1['over']/a1['frames']:.1f}%)  lag {a1['lag_s']:.1f} s")
print(f"2x10^5 : p50 {a2['p50_ms']:.3f} ms  p99 {a2['p99_ms']:.3f}  max {a2['max_ms']:.1f}  "
      f"over {a2['over']}/{a2['frames']} ({100*a2['over']/a2['frames']:.1f}%)  lag {a2['lag_s']:.1f} s")
print(f"worst-frame events: {w1:,} vs {m1} median ({w1/m1:.0f}x) (10^5); {w2:,} vs {m2} median ({w2/m2:.0f}x) (2x10^5)")
print(f"P1 p50 <= 3 ms            : {a1['p50_ms']:.2f} / {a2['p50_ms']:.2f}  -> FAIL on letter "
      f"({100*a1['p50_ms']/12:.0f}%/{100*a2['p50_ms']/12:.0f}% of budget)")
print(f"P3 worst/p50 events >= 20x: {w1/m1:.0f}x / {w2/m2:.0f}x                        -> {'HELD' if w1/m1 >= 20 and w2/m2 >= 20 else 'FAILED'}")
print(f"P4 max ratio in [1.5, 8]  : {a2['max_ms']/a1['max_ms']:.2f}                         -> "
      f"{'HELD' if 1.5 <= a2['max_ms']/a1['max_ms'] <= 8 else 'FAILED'}")
print(f"p99 / budget              : {a1['p99_ms']/12:.1f}x / {a2['p99_ms']/12:.1f}x")
print(f"P2 over-frames cluster    : {c1}/{t1} (10^5) and {c2}/{t2} (2x10^5) printed over-frames "
      f"inside the wave window (frame >= 400) -> HALF-HELD (shipped code prints only the first 12)")
