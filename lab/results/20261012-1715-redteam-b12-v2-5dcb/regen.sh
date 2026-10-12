#!/usr/bin/env bash
# Regenerates every number in the dossier from the candidate branch plus this
# run's patch. Total wall time ~5 min on 8 cores. Fails loudly if the patch
# does not land or the red-team module is missing from the build.
set -euo pipefail
RUN="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$RUN/../../.." && pwd)"
WT="$(mktemp -d /tmp/rtb12-regen-XXXX)"
rmdir "$WT"
trap 'git -C "$ROOT" worktree remove --force "$WT" >/dev/null 2>&1 || rm -rf "$WT"' EXIT

git -C "$ROOT" worktree add --detach "$WT" wt/cx-b12-v2 >/dev/null
echo "worktree at $WT"
git -C "$WT" apply "$RUN/work/patch.diff"
test -f "$WT/xtask/src/behave/rt_b12.rs" || { echo "FATAL: patch did not create rt_b12.rs" >&2; exit 1; }
grep -q "mod rt_b12" "$WT/xtask/src/behave/mod.rs" || { echo "FATAL: mod wiring missing" >&2; exit 1; }
echo "patch landed"
cd "$WT"
export CARGO_TARGET_DIR="$WT/target"
echo "target dir: $CARGO_TARGET_DIR"
cargo test --release -p xtask rt_b12::rt_ -- --nocapture --test-threads=1 2>&1 | tee "$RUN/work/rt-all.log"
echo "--- verdict summary"
grep -E "VERDICT|official gate" "$RUN/work/rt-all.log"
echo "--- receipt sha256 cross-check (must match artifacts/evidence/cx-b12-v2/receipt.json)"
sha256sum xtask/src/behave/b12_corpus.json xtask/src/behave/b12_stat.rs xtask/src/behave/handoff.rs
