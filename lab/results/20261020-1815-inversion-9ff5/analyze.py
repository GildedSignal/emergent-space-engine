#!/usr/bin/env python3
"""Era anatomy of a longflight CSV: per belt-comb arrivals, mint bill, cost, held, counters."""
import csv, sys

def load(path):
    rows = []
    with open(path) as f:
        for r in csv.DictReader(f):
            rows.append({k: float(v) for k, v in r.items()})
    return rows

def combs(rows, bodies, period=27900.0, half=13950.0, w=3500.0):
    """Kick combs sit at half+k*period (measured: 14k, 42k, 70k...), boundary combs at k*period."""
    out, k = [], 0
    while True:
        kc, bc = half + k * period, k * period
        if rows and rows[-1]["gs"] < min(kc, bc) - w and k > 0:
            break
        kw = [r for r in rows if kc - w <= r["gs"] <= kc + w]
        bw = [r for r in rows if k > 0 and bc - w <= r["gs"] <= bc + w]
        if not kw and not bw:
            k += 1
            continue
        before = [r for r in rows if r["gs"] < min(kc, bc) - w]
        after = kw or bw
        live0 = before[-1]["live_mb"] if before else after[0]["live_mb"]
        live1 = after[-1]["live_mb"]
        kev = sum(r["events"] for r in kw)
        out.append({"era": k, "gs": kc, "kicks": sum(r["kicks"] for r in kw),
                    "bounds": sum(r["boundaries"] for r in bw),
                    "arr": sum(r["kicks"] for r in kw) / bodies if kw else 0.0,
                    "barr": sum(r["boundaries"] for r in bw) / bodies if bw else 0.0,
                    "cost_us_ev": sum(r["ship_us"] for r in kw) / kev if kev else 0.0,
                    "live0": live0, "live1": live1,
                    "held_peak": max([r["held"] for r in kw + bw], default=0),
                    "worst_ms": max([r["worst_ms"] for r in kw + bw], default=0.0),
                    "bpb": kw[-1]["bpb"] if kw else 0, "cat": kw[-1]["cat_live"] if kw else 0})
        k += 1
        if k > 60:
            break
    return out

if __name__ == "__main__":
    path, bodies = sys.argv[1], int(sys.argv[2])
    rows = load(path)
    print(f"windows={len(rows)} gs_end={rows[-1]['gs']:.0f} live_end={rows[-1]['live_mb']:.1f} rss_end={rows[-1]['rss_mb']:.1f} held_end={rows[-1]['held']:.0f}")
    print("era  gs_kick   arr/b   barr/b  cost_us/ev  live0   live1   dMB   held_pk  worst_ms  bpb   cat")
    cs = combs(rows, bodies)
    for c in cs:
        print(f"{c['era']:>3} {c['gs']:>8.0f} {c['arr']:>6.3f} {c['barr']:>7.3f} {c['cost_us_ev']:>10.2f} "
              f"{c['live0']:>7.1f} {c['live1']:>7.1f} {c['live1']-c['live0']:>5.1f} {c['held_peak']:>7.0f} "
              f"{c['worst_ms']:>8.1f} {c['bpb']:>5.0f} {c['cat']:>6.0f}")
    xs = [c["era"] for c in cs if c["era"] >= 3]
    ys = [c["live1"] for c in cs if c["era"] >= 3]
    if len(xs) > 3:
        n = len(xs); mx = sum(xs)/n; my = sum(ys)/n
        sxy = sum((x-mx)*(y-my) for x, y in zip(xs, ys)); sxx = sum((x-mx)**2 for x in xs); syy = sum((y-my)**2 for y in ys)
        print(f"\nratchet fit eras>=3: {sxy/sxx:+.2f} MB/era (r={(sxy*sxy/(sxx*syy))**0.5:.3f}); last-era growth {cs[-1]['live1']-cs[-2]['live1']:+.1f} MB")
    late = [c for c in cs if c["era"] >= 20]
    if late:
        g = [late[i+1]["live1"]-late[i]["live1"] for i in range(len(late)-1)]
        print(f"late eras>=20: mean growth {sum(g)/max(1,len(g)):+.2f} MB/era, arrivals {sum(c['arr'] for c in late)/len(late):.3f}/body, cost {sum(c['cost_us_ev'] for c in late)/len(late):.1f} us/ev")
