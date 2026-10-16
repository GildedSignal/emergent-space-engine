#!/usr/bin/env bash
# Regenenerates every number in dossier.md from shipped code + work/patch.diff.
# Total wall: ~3 min (one release build + 4 bench runs of <1 s each).
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root
PATCH=lab/results/20261016-2229-components-a765/work/patch.diff
if [ -f "$PATCH" ]; then git apply "$PATCH" 2>/dev/null || true; fi   # run.sh already applies it in the run tree
cargo build --release -p xtask
X=./target/release/xtask
[ -x "$X" ] || X=$(cargo metadata --no-deps --format-version 1 | python3 -c "import json,sys; print(json.load(sys.stdin)['target_directory'])")/release/xtask
OUT=lab/results/20261016-2229-components-a765
"$X" universe --kick-bench --seed 1  --rtf 100 --seconds 10 > "$OUT/bench-clean-seed1.json"
for sd in 1 7 42; do
  ES_FLOOR_AUDIT=1 "$X" universe --kick-bench --seed $sd --rtf 100 --seconds 10 > "$OUT/bench-audit-seed$sd.json"
done
python3 - "$OUT" <<'EOF'
import json, sys, pathlib
out = pathlib.Path(sys.argv[1])
print("== clean anchor (seed 1) ==")
j = json.loads((out/"bench-clean-seed1.json").read_text())
print("kick_us made   ", json.dumps(j["kick_us"]))
print("kick_us leavers", json.dumps(j["kick_us_leavers"]))
print("memo           ", json.dumps(j["memo"]))
print("== audited rebind decomposition (ES_FLOOR_AUDIT=1) ==")
for sd in (1, 7, 42):
    raw = (out/f"bench-audit-seed{sd}.json").read_text()
    fa = json.loads([l for l in raw.splitlines() if l.startswith('"floor_audit"')][0]
                    .removeprefix('"floor_audit": ').strip())
    n = fa["calls"]
    fit = fa["ns_fit_key"]/n/1e3; comp = fa["ns_compile"]/n/1e3
    tot = fa["ns_phase_residual"]/n/1e3; proto = fa["ns_proto"]/n/1e3
    tail = tot - fit - comp - proto
    print(f"seed {sd:>2}: calls {n}  fit_key {fit:.2f} us  compile {comp:.2f} us  "
          f"tail {tail:.2f} us  proto {proto:.2f} us  rebind_mean {fit+comp+tail:.2f} us")
    print(f"          bit-agree {fa['agree']}  bit-disagree {fa['disagree']} "
          f"(sub-quantum {fa['agree_quantum']}, quantum-level {fa['disagree_quantum']})  "
          f"exact_bigint_path {fa['exact_path']}  circular {fa['circular']}  passages {fa['passages']}")
    print(f"          distinct exact keys {fa['distinct_exact_keys']} / distinct 2^-20-census keys {fa['distinct_quantized_keys']}")
EOF
