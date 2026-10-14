#!/usr/bin/env python3
"""Regenerate triples.rs from a game3d-enc.jsonl dump (c7eb dumper format).

Each dumped truth encounter: d (closest approach, AU), vrel, ai (kicked body's a),
cospsi_i = v_i · b̂. Stored dimensionless: (d/a_i, v_rel/v_circ(a_i), cos_psi_i).
Usage: extract.py <dump.jsonl> <out.rs>
"""
import json
import math
import sys

rows = [json.loads(l) for l in open(sys.argv[1])]
trip = [(r["d"] / r["ai"], r["vrel"] * math.sqrt(r["ai"]), r["cospsi_i"]) for r in rows]
with open(sys.argv[2], "w") as f:
    f.write(
        "/// Measured conjunction geometry, %d game-density truth encounters (c7eb gold run,\n"
        "/// game3d-planar: n=2000, sigma_e=0.1, rho=1e-4 AU, a in [2.45,2.95], 50 orbits).\n"
        "/// Each row: (d/a_i, v_rel/v_circ(a_i), cos_psi_i = v_i . b_hat).\n"
        "pub const TRIPLES: [(f64, f64, f64); %d] = [" % (len(trip), len(trip))
    )
    for a, b, c in trip:
        f.write("(%r,%r,%r)," % (a, b, c))
    f.write("];\n")
print("wrote %d triples" % len(trip))
