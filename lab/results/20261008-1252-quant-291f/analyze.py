#!/usr/bin/env python3
"""Analyze the wake panel: burn vs coast twins, per seed. Emits the frozen verdict inputs."""
import sys, glob

COLS = ["f","ms","events","presented","ov","kick","open","bound","hand","slice","dec","enc","ref","leav","diss","c_planet","c_moon","c_ship","c_player","c_fleet"]

def load(path):
    rows, meta, foot = [], {}, None
    for line in open(path):
        line = line.strip()
        if line.startswith("# mode"):
            meta = dict(kv.split("=",1) for kv in line[2:].split() if "=" in kv)
        elif line.startswith("# digest"):
            foot = dict(kv.split("=",1) for kv in line[2:].split() if "=" in kv)
        elif line and not line.startswith("#"):
            rows.append(dict(zip(COLS, line.split(","))))
    return rows, meta, foot

def pct(xs, p):
    if not xs: return float("nan")
    xs = sorted(xs); return xs[min(len(xs)-1, int(len(xs)*p))]

def arm(path):
    rows, meta, foot = load(path)
    ms  = [float(r["ms"]) for r in rows]
    burn_window = [float(r["ms"]) for i,r in enumerate(rows) if 600 <= i < 1800]
    pre  = [float(r["ms"]) for i,r in enumerate(rows) if i < 600]
    ev   = lambda i0,i1: sum(int(r["events"]) for i,r in enumerate(rows) if i0 <= i < i1)
    kinds = lambda i0,i1: {k: sum(int(r[k]) for i,r in enumerate(rows) if i0 <= i < i1) for k in ["kick","open","bound","hand","slice","enc"]}
    ovf  = sum(int(r["ov"]) for i,r in enumerate(rows) if 600 <= i < 1800)
    # presented-tick progression: game ticks per frame, pre and during
    tk_pre  = (int(rows[599]["presented"]) - int(rows[0]["presented"])) / 600
    tk_post = (int(rows[1799]["presented"]) - int(rows[610]["presented"])) / (1799-610)
    return dict(path=path, rows=rows, foot=foot, ms=ms, burn=burn_window, pre=pre,
                ev_pre=ev(0,600), ev_wake=ev(600,1800), kinds_pre=kinds(0,600), kinds_wake=kinds(600,1800),
                ovf=ovf, tk_pre=tk_pre, tk_post=tk_post)

def fmt(a, b, tag):
    wake_extra = a["ev_wake"] - b["ev_wake"]
    b999 = pct(b["burn"], 0.999)
    worst = max(a["burn"])
    ratio = worst / b999 if b999 > 0 else float("inf")
    print(f"== {tag}")
    print(f"  coast p50/p95/p99/p99.9/max ms: {pct(b['burn'],0.5):.3f} {pct(b['burn'],0.95):.3f} {pct(b['burn'],0.99):.3f} {b999:.3f} {max(b['burn']):.3f}  (pre-burn p99.9 {pct(b['pre'],0.999):.3f})")
    print(f"  arm   p50/p95/p99/p99.9/max ms: {pct(a['burn'],0.5):.3f} {pct(a['burn'],0.95):.3f} {pct(a['burn'],0.99):.3f} {pct(a['burn'],0.999):.3f} {worst:.3f}   worst/coast_p99.9 = {ratio:.2f}x")
    print(f"  events pre(600f)->arm-window(1200f): coast {b['ev_pre']}->{b['ev_wake']}, arm {a['ev_pre']}->{a['ev_wake']}; wake extra events = {wake_extra}")
    print(f"  wake kinds (arm minus pre-window baseline): { {k: a['kinds_wake'][k] - a['kinds_pre'][k] for k in a['kinds_wake']} }")
    print(f"  coast kinds wake-window: {b['kinds_wake']}; arm overflow frames {a['ovf']}, coast {b['ovf']}")
    print(f"  ticks/frame: coast {b['tk_pre']:.0f} -> {b['tk_post']:.0f}; arm {a['tk_pre']:.0f} -> {a['tk_post']:.0f}  (rtf {100*a['tk_post']/b['tk_pre']:.2f}x of coast rate)")
    d1, d2 = a["foot"], b["foot"]
    same_digest = d1.get("digest") == d2.get("digest")
    print(f"  end: arm digest {d1.get('digest','')[:8]} coast {d2.get('digest','')[:8]} same={same_digest} refused arm={d1.get('refused')} coast={d2.get('refused')} periapsis arm={d1.get('periapsis','')[:40]} coast={d2.get('periapsis','')[:40]}")
    return wake_extra, ratio

for seed in [1,2,3]:
    fmt(arm(f"burn15-s{seed}.csv"), arm(f"coast-s{seed}.csv"), f"seed {seed}: burn15 vs coast")
    n = arm(f"noop-s{seed}.csv"); c = arm(f"coast-s{seed}.csv")
    print(f"== seed {seed}: noop vs coast -> wake extra events {n['ev_wake']-c['ev_wake']}, worst {max(n['burn']):.3f} ms, digest same={n['foot'].get('digest')==c['foot'].get('digest')}")
a = arm("burn15-s2b.csv"); b = arm("coast-s2b.csv")
fmt(a, b, "seed 2 repeat (ABBA): burn15 vs coast")
print(f"  determinism: burn s2 digests {arm('burn15-s2.csv')['foot'].get('digest','')[:8]} vs {a['foot'].get('digest','')[:8]}; coast s2 {arm('coast-s2.csv')['foot'].get('digest','')[:8]} vs {b['foot'].get('digest','')[:8]}")

print("\n== level sweep (seed 2), burn window 600..1200 (held), release 1200..1800 (decay)")
for lv in [4,8,12,15]:
    x = arm(f"burn{lv}-s2.csv")
    held = [float(r["ms"]) for i,r in enumerate(x["rows"]) if 600 <= i < 1200]
    decay = [float(r["ms"]) for i,r in enumerate(x["rows"]) if 1200 <= i < 1320]
    tk_held = (int(x["rows"][1199]["presented"]) - int(x["rows"][610]["presented"])) / (1199-610)
    tk_dec  = (int(x["rows"][1319]["presented"]) - int(x["rows"][1200]["presented"])) / 120
    n_held = sum(int(r["events"]) for i,r in enumerate(x["rows"]) if 600 <= i < 1200)
    n_dec  = sum(int(r["events"]) for i,r in enumerate(x["rows"]) if 1200 <= i < 1320)
    print(f"  L{lv:>2}: held p50 {pct(held,0.5):.2f} p99 {pct(held,0.99):.2f} max {max(held):.2f} ms, events/frame {n_held/600:.1f}; ticks/frame held {tk_held:.0f} -> after release {tk_dec:.0f}; decay-window events/frame {n_dec/120:.1f}")
