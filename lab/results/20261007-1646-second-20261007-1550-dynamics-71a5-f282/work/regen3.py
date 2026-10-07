#!/usr/bin/env python3
"""Regenerate the author's results3 record from shipped code, with the corrected column.

The stored results3.json's third column is t_cross = 0.0269/om (the NEAR-side travel), but
the run direction (body j at Om = -om) travels the FAR tangency: t_tang = 1.426924/om. The
author's dossier text is correct; the stored column and the 3-field reproduce snippet are
not (both checkers flagged this). This script regenerates the full 4-column record from the
truth files computed by jobs.py (same instrument, same grid) and verifies the realized-event
column bit-for-bit against the stored one.
"""
import json
import math
import os

from cert import TAU, body

HERE = os.path.dirname(os.path.abspath(__file__))
TR = os.path.join(HERE, "truth")
nn = lambda a: a ** -1.5
G4N = (body(1.0, 0.30, 0.3, nn(1.0)), body(0.8, 0.30, 1.00, nn(0.8)))
RHO = 0.004

pi_, pj_ = (b["a"] * (1 - b["e"] ** 2) for b in G4N)
Vi, Vj = G4N[0]["e"] / pi_, G4N[1]["e"] / pj_
dU = abs(1 / pi_ - 1 / pj_)
dstar = math.acos((Vi * Vi + Vj * Vj - dU * dU) / (2 * Vi * Vj))
travel_far = (G4N[1]["pom"] - G4N[0]["pom"]) + dstar
travel_near = dstar - (G4N[1]["pom"] - G4N[0]["pom"])


def main():
    orig = json.load(open(os.path.join(HERE, "results3.orig.json")))
    tags = {5e-4: "0.0005", 1e-3: "0.001", 2e-3: "0.002"}
    rows, bad = [], []
    for (om, k, t_cross_near_stored, first_stored) in orig:
        mins = json.load(open(os.path.join(TR, f"regen_{tags[om]}_k{k}.json")))["mins"]
        first = next((t for (t, d) in mins if d < RHO), None)
        if first != first_stored:
            bad.append((om, k, first_stored, first))
        rows.append([om, k, travel_far / om, first])
    rec = dict(
        note="regenerated 2026-10-07 by regen3.py (second-author run f282); columns "
             "[om, phase, t_tang_far, first_sub_rho]; t_tang_far = 1.426924/om replaces the "
             "stored near-side t_cross (0.0269/om), which described the direction not run; "
             "first_sub_rho verified bit-identical to the author's stored values",
        dstar=dstar, travel_far=travel_far, travel_near=travel_near,
        mismatches=bad, rows=rows)
    with open(os.path.join(HERE, "results3.regen.json"), "w") as f:
        json.dump(rec, f, indent=1)
    n_ev = sum(1 for r in rows if r[3] is not None)
    n_after = sum(1 for r in rows if r[3] is not None and r[3] > r[2])
    print(f"regen3: {len(rows)} rows, {n_ev} realized events, {n_after} after far tangency, "
          f"{len(rows) - n_after - (len(rows) - n_ev)} before; mismatches vs stored: {bad}")
    print(f"dstar={dstar:.6f} travel_far={travel_far:.6f} travel_near={travel_near:.6f}")


if __name__ == "__main__":
    main()
