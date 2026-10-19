#!/usr/bin/env python3
# Recompute the dossier's headline numbers from the run's own logs (stdout of the genesis example).
# Usage: analyze.py <ship_log> <stagger_log> [seed2_log]
import re, sys

def parse(path):
    rows = []
    head = {}
    for line in open(path):
        if line.startswith("# arm") or line.startswith("# stagger"):
            for k in ("C50_steps", "step_med", "dues0_span", "span="):
                m = re.search(k + r"([\d.e+-]+)", line)
                if m:
                    head[k] = float(m.group(1))
            continue
        m = re.match(r"gen g=(\d+).*?C50=([\d.]+) C50_steps=([\d.]+) battalion=(\d+) span=([\d.e+-]+).*?load_max=([\d.]+) load_p99=([\d.]+) drift_p50=([\d.e+-]+) drift_p90=([\d.e+-]+) fc_p50=([\d.]+) fc_p90=([\d.]+)", line)
        if m:
            rows.append(dict(g=int(m.group(1)), c50=float(m.group(2)), c50s=float(m.group(3)), bat=int(m.group(4)),
                             span=float(m.group(5)), lmax=float(m.group(6)), lp99=float(m.group(7)),
                             d50=float(m.group(8)), d90=float(m.group(9)), f50=float(m.group(10)), f90=float(m.group(11))))
    return head, rows

def show(name, path):
    h, r = parse(path)
    if not r:
        print(f"{name}: EMPTY")
        return
    print(f"== {name} (step C50 at birth {h.get('C50_steps=', '?')}, dues0 span {h.get('dues0_span=', '?')}) ==")
    gcross = next((x["g"] for x in r if x["c50"] < 1.0 + 1e-9), None)
    gbelow2 = next((x["g"] for x in r if x["c50"] < 2.0), None)
    late = [x for x in r if x["g"] >= max(0, r[-1]["g"] - 4)]
    ml = max(x["lmax"] for x in late)
    print(f"  plateau-track: C50/C50_steps at g=1..7 in [{min(x['c50']/x['c50s'] for x in r if 1<=x['g']<=7 and x['c50s']>0):.3f}, {max(x['c50']/x['c50s'] for x in r if 1<=x['g']<=7):.3f}]")
    print(f"  first g with C50<2.0: {gbelow2}; first g with C50==1.0x: {gcross}; late-g load_max max: {ml:.2f}; battalion max: {max(x['bat'] for x in r)}")
    print(f"  drift p50/p90: {r[-1]['d50']:.2e}/{r[-1]['d90']:.2e}; forecast fc p50 at last g: {r[-1]['f50']:.4f} (p90 {r[-1]['f90']:.4f})")
    print(f"  C50 curve: " + " ".join(f"{x['g']}:{x['c50']:.2f}" for x in r))
    print(f"  load_max curve: " + " ".join(f"{x['g']}:{x['lmax']:.1f}" for x in r))

show("SHIP seed 1", sys.argv[1])
if len(sys.argv) > 2:
    show("STAGGER seed 1", sys.argv[2])
if len(sys.argv) > 3:
    show(sys.argv[3], sys.argv[3])
