#!/usr/bin/env bash
# Regenerates every number in dossier.md (run id 20261017-1447-second-20261017-1330-redteam-68e7-506c).
# The runner applies work/patch.diff first; this script needs only cargo + python3.
# Quiet 8-core box: ~5 min (two full executions of both arms, release) + verdict + checks.
set -euo pipefail
cd "$(dirname "$0")/../../.."
OUT=lab/results/20261017-1447-second-20261017-1330-redteam-68e7-506c
mkdir -p "$OUT/rows" /tmp/r5second

echo "== 1. Decisive execution: both arms (release; the integer law is profile-independent) =="
R5S_OUT="$OUT/rows" cargo test --release -p emergent-engine --test r5_starve -- --test-threads=2 2>&1 | tail -2
R5S_OUT="$OUT/rows" cargo test --release -p emergent-allocator --test r5_starve_alloc -- --test-threads=3 2>&1 | tail -2

echo "== 2. metrics.json and the mechanical verdict =="
python3 "$OUT/metrics.py" "$OUT/rows" | tee "$OUT/metrics.json"
python3 lab/verdict.py "$OUT/r5-starve.md" "$OUT/metrics.json"

echo "== 3. Lineage: the starved sparse digests equal the checker-verified 68e7 unstarved rows =="
python3 - "$OUT" <<'EOF'
import json, sys
out = sys.argv[1]
ref = json.load(open(f"{out}/reference-digests.json"))
ok, bad = 0, []
for s, want in ref.items():
    rows = [json.loads(l) for l in open(f"{out}/rows/r5s-{s}.json")]
    r = [x for x in rows if x["config"] == "cpu-pair-starved" and x["pair"] == "sparse-rand-vs-lockstep"][0]
    if r["world"] == want: ok += 1
    else: bad.append((s, want, r["world"]))
print(f"lineage: {ok}/10 world digests match", "MISMATCH:" + str(bad) if bad else "")
EOF

echo "== 4. Second full execution: the record regenerates bit for bit (wall fields aside) =="
R5S_OUT=/tmp/r5second cargo test --release -p emergent-engine --test r5_starve -- --test-threads=2 2>&1 | tail -2
R5S_OUT=/tmp/r5second cargo test --release -p emergent-allocator --test r5_starve_alloc -- --test-threads=3 2>&1 | tail -2
python3 - "$OUT" <<'EOF'
import json, glob, os, sys
out = sys.argv[1]
WALL = ("secs_a", "secs_b", "secs", "slow")
META = ("units", "merges", "splits", "rollbacks", "over_budget")  # allocator schedule chatter
def load(p, drop):
    rs = [json.loads(l) for l in open(p) if l.strip()]
    for r in rs:
        for k in drop: r.pop(k, None)
    return rs
battle = sorted(glob.glob(f"{out}/rows/r5s-*.json"))
alloc = sorted(glob.glob(f"{out}/rows/r5sa-*.json"))
d = [os.path.basename(p) for p in battle if load(p, WALL) != load("/tmp/r5second/" + os.path.basename(p), WALL)]
print("battle rows (digests, counters, starved call-counts):", "ALL MATCH" if not d else f"DIFFER: {d}")
flips = meta = 0
for p in alloc:
    q = "/tmp/r5second/" + os.path.basename(p)
    for x, y in zip(load(p, ()), load(q, ())):
        flips += x["identical"] != y["identical"] or not x["identical"]
        meta += any(x[k] != y[k] for k in META)
print(f"allocator cells: digest flips across executions: {flips} (0 required); "
      f"scheduler-metadata moves in {meta} cells — wall-fed by design under calibrated "
      "budgets and worker races (allocator lib.rs: scheduling changes speed, never results)")
EOF
