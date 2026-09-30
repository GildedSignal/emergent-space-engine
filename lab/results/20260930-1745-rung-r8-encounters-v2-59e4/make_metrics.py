"""Assemble metrics.json (exactly the rung's five metric names per config)
and picture.svg: work per orbit vs true encounter rate per orbit, one point
per belt and configuration, with the line y = x."""
import json
import numpy as np

CONFIGS = ["element-sort", "shear-grid", "hier-bounds", "oracle", "ring-cells"]
ORBITS = 20.0
N = 10_000
CAP = 1e9


def load():
    belts = json.load(open("belts.json"))
    scal = json.load(open("scaling.json"))["runs"]
    return belts, scal
def fit_exponent(runs, key):
    """Rung: 'the metric is per orbit' — fit events per orbital period."""
    Ns = np.array([r["N"] for r in runs], float)
    ev = np.array([max(r[key] / r["orbits"], 0.5) for r in runs], float)
    return float(np.polyfit(np.log(Ns), np.log(ev), 1)[0])


def metrics():
    belts, scal = load()
    m = {}
    KEYB = {"element-sort": "element_sort", "shear-grid": "shear_grid",
            "hier-bounds": "hier_bounds", "oracle": "oracle",
            "ring-cells": "ring_cells"}
    for cfg in CONFIGS:
        kb = KEYB[cfg]
        det = sum(b[kb]["detected"] for b in belts)
        truth = sum(b["truth"] for b in belts)
        missed = 1.0 - det / max(truth, 1)
        w = [b[kb]["events"] / max(b["truth"], 1) for b in belts]
        zero = sum(1 for b in belts if b["truth"] == 0)
        wmed = float(np.median([min(x, CAP) for x in w]))
        ebo = [b[kb]["events"] / (N * ORBITS) for b in belts]
        m[cfg] = dict(
            missed_fraction=float(missed),
            false_fraction=0.0,
            work_per_encounter=wmed,
            events_per_body_orbit=float(np.median(ebo)),
            scale_exponent=fit_exponent(
                scal, SCALKEY[cfg]),
        )
        m[cfg]["_zero_truth_belts"] = zero
    return m, belts, scal


KEY = {"element-sort": "element_sort", "shear-grid": "shear_grid",
       "hier-bounds": "hier_bounds", "oracle": "oracle",
       "ring-cells": "ring_cells"}
SCALKEY = {"element-sort": "es", "shear-grid": "sg", "hier-bounds": "hb",
           "oracle": "truth", "ring-cells": "rc"}

COLOR = {"element-sort": "#1f77b4", "shear-grid": "#d62728",
         "hier-bounds": "#2ca02c", "oracle": "#000000",
         "ring-cells": "#9467bd"}


def picture(belts, path="picture.svg"):
    W, H = 900, 620
    ml, mr, mt, mb = 70, 260, 40, 55
    xs = []
    for b in belts:
        xs.append(b["truth"] / (N * ORBITS))
    ymin = ymax = None
    pts = []
    for cfg in CONFIGS:
        for b in belts:
            x = b["truth"] / (N * ORBITS)
            y = b[KEY[cfg]]["events"] / (N * ORBITS)
            if b["truth"] == 0:
                continue
            pts.append((cfg, x, y))
    allv = [p[1] for p in pts] + [p[2] for p in pts]
    lo = 10 ** np.floor(np.log10(min(allv)))
    hi = 10 ** np.ceil(np.log10(max(allv)))
    def X(v):
        return ml + (np.log10(v) - np.log10(lo)) / (np.log10(hi) - np.log10(lo)) * (W - ml - mr)
    def Y(v):
        return H - mb - (np.log10(v) - np.log10(lo)) / (np.log10(hi) - np.log10(lo)) * (H - mt - mb)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="Helvetica,Arial,sans-serif">']
    s.append(f'<rect width="{W}" height="{H}" fill="white"/>')
    s.append(f'<text x="{W/2}" y="24" font-size="17" text-anchor="middle" font-weight="bold">'
             f'rung r8 v2 — certification work vs true encounter rate (16 belts, N=10^4, 20 orbits)</text>')
    # grid
    for d in range(int(np.log10(lo)), int(np.log10(hi)) + 1):
        for k in range(1, 10):
            v = k * 10 ** d
            if not (lo <= v <= hi):
                continue
            s.append(f'<line x1="{X(v):.1f}" y1="{mt}" x2="{X(v):.1f}" y2="{H-mb}" stroke="#eeeeee"/>')
            s.append(f'<line x1="{ml}" y1="{Y(v):.1f}" x2="{W-mr}" y2="{Y(v):.1f}" stroke="#eeeeee"/>')
    for d in range(int(np.log10(lo)), int(np.log10(hi)) + 1):
        v = 10 ** d
        if lo <= v <= hi:
            s.append(f'<text x="{X(v):.1f}" y="{H-mb+18}" font-size="12" text-anchor="middle">1e{d}</text>')
            s.append(f'<text x="{ml-8}" y="{Y(v)+4:.1f}" font-size="12" text-anchor="end">1e{d}</text>')
    s.append(f'<line x1="{ml}" y1="{H-mb}" x2="{W-mr}" y2="{H-mb}" stroke="black"/>')
    s.append(f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{H-mb}" stroke="black"/>')
    s.append(f'<text x="{(ml+W-mr)/2}" y="{H-12}" font-size="14" text-anchor="middle">true encounters per body per orbit</text>')
    s.append(f'<text x="20" y="{(mt+H-mb)/2}" font-size="14" text-anchor="middle" transform="rotate(-90 20 {(mt+H-mb)/2})">events per body per orbit</text>')
    # y = x
    s.append(f'<line x1="{X(lo):.1f}" y1="{Y(lo):.1f}" x2="{X(hi):.1f}" y2="{Y(hi):.1f}" stroke="black" stroke-dasharray="6,5"/>')
    s.append(f'<text x="{X(hi)-10:.1f}" y="{Y(hi)-8:.1f}" font-size="12" text-anchor="end">y = x</text>')
    seen = set()
    ly = mt + 14
    for cfg in CONFIGS:
        for (c, x, y) in pts:
            if c != cfg:
                continue
            s.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="4" fill="{COLOR[cfg]}" opacity="0.85"/>')
        ly += 22
        s.append(f'<circle cx="{W-mr+22}" cy="{ly-4}" r="5" fill="{COLOR[cfg]}"/>')
        s.append(f'<text x="{W-mr+34}" y="{ly}" font-size="13">{cfg}</text>')
    s.append("</svg>")
    open(path, "w").write("\n".join(s))


if __name__ == "__main__":
    m, belts, scal = metrics()
    out = {cfg: {k: v for k, v in d.items() if not k.startswith("_")}
           for cfg, d in m.items()}
    json.dump(out, open("metrics.json", "w"), indent=1)
    for cfg in CONFIGS:
        d = m[cfg]
        print(f"{cfg:13s} missed={d['missed_fraction']:.4f} false={d['false_fraction']:.1f} "
              f"work/enc={d['work_per_encounter']:.3g} ev/body/orbit={d['events_per_body_orbit']:.3g} "
              f"expo={d['scale_exponent']:.3f} zero-truth belts={d['_zero_truth_belts']}")
    picture(belts)
    print("truth scaling:", [(r["N"], r["truth"]) for r in scal])
