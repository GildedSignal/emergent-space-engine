#!/usr/bin/env python3
"""Parse birth_rail output (+ ES_BIRTH_SPLIT stderr) into the birth-rail table.

Input: a log file with, per rep, lines
  [birth] ladder extra=<N> draw_add=<ns>ns
  [birth] start n=<n> alloc=<ns> plan=<ns> requeue=<ns> fleet=<ns> rekey=<ns> total=<ns>
and stdout lines
  N=<n> build <s> s  <us> us/body(incl fixed)  slope vs N=<n0>: <us> us/body

The per-body split for each N>0 takes the FASTEST rep's stderr pair (matching the
stdout best-rep choice is not possible from separate streams, so we take each
stream's own min; reps are homogeneous, and we report the spread).
"""
import re
import sys
from collections import defaultdict

log = open(sys.argv[1]).read()

ladder = defaultdict(list)   # extra -> [ns]
start = defaultdict(list)    # n -> [(alloc, plan, requeue, fleet, rekey, total)]
for m in re.finditer(r"\[birth\] ladder extra=(\d+) draw_add=(\d+)ns", log):
    ladder[int(m.group(1)) + 28].append(int(m.group(2)))
for m in re.finditer(
    r"\[birth\] start n=(\d+) alloc=(\d+) plan=(\d+) requeue=(\d+) fleet=(\d+) rekey=(\d+) total=(\d+)", log
):
    start[int(m.group(1))].append(tuple(int(m.group(i)) for i in range(2, 8)))

print(f"{'N':>8} {'us/body total':>13} {'draw+add':>9} {'plan':>8} {'requeue':>8} {'alloc':>7} {'rekey':>7} {'fleet(fixed)':>12} {'reps':>4}")
tot = {}
for m in re.finditer(r"N=\s*(\d+) build\s+([\d.]+) s\s+([\d.]+) us/body", log):
    tot[int(m.group(1))] = float(m.group(2)) * 1e6  # us for the best rep

for n in sorted(set(ladder) | set(start)):
    rows = start.get(n, [])
    lad = min(ladder.get(n, [0])) if ladder.get(n) else None
    if not rows:
        continue
    best = min(rows, key=lambda r: r[5])  # fastest total rep
    alloc, plan, requeue, fleet, rekey, total = best
    f = lambda ns: ns / 1e3 / max(n, 1)  # us per body
    t = tot.get(n, float("nan")) / max(n, 1)
    print(
        f"{n:>8} {t:>13.2f} "
        + (f"{f(lad):>9.2f}" if lad else f"{'-':>9}")
        + f"{f(plan):>8.2f} {f(requeue):>8.2f} {f(alloc):>7.2f} {f(rekey):>7.2f} {fleet/1e3:>12.1f} {len(rows):>4}"
    )

print("\nrep spread (us/body, per stage): fastest and slowest rep per N")
for n in sorted(start):
    rows = start[n]
    per = [[v / 1e3 / n for v in r[:5]] for r in rows]
    lo = [min(c) for c in zip(*per)]
    hi = [max(c) for c in zip(*per)]
    print(f"  N={n}: alloc {lo[0]:.2f}-{hi[0]:.2f} plan {lo[1]:.2f}-{hi[1]:.2f} requeue {lo[2]:.2f}-{hi[2]:.2f} fleet {lo[3]*n/1e3:.0f}-{hi[3]*n/1e3:.0f}us rekey {lo[4]:.2f}-{hi[4]:.2f}")
