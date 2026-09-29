"""Criteria 2 + 5: precession vs elliptic oracle at p=20 and p=1000 (both e),
and events per orbit (steps + shell crossings) at p=20, 100, 1000.
KILL(prec): no eta <= 1/32 within 1% at both p.  KILL(cost): > 512 events/orbit.
Usage: run_precession.py CFG [CFG...]"""
import sys, json, time
import gv1b as G

cfgs = sys.argv[1:]
t0 = time.perf_counter()
rows = []
for cfg in cfgs:
    plan = ([(20.0, 24), (100.0, 30), (1000.0, 120)] if cfg != "C3"
            else [(20.0, 24), (100.0, 12), (1000.0, 8)])
    maxfact = 120.0 if cfg != "C3" else 4000.0
    print(f"== {cfg}: precession (vs oracle) and events/orbit ==")
    print(f"{'p':>7} {'e':>4} {'eta':>7} {'ord':>3} {'orb':>4} {'rel_err':>10} "
          f"{'ev/orb':>8} {'cr/orb':>7} {'E_drift':>10}")
    for (p, K) in plan:
        for e in (0.2, 0.5):
            agr = G.periapsis_advance_gr(p, e)
            for eta in (1/16, 1/32, 1/64):
                for order in (2, 4):
                    r = G.run_bound(cfg, order, eta, p, e, K, maxfact=maxfact)
                    rel = abs(r["advance"] - agr)/agr
                    cro = r["crossings"]/max(r["n_orbits"], 1)
                    rows.append({
                        "cfg": cfg, "order": order, "eta": eta, "p": p, "e": e,
                        "rel": rel, "advance": r["advance"], "agr": agr,
                        "ev_per_orbit": r["events_per_orbit"], "cr_per_orbit": cro,
                        "K": r["n_orbits"], "E_drift": r["E_drift"],
                    })
                    print(f"{p:7.0f} {e:4.1f} {eta:7.4f} {order:3d} {r['n_orbits']:4d} "
                          f"{rel:10.2e} {r['events_per_orbit']:8.1f} {cro:7.2f} "
                          f"{r['E_drift']:10.2e}")
print("== eta-convergence slopes of the precession error (expect ~order) ==")
import math
for cfg in cfgs:
    for (p, e) in [(20.0, 0.2), (20.0, 0.5), (1000.0, 0.2), (1000.0, 0.5)]:
        for order in (2, 4):
            pts = [(math.log(rrow["eta"]), math.log(rrow["rel"])) for rrow in rows
                   if rrow["cfg"] == cfg and rrow["order"] == order
                   and rrow["p"] == p and rrow["e"] == e]
            if len(pts) == 3:
                (x1, y1), (x2, y2), (x3, y3) = sorted(pts)
                sl = (y3 - y1)/(x3 - x1)
                print(f"  {cfg} p={p:.0f} e={e} o{order}: slope={sl:.2f}")
with open("results_prec.jsonl", "a") as f:
    for rrow in rows:
        f.write(json.dumps(rrow) + "\n")
print(f"wall: {time.perf_counter()-t0:.1f} s")
