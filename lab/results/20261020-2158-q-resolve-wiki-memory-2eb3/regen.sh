#!/usr/bin/env bash
# Regenerates every number in dossier.md from the repo, the run branches and this
# run's files. No network, no writes outside a temp dir. Well under 1 minute.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec python3 lab/results/20261020-2158-q-resolve-wiki-memory-2eb3/resolve_check.py
