#!/usr/bin/env python3
"""Assemble metrics.json for rung r3 v2 from r3 outputs. Run from the run folder."""
import csv, json, math, re, sys

# ---------------- binaries ----------------
rows = list(csv.DictReader(open("bin.csv")))
def f(r, k): return float(r[k])
judged_p = judged_T = judged_n = 0
pass_frac = {c: {"prec": [0, 0], "period": [0, 0], "nu": [0, 0]} for c in ("eob", "test", "newton")}
cols = {"eob": ("Aeob", "Peob", "Peob"), "test": ("Atm", "Ptm", "Ptm"), "newton": ("Anw", "Pnw", "Pnw")}
resid = []
for r in rows:
    p, e, nu = f(r, "p"), f(r, "e"), f(r, "nu")
    Aor, Por, Por0 = f(r, "Aor"), f(r, "Por"), f(r, "Por0")
    epsp, epsT, epsn = f(r, "epsp"), f(r, "epsT"), f(r, "epsn")
    if epsp <= 0.005:
        judged_p += 1
        for c, (ca, _, _) in cols.items():
            pass_frac[c]["prec"][1] += 1
            if abs(f(r, ca) - Aor) <= 0.01 * abs(Aor): pass_frac[c]["prec"][0] += 1
    if epsT <= 5e-4:
        judged_T += 1
        for c, (_, cp, _) in cols.items():
            pass_frac[c]["period"][1] += 1
            if abs(f(r, cp) - Por) <= 1e-3 * Por: pass_frac[c]["period"][0] += 1
    if nu >= 0.05 and epsn <= 0.05:
        judged_n += 1
        dP_or = Por - Por0
        for c, (_, _, cp) in cols.items():
            pass_frac[c]["nu"][1] += 1
            # each config's own nu=0 limit: eob's exact test-mass map; test-mass and
            # newton have no nu-dependence, so their baseline is their own value
            base = {"eob": f(r, "Peob0"), "test": f(r, "Ptm"), "newton": f(r, "Pnw")}[c]
            dP = f(r, cp) - base
            if dP * dP_or > 0 and abs(dP - dP_or) <= 0.1 * abs(dP_or): pass_frac[c]["nu"][0] += 1
    resid.append((p, e, nu, (f(r, "Aeob") - Aor) / Aor, (f(r, "Peob") - Por) / Por))

def frac(a, b): return a / b if b else 0.0

# ---------------- transfer ----------------
def transfer_metrics(fn):
    ev, summ = [], None
    for line in open(fn):
        if line.startswith("SUMMARY"):
            summ = line.split()
        elif line.startswith("EV"):
            _, k, t, ed, er = line.split()
            ev.append((int(k), float(t), float(ed), float(er)))
    if summ is None: return None
    d = {summ[i]: summ[i + 1] for i in range(1, len(summ) - 1, 2)}
    ncross, nh = int(d["crossings"]), int(d["handoffs"])
    t_end = float(d["t_ref_end"])
    n_orb = t_end / (2 * math.pi)
    ks = [k for k, _, _, _ in ev]
    errs = [abs(ed - er) for _, _, ed, er in ev]
    if len(errs) >= 3:
        n = len(errs)
        mx = sum(math.log(k) for k in ks) / n
        my = sum(math.log(max(e, 1e-300)) for e in errs) / n
        alpha = sum((math.log(k) - mx) * (math.log(max(e, 1e-300)) - my) for k, e in zip(ks, errs)) / \
                sum((math.log(k) - mx) ** 2 for k in ks)
    else:
        alpha = 0.0
    evs = [nh / n_orb, ncross / n_orb, 0.0]
    evs.sort()
    return {"exponent": alpha, "events_per_orbit": evs[1], "ncross": ncross, "nh": nh,
            "t_end": t_end, "n": len(errs), "err_last": errs[-1] if errs else None,
            "halfstep": d.get("halfstep", "n/a")}

tr = {c: transfer_metrics("tr_law%d.txt" % i) for i, c in enumerate(("eob", "test", "newton"))}

# ---------------- flybys ----------------
def flyby_metrics(fn):
    tot = ok = 0
    worst = 0.0
    for line in open(fn):
        if not line.startswith("FB"): continue
        d = line.split()
        i = d.index("dv_doll")
        dvx, dvy = float(d[i + 1]), float(d[i + 2])
        j = d.index("dv_ref")
        rvx, rvy = float(d[j + 1]), float(d[j + 2])
        dv = math.hypot(dvx, dvy); rv = math.hypot(rvx, rvy)
        tot += 1
        rel = math.hypot(dvx - rvx, dvy - rvy) / rv if rv > 0 else float("inf")
        if rel <= 0.01: ok += 1
        worst = max(worst, rel)
    return ok, tot, worst

fb = {c: flyby_metrics("fb_law%d.txt" % i) for i, c in enumerate(("eob", "test", "newton"))}

# ---------------- assemble ----------------
metrics = {}
for c in ("eob", "test", "newton"):
    name = {"eob": "eob-doll", "test": "test-mass", "newton": "newton-doll"}[c]
    okp, tp = pass_frac[c]["prec"]; okT, tT = pass_frac[c]["period"]; okn, tn = pass_frac[c]["nu"]
    okf, tf, worst = fb[c]
    metrics[name] = {
        "precession_pass_fraction": round(frac(okp, tp), 6),
        "period_pass_fraction": round(frac(okT, tT), 6),
        "nu_effect_pass_fraction": round(frac(okn, tn), 6),
        "min_judged_seeds": min(judged_p, judged_T, judged_n),
        "handoff_energy_growth_exponent": round(tr[c]["exponent"], 4),
        "assist_pass_fraction": round(frac(okf, tf), 6),
        "events_per_orbit": round(tr[c]["events_per_orbit"], 4),
    }
json.dump(metrics, open("metrics.json", "w"), indent=1)

print("judged: prec %d, period %d, nu %d" % (judged_p, judged_T, judged_n))
for c in metrics: print(c, metrics[c])
print("transfer:", {c: {k: tr[c][k] for k in ('ncross', 'n', 'exponent', 'err_last', 'halfstep')} for c in tr})
print("flyby worst rel err:", {c: fb[c][2] for c in fb})
# residual family for the dossier
import statistics
buckets = {}
for p, e, nu, ra, rT in resid:
    buckets.setdefault(int(p // 100), []).append((p * ra if False else ra * p, rT * p / (1 - e * e) ** 1.5 * (1 - e * e) ** 0))
for b in sorted(buckets):
    v = buckets[b]
    print("p-bucket %d00: n=%d  C_adv=%.2f" % (b, len(v), statistics.median(x[0] for x in v)))
