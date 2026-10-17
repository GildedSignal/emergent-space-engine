#!/bin/sh
# Regen for 20261017-1149-system-859b (system lens: the boundary walk vs the standing key).
# Applies work/patch.diff, builds the two examples, and regenerates every dossier number.
# Total wall: ~7-9 min on the lab's 8-vCPU Linux runner.
set -e
cd "$(dirname "$0")/../../.."   # repo root (lab/results/<run>/regen.sh)
RUN=lab/results/20261017-1149-system-859b

git apply --whitespace=nowarn "$RUN/work/patch.diff" 2>/dev/null || git diff --stat || true
cargo build --release -p emergent-universe --example nladder --example ladder_digest --features prof 2>&1 | tail -1

echo '== digests: OFF vs HOIST (must be identical lines; parity check at the end) =='
cargo run --release -p emergent-universe --example ladder_digest --features prof > "$RUN/work/digest_off.txt" 2>&1
ES_KEY_HOIST=1 cargo run --release -p emergent-universe --example ladder_digest --features prof > "$RUN/work/digest_on.txt" 2>&1
diff <(grep -v ' s\]' "$RUN/work/digest_off.txt") <(grep -v ' s\]' "$RUN/work/digest_on.txt") && echo 'DIGEST PARITY: identical (hashes, kicks, encounters, contacts)' || echo 'DIGEST PARITY: DIFFER (kill)'
echo '== verify arm: predicate vs walked radius on every boundary (belt + locals) =='
ES_KEY_HOIST=verify cargo run --release -p emergent-universe --example nladder --features prof 30000 coast 30 300 2>&1 | grep -E 'hoist:|game |frames after'

echo '== timed arms (sequential, same machine class): OFF then HOIST =='
cargo run --release -p emergent-universe --example nladder --features prof 100000 coast 45 300 2>&1 | grep -E 'hoist:|game |frames after|item: boundary|item: kick \(clock\)|memory' > "$RUN/work/nl_off.txt"
cat "$RUN/work/nl_off.txt"
ES_KEY_HOIST=1 cargo run --release -p emergent-universe --example nladder --features prof 100000 coast 45 300 2>&1 | grep -E 'hoist:|game |frames after|item: boundary|item: kick \(clock\)|memory' > "$RUN/work/nl_on.txt"
cat "$RUN/work/nl_on.txt"

git checkout -- crates/universe/src/step.rs crates/universe/src/universe.rs crates/universe/examples/nladder.rs 2>/dev/null || true
echo done
