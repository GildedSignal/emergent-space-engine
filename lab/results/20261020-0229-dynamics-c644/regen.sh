#!/usr/bin/env bash
# Regenerates every dossier number: builds the harness from work/patch.diff, flies the
# four arms (A staggered first: four concurrent storms once exhausted this machine's
# budget), analyzes, and prints/writes analysis.json. Runtime ~8 min.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
RUN=lab/results/20261020-0229-dynamics-c644
# The runner applies work/patch.diff before this script; apply only if missing.
git apply --check "$RUN/work/patch.diff" 2>/dev/null && git apply "$RUN/work/patch.diff" || true
cargo build --release --example beltewalk
B="$CARGO_TARGET_DIR/release/examples/beltewalk"; [ -x "$B" ] || B=target/release/examples/beltewalk
cd "$RUN/work"
rm -rf flights; mkdir flights; cd flights
"$B" --horizon 49152 --seed 1 --thermal 4096 --out A_th_s1 > A.log 2>&1 &
sleep 90   # stagger: A's storm is late-phase; let B/C/D finish before it lands
"$B" --horizon 49152 --seed 1 --thermal 0 --out B_cold_s1 > B.log 2>&1 &
"$B" --horizon 49152 --seed 2 --thermal 4096 --out C_th_s2 > C.log 2>&1 &
"$B" --horizon 8192 --seed 1 --thermal 4096 --pass --out D_pass_s1 > D.log 2>&1 &
wait
cd ..
python3 analyze.py flights/A_th_s1 flights/B_cold_s1 flights/C_th_s2 flights/D_pass_s1 > analysis.json
echo "--- headline numbers ---"
python3 - <<'EOF'
import json
d = json.load(open("analysis.json"))
for arm, r in d.items():
    g = r["global"]
    print(arm, "contacts", g["contacts"], "maxk", g["maxk"], "dead", r["n_dead"],
          "firstU/D", r["first_U"], r["first_D"], "lam", r.get("p4", {}).get("lam"),
          "remnant", g["n_in_end"], "late c/ch", round(g["contacts_per_ch_late"]),
          "clamp-among-dead", r.get("p1", {}).get("n_with_clamp"),
          "spearman", r.get("eps_ct_spearman"), "De/ct", r["p2"]["De_per_contact"])
EOF
