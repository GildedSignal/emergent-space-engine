#!/usr/bin/env bash
# Regen for 20261017-1240-quant-ceb2: every dossier number, from the patched tree.
# The patch adds only crates/universe/examples/bwfloor.rs (a print-only example; the
# engine, the law and the flights are untouched). ~2-3 min on the lab runner.
set -euo pipefail
cd "$(dirname "$0")/../../.."

echo "== sizes: struct sizes and allocator-counted compile write bill (evidence 1) =="
cargo run --release -p emergent-universe --example bwfloor -- sizes

echo "== micro: hot/cold read and compile, code-vs-data split (evidence 3) =="
cargo run --release -p emergent-universe --example bwfloor -- micro

echo "== wave N=3000 and held-out N=10000: per-kick allocation traffic (evidence 2) =="
cargo run --release -p emergent-universe --example bwfloor -- wave 3000 20000
cargo run --release -p emergent-universe --example bwfloor -- wave 10000 20000

echo "Roofline arithmetic (evidence 4):"
python3 - <<'EOF'
for tag, b in [("N=3000", 18822), ("N=10000", 12205)]:
    ns68 = b / 68e9 * 1e9        # M1-class roof
    ns17 = b / 17e9 * 1e9        # one core's measured share here
    print(f"{tag}: {b} B/kick -> {ns68:.0f} ns at 68 GB/s, {ns17:.0f} ns at 17 GB/s; "
          f"vs 50-165 us compute: {50e3/ns68:.0f}-{165e3/ns68:.0f}x under the roof")
EOF
