#!/usr/bin/env python3
"""Rung r10 metrics: reads raw-{truth,symba,wh,soi}.json, writes metrics.json and picture.svg.

Rules ported from the frozen rung and the gates it cites:
- jacobi_exponent (B12): median growth exponent over the frozen ships that are converged in the
  reference and rise above the 1e-12 floor; a ship below the floor has no exponent; if none
  rises, the median is 0. NaN counts as +inf.
- class_match (B14): over moons whose reference class is decided (bound or escaped, not chaotic
  or unconverged), the fraction whose escape flag matches.
- precession_match (B14): over bound moons with a stable reference apsidal rate, the fraction of
  the candidate's rates within 10% (a candidate with no rate misses).
- libration_ratio (B17): over converged resonant cases whose reference excursion is under 2pi
  and not within 20% of 2pi, the worst of min(r, 1/r), r = excursion ratio.
- force_evals_per_orbit: median over every body of every case (16 ships + 256 moons + 41
  resonant cases); the reference reports 0 by the rung's convention.
"""
import json, math, os, statistics

HERE = os.path.dirname(os.path.abspath(__file__))

def load(name):
    with open(os.path.join(HERE, f"raw-{name}.json")) as f:
        text = f.read()
    return json.loads("{" + text.replace('}\n"', '},\n"') + "}")

truth = load("truth")
configs = {"symba": load("symba"), "wh-fixed": load("wh"), "soi-switch": load("soi")}
RAWKEY = {"symba": "symba", "wh-fixed": "wh", "soi-switch": "soi"}

def median(xs):
    xs = sorted(math.inf if (isinstance(x, float) and math.isnan(x)) else x for x in xs)
    if not xs:
        return math.inf
    n = len(xs)
    return xs[n // 2] if n % 2 else 0.5 * (xs[n // 2 - 1] + xs[n // 2])

def jacobi_exponent(cfg):
    t = truth["ships_truth"]
    conv = t["converged"]
    if cfg == "truth":
        return 0.0, 0   # the reference defines the invariant; its own drift is reported separately
    exps, maxs = configs[cfg]["ships"]["exponent"], configs[cfg]["ships"]["max_err"]
    rising = [e for e, m, c in zip(exps, maxs, conv) if c and not (m <= 1e-12)]
    return (median(rising) if rising else 0.0), len(rising)

def class_match(cfg):
    tcls = truth["moons_truth"]["class"]
    esc = configs[cfg]["moons"]["escaped"]
    judged = agree = 0
    for i, c in enumerate(tcls):
        if c in (0, 1):
            judged += 1
            agree += int(bool(esc[i]) == (c == 1))
    return (agree / judged if judged else 0.0), judged

def prec_match(cfg):
    trate = [r if r != 0 else None for r in truth["moons_truth"]["rate"]]
    crate = [r if r != 0 else None for r in configs[cfg]["moons"]["rate"]]
    rated = ok = 0
    for rt, rc in zip(trate, crate):
        if rt is None:
            continue
        rated += 1
        if rc is not None and abs(rc - rt) <= 0.1 * abs(rt):
            ok += 1
    return (ok / rated if rated else 0.0), rated

def lib_ratio(cfg):
    tt, tc = truth["res_truth"], truth["res_truth"]["converged"]
    exc = configs[cfg]["res"]["excursion"]
    worst, n = 1.0, 0
    for i, j in enumerate(tt["kind_j"]):
        if j < 0 or not tc[i]:
            continue
        e_t = tt["excursion"][i]
        if e_t is None or not (e_t < 2 * math.pi) or abs(e_t - 2 * math.pi) <= 0.2 * 2 * math.pi:
            continue
        n += 1
        e_c = exc[i]
        if e_c is None:
            worst = 0.0
            continue
        r = e_c / e_t
        worst = min(worst, min(r, 1 / r) if r > 0 else 0.0)
    return worst, n

def force_evals(cfg):
    if cfg == "truth":
        return 0.0
    d = configs[cfg]
    xs = list(d["ships"]["evals_per_orbit"]) + list(d["moons"]["evals_per_orbit"]) + list(d["res"]["evals_per_orbit"])
    return median(xs)

metrics = {}
for cfg in ["symba", "wh-fixed", "truth", "soi-switch"]:
    key = "truth" if cfg == "truth" else cfg
    je, nrise = jacobi_exponent(key)
    if cfg == "truth":
        cm, cm_n = 1.0, sum(1 for c in truth["moons_truth"]["class"] if c in (0, 1))
        pm, pm_n = 1.0, sum(1 for r in truth["moons_truth"]["rate"] if r is not None and r != 0)
        lr, lr_n = 1.0, 0
    else:
        cm, cm_n = class_match(cfg)
        pm, pm_n = prec_match(cfg)
        lr, lr_n = lib_ratio(cfg)
    metrics[cfg] = {
        "jacobi_exponent": round(je, 4),
        "class_match": round(cm, 4),
        "precession_match": round(pm, 4),
        "libration_ratio": round(lr, 4),
        "force_evals_per_orbit": round(force_evals(key), 1),
    }

with open(os.path.join(HERE, "metrics.json"), "w") as f:
    json.dump(metrics, f, indent=1)

# ---- report of everything the dossier quotes -------------------------------------
def detail(name):
    out = [f"== {name} =="]
    for cfg, m in metrics.items():
        out.append(f"  {cfg:10s} jacobi {m['jacobi_exponent']:+.3f}  class {m['class_match']:.4f}  "
                   f"prec {m['precession_match']:.4f}  lib {m['libration_ratio']:.3f}  evals/orbit {m['force_evals_per_orbit']:.0f}")
    t = truth["ships_truth"]
    out.append(f"ships: crossings {t['crossings']}")
    out.append(f"  converged {sum(t['converged'])}/16, truth exponents "
               + " ".join(f"{e:+.2f}" for e in t["err_exponent"]))
    for cfg in configs:
        d = configs[cfg]["ships"]
        out.append(f"  {cfg:10s} exponents " + " ".join(f"{e:+.2f}" for e in d["exponent"]))
        out.append(f"  {'':10s} max_err  " + " ".join(f"{m:.0e}" for m in d["max_err"]))
    tc = truth["moons_truth"]["class"]
    out.append(f"moons: bound {tc.count(0)} escape {tc.count(1)} chaotic {tc.count(2)} unconverged {tc.count(3)}; "
               f"rated {sum(1 for r in truth['moons_truth']['rate'] if r is not None)}")
    for cfg in configs:
        cm, cmn = class_match(cfg)
        pm, pmn = prec_match(cfg)
        out.append(f"  {cfg:10s} class {cm:.4f} of {cmn}, prec {pm:.4f} of {pmn}")
    tt = truth["res_truth"]
    lib = [i for i, j in enumerate(tt["kind_j"]) if j >= 0 and tt["converged"][i]
           and tt["excursion"][i] is not None and tt["excursion"][i] < 2 * math.pi
           and abs(tt["excursion"][i] - 2 * math.pi) > 0.2 * 2 * math.pi]
    circ = [i for i, j in enumerate(tt["kind_j"]) if j >= 0 and tt["converged"][i]
            and tt["excursion"][i] is not None and tt["excursion"][i] >= 2 * math.pi
            and abs(tt["excursion"][i] - 2 * math.pi) > 0.2 * 2 * math.pi]
    out.append(f"resonance: {len(lib)} librating, {len(circ)} circulating, "
               f"{sum(1 for c in tt['converged'] if not c)} not converged; borderline "
               f"{sum(1 for i, j in enumerate(tt['kind_j']) if j >= 0 and tt['excursion'][i] is not None and abs(tt['excursion'][i] - 2*math.pi) <= 0.2*2*math.pi)}")
    for cfg in configs:
        worst, n = lib_ratio(cfg)
        ratios = []
        for i in lib:
            e_c = configs[cfg]["res"]["excursion"][i]
            if e_c:
                r = e_c / tt["excursion"][i]
                ratios.append((min(r, 1 / r), tt["names"][i]))
        ratios.sort()
        out.append(f"  {cfg:10s} worst libration {worst:.3f} of {n}; worst 3: "
                   + "; ".join(f"{n_} {r:.2f}" for r, n_ in ratios[:3]))
    te = truth["ships_truth"]["evals_per_orbit"]
    out.append(f"truth's real force evals/orbit (ships): median {median(te):.0f}, max {max(te):.0f}")
    tre = truth["res_truth"]["evals_per_orbit"]
    out.append(f"truth's real force evals/orbit (resonant): median {median(tre):.0f}")
    return "\n".join(out)

with open(os.path.join(HERE, "report.txt"), "w") as f:
    f.write(detail("r10") + "\n")

# ---- picture: |dC_J/C_J| against time for three ships ----------------------------
SHIPS = ["0", "5", "10"]
colors = {"symba": "#0a7d33", "wh-fixed": "#c47a00", "soi-switch": "#b3261e", "truth": "#555555"}
series = {"truth": truth["ships_truth"]["err_series"]}
for cfg in ["symba", "wh-fixed", "soi-switch"]:
    series[cfg] = configs[cfg]["ships"]["err_series"]

W, H, PW, PH, M = 960, 360, 290, 260, 42
def xmap(i, frac):
    return M + i * (PW + 24) + frac * PW
def ymap(v):
    lv = math.log10(max(v, 1e-14))
    return M + PH - (min(max(lv, -14), -1.5) + 14) / 12.5 * PH

parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="Helvetica,Arial,sans-serif">',
         '<rect width="100%" height="100%" fill="white"/>',
         '<text x="24" y="24" font-size="15">r10: Jacobi drift |ΔC_J/C_J| of the compiled drift+kicks — three frozen ships, 200 planet periods</text>']
cross = truth["ships_truth"]["crossings"]
for i, ship in enumerate(SHIPS):
    ox = M + i * (PW + 24)
    parts.append(f'<rect x="{ox}" y="{M}" width="{PW}" height="{PH}" fill="#fafafa" stroke="#999"/>')
    for d in range(-14, 0):
        y = ymap(10.0 ** d)
        parts.append(f'<line x1="{ox}" y1="{y:.1f}" x2="{ox+PW}" y2="{y:.1f}" stroke="#e4e4e4"/>')
    for frac, lbl in [(0, "0"), (0.5, "100"), (1, "200")]:
        parts.append(f'<text x="{ox+frac*PW:.0f}" y="{M+PH+16}" font-size="11" text-anchor="middle" fill="#333">{lbl}</text>')
    for d in (-12, -9, -6, -3):
        parts.append(f'<text x="{ox-6}" y="{ymap(10.0**d)+4:.1f}" font-size="10" text-anchor="end" fill="#333">1e{d}</text>')
    for cfg, col in colors.items():
        pts = series[cfg][ship]
        step = max(1, len(pts) // 320)
        path = " ".join(f"{xmap(i, k/(len(pts)-1)):.1f},{ymap(pts[k]):.1f}" for k in range(0, len(pts), step))
        dash = ' stroke-dasharray="5,3"' if cfg == "truth" else ""
        parts.append(f'<polyline points="{path}" fill="none" stroke="{col}" stroke-width="1.4"{dash}/>')
    parts.append(f'<text x="{ox+PW/2:.0f}" y="{M-10}" font-size="12" text-anchor="middle">ship {ship} '
                 f'({cross[int(ship)]} SOI crossings)</text>')
    parts.append(f'<text x="{ox+8}" y="{M+14}" font-size="10" fill="#333">|ΔC_J/C_J|, log</text>')
lx = M
for cfg, col in colors.items():
    parts.append(f'<line x1="{lx}" y1="{H-16}" x2="{lx+22}" y2="{H-16}" stroke="{col}" stroke-width="2"/>')
    parts.append(f'<text x="{lx+27}" y="{H-12}" font-size="11">{cfg}</text>')
    lx += 130
parts.append(f'<text x="{M}" y="{H-12}" font-size="11" fill="#666">planet periods →</text>')
parts.append("</svg>")
with open(os.path.join(HERE, "picture.svg"), "w") as f:
    f.write("\n".join(parts))

print(json.dumps(metrics, indent=1))
