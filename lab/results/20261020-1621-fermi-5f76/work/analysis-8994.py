#!/usr/bin/env python3
"""Regenerates every dossier number from the arms' logs + per-frame CSVs.
Usage: analysis.py <dir-with-D1.log,D2.log,D3.log,D*.csv>"""
import csv, re, sys

d = sys.argv[1] if len(sys.argv) > 1 else '.'
LAMBDAS = (4e-5, 8.4e-5)  # f623/0659 per-body per-game-s kick rate at 10^9, rtf 100
CLASSES = ["base(frame)", "planet", "moon", "ship", "player", "fleet/handout"]

def parse_log(p):
    t = open(p).read()
    h = re.search(r"game_s=(\d+) kicks=(\d+) events=(\d+) items=\[(.*?)\]", t)
    per_kick = float(re.search(r"item-scope ([\d.]+) KB", t).group(1))
    base_gs = float(re.search(r"base ([\d.]+) KB/game-s", t).group(1))
    scopes = {}
    for m in re.finditer(r"scope\s+\S+\s+\(\d\): allocs (\d+), bytes (\d+) \(([\d.]+) KB\), frees (\d+), freed ([\d.]+) KB, reallocs (\d+)", t):
        s = int(m.group(1))  # placeholder, fixed below
    for m in re.finditer(r"scope\s+(\S+)\s+\((\d)\): allocs (\d+), bytes (\d+) \(([\d.]+) KB\)", t):
        scopes[int(m.group(2))] = dict(allocs=int(m.group(3)), bytes=int(m.group(4)))
    for m in re.finditer(r"scope\s+(\S+)\s+\((\d)\): realloc bytes (\d+) \(([\d.]+) KB\)", t):
        scopes[int(m.group(2))]["rbytes"] = int(m.group(3))
    return dict(game_s=int(h.group(1)), kicks=int(h.group(2)),
                items=[int(x) for x in h.group(4).split(',')],
                per_kick=per_kick, base_gs=base_gs, scopes=scopes)

def med(v):
    s = sorted(v); return s[len(s)//2] if s else 0

def clusters(rows):
    item = [r['item_b']+r['item_rb']+r['player_b']+r['player_rb'] for r in rows]
    base = [r['base_b']+r['base_rb'] for r in rows]
    ev = [r['events'] for r in rows]
    em = med(ev)
    out, hot = [], [i for i in range(len(rows)) if ev[i] > 2*em]
    for i in hot:
        if out and i - out[-1][-1] <= 5: out[-1].append(i)
        else: out.append([i])
    mi, mb, inw = med(item), med(base), set(i for c in out for i in c)
    ei = sum(item[i] for i in range(len(rows)) if i not in inw)
    ee = sum(ev[i] for i in range(len(rows)) if i not in inw)
    rows_out = [(c[0], c[-1], len(c), sum(item[c[0]:c[-1]+1])/1e6,
                 sum(item[c[0]:c[-1]+1])/len(c)/mi, sum(base[c[0]:c[-1]+1])/len(c)/mb,
                 sum(item[c[0]:c[-1]+1])/max(sum(ev[c[0]:c[-1]+1])//2, 1)/1e3)
                for c in out if len(c) >= 20]
    return mi, mb, ei/max(ee//2, 1)/1e3, rows_out

print(f"{'arm':<4}{'game_s':>8}{'kicks':>9}{'ship/pl items':>15}{'item KB/kick':>14}{'% naive':>9}{'base KB/gs':>12}")
logs = {}
for name in ('D1', 'D2', 'D3'):
    a = parse_log(f'{d}/{name}.log')
    logs[name] = a
    tot = sum(s['bytes'] + s.get('rbytes', 0) for s in a['scopes'].values())
    naive = tot / a['kicks'] / 1e3
    a['naive'] = naive
    print(f"{name:<4}{a['game_s']:>8}{a['kicks']:>9}{str(a['items'][2])+'/'+str(a['items'][4]):>15}"
          f"{a['per_kick']:>14.2f}{100*a['per_kick']/naive:>8.1f}%{a['base_gs']:>12.2f}")

a = logs['D1']
ship, player = a['scopes'][3], a['scopes'][4]
ship_kb = (ship['bytes']+ship.get('rbytes',0))/1e3
player_kb = (player['bytes']+player.get('rbytes',0))/1e3
print(f"\nD1 anatomy: ship {ship_kb/1e3:.1f} MB / {a['items'][2]} items = {ship_kb/a['items'][2]:.2f} KB per ship item"
      f" (~{ship_kb/a['items'][2]/2.27:.2f} KB/kick); player {player_kb/1e3:.1f} MB / {a['items'][4]} items"
      f" = {player_kb/a['items'][4]/1e3:.2f} MB per player item = {player_kb/a['items'][4]/10028*1e3:.0f} B per body of the doll")
print(f"D1 player realloc {player.get('rbytes',0)/1e3/1e3:.1f} MB = {100*player.get('rbytes',0)/(player['bytes']+player.get('rbytes',0)):.0f}% of player term;"
      f" player share of item traffic {100*player_kb*1e3/sum((s['bytes']+s.get('rbytes',0)) for k,s in a['scopes'].items() if k != 0):.0f}%")
b = logs['D2']['scopes'][4]
print(f"D2 player realloc {b.get('rbytes',0)/1e3/1e3:.1f} MB; chains: 3,670,016 B = one ~{3670016/10028:.0f} B entry per body")

print("\nwave clusters (frame lo-hi, n, item MB, item x ebb, base x ebb, item KB/kick):")
for name in ('D1', 'D2', 'D3'):
    with open(f'{d}/{name}.csv') as f:
        rows = [{k: (int(v) if k != 'ms' else float(v)) for k, v in r.items()} for r in csv.DictReader(f)]
    mi, mb, ebb_pk, cs = clusters(rows)
    print(f" {name}: ebb item {mi/1e3:.0f} KB/f base {mb/1e3:.0f} KB/f ebb item/kick {ebb_pk:.1f} KB -> " +
          "; ".join(f"[{c[0]},{c[1]}] n{c[2]} {c[3]:.0f}MB item {c[4]:.1f}x base {c[5]:.1f}x {c[6]:.1f}KB/kick" for c in cs))

ship_kbkick = ship_kb/a['items'][2]/2.27
print("\n10^9 composition (rtf 100, 60 GB/s):")
for lam in LAMBDAS:
    ev = lam*1e9*100
    print(f" lambda {lam:g}: ship-stream marginal {ship_kbkick:.2f} KB/kick -> {ship_kbkick*ev/1e6:.1f} GB/s = {100*ship_kbkick*ev/1e6/60:.0f}%"
          f" | mixture {a['per_kick']:.2f} KB/kick -> {a['per_kick']*ev/1e6:.1f} GB/s = {100*a['per_kick']*ev/1e6/60:.0f}%")
print(f" player item at 10^9: 490 B/body x 1e9 = {490*1e9/1e9:.0f} GB allocated per player item (cc9d's row, priced)")
