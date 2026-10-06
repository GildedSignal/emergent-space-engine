#!/usr/bin/env python3
"""Picture: events per body per orbit against the horizon (log-log), one series per
configuration, with the truth's encounter rate as a line. Data from steady.jsonl."""
import json, math, os

R = os.path.dirname(os.path.abspath(__file__))
import re
_raw = [l.strip() for l in open(os.path.join(R, "steady.jsonl")) if l.strip()]
truth_rate = [float(re.search(r'truth_rate":([\d.e+-]+)', l).group(1)) for l in _raw if "truth_rate" in l][0]
st = [json.loads(l) for l in _raw if "truth_rate" not in l]

series = {"diophantine": [], "element-sort": [], "conjunction-sampled": [], "oracle": []}
for l in st:
    if l.get("steady") in series and "rate" in l:
        h = l.get("horizon", 1e5 if l["steady"] != "diophantine" else None)
        if h is None:
            continue
        series[l["steady"]].append((float(h), float(l["rate"])))
# non-dio configurations have horizon-independent rates: draw them at the sweep's ends
for k in ("element-sort", "conjunction-sampled", "oracle"):
    if series[k]:
        r = series[k][0][1]
        series[k] = [(10.0, r), (1e5, r)]
for k in series:
    series[k].sort()

W, H = 900, 560
ml, mr, mt, mb = 70, 230, 45, 60
pw, ph = W - ml - mr, H - mt - mb

xmin, xmax = 1.0, 2.0e5     # horizon in orbits
ymin, ymax = 1e-3, 2.0e3    # events per body per orbit


def X(x):
    return ml + pw * (math.log10(x) - math.log10(xmin)) / (math.log10(xmax) - math.log10(xmin))


def Y(y):
    return mt + ph * (1 - (math.log10(y) - math.log10(ymin)) / (math.log10(ymax) - math.log10(ymin)))


def sx(v, base):
    return f"{v / base:.0f}"


out = []
out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="Helvetica,Arial,sans-serif" font-size="13">')
out.append(f'<rect width="{W}" height="{H}" fill="#faf9f6"/>')
# grid + axes (major decades)
for d in range(-3, 4):
    y = 10.0 ** d
    if y < ymin / 1.001 or y > ymax * 1.001:
        continue
    yy = Y(y)
    out.append(f'<line x1="{ml}" y1="{yy:.1f}" x2="{ml + pw}" y2="{yy:.1f}" stroke="#d8d4c8" stroke-width="1"/>')
    out.append(f'<text x="{ml - 8}" y="{yy + 4:.1f}" text-anchor="end" fill="#6b6659">1e{d}</text>')
for d in range(0, 6):
    x = 10.0 ** d
    if x < xmin / 1.001 or x > xmax * 1.001:
        continue
    xx = X(x)
    out.append(f'<line x1="{xx:.1f}" y1="{mt}" x2="{xx:.1f}" y2="{mt + ph}" stroke="#e4e0d4" stroke-width="1"/>')
    out.append(f'<text x="{xx:.1f}" y="{mt + ph + 18}" text-anchor="middle" fill="#6b6659">1e{d}</text>')
out.append(f'<rect x="{ml}" y="{mt}" width="{pw}" height="{ph}" fill="none" stroke="#3c3830" stroke-width="1.2"/>')
out.append(f'<text x="{ml + pw / 2}" y="{H - 16}" text-anchor="middle" fill="#3c3830">horizon (orbits)</text>')
out.append(f'<text x="20" y="{mt + ph / 2}" text-anchor="middle" fill="#3c3830" transform="rotate(-90 20 {mt + ph / 2})">events per body per orbit</text>')

# truth line
yy = Y(truth_rate)
out.append(f'<line x1="{ml}" y1="{yy:.1f}" x2="{ml + pw}" y2="{yy:.1f}" stroke="#8a3324" stroke-width="1.8" stroke-dasharray="7 4"/>')
out.append(f'<text x="{ml + 8}" y="{yy - 6:.1f}" fill="#8a3324">truth encounter rate {truth_rate:.2e}</text>')

style = {
    "diophantine": ("#1f4e79", "o"),
    "element-sort": ("#7a6c4f", "s"),
    "conjunction-sampled": ("#556b2f", "^"),
    "oracle": ("#8a3324", "D"),
}
for name, (color, marker) in style.items():
    pts = series[name]
    if not pts:
        continue
    path = " ".join(f"{X(x):.1f},{Y(y):.1f}" for x, y in pts)
    out.append(f'<polyline points="{path}" fill="none" stroke="{color}" stroke-width="1.8"/>')
    for x, y in pts:
        cx, cy = X(x), Y(y)
        if marker == "o":
            out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="{color}"/>')
        elif marker == "s":
            out.append(f'<rect x="{cx - 3.5:.1f}" y="{cy - 3.5:.1f}" width="7" height="7" fill="{color}"/>')
        elif marker == "^":
            out.append(f'<path d="M {cx:.1f} {cy - 4:.1f} L {cx + 4:.1f} {cy + 3:.1f} L {cx - 4:.1f} {cy + 3:.1f} Z" fill="{color}"/>')
        else:
            out.append(f'<path d="M {cx - 4:.1f} {cy:.1f} L {cx:.1f} {cy - 4:.1f} L {cx + 4:.1f} {cy:.1f} L {cx:.1f} {cy + 4:.1f} Z" fill="{color}"/>')

# legend
lx = ml + pw + 18
labels = {
    "diophantine": "diophantine (Binet cone + first hit)",
    "element-sort": "element-sort (r8 v2)",
    "conjunction-sampled": "conjunction-sampled (r8 v2 ref)",
    "oracle": "oracle",
}
for i, (name, lab) in enumerate(labels.items()):
    color, marker = style[name]
    yy = mt + 20 + i * 44
    out.append(f'<line x1="{lx}" y1="{yy}" x2="{lx + 26}" y2="{yy}" stroke="{color}" stroke-width="2"/>')
    words = lab.split()
    for j in range(0, len(words), 2):
        out.append(f'<text x="{lx + 32}" y="{yy - 8 + j * 12 + 4}" fill="#3c3830" font-size="12">{" ".join(words[j:j + 2])}</text>')
out.append("</svg>")
open(os.path.join(R, "picture.svg"), "w").write("\n".join(out))
print("wrote picture.svg;", {k: len(v) for k, v in series.items()})
