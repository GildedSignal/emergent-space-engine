#!/usr/bin/env python3
"""Held-out extension: lambda=1.1 to t=400 on the same seed (predictions.md items 7-9)."""
import importlib.util, json
spec = importlib.util.spec_from_file_location("bs", "belt_scars.py")
bs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bs)
rows = bs.run(1.1, 1 << 18, seed=20261006, t_orbits=400, report_every=50)
out = [{"t": r[0], "scarred_frac": round(r[1], 3),
        "onetier_bits_per_body": round(r[4], 2),
        "twotier_bits_per_body": round(r[5], 2)} for r in rows]
json.dump(out, open("t400.json", "w"), indent=1)
print(out)
