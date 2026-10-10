#!/usr/bin/env python3
"""Check the held-out predictions against run_a/b/c.json."""
import json, math
from collections import defaultdict

A = json.load(open("run_a.json"))
B = json.load(open("run_b.json"))
C = json.load(open("run_c.json"))

print("=== A: retention law (36 runs: lambda x r_q x 3 seeds) ===")
print(f"{'lam':>5} {'r_q':>6} | {'keep@4k':>8} {'ttlR@4k':>8} {'ttl_rq@4k':>9} {'exact@4k':>9} "
      f"| {'pred lam*min(rq,R)':>18} | {'misses kF/R/rq/ex/half':>24}")
groups = defaultdict(list)
for r in A:
    groups[(r["lambda"], r["rq"])].append(r)
ok1 = ok2 = ok4 = True
for (lam, rq), rs in sorted(groups.items()):
    last = [x["checkpoints"][-1] for x in rs]
    def avg(policy):
        return sum(row[policy] for row in last) / len(last)
    pred = lam * min(rq, 1000.0)
    m = [sum(x["misses"].get(p, 0) for x in rs) for p in
         ("keep_forever", "ttl_R", "ttl_rq", "exact", "ttl_half")]
    grow = avg("keep_forever") / max(avg("ttl_rq"), 1e-9)
    ok1 &= avg("keep_forever") > 3 * max(avg("ttl_rq"), 1.0)
    ok2 &= abs(avg("ttl_rq") - pred) <= 3 * math.sqrt(max(pred, 1.0)) + 2
    ok4 &= (m[0] == 0 and m[1] == 0 and m[2] == 0 and m[3] == 0 and m[4] > 0)
    print(f"{lam:>5} {rq:>6} | {avg('keep_forever'):>8.1f} {avg('ttl_R'):>8.1f} "
          f"{avg('ttl_rq'):>9.2f} {avg('exact'):>9.2f} | {pred:>18.2f} | {m!s:>24}")
print(f"P1 keep-forever grows (>=3x flatline at t=4000): {ok1}")
print(f"P2 flatline = lambda*min(rq,R) within 3*sqrt(n)+2: {ok2}")
print(f"P4 zero misses at every policy except ttl_half, ttl_half misses: {ok4}")

# over-retention factor of ttl_R vs exact, per rq
print("\nover-retention ttl_R/exact (memory wasted by the naive doll bound):")
for (lam, rq), rs in sorted(groups.items()):
    last = [x["checkpoints"][-1] for x in rs]
    a = sum(row["ttl_R"] for row in last) / len(last)
    b = sum(row["exact"] for row in last) / len(last)
    print(f"  lam={lam:<5} rq={rq:<6}: {a:>8.1f} / {b:>8.1f} = {a / max(b, 1e-9):>7.2f}x  (R/min(rq,R) = {1000.0 / min(rq, 1000.0):>6.2f})")

print("\n=== B: frontier vs volume (player at v=0.5c, action every 10 ticks) ===")
print(f"{'t':>3} {'frontier_dedup':>15} {'naive_ring_sum':>14} {'ratio':>6} {'touched_total':>13}")
for f in B:
    ratio = f["naive_ring_sum_cells"] / max(f["frontier_dedup_cells"], 1)
    print(f"{f['t']:>3} {f['frontier_dedup_cells']:>15} {f['naive_ring_sum_cells']:>14} "
          f"{ratio:>6.1f} {f['touched_total']:>13}")

print("\n=== C: hierarchy shadow (parent R=1000, sub-doll r=50, lam=0.05, 7 members) ===")
print(f"predicted parent flatline {C['predicted_parent_flatline']}, sub {C['predicted_sub_flatline']}")
for row in C["checkpoints"]:
    print(f"  t={row['t']:>5} parent_chain_live={row['parent_chain_live']:>6} sub_chain_live={row['sub_chain_live']:>6}")
print("members entering parent:", [(m['rq'], m['enters_parent']) for m in C['members']])
