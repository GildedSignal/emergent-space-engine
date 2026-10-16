#!/usr/bin/env bash
# Run 20261016-1120 (second author on 20261016-0504-dynamics-4c22). Regenerates every number in
# dossier.md from shipped code + work/patch.diff (the runner applies the patch first).
# ~4 min on 8 vCPU: two example builds + 8 flights (3x60 s, 5x20 s) + 3 digest runs.
set -u
cd "$(git rev-parse --show-toplevel)"
R=lab/results/20261016-1120-second-20261016-0504-dynamics-4c22-dd75
# The patch is applied by the runner; if the tree is pristine, apply it ourselves (idempotent check).
if ! grep -q "run 20261016-1120" crates/universe/examples/nladder.rs 2>/dev/null; then
  git apply "$R/work/patch.diff"
fi
cargo build --release -p emergent-universe --example nladder --example ladder_digest 2>&1 | tail -1
bash "$R/scripts/run_batch.sh"
python3 "$R/scripts/summarize.py"
echo "--- worst-6 composition (fixed instrument), 60-s baseline:"
grep "^attrib" "$R/data/base_n1e3_60s.txt"
echo "--- whole-flight attribution (dolls + kinds):"
python3 - <<'EOF'
import sys
sys.path.insert(0, "lab/results/20261016-1120-second-20261016-0504-dynamics-4c22-dd75/scripts")
from analyze import load
for name in ["base_n1e3_60s", "base_n0_20s", "phase_n1e3_60s"]:
    rows = [r for r in load(name) if r["frame"] >= 60]
    tot = sum(r["ev"] for r in rows); att = 0; dolls = {}
    for r in rows:
        for d, v in r["att"].items():
            dolls[d] = dolls.get(d, 0) + sum(v); att += sum(v)
    print(name, "events", tot, "attributed", att, f"({att/tot:.1%})", "by doll", dolls)
EOF
echo "--- digests (off must equal the record: N=100 4b822570, N=1000 6895ce06, N=3000 ddd5b1cc; stag e5e9bea5 kicks 3750; phase 708f7d82 kicks 3932)"
for a in off stag phase; do grep " coast " "$R/data/digest_$a.txt" | head -3; done
echo REGEN_DONE
