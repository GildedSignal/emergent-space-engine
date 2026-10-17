#!/bin/sh
# Regenerates every number in the dossier from the run's own code: ~30 s, one core, < 100 MB.
# Timing cells (cost_*, S_ms_*) vary with machine load by design; every scene row, margin,
# tail, keep fraction, truth hit and miss count is bit-deterministic (verified twice by author).
set -e
cd "$(dirname "$0")"
rustc -O falsifier2.rs -o falsifier2
./falsifier2 > regen-run.jsonl

# Row budget and the dossier's load-bearing invariants, machine-checked:
#  - 38 rows; every scene row has miss = 0 (soundness, K1);
#  - the three co-located adversarial rows each have truth_hits >= 1 and miss_old_margin >= 1
#    (the silver run's clamped margin misses them; the exact margin keeps them);
#  - the closed-form margin dominates the same-e grid (K0: min >= -1e-6);
#  - formation-true-scale keeps 500/500 truth hits; the counterfactual row holds ~550.
python3 - <<'EOF'
import json, sys
rows = [json.loads(l) for l in open("regen-run.jsonl")]
assert len(rows) == 38, f"row count {len(rows)} != 38"
scenes = [r for r in rows if "scene" in r]
assert all(r["miss"] == 0 for r in scenes), "K1 violated: a true hit was rejected"
adv = [r for r in scenes if r["scene"].startswith("colocated-")]
assert len(adv) == 3 and all(r["truth_hits"] >= 1 and r["miss_old_margin"] >= 1 for r in adv), "adversarial rows"
assert all(r["truth_hits"] >= 1 for r in adv), "adversarial rows lost their crafted hits"
m = rows[0]
assert m["margin_closed_minus_grid_min"] >= -1e-6, "K0: closed-form margin wrong"
form = next(r for r in scenes if r["scene"] == "formation-true-scale")
assert form["truth_hits"] == 500 and form["keep1"] == 1.0, "formation control"
cf = next(r for r in scenes if r["scene"] == "counterfactual-0.176AU")
assert 500 <= cf["truth_hits"] <= 600, "counterfactual wall row"
assert m["margin_e06"] == 1.2615, "checker's margin value must reproduce"
print("REGEN OK:", len(scenes), "scenes, 0 misses,", len(adv), "adversarial misses under the old table")
EOF
