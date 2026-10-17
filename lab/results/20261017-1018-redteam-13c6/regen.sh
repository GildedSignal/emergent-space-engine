#!/usr/bin/env bash
# Regenerates every number in dossier.md from the shipped tree + work/patch.diff (applied by the
# runner before this runs). Total time: one release build of one example (~10 s) + 4 runs (~10 s).
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261017-1018-redteam-13c6

# The probe is part of the patch; if the tree was restored without it, restore from the run folder.
if [ ! -f crates/universe/examples/r6_view.rs ]; then
  cp "$R/r6_view.rs" crates/universe/examples/r6_view.rs
fi

cargo build --release -p emergent-universe --example r6_view 2>&1 | grep -E "^error" && exit 1 || true
B=$(ls /home/glmlab/lab-target-3/release/examples/r6_view 2>/dev/null || ls target/release/examples/r6_view)

# The decisive run: one JSON line per configuration, merged into metrics.json (the frozen order).
: > "$R/metrics.json"
for c in warm poisoned cold amnesiac; do
  R6_DIAG=1 "$B" "$c" > /tmp/r6_$c.json 2> /tmp/r6_$c.diag
  echo "--- $c ---"; cat /tmp/r6_$c.diag
done
python3 - <<'EOF'
import json, pathlib
R = pathlib.Path("lab/results/20261017-1018-redteam-13c6")
out = {}
for c in ["warm", "poisoned", "cold", "amnesiac"]:
    out[c] = json.loads(pathlib.Path(f"/tmp/r6_{c}.json").read_text())[c]
json.dump(out, open(R / "metrics.json", "w"), indent=1)
EOF
cat "$R/metrics.json"

# The mechanical verdict (checker metrics = author metrics here: the self-check; a real checker
# reruns this script and replaces metrics.json with metrics-check.json).
python3 lab/verdict.py "$R/r6-view.md" "$R/metrics.json" "$R/metrics.json" | tee "$R/verdict.txt"
