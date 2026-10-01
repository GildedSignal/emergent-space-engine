#!/usr/bin/env python3
"""Fills the dossier's PLACEHOLDER sections from metrics.json / metrics_extra.json."""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

m = json.load(open("metrics.json"))
x = json.load(open("metrics_extra.json"))

crit = {"jacobi_exponent": ("<= 0.2", lambda v: v <= 0.2),
        "class_match": (">= 0.99", lambda v: v >= 0.99),
        "precession_match": (">= 0.99", lambda v: v >= 0.99),
        "libration_ratio": (">= 0.8", lambda v: v >= 0.8),
        "force_evals_per_orbit": ("<= 200", lambda v: v <= 200)}

lines = ["| config | jacobi_exponent | class_match | precession_match | libration_ratio "
         "| force_evals_per_orbit | verdict |",
         "|---|---|---|---|---|---|---|"]
for cfg, row in m.items():
    vals, oks = [], []
    for k, (txt, fn) in crit.items():
        v = row[k]
        vals.append(f"{v:.4g}" if isinstance(v, float) else str(v))
        oks.append("Y" if fn(v) else "N")
    verdict = "all criteria pass" if all(o == "Y" for o in oks) else \
        "fails: " + ", ".join(k for (o, k) in zip(oks, crit) if o == "N")
    lines.append(f"| {cfg} | " + " | ".join(vals) + f" | {verdict} |")
table = "\n".join(lines)

t = x.get("truth", {})
truth_cost = (f"truth's true cost (reported, not the convention 0): "
              f"{t.get('nfev_b12', 0):,} force evaluations for the 16 ships "
              f"(~{t.get('nfev_b12', 0) / 16 / (200 * 192):.0f} per planet orbit at DOP853's 12 "
              f"stages), {t.get('nfev_b14', 0):,} for the 256 moons, {t.get('nfev_res', 0):,} "
              f"for the 36 resonant cases.")
denoms = (f"denominators: {t.get('judged_moons')} non-chaotic moons judged, "
          f"{t.get('bound_rated')} bound moons with a defined apse, "
          f"{t.get('librating')} librating resonant cases; "
          f"{t.get('jacobi_judged')} of 16 ships rose above the 1e-12 floor for the truth, "
          f"and the truth's own worst Jacobi error was {t.get('truth_jacobi_max', 0):.1e}.")

extra_lines = []
for cfg in ["symba", "wh-fixed", "soi-switch"]:
    e = x.get(cfg, {})
    extra_lines.append(f"- {cfg}: {e.get('jacobi_judged')} ships judged on Jacobi, "
                       f"worst |dC_J/C_J| {e.get('b12_maxerr', 0):.2e} (B12 also demands 1e-4).")
extra = "\n".join(extra_lines)

doc = open("dossier.md").read()
doc = doc.replace("PLACEHOLDER\n\n**Metrics**", "**Metrics**")  # tidy if needed
doc = doc.replace("PLACEHOLDER_PREDICTIONS", "see below")
parts = doc.split("PLACEHOLDER")
assert len(parts) == 3, len(parts)
doc = parts[0] + table + f"\n\n{truth_cost}\n\n{denoms}\n\n" + extra + parts[2]
open("dossier.md", "w").write(doc)
print("dossier filled")
