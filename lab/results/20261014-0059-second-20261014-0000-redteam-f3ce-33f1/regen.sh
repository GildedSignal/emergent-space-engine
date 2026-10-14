#!/bin/sh
# Regenerates every number in dossier.md (20261014-0059-second-...-redteam-f3ce-33f1).
# work/patch.diff (applied by the runner before this runs) carries:
#   - crates/lattice/src/relativity.rs: the pair-carry candidate behind RUNG_PAIR_CARRY=1
#   - crates/lattice/examples/rt_r5.rs: the probe
# The .rs copy beside this script is the fallback if the patch is absent.
# Total ~4 min. Each command < 60 s.
set -e
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261014-0059-second-20261014-0000-redteam-f3ce-33f1

# 1. restore the probe if the patch is missing
if ! grep -q "pair_carry_on" crates/lattice/src/relativity.rs 2>/dev/null; then
  git apply "$R/work/patch.diff" 2>/dev/null || cp "$R/rt_r5.rs" crates/lattice/examples/rt_r5.rs
fi

# 2. build
(cd crates/lattice && cargo build --release --example rt_r5)

# 3. the rung's four cells at the engine's Q (2^20), seeds 0-4, then held-out 11-15
cd crates/lattice
run() { cargo run --release --quiet --example rt_r5 -- "$@" 2>/dev/null; }
run rung pair1000  1048576 0 1 2 3 4  | tee ../../$R/rung-shipped-pair1000.log
run rung pairequal 1048576 0 1 2 3 4  | tee ../../$R/rung-shipped-pairequal.log
RUNG_PAIR_CARRY=1 cargo run --release --quiet --example rt_r5 -- rung pair1000  1048576 0 1 2 3 4 2>/dev/null | tee ../../$R/rung-paircarry-pair1000.log
RUNG_PAIR_CARRY=1 cargo run --release --quiet --example rt_r5 -- rung pairequal 1048576 0 1 2 3 4 2>/dev/null | tee ../../$R/rung-paircarry-pairequal.log
run rung pair1000  1048576 11 12 13 14 15 | tee ../../$R/heldout-shipped.log
RUNG_PAIR_CARRY=1 cargo run --release --quiet --example rt_r5 -- rung pair1000 1048576 11 12 13 14 15 2>/dev/null | tee ../../$R/heldout-paircarry.log

# 4. metrics.json (median over seeds of per-seed |sum_res|/KE, per the frozen rung)
#    and the verdict
cd ../../
python3 - "$R" <<'EOF'
import json, re, sys
R = sys.argv[1]
def med(path):
    vals = []
    for line in open(path):
        m = re.search(r"res_over_KE=(-?[0-9.e+-]+)", line)
        if line.startswith("rung ") and " seed=" in line and m:
            vals.append(abs(float(m.group(1))))
    vals.sort()
    return vals[len(vals)//2]
m = {
  "shipped":    {"frac_1000_1_median": med(f"{R}/rung-shipped-pair1000.log"),
                 "frac_equal_median":  med(f"{R}/rung-shipped-pairequal.log")},
  "pair-carry": {"frac_1000_1_median": med(f"{R}/rung-paircarry-pair1000.log"),
                 "frac_equal_median":  med(f"{R}/rung-paircarry-pairequal.log")},
}
json.dump(m, open(f"{R}/metrics.json","w"), indent=1)
print(json.dumps(m))
EOF
python3 lab/verdict.py "$R/r5-contact-carry.md" "$R/metrics.json" | tee "$R/verdict.txt"

# 5. the shipped path is untouched: full suite green with the flag off; one digest
#    test differs with it on (the law change)
(cd crates/lattice && cargo test --release 2>&1 | grep -c "test result: ok")
RUNG_PAIR_CARRY=1 sh -c 'cd crates/lattice && cargo test --release 2>&1 | grep -E "test result:"' | tee "$R/tests-flag-on.txt"
