"""Assemble metrics.json, the picture and the summary from the rung outputs (casea/b/c/d .jsonl)."""
import json, math, re, sys

RUN = "."
def lines(name):
    try:
        return [json.loads(l) for l in open(f"{RUN}/{name}") if l.strip().startswith("{")]
    except FileNotFoundError:
        return []

casea = lines("casea.jsonl"); caseb = lines("caseb.jsonl"); casec = lines("casec.jsonl"); cased = lines("cased.jsonl")
pool = {r["cfg"]: r for r in casea if r.get("exp") == "pool"}
if not pool:  # partial run: pool from the per-belt lines
    agg = {}
    for r in casea:
        if r.get("exp") != "a":
            continue
        nt = r.get("n_truth", r["truth"])
        for cfg, mi, fa, ch in [("diophantine", r["missed_d"], r["false_d"], r["checks_d"]),
                                ("element-sort", r["missed_c"], r["false_c"], r["conj_events"]),
                                ("conjunction-sampled", r["missed_c"], r["false_c"], r["conj_events"]),
                                ("oracle", 0, 0, nt)]:
            a = agg.setdefault(cfg, [0, 0, 0, 0]); a[0] += mi; a[1] += fa; a[2] += nt; a[3] += ch
    pool = {k: {"missed_fraction": v[0]/max(v[2],1), "false_fraction": v[1]/max(v[2],1),
                "truth": v[2], "checks": v[3], "checks_per_encounter": v[3]/max(v[2],1)} for k, v in agg.items()}
truth_rate = next(r for r in caseb if r.get("exp") == "b-truth")
bd = {r["orbits"]: r for r in caseb if r.get("exp") == "b-dioph"}
bn = {r["orbits"]: r for r in caseb if r.get("exp") == "b-neg"}
fit = next(r for r in casec if r.get("exp") == "c-fit")
d = next(r for r in cased if r.get("exp") == "d")
bbytes = next((r for r in caseb if r.get("exp") == "b-bytes"), None)

# steady_ratio at the rung's horizon 1e5 orbits; oracle reads the truth's list (ratio 1 by construction)
steady = {
    "diophantine": bd[1e5]["steady_ratio"],
    "element-sort": bn[1e5]["steady_ratio"],
    "conjunction-sampled": bn[1e5]["steady_ratio"],
    "oracle": 1.0,
}
m = {}
for cfg in ["diophantine", "element-sort", "conjunction-sampled", "oracle"]:
    p = pool[cfg]
    m[cfg] = {
        "missed_fraction": p["missed_fraction"],
        "false_fraction": p["false_fraction"],
        "steady_ratio": steady[cfg],
        "checks_per_encounter": p["checks_per_encounter"],
        "scale_exponent": {
            "diophantine": fit["scale_exponent_dioph"],
            "element-sort": fit["scale_exponent_esort"],
            "conjunction-sampled": fit["scale_exponent_conj"],
            "oracle": fit["scale_exponent_oracle"],
        }[cfg],
        "kick_setup_ratio": d["kick_setup_ratio_dioph"] if cfg == "diophantine" else d["kick_setup_ratio_radial"],
        "other_certificates_touched": 0,
    }
json.dump(m, open("metrics.json", "w"), indent=1)
print(json.dumps(m, indent=1))

# ---- picture: events per body per orbit vs horizon (log-log), truth rate as a line
H = sorted(bd.keys())
dioph = [bd[h]["events_per_body_orbit"] for h in H]
neg = [bn[h]["events_per_body_orbit"] for h in H]
rate = truth_rate["rate"]
xs = [math.log10(h) for h in H]
x0, x1 = xs[0] - 0.15, xs[-1] + 0.15
ylo = min(min(dioph), rate) ; yhi = max(max(dioph), max(neg))
ys0, ys1 = math.log10(ylo) - 0.2, math.log10(yhi) + 0.25
W, Ht, mx, my = 760, 520, 70, 55
def X(x): return mx + (x - x0) / (x1 - x0) * (W - 2 * mx)
def Y(y): return Ht - my - (math.log10(y) - ys0) / (ys1 - ys0) * (Ht - 2 * my)
def path(vals, color, dash="", lbl=None, off=0):
    pts = " ".join(f"{X(x):.1f},{Y(v):.1f}" for x, v in zip(xs, vals))
    s = f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.2" {dash}/>'
    if lbl: s += f'<text x="{X(xs[-1])+6:.0f}" y="{Y(vals[-1])+4:.0f}" font-size="13" fill="{color}">{lbl}</text>'
    return s
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{Ht}" font-family="Helvetica,Arial">',
       '<rect width="100%" height="100%" fill="white"/>',
       f'<text x="{W/2}" y="24" text-anchor="middle" font-size="16">r8 v3 — events per body per orbit vs horizon (N=3000, rho=1e-4)</text>']
for h in H:
    svg.append(f'<line x1="{X(math.log10(h)):.1f}" y1="{Ht-my}" x2="{X(math.log10(h)):.1f}" y2="{Ht-my+5}" stroke="gray"/>')
    svg.append(f'<text x="{X(math.log10(h)):.1f}" y="{Ht-my+20}" text-anchor="middle" font-size="12" fill="gray">{h:g}</text>')
dec = math.floor(ys0); 
yy = ys0
while yy <= ys1:
    v = 10 ** yy
    svg.append(f'<line x1="{mx-5}" y1="{Y(v):.1f}" x2="{mx}" y2="{Y(v):.1f}" stroke="gray"/>')
    svg.append(f'<text x="{mx-8}" y="{Y(v)+4:.1f}" text-anchor="end" font-size="11" fill="gray">{v:.0e}</text>'.replace("e-0", "e-").replace("e+0", "e"))
    yy += 1
svg.append(f'<line x1="{mx}" y1="{Ht-my}" x2="{W-mx}" y2="{Ht-my}" stroke="black"/><line x1="{mx}" y1="{my}" x2="{mx}" y2="{Ht-my}" stroke="black"/>')
svg.append(f'<text x="{W/2}" y="{Ht-8}" text-anchor="middle" font-size="13">horizon (orbits at a=1)</text>')
svg.append(f'<text x="18" y="{Ht/2}" text-anchor="middle" font-size="13" transform="rotate(-90 18 {Ht/2})">events per body per orbit</text>')
svg.append(path(dioph, "#0b6e4f", lbl="diophantine"))
svg.append(path(neg, "#b3541e", dash='stroke-dasharray="8 4"', lbl="element-sort / conjunction-sampled"))
yr = Y(rate)
svg.append(f'<line x1="{mx}" y1="{yr:.1f}" x2="{W-mx}" y2="{yr:.1f}" stroke="#1f4e9c" stroke-width="1.6" stroke-dasharray="3 3"/>')
svg.append(f'<text x="{W-mx-4}" y="{yr-6:.1f}" text-anchor="end" font-size="13" fill="#1f4e9c">truth encounter rate {rate:.2e}</text>')
svg.append(f'<text x="{W-mx-4}" y="{yr+14:.1f}" text-anchor="end" font-size="12" fill="#606060">(oracle sits on this line)</text>')
for x, v in zip(xs, dioph):
    svg.append(f'<circle cx="{X(x):.1f}" cy="{Y(v):.1f}" r="3.4" fill="#0b6e4f"/>')
for x, v in zip(xs, neg):
    svg.append(f'<circle cx="{X(x):.1f}" cy="{Y(v):.1f}" r="3.4" fill="#b3541e"/>')
svg.append(f'<text x="{mx+8}" y="{my+16}" font-size="12" fill="#404040">setup amortises as 1/orbit; the steady gate is the ratio to the truth line at 1e5 orbits</text>')
svg.append('</svg>')
open("picture.svg", "w").write("\n".join(svg))
print("picture.svg written", len("\n".join(svg)))
