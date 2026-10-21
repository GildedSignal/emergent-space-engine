#!/usr/bin/env bash
# Regen (inversion 279d): every dossier number, from shipped code + this run's patch (truthprobe example).
# ~11 min wall. Scene: plane_extra belt N=10^4, seed 1, coast/burn, rtf 6000, cut at 20 s game time.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
out=lab/results/20261021-1655-inversion-279d/work
mkdir -p "$out"
cargo build --release -p emergent-universe --example truthprobe 2>&1 | tail -1
B="${CARGO_TARGET_DIR:-target}/release/examples/truthprobe"

# Clean matrix (Table 1): 5 arms x 2 reps, input none, no gather. One digest expected.
: > "$out/clean-matrix.jsonl"
for arm in "unlimited 6000 20 12" "events 6000 20 12" "unpaced 6000 20 12" "unpaced 6000 20 0.5" "paced 6000 20 12"; do
  for rep in 1 2; do set -- $arm; $B $1 $2 $3 $4 10000 1 1 0 none >> "$out/clean-matrix.jsonl"; done
done

# Attribution matrix (Table 2): input placement, 3 reps each; gather arm, 3 reps.
: > "$out/burn-matrix.jsonl"; : > "$out/gather-matrix.jsonl"
for rep in 1 2 3; do
  $B unpaced 6000 20 12 10000 1 1 0 presented >> "$out/burn-matrix.jsonl"
  $B unpaced 6000 20 12 10000 1 1 0 scheduled >> "$out/burn-matrix.jsonl"
  $B unpaced 6000 20 12 10000 1 1 60 none     >> "$out/gather-matrix.jsonl"
done

# Shipped-surface control: the bench's own canonical-log path, one flight.
"${CARGO_TARGET_DIR:-target}/release/xtask" universe --bench --seed 1 --rtf 6000 --seconds 20 \
  --engine-ms 12 --no-record > "$out/shipped-bench.json" 2>/dev/null || true

python3 - "$out" <<'EOF'
import json, sys
out = sys.argv[1]
print("== Table 1: clean matrix (one digest per arm expected)")
digs = {}
for l in open(f"{out}/clean-matrix.jsonl"):
    d = json.loads(l)
    digs.setdefault(d["arm"], set()).add(d["digest"][:16])
    print(f'{d["arm"]:<10} {d["digest"][:16]} kicks {d["kicks"]:>7} enc {d["encounters"]:>6} pres {d["presented_at_end"]/1e9:6.2f}e9')
all_d = set().union(*digs.values())
print("arms:", len(digs), "| distinct digests across ALL clean arms:", len(all_d), sorted(all_d))
print("== Table 2: attribution")
for fn in ("burn-matrix.jsonl", "gather-matrix.jsonl"):
    for key in ("presented", "scheduled", "none"):
        rows = [json.loads(l) for l in open(f"{out}/{fn}") if json.loads(l)["input"] == key]
        if rows:
            ds = {r["digest"][:16] for r in rows}
            ps = {r["digest_presented"][:16] for r in rows}
            print(f'input={key:<10} reps {len(rows)} digests {len(ds)} {sorted(ds)} | digest_presented {len(ps)} distinct | kicks {[r["kicks"] for r in rows]}')
b = json.load(open(f"{out}/shipped-bench.json"))
print("== Shipped bench: cut", b["cut_tick"], "digest", b["digest"][:16], "decisions", len(b["decisions"]["taken"]), "pres", b["presented_tick_at_end"])
EOF
