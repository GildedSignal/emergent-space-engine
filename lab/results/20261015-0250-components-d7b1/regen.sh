#!/bin/sh
# Regenerates every number in dossier.md from shipped code + work/patch.diff (applied first).
# The A/B: PATCHED = work/patch.diff applied; SHIPPED = the two source files reverted.
# ≤ 15 min on this box (build ~40 s per side, benches < 1 s, flights ~5 s per side).
set -e
cd "$(dirname "$0")/../../.."
OUT=lab/results/20261015-0250-components-d7b1/out
mkdir -p "$OUT"
cp lab/results/20261015-0250-components-d7b1/work/bindfloor.rs crates/universe/examples/bindfloor.rs
cp lab/results/20261015-0250-components-d7b1/work/bindflight.rs crates/universe/examples/bindflight.rs
RUN="cargo run --release -q -p emergent-universe"

echo "== PATCHED (work/patch.diff applied) =="
git apply lab/results/20261015-0250-components-d7b1/work/patch.diff || true
{ echo "--- belt (tuned)"; $RUN --example bindfloor;
  echo "--- strong (held out)"; $RUN --example bindfloor 51966 strong;
  echo "--- belt seed 1337 (held out)"; $RUN --example bindfloor 1337;
  echo "--- strong seed 1337 (held out)"; $RUN --example bindfloor 1337 strong; } | tee "$OUT/bindfloor-patched.txt"
$RUN --example bindflight 1000 4000000000 | tee "$OUT/bindflight-patched.txt"

echo "== SHIPPED (patch reverted) =="
git checkout crates/space/src/binding.rs crates/universe/src/bind.rs
{ echo "--- belt (tuned)"; $RUN --example bindfloor;
  echo "--- strong (held out)"; $RUN --example bindfloor 51966 strong;
  echo "--- belt seed 1337 (held out)"; $RUN --example bindfloor 1337;
  echo "--- strong seed 1337 (held out)"; $RUN --example bindfloor 1337 strong; } | tee "$OUT/bindfloor-shipped.txt"
$RUN --example bindflight 1000 4000000000 | tee "$OUT/bindflight-shipped.txt"

echo "== identity checks =="
grep -h "Bound digest" "$OUT/bindfloor-patched.txt" > "$OUT/digests-patched.txt"
grep -h "Bound digest" "$OUT/bindfloor-shipped.txt" > "$OUT/digests-shipped.txt"
diff "$OUT/digests-patched.txt" "$OUT/digests-shipped.txt" && echo "BOUND DIGESTS IDENTICAL"
diff "$OUT/bindflight-patched.txt" "$OUT/bindflight-shipped.txt" && echo "FLIGHT DIGEST+COUNTERS IDENTICAL"
git apply lab/results/20261015-0250-components-d7b1/work/patch.diff || true
echo done
