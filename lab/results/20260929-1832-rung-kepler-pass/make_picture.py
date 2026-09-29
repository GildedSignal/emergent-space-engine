#!/usr/bin/env python3
"""Builds picture.svg from the data files written by kepler_rung."""
import json
import math

PALETTE = dict(paper="#f4efe4", ink="#3a362f", grid="#dcd4c1", faint="#e8e1d0",
               lf="#33697e", eu="#b3593b", note="#8a7f66", star="#c9a15a")

def read_xy(path):
    pts = []
    with open(path) as f:
        for line in f:
            a, b = line.split()
            pts.append((float(a), float(b)))
    return pts

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def fmt_exp(v):
    if v == 0:
        return "0"
    return f"{v:.2e}".replace("e-0", "e-").replace("e+0", "e+")

traj_lf = read_xy("traj_leapfrog.txt")
traj_eu = read_xy("traj_euler.txt")
ener_lf = read_xy("ener_leapfrog.txt")
ener_eu = read_xy("ener_euler.txt")
win_lf  = read_xy("win_leapfrog.txt")
win_eu  = read_xy("win_euler.txt")

metrics = json.load(open("metrics.json"))
m_lf, m_eu = metrics["leapfrog"], metrics["euler"]
h = 2 * math.pi / 200.0
t_end = 2000000 * h
t_unbind_eu = 15547 * h

W, H = 1240, 830
S = []
S.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="DejaVu Sans Mono, monospace">')
S.append(f'<rect width="{W}" height="{H}" fill="{PALETTE["paper"]}"/>')
S.append(f'<text x="30" y="34" font-size="19" fill="{PALETTE["ink"]}" '
         f'font-weight="bold">Kepler rung canary &#8212; e = 0.5, h = T/200, '
         f'10&#8308; orbits, float64</text>')
S.append(f'<text x="30" y="56" font-size="13" fill="{PALETTE["note"]}">'
         f'leapfrog stays bound (bounded |dE| oscillation) &#183; '
         f'euler spirals out and escapes at orbit 77.7</text>')

def orbit_panel(x0, y0, x1, y1, pts, color, title, sub):
    """Square-aspect plot of a trajectory, plus the true ellipse dashed."""
    S.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" '
             f'fill="#faf6ec" stroke="{PALETTE["grid"]}"/>')
    xs = [p[0] for p in pts] + [-1.5, 0.5]
    ys = [p[1] for p in pts] + [-0.87, 0.87]
    xmin, xmax, ymin, ymax = min(xs), max(xs), min(ys), max(ys)
    cx, cy = (xmin + xmax) / 2, (ymin + ymax) / 2
    half = max(xmax - xmin, ymax - ymin) / 2 * 1.08
    scale = min(x1 - x0, y1 - y0) / (2 * half)
    def PX(x, y): return (x0 + (x1 - x0) / 2 + (x - cx) * scale,
                          y0 + (y1 - y0) / 2 - (y - cy) * scale)
    ax0, ay0 = PX(xmin - 2 * half, 0)
    bx0, by0 = PX(0, ymin - 2 * half)
    S.append(f'<line x1="{x0}" y1="{ay0:.1f}" x2="{x1}" y2="{ay0:.1f}" '
             f'stroke="{PALETTE["faint"]}"/>')
    S.append(f'<line x1="{bx0:.1f}" y1="{y0}" x2="{bx0:.1f}" y2="{y1}" '
             f'stroke="{PALETTE["faint"]}"/>')
    # true ellipse: a=1, b=sqrt(3)/2, focus at origin -> center (-0.5, 0)
    ep = []
    for i in range(241):
        th = 2 * math.pi * i / 240
        ex, ey = -0.5 + math.cos(th), (math.sqrt(3) / 2) * math.sin(th)
        px, py = PX(ex, ey)
        ep.append(f"{px:.1f},{py:.1f}")
    S.append(f'<polyline points="{" ".join(ep)}" fill="none" '
             f'stroke="{PALETTE["note"]}" stroke-width="1" stroke-dasharray="4 4"/>')
    # star at focus
    fx, fy = PX(0, 0)
    S.append(f'<circle cx="{fx:.1f}" cy="{fy:.1f}" r="3.2" fill="{PALETTE["star"]}"/>')
    # trajectory, downsampled
    step = max(1, len(pts) // 3000)
    tp = []
    for i in range(0, len(pts), step):
        px, py = PX(*pts[i])
        tp.append(f"{px:.1f},{py:.1f}")
    S.append(f'<polyline points="{" ".join(tp)}" fill="none" stroke="{color}" '
             f'stroke-width="1" opacity="0.9"/>')
    px, py = PX(*pts[0])
    S.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3" fill="{color}"/>')
    S.append(f'<text x="{x0+8}" y="{y0+18}" font-size="13" fill="{PALETTE["ink"]}" '
             f'font-weight="bold">{esc(title)}</text>')
    S.append(f'<text x="{x0+8}" y="{y0+34}" font-size="11" fill="{PALETTE["note"]}">{esc(sub)}</text>')

orbit_panel(30, 80, 430, 430, traj_lf, PALETTE["lf"], "leapfrog (first 40 orbits)",
            f"max|dE| = 1.34e-3, bounded; slope = {fmt_exp(m_lf['energy_growth_exponent'])}")
orbit_panel(460, 80, 860, 430, traj_eu, PALETTE["eu"], "euler (first 40 orbits)",
            "escapes: E >= 0 at orbit 77.7 of 10^4")

# ---- readout column -------------------------------------------------------
rx, ry = 885, 80
S.append(f'<rect x="{rx}" y="{ry}" width="335" height="350" fill="#faf6ec" '
         f'stroke="{PALETTE["grid"]}"/>')
rows = [
    ("", "leapfrog", "euler", True),
    ("energy_growth_exponent", fmt_exp(m_lf["energy_growth_exponent"]),
     fmt_exp(m_eu["energy_growth_exponent"]), False),
    ("  E1  type     &lt;= 0.2", "pass", "pass", False),
    ("bound_fraction", f"{m_lf['bound_fraction']:.4f}", f"{m_eu['bound_fraction']:.5f}", False),
    ("  B1  behaviour &gt;= 1.0", "pass", "FAIL", False),
    ("steps_per_orbit", "200", "200", False),
    ("  C1  cost      &lt;= 256", "pass", "pass", False),
    ("verdict", "PASS", "FAIL", True),
]
yy = ry + 26
for label, a, b, bold in rows:
    fw = ' font-weight="bold"' if bold else ""
    S.append(f'<text x="{rx+12}" y="{yy}" font-size="12" fill="{PALETTE["ink"]}"{fw}>{label}</text>')
    S.append(f'<text x="{rx+215}" y="{yy}" font-size="12" fill="{PALETTE["lf"]}"{fw}>{esc(a)}</text>')
    S.append(f'<text x="{rx+280}" y="{yy}" font-size="12" fill="{PALETTE["eu"]}"{fw}>{esc(b)}</text>')
    yy += 24 if not bold else 28
S.append(f'<text x="{rx+12}" y="{yy+2}" font-size="10.5" fill="{PALETTE["note"]}">'
         f'euler E1 passes vacuously: it unbinds before</text>')
S.append(f'<text x="{rx+12}" y="{yy+16}" font-size="10.5" fill="{PALETTE["note"]}">'
         f't = 0.1*t_end, so all 20 windows sit on the</text>')
S.append(f'<text x="{rx+12}" y="{yy+30}" font-size="10.5" fill="{PALETTE["note"]}">'
         f'post-escape plateau |dE| = 0.537.</text>')

# ---- energy panel ---------------------------------------------------------
ex0, ex1, ey0, ey1 = 90, 1190, 480, 780
def LX(t): return ex0 + (math.log10(t) - math.log10(40)) / (math.log10(t_end) - math.log10(40)) * (ex1 - ex0)
def LY(v): return ey1 - (math.log10(v) - (-6)) / (0 - (-6)) * (ey1 - ey0)
S.append(f'<rect x="{ex0}" y="{ey0}" width="{ex1-ex0}" height="{ey1-ey0}" '
         f'fill="#faf6ec" stroke="{PALETTE["grid"]}"/>')
for d in range(-6, 1):
    y = LY(10.0 ** d)
    S.append(f'<line x1="{ex0}" y1="{y:.1f}" x2="{ex1}" y2="{y:.1f}" '
             f'stroke="{PALETTE["faint"]}"/>')
    S.append(f'<text x="{ex0-10}" y="{y+4:.1f}" font-size="11" fill="{PALETTE["note"]}" '
             f'text-anchor="end">1e{d}</text>')
for d in range(2, 8):
    x = LX(10.0 ** d)
    S.append(f'<line x1="{x:.1f}" y1="{ey0}" x2="{x:.1f}" y2="{ey1}" '
             f'stroke="{PALETTE["faint"]}"/>')
    S.append(f'<text x="{x:.1f}" y="{ey1+18}" font-size="11" fill="{PALETTE["note"]}" '
             f'text-anchor="middle">1e{d}</text>')
xu = LX(0.1 * t_end)
S.append(f'<line x1="{xu:.1f}" y1="{ey0}" x2="{xu:.1f}" y2="{ey1}" '
         f'stroke="{PALETTE["note"]}" stroke-dasharray="5 4"/>')
S.append(f'<text x="{xu-6:.1f}" y="{ey0+16}" font-size="11" fill="{PALETTE["note"]}" '
         f'text-anchor="end">windows start: t = 0.1*t_end (orbit 1000)</text>')
for pts, color in ((ener_lf, PALETTE["lf"]), (ener_eu, PALETTE["eu"])):
    pl = " ".join(f"{LX(t):.1f},{LY(v):.1f}" for t, v in pts if 40 <= t <= t_end and v >= 1e-6)
    S.append(f'<polyline points="{pl}" fill="none" stroke="{color}" '
             f'stroke-width="1.2" opacity="0.85"/>')
for pts, color in ((win_lf, PALETTE["lf"]), (win_eu, PALETTE["eu"])):
    for t, v in pts:
        S.append(f'<circle cx="{LX(t):.1f}" cy="{LY(max(v,1e-6)):.1f}" r="3.4" '
                 f'fill="{color}" stroke="#faf6ec" stroke-width="1"/>')
xu2 = LX(t_unbind_eu)
S.append(f'<circle cx="{xu2:.1f}" cy="{ey1}" r="4" fill="{PALETTE["eu"]}"/>')
S.append(f'<text x="{xu2+7:.1f}" y="{ey1-8}" font-size="11" fill="{PALETTE["eu"]}">'
         f'euler unbinds (orbit 77.7)</text>')
S.append(f'<text x="{ex0+10}" y="{ey0+18}" font-size="13" fill="{PALETTE["ink"]}" '
         f'font-weight="bold">|dE| vs t &#8212; dots: the 20 window maxima the exponent fits</text>')
S.append(f'<text x="{ex0+10}" y="{ey0+36}" font-size="11.5" fill="{PALETTE["lf"]}">'
         f'leapfrog: flat, slope {fmt_exp(m_lf["energy_growth_exponent"])} (bounded oscillation)</text>')
S.append(f'<text x="{ex0+10}" y="{ey0+52}" font-size="11.5" fill="{PALETTE["eu"]}">'
         f'euler: secular rise, then plateau at |E_inf - E0| = 0.537; slope '
         f'{fmt_exp(m_eu["energy_growth_exponent"])} on the plateau</text>')
S.append(f'<text x="{(ex0+ex1)/2}" y="{ey1+40}" font-size="12" fill="{PALETTE["note"]}" '
         f'text-anchor="middle">t (GM = 1, T = 2*pi; run ends at t = 1.26e7 = 10^4 orbits)</text>')
S.append(f'<text x="34" y="{(ey0+ey1)/2}" font-size="12" fill="{PALETTE["note"]}" '
         f'text-anchor="middle" transform="rotate(-90 34 {(ey0+ey1)/2})">|dE|</text>')
S.append('</svg>')
open("picture.svg", "w").write("\n".join(S))
print(f"picture.svg written, {len(S)} elements")
