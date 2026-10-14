#!/usr/bin/env python3
"""Summarize the wave flights: one row an arm, the worst-frame exponent in N, and the P1-P6 verdicts."""
import re, sys, glob, os

here = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(here, "raw")


def arm(path):
    out = {}
    if not os.path.exists(path):
        return None
    for line in open(path):
        if line.startswith("ladder:"):
            out.update(kv for kv in re.findall(r"(\w+)=(\S+)", line))
        m = re.match(r"trace f=(\d+) ms=([\d.]+) ev=(\d+) lag=([\d.]+)", line)
        if m:
            out.setdefault("trace", []).append(tuple(float(x) for x in m.groups()))
        m = re.match(r"frames over the budget \(first 12\): \[(.*)\]", line)
        if m:
            out["over_at"] = [int(x) for x in re.findall(r"\d+", m.group(1))]
        m = re.match(r"worst frames \(frame, ms, events, lag s\): (.*)", line)
        if m:
            out["worst"] = [tuple(float(x) for x in re.findall(r"[-\d.]+", g)) for g in m.group(1).split("), ")]
        m = re.match(r"the player's doll \(frame, doll\): (.*)", line)
        if m:
            out["doll_at"] = m.group(1)
        m = re.match(r"belt: (\d+) bodies, first item \(game s\) min (\S+) p01 (\S+) p50 (\S+) p99 (\S+) max (\S+)", line)
        if m:
            out["belt"] = m.groups()
    return out or None


arms = {}
for f in sorted(glob.glob(os.path.join(R, "n*k_*.txt"))):
    name = os.path.basename(f)[:-4]
    a = arm(f)
    if a:
        arms[name] = a

print(f"{'arm':<18}{'max ms':>9}{'p99':>8}{'over':>6}{'lag s':>7}{'wall s':>8}{'MiB':>7}  worst_ev_frame")
for name, a in arms.items():
    print(f"{name:<18}{float(a.get('max_ms', 0)):>9.1f}{float(a.get('p99_ms', 0)):>8.2f}{a.get('over', '?'):>6}"
          f"{float(a.get('lag_s', 0)):>7.2f}{float(a.get('wall_s', 0)):>8.0f}{float(a.get('foot_end_mb', 0)):>7.0f}"
          f"  {max([w[2] for w in a.get('worst', [])] or [0]):.0f}")
    if "worst" in a:
        print("   worst:", a["worst"][:5])
    if "over_at" in a:
        print("   over at frames:", a["over_at"])
    if "doll_at" in a:
        print("   doll:", a["doll_at"])

w = {k: float(v.get("max_ms", 0)) for k, v in arms.items()}
ev = {k: max([t[2] for t in v.get("trace", [(0, 0, 0, 0)])] or [0]) for k, v in arms.items()}
if "n100k_burn_s1" in w and "n200k_burn_s1" in w and w["n100k_burn_s1"] > 0:
    import math
    e = math.log(w["n200k_burn_s1"] / w["n100k_burn_s1"]) / math.log(2)
    print(f"\nexponent of the worst frame, 10^5 -> 2x10^5 burn: {e:.2f} (linear drain would be 1.0)")
if "n200k_burn_s1" in arms:
    a = arms["n200k_burn_s1"]
    tr = a.get("trace", [])
    if tr:
        peak = max(tr, key=lambda t: t[1])
        late = [t for t in tr if t[0] * (1 / 60.0) > 155]
        print(f"2x10^5 burn: peak trace frame {peak}; after 155 s wall: max ms {max([t[1] for t in late] or [0]):.2f}, "
              f"frames over 12 in trace: {sum(1 for t in late if t[1] > 12)} of {len(late)} sampled")
bf = arm(os.path.join(R, "belt_first_200k.txt"))
if bf and "belt" in bf:
    print("\nbelt: {} bodies, first item (game s) min {} p01 {} p50 {} p99 {} max {}".format(*bf["belt"]))
