#!/usr/bin/env python3
"""Summarise the depth ladder: digest identity, the record stack's growth law, the bill."""
import re, sys, os, math

R = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
rows = {}
for f in sorted(os.listdir(os.path.join(R, "flights"))):
    if not f.endswith(".txt"):
        continue
    txt = open(os.path.join(R, "flights", f)).read()
    g = lambda p: (re.search(p, txt, re.M) or [None]) and re.search(p, txt, re.M)
    d = g(r"^digest ([0-9a-f]{64})")
    c = g(r"^census cycles (\d+) passages (\d+) .*?demoted_cycles (\d+) demoted_passages (\d+) dead (\d+)")
    h = g(r"^history bodies_with (\d+) segments (\d+) max (\d+) seg_per_body ([\d.]+) plan_items (\d+) segment_b (\d+)")
    b = g(r"^bodies (\d+) bytes_per_body (\d+) catalogue_live (\d+) demotions (\d+) promotions (\d+)")
    s = g(r"^kicks (\d+) opens (\d+)")
    r = g(r"^reached (\d+) .*?wall_s ([\d.]+) rss_mb (\d+) hwm_mb (\d+)")
    pp = g(r"passage: demotions (\d+) promotions (\d+)")
    if d and h and b:
        rows[f[:-4]] = dict(
            digest=d.group(1), cycles=int(c.group(1)) if c else -1,
            passages=int(c.group(2)) if c else -1,
            dem_cyc=int(c.group(3)) if c else -1, dem_pas=int(c.group(4)) if c else -1,
            dead=int(c.group(5)) if c else -1,
            nb=int(h.group(1)), seg=int(h.group(2)), segmax=int(h.group(3)),
            segpb=float(h.group(4)), plan=int(h.group(5)), segb=int(h.group(6)),
            bodies=int(b.group(1)), bpb=int(b.group(2)), cat=int(b.group(3)),
            dem=int(b.group(4)), pro=int(b.group(5)),
            pdem=int(pp.group(1)) if pp else 0, ppro=int(pp.group(2)) if pp else 0,
            kicks=int(s.group(1)) if s else -1, opens=int(s.group(2)) if s else -1,
            wall=float(r.group(2)) if r else -1, rss=int(r.group(3)) if r else -1,
        )

hdr = f"{'flight':16} {'cut':>6} {'seg/body':>8} {'max':>5} {'bpb':>6} {'rss':>5} {'promos':>8} {'passPro':>8} {'digest'}"
print(hdr)
for k in sorted(rows):
    v = rows[k]
    cut = re.search(r"(\d+)k", k)
    print(f"{k:16} {cut.group(1)+'k' if cut else '?':>6} {v['segpb']:8.2f} {v['segmax']:5d} {v['bpb']:6d} {v['rss']:5d} {v['pro']:8d} {v['ppro']:8d} {v['digest'][:12]}")

# digest identity: belt ctl vs all at the deepest shared cut; comet all vs ctl at 32k
def dg(name):
    v = rows.get(name, {}).get("digest")
    return v
belt_ok = dg("belt_ctl_96k") and dg("belt_ctl_96k") == dg("belt_all_96k")
print("\nidentity: belt 96k ctl==all:", bool(belt_ok),
      "| comet 64k (N=25) ctl==all:", bool(dg("comet25_ctl_64k") and dg("comet25_ctl_64k") == dg("comet25_all_64k")))

def fit(names, label):
    pts = []
    for n in names:
        if n in rows:
            m = re.search(r"(\d+)k", n)
            pts.append((int(m.group(1)) * 1000, rows[n]["segpb"], rows[n]["bpb"], rows[n]["seg"], rows[n]["rss"]))
    if len(pts) >= 2:
        (t0, s0, b0, n0, r0), (t1, s1, b1, n1, r1) = pts[0], pts[-1]
        alpha = math.log(s1 / s0) / math.log(t1 / t0) if s0 > 0 and s1 > 0 else float("nan")
        print(f"\n{label}: seg/body {s0:.2f} -> {s1:.2f} over t x{t1//t0}: exponent {alpha:+.2f}")
        for t, s, b, n, r in pts:
            print(f"  cut {t:>7}: seg/body {s:8.2f}  bpb {b:7d}  segments {n:6d}  rss_mb {r}")

print()
fit(["belt_all_32k", "belt_all_48k", "belt_all_96k"], "belt (all: saturation)")
fit(["comet_ctl_3k", "comet_ctl_32k"], "comet ctl N=100 (shipped: growth)")
fit(["comet25_ctl_32k", "comet25_ctl_64k"], "comet ctl N=25 (shipped: depth)")
if "comet25_all_64k" in rows:
    print(f"comet all N=25 64k: seg/body {rows['comet25_all_64k']['segpb']:.2f} bpb {rows['comet25_all_64k']['bpb']} rss {rows['comet25_all_64k']['rss']}")
if "comet25_ctl_32k" in rows and "comet_ctl_32k" in rows:
    print(f"intensivity check at 32k ctl: N=100 {rows['comet_ctl_32k']['segpb']:.2f} vs N=25 {rows['comet25_ctl_32k']['segpb']:.2f} seg/body")
