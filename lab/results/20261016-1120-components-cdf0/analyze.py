#!/usr/bin/env python3
"""Aggregate the ES_SCAN_CENSUS lines of the run's flights (lab 20261016-1120-components-cdf0).

Every count is an exact integer read from the shipped engine's own scan; timings are
Linux/x86 orders of magnitude. Joins SCAN_CAP (the cheap half: what the finder kept) with
SCAN_ANS (the expensive half: what the answer read and what it found) on (t, order).
"""
import re
import sys
from collections import defaultdict

CAP = re.compile(r"SCAN_CAP t=(\d+) doll=(\d+) bodies=(\d+) near=(-?\d+) cand=(\d+) interval=(\S+) r=(\S+) v=(\S+)")
ANS = re.compile(r"SCAN_ANS t=(\d+) cand=(\d+) hits=(\d+) us=(\S+) us_per_cand=(\S+) min_any_reach=(\S+) min_miss_reach=(\S+)")


def one(path):
    caps = {}
    order = []
    ans = []
    for line in open(path):
        if m := CAP.search(line):
            t, doll, bodies, near, cand = int(m[1]), int(m[2]), int(m[3]), int(m[4]), int(m[5])
            caps.setdefault((t, doll), []).append((near, cand, bodies))
            order.append((t, doll))
        elif m := ANS.search(line):
            ans.append(dict(t=int(m[1]), cand=int(m[2]), hits=int(m[3]), us=float(m[4]),
                            upc=float(m[5]), min_any=float(m[6]), min_miss=float(m[7])))
    # A scan's capture line: the census prints per capture call; the answer's candidates equal the
    # capture's cand of the same t (repeats share t). Match each answer to the modal capture at its t.
    by_t = defaultdict(list)
    for (t, doll) in order:
        by_t[t].append(doll)
    for a in ans:
        dolls = by_t.get(a["t"], [])
        a["doll"] = max(set(dolls), key=dolls.count) if dolls else -1
        rows = [c for (t, doll), cs in caps.items() if t == a["t"] for c in cs]
        if rows:
            nears = [r[0] for r in rows]
            bods = [r[2] for r in rows]
            a["near"] = max(set(nears), key=nears.count)
            a["bodies"] = max(set(bods), key=bods.count)
    return ans


def agg(name, ans):
    if not ans:
        print(f"{name}: no scans")
        return
    for doll in sorted({a["doll"] for a in ans}):
        rows = [a for a in ans if a["doll"] == doll]
        n = len(rows)
        cands = sorted(a["cand"] for a in rows)
        hits = sum(a["hits"] for a in rows)
        tot_cand = sum(cands)
        upcs = sorted(a["upc"] for a in rows if a["cand"] > 0)
        miss = sorted(a["min_miss"] for a in rows)
        anym = sorted(a["min_any"] for a in rows)
        frac = [a["cand"] / a["bodies"] for a in rows if a.get("bodies")]
        med = lambda v: v[len(v) // 2] if v else float("nan")
        print(f"{name} doll={doll}: answered_scans={n} cand: med={med(cands)} p90={cands[int(0.9*len(cands))]} max={cands[-1]} | "
            f"read_fraction_of_doll: med={med(frac) if frac else float('nan'):.3f} max={max(frac) if frac else float('nan'):.3f} | hits_total={hits} per_scan_med={med(sorted(a['hits'] for a in rows))} | "
              f"us_per_cand: med={med(upcs):.2f} max={upcs[-1]:.2f} | answer_us: med={med(sorted(a['us'] for a in rows)):.0f} | "
              f"min_miss/reach: med={med(miss):.3g} min={miss[0]:.3g} | min_any/reach: med={med(anym):.3g} min={anym[0]:.3g}")
        # the emptiness ratio: reads per hit
        print(f"    reads_per_hit={tot_cand / max(hits, 1):.1f}; total_reads={tot_cand}")


if __name__ == "__main__":
    for path in sys.argv[1:]:
        agg(path.split("/")[-1].replace(".err", ""), one(path))
