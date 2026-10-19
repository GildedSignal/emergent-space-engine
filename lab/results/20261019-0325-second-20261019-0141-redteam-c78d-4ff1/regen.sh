#!/bin/sh
# Regen: every number in dossier.md, from this folder's scripts. ~3 min, < 1 GB.
# 1. the rung is the frozen file; 2. the decisive run + independent check path + verdict;
# 3. diagnostics; 4. c78d's base record still regenerates byte-identical.
set -e
cd "$(dirname "$0")"

echo "== 0. rung hash (frozen before the run; must still match) =="
sha256sum -c rung.sha256

echo "== 1. decisive configs (author path, quadratic root) =="
rm -f author-runs.txt
for c in pixel-h2 pixel-h1 one-sample overlap-disc; do
  python3 eclipse_rung.py "$c" | tee -a author-runs.txt
done
python3 - <<'EOF'
import json
out = {}
for line in open("author-runs.txt"):
    line = line.strip()
    if line.startswith("{"):
        out.update(json.loads(line))
json.dump(out, open("metrics.json", "w"), indent=1)
EOF

echo "== 2. independent check path (monotone bisection, 3-case predicate) =="
python3 eclipse_rung.py --check

echo "== 3. mechanical verdict (checker vs author metrics) =="
python3 ../../verdict.py r11-eclipse-aggregate.md metrics-check.json metrics.json | tee verdict.txt

echo "== 4. diagnostics (beta 0.9, cap-as-function to R_f=30, arc resolving pitch) =="
python3 eclipse_rung.py --diagnostics
cat diagnostics.json

echo "== 5. c78d's base record regenerates byte-identical =="
mkdir -p /tmp/c78d-regen && cp orig-occlusion.py /tmp/c78d-regen/occlusion.py
cp orig-regen-output.txt /tmp/c78d-regen/stored.txt
( cd /tmp/c78d-regen && python3 occlusion.py > new.txt 2>&1 && diff stored.txt new.txt \
  && echo "c78d REGEN-IDENTICAL" )
rm -rf /tmp/c78d-regen
echo "done"
