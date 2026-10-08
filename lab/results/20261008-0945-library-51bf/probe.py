#!/usr/bin/env python3
"""Probe: does any single recorded dimensionless number order the per-seed minimum
kick cadence on quant-5022's published data? Gates copied verbatim from that run's
verdict.py (apsis 10%, emax 1.2x, maxdJ 10x of its 64-cadence control)."""
import json, re, itertools

BASE = "data/"

def rows_from(fname, seed_by_letter=None):
    rows = {}
    for ln in open(BASE + fname):
        ln = ln.strip()
        m = re.match(r'"seed":"(\w+)",(.*)', ln)
        if m:
            d = json.loads(m.group(2)); key = m.group(1)
        else:
            try: d = json.loads(ln)
            except json.JSONDecodeError: continue  # "rebind guard" lines
            key = None
        cfg = (round(d["a0"], 4), round(d["e0"], 4), round(d["mu"], 8))
        rows.setdefault(cfg, {})[(d["method"], d["steps"])] = d
        if key: seed_by_letter[key] = cfg
    return rows

letters = {}
dec = rows_from("quant-5022-decisive.jsonl", letters)
tun = rows_from("quant-5022-tuning.jsonl", letters)
allrows = {**tun, **dec}

NAME = {  # from quant-5022's dossier/check
 "T1": (0.55, 0.05, 1e-3), "T2": (0.70, 0.20, 1e-3), "T3": (1.70, 0.05, 1e-3),
 "H1": (0.62, 0.30, 1e-3), "H2": (0.48, 0.10, 3e-4), "H5": (0.55, 0.60, 1e-3)}
# verify letter->config map from decisive.jsonl itself
letters = {**{n: cfg for n, cfg in NAME.items() if n.startswith("T")}, **letters}
inv = {v: k for k, v in letters.items()}
for n, cfg in NAME.items():
    assert inv.get(cfg) == n, (n, cfg, inv.get(cfg))

def passes(cfg, k):
    r = allrows[cfg][("kdk", 1024)]; c = allrows[cfg].get(("kdk", 64))
    d = allrows[cfg].get(("kdk", k))
    if not d or not c: return None
    dom = abs(d["domdt"] - r["domdt"]) <= 0.10 * abs(r["domdt"])
    em = d["emax"] <= max(1.2 * r["emax"], 1.2 * d["e0"] + 0.02)
    jd = d["maxdJ"] <= 10 * c["maxdJ"]
    return dom and em and jd

mins = {}
for n, cfg in NAME.items():
    for k in (2, 4, 8, 16, 32, 64):  # climb from the bottom: first pass = true minimum
        if passes(cfg, k) is True:
            mins[n] = k; break
    else:
        mins[n] = None  # nothing at or below 64 passes

print(f"{'seed':4} {'a0':>5} {'e0':>5} {'mu':>8} {'min_cadence':>11}")
for n, cfg in NAME.items():
    print(f"{n:4} {cfg[0]:5.2f} {cfg[1]:5.2f} {cfg[2]:8.1e} {mins[n]:>11}")

alive = [n for n in NAME if mins[n]]
tot_min = sum(mins[n] for n in alive); tot_uni = 64 * len(alive)
print(f"\nP1 ceiling: per-body minimums sum {tot_min} vs uniform {tot_uni} "
      f"-> best possible gain {tot_uni/tot_min:.2f}x on these {len(alive)} seeds")

def spearman(xs, ys):
    def rank(v):
        s = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0]*len(v); i = 0
        while i < len(s):
            j = i
            while j+1 < len(s) and v[s[j+1]] == v[s[i]]: j += 1
            for t in range(i, j+1): r[s[t]] = (i + j)/2 + 1
            i = j + 1
        return r
    rx, ry = rank(xs), rank(ys); mx, my = sum(rx)/len(rx), sum(ry)/len(ry)
    num = sum((a-mx)*(b-my) for a, b in zip(rx, ry))
    den = (sum((a-mx)**2 for a in rx) * sum((b-my)**2 for b in ry)) ** 0.5
    return num/den if den else float('nan')

sensors = {"e0": lambda c: c[1], "a0": lambda c: c[0], "mu": lambda c: c[2],
           "mu*e0": lambda c: c[2]*c[1], "a0*e0": lambda c: c[0]*c[1]}
print("\nP2 sensor ordering (Spearman rho of sensor vs min cadence):")
for sname, f in sensors.items():
    xs = [f(NAME[n]) for n in alive]; ys = [mins[n] for n in alive]
    print(f"  {sname:6} rho = {spearman(xs, ys):+.2f}")

# P3: e0 ladder fitted on T1/T2/T3 only, predict H1/H2/H5 (and in-sample fit quality)
fit = ["T1", "T2", "T3"]; held = ["H1", "H2", "H5"]
def ladder_rate(e0, cuts):
    r = 8
    for cut, up in cuts:          # up: multiplier applied when e0 >= cut
        if e0 >= cut: r = up
    return r
# grid of monotone cuts on e0 from tuning seeds' own minima
tuned = sorted((NAME[n][1], mins[n]) for n in fit)
cuts, last = [], None
for e0, mk in tuned:
    if mk != last: cuts.append((e0, mk)); last = mk
print(f"\nP3 ladder fitted on tuning seeds (e0 thresholds -> rate): {cuts}")
miss = 0
for n in fit + held:
    pred = ladder_rate(NAME[n][1], cuts); act = mins[n]
    steps = abs(__import__('math').log2(pred) - __import__('math').log2(act))
    miss += steps > 1
    print(f"  {n}: predicted {pred}, actual {act}  ({'OK' if steps <= 1 else 'MISS >1 step'})")
print(f"P3: {'HELD (all within one ladder step)' if miss == 0 else f'{miss} seed(s) miss by >1 step'}")

out = {"mins": mins, "uniform": 64, "gain_ceiling": tot_uni/tot_min,
       "spearman": {s: spearman([f(NAME[n]) for n in alive], [mins[n] for n in alive])
                    for s, f in sensors.items()},
       "ladder": {"cuts": cuts, "held_out_misses": miss}}
json.dump(out, open("metrics.json", "w"), indent=1)
print("\nwrote metrics.json")
