#!/usr/bin/env python3
"""Allocator trace analysis: mandatory (deadline<=target) vs deferrable engine work per frame."""
import csv, sys, math

TICK_S = 4.925490947e-6
RTF = float(sys.argv[2]) if len(sys.argv) > 2 else 100.0
TPF = RTF / 60.0 / TICK_S  # ticks per frame advance

rows = list(csv.DictReader(open(sys.argv[1])))
frames = {}
items = []
for r in rows:
    if r["row"] == "F":
        frames[int(r["frame"])] = dict(target=int(r["target"]), now0=int(r["now0"]),
            rekey_ns=int(r["rekey_ns"]), wall_ns=int(r["wall_ns"]), events=int(r["events"]),
            overflow=r["overflow"] == "1", mand_ns=0, def_ns=0, n=0, nmand=0, maxitem=0, maxent=-1)
    else:
        items.append(r)
for r in items:
    f = frames[int(r["frame"])]
    c = int(r["cost_ns"])
    if r["mandatory"] == "1":
        f["mand_ns"] += c; f["nmand"] += 1
    else:
        f["def_ns"] += c
    f["n"] += 1
    if c > f["maxitem"]:
        f["maxitem"] = c; f["maxent"] = int(r["entity"])

fs = [frames[i] for i in sorted(frames)]
def pct(xs, p):
    xs = sorted(xs); i = min(len(xs) - 1, math.ceil(p * (len(xs) - 1)))
    return xs[i]
def col(k): return [f[k] / 1e6 for f in fs]  # ms

print(f"frames={len(fs)} items={len(items)} ticks/frame={TPF:,.0f}")
print(f"{'':14s}{'p50':>9s}{'p90':>9s}{'p99':>9s}{'p99.9':>9s}{'max':>9s}{'mean':>9s}")
for k, lab in [("wall_ns", "engine wall"), ("mand_ns", "MANDATORY"), ("def_ns", "deferrable"), ("rekey_ns", "rekey"), ("maxitem", "max item")]:
    xs = col(k)
    print(f"{lab:14s}{pct(xs,0.5):9.3f}{pct(xs,0.9):9.3f}{pct(xs,0.99):9.3f}{pct(xs,0.999):9.3f}{max(xs):9.3f}{sum(xs)/len(xs):9.3f}")

ovf = [f for f in fs if f["overflow"]]
print(f"\noverflow frames: {len(ovf)}/{len(fs)} ({100*len(ovf)/len(fs):.1f}%)")
mand_p99 = pct(col('mand_ns'), 0.99)
wall_p99 = pct(col('wall_ns'), 0.99)
print(f"idiot index p99(engine wall)/p99(mandatory) = {wall_p99/max(mand_p99,1e-9):.2f}")
print(f"deferrable share of resolved engine time = {sum(f['def_ns'] for f in fs)/max(1,sum(f['def_ns']+f['mand_ns'] for f in fs))*100:.1f}%")

# slack of deferrable items, in frames
slack = sorted((int(r["deadline"]) - frames[int(r["frame"])]["target"]) / TPF for r in items if r["mandatory"] == "0")
if slack:
    print(f"deferrable slack (frames): p10={slack[int(0.1*len(slack))]:.1f} med={slack[len(slack)//2]:.1f} p90={slack[int(0.9*len(slack))]:.1f} max={slack[-1]:.1f}")
    print(f"  share with slack >= 10 frames: {sum(1 for s in slack if s >= 10)/len(slack)*100:.1f}%")

# item costs by kind
byk = {}
for r in items:
    byk.setdefault(r["kind"], []).append(int(r["cost_ns"]) / 1e3)
for k, xs in sorted(byk.items()):
    print(f"kind {k}: n={len(xs)} p50={pct(xs,0.5):.1f}us p99={pct(xs,0.99):.1f}us max={max(xs):.1f}us")

# top entities by total and by max item
bye = {}
for r in items:
    d = bye.setdefault(int(r["entity"]), [0, 0])
    d[0] += int(r["cost_ns"]); d[1] = max(d[1], int(r["cost_ns"]))
top = sorted(bye.items(), key=lambda kv: -kv[1][0])[:8]
print("top entities by total ms:", [(e, round(v[0]/1e6,2), round(v[1]/1e3,0)) for e, v in top])

# overflow frames: composition of mandatory work
if ovf:
    ovset = {id(f) for f in ovf}
    pm = sum(int(r["cost_ns"]) for r in items if r["mandatory"] == "1" and frames[int(r["frame"])] is not None and id(frames[int(r["frame"])]) in ovset and int(r["entity"]) == 27)
    tm = sum(int(r["cost_ns"]) for r in items if r["mandatory"] == "1" and id(frames[int(r["frame"])]) in ovset)
    print(f"overflow frames: mandatory total {tm/1e6:.1f} ms, player(entity 27) share {pm/max(tm,1)*100:.0f}%")
    print(f"  overflow frames' wall ms: p50={pct([f['wall_ns']/1e6 for f in ovf],0.5):.2f} max={max(f['wall_ns'] for f in ovf)/1e6:.2f}; their maxitem p50={pct([f['maxitem']/1e6 for f in ovf],0.5):.2f} ms (entity {ovf[0]['maxent']})")

# the flattening ratio: work binned by tick (arrival) vs by deadline (due)
tickw, duew = {}, {}
for r in items:
    c = int(r["cost_ns"])
    t, dl = int(r["tick"]), int(r["deadline"])
    tickw[t // TPF] = tickw.get(t // TPF, 0) + c
    duew[dl // TPF] = duew.get(dl // TPF, 0) + c
tv, dv = [v / 1e6 for v in tickw.values()], [v / 1e6 for v in duew.values()]
print(f"\nper-frame-work by tick (arrival): p50={pct(tv,0.5):.2f} p99={pct(tv,0.99):.2f} max={max(tv):.2f} ms")
print(f"per-frame-work by deadline (due):  p50={pct(dv,0.5):.2f} p99={pct(dv,0.99):.2f} max={max(dv):.2f} ms")
print(f"causal flattening (light-cone smoothing available): p99 ratio {pct(tv,0.99)/max(pct(dv,0.99),1e-9):.2f}x, max ratio {max(tv)/max(dv):.2f}x")
