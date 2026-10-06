#!/usr/bin/env python3
"""Analysis of rows.json: pass rates by configuration and by bin, error ratios, kick costs."""
import json
import sys

rows = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "rows.json"))
IN_LO, IN_HI = 1.2, 50.0
band = [r for r in rows if IN_LO <= r["ca_RJ"] <= IN_HI]
print(f"seeds: {len(rows)} total, {len(band)} in B13's band (closest approach {IN_LO}-{IN_HI} R_J)")
print(f"heliocentric e in band: min {min(r['e'] for r in band):.3f} "
      f"median {sorted(r['e'] for r in band)[len(band)//2]:.3f} max {max(r['e'] for r in band):.3f}")
print(f"v_inf spread in band: {sorted(set(r['vinf'] for r in band))}")

def worst(r, m):
    return max(r[f"{m}_errE"], r[f"{m}_errL"])


print("\n== pass counts (err <= 1% on both E and L; degenerate |dL|<1e-4 not judged) ==")
for m in ("A", "A2", "A01", "A002", "B", "C"):
    n = sum(1 for r in band if r[f"{m}_pass"])
    wk = sum(r[f"{m}_kicks"] for r in band)
    w = max(worst(r, m) for r in band)
    med = sorted(worst(r, m) for r in band)[len(band) // 2]
    print(f"{m:5s}: {n:3d}/{len(band)}  median worst-err {med:.3g}  worst {w:.3g}  total kicks {wk}")

print("\n== A (plane rule) failures in band: where do they sit? ==")
afail = [r for r in band if not r["A_pass"]]
for r in sorted(afail, key=lambda x: x["vinf"]):
    print(f"  vinf={r['vinf']:4.0f} e={r['e']:.3f} ca={r['ca_RJ']:5.1f} "
          f"A:{worst(r,'A'):.3g} A2:{worst(r,'A2'):.3g} A002:{worst(r,'A002'):.3g} "
          f"B:{worst(r,'B'):.3g} {'PASS' if r['B_pass'] else 'FAIL'}")

print("\n== B failures in band ==")
bfail = [r for r in band if not r["B_pass"]]
for r in bfail:
    print(f"  vinf={r['vinf']:4.0f} e={r['e']:.3f} ca={r['ca_RJ']:5.1f} "
          f"A:{worst(r,'A'):.3g} B:{worst(r,'B'):.3g} Bkicks={r['B_kicks']}")

print("\n== bins: pass rate by v_inf (A vs B) ==")
for v in sorted(set(r["vinf"] for r in band)):
    b = [r for r in band if r["vinf"] == v]
    na = sum(1 for r in b if r["A_pass"])
    nb = sum(1 for r in b if r["B_pass"])
    nb2 = sum(1 for r in b if r["A002_pass"])
    print(f"  v_inf {v:4.0f}: A {na}/{len(b)}  A002 {nb2}/{len(b)}  B {nb}/{len(b)}")

print("\n== bins: pass rate by heliocentric e ==")
for lo, hi in ((0.0, 0.7), (0.7, 0.95), (0.95, 1.05), (1.05, 9.0)):
    b = [r for r in band if lo <= r["e"] < hi]
    if not b:
        continue
    na = sum(1 for r in b if r["A_pass"])
    nb = sum(1 for r in b if r["B_pass"])
    print(f"  e in [{lo},{hi}): n={len(b)}  A {na}  B {nb}")

print("\n== controls ==")
same = sum(1 for r in band if abs(worst(r, "A") - worst(r, "C")) < 1e-12)
a2w = sum(1 for r in band if worst(r, "A2") > worst(r, "A"))
print(f"C identical to A (jup-doll cadence irrelevant): {same}/{len(band)}")
print(f"A2 (clamp 2yr) strictly worse than A: {a2w}/{len(band)}")
imp = [worst(r, "A") / worst(r, "B") for r in band if worst(r, "B") > 0 and not r["A_pass"]]
if imp:
    imp.sort()
    print(f"A->B error reduction on A's failures: median {imp[len(imp)//2]:.3g}x  min {imp[0]:.3g}x")
kA = sum(r["A_kicks"] for r in band)
kB = sum(r["B_kicks"] for r in band)
kA2 = sum(r["A002_kicks"] for r in band)
print(f"kicks: A {kA}  B {kB} ({kB/kA:.2f}x A)  A002 {kA2} ({kA2/kA:.1f}x A)")
