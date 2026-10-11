#!/usr/bin/env python3
"""Final tables for the dossier: e(B,M) linearity, the cliff decomposition,
the density profile, the paced worst cell, and the corrected record."""
import json, csv, os

TICK = 4.925_490_947e-6
D = os.path.join(os.path.dirname(__file__), 'data')

def load(name):
    d = json.load(open(os.path.join(D, name + '.json')))
    frames = d['frames']
    nominal = frames / 60.0 if not d['paced'] else d['wall_seconds']
    E = d['events_per_second'] * nominal          # dash events in the frame loop
    wall = d['wall_seconds']
    pres = d['presented_tick_at_end'] * TICK
    fps = frames / wall
    return dict(d=d, E=E, wall=wall, pres=pres, fps=fps, e=E / frames,
                T=E / wall, Dn=E / pres if pres else float('inf'),
                delivered=pres / wall, med=d['rtf']['median'],
                digest=d['digest'], bodies=d['bodies'],
                eng=d['where_the_time_goes_ms']['engine']['p50'],
                view=d['where_the_time_goes_ms']['view_gather']['p50'],
                frame=d['frame_ms']['p50'])

print("### Table 1: events bought per frame e(B,M) -- budget-bound or demand-bound")
print(f"{'M':>5s} {'B ms':>6s} {'bodies':>6s} {'e/fr':>7s} {'e per ms':>8s} {'T ev/s':>8s} {'fps':>6s} "
      f"{'med rtf':>9s} {'delivered':>9s} {'D ev/gs':>8s} {'ovf':>4s}")
for M in [4, 100, 400]:
    for B in ['5', '1', '0.2', '0.05']:
        c = load(f'G-m{M}-b{B}')
        b = float(B)
        print(f"{M:5d} {B:>6s} {c['bodies']:6d} {c['e']:7.2f} {c['e']/b:8.1f} {c['T']:8.0f} {c['fps']:6.0f} "
              f"{c['med']:9.2f} {c['delivered']:9.1f} {c['Dn']:8.2f} {c['d']['rtf']['overflow_frames']:4d}")

print("\n### Table 2: the m4 -> m400 cliff at 0.2 ms, factored")
a, b = load('G-m4-b0.2'), load('G-m400-b0.2')
print(f"delivered ratio: {a['delivered']:.0f} / {b['delivered']:.1f} = {a['delivered']/b['delivered']:.0f}x")
print(f"  T drop:  {a['T']:.0f} -> {b['T']:.0f} ev/s = {a['T']/b['T']:.1f}x  (e {a['e']:.1f}->{b['e']:.1f} = {a['e']/b['e']:.1f}x; fps {a['fps']:.0f}->{b['fps']:.0f} = {a['fps']/b['fps']:.1f}x; frame p50 {a['frame']:.2f}->{b['frame']:.2f} ms)")
print(f"  D rise:  {a['Dn']:.2f} -> {b['Dn']:.1f} ev/game-s = {b['Dn']/a['Dn']:.0f}x")
print(f"  product: {(a['T']/b['T'])*(b['Dn']/a['Dn']):.0f}x  (matches {a['delivered']/b['delivered']:.0f}x)")

print("\n### Table 3: the scene's density profile D(game-time) at m400 (deterministic scene: nested ranges)")
runs = [(load('G-m400-b0.05'), 0.05), (load('G-m400-b0.2'), 0.2), (load('G-m400-b1'), 1), (load('G-m400-b5'), 5)]
prev_e, prev_p = 0.0, 0.0
for c, B in runs:
    de, dp = c['E'] - prev_e, c['pres'] - prev_p
    seg = (de / dp) if dp > 1e-9 else float('nan')
    print(f"  budget {B:>5} ms: covers 0-{c['pres']:8.1f} gs, {c['E']:7.0f} events, avg {c['Dn']:5.1f}/gs; segment ({prev_p:6.1f},{c['pres']:7.1f}] = {de:7.0f} ev / {dp:7.1f} gs = {seg:5.1f}/gs")
    prev_e, prev_p = c['E'], c['pres']
for M in [4, 100]:
    runs = [(load(f'G-m{M}-b0.05'), 0.05), (load(f'G-m{M}-b0.2'), 0.2), (load(f'G-m{M}-b1'), 1), (load(f'G-m{M}-b5'), 5)]
    pe, pp = 0.0, 0.0
    segs = []
    for c, B in runs:
        de, dp = c['E'] - pe, c['pres'] - pp
        segs.append(f"{de/dp:5.2f}" if dp > 1e-9 else "  n/a")
        pe, pp = c['E'], c['pres']
    print(f"  m{M}: segment densities {', '.join(segs)} ev/gs")

print("\n### Table 4: the paced worst cell (60 Hz, 10 s)")
for n in ['P-m4-b0.2', 'P-m400-b0.2', 'P-m400-b5']:
    c = load(n)
    rows = list(csv.DictReader(open(os.path.join(D, n + '.csv'))))
    rtf = [float(r['rtf']) for r in rows]
    game = [r / 60.0 for r in rtf]
    tot = sum(game)
    srt = sorted(game, reverse=True)
    frozen = sum(1 for r in rtf if r < 0.01) / len(rtf)
    print(f"  {n:12s} delivered {c['delivered']:7.1f}x  med {c['med']:7.1f}  frozen {frozen:4.2f}  "
          f"top10% share {sum(srt[:len(srt)//10])/tot if tot else 0:5.2f}  worst {c['d']['worst_hitch_ms']:5.2f} ms  "
          f"T {c['T']:5.0f} ev/s  D {c['Dn']:5.1f}  digest {c['digest'][:8]}")

print("\n### Table 5: the corrected record (original table row by row)")
r1 = [('300', 'R1-300-scripted'), ('3000', 'R1-3000-scripted'), ('30000', 'R1-30000-scripted'), ('300000 (3s)', 'R1-300000-coast')]
orig_med = {'300': 300.0, '3000': 3000.0, '30000': 30000.0, '300000 (3s)': 6818.0}
orig_dig = {'300': '029f9c92', '3000': 'e68f7fcf', '30000': '95750d31', '300000 (3s)': '475f4db2'}
for label, n in r1:
    c = load(n)
    print(f"  rtf {label:>11s}: med {c['med']:9.1f} (orig {orig_med[label]:9.1f})  low1 {c['d']['rtf']['lowest_1pct']:8.1f}  "
          f"ovf {c['d']['rtf']['overflow_frames']:3d}/600  digest {c['digest'][:8]} == orig {orig_dig[label]}: {c['digest'][:8]==orig_dig[label]}")
b2, b5 = load('G-m400-b0.2'), load('G-m400-b5')
print(f"  m400 @0.2 ms: bodies {b2['bodies']} (orig claimed 428; 428 is the 5 ms count: {b5['bodies']})  "
      f"engine p50 {b2['eng']:.2f} -> {b5['eng']:.2f} ms (0.2 -> 5 ms); view p50 {b2['view']:.2f} -> {b5['view']:.2f}; frame p50 {b2['frame']:.2f} -> {b5['frame']:.2f}")
