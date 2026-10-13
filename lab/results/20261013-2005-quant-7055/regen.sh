#!/bin/sh
# lab run 20261013-2005-quant-7055 — regenerates every dossier number from the patched tree.
# The runner applies work/patch.diff (saved by run.sh) before this runs. <= 15 minutes.
set -e
cd "$(dirname "$0")/../../.."           # repo root
RUN=lab/results/20261013-2005-quant-7055
W=$RUN/work
XBIN=$(cargo metadata --no-deps --format-version 1 | python3 -c "import json,sys; print(json.load(sys.stdin)['target_directory'])")/release/xtask

echo "== build (probe patch applied by the runner)"
cargo build --release -p xtask
mkdir -p "$W"

echo "== matrix: 6 scenes x 3 arms (A base, B keys, C exact memo)"
for spec in "m48:48:1:8:1" "m400:400:1:8:1" "m1500:1500:1:8:1" "m4000:4000:1:8:1" "m4000s3:4000:1:8:3" "m400rtf100:400:100:8:1"; do
  name=${spec%%:*}; rest=${spec#*:}; m=${rest%%:*}; rest=${rest#*:}; rtf=${rest%%:*}; rest=${rest#*:}; secs=${rest%%:*}; seed=${rest#*:}
  env ES_PROBE_ARM=A $XBIN universe --bench --seed "$seed" --rtf "$rtf" --seconds "$secs" --unpaced --members "$m" > "$W/${name}_A.json"
  env "ES_ORBIT_KEYS=$W/${name}_A_keys.csv" $XBIN universe --bench --seed "$seed" --rtf "$rtf" --seconds "$secs" --unpaced --members "$m" > "$W/${name}_B.json"
  env ES_PROBE_ARM=C ES_ORBIT_MEMO=1 $XBIN universe --bench --seed "$seed" --rtf "$rtf" --seconds "$secs" --unpaced --members "$m" > "$W/${name}_C.json"
done

echo "== interleaved A/C at m4000 with the memo's keys logged (true hit counts)"
env ES_ORBIT_MEMO=1 "ES_ORBIT_KEYS=$W/m4000_memo_keys.csv" $XBIN universe --bench --seed 1 --rtf 1 --seconds 8 --unpaced --members 4000 > "$W/m4000_memo.json"
cp "$W/m4000_memo.json" "$W/m4000_C_repeat.json"

echo "== pair locality (adjacency of duplicate keys) and the table"
python3 - <<'EOF'
import csv
from collections import Counter, defaultdict
rows=[r for r in csv.DictReader(open("lab/results/20261013-2005-quant-7055/work/m4000_memo_keys.csv"))]
ho=[(i,r) for i,r in enumerate(rows) if r["site"]=="1"]
pos=defaultdict(list)
for i,r in ho: pos[r["key"]].append(i)
dups={k:v for k,v in pos.items() if len(v)>1}
gaps=Counter(b-a for v in dups.values() for a,b in zip(v,v[1:]))
sizes=Counter(len(v) for v in pos.values())
print("hand-out compiles:", len(ho), "distinct keys:", len(pos))
print("key multiplicity histogram:", dict(sizes))
print("gap between duplicate hand-outs (rows):", dict(gaps))
print("hand-out hits:", sum(1 for _,r in ho if r["hit"]=="true"))
print("all hits:", sum(1 for r in rows if r["hit"]=="true"), "of", len(rows))
EOF
python3 "$W/analyze.py" "$W"

echo "== digest identity with the memo forced on: the universe suite (1 ignored clock flight)"
ES_ORBIT_MEMO=1 cargo test --release -p emergent-universe 2>&1 | grep -E "test result" || true
echo "== done"
