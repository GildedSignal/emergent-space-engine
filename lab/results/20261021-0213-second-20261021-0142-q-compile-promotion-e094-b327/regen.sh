#!/usr/bin/env bash
# Regenerates every number in dossier.md from shipped code (pinned commits),
# this folder's scripts, and work/patch.diff (already applied to the tree by
# the runner: lab/wiki.py == pristine 046d8d9c829b + 6ccc-fold.diff + b327-ext.diff).
# Runtime ~2 s. Exits non-zero on any failed assertion.
set -euo pipefail
cd "$(dirname "$0")"
python3 replay.py       # P1–P9: rebuilds work/<box> sandboxes, asserts, writes work/record.json
python3 verify.py       # audits the record against the boxes on disk (no git needed)
# keep the folder small: the boxes are deterministic rebuilds of replay.py
rm -rf work/p1 work/p2 work/p3 work/p4 work/p5 work/p6 work/p7b work/corpus work/corpusP work/variants
echo "regen: done (record in work/record.json)"
