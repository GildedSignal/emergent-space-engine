#!/usr/bin/env python3
"""Merge per-config metrics into metrics.json (exactly the rung's metric names) and build picture.svg."""
import json, math, os

RUN = os.path.dirname(os.path.abspath(__file__))
CONFIGS = ["binet-m8", "binet-m16", "binet-m32", "river-m16", "river-m32", "square", "tiltonly"]
METRICS = ["precession_pass_fraction", "prograde_fraction", "period_pass_fraction",
           "deflection_pass_fraction", "capture_misclassified", "isco_correct",
           "shape_kept_fraction", "cycle_repeat_fraction", "crossings_per_cycle"]

merged = {}
for c in CONFIGS:
    with open(os.path.join(RUN, f"metrics-{c}.json")) as f:
        d = json.load(f)
    merged[c] = {k: d[k] for k in METRICS}
with open(os.path.join(RUN, "..", "metrics.json"), "w") as f:
    json.dump(merged, f, indent=1)

# ---------------- picture: 7 orbit panels + 1 light panel ----------------
W, H = 1600, 900
cols, rows = 4, 2
cw, ch = W / cols, H / rows
colors = ["#d4a017", "#3a7d44", "#2e5d8a", "#8a2e5d", "#5d3a8a", "#8a5d2e", "#444444"]
lightc = ["#b22222", "#d4a017", "#3a7d44", "#2e5d8a", "#8a2e5d"]

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       f'<rect width="{W}" height="{H}" fill="#101418"/>',
       '<style text="style">.t{font-family:Georgia,serif;fill:#c8b98a}.s{font:11px monospace;fill:#8a9199}</style>']

def panel(i, title):
    px, py = (i % cols) * cw, (i // cols) * ch
    svg.append(f'<g transform="translate({px},{py})">')
    svg.append(f'<rect x="1" y="1" width="{cw-2}" height="{ch-2}" fill="#141a20" stroke="#2a323c"/>')
    svg.append(f'<text x="10" y="20" class="t" font-size="15">{esc(title)}</text>')
    return px, py

def poly(pts, col, ox, oy, sc, dash=None):
    if not pts:
        return
    d = " ".join(f"{ox + x*sc:.1f},{oy + y*sc:.1f}" for x, y in pts[::1])
    svg.append(f'<polyline points="{d}" fill="none" stroke="{col}" stroke-width="0.8"'
               + (f' stroke-dasharray="{dash}"' if dash else "") + "/>")

def circles(rs, col, ox, oy, sc):
    for r in rs:
        svg.append(f'<circle cx="{ox}" cy="{oy}" r="{r*sc:.1f}" fill="none" stroke="{col}" stroke-width="0.4"/>')

for ci, c in enumerate(CONFIGS):
    px, py = panel(ci, c)
    with open(os.path.join(RUN, f"trace-{c}.json")) as f:
        tr = json.load(f)
    pts = tr["orbit"]
    sc = min((cw - 40) / (2 * 42.0), (ch - 60) / (2 * 42.0))
    ox, oy = px + cw / 2, py + ch / 2 + 8
    circles([2, 13.333, 26.67, 40], "#232c36", ox, oy, sc)
    svg.append(f'<circle cx="{ox}" cy="{oy}" r="3" fill="#c8b98a"/>')
    poly(pts, colors[ci], ox, oy, sc)
    with open(os.path.join(RUN, f"metrics-{c}.json")) as f:
        mm = json.load(f)
    svg.append(f'<text x="10" y="{ch-28}" class="s">prec {mm["precession_pass_fraction"]:.3f}'
               f'  per {mm["period_pass_fraction"]:.3f}  defl {mm["deflection_pass_fraction"]:.3f}'
               f'  cap {mm["capture_misclassified"]}  isco {mm["isco_correct"]}</text>')
    svg.append(f'<text x="10" y="{ch-12}" class="s">shape {mm["shape_kept_fraction"]:.3f}'
               f'  repeat {mm["cycle_repeat_fraction"]:.3f}  cross/cyc {mm["crossings_per_cycle"]:.0f}</text>')
    svg.append("</g>")

# light panel: five paths from binet-m32 and river-m32 overlaid
px, py = panel(7, "light: b = 10, 30, 100, 300, 1000 (solid binet-m32, dashed river-m32)")
with open(os.path.join(RUN, "trace-binet-m32.json")) as f:
    trb = json.load(f)
with open(os.path.join(RUN, "trace-river-m32.json")) as f:
    trr = json.load(f)
sc = (cw - 60) / 2200.0
ox, oy = px + cw / 2, py + ch / 2 + 10
svg.append(f'<circle cx="{ox}" cy="{oy}" r="3" fill="#c8b98a"/>')
for i, lp in enumerate(trb["light"]):
    pts = [(x + 1100, y) for x, y in lp["pts"]]
    poly(pts, lightc[i], ox - (cw - 60) / 2 + 30, oy, sc)
for i, lp in enumerate(trr["light"]):
    pts = [(x + 1100, y) for x, y in lp["pts"]]
    poly(pts, lightc[i], ox - (cw - 60) / 2 + 30, oy, sc, dash="3,3")
for i, b in enumerate([10, 30, 100, 300, 1000]):
    svg.append(f'<text x="{10 + i*90}" y="{ch-12}" class="s" fill="{lightc[i]}">b={b}</text>')
svg.append("</g>")
svg.append("</svg>")
with open(os.path.join(RUN, "..", "picture.svg"), "w") as f:
    f.write("\n".join(svg).replace('<style text="style">','<style>').replace("</style>","</style>"))
print("metrics.json + picture.svg written")
print(json.dumps(merged, indent=1))
