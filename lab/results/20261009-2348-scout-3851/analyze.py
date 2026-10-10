#!/usr/bin/env python3
"""Score predictions P1-P7 against the held-out sweep."""
import json
import numpy as np

cases = []
for tag in ("e0", "e03", "e06"):
    cases += json.load(open(f"results-{tag}.json"))

def static_contains(r, b):
    se = r.get("static_edge")
    return se is not None and (b["center"] - b["half_width"]) < se + 0.05

def param_bands(r, law="truth", minpeak=0.0):
    return [b for b in r["bands"][law]
            if b["peak"] >= minpeak and not static_contains(r, b)]

def mu_in(r, law, lo, hi):
    om = np.array(r["Om_over_Om_r"]); mu = np.array(r["laws"][law])
    sel = (om >= lo) & (om <= hi)
    return float(mu[sel].max()) if sel.any() else 0.0

print("=== P1: band centers from the tide's own moments (2 w_eff = k Om_r)")
tot = match = 0; orphans = 0; worst = 0.0
for r in cases:
    if r["e"] == 0:
        continue
    for b in param_bands(r, minpeak=0.1):
        tot += 1
        preds = [p["center"] for p in r["predicted_centers"]]
        d = min(abs(b["center"] - p) for p in preds) if preds else 9e9
        worst = max(worst, d)
        if d <= 0.10:
            match += 1
        elif d > 0.15:
            orphans += 1
print(f"  matched {match}/{tot} within 0.10; orphans(>0.15) {orphans}; worst miss {worst:.3f}")

print("=== P2: averaging blind to pumping; keeps static edge")
bad = [r for r in cases if param_bands(r, "avg", 0.02)]
print(f"  avg parametric-band count nonzero in {len(bad)}/{len(cases)} cases (want 0)")
errs = []
for r in cases:
    se = r.get("static_edge")
    if se is None or not r["bands"]["truth"]:
        continue
    b0 = r["bands"]["truth"][0]
    edge = b0["center"] + b0["half_width"]
    errs.append(abs(edge - se) / se)
print(f"  avg static edge vs truth region edge: max rel err {max(errs):.3%} over {len(errs)} cases")

print("=== P3: cadence")
for law, ctol, ptol in (("hold32", 0.10, 0.25), ("kick32", 0.10, 0.25)):
    tb = pb = ob = 0; worst_p = 0.0
    for r in cases:
        for b in param_bands(r, minpeak=0.1):
            tb += 1
            law_bands = param_bands(r, law, 0.02)
            d = min((abs(x["center"] - b["center"]) for x in law_bands), default=9e9)
            pk = mu_in(r, law, b["center"] - b["half_width"], b["center"] + b["half_width"])
            pr = pk / b["peak"] if b["peak"] else 0
            if d <= ctol and abs(pr - 1) <= ptol:
                pb += 1
            elif d > ctol * 1.5:
                ob += 1
            worst_p = max(worst_p, abs(pr - 1))
    print(f"  {law}: matched {pb}/{tb}; badly off-center {ob}; worst peak-ratio err {worst_p:.0%}")
h4 = 0; h4tot = 0
for r in cases:
    if r["e"] != 0.6:
        continue
    for b in param_bands(r, minpeak=0.1):
        h4tot += 1
        pk = mu_in(r, "hold4", b["center"] - b["half_width"], b["center"] + b["half_width"])
        if b["peak"] and abs(pk / b["peak"] - 1) >= 0.30:
            h4 += 1
print(f"  hold4: peak off by >=30% on {h4}/{h4tot} e=0.6 band instances")
spur = miss = 0; tot1 = 0
for r in cases:
    if r["e"] == 0:
        continue
    tot1 += 1
    om = np.array(r["Om_over_Om_r"]); mu_t = np.array(r["laws"]["truth"])
    mu_1 = np.array(r["laws"]["hold1"])
    se = r.get("static_edge") or 0
    safe = om > se + 0.3
    if (mu_1[safe] >= 0.5).any() and (mu_t[safe] < 0.02).any():
        spur += 1
    big = param_bands(r, minpeak=1.0)
    if big and all(mu_in(r, "hold1", b["center"] - b["half_width"], b["center"] + b["half_width"]) < 0.5 for b in big):
        miss += 1
print(f"  hold1: qualitative failure in {spur + miss}/{tot1} eccentric cases "
      f"(spurious {spur}, missing {miss}; want >= 2/3 i.e. >= {2*tot1//3})")

print("=== P4: e = 0")
for r in cases:
    if r["e"] != 0:
        continue
    pb = len(param_bands(r, "truth", 0.02))
    dmu = max(abs(np.array(r["laws"][l]) - np.array(r["laws"]["truth"])).max()
              for l in ("avg", "hold32", "kick32"))
    print(f"  rp={r['rp']:>6} a={r['alpha']:+d}: parametric bands {pb}, "
          f"max law-vs-truth |dmu|/orbit {dmu:.4f} (static band {'yes' if r['bands']['truth'] else 'no'})")

print("=== P5: compressive channel at e=0.6")
c5 = [r for r in cases if r["e"] == 0.6 and r["alpha"] == -1]
n5 = sum(1 for r in c5 if any(b["peak"] >= 0.05 for b in r["bands"]["truth"]))
print(f"  alpha=-1 e=0.6 with a >=0.05/orbit truth band: {n5}/{len(c5)} (want >= 2)")

print("=== P6: bands reach the outermost moons (2.2-3.6 x Om_az)")
n6 = 0; tot6 = 0; det6 = []
for r in cases:
    if r["e"] == 0 or r["alpha"] != 1:
        continue
    tot6 += 1
    conv = 1.0 / r["az_over_Om_r"]  # Om_r/Om_az
    centers = [b["center"] * conv for b in param_bands(r, "truth", 0.05)]
    se = (r["static_edge"] or 0) * conv
    hit = any(2.2 <= c <= 3.6 for c in centers) or 2.2 <= se <= 3.6
    n6 += hit
    det6.append((r["rp"], r["e"], round(se, 2), [round(c, 2) for c in centers if 1.5 < c < 5]))
print(f"  hit in {n6}/{tot6} cases (want >= half). (rp, e, static_edge x Om_az, centers x Om_az):")
for d in det6:
    print("   ", d)

print("=== P7: relativistic widening")
for e in (0.3, 0.6):
    a = next(r for r in cases if r["rp"] == 10 and r["e"] == e and r["alpha"] == 1)
    b = next(r for r in cases if r["rp"] == 10000 and r["e"] == e and r["alpha"] == 1)
    Om2a, Om2b = a["Om_r"]**2, b["Om_r"]**2
    s_a = a["lam"]["amps"]["1"] / Om2a
    s_b = b["lam"]["amps"]["1"] / Om2b
    ea = a["static_edge"] / a["az_over_Om_r"]
    eb = b["static_edge"] / b["az_over_Om_r"]
    print(f"  e={e}: drive strength ratio rp10/rp1e4 = {s_a/s_b:.2f} (want >=1.4 at e=0.6); "
          f"static edge x Om_az: {ea:.2f} vs {eb:.2f} ratio {ea/eb:.2f} (want >=1.2)")
