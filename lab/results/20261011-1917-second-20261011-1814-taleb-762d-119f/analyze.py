#!/usr/bin/env python3
"""Decompose the stall: per members count, density D (events per presented game-second)
and throughput T (events per wall-second) at each budget; check delivered ~= T/D;
stutter structure from the per-frame series."""
import json, csv, glob, os, sys

TICK = 4.925_490_947e-6
D = os.path.join(os.path.dirname(__file__), 'data')

def load(name):
    d = json.load(open(os.path.join(D, name + '.json')))
    frames = d['frames']
    paced = d['paced']
    # dash.wall_seconds = sum(wall_dt): 600/60 = 10 nominal for unpaced; ~real for paced
    nominal = frames / 60.0 if not paced else d['wall_seconds']
    dash_events = d['events_per_second'] * nominal
    wall = d['wall_seconds']
    pres_s = d['presented_tick_at_end'] * TICK
    T = dash_events / wall                      # events per wall-second (real)
    e = dash_events / frames                    # events per frame
    dens = dash_events / pres_s if pres_s > 0 else float('inf')  # events per presented game-second
    delivered = pres_s / wall
    return dict(name=name, d=d, frames=frames, wall=wall, dash_events=dash_events,
                T=T, e=e, D=dens, pres_s=pres_s, delivered=delivered,
                med=d['rtf']['median'], low1=d['rtf']['lowest_1pct'],
                eng_p50=d['where_the_time_goes_ms']['engine']['p50'],
                frame_p50=d['frame_ms']['p50'], digest=d['digest'][:8],
                evps=d['events_per_second'], overflow=d['rtf']['overflow_frames'],
                bodies=d['bodies'])

def stutter(name):
    """Structure of presented-time advance from the per-frame series."""
    path = os.path.join(D, name + '.csv')
    if not os.path.exists(path):
        return None
    rows = list(csv.DictReader(open(path)))
    rtf = [float(r['rtf']) for r in rows]
    game = [r * (1.0 / 60.0) for r in rtf]     # game-seconds per frame (rtf = game/wall_dt, wall_dt=1/60 nominal)
    tot = sum(game)
    if tot <= 0:
        return dict(frozen=1.0, top10=0.0, jumps=0)
    frozen = sum(1 for r in rtf if r < 0.01) / len(rtf)
    srt = sorted(game, reverse=True)
    top10 = sum(srt[:len(srt)//10]) / tot      # share of game time in the busiest 10% of frames
    jumps = sum(1 for g in game if g > 1.0)    # frames advancing > 1 game-second
    nz = [g for g in game if g > 0]
    return dict(frozen=frozen, top10=top10, jumps=jumps,
                max_jump=max(game) if game else 0)

print(f"{'cell':16s} {'bod':>4s} {'wall':>6s} {'e/fr':>6s} {'T(ev/s)':>8s} {'D(ev/gs)':>8s} "
      f"{'T/D':>9s} {'deliv':>9s} {'ratio':>5s} {'med':>9s} {'froz':>5s} {'top10':>5s} {'digest':>8s}")
rows = []
for name in sorted(os.listdir(D)):
    if not name.endswith('.json'):
        continue
    cell = name[:-5]
    try:
        c = load(cell)
    except Exception as ex:
        print(cell, 'ERR', ex); continue
    st = stutter(cell) or {}
    td = c['T'] / c['D'] if c['D'] > 0 else float('inf')
    ratio = c['delivered'] / td if td > 0 else float('nan')
    rows.append((cell, c, st, td, ratio))
    print(f"{cell:16s} {c['bodies']:4d} {c['wall']:6.2f} {c['e']:6.2f} {c['T']:8.0f} {c['D']:8.2f} "
          f"{td:9.1f} {c['delivered']:9.1f} {ratio:5.2f} {c['med']:9.2f} "
          f"{st.get('frozen', float('nan')):5.2f} {st.get('top10', float('nan')):5.2f} {c['digest']:>8s}")

print("\nDigest equality across budgets (same members, same cut):")
from collections import defaultdict
by_m = defaultdict(dict)
for cell, c, st, td, ratio in rows:
    if cell.startswith(('G-', 'B-', 'P-')):
        m = cell.split('-')[1] if cell.startswith('G-') else ('m48' if cell.startswith('B-') else cell.split('-')[1])
        by_m[m][cell] = c['digest']
for m, cells in sorted(by_m.items()):
    print(' ', m, len(set(cells.values())), 'distinct digests among', list(cells))
