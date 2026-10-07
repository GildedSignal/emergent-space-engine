#!/usr/bin/env python3
# Gate analysis for out_full.json. Pre-registered gate (predictions.md):
# hold iff not unbound AND epump in [0.8,1.25] AND da_rel <= 0.05 at BOTH
# horizons. Cost = tide evals per orbit = kpo(h200) * epk, epk = 3 for
# TRIG*/TRIG2G else 1 (harness accounting; engine accounting in the dossier).
import json, sys

BAND = (0.8, 1.25)
DAMAX = 0.05
EPK3 = ("TRIG", "TRIG2", "TRIG2G")
FIXEDS = ["FIXED-2", "FIXED-4", "FIXED-8", "FIXED-16", "FIXED-32", "FIXED-64"]
POL_ORDER = FIXEDS + ["AVG", "DEPH-2.5", "GOLD", "TRIG-0.25", "TRIG-0.5",
                      "TRIG2-0.125", "TRIG2-0.5", "TRIG2-2.0", "TRIG2G-2.0"]

def epk(pol):
    return 3 if pol.startswith(EPK3) else 1

def holds(row):
    if row.get("unbound"): return False
    for h in ("h100", "h200"):
        s = row[h]
        if s["epump"] != s["epump"]: return False
        if not (BAND[0] <= s["epump"] <= BAND[1]): return False
        if not (s["da_rel"] <= DAMAX): return False
    return True

def evpo(row):
    return row["h200"]["kpo"] * epk_policy[0] if False else None

def main(path="out_full.json"):
    d = json.load(open(path))
    # policy-name -> epk
    rows = []
    for key, sc in d.items():
        hors = ("h30", "h60") if key == "S1" else ("h100", "h200")
        r = dict(key=key, pq=sc["pq"], delta=sc["delta"], dPdW=sc["dPdW"],
                 order="S" if sc["pq"] in ("S1", "S3") else
                       ("1st" if sc["pq"] in ("2:1", "3:2") else "2nd"))
        pols = {}
        for p in POL_ORDER:
            if p in sc:
                pr = sc[p]
                hl = True
                if not pr.get("unbound"):
                    for h in hors:
                        s = pr[h]
                        if s["epump"] != s["epump"] or not (BAND[0] <= s["epump"] <= BAND[1]) or not (s["da_rel"] <= DAMAX):
                            hl = False; break
                else:
                    hl = False
                pols[p] = dict(hold=hl, evpo=pr[hors[1]]["kpo"] * epk(p),
                               kpo=pr[hors[1]]["kpo"], unbound=pr.get("unbound", False),
                               ep=[pr[h]["epump"] for h in hors],
                               da=[pr[h]["da_rel"] for h in hors])
        base = None
        for p in FIXEDS:
            if p in pols and pols[p]["hold"]:
                base = (p, pols[p]["evpo"]); break
        r["pols"] = pols; r["base"] = base
        rows.append(r)

    print("=== per-row: holding policies (o=hold, .=fail, U=unbound) ===")
    hdr = "%-22s %-4s %+5.2f" % ("row", "ord", 0)
    print("%-28s %-4s %7s | %-46s | %s" % ("row", "ord", "dPdW/W", "holding policies (evpo)", "baseline"))
    ncert = 0
    for r in sorted(rows, key=lambda r: (r["order"], r["pq"], r["dPdW"], r["key"])):
        hset = [p for p in POL_ORDER if p in r["pols"] and r["pols"][p]["hold"]]
        tag = "%-28s %-4s %+7.2f" % (r["key"], r["order"], r["dPdW"])
        if r["base"]: ncert += 1
        print("%s | %-46s | %s" % (tag, ",".join(hset) if hset else "NONE",
                                   f"{r['base'][0]}@{r['base'][1]:.1f}" if r["base"] else "-"))
    print(f"certifiable rows (some FIXED holds): {ncert}/{len(rows)}")

    print("\n=== aggregate cuts over certifiable rows (tide evals, h200) ===")
    cert = [r for r in rows if r["base"]]
    B = sum(r["base"][1] for r in cert)
    print(f"baseline total evals/orbit: {B:.1f} over {len(cert)} rows")
    for p in POL_ORDER:
        if any(p in r["pols"] for r in cert):
            tot = 0.0; fails = 0
            for r in cert:
                if p in r["pols"] and r["pols"][p]["hold"]:
                    tot += r["pols"][p]["evpo"]
                else:
                    fails += 1
            if fails == 0:
                print("  %-12s holds everywhere: total %7.1f  cut %5.2fx" % (p, tot, B / tot if tot else float("inf")))
            else:
                print("  %-12s FAILS on %d/%d certifiable rows" % (p, fails, len(cert)))

    print("\n=== frequency-derived rule R1 (pre-registered) ===")
    # R1: |dPdW/W| <= 1 AND first order -> doll (no cut claimable; counted at
    # FIXED-64 cost both sides); else TRIG2-0.5.
    tot = 0.0; uncert = 0; fails = 0
    for r in rows:
        if r["order"] == "1st" and abs(r["dPdW"]) <= 1.0:
            uncert += 1
            tot += 66.0 if "FIXED-64" in r["pols"] else 66.0   # dense fallback both sides
            continue
        if "TRIG2-0.5" in r["pols"] and r["pols"]["TRIG2-0.5"]["hold"]:
            tot += r["pols"]["TRIG2-0.5"]["evpo"]
        else:
            fails += 1
    Ball = sum((r["base"][1] if r["base"] else 66.0) for r in rows)
    print(f"rows total {len(rows)}, first-order near-resonant (doll) {uncert}, "
          f"R1 failures elsewhere {fails}; R1 cost {tot:.0f} vs all-rows baseline {Ball:.0f} "
          f"-> cut {Ball/tot if tot else 0:.2f}x (capped at 1.0 on doll rows by construction)")

    print("\n=== epump/da detail at centres (phase 0) ===")
    for r in rows:
        if r["delta"] == 0.0 and r["key"].endswith("p0"):
            t = d[r["key"]]["truth"]
            print(f"{r['key']}: truth e {t['100']['e']:.4f}->{t['200']['e']:.4f} a {t['100']['a']:.4f}->{t['200']['a']:.4f}")
            for p in POL_ORDER:
                if p in r["pols"]:
                    q = r["pols"][p]
                    print("   %-12s epump %6.2f->%6.2f  da %6.4f->%6.4f  kpo %5.1f  %s" %
                          (p, q["ep"][0], q["ep"][1], q["da"][0], q["da"][1], q["kpo"],
                           "HOLD" if q["hold"] else ("UNB" if q["unbound"] else "")))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "out_full.json")
