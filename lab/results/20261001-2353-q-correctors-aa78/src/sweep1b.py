import numpy as np, sys, json
sys.path.insert(0, ".")
from replica import *
exec(open("sweep1_defs.py").read())
res = json.load(open("../s1_partial.json")) if False else {}
out = {}
# reference k=10 (convergence to k=11 measured at 0.8%)
for kref in (10,):
    out[f"ref{kref}"] = [run_one("dkd", kref, m)[0] for m in range(4)]
for scheme in ("saba3", "whc3", "whc3b"):
    for k in (1, 2, 3, 4, 5):
        rows = [run_one(scheme, k, m)[0] for m in range(4)]
        out[f"{scheme}_k{k}"] = dict(kicks_per_orbit=KICKS_PER_STEP[scheme] * 2 ** k, moons=rows)
        print(scheme, k, ["%.3e" % r["rate"] for r in rows], ["%.3f" % r["emax"] for r in rows], flush=True)
tel = {}
for m in (1, 2):
    _, t3 = run_one("whc3", 3, m)
    _, tb = run_one("whc3b", 3, m)
    tel[f"moon{m}"] = float(np.max(np.abs(t3 - tb)) / am[m])
out["telescope"] = tel
print("telescoping maxdiff/a:", tel, flush=True)
json.dump(out, open("../s1_more.json", "w"), indent=1)
print("saved")
