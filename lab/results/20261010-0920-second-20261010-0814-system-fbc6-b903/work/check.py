#!/usr/bin/env python3
"""Renders every table in the dossier from the run's JSONs and grades the
held-out predictions. Run from this folder after accum.py d1|d1b|d2|e|equiv."""
import glob, json, math

D1 = json.load(open("run_d1.json"))
D1B = json.load(open("run_d1b.json"))
D2 = sum((json.load(open(p)) for p in sorted(glob.glob("run_d2_*.json"))), [])
E = json.load(open("run_e.json"))
EQ = json.load(open("equiv.json"))
SEP, R_SUB, R_P = 5.27e8, 3.65e7, 5.27e9

print("=== P1: the member-level wall (D1, real scene; 1.3e6 member news) ===")
for c in D1["cells"][:1]:
    mc = c["member_chain"]["checkpoints"]
    kf = [r["keep_forever"] for r in mc]
    rule = [r["death_at_arrival"] for r in mc]
    rsub = [r["ttl_Rsub"] for r in mc]
    little = c["member_chain"]["predicted_flatline_little"]
    print(f"  keep_forever {kf[0]} -> {kf[-1]} (linear wall)")
    print(f"  death-at-arrival flatline mean {sum(rule)/len(rule):.0f} "
          f"(Little {little:.0f}), no trend; starved at half-window: "
          f"{c['member_chain']['starved_folds_half']}")
    print(f"  ttl_R_sub mean {sum(rsub)/len(rsub):.0f} = "
          f"{(sum(rsub)/len(rsub))/(sum(rule)/len(rule)):.1f}x over-retention")

print("\n=== P2: the fleet at the parent, real parameters (D1) ===")
for c in D1["cells"]:
    print(f"  rq_agg={c['rq_agg']:.2e} (dx={c['dx']:.2e}): "
          f"{c['n_member_news']} member news -> {c['n_aggregate']} aggregate crossings")

print("\n=== P4: parent chain on accumulator-produced records (D1b, driven) ===")
c = D1B["cells"][0]
pc = c["parent_chain"]["checkpoints"]
kf = [r["keep_forever"] for r in pc]
rule = [r["ttl_rule"] for r in pc]
rpp = [r["ttl_R"] for r in pc]
half = [r["ttl_half"] for r in pc]
print(f"  {c['n_member_news']} news -> {c['n_aggregate']} aggregate; "
      f"rule flatline pred {c['predicted_parent_flatline']:.1f}")
print(f"  keep_forever {kf}")
print(f"  ttl_rule     {rule}  (misses {c['parent_chain']['misses']['ttl_rule']})")
print(f"  ttl_R_p      {rpp}  (misses {c['parent_chain']['misses']['ttl_R']})")
print(f"  half         {half}  (misses {c['parent_chain']['misses']['ttl_half']})")
m = sum(rule) / len(rule)
print(f"  ttl_R_p at run end {rpp[-1]} vs rule {rule[-1]}: over-retention "
      f"{rpp[-1]/rule[-1]:.0f}x (asymptote R_p/R_sub = {R_P/R_SUB:.0f}x, beyond t_end)")

print("\n=== P5: the doll-less thrusting giant (D1) ===")
for tag in ("rq_eq_Rp", "rq_Rp_third"):
    g = D1["giant"][tag]
    kf = [r["keep_forever"] for r in g["checkpoints"]]
    rule = [r["ttl_rule"] for r in g["checkpoints"]]
    print(f"  {tag}: pred flatline {g['predicted_flatline']:.1f}; "
          f"keep_forever {kf[0]}->{kf[-1]} (grows); rule {rule} (flat); "
          f"half-misses {g['misses']['ttl_half']}")

print("\n=== P3: lambda_agg exponents + stationarity (D2) ===")
for cell in D2:
    fit = cell["fit"]
    zs = [p["stationarity_z"] for p in cell["points"] if "stationarity_z" in p]
    zmax = max(abs(z) for z in zs) if zs else 0
    npts = len(zs)
    print(f"  {cell['process']:>8}/{cell['fold']}/order{cell['order']}: "
          f"fit {fit['exponent']:+.3f} vs pred {fit['predicted']:+.3f} "
          f"({fit['n_points']} pts) |z|max {zmax:.1f} "
          f"{'STATIONARY' if zmax <= 3 else 'NONSTATIONARY'}")

print("\n=== P6: the ghost question (E) ===")
print(f"  sub-quantum readers: {E['n_subquantum_readers']}/400")
print(f"  tubes mode: rule misses {E['tubes_misses']['ttl_rule']} "
      f"(all sub-quantum: {E['subquantum_missed_at_rule']}), "
      f"ttl_R misses {E['tubes_misses']['ttl_R']}")
a = E["aggregate"]
print(f"  aggregate mode: {a['n_publishes']} publishes, "
      f"misses at window R {a['misses']}, at half {a['misses_half_window']}")
print(f"  served-version error: max {a['max_version_error']:.1f} vs quantum "
      f"{E['dx_agg']:.0f} -> violations {a['quantum_violations']}")
print(f"  aggregate chain live {a['live_at_end']} vs lambda*R = "
      f"{E['lam'] * E['R']:.0f} (member tubes would hold)")

print("\n=== fold equivalence ===")
print(f"  {EQ}")

print("\n=== prediction verdicts ===")
v = []
c0 = D1["cells"][0]
mc = c0["member_chain"]["checkpoints"]
rule_m = sum(r["death_at_arrival"] for r in mc) / len(mc)
rsub_m = sum(r["ttl_Rsub"] for r in mc) / len(mc)
v.append(("P1 wall killed by fold", mc[-1]["keep_forever"] > 10 * rule_m > 100))
v.append(("P1 ttl_Rsub ~2x over", 1.4 <= rsub_m / rule_m <= 3.0))
v.append(("P2 rq<=sep: <=1 crossing", all(D1["cells"][i]["n_aggregate"] <= 1 for i in (0, 1))))
v.append((f"P2 rq=R_p: 10-25 crossings (measured {D1['cells'][2]['n_aggregate']})",
          10 <= D1["cells"][2]["n_aggregate"] <= 25))
c = D1B["cells"][0]
pc = c["parent_chain"]
v.append(("P4 rule zero misses", pc["misses"]["ttl_rule"] == 0))
v.append(("P4 half misses > 0", pc["misses"]["ttl_half"] > 0))
ratio = pc["checkpoints"][-1]["ttl_R"] / max(pc["checkpoints"][-1]["ttl_rule"], 1)
v.append((f"P4 ttl_R_p >= 5x rule at run end (measured {ratio:.0f}x, climbing to "
          f"R_p/R_sub=144x)", ratio >= 5))
g = D1["giant"]["rq_eq_Rp"]
gk = [r["keep_forever"] for r in g["checkpoints"]]
gr = [r["ttl_rule"] for r in g["checkpoints"]]
v.append(("P5 giant: level not slope", gk[-1] > 2 * gk[0] and max(gr) < 2.2 * g["predicted_flatline"]))
for cell in D2:
    fit, zs = cell["fit"], [p["stationarity_z"] for p in cell["points"] if "stationarity_z" in p]
    tag = f"P3 {cell['process']}/{cell['fold']}/o{cell['order']}"
    v.append((tag + " exponent", abs(fit["exponent"] - fit["predicted"]) <= 0.15))
    v.append((tag + " stationarity", (max(abs(z) for z in zs) <= 3) == (cell["order"] == 1 or cell["fold"] == "impulse")))
v.append(("P6 tubes: rule misses >0", E["tubes_misses"]["ttl_rule"] > 0))
v.append(("P6 agg: zero misses", E["aggregate"]["misses"] == 0))
v.append(("P6 agg: no quantum violation", E["aggregate"]["quantum_violations"] == 0))
v.append(("fold bit-identical", EQ["bit_identical"]))
for name, ok in v:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
print(f"\n  {sum(1 for _, ok in v if ok)}/{len(v)} predictions hold")
