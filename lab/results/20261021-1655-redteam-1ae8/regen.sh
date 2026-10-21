#!/usr/bin/env bash
# Regenerates every number in dossier.md for run 20261021-1655-redteam-1ae8.
# Applies the run's saved patch (if any), then runs the falsifier. ~60 s single core.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"

# Apply the author's tree edits (saved by run.sh), if present.
if [ -f "$HERE/../work/patch.diff" ]; then
  git -C "$ROOT" apply "$HERE/../work/patch.diff" 2>/dev/null || echo "note: patch.diff present but not applied (or already applied)"
fi

cd "$HERE"
python3 peters.py | tee peters_regen.log

# Summary lines quoted in the dossier (from peters_out.json).
python3 - <<'EOF'
import json
d = json.load(open("peters_out.json"))
rows = d["rows"]
g = lambda p, e, nu: next(r for r in rows if r["p0"] == p and r["e0"] == e and r["nu"] == nu)
print("C1", f"{d['c1']:.2e}", "| C3", f"{d['c3']:.3f}", "| conv", d["conv"])
for (p, e, nu) in [(65, 0.0, 0.25), (65, 0.6, 0.25), (65, 0.9, 0.25),
                   (15, 0.9, 0.25), (20, 0.9, 0.25), (30, 0.9, 0.25),
                   (15, 0.0, 0.25), (20, 0.0, 0.25), (30, 0.0, 0.25), (15, 0.0, 0.5)]:
    r = g(p, e, nu)
    print(f"p0={p:3.0f} e0={e:.1f} nu={nu:.2f}: dtt {100*r['dt_rel']:+7.2f}%  "
          f"dcyc {100*r['dcyc_rel']:+7.1f}%  maxDa/a {r['max_da_over_a']:.2f}  "
          f"p_end_l {r['p_end_letter']:+.2f}  cyc_l {r['cycles_letter']}")
print("circular law |dtt|/q0:",
      [f"{abs(r['dt_rel'])/r['q0']:.2f}" for r in rows if r["e0"] == 0.0])
EOF
