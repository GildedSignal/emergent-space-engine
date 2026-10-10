#!/usr/bin/env python3
"""Held-out decisive runs H1-H5; writes metrics.json."""
import json
import os
import time

import numpy as np

import news

t0 = time.time()
out = {"started": time.strftime("%Y-%m-%dT%H:%M:%S"),
       "loadavg_start": os.getavgsize if False else os.getloadavg(),
       "runs": {}}


def tag(name, res):
    out["runs"][name] = res
    print(name, "->", "PASS" if res["pass"] else "FAIL",
          f"pos={res['pos_err_final']:.2e} dE={res['dE_final']:+.2e} "
          f"work={res['work_true']:+.2e} ferr={res['field_rms_rel']:.2e} "
          f"vac={res['vacuous']}", flush=True)


# H1: body-count scaling, config frozen at (2, 8, 32)
for nb in (64, 1024):
    sc = news.make_scene(1, nb)
    tag(f"H1_nb{nb}", news.run_config(sc, 12.0, 0.1, 8.37, 2, 8, 32,
                                      quiet=True))

# H2: distance grading at D=24
sc = news.make_scene(3, 1024)
tag("H2_l2", news.run_config(sc, 24.0, 0.2, 8.37, 2, 8, 32, quiet=True))
tag("H2_l1", news.run_config(sc, 24.0, 0.2, 8.37, 1, 8, 32, quiet=True))

# H3: independent seed
sc = news.make_scene(2, 1024)
tag("H3", news.run_config(sc, 12.0, 0.1, 8.37, 2, 8, 32, quiet=True))

# H4: 4x window, error type
sc = news.make_scene(1, 256)
tag("H4_4xwindow", news.run_config(sc, 12.0, 0.1, 32.37, 2, 8, 32,
                                   quiet=True))
d = out["runs"]["H4_4xwindow"]["dist_traj"]
ts = np.linspace(0, 32.37, len(d))
m = np.array(d) > 0
exponent = float(np.polyfit(np.log(ts[m]), np.log(np.array(d)[m]), 1)[0])
out["H4_growth_exponent"] = exponent
print("H4 dist growth exponent:", round(exponent, 3), flush=True)

# H5: fast heavy intruder, base rate 64
sc = news.make_scene(4, 256, intruder=dict(a=0.12, e=0.4, m=0.3))
tag("H5_rate8", news.run_config(sc, 12.0, 0.1, 8.37, 2, 8, 32,
                                base_rate=64, quiet=True))
tag("H5_rate32", news.run_config(sc, 12.0, 0.1, 8.37, 2, 32, 32,
                                 base_rate=64, quiet=True))

out["finished"] = time.strftime("%Y-%m-%dT%H:%M:%S")
out["loadavg_end"] = os.getloadavg()
out["wall_s"] = round(time.time() - t0, 1)
with open("metrics.json", "w") as f:
    json.dump(out, f, indent=1)
print("DONE", out["wall_s"], "s", flush=True)
