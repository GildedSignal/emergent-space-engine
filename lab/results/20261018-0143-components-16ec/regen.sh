#!/bin/sh
# Regenerates every number in dossier.md. Applies work/patch.diff to the pristine tree,
# builds, runs the exactness probe and the four flight arms, and diffs the digests.
# Linux/x86; orders of magnitude only. ~8 minutes.
set -e
cd "$(dirname "$0")/../../.."
git apply --check lab/results/20261018-0143-components-16ec/work/patch.diff 2>/dev/null && git apply lab/results/20261018-0143-components-16ec/work/patch.diff
cargo build --release -p emergent-universe --example nladder --example bound_probe
BIN=$(cargo metadata --no-deps --format-version 1 | python3 -c "import json,sys; print(json.load(sys.stdin)['target_directory'])")/release/examples
OUT=lab/results/20261018-0143-components-16ec/work
mkdir -p "$OUT"

echo "== exactness probe =="
"$BIN/bound_probe" | tee "$OUT/probe.txt"

echo "== flights (fixed canonical cut 1.2e10 ticks) =="
run() { # name, extra env...
  name=$1; shift
  ( for e in "$@"; do export "$e"; done
    timeout 90 "$BIN/nladder" 10000 "$MODE" 60 1800 2>&1 | grep -E "^bound:|^game " > "$OUT/$name.txt" )
}
MODE=coast run ctl          ES_LIMIT=12000000000
MODE=coast run ctl2         ES_LIMIT=12000000000
MODE=coast run fast         ES_BOUND_RANGE=1 ES_LIMIT=12000000000
MODE=burn  run burn_ctl     ES_LIMIT=12000000000
MODE=burn  run burn_fast    ES_BOUND_RANGE=1 ES_LIMIT=12000000000
MODE=coast run seed7_ctl    ES_SEED=7 ES_LIMIT=12000000000
MODE=coast run seed7_fast   ES_SEED=7 ES_BOUND_RANGE=1 ES_LIMIT=12000000000
cat "$OUT"/ctl.txt "$OUT"/ctl2.txt "$OUT"/fast.txt "$OUT"/burn_ctl.txt "$OUT"/burn_fast.txt "$OUT"/seed7_ctl.txt "$OUT"/seed7_fast.txt
echo "== digest comparisons =="
for a in ctl fast burn_ctl burn_fast seed7_ctl seed7_fast; do d=$(sed -n 's/^bound: digest \([0-9a-f]*\) .*/\1/p' "$OUT/$a.txt"); echo "$a $d"; done
d1=$(sed -n 's/^bound: digest \([0-9a-f]*\) .*/\1/p' "$OUT/ctl.txt"); d2=$(sed -n 's/^bound: digest \([0-9a-f]*\) .*/\1/p' "$OUT/fast.txt")
[ "$d1" = "$d2" ] && echo "COAST: digests identical ($d1)" || echo "COAST: DIGESTS DIFFER"
d1=$(sed -n 's/^bound: digest \([0-9a-f]*\) .*/\1/p' "$OUT/seed7_ctl.txt"); d2=$(sed -n 's/^bound: digest \([0-9a-f]*\) .*/\1/p' "$OUT/seed7_fast.txt")
[ "$d1" = "$d2" ] && echo "SEED7: digests identical ($d1)" || echo "SEED7: DIGESTS DIFFER"
d1=$(sed -n 's/^bound: digest \([0-9a-f]*\) .*/\1/p' "$OUT/burn_ctl.txt"); d2=$(sed -n 's/^bound: digest \([0-9a-f]*\) .*/\1/p' "$OUT/burn_fast.txt")
[ "$d1" = "$d2" ] && echo "BURN: digests identical" || echo "BURN: DIGESTS DIVERGE (the reported held-out failure)"
git checkout -- crates/universe/src/step.rs crates/universe/examples/nladder.rs 2>/dev/null || true
git clean -f crates/universe/examples/bound_probe.rs 2>/dev/null || true
