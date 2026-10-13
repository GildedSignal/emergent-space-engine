#!/usr/bin/env python3
"""Summarize the ruin-probe matrix: digest identity per phase, the compounding ladder, the fix's
latency price, and the straddle limit. One line per fact; exits 1 if a prediction fails."""
import math, re, sys
from pathlib import Path

rows = []
for line in Path(sys.argv[1] if len(sys.argv) > 1 else "matrix.txt").read_text().splitlines():
    d = dict(re.findall(r"(\w+)=(\S+)", line))
    d["px_py"] = [float(x) for x in d["px_py"].split()]
    rows.append(d)

def find(**kw):
    return [r for r in rows if all(re.fullmatch(v, str(r[k])) for k, v in kw.items())]

def sep(a, b):
    return math.dist(a["px_py"], b["px_py"])

print("== P1: the hole, raw mode, cut 84M, rtf 100, members 48")
raw4 = find(mode="raw", cut="84000000", rtf="100", members="48", script="std")
digs = {r["digest"] for r in raw4}
print(f"arms={len(raw4)} distinct digests={len(digs)} (60rich/60starve/30/144)")
for r in raw4:
    print(f"  fps={r['fps']} starve={r['starve']}: {r['digest'][:12]} enc={r['encounters']} contacts={r['contacts']} ticks={r['input_ticks']}")
ok1 = len(digs) == len(raw4)

print("== P2: compounding, raw 60rich vs 60starve, members 48")
prev = None
for cut in ("84000000", "252000000", "756000000"):
    a = find(mode="raw", fps="60", starve="0", cut=cut)[0]
    b = find(mode="raw", fps="60", starve="1", cut=cut)[0]
    s = sep(a, b)
    grow = f" x{s/prev:.1f}" if prev else ""
    print(f"  cut {int(cut)//10**6}M: sep {s:.3e} doll units ({s*1476.246/1.496e11:.3f} AU) enc {a['encounters']}/{b['encounters']} contacts {a['contacts']}/{b['contacts']}{grow}")
    prev = s

print("== P3: the fix holds")
fix4 = find(mode="fix", cut="84000000", rtf="100", members="48", script="std")
ok3 = len({r["digest"] for r in fix4}) == 1 and len(fix4) == 4
print(f"  rtf100 4 arms -> {len({r['digest'] for r in fix4})} digest(s): {fix4[0]['digest'][:12]} ticks {fix4[0]['input_ticks']}")
r1 = find(mode="fix", cut="84000000", rtf="1", members="48", script="std")
ok3 &= len({r["digest"] for r in r1}) == 1
def arm(cut, st):
    return find(mode="raw", fps="60", starve=st, cut=cut)[0]


seps = [sep(arm(c, "0"), arm(c, "1")) for c in ("84000000", "252000000", "756000000")]
ratios = [seps[1] / seps[0], seps[2] / seps[1]]  # growth per 3x flight time

print("== P4: latency price (logged tick - sched at press), rtf 100 / rtf 1")
for r in fix4[:1] + r1[:1]:
    rtf = float(r["rtf"])
    lag = [(int(t) - int(s)) for t, s in zip(r["input_ticks"].split(","), r["press_at"].split(","))]
    wall = [l * 4.925490947e-6 / rtf for l in lag]
    print(f"  rtf {rtf:.0f}: game-s lag {[round(l*4.925490947e-6,3) for l in lag]} wall-s {[round(w,4) for w in wall]} (quantum 0.25 s wall)")
ok2 = min(ratios) > 3.0  # predictions.md: separation(3x t)/separation(t) > 3 (superlinear)
print(f"  growth ratios per 3x time: {[round(r, 1) for r in ratios]} (criterion > 3)")

print("== P5: straddle limit, fix, press 0.26 s")
st = find(mode="fix", script="straddle", cut="84000000", rtf="100", members="48")
ok4 = all(0 <= (int(t) - int(s)) * 4.925490947e-6 / float(r["rtf"]) <= 0.26
          for r in fix4[:1] + r1[:1]
          for t, s in zip(r["input_ticks"].split(","), r["press_at"].split(",")))
print(f"  30Hz ticks {st[0]['input_ticks']} digest {st[0]['digest'][:12]}")
print(f"  144Hz ticks {st[1]['input_ticks']} digest {st[1]['digest'][:12]}")
ok5 = st[0]["digest"] != st[1]["digest"]

print("== P6: 400 members")
raw400 = find(mode="raw", members="400", cut="84000000", rtf="100", script="std")
fix400 = find(mode="fix", members="400", cut="84000000", rtf="100", script="std")
print(f"  raw load pair digests {len({r['digest'] for r in raw400})} (enc {raw400[0]['encounters']}/{raw400[1]['encounters']}, contacts {raw400[0]['contacts']}/{raw400[1]['contacts']})")
print(f"  fix load pair digests {len({r['digest'] for r in fix400})}")
ok6 = len({r["digest"] for r in raw400}) == 2 and len({r["digest"] for r in fix400}) == 1

for name, ok in [("P1", ok1), ("P2", ok2), ("P3", ok3), ("P4", ok4), ("P5", ok5), ("P6", ok6)]:
    print(f"{name}: {'HELD' if ok else 'FAILED'}")
sys.exit(0 if all([ok1, ok2, ok3, ok4, ok5, ok6]) else 1)
