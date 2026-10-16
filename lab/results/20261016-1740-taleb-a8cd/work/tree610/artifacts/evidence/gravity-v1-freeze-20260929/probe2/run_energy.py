"""Criterion 1 (energy): growth exponent of |dE| over 10^4 orbits at p=20,
fitted over [10^3, 10^4]; KILL if exponent > 0.2 or max|dE/E| > 1e-6.
Usage: run_energy.py CFG ORDER ETA E KORBITS   (ETA like 1/16)"""
import sys, json, time
import gv1b as G

cfg = sys.argv[1]
order = int(sys.argv[2])
eta = eval(sys.argv[3])
e = float(sys.argv[4])
K = int(sys.argv[5])

t1 = time.perf_counter()
r = G.run_bound(cfg, order, eta, 20.0, e, K)
wall = time.perf_counter() - t1
slope = G.fit_slope(r["samples"], 1000, min(10000, r["n_orbits"]))
marks = [10, 100, 1000, 5000, 10000]
idx = {}
for k_, m_ in r["samples"]:
    for mk in marks:
        if k_ - 10 < mk <= k_:
            idx[mk] = m_
verdict = "PASS" if (slope <= 0.2 and r["max_dE"] <= 1e-6) else "KILL"
out = {
    "cfg": cfg, "order": order, "eta": eta, "e": e, "K": r["n_orbits"],
    "slope": round(slope, 4), "max_dE": r["max_dE"], "verdict": verdict,
    "E_drift": r["E_drift"], "L_drift": r["L_drift"],
    "steps_per_orbit": round(r["steps_per_orbit"], 1),
    "cross_per_orbit": round(r["crossings"]/max(r["n_orbits"], 1), 2),
    "wall": round(wall, 1),
}
tab = "  ".join(f"n={mk}:{idx.get(mk, float('nan')):.2e}" for mk in marks if mk <= r["n_orbits"])
print(f"{cfg} o{order} eta={eta:.5f} e={e}: orbits={r['n_orbits']} "
      f"max|dE/E|={r['max_dE']:.3e} slope[{slope:.3f}] {verdict}  [{wall:.1f} s]")
print(f"   {tab}")
print(f"   E_drift={r['E_drift']:.2e} L_drift={r['L_drift']:.2e} "
      f"steps/orbit={r['steps_per_orbit']:.0f} cross/orbit={out['cross_per_orbit']}")
with open("results_energy.jsonl", "a") as f:
    f.write(json.dumps(out) + "\n")
