#!/usr/bin/env python3
"""Era analysis with per-class decomposition: where does the freeze-era wall go?
Reads escsv lines (f, ms, ev, k, gs, lag, held, rss, op, bo, sl, it[5], cn[5], en),
bins by presented game-s, finds the combs, and decomposes each era's wall into
player-class (cn[3], the nested-pull path), ship-wave class (cn[2]), and the rest."""
import sys

def load(path):
    rows = []
    for line in open(path):
        if not line.startswith("escsv"):
            continue
        d = dict(kv.split("=", 1) for kv in line.split()[1:])
        it = [int(v) for v in d["it"].split(",")]
        cn = [float(v) for v in d["cn"].split(",")]
        rows.append(dict(f=int(d["f"]), ms=float(d["ms"]), ev=int(d["ev"]), k=int(d["k"]),
                         gs=float(d["gs"]), lag=float(d["lag"]), held=int(d["held"]),
                         rss=float(d["rss"]), op=int(d["op"]), bo=int(d["bo"]), sl=int(d["sl"]),
                         it=it, cn=cn, en=int(d["en"])))
    return rows

def analyze(path, bodies, label):
    rows = load(path)
    print(f"== {label}: {len(rows)} frames, gs {rows[0]['gs']:.0f}..{rows[-1]['gs']:.0f}")
    bins = {}
    for r in rows:
        b = int(r["gs"] // 2000)
        e = bins.setdefault(b, dict(ev=0, ms=0.0, mx=0.0, n=0, k=0, it=[0]*5, cn=[0.0]*5,
                                    held=0.0, rss=0.0, over=0, lag=0.0, en=0))
        e["ev"] += r["ev"]; e["ms"] += r["ms"]; e["mx"] = max(e["mx"], r["ms"]); e["n"] += 1
        e["k"] += r["k"]; e["held"] += r["held"]; e["rss"] = max(e["rss"], r["rss"])
        e["over"] += r["ms"] > 12.0; e["lag"] = max(e["lag"], r["lag"]); e["en"] += r["en"]
        for c in range(5):
            e["it"][c] += r["it"][c]; e["cn"][c] += r["cn"][c]
    print("bin_gs   ev/body  wall_ms    max_ms  over  kicks  held~   en")
    for b in sorted(bins):
        e = bins[b]
        print(f"{b*2:>5}k  {e['ev']/bodies:8.3f}  {e['ms']:8.0f}  {e['mx']:8.1f}  {e['over']:4d}  {e['k']:6d}  {e['held']/max(e['n'],1):6.0f}  {e['en']:4d}")
    mark = [b for b in sorted(bins) if bins[b]["ev"] / bodies >= 0.15]
    eras = []
    for b in mark:
        if eras and b == eras[-1][-1] + 1:
            eras[-1].append(b)
        else:
            eras.append([b])
    tot_ev = sum(bins[b]["ev"] for b in bins)
    print(f"\neras: {len(eras)}; total events {tot_ev} ({tot_ev/bodies:.3f}/body)")
    hdr = ("era", "gs", "ev/body", "wall_s", "max_ms", "over", "kicks", "it2", "it3",
           "cn2_s", "cn3_s", "rest_s", "nest%", "us/ev", "us/it2", "us/kick", "held~", "rss")
    print(("{:>3} {:>11} {:>7} {:>6} {:>7} {:>4} {:>7} {:>6} {:>5} {:>6} {:>6} {:>6} {:>5} {:>6} {:>6} {:>7} {:>6} {:>5}").format(*hdr))
    era_rows = []
    for i, era in enumerate(eras):
        g0, g1 = era[0]*2000, (era[-1]+1)*2000
        ev = sum(bins[b]["ev"] for b in era); k = sum(bins[b]["k"] for b in era)
        mx = max(bins[b]["mx"] for b in era); ov = sum(bins[b]["over"] for b in era)
        w = sum(bins[b]["ms"] for b in era) / 1e3
        it = [sum(bins[b]["it"][c] for b in era) for c in range(5)]
        cn = [sum(bins[b]["cn"][c] for b in era) / 1e3 for c in range(5)]
        held = sum(bins[b]["held"] for b in era) / max(sum(bins[b]["n"] for b in era), 1)
        rss = max(bins[b]["rss"] for b in era)
        rest = w - sum(cn)
        nest = 100.0 * (k - it[2]) / max(k, 1)
        row = dict(i=i+1, g0=g0, g1=g1, ev=ev, k=k, w=w, mx=mx, ov=ov, it=it, cn=cn,
                   rest=rest, held=held, rss=rss)
        era_rows.append(row)
        print(f"{i+1:>3} {g0/1000:>4.0f}-{g1/1000:<4.0f}k {ev/bodies:7.3f} {w:6.1f} {mx:7.1f} {ov:4d} {k:7d} {it[2]:6d} {it[3]:5d} "
              f"{cn[2]:6.2f} {cn[3]:6.2f} {rest:6.2f} {nest:5.1f} {w*1e3/max(ev,1):6.1f} {cn[2]*1e3/max(it[2],1):6.1f} {sum(cn)*1e3/max(k,1):7.2f} {held:6.0f} {rss:5.0f}")
    # comb concentration: events in the 4 hottest 2k bins vs all
    hot = sorted(bins, key=lambda b: -bins[b]["ev"])[:4]
    conc = sum(bins[b]["ev"] for b in hot) / max(tot_ev, 1)
    hotw = sum(bins[b]["ms"] for b in hot) / 1e3
    print(f"crest concentration: 4 hottest bins ({','.join(f'{b*2}k' for b in sorted(hot))}) hold {conc*100:.0f}% of events, wall {hotw:.1f} s")
    worst = sorted(rows, key=lambda r: -r["ms"])[:6]
    print("worst frames:", " ".join(f"(f{r['f']},gs{r['gs']:.0f},{r['ms']:.0f}ms,ev{r['ev']},k{r['k']},it2={r['it'][2]},cn3={r['cn'][3]:.0f})" for r in worst))
    print(f"held max {max(r['held'] for r in rows)}, rss max {max(r['rss'] for r in rows):.0f} MB, max lag {max(r['lag'] for r in rows):.1f} s\n")
    return bins, eras, era_rows

if __name__ == "__main__":
    analyze(sys.argv[1], int(sys.argv[2]), sys.argv[3])
