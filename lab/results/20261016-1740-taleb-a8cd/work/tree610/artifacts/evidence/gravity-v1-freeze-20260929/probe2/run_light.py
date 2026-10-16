"""Criterion 3 (distant light): photon anchored at r0=1e4, b=10 and b=30,
integrated to r=1e5 outgoing; deflection vs exact oracle with analytic
finite-radius tails at both ends.  KILL if > 1% off.
Usage: run_light.py CFG [CFG...]"""
import sys, json, time
import gv1b as G

cfgs = sys.argv[1:]
t0 = time.perf_counter()
rows = []
for cfg in cfgs:
    print(f"== {cfg}: distant light, r0=1e4 -> r_exit=1e5 ==")
    print(f"{'b':>6} {'eta':>7} {'ord':>3} {'delta':>11} {'oracle':>11} {'rel_err':>10} "
          f"{'steps':>7} {'cross':>6} {'b_drift':>10}")
    for b in (10.0, 30.0):
        agr = G.deflection_gr(b)
        for eta in (1/16, 1/32, 1/64):
            for order in (2, 4):
                d, ev, cr, ab, bdr = G.run_photon_r0(cfg, order, eta, b)
                rel = abs(d - agr)/agr
                rows.append({
                    "cfg": cfg, "order": order, "eta": eta, "b": b,
                    "delta": d, "agr": agr, "rel": rel, "steps": ev,
                    "cross": cr, "b_drift": bdr, "absorbed": ab,
                })
                print(f"{b:6.1f} {eta:7.4f} {order:3d} {d:11.7f} {agr:11.7f} "
                      f"{rel:10.2e} {ev:7d} {cr:6d} {bdr:10.1e}"
                      + ("  ABSORBED!" if ab else ""))
with open("results_light.jsonl", "a") as f:
    for rrow in rows:
        f.write(json.dumps(rrow) + "\n")
print(f"wall: {time.perf_counter()-t0:.1f} s")
