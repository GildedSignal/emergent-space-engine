import json
import numpy as np
import exp

out = []
for N in (512, 2048, 8192):
    sc = exp.mk_fleet(N, 1e-3, arc=0.5, seed=40)
    for name, fn in (("cone-only", lambda s: s.cone_only()), ("unified", lambda s: s.unified())):
        cand, st = fn(sc)
        out.append({"scene": "fleet", "N": N, "method": name, "cand": len(cand), **st})
for N in (2500, 5000):
    sc = exp.mk_belt(N, seed=41)
    for name, fn in (("cone-only", lambda s: s.cone_only()), ("unified", lambda s: s.unified())):
        cand, st = fn(sc)
        out.append({"scene": "belt", "N": N, "method": name, "cand": len(cand), **st})
for r in out:
    print(json.dumps(r))
