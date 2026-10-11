#!/usr/bin/env python3
"""Tables for the dossier: reads battle.jsonl (parent record, regenerated) and fix.jsonl."""
import json, sys

def load(p):
    out = []
    for line in open(p):
        line = line.strip()
        if line and not line.startswith('#'):
            out.append(json.loads(line))
    return out

battle = {d['scene']: d for d in load('battle.jsonl') if 'scene' in d}
fix = load('fix.jsonl')
KS = [1, 2, 4, 8, 16, 32, 64, 128, 256]

print('== A: period sweep (n=150/fleet, 300 total) ==')
print(f"{'spread':7} {'H':>4} {'enc':>7} {'cross':>7} {'coneX':>6} {'o_cone':>6} {'kmed':>5} {'kmax':>5} {'kp99':>5} {'c_uc(32)':>8} {'plateau':>7}")
for d in fix:
    if d.get('part') != 'A':
        continue
    c32 = d['caught_uc_k'][KS.index(32)]
    plat = d['caught_f_k'][-1]
    print(f"{d['spread']:7} {d['orbits']:>4.0f} {d['truth_enc']:>7} {d['truth_cross']:>7} {d['cone_cross']:>6} "
          f"{d['outside_cone']:>6} {d['kmed_uc']:>5} {d['kmax_uc']:>5} {d['kp99_uc']:>5} {c32:>8.4f} {plat:>7.4f}")

print()
print('== A: validity horizon H* (linear interp of kmax between measured horizons) ==')
by_spread = {}
for d in fix:
    if d.get('part') == 'A':
        by_spread.setdefault(d['spread'], []).append((d['orbits'], d['kmax_uc']))
for sp, pts in by_spread.items():
    pts.sort()
    for (h0, k0), (h1, k1) in zip(pts, pts[1:]):
        if k0 <= 32 <= k1:
            h = h0 + (32 - k0) * (h1 - h0) / (k1 - k0)
            print(f"  spread {sp:6}: kmax crosses 32 at H* ~= {h:.0f} orbits")
        if k1 < 32 and (h0, k0) == pts[-2]:
            pass
    if pts[-1][1] < 32:
        print(f"  spread {sp:6}: kmax {pts[-1][1]} at H={pts[-1][0]:.0f} — never crosses 32 (eternal to {pts[-1][0]:.0f}+)")
    if pts[0][1] > 32:
        print(f"  spread {sp:6}: already broken at H={pts[0][0]:.0f} (kmax {pts[0][1]})")

print()
print('== B: merge-join at the crossing epoch (b2, parent seeds; k0 = setup-sort control) ==')
print(f"{'scene':16} {'n':>4} {'cross':>5} {'k0 med/max':>11} {'km med/max':>11} {'kt med/max':>11} {'ke med/max':>11} "
      f"{'c32 k0':>7} {'c32 km':>7} {'c64 km':>7} {'c128 km':>8} {'coneX':>6} {'cpkm 32/64/128':>16} {'x@0miss':>8}")
for d in fix:
    if d.get('part') != 'B':
        continue
    n = d['n_a'] + d['n_b']
    kzm = next(k for k, c in zip(KS, d['km_curve']) if c >= 1.0)
    pzm = d['cp_km_32_64_128'][[32, 64, 128].index(kzm)]
    tag = f"{d['cone_cross']/pzm:.2f}x@k{kzm}"
    print(f"{d['scene']:16} {n:>4} {d['truth_cross']:>5} {d['k0_med_max'][0]:>5}/{d['k0_med_max'][1]:<5} "
          f"{d['km_med_max'][0]:>5}/{d['km_med_max'][1]:<5} {d['kt_med_max'][0]:>5}/{d['kt_med_max'][1]:<5} "
          f"{d['ke_med_max'][0]:>5}/{d['ke_med_max'][1]:<5} "
          f"{d['k0_curve'][KS.index(32)]:>7.4f} {d['km_curve'][KS.index(32)]:>7.4f} {d['km_curve'][KS.index(64)]:>7.4f} "
          f"{d['km_curve'][KS.index(128)]:>8.4f} {d['cone_cross']:>6} {str(d['cp_km_32_64_128']):>16} {tag:>10}")

print()
print('== C: the honest number (parent b1 scenes; caught curves from battle.jsonl) ==')
secs = {s: battle[s]['setup_secs_within'] + battle[s]['setup_secs_cross'] for s in battle}
cone = {s: battle[s]['cone_pairs'] for s in battle}
for d in fix:
    if d.get('part') != 'C':
        continue
    s = d['scene']
    cu = battle[s]['caught_union_k']
    # smallest k on the grid with caught == 1.0
    k0 = next(k for k, c in zip(KS, cu) if c >= 1.0)
    p0 = d[f'pairs_k{k0}']
    print(f"  {s}: n={d['n_total']}, zero-miss k={k0} (caught {cu[KS.index(k0)]:.4f}), "
          f"pairs@k={k0}: {p0}, window sections {secs[s]}, cone pairs {cone[s]} -> "
          f"{secs[s]/p0:.2f}x / {cone[s]/p0:.2f}x at zero miss")
    print(f"    pairs@16: {d['pairs_k16']} -> {secs[s]/d['pairs_k16']:.2f}x but caught(16)={cu[KS.index(16)]:.4f} "
          f"({(1-cu[KS.index(16)])*100:.1f}% silently missed)")

print()
print('== C+: the quantized battle (a-q scenes): pair budget at the measured kmax ==')
for d in fix:
    if d.get('part') != 'A' or d['spread'] != 'q':
        continue
    n = d['n_a'] + d['n_b']
    kmax = d['kmax_uc']
    pkmax = n * kmax - kmax * (kmax + 1) // 2
    p8 = n * 8 - 8 * 9 // 2
    if d['orbits'] == 20:
        print(f"  q H={d['orbits']:.0f}: kmax={kmax} (flat to 320), caught_uc(8)={d['caught_uc_k'][KS.index(8)]:.4f}; "
              f"pairs@kmax={pkmax}, pairs@8={p8}, window sections {secs['b1-cross-150']}, cone {cone['b1-cross-150']} "
              f"-> {secs['b1-cross-150']/p8:.1f}x eternal at k=8 (this scene's cone = the b1-150 cone)")
