#!/usr/bin/env bash
# Regenerates the H_live record of run 20261007-2344-spacex-dbf9 from the patch in
# this folder (recovered from the runner's dangling stash objects a2246852 + 8e5e31a2,
# whose bytes were never published on the branch). Applies to base a838a28, builds,
# runs the five evidence rows plus the held-out seed, and re-derives the 10^9
# extrapolation. Usage: bash regen.sh [workdir] (default /tmp/hlive-regen).
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
repo=$(git -C "$here/../../../.." rev-parse --show-toplevel)
base=a838a284a27a6813434362cc2adfde946d2085db
dir=${1:-/tmp/hlive-regen}

git -C "$repo" worktree add --detach "$dir" "$base"
trap 'git -C "$repo" worktree remove --force "$dir"' EXIT
cd "$dir"
git apply "$here/live-ledger.patch"
CARGO_TARGET_DIR=~/lab-target-2 cargo build --release -p xtask
xt=~/lab-target-2/release/xtask

for args in "--rtf 1 --seconds 30 --seed 1" \
            "--rtf 100 --seconds 30 --seed 1" \
            "--rtf 100 --seconds 30 --seed 5" \
            "--rtf 1000 --seconds 30 --seed 1" \
            "--rtf 10000 --seconds 20 --seed 1" \
            "--rtf 10000 --seconds 20 --seed 5"; do
  echo "== xtask universe --bench --unpaced $args"
  "$xt" universe --bench --unpaced $args
done
CARGO_TARGET_DIR=~/lab-target-2 cargo test --release -p emergent-universe 2>&1 | tail -3
