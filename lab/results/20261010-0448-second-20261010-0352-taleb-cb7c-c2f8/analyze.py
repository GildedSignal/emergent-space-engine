#!/usr/bin/env python3
"""Summarize the contention-controlled ladder: provenance, wall-vs-CPU attribution validity,
the CPU cliff location, gather share in CPU terms, seed spread, and the spinner mechanism."""
import json, os, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__))

def load(n): return json.load(open(f"{HERE}/data/{n}.json"))
def exists(n): return os.path.exists(f"{HERE}/data/{n}.json")

print("== E0 provenance (pinned rerun of the author's det_repeat) ==")
d = load("det_repeat")
want = json.load(open(f"{HERE}/orig_run/data/det_repeat.json"))
print(f"  digest {d['digest'][:16]} vs author {want['digest'][:16]} -> {'EQUAL' if d['digest']==want['digest'] else 'DIFFERENT'}")

print("\n== P2 attribution validity: frame wall vs frame CPU, quiet ladder ==")
runs = sorted(f for f in os.listdir(f"{HERE}/data") if f.startswith("q_") and f.endswith(".json"))
bad, gstall = [], []
for f in runs:
    d = load(f[:-5])
    gap = d["worst_hitch_ms"] - d["frame_cpu_ms"]["worst"]
    if gap > 1.5: bad.append((f[:-5], round(gap, 2)))
    gm = d["where_the_time_goes_ms"]["view_gather"]["max"]
    if gm > d["frame_cpu_ms"]["worst"] + 1.5: gstall.append((f[:-5], round(gm - d["frame_cpu_ms"]["worst"], 2)))
print(f"  {len(runs)} runs; interior-stalled (wall worst - cpu worst > 1.5 ms): {len(bad)} {bad}")
print(f"  gather-max frame stalled (gather_max > cpu_worst + 1.5): {len(gstall)} {gstall}")

print("\n== E1 the ladder (quiet, pinned core 6, paced, rtf 100, 30 s, 8 seeds/point) ==")
print("  point      N(bodies) | cpu_p50 cpu_p99 cpu_worst cpuH16 | wall_worst wallH/hr | gather_p99 gather_max sh | eng_p99 | ovfl")
by_M = {}
for M in (96, 192, 256, 320, 384, 400):
    rows = []
    for S in range(1, 9):
        n = f"q_M{M}_s{S}"
        if not exists(n): continue
        d = load(n); f, c, w = d["frame_ms"], d["frame_cpu_ms"], d["where_the_time_goes_ms"]
        rows.append(dict(N=d["bodies"], cp50=c["p50"], cp99=c["p99"], cw=c["worst"],
                         ch=c["hitch_counts"][0], ww=d["worst_hitch_ms"],
                         wh=d["hitches_per_gameplay_hour"]["above_16.7ms"],
                         g99=w["view_gather"]["p99"], gm=w["view_gather"]["max"],
                         gs=w["view_gather"]["share"], e99=w["engine"]["p99"],
                         ov=d["rtf"]["overflow_frames"]))
    by_M[M] = rows
    med = lambda k: st.median(r[k] for r in rows)
    mx = lambda k: max(r[k] for r in rows)
    mn = lambda k: min(r[k] for r in rows)
    print(f"  M{M:3d} N~{int(med('N')):3d} med | {med('cp50'):6.2f} {med('cp99'):6.2f} {med('cw'):7.2f} {med('ch'):5.0f} | {med('ww'):7.2f} {med('wh'):7.0f} | {med('g99'):6.2f} {med('gm'):7.2f} {med('gs'):.2f} | {med('e99'):5.1f} | {med('ov'):4.0f}")
    print(f"           range      | {mn('cp50'):6.2f} {mn('cp99'):6.2f} {mn('cw'):7.2f} {mn('ch'):5.0f} | {mx('ww'):7.2f} {mx('wh'):7.0f} | {mn('g99'):6.2f} {mx('gm'):7.2f} [{mn('gs'):.2f},{mx('gs'):.2f}] | {mx('e99'):5.1f} | {mx('ov'):4.0f}")
    chs = [r["ch"] for r in rows]
    print(f"           cpuH16 per seed: {chs}  (median {st.median(chs):.0f}, max {max(chs)})")

print("\n== gather CPU share of frame (share of summed terms) and cpu_hitch spread at M400 ==")
rows = by_M.get(400, [])
if rows:
    for k in ("cp50","cp99","cw","g99","gm","gs","ww","wh","ch"):
        v = [r[k] for r in rows]
        print(f"  {k:5s} median={st.median(v):8.2f} min={min(v):8.2f} max={max(v):8.2f} max/med={max(v)/max(st.median(v),1e-9):6.2f}")

print("== u30: unpaced 30 s vs paced 30 s, same cut ==")
a, b = load("u30_M384_s1"), load("q_M384_s1")
print(f"  digest {a['digest'][:16]} vs {b['digest'][:16]} -> {'EQUAL' if a['digest']==b['digest'] else 'DIFFERENT'}"
      f" (author stored mem384: dd178af980bf2a4b)")
wa, wb = a["where_the_time_goes_ms"], b["where_the_time_goes_ms"]
print(f"  paced:   wall {b['wall_seconds']:.1f}s cpu_p50 {b['frame_cpu_ms']['p50']:.2f} cpu_worst {b['frame_cpu_ms']['worst']:.2f} "
      f"engine_p50 {wb['engine']['p50']:.2f} gather_p50 {wb['view_gather']['p50']:.2f} ovfl {b['rtf']['overflow_frames']}")
print(f"  unpaced: wall {a['wall_seconds']:.1f}s cpu_p50 {a['frame_cpu_ms']['p50']:.2f} cpu_worst {a['frame_cpu_ms']['worst']:.2f} "
      f"engine_p50 {wa['engine']['p50']:.2f} gather_p50 {wa['view_gather']['p50']:.2f} ovfl {a['rtf']['overflow_frames']}")
print(f"  cadence cost: cpu_p50 x{b['frame_cpu_ms']['p50']/a['frame_cpu_ms']['p50']:.2f}, "
      f"engine x{wb['engine']['p50']/max(wa['engine']['p50'],1e-9):.1f}, gather x{wb['view_gather']['p50']/wa['view_gather']['p50']:.2f} (same frames, same digest)")
for M in (256, 320, 384, 400):
    for S in (1, 4, 8):
        n = f"u_M{M}_s{S}"
        if not exists(n): continue
        d = load(n); f, c, w = d["frame_ms"], d["frame_cpu_ms"], d["where_the_time_goes_ms"]
        print(f"  M{M:3d} s{S} N={d['bodies']:3d} wall_p50={f['p50']:5.2f} cpu_p50={c['p50']:5.2f} cpu_worst={c['worst']:6.2f} "
              f"gather_p99={w['view_gather']['p99']:5.2f} max={w['view_gather']['max']:6.2f} share={w['view_gather']['share']:.2f}")

print("\n== E3 controlled contention (same-core spinner) vs quiet same-seed ==")
for S in (1, 2):
    q, c_ = load(f"q_M400_s{S}"), load(f"c_M400_s{S}")
    for tag, d in (("quiet ", q), ("spin  ", c_)):
        w = d["where_the_time_goes_ms"]
        print(f"  s{S} {tag} N={d['bodies']:3d} wall_worst={d['worst_hitch_ms']:6.2f} cpu_worst={d['frame_cpu_ms']['worst']:6.2f} "
              f"gather_max={w['view_gather']['max']:6.2f} gather_p99={w['view_gather']['p99']:5.2f} share={w['view_gather']['share']:.2f} "
              f"wallH/hr={d['hitches_per_gameplay_hour']['above_16.7ms']:7.0f} cpuH={d['frame_cpu_ms']['hitch_counts']} "
              f"digest-vs-quiet={'EQUAL' if q['digest']==c_['digest'] else 'DIFFERENT'}")
