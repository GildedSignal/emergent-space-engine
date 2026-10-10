#!/bin/sh
# Regenerates every number in dossier.md from shipped code (each command < 60 s).
set -e
cd "$(dirname "$0")"
# validation: closed forms vs exact transport (incl. circular analytic Delta psi)
python3 marck.py validate \
  '[{"rp":100,"e":0.3},{"rp":10,"e":0.6},{"rp":30,"e":0.0},{"rp":1e4,"e":0.6},{"rp":1e6,"e":0.3}]' \
  > val.json
# held-out sweeps (predictions.md predates these files)
python3 marck.py sweep \
  '[{"rp":10,"e":0.0},{"rp":30,"e":0.0}]' e0a
python3 marck.py sweep \
  '[{"rp":100,"e":0.0},{"rp":1e4,"e":0.0}]' e0b
python3 marck.py sweep \
  '[{"rp":10,"e":0.3},{"rp":30,"e":0.3}]' e03a
python3 marck.py sweep \
  '[{"rp":100,"e":0.3},{"rp":1e4,"e":0.3},{"rp":1e6,"e":0.3}]' e03b
python3 marck.py sweep \
  '[{"rp":10,"e":0.6},{"rp":30,"e":0.6}]' e06a
python3 marck.py sweep \
  '[{"rp":100,"e":0.6},{"rp":1e4,"e":0.6}]' e06b
python3 analyze2.py > analysis.txt
