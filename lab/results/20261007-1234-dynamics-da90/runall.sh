#!/bin/bash
# Full decisive run. Each config ≤ 60 s target; policy variants included.
set -e
for spec in "generic absorb" "resonant absorb" "precession absorb" "precessionNoM noM" "noabsorb noabsorb" "precession driftwin" "snaps absorb" "kicks absorb"; do
  set -- $spec
  cfg=$1; pol=$2
  python3 study.py --config $cfg --policy $pol --pairs 300 --K 2500 --seed 11 > raw-$cfg-$pol.json 2> raw-$cfg-$pol.err &
done
wait
python3 - <<'PY'
import json, glob, collections
out = {}
for f in sorted(glob.glob("raw-*.json")):
    try:
        d = json.load(open(f))
    except Exception as e:
        d = {"error": str(e), "err": open(f.replace(".json",".err")).read()[:200]}
    out[f[4:-5]] = d
json.dump(out, open("metrics.json","w"), indent=1)
# headline summary
for k, d in out.items():
    if "error" in d: print(k, "ERROR", d["error"], d["err"][:100]); continue
    print(f"{k:24s} work {d['work_ratio']:.4f}  late {d['late']:5d}  enc {d['encounters']:5d}  hits {d['hits']:5d}  grants {d['grants']:6d}  fh_med {d['fh_median']:6.1f}  snaps {d['snaps']:5d}  kicks {d['kicks']:4d}  spacing_med {d.get('spacing_median',0):6.1f}  resfrac {d['res_frac_q2_64_eps3']:.3f}")
PY
