#!/usr/bin/env python3
"""picture.svg: e1(t) law vs truth for each case + resonant-angle histograms."""
import math, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

CASES = [("res-2to1", 0.5), ("res-2to1-shift", 0.5), ("ctrl-r5.00", 0.2),
         ("ctrl-r2.55", 1/2.55), ("ctrl-r2.15", 1/2.15)]   # (name, n2)
RES = ["res-2to1", "res-2to1-shift"]

def load(path):
    rows = []
    with open(path) as f:
        for line in f:
            a, b, c = line.split()
            rows.append((float(a), float(b), float(c)))
    return rows

W, H = 1660, 1000
PANEL_W, PANEL_H = 300, 200
MX, MY = 20, 70
colors = {"truth-2400": "#111111", "arc-g8": "#1f6fb2", "arc-g8-half": "#c17d1a", "none": "#999999"}

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def panel_xy(i, row):
    return MX + i*(PANEL_W+22), MY + row*(PANEL_H+58)

def line_path(rows, x0, y0, w, h, xmax, ymin, ymax, key):
    if not rows:
        return ""
    sx = w/max(xmax, 1e-9)
    sy = h/max(ymax-ymin, 1e-9)
    step = max(1, len(rows)//900)
    pts = []
    for t, e, phi in rows[::step]:
        px = x0 + t*sx
        py = y0 + h - (e-ymin)*sy
        pts.append(f"{px:.1f},{py:.1f}")
    return f'<polyline fill="none" stroke="{colors[key]}" stroke-width="1.1" points="{" ".join(pts)}"/>'

out = []
out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="Helvetica,Arial,sans-serif">')
out.append(f'<rect width="{W}" height="{H}" fill="#fcfcfa"/>')
out.append('<text x="20" y="26" font-size="17" font-weight="bold">Rung r4 v2 — 2:1 mean-motion resonance: arc-integrated kicks vs dense truth</text>')
out.append('<text x="20" y="46" font-size="12">restricted 3-body, m2/m1=3e-3, 2:1 exact, e1(0)=0.01, 200 synodic periods; black = truth (RK4, 2400 steps/orbit), blue = arc-g8 (Gauss–Picard element kicks at conjunctions)</text>')

# top row: e1(t) per case, truth vs arc-g8
for i, (case, n2) in enumerate(CASES):
    x0, y0 = panel_xy(i, 0)
    psyn = 2*math.pi/(1.0-n2)
    truth = load(os.path.join(DATA, f"{case}--truth-2400.txt"))
    law = load(os.path.join(DATA, f"{case}--arc-g8.txt"))
    half = load(os.path.join(DATA, f"{case}--arc-g8-half.txt"))
    xmax = 200.0
    ymax = max(r[1] for r in truth)*1.08 + 1e-3
    ymin = 0.0
    out.append(f'<rect x="{x0}" y="{y0}" width="{PANEL_W}" height="{PANEL_H}" fill="white" stroke="#bbb"/>')
    out.append(line_path(truth, x0, y0, PANEL_W, PANEL_H, xmax, ymin, ymax, "truth-2400"))
    out.append(line_path(half, x0, y0, PANEL_W, PANEL_H, xmax, ymin, ymax, "arc-g8-half"))
    out.append(line_path(law, x0, y0, PANEL_W, PANEL_H, xmax, ymin, ymax, "arc-g8"))
    tlaw = law[-1][0]/psyn if law else 0
    note = "" if tlaw > 197 else f'  t_guards={tlaw:.0f} syn'
    out.append(f'<text x="{x0+6}" y="{y0-8}" font-size="12" font-weight="bold">{esc(case)}</text>')
    out.append(f'<text x="{x0+6}" y="{y0+PANEL_H+15}" font-size="10">x: synodic periods (0–200); y: e1 (0–{ymax:.3f}){note}</text>')
    mt = max(r[1] for r in truth); ml = max(r[1] for r in law)
    out.append(f'<text x="{x0+6}" y="{y0+PANEL_H+29}" font-size="10">max e1: truth {mt:.4f}, arc-g8 {ml:.4f} (ratio {ml/mt:.2f})</text>')

# bottom row: histograms of the resonant angle, truth vs arc-g8
for j, case in enumerate(RES):
    x0, y0 = panel_xy(j, 1)
    truth = load(os.path.join(DATA, f"{case}--truth-2400.txt"))
    law = load(os.path.join(DATA, f"{case}--arc-g8.txt"))
    NB = 36
    def hist(rows):
        h = [0]*NB
        for t, e, phi in rows:
            h[min(NB-1, int(phi/(2*math.pi)*NB))] += 1
        return h
    ht, hl = hist(truth), hist(law)
    peak = max(max(ht), max(hl))
    bw = PANEL_W/NB
    for b in range(NB):
        hh = PANEL_H*ht[b]/peak*0.62
        out.append(f'<rect x="{x0+b*bw:.1f}" y="{y0+PANEL_H-hh:.1f}" width="{bw-0.6:.1f}" height="{hh:.1f}" fill="#333" opacity="0.55"/>')
        hh = PANEL_H*hl[b]/peak*0.62
        out.append(f'<rect x="{x0+b*bw:.1f}" y="{y0+PANEL_H-hh:.1f}" width="{bw-0.6:.1f}" height="{hh:.1f}" fill="#1f6fb2" opacity="0.65"/>')
    out.append(f'<rect x="{x0}" y="{y0}" width="{PANEL_W}" height="{PANEL_H}" fill="none" stroke="#bbb"/>')
    ct = abs(sum(math.cos(r[2]) for r in truth))/len(truth)
    cl = abs(sum(math.cos(r[2]) for r in law))/len(law)
    out.append(f'<text x="{x0+6}" y="{y0-8}" font-size="12" font-weight="bold">{esc(case)}: resonant angle phi = 2*lam2 - lam1 - varpi1</text>')
    out.append(f'<text x="{x0+6}" y="{y0+PANEL_H+15}" font-size="10">grey = truth, blue = arc-g8; x: phi 0..2pi ({NB} bins); concentration: truth {ct:.3f}, arc-g8 {cl:.3f}</text>')

# verdict box
x0, y0 = panel_xy(2, 1)
out.append(f'<rect x="{x0}" y="{y0}" width="{2*PANEL_W+22}" height="{PANEL_H}" fill="#f6e8e8" stroke="#c99"/>')
out.append(f'<text x="{x0+14}" y="{y0+28}" font-size="13" font-weight="bold">Verdict: KILL of arc-g8, arc-g16, arc-g8-half (positive control passes, negatives fail)</text>')
kv = [
    ("arc-g8", "pump ratio 1.27-1.30 (>1.25), lib ratio 0.23 (<0.8), controls 2/3"),
    ("arc-g16", "same as g8: quadrature is not the bottleneck"),
    ("arc-g8-half", "closest: pump 1.13-1.15, lib 0.68, controls 2/3"),
    ("mechanism", "first window kicks O(e1): Dvarpi ~ 1-10 rad/window, De up to -0.011 at e1=0.01;"),
    ("", "the pumping is second-order feedback a frozen arc cannot see (full-window Da=De~0 at exact 2:1)"),
    ("guard deaths", "arc runs end early (t~7-45 synodic); max_e is over their lifetime, not 200 synodic"),
]
for k, (a, b) in enumerate(kv):
    out.append(f'<text x="{x0+14}" y="{y0+52+k*20}" font-size="11"><tspan font-weight="bold">{esc(a)}</tspan>  {esc(b)}</text>')
out.append('</svg>')

with open(os.path.join(os.path.dirname(HERE), "picture.svg"), "w") as f:
    f.write("\n".join(out))
print("wrote picture.svg", sum(len(o) for o in out), "bytes")
