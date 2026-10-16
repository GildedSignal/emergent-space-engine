#!/usr/bin/env python3
"""Key-displacement census for the kick (run 20261016-1459-spacex-7fd2).

Reads the bench dumps (kicks-s*.json) and answers, per population:
  1. how many bits a kick moves the compiled key's own inputs
     (p = periapsis significand, k = shape mantissa Q48): the low bits that
     change are the information the recompile must consume;
  2. the hit-rate curve of a cache keyed at g significant bits (both p and k
     must fall in the same bin) — the reuse available at each granularity;
  3. controls: g=12+12 vs the bench's measured quantized_hit_rate, full
     precision vs the measured exact_hit_rate.
Exact integer arithmetic; floats appear only for reported bit positions.
"""
import json, sys, math
from collections import defaultdict

def bits(x: int) -> int:
    return abs(x).bit_length()

def top_g(value: int, g: int) -> int:
    """Keep the top g significant bits (truncation), normalized to a power-of-two scale."""
    if value == 0:
        return 0
    b = bits(value)
    if b <= g:
        return value
    return value >> (b - g)

def analyze(path: str):
    rows = json.load(open(path))["rows"]
    per_body = defaultdict(list)
    for r in rows:
        per_body[(r["body"], r["made"])].append(r)
    out = {"seed": path.split("-s")[-1].split(".")[0], "rows": len(rows), "pops": {}}
    for made in (True, False):
        pop = "made" if made else "leavers"
        pairs = 0
        dp_bits, dk_bits, dk_lowbits = [], [], []
        knot_counts = []
        curve = {g: [0, 0] for g in (8, 12, 16, 20, 24, 28, 32, 40, 48, 62)}
        exact_p = exact_k = exact_both = 0
        for (body, m), rs in per_body.items():
            if m != made:
                continue
            rs.sort(key=lambda r: r["t"])
            for a, b in zip(rs, rs[1:]):
                pairs += 1
                knot_counts.append(b["knots"] if b["knots"] and b["knots"] > 0 else None)
                # p as exact integers: p = sig * 2^(exp-62); compare relative change.
                sa, sb = a["p_sig"], b["p_sig"]
                ea, eb = a["p_exp"], b["p_exp"]
                # align exponents
                if ea <= eb:
                    s1, s2, sh = sa << (eb - ea), sb, eb
                else:
                    s1, s2, sh = sa, sb << (ea - eb), ea
                d = s2 - s1
                dp = -1.0 if d == 0 else math.log2(abs(d) / abs(s2))
                dp_bits.append(dp)
                dp_low = 0 if d == 0 else bits(d) - bits(s2)  # negative: bits below p's msb
                ka, kb = a["k"], b["k"]
                dk = kb - ka
                dkbit = -1.0 if dk == 0 else math.log2(abs(dk) / kb)
                dk_bits.append(dkbit)
                dk_lowbits.append(bits(dk))
                exact_p += d == 0
                exact_k += dk == 0
                exact_both += (d == 0 and dk == 0)
                for g in curve:
                    same = top_g(s1, g) == top_g(s2, g) and top_g(ka, g) == top_g(kb, g)
                    curve[g][0] += same
                    curve[g][1] += 1
        def med(v):
            v = sorted(x for x in v if x is not None)
            return None if not v else v[len(v) // 2]
        kc = sorted(k for k in knot_counts if k)
        out["pops"][pop] = {
            "pairs": pairs,
            "dp_bits_median": med(dp_bits), "dp_bits_p10": None,
            "dk_bits_median": med(dk_bits),
            "dk_lowbits_median": med(dk_lowbits), "dk_lowbits_max": max(dk_lowbits) if dk_lowbits else None,
            "exact_p_repeats": exact_p, "exact_k_repeats": exact_k, "exact_both": exact_both,
            "knots_median": kc[len(kc) // 2] if kc else None, "knots_max": kc[-1] if kc else None,
            "same_bin_rate": {g: (c / n if n else None) for g, (c, n) in curve.items()},
        }
        # p10 of dp_bits
        sv = sorted(x for x in dp_bits if x != -1.0)
        if sv:
            out["pops"][pop]["dp_bits_p10"] = sv[len(sv) // 10]
    return out

if __name__ == "__main__":
    results = [analyze(p) for p in sys.argv[1:]]
    json.dump(results, open("census-summary.json", "w"), indent=1)
    for r in results:
        print(f"== seed {r['seed']}: {r['rows']} key rows")
        for pop, d in r["pops"].items():
            print(f"  {pop}: pairs={d['pairs']} exact(p,k,both)={d['exact_p_repeats']},{d['exact_k_repeats']},{d['exact_both']}")
            print(f"    dp_bits median {d['dp_bits_median']} p10 {d['dp_bits_p10']} | dk_bits median {d['dk_bits_median']} | dk low-bits moved median {d['dk_lowbits_median']} max {d['dk_lowbits_max']}")
            print(f"    knots median {d['knots_median']} max {d['knots_max']}")
            print("    same-bin:", {g: (round(v, 4) if v is not None else None) for g, v in d["same_bin_rate"].items()})
