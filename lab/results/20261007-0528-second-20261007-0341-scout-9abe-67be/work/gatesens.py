#!/usr/bin/env python3
# Gate-sensitivity: does the verdict (first-order uncertifiable; oracle eval
# cut << 4x) depend on the pre-registered gate? Run: python3 gatesens.py
import json
from collections import Counter
import analyze as A

d = json.load(open("out_full.json"))

def gate_rows(demax=0.05, use_abs_e=None):
    rows = []
    for key, sc in d.items():
        hors = ("h30", "h60") if key == "S1" else ("h100", "h200")
        def holds(p):
            pr = sc.get(p)
            if not pr or pr.get("unbound"): return False
            for h in hors:
                s = pr[h]; t_e = sc["truth"][h[1:]]["e"]
                if s["epump"] != s["epump"]: return False
                okp = (abs(s["e"]-t_e) <= use_abs_e) if use_abs_e else (0.8 <= s["epump"] <= 1.25)
                if not okp or not (s["da_rel"] <= demax): return False
            return True
        hf = [(p, sc[p][hors[1]]["kpo"]) for p in A.FIXEDS if holds(p)]
        ha = [(p, sc[p][hors[1]]["kpo"]*A.epk(p)) for p in A.POL_ORDER if holds(p)]
        if hf:
            rows.append((key, min(hf, key=lambda x: x[1])[1],
                         min(ha, key=lambda x: x[1])[1] if ha else None,
                         min(ha, key=lambda x: x[1])[0] if ha else None))
    return rows

if __name__ == "__main__":
    for name, kw in [("pre-registered (epump band, da<=0.05)", {}),
                     ("absolute e (de<=0.01, da<=0.05)", dict(use_abs_e=0.01)),
                     ("loose (de<=0.02, da<=0.10)", dict(use_abs_e=0.02, demax=0.10))]:
        rows = gate_rows(**kw)
        B = sum(r[1] for r in rows); O = sum(r[2] if r[2] else r[1] for r in rows)
        fo = sum(1 for k in d if d[k]["pq"] in ("2:1", "3:2"))
        heldfo = sum(1 for r in rows if r[0].startswith(("21_", "32_")))
        print("%-42s certifiable %2d/62 (1st-order held: %d/%d)  oracle eval cut %.2fx  winners %s" %
              (name, len(rows), heldfo, fo, B/O, Counter(r[3] for r in rows if r[3]).most_common(3)))
