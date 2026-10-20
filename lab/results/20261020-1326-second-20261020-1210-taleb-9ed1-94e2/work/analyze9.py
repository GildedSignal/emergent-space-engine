#!/usr/bin/env python3
"""Per-arm decomposition for the stagger-scaling run (20261020-1210-taleb-9ed1).

Reads an escsv trace (8365's instrument): columns f, ms, ev, k, gs, lag, held, rss,
op, bo, sl, it (5 classes), cn (5 classes, ms), en. Prints: worst frames, per-era
kicks/boundaries/wall/us-per-kick, hottest 1k-gs bin share of kick arrivals per
kick era, end lag, peak rss. Off = shipped behaviour for the engine; this file only
reads CSVs.
"""
import sys

def load(name):
    rows = []
    for line in open(name):
        if not line.startswith("escsv"):
            continue
        d = {}
        for tok in line.split()[1:]:
            if "=" in tok:
                kk, v = tok.split("=", 1)
                d[kk] = v
        rows.append({
            "f": int(d["f"]), "ms": float(d["ms"]), "ev": int(d["ev"]), "k": int(d["k"]),
            "bo": int(d["bo"]), "gs": float(d["gs"]), "lag": float(d["lag"]),
            "held": int(d["held"]), "rss": float(d["rss"]),
            "it": [int(x) for x in d["it"].split(",")],
            "cn": [float(x) for x in d["cn"].split(",")],
            "en": int(d["en"]),
        })
    return rows

# kick-comb eras in game-s (period 27.9k, onset ~13.9k); boundary eras sit between.
KICK_ERAS = [(12000, 16000), (40000, 44000), (68000, 72000), (96000, 100000)]
ALL_ERAS = [(12000, 16000), (26000, 30000), (40000, 44000), (54000, 58000),
            (68000, 72000), (82000, 86000), (96000, 100000), (110000, 114000)]

def main(name, label):
    rows = load(name)
    n_frames = len(rows)
    total_k = sum(r["k"] for r in rows)
    worst = sorted(rows, key=lambda r: -r["ms"])[:5]
    print(f"== {label} ({name}): {n_frames} frames, kicks {total_k}")
    print("   worst frames:", ", ".join(f"(f{r['f']} {r['ms']:.0f}ms ev{r['ev']} k{r['k']} gs{r['gs']:.0f})" for r in worst))
    for lo, hi in ALL_ERAS:
        sel = [r for r in rows if lo <= r["gs"] < hi]
        if not sel:
            continue
        k = sum(r["k"] for r in sel); bo = sum(r["bo"] for r in sel)
        w = sum(r["ms"] for r in sel)
        # sequential µs per kick: era wall over era kicks (kicks dominate kick eras)
        uk = w * 1e3 / k if k else 0.0
        print(f"   era [{lo//1000},{hi//1000})k gs: kicks {k:>7} bnd {bo:>7} wall {w/1e3:6.1f}s  {uk:6.1f} us/kick  maxf {max(r['ms'] for r in sel):7.1f}ms")
    # hottest 1k-gs bin share of KICK arrivals, per kick era
    for lo, hi in KICK_ERAS:
        sel = [r for r in rows if lo <= r["gs"] < hi]
        if not sel:
            continue
        bins = {}
        for r in sel:
            b = int(r["gs"] // 1000)
            bins[b] = bins.get(b, 0) + r["k"]
        tot = sum(bins.values())
        if tot == 0:
            continue
        hot = max(bins.items(), key=lambda kv: kv[1])
        print(f"   kick era [{lo//1000},{hi//1000})k: arrivals {tot}, hottest 1k-gs bin {hot[0]*1000}-{hot[0]*1000+1000}: {hot[1]} ({100.0*hot[1]/tot:.0f}% of era kicks)")
    end = rows[-1]
    print(f"   end lag {end['lag']:.1f}s, peak rss {max(r['rss'] for r in rows):.0f} MB, held_max {max(r['held'] for r in rows)}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
