#!/bin/bash
# Regenerate the shipped-code record (9 runs of hlive.py + analyze.py).
# Idempotent: skips runs whose JSON already exists. metrics-regen.json is
# produced in the clean regen/ subdir because *.2.json files would pollute
# analyze.py's glob in the run folder itself.
set -e
cd "$(dirname "$0")"
run() { [ -f "$1.json" ] || python3 hlive.py "${@:2}"; }
run belt_s1    --tag belt_s1 --seed 1 --N 4000 --po 300
run belt_s2    --tag belt_s2 --seed 2 --N 4000 --po 300
run belt_hot_s3 --tag belt_hot_s3 --seed 3 --N 4000 --po 300 --sige 0.08
run ctl_s1     --tag ctl_s1 --seed 1 --N 4000 --po 300 --mu 0
run ctl_s2     --tag ctl_s2 --seed 2 --N 4000 --po 300 --mu 0
run ring21_s1  --tag ring21_s1 --seed 1 --N 2000 --po 600 --ring 2.54,0.05,0.02
run ring21_s2  --tag ring21_s2 --seed 2 --N 2000 --po 600 --ring 2.54,0.05,0.02
run ringoff_s1 --tag ringoff_s1 --seed 1 --N 2000 --po 600 --ring 2.80,0.05,0.02
run ringoff_s2 --tag ringoff_s2 --seed 2 --N 2000 --po 600 --ring 2.80,0.05,0.02
mkdir -p regen
cp hlive.py analyze.py belt_s1.json belt_s2.json belt_hot_s3.json ctl_s1.json \
   ctl_s2.json ring21_s1.json ring21_s2.json ringoff_s1.json ringoff_s2.json regen/
(cd regen && python3 analyze.py && mv metrics.json ../metrics-regen.json)
python3 - <<'PY'
import json
r = json.load(open("metrics-regen.json")); o = json.load(open("metrics.json"))
diff = [k for k in set(o) | set(r) if o.get(k) != r.get(k)]
assert diff == ["wall_s_max"], diff
print("record regenerates; only wall_s_max differs")
PY
