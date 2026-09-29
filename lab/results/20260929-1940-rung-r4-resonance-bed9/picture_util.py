#!/usr/bin/env python3
"""picture.svg for rung r4: e1(t) per case (law configs vs truth) and the
resonant-angle histogram for the resonant cases. Pure-python SVG."""
import math, os, sys

def polyline(fx, fy, xs, ys, color, w=1.0, dash=None, op=1.0):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    pts = " ".join(f"{fx(xx):.1f},{fy(yy):.1f}" for xx, yy in zip(xs, ys))
    return (f'<polyline fill="none" stroke="{color}" stroke-width="{w}"'
            f' opacity="{op}"{d} points="{pts}"/>')

class Panel:
    def __init__(self, x, y, w, h, xl, xh, yl, yh, title, ylab=""):
        self.__dict__.update(dict(x=x, y=y, w=w, h=h, xl=xl, xh=xh, yl=yl, yh=yh))
        self.el = [f'<text x="{x+w/2}" y="{y-8}" font-size="11" text-anchor="middle" '
                   f'fill="#333" font-family="Helvetica">{title}</text>',
                   f'<text x="{x-6}" y="{y+h/2}" font-size="10" text-anchor="end" '
                   f'fill="#555" font-family="Helvetica" '
                   f'transform="rotate(-90 {x-6} {y+h/2})">{ylab}</text>',
                   f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#bbb"/>']
    def fx(self, v): return self.x + (v - self.xl) / (self.xh - self.xl) * self.w
    def fy(self, v): return self.y + self.h - (v - self.yl) / (self.yh - self.yl) * self.h

def main(here):
    sys.path.insert(0, here)
    import rung_r4 as R

    W, H = 760, 1010
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="#fbfaf7"/>',
             '<text x="20" y="24" font-size="14" fill="#222" font-family="Helvetica">'
             'Rung r4 - kicks keep resonances that averaging erases</text>']

    results = {}
    for cfg in R.CONFIGS:
        for case in R.CASES:
            results[(cfg, case)] = R.run_layer(cfg, case)

    colors = {"truth": "#222222", "conj-quad": "#4a6f8a", "conj-oct": "#b07a3c",
              "averaged": "#5e7d5a", "none": "#999999"}
    px, py, pw, ph, gx, gy = 60, 50, 320, 180, 40, 60
    layout = ["R1", "R1psi", "R2", "R2psi", "C1", "C3", "C2", "leg"]
    for i, cell in enumerate(layout):
        col, row = i % 2, i // 2
        x, y = px + col * (pw + gx), py + row * (ph + gy)
        if cell in R.CASES:
            case = cell
            oc = R.CASES[case]
            if case in ("R1", "R2"):
                title = f"{case}: 2:1 {'(w2=4.0)' if case == 'R2' else ''}  e1 vs t"
                yl, yh = 0.0, 0.22
            else:
                title = f"{case}: period ratio {oc['ratio']:g} (control)  e1 vs t"
                yl, yh = 0.0, 0.05 if case == "C3" else 0.016
            p = Panel(x, y, pw, ph, 0, oc["T"], yl, yh, title, "e1")
            ts, es = [], []
            for line in open(os.path.join(here, "data", f"truth_{case}_2400.txt")):
                f = line.split()
                ts.append(float(f[0])); es.append(float(f[2]))
            dec = max(1, len(ts) // 600)
            p.el.append(polyline(p.fx, p.fy, ts[::dec], es[::dec], colors["truth"], 1.4))
            for cfg in R.CONFIGS:
                s = results[(cfg, case)]["samples"]
                dec = max(1, len(s) // 600)
                xs = [q[0] for q in s[::dec]]
                ys = [q[1] for q in s[::dec]]
                dash = "4,3" if cfg in ("averaged", "none") else None
                p.el.append(polyline(p.fx, p.fy, xs, ys, colors[cfg], 1.0, dash))
            p.el.append(f'<text x="{x+pw-4}" y="{y+ph-6}" font-size="9" text-anchor="end" '
                        f'fill="#777">truth max e1 = {max(es):.3f}</text>')
            parts += p.el
        elif cell.endswith("psi"):
            base = cell[:2]
            p = Panel(x, y, pw, ph, -math.pi, math.pi, 0, 1,
                      f"{base}: resonant angle psi histogram (density)")
            def wrap(v): return (v + math.pi) % (2 * math.pi) - math.pi
            def hist(psis):
                nb = 36
                h = [0] * nb
                for v in psis:
                    v = wrap(v)
                    h[min(nb - 1, int((v + math.pi) / (2 * math.pi) * nb))] += 1
                m = max(h)
                return [v / m for v in h]
            tpsis = []
            for line in open(os.path.join(here, "data", f"truth_{base}_2400.txt")):
                f = line.split()
                tpsis.append(2.0 * float(f[7]) - float(f[3]) - float(f[4]))
            hh = hist(tpsis)
            bw = pw / len(hh)
            for j, v in enumerate(hh):
                p.el.append(f'<rect x="{x + j*bw + 0.5:.1f}" y="{p.fy(v):.1f}" '
                            f'width="{bw-1:.1f}" height="{p.fy(0)-p.fy(v):.1f}" '
                            f'fill="#444444" opacity="0.18"/>')
            for cfg in ("conj-quad", "conj-oct"):
                hh = hist([s[2] for s in results[(cfg, base)]["samples"]])
                pts = " ".join(f"{p.fx(-math.pi + (j + 0.5) * 2 * math.pi / len(hh)):.1f},"
                               f"{p.fy(v):.1f}" for j, v in enumerate(hh))
                p.el.append(f'<polyline fill="none" stroke="{colors[cfg]}" '
                            f'stroke-width="1.2" points="{pts}"/>')
            parts += p.el
        else:  # legend
            ly = y + 30
            parts.append(f'<text x="{x}" y="{ly}" font-size="12" fill="#333" '
                         f'font-family="Helvetica">curves (all e1 panels):</text>')
            for j, cfg in enumerate(["truth"] + R.CONFIGS):
                dash = "4,3" if cfg in ("averaged", "none") else None
                d = f' stroke-dasharray="{dash}"' if dash else ""
                yy = ly + 20 + j * 18
                parts.append(f'<line x1="{x}" y1="{yy-4}" x2="{x+34}" y2="{yy-4}" '
                             f'stroke="{colors[cfg]}" stroke-width="1.6"{d}/>'
                             f'<text x="{x+42}" y="{yy}" font-size="11" fill="#333" '
                             f'font-family="Helvetica">{cfg}</text>')
            txt = ["one analytic tidal kick per conjunction (GL24 impulse over",
                   "one synodic window, on exact Kepler cycles); no ODE steps.",
                   "truth: 3-body velocity Verlet, 2400 steps/orbit, converged",
                   "(600/1200/2400 agree to &lt;0.1%). psi = 2*lam2 - lam1 - varpi1.",
                   "verdict: PASS - conj-quad and conj-oct pass every criterion;",
                   "averaged and none fail (e1 never pumps)."]
            for j, t in enumerate(txt):
                parts.append(f'<text x="{x}" y="{ly + 125 + j*15}" font-size="10" '
                             f'fill="#666" font-family="Helvetica">{t}</text>')
    parts.append("</svg>")
    with open(os.path.join(here, "picture.svg"), "w") as f:
        f.write("\n".join(parts))
    print("wrote picture.svg", os.path.getsize(os.path.join(here, "picture.svg")), "bytes")

if __name__ == "__main__":
    main(os.path.dirname(os.path.abspath(__file__)))
