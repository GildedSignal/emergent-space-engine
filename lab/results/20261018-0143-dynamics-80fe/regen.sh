#!/usr/bin/env bash
# Regen: rebuilds every number in dossier.md from shipped code + this run's probe
# (work/patch.diff = e846's census counters + trojan_dive with the events arm and TROJAN_MU)
# in ~12 min on a dedicated 8-vCPU Linux box (shared-host timings are orders of magnitude only).
set -euo pipefail
cd "$(dirname "$0")"/../../.. || exit 1   # repo root
R="$(pwd)/lab/results/20261018-0143-dynamics-80fe"
W="$R/work"
# Idempotent: the checker may run on a tree that already carries the patch (that is what made
# the first regen fail: trojan_dive.rs "already exists"). Unapply if present, then apply fresh.
git apply --reverse --check "$W/patch.diff" 2>/dev/null && git apply --reverse "$W/patch.diff" || true
git apply "$W/patch.diff"
cargo test --release -p xtask behave::trojan_dive::trojan_dive --no-run >/dev/null
# Truth arms: disk-entry events at both mu, plus the rtol pair (seconds each).
TROJAN_OUT=$W/ev-mu2.jsonl    TROJAN_MU=0.01  TROJAN_RTOL=1e-12 TROJAN_ARM=events TROJAN_PERIODS=512 TROJAN_WORKERS=6 \
  cargo test --release -p xtask behave::trojan_dive::trojan_dive -- --exact --ignored --nocapture 2>&1 | grep 'dive: arm'
TROJAN_OUT=$W/ev-mu3.jsonl    TROJAN_MU=0.001 TROJAN_RTOL=1e-12 TROJAN_ARM=events TROJAN_PERIODS=512 TROJAN_WORKERS=6 \
  cargo test --release -p xtask behave::trojan_dive::trojan_dive -- --exact --ignored --nocapture 2>&1 | grep 'dive: arm'
TROJAN_OUT=$W/ev-mu3fine.jsonl TROJAN_MU=0.001 TROJAN_RTOL=1e-13 TROJAN_ARM=events TROJAN_PERIODS=512 TROJAN_WORKERS=6 \
  cargo test --release -p xtask behave::trojan_dive::trojan_dive -- --exact --ignored --nocapture 2>&1 | grep 'dive: arm'
# Plane arms. mu=1e-2 explodes in cost (the dossier's cost-wall observation): 4 P completes in
# ~6 s; 16 P does NOT finish under a 120 s budget on 2 workers (the wall, reproduced on purpose);
# 64 P is the wall probe at 4 workers under a hard 120 s timeout (partial by design: only the
# first ICs finish; the row count of pl-mu2-64P.jsonl IS the number quoted in the dossier).
TROJAN_OUT=$W/pl-mu2-4P.jsonl TROJAN_MU=0.01 TROJAN_ARM=plane TROJAN_STEP=7 TROJAN_PERIODS=4 TROJAN_WORKERS=6 \
  cargo test --release -p xtask behave::trojan_dive::trojan_dive -- --exact --ignored --nocapture 2>&1 | grep 'dive: arm'
( TROJAN_OUT=$W/pl-mu2-16P-partial.jsonl TROJAN_MU=0.01 TROJAN_ARM=plane TROJAN_STEP=7 TROJAN_PERIODS=16 TROJAN_WORKERS=2 \
    timeout 120 cargo test --release -p xtask behave::trojan_dive::trojan_dive -- --exact --ignored --nocapture 2>&1 | grep -q 'done in' \
    && echo "16P finished (unexpected)" ) || echo "mu2-16P: unfinished at 120 s (the cost wall)"
TROJAN_OUT=$W/pl-mu2-64P.jsonl TROJAN_MU=0.01 TROJAN_ARM=plane TROJAN_STEP=7 TROJAN_PERIODS=64 TROJAN_WORKERS=4 \
  timeout 120 cargo test --release -p xtask behave::trojan_dive::trojan_dive -- --exact --ignored --nocapture 2>&1 | grep 'dive: arm' || true
# mu=1e-3 control: 512 P ensemble (on a contended host, a 500 s budget leaves a job-order prefix;
# the analysis restricts parity to the completed prefix and reports n).
TROJAN_OUT=$W/pl-mu3.jsonl TROJAN_MU=0.001 TROJAN_ARM=plane TROJAN_STEP=7 TROJAN_PERIODS=512 TROJAN_WORKERS=7 \
  timeout 500 cargo test --release -p xtask behave::trojan_dive::trojan_dive -- --exact --ignored --nocapture 2>&1 | grep 'dive: arm' || true
# Analysis: rates, survival, hazards, rtol pair, driver check, the 4 P epoch table.
python3 - <<'PY'
import json
for f in ("pl-mu3.jsonl", "pl-mu2-4P.jsonl", "pl-mu2-16P-partial.jsonl", "pl-mu2-64P.jsonl"):
    try:
        out = [json.dumps({k: v for k, v in json.loads(l.replace(":inf", ":0").replace(":NaN", ":0")).items() if k != "series"}, separators=(",", ":")) for l in open(f"{W}/" + f)]
        open(f"{W}/" + f, "w").write("\n".join(out) + "\n")
    except FileNotFoundError:
        pass
PY
python3 "$W/parity.py" "$W"
python3 "$W/burst.py" "$W"
