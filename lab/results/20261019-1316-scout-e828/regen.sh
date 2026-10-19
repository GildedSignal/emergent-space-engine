#!/bin/sh
# Regen for 20261019-1316-scout-e828. Assumes work/patch.diff (the epochflux
# example) is applied. Rebuilds every number in dossier.md: ~2 min, 1 core, <200 MB.
set -e
cd "$(dirname "$0")/../../.."   # repo root
cargo build --release --example epochflux -p emergent-encounters 2>&1 | grep -E "^error" && exit 1 || true
R=""
for c in /home/glmlab/lab-target-3/release/examples/epochflux /home/glmlab/lab-target-2/release/examples/epochflux; do
  [ -x "$c" ] && R="$c" && break
done
if [ -z "$R" ]; then R=$(find / -name epochflux -type f -path "*release/examples*" 2>/dev/null | head -1); fi
D=lab/results/20261019-1316-scout-e828
timeout 120 $R book 20261018 1e-4        > $D/book.txt
timeout 120 $R smallh 20261018 1e-4      > $D/smallh.txt
# decisive streams: 3 kappa arms (seed 1), dv0 control, held-out seeds 777 and 5
(timeout 200 $R stream 20261018 1e-4 26 2048 1500 4242
 timeout 200 $R stream 20261018 1e-4 23 2048 1500 4242
 timeout 200 $R stream 20261018 1e-4 20 2048 1500 4242) > $D/stream-s1.txt
(timeout 200 $R stream 20261018 1e-4 0 512 1500 4242
 timeout 200 $R stream 777 1e-4 23 2048 1500 4242
 timeout 200 $R stream 5 1e-4 23 2048 1500 4243)           > $D/stream-ctl.txt
echo REGEN-DONE
