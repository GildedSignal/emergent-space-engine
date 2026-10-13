#!/usr/bin/env python3
"""lab run 20261013-2005-quant-7055: analyze the probe matrix (A base, B keys, C memo)."""
import json, sys, glob, os, csv
from collections import Counter

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
scenes = sorted({os.path.basename(p).rsplit("_", 1)[0] for p in glob.glob(f"{OUT}/*_A.json")})

def prof(name):
    r = json.load(open(f"{OUT}/{name}.json"))
    st = {s["stage"]: s for s in r["prof_main_thread"] if s["calls"]}
    return r, st

print(f"{'scene':<12} {'leavers':>7} {'ho_comp':>8} {'ho_dist':>8} {'ho_hits':>8} {'hit%':>6} {'all_comp':>8} {'all_hits':>9} {'bindA_us':>9} {'bindC_us':>9} {'hoA_us':>8} {'hoC_us':>8} {'dgAB':>5} {'dgAC':>5}")
for sc in scenes:
    A, pa = prof(f"{sc}_A")
    B, pb = prof(f"{sc}_B")
    C, pc = prof(f"{sc}_C")
    pp = B["promo_probe"]
    ho = pp["handout_compiles"]; hod = pp["handout_distinct"]; hoh = pp["handout_exact_hits"]
    hit = 100.0 * hoh / ho if ho else 0.0
    bindA = pa.get("  hand-out: bind (the member as a tube)", {}).get("us_per_call", 0)
    bindC = pc.get("  hand-out: bind (the member as a tube)", {}).get("us_per_call", 0)
    hoA = pa.get("hand-out (a member made a body)", {}).get("us_per_call", 0)
    hoC = pc.get("hand-out (a member made a body)", {}).get("us_per_call", 0)
    dgAB = A["digest"] == B["digest"]
    dgAC = A["digest"] == C["digest"]
    print(f"{sc:<12} {A['stats'].split('leavers: ')[1].split(',')[0]:>7} {ho:>8} {hod:>8} {hoh:>8} {hit:>5.1f}% {pp['compiles']:>8} {(pp["compiles"] - pp["distinct_keys"]):>9} {bindA:>9.1f} {bindC:>9.1f} {hoA:>8.1f} {hoC:>8.1f} {str(dgAB):>5} {str(dgAC):>5}")

# Key-distance structure from the biggest scene's CSV: how near are hand-out keys to each other?
for f in sorted(glob.glob(f"{OUT}/*_keys.csv"), key=os.path.getsize, reverse=True)[:2]:
    # the key's Debug contains commas: split on the first three only
    rows = []
    for line in open(f).read().splitlines()[1:]:
        site, periodic, hit, key = line.split(",", 3)
        rows.append({"site": site, "periodic": periodic, "hit": hit, "key": key})
    ho = [r for r in rows if r["site"] == "1"]
    if len(ho) < 10:
        continue
    def parse(k):
        # OrbitKey { periapsis: Scalar { significand: X, exponent: Y }, k: Z, ... }
        import re
        sig = int(re.search(r"significand: (-?\d+)", k).group(1))
        e = int(re.search(r"exponent: (-?\d+)", k).group(1))
        kk = int(re.search(r"k: (\d+)", k).group(1))
        return sig, e, kk
    vals = [parse(r["key"]) for r in ho]
    # relative spread of periapsis significand (same exponent) and k
    print(f"\n{os.path.basename(f)}: {len(ho)} hand-out keys")
    exps = Counter(v[1] for v in vals)
    print("  periapsis exponents:", dict(exps))
    same = [v for v in vals if v[1] == exps.most_common(1)[0][0]]
    sigs = sorted(v[0] for v in same)
    rel = (sigs[-1] - sigs[0]) / abs(sigs[len(sigs) // 2]) if len(sigs) > 1 else 0
    print(f"  periapsis significand spread (modal exponent): {rel:.3e} relative; distinct {len(set(sigs))}/{len(sigs)}")
    ks = Counter(v[2] for v in vals)
    print(f"  k: {len(ks)} distinct of {len(vals)}; top-3 shared by {[c for _, c in ks.most_common(3)]} members")
