#!/usr/bin/env bash
# Regen: rebuilds every dossier number from shipped code + work/patch.diff + the matrix flights.
# ~14 min: build (~17 s warm) + 15 sequential flights + gs_analysis.py. Idempotent: existing
# flight outputs are kept, so a partial regen resumes. Forces CARGO_TARGET_DIR=lab-target-2
# (the session env may point at a stale unpatched binary elsewhere).
set -u
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT" || exit 1
RUN=lab/results/20261020-0440-second-20261020-0229-fermi-476d-ca63
export CARGO_TARGET_DIR=/home/glmlab/lab-target-2

git apply "$RUN/work/patch.diff" 2>/dev/null || echo "patch already applied (regen rerun)"
cargo build --release -p emergent-universe --example nladder || exit 1

bash "$RUN/work/fly_matrix.sh"
echo "--- gs analysis ---"
python3 "$RUN/work/gs_analysis.py"
