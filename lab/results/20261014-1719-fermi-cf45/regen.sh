#!/usr/bin/env bash
# Regenenerates every number in dossier.md (run 20261014-1719-fermi-cf45).
# The runner applies work/patch.diff (adds crates/universe/examples/cadence.rs) before this runs;
# the copy below is belt and braces for a checker starting from a clean tree.
set -euo pipefail
D="$(cd "$(dirname "$0")" && pwd)"
cd "$D/../../.."
if [ ! -f crates/universe/examples/cadence.rs ]; then cp "$D/cadence.rs" crates/universe/examples/cadence.rs; fi
cargo build --release -p emergent-universe --example cadence 2>&1 | grep -E "^error" && exit 1 || true
cargo run --release -p emergent-universe --example cadence -- 4000    2>/dev/null > "$D/cadence-4000.txt"
cargo run --release -p emergent-universe --example cadence -- 4000 11 2>/dev/null | grep -E 'belt \(root|quartile|advanced|P_D|source 0' > "$D/cadence-4000-seed11.txt"
cargo run --release -p emergent-universe --example cadence -- 1000 3  2>/dev/null | grep -E 'belt \(root|quartile|advanced|P_D' > "$D/cadence-1000-seed3.txt"
python3 "$D/compose.py" > "$D/compose-out.txt"
echo "regen OK: cadence-4000.txt, cadence-4000-seed11.txt, cadence-1000-seed3.txt, compose-out.txt"
