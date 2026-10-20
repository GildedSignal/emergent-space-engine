#!/usr/bin/env python3
"""Compose the mint census (run 20261020-1621-system-7fd3) from the two arm logs."""
import re, sys

def parse(path):
    out = {}
    for line in open(path):
        m = re.search(r'census\[space\]: mints (\d+) compile_ms ([\d.]+) reads_state (\d+) reads_radius (\d+) mint_own (\d+)', line)
        if m:
            out.update(mints=int(m.group(1)), compile_ms=float(m.group(2)),
                       reads_state=int(m.group(3)), reads_radius=int(m.group(4)), mint_own=int(m.group(5)))
        m = re.search(r'ucensus\[universe\]: kicks (\d+) kick_ms ([\d.]+) rebinds (\d+) rebind_ms ([\d.]+) hist_queries (\d+) hist_hits (\d+)', line)
        if m:
            out.update(kicks=int(m.group(1)), kick_ms=float(m.group(2)), rebinds=int(m.group(3)),
                       rebind_ms=float(m.group(4)), hist_q=int(m.group(5)), hist_hit=int(m.group(6)))
        m = re.search(r'kicks (\d+) \(', line)
        if m:
            out.setdefault('flight_kicks', int(m.group(1)))
        m = re.search(r'dashboard bytes/body (\d+)', line)
        if m:
            out['bpb'] = int(m.group(1))
        m = re.search(r'catalogue (\d+) entries', line)
        if m:
            out['cat'] = int(m.group(1))
        m = re.search(r'foot_end_mb=(\d+)', line)
        if m:
            out['end_mb'] = float(m.group(1))
    return out

for arm in ('10000', '30000'):
    d = parse(f'lab/results/20261020-1621-system-7fd3/out/arm-{arm}.log')
    if not d:
        continue
    mints, kicks = d['mints'], d['kicks']
    ext = d['reads_state'] + d['reads_radius']
    print(f"arm N={arm}: mints {mints} kicks(fired) {kicks} rebinds {d['rebinds']}")
    print(f"  compile_ms {d['compile_ms']:.0f}  kick_ms {d['kick_ms']:.0f}  rebind_ms {d['rebind_ms']:.0f}")
    print(f"  compile/rebind {d['compile_ms']/max(d['rebind_ms'],1e-9):.3f}   rebind/kick {d['rebind_ms']/max(d['kick_ms'],1e-9):.3f}")
    print(f"  external reads {ext} (state {d['reads_state']}, radius {d['reads_radius']})  mint_own {d['mint_own']}")
    print(f"  reads per mint {ext/max(mints,1):.3f}   mint_own per mint {d['mint_own']/max(mints,1):.3f}")
    print(f"  history queries {d['hist_q']} hits {d['hist_hit']}  hits per mint {d['hist_hit']/max(mints,1):.5f}")
    print(f"  compile µs per mint {d['compile_ms']*1e3/max(mints,1):.2f}   kick µs per kick {d['kick_ms']*1e3/max(kicks,1):.2f}")
    if 'bpb' in d:
        print(f"  dashboard bytes/body {d.get('bpb')} catalogue {d.get('cat')} end_mb {d.get('end_mb')}")
