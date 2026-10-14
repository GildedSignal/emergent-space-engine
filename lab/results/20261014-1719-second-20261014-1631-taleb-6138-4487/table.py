#!/usr/bin/env python3
"""The held-pull fix's record: one row an arm (worst frame, over-budget frames, events a frame),
the wave region's own worst, the digests at the canonical cuts, and the F1-F8 verdicts."""
import re, os, glob

here = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(here, "raw")


def arm(path):
    out = {}
    if not os.path.exists(path):
        return None
    for line in open(path):
        if line.startswith("ladder:"):
            out.update(re.findall(r"(\w+)=(\S+)", line))
        m = re.match(r"trace f=(\d+) ms=([\d.]+) ev=(\d+) lag=([\d.]+)", line)
        if m:
            out.setdefault("trace", []).append(tuple(float(x) for x in m.groups()))
        m = re.match(r"cut (\S+) game-s: digest (\S+) \[settle \S+ s, kicks (\d+), events (\d+), encounters (\d+)", line)
        if m:
            out.setdefault("cuts", []).append(m.groups())
        m = re.search(r"events/frame p50 (\d+) p99 (\d+) max (\d+)", line)
        if m:
            out["evmax"] = m.group(3)
        m = re.match(r"worst frames \(frame, ms, events, lag s\): (.*)", line)
        if m:
            out["worst"] = [tuple(float(x) for x in re.findall(r"[-\d.]+", g)) for g in m.group(1).split("), ")]
    return out or None


arms = {}
for f in sorted(glob.glob(os.path.join(R, "*.txt"))):
    name = os.path.basename(f)[:-4]
    a = arm(f)
    if a and "max_ms" in a:
        arms[name] = a

print(f"{'arm':<34}{'max ms':>9}{'p99':>8}{'over':>6}{'evmax':>8}{'lag':>6}{'MiB':>6}  wave-region worst (8300-8799)")
for name, a in sorted(arms.items()):
    tr = [t for t in a.get("trace", []) if 8300 <= t[0] <= 8799]
    wave = max([t[1] for t in tr] or [0])
    print(f"{name:<34}{float(a['max_ms']):>9.1f}{float(a['p99_ms']):>8.2f}{a.get('over','?'):>6}"
          f"{a.get('evmax', a.get('events_max','?')):>8}{float(a.get('lag_s',0)):>6.2f}{float(a.get('foot_end_mb',0)):>6.0f}  {wave:.2f}")

print("\ndigests at the canonical cuts (game-s -> digest[:16], kicks/events/encounters):")
for name, a in sorted(arms.items()):
    for c in a.get("cuts", []):
        print(f"  {name:<34}{c[0]:>6}  {c[1][:16]}  kicks {c[2]:>7} events {c[3]:>7} enc {c[4]:>5}")

print("\nframe_digest (the shipped certificate, 8 scripted flights x 4 schedules):")
for f, tag in [("fd_pristine.txt", "pristine "), ("fd_fixed_default.txt", "fixed    "), ("fd_fixed_forced.txt", "forced-0 ")]:
    p = os.path.join(R, f)
    if os.path.exists(p):
        ds = re.findall(r"\| ([0-9a-f]{32}) \|", open(p).read())
        print(f"  {tag}: {len(ds)} digests, first {ds[0][:16] if ds else '-'}")
same = all(len(set(x)) == 1 for x in zip(*[re.findall(r"\| ([0-9a-f]{32}) \|", open(os.path.join(R, f)).read())
                                           for f in ["fd_pristine.txt", "fd_fixed_default.txt", "fd_fixed_forced.txt"]
                                           if os.path.exists(os.path.join(R, f))]))
print(f"  pristine == fixed == forced on every flight: {same}")
