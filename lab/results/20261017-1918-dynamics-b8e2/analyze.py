#!/usr/bin/env python3
"""Summarize the FLOW probe arms: lambda, mu, pin(m), the latch plateau, the budget bracket.
Every number in the dossier comes from here; run from lab/results/20261017-1918-dynamics-b8e2."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ARMS = os.path.join(HERE, "arms")

def load(name):
    rows = []
    for ln in open(os.path.join(ARMS, name + ".probe")):
        p = ln.strip().split(",")
        if p[0] == "PROBE" and p[1] == "f":
            rows.append(dict(gs=float(p[3]), held=int(p[4]), sin=int(p[5]), sout=int(p[6]), live=float(p[7]), allocs=float(p[8])))
    return rows

def settle(name):
    for ln in open(os.path.join(ARMS, name + ".probe")):
        p = ln.strip().split(",")
        if p[0] == "PROBE" and p[1] == "settle":
            return dict(gs=float(p[3]), held=int(p[4]), sin=int(p[5]), sout=int(p[6]), live=float(p[7]), allocs=float(p[8]))
    return None

def at(rows, gs):
    return min(rows, key=lambda r: abs(r["gs"] - gs))

def slope_lambda(rows, g0, g1):
    a, b = at(rows, g0), at(rows, g1)
    return (b["sin"] - a["sin"]) / (b["gs"] - a["gs"])

def pin(loaded, quiet, held_min=6):
    L = [r for r in loaded if r["held"] >= held_min]
    g0, g1 = L[0]["gs"], L[-1]["gs"]
    h0, h1 = L[0]["held"], L[-1]["held"]
    dl = L[-1]["live"] - L[0]["live"]
    dq = at(quiet, g1)["live"] - at(quiet, g0)["live"]
    raw = dl / (h1 - h0)
    return dict(window=[g0, g1], held=[h0, h1], d_loaded_MB=dl / 1e6, d_quiet_MB=dq / 1e6,
                pin_kB=(dl - dq) / (h1 - h0) / 1e3, raw_pin_kB=raw / 1e3, lam=slope_lambda(loaded, g0, g1))

out = {}

# lambda and mu per arm (growth phase = whole flight for f-lines)
for name in ["a100-load6", "a200-load6", "a400-load6", "a2s2-m400-load6", "a400-quiet", "l1-m400-load6-backlog256"]:
    rows = load(name)
    lam = slope_lambda(rows, rows[0]["gs"], rows[-1]["gs"])
    mu = (rows[-1]["sout"] - rows[0]["sout"]) / max(1e-9, rows[-1]["sin"] - rows[0]["sin"])
    out[name] = dict(lambda_per_gs=round(lam, 5), mu_over_lambda=round(mu, 3),
                     max_held=max(r["held"] for r in rows), presented_gs=rows[-1]["gs"])

# pin(m), quiet-subtracted over the same game-time window
for m in (100, 200, 400):
    out[f"pin_m{m}"] = {k: (round(v, 4) if isinstance(v, float) else v) for k, v in
                        pin(load(f"a{m}-load6"), load(f"a{m}-quiet")).items()}
import math, sys
p1, p4 = out["pin_m100"]["pin_kB"], out["pin_m400"]["pin_kB"]
if p1 <= 0 or p4 <= 0:
    sys.exit(f"VOID: quiet-subtracted pin(m) non-positive (pin100={p1:.1f} kB, pin400={p4:.1f} kB); "
             "the quiet arm was itself under external load (shared machine), so the subtraction is invalid — rerun in a quieter window")
out["pin_exponent_100_to_400"] = round(math.log(p4 / p1) / math.log(4), 3)
out["plateau_at_shipped_cap_GB"] = {f"m{m}": round(2048 * out[f"pin_m{m}"]["pin_kB"] / 1e6, 3) for m in (100, 200, 400)}

L2 = load("l2-m400-load6-backlog48")
cap = next(r for r in L2 if r["held"] >= 47)
pre = at(L2, cap["gs"] - 40)
post = L2[-1]
out["latch"] = dict(cap=48, engaged_at_gs=cap["gs"],
                    growth_rate_per_gs=round((cap["held"] - pre["held"]) / (cap["gs"] - pre["gs"]), 4),
                    held_after_3188_more_gs=post["held"], presented_after_cap_gs=round(post["gs"] - cap["gs"], 1),
                    scans_out_growth_phase=pre["sout"], scans_out_at_end=post["sout"],
                    live_MB_at_engagement=round(cap["live"] / 1e6, 2), live_MB_at_end=round(post["live"] / 1e6, 2),
                    live_MB_max_after_cap=round(max(r["live"] for r in L2 if r["gs"] >= cap["gs"]) / 1e6, 2))

# digest equality: quiet vs load6, same cut (a1 vs a2, m400 rtf100 s30)
dg = [json.load(open(os.path.join(ARMS, f + ".json")))["digest"] for f in ["a1-m400-quiet", "a2-m400-load6"]]
out["digest_quiet_equals_load6"] = dg[0] == dg[1]
out["digest"] = dg[0]
# budget bracket + pace arm: max held and service fraction
for name in ["e12-m400-load6", "e16-m400-load6", "r1-m400-quiet-rtf600"]:
    rows = load(name)
    out[name] = dict(max_held=max(r["held"] for r in rows), presented_gs=rows[-1]["gs"],
                     scans_in_end=rows[-1]["sin"], scans_out_end=rows[-1]["sout"],
                     engine_ms=json.load(open(os.path.join(ARMS, name + ".json")))["engine_budget_ms"])

print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1)
