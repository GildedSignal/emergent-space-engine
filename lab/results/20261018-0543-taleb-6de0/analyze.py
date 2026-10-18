#!/usr/bin/env python3
"""Summarize the runaway-tail run (20261018-0543-taleb-6de0). Reads the screen JSONs and
the kick traces, prints every number quoted in dossier.md. Units: root units (M_star);
P = one planet period in root ticks; sep, R_p in root units; R_H = sep*(mu/3)^(1/3)."""
import json, math, sys

MU = 0.01
SEP = 5.27e8 / (1.0 - MU)      # judge sep -> root units
RP = 4.84e4 / (1.0 - MU)
P = 2 * math.pi * SEP ** 1.5   # planet period, root ticks
C = 10.0 * (MU / (1 - MU)) / SEP  # the clock's c: FLOOR_FACTOR * sum gm_j/a_j (ext.rs)
B = 30.0 * C
DS = P / (2 ** 7 * (1.0 / C ** 2 + 1.0 / (B * C)))  # the fictitious step (ext.rs constants)

def load(d):
    return [json.load(open(f"{d}/ic-{i}-{j}.json")) for i in range(12) for j in range(12)]

print(f"constants: c={C:.3e} b={B:.3e} ds={DS:.3e} A=ds/b={DS/B:.2f} P={P:.3e} ticks")

def screen(name, d, horizon_note):
    rows = load(d)
    ev = sorted(r["events"] for r in rows)
    tot = sum(ev)
    capped = [r for r in rows if r["capped"]]
    dead = [r for r in rows if not r["alive"]]
    kp = sorted(r["kicks"] / r["cp"][-1][0] for r in rows if r["cp"])
    print(f"\n== {name} ({horizon_note}): {len(rows)} ICs")
    print(f"   events total={tot} median={ev[len(ev)//2]} max={ev[-1]}")
    print(f"   capped={len(capped)} holding {sum(r['events'] for r in capped)/tot:.1%} of all events"
          f" | top1={ev[-1]/tot:.1%} | dead={len(dead)} | median kicks/P={kp[len(kp)//2]:.0f}")
    if capped:
        ce = sum(r["events"] / r["secs"] for r in capped) / len(capped)
        nc = [r for r in rows if not r["capped"]]
        ne = sum(r["events"] / r["secs"] for r in nc) / len(nc)
        print(f"   events/s: uncapped~{ne:.0f} ({1e6/ne:.0f} us/event) capped~{ce:.0f} ({1e6/ce:.0f} us/event, x{ce and ne/ce:.1f})")
    return rows, capped

rows2, capped = screen("mu=1e-2", "work/screen-m2-16", "16 P, cap 100k")
screen("mu=1e-2 early", "work/screen-m2", "4 P, cap 100k")
screen("mu=1e-3 control", "work/screen-m3", "64 P (16x horizon), cap 100k")

# the capped ICs' rate walk (convexity): grinder b
r = [x for x in capped if abs(x["du"] + 0.682) < 0.01 and abs(x["phi"] - 81.8) < 0.1][0]
sl = [(r["cp"][i+1][0], (r["cp"][i+1][2] - r["cp"][i][2]) / (r["cp"][i+1][0] - r["cp"][i][0])) for i in range(len(r["cp"]) - 1)]
print("\ngrinder (du=-0.68, phi=81.8) events/P:", " ".join(f"{p:.1f}P:{int(s)}" for p, s in sl[::4]))

def trace(fn):
    # trace.rs line: t doll x0 x1 nsecs y |v| (gm p0 p1)*nsecs full — y is always
    # Some(y) at the kick call site, so nsecs=1 here means 11 fields, full last.
    out = []
    for ln in open(fn):
        f = ln.split()
        t = int(f[0]); x = (float(f[2]), float(f[3])); n = int(f[4])
        y = float(f[5]); v = float(f[6])
        p = (float(f[8]), float(f[9])); full = int(f[7 + 3 * n])
        out.append((t, x, p, v, y, full))
    return out

print("\n== deep traces (end state at the cap):")
for tag in ["a", "b", "c", "a2", "d", "e", "f", "g", "h"]:
    rows = trace(f"work/trace/k{tag}.txt")
    t, x, p, v, y, full = rows[-1]
    rpl = [math.hypot(q[1][0]-q[2][0], q[1][1]-q[2][1]) for q in rows]
    rs = math.hypot(*x)
    print(f"   {tag}: kicks_sampled={len(rows)} t_end={t/P:7.3f}P r_star={rs/SEP:6.2f}sep r_pl={math.hypot(x[0]-p[0],x[1]-p[1])/SEP:6.2f}sep "
          f"min_r_pl={min(rpl)/RP:6.0f}R_p v={v:.3e} interval={full}")

# the feedback arithmetic on a2's tail: dt = A/y, dv/kick from the ratchet
rows = trace("work/trace/ka2.txt")
tail = [q for q in rows if q[3] and q[3] > 0.15]
ys = [q[4] for q in tail]; dts = [q[5] for q in tail]; vs = [q[3] for q in tail]
A = [d * y for d, y in zip(dts, ys)]
dvs = sorted((vs[i + 1] - vs[i]) / 16 for i in range(len(vs) - 1))
print(f"\n== a2 storm tail (v>0.15, n={len(tail)}): dt*y=A: mean={sum(A)/len(A):.2f} min={min(A):.2f} "
      f"max={max(A):.2f} (constant to {(max(A)-min(A))/(sum(A)/len(A)):.1%}; constants give ds/b={DS/B:.2f})")
print(f"   -> dt = A/y with y = v^2/2 (last ratio {ys[-1]/(vs[-1]**2/2):.3f}); ratchet dv/kick "
      f"median={dvs[len(dvs)//2]:.2e} IQR=({dvs[len(dvs)//4]:.1e},{dvs[3*len(dvs)//4]:.1e}) "
      f"all_positive={all(d > 0 for d in dvs)}")
print(f"   v {vs[0]:.3f}->{vs[-1]:.3f}; interval {dts[0]}->{dts[-1]} ticks; energy minted vs orbital KE "
      f"(v_orb=4.35e-5): x{(vs[-1]/4.35e-5)**2:.1e}")
tk = [int(ln.split()[0]) for ln in open("work/trace/ka.txt")]
print(f"   freeze: the last 25600 kicks of the 1.5M run advance the clock {tk[-1]-tk[-1600]} ticks "
      f"= {(tk[-1]-tk[-1600])/P:.1e} P; the 16 P horizon is unreachable")
