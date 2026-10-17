#!/usr/bin/env bash
# Regenerates every number in dossier.md (run 20261017-0839-fermi-2b89).
# Applies work/patch.diff (adds the print-only example crates/universe/examples/enc_quantum.rs),
# builds it on shipped code, runs it (probe.out), and recomposes the ledger (compose.out).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
root="$(git -C "$here" rev-parse --show-toplevel)"
cd "$root"
[ -f crates/universe/examples/enc_quantum.rs ] || git apply "$here/work/patch.diff"
cargo build --release -p emergent-universe --example enc_quantum
cargo run --release -p emergent-universe --example enc_quantum > "$here/probe.out" 2>/dev/null
python3 "$here/compose.py" > "$here/compose.out"
echo "--- anchors (probe.out) ---";   grep -E "ev=|quantum|fires|D\*|b_flip|CONTROL|2\^12" "$here/probe.out" | head -24
echo "--- ledger (compose.out) ---";  cat "$here/compose.out"
