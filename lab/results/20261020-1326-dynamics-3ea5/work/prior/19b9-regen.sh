#!/usr/bin/env bash
# Regenerates every dossier number: builds the harness from work/patch.diff (applied by
# the runner), flies the four arms plus the unit isolation, analyzes. ~9 min.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
RUN=lab/results/20261020-0548-dynamics-19b9
git apply --check "$RUN/work/patch.diff" 2>/dev/null && git apply "$RUN/work/patch.diff" || true
cargo build --release --example beltledger --example iso_ledger
B="$CARGO_TARGET_DIR/release/examples/beltledger"; [ -x "$B" ] || B=target/release/examples/beltledger
I="$CARGO_TARGET_DIR/release/examples/iso_ledger"; [ -x "$I" ] || I=target/release/examples/iso_ledger
cd "$RUN/work"
rm -rf flights; mkdir flights; cd flights
"$B" --horizon 98304 --seed 1 --thermal 0 --out B_cold_s1 > B.log 2>&1 &
"$B" --horizon 49152 --seed 2 --thermal 4096 --out C_th_s2 > C.log 2>&1 &
"$B" --horizon 16384 --seed 1 --thermal 0 --notide --out E_notide_s1 > E.log 2>&1 &
"$B" --horizon 8192 --seed 1 --thermal 4096 --pass --out D_pass_s1 > D.log 2>&1 &
wait
"$I" | tail -1
cd ..
python3 analyze.py flights > analysis.json
python3 - <<'EOF'
import json
d = json.load(open("analysis.json"))
for arm in ["B_cold_s1", "C_th_s2"]:
    r = d[arm]
    print(arm, "contacts", r["contacts"], "ch", r["n_ch"],
          "slope", r["p2_walk_slope"], "envratio", r["p1_envelope"]["maxAbsR_over_2maxk"],
          "P1ok", r["p1_envelope"]["ok"], "netfrac", round(r["p2b_global_debt"]["max_frac"], 9),
          "maxAbsR", r["p6_headroom"]["maxAbsR"], "bits", r["p6_headroom"]["bits_R"],
          "gross", r["gross_absR"], "net", r["net_R"])
print("D_pass_zero", d["D_pass_zero"]["ok"], "| E_identity dev", d["E_identity"]["identity_max_abs_dev"])
for l in open("flights/C_th_s2.head").read().splitlines()[:2]:
    print(l)
EOF
