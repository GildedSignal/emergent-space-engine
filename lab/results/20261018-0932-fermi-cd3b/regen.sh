#!/usr/bin/env bash
# Regen for 20261018-0932-fermi-cd3b: every dossier number from shipped code + this run's
# scripts. No patch needed (work/patch.diff is empty: no source was edited).
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
cargo build --release -q -p emergent-universe --example belt_first
python3 lab/results/20261018-0932-fermi-cd3b/ledger.py | tee lab/results/20261018-0932-fermi-cd3b/ledger-out.json
