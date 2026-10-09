#!/usr/bin/env python3
"""Stage-share analysis for the kick bench (lab run 20261009-0521).
Usage: python3 analyze.py <json> [json ...]"""
import json, sys

def slots(report: str):
    out = {}
    for line in report.split("\n"):
        parts = line.split()
        if not parts:
            continue
        tag = parts[0].split("_calls")[0]
        vals = dict(p.split("=") for p in parts)
        out[tag] = vals
    return out

for path in sys.argv[1:]:
    d = json.load(open(path))
    print(f"=== {path} ===")
    print(f"samples={d['samples']} digest={d['replay_digest'][:16]} "
          f"memo q-hit={d['memo']['quantized_hit_rate']:.12f} shapes={d['memo']['quantized_shapes']} rebinds={d['memo']['cycle_rebinds']}")
    if 'ships_mean' in d:
        print(f"ships_mean={d['ships_mean']:.1f} game_s={d['game_seconds']:.0f} "
              f"cadence={d['cadence_kicks_per_ship_per_game_s']:.3e} kicks/ship/game-s")
    a = d['kick_us_all']
    if a['median'] is None:
        print("all: no non-cold samples (cold-mode run)")
    else:
        print(f"all: median={a['median']:.2f} mean={a['mean']:.2f} p99={a['p99']:.2f} us")
    if d.get('doll_histogram'):
        print("dolls:", d['doll_histogram'])
    if d.get('paths'):
        for p, v in d['paths'].items():
            for pop in ('made', 'leavers'):
                if v[pop]['samples']:
                    print(f"  {p}/{pop}: n={v[pop]['samples']} median={v[pop]['median']:.2f} mean={v[pop]['mean']:.2f}")
    for tag, vals in slots(d['stages_total']).items():
        calls = int(vals[f"{tag}_calls"])
        if calls == 0:
            continue
        tot = int(vals[f"{tag}_total_ns"])
        print(f"{tag}: calls={calls} total={tot/1e6:.1f}ms mean={tot/calls/1e3:.2f}us")
        for st in ("readout", "gather", "forces_quant", "rebind", "other"):
            v = int(vals[f"{tag}_{st}_ns"])
            print(f"   {st:13s} {v/1e6:9.2f}ms {100*v/tot:5.1f}%")
        print(f"   rebind_calls={vals[f'{tag}_rebind_calls']} (no-fire {100*(1-int(vals[f'{tag}_rebind_calls'])/calls):.2f}%)")
        # units audit: calls x mean(sampled) vs total_ns only for bench phases
    for coldkey in ('kick_us_cold', 'kick_us_warm_paired'):
        if d.get(coldkey) and d[coldkey]['samples']:
            print(f"{coldkey}: median={d[coldkey]['median']:.2f} mean={d[coldkey]['mean']:.2f} n={d[coldkey]['samples']}")
