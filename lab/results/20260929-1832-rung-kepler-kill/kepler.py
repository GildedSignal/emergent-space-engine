#!/usr/bin/env python3
"""Rung canary 20260929-1832-rung-kepler-kill (frozen case, see author-prompt.md).

One case: Kepler, GM = 1, a = 1, e = 0.5, float64, start at periapsis
x = (0.5, 0), v = (0, sqrt 3), fixed step h = T/200 with T = 2*pi,
2,000,000 steps = 10^4 orbits. Two configurations:
  euler  - forward Euler: x += h*v and v += h*a(x), both from the old state
  frozen - the body never advances (negative control); it is still stepped

Metrics, exactly as the rung defines them (state after every step,
E = |v|^2/2 - 1/|x|, dE = E - E0 with E0 = -0.5):
  energy_growth_exponent  least-squares slope of ln(max|dE| per window) vs
                          ln(geometric mid-time), 20 log-spaced windows over
                          [0.1*t_end, t_end], maxima floored at 1e-16
  bound_fraction          fraction of the run before the first step with E >= 0
  steps_per_orbit         total steps / 10^4, counting every substep
  orbit_closure_count     floor(|sum d_theta| / 2*pi), d_theta the signed angle
                          swept per step (atan2 of cross vs dot)

Run: python3 kepler.py   (stdlib only; writes metrics.json and picture.svg)
"""
import json
import math
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))

T = 2.0 * math.pi
H = T / 200.0
N = 2_000_000
ORBITS = 10_000
E0 = -0.5
# 20 windows: log-spaced edges from 0.1*N to N, in step units (time = n*h)
EDGES = [0.1 * N * 10.0 ** (j / 20.0) for j in range(21)]


def run(config):
    x, y = 0.5, 0.0
    vx, vy = 0.0, math.sqrt(3.0)
    advance = config != "frozen"
    atan2, sqrt, ab = math.atan2, math.sqrt, abs
    h = H

    sum_dtheta = 0.0
    first_unbound = -1          # step index of the first step with E >= 0
    win = [0.0] * 20
    j = 0                       # window j holds steps with EDGES[j] < n <= EDGES[j+1]
    samples = []                # (t in orbits, x, y) while in view (r <= 4)
    sampling = advance          # the frozen body never leaves; no samples needed
    n_out = -1                  # first step with r > 4

    for n in range(1, N + 1):
        px, py = x, y
        if advance:
            r2 = x * x + y * y
            r = sqrt(r2)
            s = -h / (r2 * r)
            ax = x * s
            ay = y * s
            x += h * vx
            y += h * vy
            vx += ax
            vy += ay
        # metrics from the state after the step
        r2 = x * x + y * y
        r = sqrt(r2)
        E = 0.5 * (vx * vx + vy * vy) - 1.0 / r
        dE = E - E0
        sum_dtheta += atan2(px * y - py * x, px * x + py * y)
        if first_unbound < 0 and E >= 0.0:
            first_unbound = n
        while j < 19 and n > EDGES[j + 1]:
            j += 1
        a = ab(dE)
        if a > win[j]:
            win[j] = a
        if sampling:
            if r > 4.0:
                samples.append((n * h / T, x, y))
                n_out = n
                sampling = False
            elif n == 1 or (n <= 2048 and n % 4 == 0) or n % 64 == 0:
                if len(samples) < 20000:
                    samples.append((n * h / T, x, y))

    r_final = math.hypot(x, y)
    E_final = 0.5 * (vx * vx + vy * vy) - 1.0 / r_final
    L_final = x * vy - y * vx

    m = [max(w, 1e-16) for w in win]
    tau = [H * math.sqrt(EDGES[j] * EDGES[j + 1]) for j in range(20)]  # time
    lnx = [math.log(t) for t in tau]
    lny = [math.log(v) for v in m]
    mx = sum(lnx) / 20.0
    my = sum(lny) / 20.0
    sxx = sum((v - mx) ** 2 for v in lnx)
    sxy = sum((a * b - mx * my) for a, b in zip(lnx, lny))
    slope = sxy / sxx

    metrics = {
        "energy_growth_exponent": slope,
        "bound_fraction": 1.0 if first_unbound < 0 else (first_unbound - 1) / N,
        "steps_per_orbit": N / ORBITS,
        "orbit_closure_count": int(math.floor(ab(sum_dtheta) / T)),
    }
    diag = {
        "escape_orbit": None if first_unbound < 0 else first_unbound * H / T,
        "leaves_r4_orbit": None if n_out < 0 else n_out * H / T,
        "E_final": E_final,
        "r_final": r_final,
        "L_final": L_final,
        "revolutions": ab(sum_dtheta) / T,
        "m": m,
        "tau_orbits": [t / T for t in tau],
        "samples": samples,
    }
    return metrics, diag


def svg(all_metrics, all_diag):
    eu = all_diag["euler"]
    esc = eu["escape_orbit"]
    esc_s = f"orbit {esc:.1f}" if esc is not None else "never"
    out = eu["leaves_r4_orbit"]
    out_s = f"orbit {out:.1f}" if out is not None else "never"

    S = []
    S.append('<svg xmlns="http://www.w3.org/2000/svg" width="980" height="560" '
             'viewBox="0 0 980 560" font-family="ui-monospace, Menlo, Consolas, monospace">')
    S.append('<rect width="980" height="560" fill="#0f1318"/>')
    S.append('<text x="24" y="34" fill="#d6dde5" font-size="15">forward Euler kills a Kepler orbit '
             '(e = 0.5, h = T/200, 10&#8308; orbits)</text>')
    S.append('<text x="24" y="52" fill="#6b7887" font-size="11">rung canary 20260929-1832-rung-kepler-kill'
             ' &#183; cloud Linux/x86</text>')

    # ---- panel A: the orbit, clipped at r = 4 --------------------------------
    cx, cy, sc = 250.0, 306.0, 55.0
    A = ['<rect x="24" y="66" width="452" height="470" fill="#12171d" stroke="#232c37"/>']
    A.append(f'<circle cx="{cx}" cy="{cy}" r="{sc}" fill="none" stroke="#2a3440" stroke-dasharray="3 4"/>')
    A.append(f'<circle cx="{cx}" cy="{cy}" r="{4*sc}" fill="none" stroke="#26303b" stroke-dasharray="3 6"/>')
    A.append(f'<text x="{cx + sc + 5:.0f}" y="{cy + 4:.0f}" fill="#55636f" font-size="10">r = 1</text>')
    A.append(f'<text x="{cx + 4*sc - 34:.0f}" y="{cy - 4*sc - 6:.0f}" fill="#55636f" font-size="10">clip r = 4</text>')
    # exact e = 0.5 ellipse as the implied reference (focus at the origin)
    A.append(f'<ellipse cx="{cx - 0.5*sc:.1f}" cy="{cy}" rx="{sc}" ry="{0.8660254*sc:.1f}" '
             'fill="none" stroke="#465360" stroke-dasharray="5 4" opacity="0.85"/>')
    pts = " ".join(f"{cx + sc*x:.1f},{cy - sc*y:.1f}" for _, x, y in eu["samples"])
    A.append(f'<polyline points="{pts}" fill="none" stroke="#d8c398" stroke-width="1" opacity="0.9"/>')
    A.append(f'<circle cx="{cx}" cy="{cy}" r="6" fill="#f4ead2" opacity="0.12"/>')
    A.append(f'<circle cx="{cx}" cy="{cy}" r="2.6" fill="#f4ead2"/>')
    sx, sy = eu["samples"][0][1], eu["samples"][0][2]
    A.append(f'<circle cx="{cx + sc*sx:.1f}" cy="{cy - sc*sy:.1f}" r="2.6" fill="#e6e2d3"/>')
    A.append(f'<text x="{cx + sc*sx + 7:.1f}" y="{cy - sc*sy + 3:.1f}" fill="#93a1af" font-size="10">start</text>')
    A.append(f'<text x="36" y="86" fill="#93a1af" font-size="11">E &#8805; 0 at {esc_s};'
             f' crosses r = 4 at {out_s}; {eu["revolutions"]:.2f} revolutions total</text>')
    A.append(f'<text x="36" y="102" fill="#6b7887" font-size="10">dashed: exact e = 0.5 ellipse;'
             f' final r = {eu["r_final"]:.0f}</text>')
    S += A

    # ---- panel B: window maxima, log-log --------------------------------------
    x0, x1, y0, y1 = 610.0, 956.0, 96.0, 480.0   # plot rect
    lt = [math.log10(t) for t in eu["tau_orbits"]]
    lm = [math.log10(v) for v in eu["m"]]
    xmin, xmax = min(lt) - 0.06, max(lt) + 0.06
    ymin = math.floor(min(min(lm), math.log10(0.5)))
    ymax = math.ceil(max(lm) + 0.2)

    def X(v):
        return x0 + (v - xmin) / (xmax - xmin) * (x1 - x0)

    def Y(v):
        return y1 - (v - ymin) / (ymax - ymin) * (y1 - y0)

    n = len(lt)
    mxt, myt = sum(lt) / n, sum(lm) / n
    sl = sum((a - mxt) * (b - myt) for a, b in zip(lt, lm)) / sum((a - mxt) ** 2 for a in lt)

    B = ['<rect x="516" y="66" width="440" height="470" fill="#12171d" stroke="#232c37"/>',
         '<text x="528" y="86" fill="#d6dde5" font-size="12">max |&#916;E| per window &#8212; euler (log&#8211;log)</text>']
    for k in range(ymin, ymax + 1):
        B.append(f'<line x1="{x0}" y1="{Y(k):.1f}" x2="{x1}" y2="{Y(k):.1f}" stroke="#212a34"/>')
        B.append(f'<text x="{x0 - 8}" y="{Y(k) + 3.5:.1f}" fill="#55636f" font-size="10" text-anchor="end">1e{k}</text>')
    for k in (3, 4):
        B.append(f'<line x1="{X(k):.1f}" y1="{y0}" x2="{X(k):.1f}" y2="{y1}" stroke="#212a34"/>')
        B.append(f'<text x="{X(k):.1f}" y="{y1 + 14:.1f}" fill="#55636f" font-size="10" text-anchor="middle">1e{k}</text>')
    B.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="#39434f"/>')
    B.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="#39434f"/>')
    B.append(f'<text x="{(x0 + x1) / 2:.0f}" y="{y1 + 28:.1f}" fill="#55636f" font-size="10" '
             'text-anchor="middle">mid-time (orbits)</text>')
    # unbound level |dE| = 0.5
    B.append(f'<line x1="{x0}" y1="{Y(math.log10(0.5)):.1f}" x2="{x1}" y2="{Y(math.log10(0.5)):.1f}" '
             'stroke="#8a5a4a" stroke-dasharray="2 3"/>')
    B.append(f'<text x="{x1}" y="{Y(math.log10(0.5)) - 5:.1f}" fill="#a06a55" font-size="10" '
             'text-anchor="end">|&#916;E| = 0.5: unbound level</text>')
    # least-squares fit line
    fy0, fy1 = myt + sl * (xmin - mxt), myt + sl * (xmax - mxt)
    B.append(f'<line x1="{X(xmin):.1f}" y1="{Y(fy0):.1f}" x2="{X(xmax):.1f}" y2="{Y(fy1):.1f}" '
             'stroke="#8fa1b3" stroke-dasharray="5 4" opacity="0.9"/>')
    for a, b in zip(lt, lm):
        B.append(f'<circle cx="{X(a):.1f}" cy="{Y(b):.1f}" r="2.6" fill="#d8c398"/>')
    B.append(f'<text x="528" y="502" fill="#93a1af" font-size="11">fit slope = {sl:.3f}'
             f' (energy_growth_exponent = {all_metrics["euler"]["energy_growth_exponent"]:.3f})</text>')
    B.append(f'<text x="528" y="518" fill="#6b7887" font-size="10">windows start at t = 1000 orbits;'
             f' the drift finished by {esc_s} &#8212; all 20 sit on the post-escape plateau</text>')
    S += B

    S.append('<text x="516" y="556" fill="#6b7887" font-size="10">frozen control: |&#916;E| = 0 at the 1e-16 floor,'
             ' 0 revolutions (fails R1) &#183; euler unbinds (fails B1), slope and cost pass</text>')
    S.append("</svg>")
    return "\n".join(S)


def main():
    t0 = time.time()
    out = {}
    diags = {}
    for config in ("euler", "frozen"):
        t1 = time.time()
        m, d = run(config)
        out[config] = m
        diags[config] = d
        print(f"{config:7s} {time.time() - t1:5.1f}s  " + "  ".join(f"{k}={v}" for k, v in m.items()))
        dd = {k: v for k, v in d.items() if k not in ("samples", "m", "tau_orbits")}
        print(f"        diag: {dd}")

    with open(os.path.join(HERE, "metrics.json"), "w") as f:
        json.dump(out, f, indent=1)
    with open(os.path.join(HERE, "picture.svg"), "w") as f:
        f.write(svg(out, diags))
    print(f"total {time.time() - t0:.1f}s -> metrics.json, picture.svg")


if __name__ == "__main__":
    main()
