#!/usr/bin/env bash
# Regen: rebuilds every number in dossier.md from the published run branches.
# A compile run — nothing to execute but the record itself. ~10 s.
set -eu
cd "$(git rev-parse --show-toplevel)"
run=lab/results/20261012-1715-q-wiki-coorbital-cert-fd4f

# 1. The branch census (dossier: "646 branches").
git for-each-ref --format='%(refname:short)' refs/remotes/origin/claude > "$run/work/refs.txt"
echo "branches: $(wc -l < "$run/work/refs.txt")"

# 2. The abstract corpus (dossier: "77 abstracts").
bash "$run/work/extract.sh"

# 3. The audit: 48 cited grades vs check.md, 13 dead-run classifications,
#    25 load-bearing needles in primary records. Exits 1 on any mismatch.
python3 "$run/work/audit.py"

# 4. Tallies quoted in the dossier.
python3 - <<'PY'
import re
from collections import Counter
from pathlib import Path
runs = [l for l in (Path("lab/results/20261012-1715-q-wiki-coorbital-cert-fd4f")/"wiki/coorbital-cert.md").read_text().splitlines() if l.startswith("- 20")]
print("page run lines:", len(runs), dict(Counter(re.search(r"\((\w+)\):", l).group(1) for l in runs)))
PY
