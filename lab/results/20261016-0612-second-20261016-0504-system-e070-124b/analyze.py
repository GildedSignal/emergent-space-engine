#!/usr/bin/env python3
"""The seed-ensemble verdict table: does the locals class bind the worst frame, per seed and N?
Instrument: the per-frame population split (the Dash's per-frame event counts partition the
ordered trace rows; verified exact: traced == fe per frame, residue 0). Cross-checked against
the no-locals arm (the checker's fe_max delta metric)."""
import json, re, os

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
TICK_S = 4.925_490_947e-6
WAVE_TICK = 2_873_098_240  # the parent's heaviest tick (belt first kicks at ds/2)

def load(p):
    txt = open(p).read(); dec = json.JSONDecoder(); i = 0; objs = []
    while i < len(txt):
        while i < len(txt) and txt[i] != '{': i += 1
        if i >= len(txt): break
        o, j = dec.raw_decode(txt, i); objs.append(o); i = j
    main = objs[0]
    an = [o for o in objs if 'storm_anatomy' in o]
    kicks = int(re.search(r'kicks: (\d+)', main['stats']).group(1))
    return main, (an[0]['storm_anatomy'] if an else None), kicks

def frames(an):
    """per-frame (total, doll_ne_0, kicks_doll_ne_0) + alignment check."""
    fs = [tuple(x) for x in an['frame_split']]
    ok = an['frame_split_birth_rows'] + sum(x[0] for x in fs) + an['frame_split_residue'] == an['trace_rows']
    return fs, ok

print(f"{'seed':>4} {'N':>6} | storm fe_max/p99 | noloc fe_max/p99 | belt_fmax loc_fmax verdict | wave frame (t,nd) | argmax frame (t,nd) | kicks st/nl | align")
binds = {10000: [], 100000: []}
data = {}
for S in range(1, 9):
    for N in (10000, 100000):
        st = load(f"{R}/storm_s{S}_n{N}.json")
        nl = load(f"{R}/noloc_s{S}_n{N}.json")
        fs, ok = frames(st[1])
        tpf = st[1]['ticks_per_frame']
        wf = WAVE_TICK // tpf
        belt_fmax = max(t - nd for t, nd, _ in fs)
        loc_fmax = max(nd for t, nd, _ in fs)
        am = max(range(len(fs)), key=lambda f: fs[f][0])
        wrow = fs[wf] if wf < len(fs) else None
        binding = loc_fmax > belt_fmax
        binds[N].append((S, loc_fmax, belt_fmax) if binding else None)
        data[(S, N)] = dict(st=st, nl=nl, fs=fs, belt=belt_fmax, loc=loc_fmax, am=am, wf=wf, binding=binding)
        print(f"{S:>4} {N:>6} | {st[0]['frame_events']['max']:>8.0f}/{st[0]['frame_events']['p99']:<8.0f} | "
              f"{nl[0]['frame_events']['max']:>8.0f}/{nl[0]['frame_events']['p99']:<8.0f} | "
              f"{belt_fmax:>6} {loc_fmax:>6} {'BINDS' if binding else 'wave':>6} | "
              f"{wrow[0]},{wrow[1] if wrow else '':>4} @f{wf} | f{am}: {fs[am][0]},{fs[am][1]} | "
              f"{st[2]:>6}/{nl[2]:<6} | {'ok' if ok else 'SLIP'}")

for N in (10000, 100000):
    b = [r[0] for r in binds[N] if r]
    print(f"\nlocals bind at N={N}: seeds {b} ({len(b)}/8)")

print("\n== stream split (kicks carried by the locals class) ==")
for N in (10000, 100000):
    for S in range(1, 9):
        st, nl = data[(S, N)]['st'], data[(S, N)]['nl']
        share = (st[2] - nl[2]) / st[2]
        rate = (st[2] - nl[2]) / 300 / 30000
        if S == 1:
            print(f"N={N}:", end=" ")
        print(f"s{S}:{100*share:.0f}%@{rate:.1e}", end="  ")
    print()

print("\n== stagger engagement (1e4): moved first kicks, comb, kicks ==")
for tag, seed in (("s3", 3), ("s1", 1)):
    base = load(f"{R}/storm_{tag}_n10000.json")
    bfs, _ = frames(base[1])
    base_belt = max(t - nd for t, nd, _ in bfs)
    base_loc = max(nd for t, nd, _ in bfs)
    for bits in (26, 31):
        p = f"{R}/stag{bits}_{tag}_n10000.json"
        if not os.path.exists(p):
            continue
        st = load(p)
        fs, _ = frames(st[1])
        ids0 = {x[0]: x for x in base[1]['first_kicks_doll_ne_0']}
        ids1 = {x[0]: x for x in st[1]['first_kicks_doll_ne_0']}
        common = set(ids0) & set(ids1)
        moved = [i for i in common if ids0[i][2] != ids1[i][2]]
        dts = sorted(abs(ids1[i][2] - ids0[i][2]) * TICK_S for i in moved)
        belt = max(t - nd for t, nd, _ in fs)
        loc = max(nd for t, nd, _ in fs)
        med = dts[len(dts)//2] if dts else 0
        p90 = dts[min(len(dts)-1, int(.9*len(dts)))] if dts else 0
        print(f"seed {seed} bits {bits}: firsts {len(ids1)} moved {len(moved)} ({100*len(moved)/max(1,len(common)):.0f}%), "
              f"median|dt| {med:.0f} s p90 {p90:.0f} s | kicks {base[2]}->{st[2]} ({st[2]-base[2]:+d}) | "
              f"fe_max {base[0]['frame_events']['max']:.0f}->{st[0]['frame_events']['max']:.0f} | "
              f"loc_fmax {base_loc}->{loc} | belt_fmax {base_belt}->{belt}")
