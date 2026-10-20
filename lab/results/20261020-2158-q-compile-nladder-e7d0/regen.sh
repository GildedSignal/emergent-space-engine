#!/bin/sh
# Regen for 20261020-2158-q-compile-nladder-e7d0 — every number in the dossier
# regenerates from shipped code (lab/wiki/nladder.md at the run's base commit),
# this script and the run's own compile.py. Nothing here edits lab/wiki/ (the
# page is compiled INTO the run folder; publishing merges it three-way).
#
# Wall time: < 1 min (a git-reading Python script; no flights — the run's
# evidence is the compile and its audits, all deterministic).
set -e
cd "$(dirname "$0")/../../.."        # repo root (the runner applies work/patch.diff first)

echo "== base commit:"; git rev-parse HEAD

python3 lab/results/20261020-2158-q-compile-nladder-e7d0/compile.py
# compile.py exits non-zero if any audit fails (budget, run coverage, number sample)

echo "== the lab's own instrument on the compiled page (wiki.py index, sandboxed):"
T=$(mktemp -d)
cp lab/results/20261020-2158-q-compile-nladder-e7d0/wiki/nladder.md "$T/"
python3 - "$T" <<'EOF'
import sys, importlib.util
spec = importlib.util.spec_from_file_location("wiki", "lab/wiki.py")
wiki = importlib.util.module_from_spec(spec); spec.loader.exec_module(wiki)
wiki.WIKI = sys.argv[1]
wiki.index()
row = [l for l in open(sys.argv[1] + "/index.md") if "nladder" in l][0]
assert "over budget" not in row, row
print(row.strip())
EOF

echo "== report:"; cat lab/results/20261020-2158-q-compile-nladder-e7d0/compile-report.json
