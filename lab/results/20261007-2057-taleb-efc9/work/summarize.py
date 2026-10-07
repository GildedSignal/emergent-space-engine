#!/usr/bin/env python3
"""Merge grid + battery2 results into the dossier's evidence table."""
import json

grid = {r["scene"]: r for r in json.load(open("grid_results.json"))}
b2 = json.load(open("battery2.json"))

rows = []
order = ["ctl-ring-circ-aligned", "ctl-arc-circ-aligned", "ctl-ring-e03-aligned",
         "se002-aligned", "se005-aligned", "se01-aligned", "se03-aligned",
         "sw015-e03", "sw045-e03", "sw090-e03", "sw180-e01", "sw180-e03", "sw180-e06",
         "bimodal-e03", "debris-ring"]
print("| scene | n_enc | k* | miss@4 | shell setup (=all pairs) | work n·k*/enc |")
print("|---|---|---|---|---|---|")
for k in order:
    r = grid[k]
    if r["n_enc"] == 0:
        print(f"| {k} | 0 | — | — | {r['setup_shell']} | — |")
        continue
    print(f"| {k} | {r['n_enc']} | {r['k_star']} | {r['miss_at']['4']:.1%} | "
          f"{r['setup_shell']} (100%) | {r['n']*r['k_star']/r['n_enc']:.1f} |")
print()
print("battery2:")
for r in b2:
    if "k_star" in r:
        extra = ""
        for f in ("med_dnu_star_deg", "med_dM_star_deg", "med_domega_deg", "med_rank_dM0"):
            if f in r:
                extra += f" {f}={r[f]:.1f}"
        print(f"  {r['scene']:24s} R={r['R']} n={r['n']} seed={r['seed']} n_enc={r['n_enc']:5d} "
              f"k*={r['k_star']:4d} miss4={r.get('miss4', float('nan')):.1%}{extra}")
    else:
        print(f"  {r['scene']:24s} R={r['R']} n={r['n']} seed={r['seed']} n_enc={r['n_enc']} (empty)")
