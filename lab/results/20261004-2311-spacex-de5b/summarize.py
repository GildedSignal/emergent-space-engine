#!/usr/bin/env python3
"""Summarize results.jsonl into the dossier table.

Usage: python3 summarize.py   (expects ./kickcorr to have written results.jsonl)
Gates (frozen, B12/B14/B13-flavoured):
  J: max |dJ/J0| <= 1e-4 (no J gate on scene s3: planet 2 breaks the integral)
  P: apsidal precession rate within 10% of the dkd@512 reference (bound moons, defined apse)
  C: bound/escaped class matches the reference
Schemes: dkd (plane today), dkd3/dkd5 (WHFast 3rd/5th-order corrector at outputs),
y4 (Yoshida-4, 3 kicks/step), euler (negative control).
"""
import json, sys

rows = [json.loads(l) for l in open('results.jsonl')]
refs = {(r['scene'], r['moon']): r for r in rows if r['scheme'] == 'ref512'}
r2048 = {(r['scene'], r['moon']): r for r in rows if r['scheme'] == 'ref2048'}

COST = {'dkd': 1, 'dkd3': 1, 'dkd5': 1, 'y4': 3, 'euler': 1}

def gates(r, ref):
    j = (r['j_max'] <= 1e-4) if r['scene'] != 's3' else None
    if (r['prec'] == r['prec'] and ref['bound'] and ref['prec'] == ref['prec']
            and abs(ref['prec']) > 1e-12):
        prel = abs(r['prec'] - ref['prec']) / abs(ref['prec'])
        p = prel <= 0.10
    else:
        p, prel = None, float('nan')
    c = r['bound'] == ref['bound']
    return j, p, c, prel

print("reference convergence (prec: ref512 vs ref2048):")
for k in sorted(refs):
    a, b = refs[k]['prec'], r2048[k]['prec']
    if a == a and b == b and abs(b) > 1e-12:
        print(f"  {k[0]}/{k[1]:12s} rel={abs(a-b)/abs(b):.4%}  bound512={refs[k]['bound']}/{r2048[k]['bound']}")

print("\nminimum kicks/orbit (x cost) passing all gates; FAIL = none in [2..64]:")
for scene in ['s1', 's2', 's3']:
    moons = sorted({r['moon'] for r in rows if r['scene'] == scene})
    print(f"--- {scene} ---")
    hdr = f"{'scheme':7s}" + "".join(f"{m[:11]:>13s}" for m in moons)
    print(hdr)
    for sch in ['dkd', 'dkd3', 'dkd5', 'y4', 'euler']:
        line = f"{sch:7s}"
        for moon in moons:
            ref = refs[(scene, moon)]
            best = None
            for r in [x for x in rows if x['scheme'] == sch and x['scene'] == scene and x['moon'] == moon]:
                j, p, c, _ = gates(r, ref)
                ok = all(g is not False for g in (j, p, c)) and (j is None or j) and (p is None or p) and c
                if ok and best is None:
                    best = r['kpo'] * COST[sch]
            line += f"{(str(best) if best else 'FAIL'):>13s}"
        print(line)

print("\nJ-only gate (what the Jacobi behaviour alone would allow):")
for scene in ['s1', 's2']:
    moons = sorted({r['moon'] for r in rows if r['scene'] == scene})
    for sch in ['dkd', 'y4']:
        line = f"{scene} {sch:4s}"
        for moon in moons:
            ref = refs[(scene, moon)]
            best = None
            for r in [x for x in rows if x['scheme'] == sch and x['scene'] == scene and x['moon'] == moon]:
                j, p, c, _ = gates(r, ref)
                jj = j if j is not None else True
                if jj and c and best is None:
                    best = r['kpo'] * COST[sch]
            line += f" {moon[:9]}:{best if best else 'FAIL'}"
        print(line)
