#!/bin/sh
# Regen: every number in dossier.md, from shipped code + work/patch.diff (applied by the runner
# before this runs). ~10 min on 8 vCPU (Linux/x86 shared box: orders of magnitude only).
set -e
cd /home/glmlab/actions-runner/_work/emergent-space-engine/lab-0
R=lab/results/20261016-0612-second-20261016-0504-system-e070-124b
mkdir -p $R/out

cargo build --release -p xtask 2>&1 | tail -1
B=$(cargo metadata --no-deps --format-version 1 | python3 -c "import json,sys; print(json.load(sys.stdin)['target_directory'])")/release/xtask

# 1. The seed ensemble: 8 seeds x {1e4,1e5} x {storm, no-locals} + the wide stagger arms (1e4).
fly(){ name=$1; seed=$2; extra=$3; shift 3
  env ES_ENGINE_ONLY=1 ES_TRACE=1 "$@" $B universe --bench --unpaced --engine-ms 100000 \
      --rtf 1000 --seconds 30 --seed $seed --extra $extra > $R/out/$name.json 2>/dev/null
}
for S in 1 2 3 4 5 6 7 8; do
  for N in 10000 100000; do
    fly storm_s${S}_n${N} $S $N &
    fly noloc_s${S}_n${N} $S $N ES_NO_LOCALS=1 &
    wait
  done
  echo "seed $S done"
done
fly stag26_s3_n10000 3 10000 ES_STAGGER_LOCALS=26
fly stag31_s3_n10000 3 10000 ES_STAGGER_LOCALS=31
fly stag31_s1_n10000 1 10000 ES_STAGGER_LOCALS=31

# 2. The tables (per-frame population split, binding verdicts, stagger engagement).
python3 $R/analyze.py | tee $R/out/analysis.txt

# 3. Off-arm identity: this patch with every env unset vs pristine main (the parent verified
#    5b2d998b... for its half; my additions are inside ES_TRACE blocks and the bits-cap lift).
$B universe --bench --rtf 100 --seconds 20 --seed 1 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['digest'])" > $R/out/patched_off_digest.txt
git stash -q
cargo build --release -p xtask 2>&1 | tail -1
$B universe --bench --rtf 100 --seconds 20 --seed 1 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['digest'])" > $R/out/pristine_digest.txt
git stash pop -q
cargo build --release -p xtask 2>&1 | tail -1
diff $R/out/pristine_digest.txt $R/out/patched_off_digest.txt && echo OFF_ARM_IDENTICAL
