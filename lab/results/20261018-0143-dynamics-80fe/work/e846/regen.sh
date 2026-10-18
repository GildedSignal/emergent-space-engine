#!/usr/bin/env bash
# Regen: rebuilds every number in dossier.md from shipped code + this run's probe
# (work/patch.diff: trojan_dive.rs, the Lost-branch census counters, behave/mod.rs) in ~8 min.
set -euo pipefail
cd "$(dirname "$0")"/../../.. || exit 1  # repo root
R="$(pwd)/lab/results/20261016-1319-dynamics-e846"
cargo test --release -p xtask behave::trojan_dive::trojan_dive --no-run >/dev/null
# Controls: the death channel's positive control, the elements pipeline, the rtol pair.
TROJAN_CONTROL=$R/control.txt cargo test --release -p xtask behave::trojan_dive::trojan_dive_control -- --exact --ignored --nocapture 2>&1 | grep '^control' || true
# The analytic arm (neck criticals, no-confinement).
TROJAN_OUT=$R/analytic.jsonl TROJAN_ARM=analytic TROJAN_WORKERS=4 \
  cargo test --release -p xtask behave::trojan_dive::trojan_dive -- --exact --ignored --nocapture 2>&1 | grep 'dive: arm'
# The plane arm (the expensive one, ~5-6 min shared): channel census + refined epochs + series.
TROJAN_OUT=$R/plane.jsonl TROJAN_ARM=plane TROJAN_STEP=7 TROJAN_PERIODS=512 TROJAN_WORKERS=7 \
  cargo test --release -p xtask behave::trojan_dive::trojan_dive -- --exact --ignored --nocapture 2>&1 | grep 'dive: arm'
# The oracle arm (P/8 elements + periapsis-resolved conjunction over the whole horizon).
TROJAN_OUT=$R/oracle.jsonl TROJAN_ARM=oracle TROJAN_WORKERS=7 TROJAN_PERIODS=512 \
  cargo test --release -p xtask behave::trojan_dive::trojan_dive -- --exact --ignored --nocapture 2>&1 | grep 'dive: arm'
# The windowed parity pass: the truth's resolved conjunction within ±2 P of each death epoch.
python3 - "$R" <<'EOF'
import json, re, sys
R = sys.argv[1]
out = []
for l in open(f"{R}/plane.jsonl"):
    if not l.startswith("{"):
        continue
    r = json.loads(re.sub(r":inf", ":-1", l))
    if r.get("dead"):
        out.append({"du": r["du"], "phi_deg": r["phi_deg"], "epoch_P": r["epoch_P"]})
open(f"{R}/wins.jsonl", "w").write("\n".join(json.dumps(o) for o in out) + "\n")
print(f"{len(out)} windows")
EOF
TROJAN_OUT=$R/oracle-win.jsonl TROJAN_ARM=oracle TROJAN_WIN_FILE=$R/wins.jsonl TROJAN_WORKERS=7 TROJAN_PERIODS=512 \
  cargo test --release -p xtask behave::trojan_dive::trojan_dive -- --exact --ignored --nocapture 2>&1 | grep 'dive: arm'
python3 "$R/aggregate.py" | tee "$R/aggregate.out"
