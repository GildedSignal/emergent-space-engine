#!/usr/bin/env bash
# Regen: every dossier number, from the run's own scripts and the shipped crates.
#   1. the original run's float falsifier (the negative control's record), vendored verbatim;
#   2. the Rust probe: the positive control on the design's own path — an external call into
#      the shipped `lorentz.rs` (Frame::of / Frame::inverse on events), no crate edits;
#   3. analyze.py: asserts every dossier number against predictions.md's frozen bounds.
# No tree edits outside this folder, so work/patch.diff is empty.
set -euo pipefail
cd "$(dirname "$0")"
if [ -s work/patch.diff ]; then git apply work/patch.diff; fi

echo "== 1. the original falsifier (record regeneration) =="
python3 falsifier_key_depth2.py
python3 - <<'EOF'
import json
d = json.load(open("results.json"))
g = d["kill_grid"]
n1 = sum(1 for r in g if max(abs(r["err1"]), abs(r["err2"])) >= 1.0)
n10 = sum(1 for r in g if max(abs(r["err1"]), abs(r["err2"])) >= 10.0)
assert n1 == 79 and n10 == 52 and len(g) == 108, (n1, n10, len(g))
assert d["controls"]["depth1_beta2_0"]["err1"] == 0.0 and d["controls"]["depth1_beta2_0"]["err2"] == 0.0
assert abs(d["controls"]["depth2_moon_speed"]["err1"] - 3.094e-3) < 1e-4
assert d["oracle_check"] < 1e-9
assert [round(r["err1"], 2) for r in d["named"]] == [15.18, 178.63, 130.07, 0.0]
assert round(d["tb_channel"]["unscaled_error"], 1) == 6666.7
assert [round(r["err1"], 2) for r in d["depth"]] == [15.18, 78.12, 227.5]
print("regen: the frozen record reproduced and asserted")
EOF

echo "== 2. the positive control on the shipped path (cargo build + run) =="
cd probe
cargo build --offline 2>/dev/null || cargo build
SELFTEST=1 cargo run -q | tee ../selfcheck.jsonl
cd ..
cargo run -q --manifest-path probe/Cargo.toml > probe_out.jsonl

echo "== 3. assertions against the frozen predictions =="
python3 analyze.py
echo "regen: done"
