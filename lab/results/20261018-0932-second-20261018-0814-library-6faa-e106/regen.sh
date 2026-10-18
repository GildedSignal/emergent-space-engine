#!/usr/bin/env bash
# Regenerates every number in dossier.md from SHIPPED code only.
#
# Why base-only: the author's Carlson wiring (work/patch.diff) was lost before
# publication — the previous regen.sh applied the patch and REVERSED it in an
# exit trap; the author's final verification run therefore restored the tree
# clean, and lab/run.sh's phase() then captured an empty diff. The wired-arm
# numbers (carlson_wiring.json, bench-wired-*, frame-wired.txt) are kept as
# FROZEN evidence of what ran on 2026-10-18 10:03; they are NOT regenerated
# here and the dossier cites them only as frozen record.
#
# Regenerating (this script): the three base-arm kick-bench seeds, the
# frame_digest flights, and the a765 cut-digest anchor bit-identity check.
# Wall: ~2 min warm build + ~50 s of runs.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
cd "$ROOT"

cargo build --release -p xtask
X="$(cargo metadata --no-deps --format-version 1 | python3 -c 'import json,sys; print(json.load(sys.stdin)["target_directory"])')/release/xtask"

# 1) the base arm (shipped path), three seeds — a765's harness unchanged
for sd in 1 7 42; do
  "$X" universe --kick-bench --seed $sd --rtf 100 --seconds 10 > "$HERE/bench-base-seed$sd.json"
done

# 2) frame_digest's 8 flights x 4 schedules, shipped path
cargo build --release -p emergent-universe --example frame_digest
cargo run --release -p emergent-universe --example frame_digest -- 4 > "$HERE/frame-base.txt"

# 3) summary + baseline-integrity assertion (the number the dossier cites)
python3 - "$HERE" <<'EOF'
import json, pathlib, sys
out = pathlib.Path(sys.argv[1])
ANCHOR = "e622722afe27175cf09264d7be767e50ee5f644d728a12974ee29a1c1053605c"  # a765's stored seed-1 cut digest
print("== base arm (shipped path; medians per seed) ==")
for sd in (1, 7, 42):
    b = json.load(open(out / f"bench-base-seed{sd}.json"))
    print(f"seed {sd}: made {b['kick_us']['median']:.1f} us (n={b['kick_us']['samples']})  "
          f"leavers {b['kick_us_leavers']['median']:.1f} us (n={b['kick_us_leavers']['samples']})  "
          f"all {b['kick_us_all']['median']:.1f} us (n={b['kick_us_all']['samples']})  "
          f"refused {b.get('refused', 'n/a')}  cut {b['digest'][:16]}...")
ok = json.load(open(out / "bench-base-seed1.json"))["digest"] == ANCHOR
print(f"baseline integrity: seed-1 cut digest == a765 anchor: {ok}")
assert ok, "shipped-path digest drifted from a765's anchor"
print("== frame_digest: 8 flights x 4 schedules (shipped path) ==")
rows = [l for l in open(out / "frame-base.txt") if "seed" in l and "|" in l]
agree = sum("4 schedules agree" in l for l in rows)
print(f"flights: {len(rows)}  schedule-agreement: {agree}/{len(rows)}")
for l in rows:
    f = [s.strip() for s in l.split("|")]
    print(f"  {f[0].split(' seed ')[0]:<24} {f[1][:32]}  {f[2]}")
EOF
