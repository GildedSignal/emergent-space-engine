#!/usr/bin/env python3
"""Parallel shard of the held-out runs. Usage: run_part.py <part>"""
import json
import os
import sys
import time

import numpy as np

import news

part = sys.argv[1]
out = {"part": part, "started": time.strftime("%Y-%m-%dT%H:%M:%S"),
       "loadavg": os.getloadavg(), "runs": {}}


def tag(name, res):
    out["runs"][name] = res
    print(name, "->", "PASS" if res["pass"] else "FAIL",
          f"pos={res['pos_err_final']:.2e} dE={res['dE_final']:+.2e} "
          f"work={res['work_true']:+.2e} ferr={res['field_rms_rel']:.2e}",
          flush=True)


if part == "A":
    for nb in (64, 1024):
        sc = news.make_scene(1, nb)
        tag(f"H1_nb{nb}", news.run_config(sc, 12.0, 0.1, 8.37, 2, 8, 32,
                                          quiet=True))
elif part == "B":
    sc = news.make_scene(3, 1024)
    tag("H2_l2", news.run_config(sc, 24.0, 0.2, 8.37, 2, 8, 32, quiet=True))
    tag("H2_l1", news.run_config(sc, 24.0, 0.2, 8.37, 1, 8, 32, quiet=True))
elif part == "C":
    sc = news.make_scene(2, 1024)
    tag("H3", news.run_config(sc, 12.0, 0.1, 8.37, 2, 8, 32, quiet=True))
    sc = news.make_scene(1, 256)
    tag("H4_4xwindow", news.run_config(sc, 12.0, 0.1, 32.37, 2, 8, 32,
                                       quiet=True))
    d = out["runs"]["H4_4xwindow"]["dist_traj"]
    d = out["runs"]["H4_4xwindow"]["dist_traj"]
    ts = (np.arange(1, len(d) + 1) / len(d)) * 32.37
    y = np.log(np.array(d))
    out["H4_growth_exponent"] = float(np.polyfit(np.log(ts), y, 1)[0])
    print("H4 exponent:", round(out["H4_growth_exponent"], 3), flush=True)
elif part == "D":
    sc = news.make_scene(4, 256, intruder=dict(a=0.12, e=0.4, m=0.3))
    tag("H5_rate8", news.run_config(sc, 12.0, 0.1, 8.37, 2, 8, 32,
                                    base_rate=64, quiet=True))
    tag("H5_rate32", news.run_config(sc, 12.0, 0.1, 8.37, 2, 32, 32,
                                     base_rate=64, quiet=True))

out["finished"] = time.strftime("%Y-%m-%dT%H:%M:%S")
with open(f"metrics_{part}.json", "w") as f:
    json.dump(out, f, indent=1)
print("PART", part, "DONE", flush=True)
