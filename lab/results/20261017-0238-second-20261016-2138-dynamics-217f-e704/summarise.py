#!/usr/bin/env python3
"""Summarise RESULT lines from flight logs: per (scene, arm), median across reps."""
import re
import sys
from collections import defaultdict
from statistics import median

runs = []
for path in sys.argv[1:]:
    arm = scene = None
    for line in open(path):
        if line.startswith("# flight "):
            keys = dict(re.findall(r"(\w+)=([\w.]+)", line))
            scene = f"{keys.get('mode','?')}-c{keys.get('cells','?')}-p{keys.get('per','?')}-h{int(keys.get('n1','0'))*int(keys.get('n2','0'))}"
        m = re.match(r"RESULT (\S.*)", line)
        if m:
            kv = dict(re.findall(r"(\w+)=(\S+)", m.group(1)))
            runs.append((scene, kv))

groups = defaultdict(list)
for scene, kv in runs:
    groups[(scene, kv["arm"])].append(kv)

num = lambda kv, k: float(kv[k]) if "=" not in kv.get(k, "=nan") else float("nan")
print(f"{'scene':<24} {'arm':<8} {'n':>2} {'rb':>5} {'E':>6} {'regs':>6} {'avoid':>7} {'wasted':>10} {'merges':>7} {'chr/s':>8} {'wall_s':>8}")
for (scene, arm), kvs in sorted(groups.items()):
    med = lambda k: median([num(kv, k) for kv in kvs])
    print(
        f"{scene:<24} {arm:<8} {len(kvs):>2} {med('rollbacks'):>5.0f} {med('escal'):>6.0f} "
        f"{med('regions'):>6.0f} {med('avoided'):>7.0f} {med('wasted'):>10.0f} {med('merges'):>7.0f} "
        f"{med('chr_per_s'):>8.0f} {med('wall_ms')/1e3:>8.1f}"
    )
# digest agreement per scene
print("\ndigests:")
dig = defaultdict(set)
for scene, kv in runs:
    if "digest" in kv:
        dig[scene].add(kv["digest"])
for scene, ds in sorted(dig.items()):
    print(f"  {scene}: {len(ds)} distinct across {sum(1 for s,_ in runs if s==scene and 'digest' in _)} runs"
          + ("  ALL-IDENTICAL" if len(ds) == 1 else "  *** DIFFER ***"))
