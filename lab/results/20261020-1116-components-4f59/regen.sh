#!/bin/sh
# Regenerates every number in dossier.md from shipped code + this run's patch (applied before it runs).
# Total ~40 s of runs after the release build; peak ~1 GB at N=1e5.
set -e

# Find the workspace root (nearest ancestor holding Cargo.toml) from this script's location,
# whatever directory we are invoked from. The run folder is <root>/lab/results/<id>/.
here="$(cd "$(dirname "$0")" && pwd)"
root="$here"
while [ "$root" != "/" ] && [ ! -f "$root/Cargo.toml" ]; do
  root="$(dirname "$root")"
done
cd "$root"

# The probe (crates/universe/examples/seamscan.rs) rides work/patch.diff. If the runner has not
# already applied it, apply it here, and take it back off at the end so the tree is as we found it.
applied=0
if [ ! -f crates/universe/examples/seamscan.rs ]; then
  git apply "$here/work/patch.diff" || patch -p1 < "$here/work/patch.diff"
  applied=1
fi
cleanup() { [ "$applied" = 1 ] && rm -f crates/universe/examples/seamscan.rs; return 0; }
trap cleanup EXIT INT TERM

cargo build --release -p emergent-universe --example seamscan
{ ./artifacts/runs/frame/state.sh 2>/dev/null || uptime; } || true
cargo run --release -p emergent-universe --example seamscan -- 10000 1000000
cargo run --release -p emergent-universe --example seamscan -- 100000 1000000
