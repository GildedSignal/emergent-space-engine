#!/bin/sh
# Regen: every number in dossier.md, from shipped code + work/patch.diff (applied by the runner).
# Total wall: build ~40 s (cold) + run ~21 s. Linux x86, release.
set -e
cd "$(dirname "$0")/../../.."  # repo root
cd crates/universe
cargo run --release --example calendar 2>/dev/null
