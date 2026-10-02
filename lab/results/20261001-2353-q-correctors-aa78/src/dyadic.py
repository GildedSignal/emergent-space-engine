import numpy as np, sys, json
sys.path.insert(0, ".")
import replica
from replica import *

exec(open("sweep1_defs.py").read())
out = {}
ref = [run_one("dkd", 10, m)[0] for m in range(4)]

# SABA2 with 12-bit dyadic coefficients (sum of drifts stays exactly 1):
replica.SABA_C[2] = [866 / 4096, 2364 / 4096]     # 0.21142578125, 0.5771484375
rows = [run_one("saba2", k, m)[0] for k in (2,) for m in range(4)]
out["saba2q_k2"] = rows
print("saba2q k=2:", ["%.3e" % r["rate"] for r in rows], ["%.3f" % r["emax"] for r in rows], flush=True)
replica.SABA_C[2] = [0.2113248654051871177454256097490212721762, 0.5773502691896257645091487805019574556476]

# whc3b with 12-bit dyadic corrector coefficients:
A1_, B31_ = replica.A1, replica.B31
replica.A1, replica.B31 = 1713 / 4096, -102 / 4096
rows = [run_one("whc3b", k, m)[0] for k in (3,) for m in range(4)]
out["whc3bq_k3"] = rows
print("whc3bq k=3:", ["%.3e" % r["rate"] for r in rows], ["%.3f" % r["emax"] for r in rows], flush=True)
replica.A1, replica.B31 = A1_, B31_

out["ref_dkd_k10"] = ref
json.dump(out, open("../dyadic.json", "w"), indent=1)
print("ref:", ["%.3e" % r["rate"] for r in ref], ["%.3f" % r["emax"] for r in ref])
print("saved")
