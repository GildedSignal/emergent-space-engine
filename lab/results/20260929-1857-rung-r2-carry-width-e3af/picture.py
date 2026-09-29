#!/usr/bin/env python3
"""Picture: worst-seed phase error vs cycles, log-log, one curve per configuration."""
import json, math

RUN = "lab/results/20260929-1857-rung-r2-carry-width-e3af"
d = json.load(open(f"{RUN}/detail.json"))
Ns, det = d["sample_N"], d["detail"]

W, H, M = 880, 540, 64
X0, X1, Y0, Y1 = M, W - 178, H - 50, 56          # plot rect
XMIN, XMAX, YMIN, YMAX = 0.0, 6.0, -10.0, 2.0    # log10 N in [1,1e6]; log10 err rad

def px(x): return X0 + (x - XMIN) / (XMAX - XMIN) * (X1 - X0)
def py(y): return Y0 + (y - YMIN) / (YMAX - YMIN) * (Y1 - Y0)

CFG = [("trunc16", "#c0392b", "trunc16 (negative)"),
       ("round16", "#e67e22", "round16 (negative)"),
       ("sd16",    "#8e44ad", "sd16"),
       ("sd24",    "#2980b9", "sd24"),
       ("sd32",    "#1e8449", "sd32")]

out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">',
       '<rect width="100%" height="100%" fill="#ffffff"/>',
       f'<text x="{M}" y="26" font-size="16" font-weight="bold" fill="#222">Rung r2 — phase error vs cycles (worst seed per configuration)</text>',
       f'<text x="{M}" y="44" font-size="11" fill="#666">|phi_stored - phi_true| in radians, log-log. Linear growth (slope 1) is the compounding type and fails; sd32 is exactly zero.</text>']

for e in range(0, 7):
    x = px(e)
    out.append(f'<line x1="{x:.1f}" y1="{Y1}" x2="{x:.1f}" y2="{Y0}" stroke="#e6e6e6" stroke-width="1"/>')
    out.append(f'<text x="{x:.1f}" y="{Y0+16}" font-size="11" fill="#555" text-anchor="middle">{"1" if e == 0 else f"1e{e}"}</text>')
for e in range(int(YMIN), int(YMAX) + 1):
    y = py(e)
    out.append(f'<line x1="{X0}" y1="{y:.1f}" x2="{X1}" y2="{y:.1f}" stroke="#e6e6e6" stroke-width="1"/>')
    if e % 2 == 0:
        out.append(f'<text x="{X0-8}" y="{y+4:.1f}" font-size="11" fill="#555" text-anchor="end">{"1" if e == 0 else f"1e{e}"}</text>')
out.append(f'<rect x="{X0}" y="{Y1}" width="{X1-X0}" height="{Y0-Y1}" fill="none" stroke="#999"/>')
out.append(f'<text x="{(X0+X1)//2}" y="{H-12}" font-size="12" fill="#333" text-anchor="middle">cycles</text>')
out.append(f'<text x="16" y="{(Y0+Y1)//2}" font-size="12" fill="#333" transform="rotate(-90 16 {(Y0+Y1)//2})" text-anchor="middle">|phase error| (rad)</text>')

for key, col, label in CFG:
    errs = det[key]["worst_phase_errors"]
    pts = [(math.log10(n), math.log10(er)) for n, er in zip(Ns, errs) if er > 0]
    if len(pts) >= 2:
        path = "M" + " L".join(f"{px(a):.1f},{py(b):.1f}" for a, b in pts)
        dash = "" if key not in ("trunc16", "round16") else ' stroke-dasharray="6,3"'
        out.append(f'<path d="{path}" fill="none" stroke="{col}" stroke-width="2"{dash}/>')

lx, ly = X1 + 18, Y1 + 12
for i, (key, col, label) in enumerate(CFG):
    y = ly + i * 20
    dash = ' stroke-dasharray="6,3"' if key in ("trunc16", "round16") else ""
    out.append(f'<line x1="{lx}" y1="{y-4}" x2="{lx+26}" y2="{y-4}" stroke="{col}" stroke-width="3"{dash}/>')
    out.append(f'<text x="{lx+32}" y="{y}" font-size="12" fill="#222">{label}</text>')
notes = ["sd32: error == 0 at every N",
         "(float64 generator fits",
         " exactly in a 32+32 pair)",
         "", "all others: slope 1",
         "= compounding type,",
         "fails &lt;= 0.2"]
for i, t in enumerate(notes):
    out.append(f'<text x="{lx}" y="{ly + 5*20 + 12 + i*14}" font-size="10.5" fill="#555">{t}</text>')
out.append('</svg>')
open(f"{RUN}/picture.svg", "w").write("\n".join(out))
print("wrote", f"{RUN}/picture.svg")
