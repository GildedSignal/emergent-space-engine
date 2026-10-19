#!/usr/bin/env python3
"""Analyse the quantum sweep: per-class cadence, element drift vs the k=7 control,
bounded-vs-walk per checkpoint. Regenerates every number in the dossier from raw/q*_o*.log."""
import re, sys, glob, os
here = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(here, "raw")

def parse(path):
    cad2, el, summ = {}, {}, {}
    for line in open(path):
        f = line.split()
        if line.startswith("CAD2"):
            m = re.match(r"CAD2 k (\S+) (\S+) id (\S+) interval_d (\S+) a_au (\S+) kicks_per_orbit (\S+)", line)
            if m:
                cad2[int(m.group(3))] = (m.group(2), float(m.group(4)), float(m.group(6)))
        elif line.startswith("EL"):
            m = re.match(r"EL k (\S+) ck (\S+) t_yr (\S+) (\S+) id (\S+) a (\S+) e (\S+) alive (\S+) refus (\S+)", line)
            if m:
                el[(int(m.group(2)), int(m.group(5)))] = (m.group(4), float(m.group(6)), float(m.group(7)), m.group(8), int(m.group(9)))
        elif line.startswith("SUM"):
            summ = dict(zip(f[3::2], f[4::2]))
    return cad2, el, summ

arms = {}
for path in sorted(glob.glob(os.path.join(R, "q*_o2.log")) + glob.glob(os.path.join(R, "q7_o6.log")) + glob.glob(os.path.join(R, "q2_o6.log"))):
    m = re.search(r"q(-?\d+)_o(\d)\.log", path)
    k, orb = int(m.group(1)), int(m.group(2))
    arms[(k, orb)] = parse(path)

ids = sorted({i for (_, i) in arms[(7, 2)][1]})
cls = {i: arms[(7, 2)][1][(0, i)][0] for i in ids}
cks = sorted({c for (c, _) in arms[(7, 2)][1]})

print("== cadence (steady, 2-orbit arms): interval days, kicks per own orbit ==")
print(f"{'class':6} {'id':>3} " + " ".join(f"k={k:>4}" for k in [7, 5, 3, 2, 1, 0, -2]))
for i in ids:
    row = []
    for k in [7, 5, 3, 2, 1, 0, -2]:
        c = arms.get((k, 2), ({}, {}, {}))[0].get(i)
        row.append(f"{c[2]:7.0f}" if c else "      -")
    print(f"{cls[i]:6} {i:>3} " + " ".join(row))

print("\n== drift vs the k=7 control, 2-orbit arms: |a_k - a_7|/a_7 by checkpoint ==")
print(f"{'class':6} {'id':>3} {'a_7(au)':>8} " + " ".join(f"{'k='+str(k):>9}" for k in [5, 3, 2, 1, 0, -2]))
for i in ids:
    a7 = arms[(7, 2)][1][(0, i)][1]
    last = max(cks)
    row = []
    for k in [5, 3, 2, 1, 0, -2]:
        e = arms.get((k, 2))
        if not e:
            row.append("        -")
            continue
        pair = e[1].get((last, i))
        base = e[1].get((0, i))
        if not pair or not base:
            row.append("        -")
            continue
        row.append(f"{abs(pair[1]-arms[(7,2)][1][(last,i)][1])/a7:9.2e}" if pair[3] == "true" else "     dead")
    print(f"{cls[i]:6} {i:>3} {a7:8.3f} " + " ".join(row))

print("\n== walk vs bounded: |a_k - a_7|/a_7 per checkpoint (last body state per class shown; long arms) ==")
for (k, orb) in [(7, 6), (2, 6)]:
    if (k, orb) not in arms:
        continue
    a2 = arms[(k, 2)][1]
    a6 = arms[(k, orb)][1]
    for i in ids:
        if cls[i] != "belt":
            continue
        r7_2, r7_6 = arms[(7, 2)][1], arms[(7, 6)][1]
        v2 = abs(a2[(8, i)][1] - r7_2[(8, i)][1]) / r7_2[(0, i)][1]
        v6 = abs(a6[(8, i)][1] - r7_6[(8, i)][1]) / r7_6[(0, i)][1]
        print(f"k={k:>2} belt id {i}: 2-orbit drift {v2:.2e} -> 6-orbit drift {v6:.2e}  (ratio {v6/max(v2,1e-30):.1f})")

print("\n== per-checkpoint walk check (k=-2, 2-orbit arm), all belt: drift at ck2/4/6/8 ==")
r7 = arms[(7, 2)][1]
for i in ids:
    if cls[i] != "belt":
        continue
    ds = []
    for ck in [2, 4, 6, 8]:
        pair = arms[(-2, 2)][1].get((ck, i))
        ds.append(f"{abs(pair[1]-r7[(ck,i)][1])/r7[(0,i)][1]:.2e}" if pair and pair[3] == "true" else "dead")
    print(f"belt id {i}: " + " ".join(ds))

print("\n== kick bills (SUM) ==")
for (k, orb), (_, _, s) in sorted(arms.items()):
    print(f"k={k:>3} orbits={orb} kicks={s.get('kicks','?'):>7} wall_s={s.get('wall_s','?'):>7} refused={s.get('refused','?')} lost={s.get('lost','?')}")
