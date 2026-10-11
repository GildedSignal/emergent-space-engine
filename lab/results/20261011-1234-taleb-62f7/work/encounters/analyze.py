#!/usr/bin/env python3
"""Regenerate the tables/exponents in dossier.md from bulk.jsonl (deterministic, no network)."""
import json, math, sys

rows = [json.loads(l) for l in open(__file__.rsplit('/', 1)[0] + '/bulk.jsonl')]

def f(r, *keys):
    return " ".join(f"{k}={r[k]}" for k in keys)

print("== all scenes ==")
for r in rows:
    print(f(r, "scene", "n_a", "truth_cross", "truth_within", "tau_cross_per_ship",
             "p_pair_cross", "pred_total", "ratio_pred_truth", "lambda_gt0_frac",
             "frac_a_contact", "pred_per_active", "counts_per_active",
             "counts_var_over_mean", "corr_lambda_count", "cross_outside_window",
             "agg_evals", "truth_s", "load1"))

xs = [(r["n_a"], r["truth_cross"], r["tau_cross_per_ship"], r["p_pair_cross"]) for r in rows if r["scene"].startswith("x-")]
(n0, c0, _, _), (n1, c1, _, _) = xs[0], xs[-1]
exp = math.log(c1 / c0) / math.log(n1 / n0)
slopes = [math.log(b / a) / math.log(nb / na) for (na, a, _, _), (nb, b, _, _) in zip(xs, xs[1:])]
tau_slope = (xs[-1][2] - xs[0][2]) / (xs[-1][0] - xs[0][0])
p_at_800 = [x[3] for x in xs if x[0] == 800][0]

print("\n== laws ==")
print(f"contacts exponent vs n (endpoints n={n0}->{n1}): {exp:.3f}")
print(f"stepwise exponents: {[round(s,3) for s in slopes]}")
print(f"tau (contacts/A-ship/crossing) slope vs n_B: {tau_slope:.5f}  (= p_pair, linear)")
print(f"p_pair x-800: {p_at_800:.5f} -> contacts at 1e6/fleet: {p_at_800*1e12:.2e}")
print(f"tau at 1e6/fleet (measured slope): {tau_slope*1e6:.0f} contacts per A ship per crossing")

ws = [(r["scene"], r["truth_cross"], r["p_pair_cross"], r["counts_var_over_mean"]) for r in rows if r["scene"].startswith("w-")]
print("\n== width sweep (n=400 fixed) ==")
for w in ws:
    print(w)
print("w 0.5->0.03125 factor:", round(ws[-1][1] / ws[0][1], 2))

a = [(r["scene"], r["truth_cross"], r["cross_outside_window"], r["pred_total"], r["pred_total"] / (r["truth_cross"] - r["cross_outside_window"])) for r in rows if r["scene"].startswith("a-")]
print("\n== held-out angle (a=2.0, e=0.6), no refit ==")
for x in a:
    print(f"{x[0]}: truth_in_window={x[1]-x[2]} pred={x[3]:.0f} ratio_in_window={x[4]:.3f}")

belt = [r for r in rows if r["scene"].startswith("belt")][0]
print(f"\nbelt control: contacts/ship/orbit = {belt['contacts_per_ship_per_orbit']} (prediction P3 said < 0.05: MISSED)")
print("diagnosis: a radially-thin dense belt has ~0.4 discrete PAIRWISE conjunctions per ship per orbit;")
print("each loads 2 ships once. The crossing loads ~21% of ships with tau(n_B) contacts in ONE event,")
print("tau growing without bound in n_B (measured slope 0.021/ship): the separating quantity is")
print("per-event multiplicity (belt ~1; x-800: 75 per active ship), not per-orbit rate.")
