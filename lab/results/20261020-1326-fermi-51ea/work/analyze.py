#!/usr/bin/env python3
"""51ea: the scan channel decomposed — capture, answer, window tail, drain arithmetic.
Reads the ES_SCAN_TRACE logs of the four flights; prints every dossier number."""
import sys

def load(path):
    caps, ans, bails, reuses, dolls = [], [], 0, 0, {}
    doll = None
    for line in open(path):
        if line.startswith("scan: idx"):
            doll = int(line.split("doll=")[1].split()[0])
        elif line.startswith("scan: cap"):
            d = dict(kv.split("=") for kv in line.split()[2:] if "=" in kv)
            caps.append((doll, int(d["n"]), int(d["walk"]), int(d["near"]), int(d["cands"]), float(d["us"]), float(d["walk_us"])))
        elif line.startswith("scan: ans"):
            d = dict(kv.split("=") for kv in line.split()[2:] if "=" in kv)
            ans.append((int(d["cands"]), int(d["en"]), float(d["us"]), float(d["cart_us"]), float(d["cand_us"]), int(d["e"])))
        elif line.startswith("scan: radialbail"):
            bails += 1
        elif line.startswith("scan: reuse"):
            reuses += 1
    return caps, ans, bails, reuses

def pct(v, q):
    s = sorted(v)
    return s[min(len(s) - 1, int(len(s) * q))]

for name, label in [("d1b", "1e5 burn"), ("d2", "1e5 coast"), ("d3", "3e4 burn"), ("d4_1e5_burn_era2", "1e5 burn (2nd draw)")]:
    caps, ans, bails, reuses = load(f"{name}.log")
    if not caps:
        continue
    n = caps[0][1]
    root = [c for c in caps if c[0] == 0]
    cap_us = [c[5] for c in caps]
    walk_cand = [c[6] for c in caps if c[3] > 0]
    print(f"== {label} (n={n}): caps={len(caps)} bails={bails} reuses={reuses} ({reuses/(reuses+len(caps)):.0%} of captures)"
          f" distinct answers={len(ans)} f_d={len(ans)/(len(ans)+reuses):.2f}")
    print(f"   capture: us p50={pct(cap_us,0.5):.1f} p99={pct(cap_us,0.99):.1f} max={max(cap_us):.1f} |"
          f" per-candidate {sum(walk_cand)/len(walk_cand):.3f} us (indexed path)")
    if root:
        rc = [c[4] for c in root]
        print(f"   root doll (with the belt): caps={len(root)} cands p50={pct(rc,0.5)} p90={pct(rc,0.9)} max={max(rc)}"
              f" (max/n={max(rc)/n:.1e})")
    d2c = [c[4] for c in caps if c[0] == 2]
    if d2c:
        print(f"   doll 2 (locals, fixed ~200): cands p50={pct(d2c,0.5)} max={max(d2c)} (N-flat)")
    if ans:
        cu = [a[4] for a in ans]
        print(f"   answer: p50={pct([a[2] for a in ans],0.5):.0f} us max={max(a[2] for a in ans):.0f} us |"
              f" cand_us p50={pct(cu,0.5):.2f} p99={pct(cu,0.99):.2f} | cart share={sum(a[3] for a in ans)/sum(a[2] for a in ans):.3f} |"
              f" en p50={pct([a[1] for a in ans],0.5)} max={max(a[1] for a in ans)}")

print("\n== 1e9 composition (fixed density, window fractions measured at 1e5; cand_us 4.96, cap-cand 0.64)")
tail_frac = 1804 / 100028
p50_frac = 7 / 100028
for tag, frac in [("p50 window", p50_frac), ("max window (measured tail)", tail_frac), ("mid-tail (9ed1 bite windows ~500/1e5)", 500/100028)]:
    cands = frac * 1e9
    print(f"   {tag}: cands={cands:.2e} -> answer={cands*4.96e-6:.3g} s, capture={cands*0.64e-6:.3g} s")
print(f"   drain bite: 2048 backlog x f_d 0.62 x per-answer(p50-window) = {2048*0.62*p50_frac*1e9*4.96e-6:.0f} s")
print(f"              2048 x 0.62 x mid-tail = {2048*0.62*500/100028*1e9*4.96e-6:.0f} s")
print(f"   9ed1 bite reconciliation: 442.9 ms / en=178 = {442.9/178*1000:.0f} us/answer = cands {442.9/178/4.96e-3:.0f}"
      f" (mid-tail); 1273.5/178 = {1273.5/178*1000:.0f} us/answer = cands {1273.5/178/4.96e-3:.0f}")
print(f"   amortized at play (rtf 100): capture {0.167*p50_frac*1e9*0.64e-6*100:.4g} s/s-wall,"
      f" answers {0.104*p50_frac*1e9*4.96e-6*100:.4g} s/s-wall")
