#!/usr/bin/env bash
# Regenerates every number in dossier.md: applies work/patch.diff (adds
# crates/universe/examples/beltcensus.rs), builds and runs the census suite.
# Wall time ~1 min on 8 vCPU Linux; peak memory < 100 MB.
set -euo pipefail
cd "$(dirname "$0")/../../.."   # the repo root
git apply --allow-empty "$(dirname "$0")/work/patch.diff" 2>/dev/null || true  # idempotent if already applied
cargo run --release -p emergent-universe --example beltcensus -- 1000002 1,2,3 1.0 shipped 2>/dev/null
cargo run --release -p emergent-universe --example beltcensus -- 1000002 1 0.5 shipped 2>/dev/null | grep 'arm='
cargo run --release -p emergent-universe --example beltcensus -- 1000002 1 2 shipped 2>/dev/null | grep 'arm='
cargo run --release -p emergent-universe --example beltcensus -- 1000002 1 4 shipped 2>/dev/null | grep 'arm='
cargo run --release -p emergent-universe --example beltcensus -- 1000002 1,2 1.0 3.0:3.5 2>/dev/null
cargo run --release -p emergent-universe --example beltcensus -- 1000002 1,2 1.0 1.4:2.4 2>/dev/null | grep 'arm='
cargo run --release -p emergent-universe --example beltcensus -- 3000 1,2 1.0 shipped 2>/dev/null | grep 'arm='
