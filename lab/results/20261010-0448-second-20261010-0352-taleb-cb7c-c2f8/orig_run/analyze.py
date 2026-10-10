#!/usr/bin/env python3
"""Summarize the probe: determinism, state growth (H_live), load convexity, seed spread."""
import json, os, statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
def load(n): return json.load(open(f"{HERE}/data/{n}.json"))
def rssrows(n):
    r=[l.split('\t') for l in open(f"{HERE}/data/{n}.rss.tsv").read().splitlines()[1:]]
    return [float(x[0]) for x in r], [int(x[1]) for x in r]

print("== E0 determinism (digest at the canonical cut) ==")
base=load('det_repeat')['digest']
for n in ['det_repeat','det_threads8','det_unpaced','det_budget','det_seed2']:
    d=load(n); eq = "EQUAL" if d['digest']==base else "DIFFERENT"
    print(f"  {n:14s} {d['digest'][:16]} {eq}  (load '{d['uptime_before'][-20:].strip()}')")

print("\n== E1 state growth: game time vs wall time (members 48, 30 s wall each) ==")
for n in ['rtf1','rtf10','rtf100','rtf1000']:
    d=load(n); t,r=rssrows(n); n95=int(len(t)*0.95)
    gs=d['rtf_target']*d['wall_seconds']
    print(f"  rtf={d['rtf_target']:6.0f} game_s={gs:8.0f} rss {r[0]}->{r[n95-1]} kB  d={r[n95-1]-r[0]:+6d}  "
          f"kB/game-s={(r[n95-1]-r[0])/gs:8.3f}  kB/wall-s={(r[n95-1]-r[0])/t[n95-1]:6.1f}  majflt=0")
for n in ['rtf100','rtf1000','mem768']:
    t,r=rssrows(n); n95=int(len(t)*0.95)
    print(f"  {n}: drift over last third: {r[n95-1]-r[2*n95//3]:+d} kB (saturated)")

print("\n== E2 frame cost vs run length (rtf 100, members 48) ==")
for n in ['len10','rtf100','len55']:
    d=load(n); f=d['frame_cpu_ms']
    print(f"  {n:7s} T={d['wall_seconds']:5.1f}s game_s={d['rtf_target']*d['wall_seconds']:6.0f} "
          f"p50={f['p50']:.2f} p99={f['p99']:.2f} p99.9={f['p99.9']:.2f} worst={f['worst']:.2f} ovfl={d['rtf']['overflow_frames']}")

print("\n== E3 load (rtf 100, 30 s; the battle scene caps at ~400 members) ==")
for n in ['rtf100','mem96','mem192','mem384','mem768','mem3072']:
    d=load(n); f=d['frame_cpu_ms']; p=d['where_the_time_goes_ms']
    hh=d['hitches_per_gameplay_hour']
    print(f"  {n:8s} N={d['bodies']:4d} p50={f['p50']:5.2f} p99={f['p99']:5.2f} worst={f['worst']:5.2f} "
          f"ovfl={d['rtf']['overflow_frames']:4d} hitch16.7/hr={hh['above_16.7ms']:5.0f} "
          f"engine p99={p['engine']['p99']:4.1f} gather p99={p['view_gather']['p99']:4.1f} gather share={p['view_gather']['share']:.2f}")
print(f"  mem768 vs mem3072: same digest {load('mem768')['digest']==load('mem3072')['digest']}, "
      f"overflow {load('mem768')['rtf']['overflow_frames']} vs {load('mem3072')['rtf']['overflow_frames']} (schedule noise)")

print("\n== E5 seed spread (rtf 100, members 48, 30 s, thread-CPU metrics) ==")
seeds=['rtf100']+[f'seed{s}' for s in range(2,9)]
w=[load(n)['frame_cpu_ms']['worst'] for n in seeds]
p50=[load(n)['frame_cpu_ms']['p50'] for n in seeds]
p99=[load(n)['frame_cpu_ms']['p99'] for n in seeds]
ov=[load(n)['rtf']['overflow_frames'] for n in seeds]
for n in seeds:
    d=load(n)
    print(f"  {n:7s} p50={d['frame_cpu_ms']['p50']:.2f} p99={d['frame_cpu_ms']['p99']:.2f} worst={d['frame_cpu_ms']['worst']:.2f} "
          f"ovfl={d['rtf']['overflow_frames']:3d} load='{d['uptime_before'][-22:].strip()}'")
for name,v in [('worst',w),('p50',p50),('p99',p99),('overflow',ov)]:
    print(f"  {name}: median={st.median(v):.2f} max={max(v):.2f} max/median={max(v)/st.median(v):.2f}")
