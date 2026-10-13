#!/bin/sh
# Regenerates every number in dossier.md from the shipped tree plus work/patch.diff
# (scenario.rs: the parameterized player start; the lam_star probe example).
# Wall ~4 min on the shared 8-vCPU runner (build ~1 min, grid 99 s, held-out 30 s,
# determinism recheck ~15 s). Every physics column is settle-based and deterministic
# (fixed seed 1, brake at tick 2^24, checks every 2^24): a rerun reproduces each
# grid's rows bit for bit apart from the [..s wall] field.
set -e
cd "$(dirname "$0")/../../.."
R=lab/results/20261013-1249-spacex-5b98
git apply --check "$R/work/patch.diff" 2>/dev/null || { echo "patch already applied or tree dirty — continuing"; }
git apply "$R/work/patch.diff" 2>/dev/null || true
[ -f crates/universe/examples/lam_star.rs ] || cp "$R/lam_star.rs" crates/universe/examples/lam_star.rs
cargo build --release -p emergent-universe --example lam_star
T="${CARGO_TARGET_DIR:-target}/release/examples/lam_star"
# 1. the controls, the r/R bisections (L0–L4), retro, and the e-axis (the post-hoc grid)
"$T" grid 33 | tee "$R/grid-regen.txt"
# 2. the held-out predictions' flights
{ "$T" bisect 1 0 0.6 1.5 6; "$T" bisect 2 1 0.6 1.2 5; "$T" bisect 0 0 0.3 2 8; "$T" one 1.01 0 0.0 5; "$T" one 1.01 0 0.0 6; } | tee "$R/heldout-regen.txt"
# 3. determinism: one full bisection rerun must be bit-identical in its physics columns
"$T" bisect 2 0 0.0 1.2 5 | sed 's/ \[[0-9.]*s wall\]//' | sed -n '/-- bisect/,$p' > /tmp/det.$$
# the L2 e=0 bisect rows also appear inside grid-regen.txt (same invocation order as the run):
sed -n '/-- bisect L2 retro=false e=0 in \[1.2, 5\]/,/^$/p' "$R/grid-regen.txt" | sed 's/ \[[0-9.]*s wall\]//' > /tmp/grid-l2.$$
if diff -q /tmp/grid-l2.$$ /tmp/det.$$ >/dev/null; then echo "DETERMINISM: L2 bisect rerun bit-identical"; else echo "DETERMINISM: DIFFERS — inspect"; diff /tmp/grid-l2.$$ /tmp/det.$$; fi
rm -f /tmp/det.$$ /tmp/held.$$ /tmp/grid-l2.$$
echo "--- compare against the run's own outputs (physics columns must match; wall fields differ):"
for f in grid heldout; do
  sed 's/ \[[0-9.]*s wall\]//' "$R/$f-regen.txt" > /tmp/a.$$; sed 's/ \[[0-9.]*s wall\]//' "$R/$f.txt" > /tmp/b.$$
  diff /tmp/b.$$ /tmp/a.$$ >/dev/null && echo "$f: IDENTICAL" || { echo "$f: DIFFERS — inspect above"; diff /tmp/b.$$ /tmp/a.$$ | head -20; }
done
rm -f /tmp/a.$$ /tmp/b.$$
