#!/bin/sh
# Regen for 20261019-1551-fermi-73b5. work/patch.diff (applied by the runner
# before this runs) carries e828's epochflux example verbatim; work/epochflux.rs
# is the fallback copy. Rebuilds every number in dossier.md: ~1-3 min, 1 core,
# <300 MB. Sections: (A-E) work/ledger.py arithmetic; (F) e828's anchors + leak
# surface reproduced on this box.
set -e
cd "$(dirname "$0")/../../.."   # repo root
D=lab/results/20261019-1551-fermi-73b5
mkdir -p crates/encounters/examples
[ -f crates/encounters/examples/epochflux.rs ] || \
  cp $D/work/epochflux.rs crates/encounters/examples/epochflux.rs
cargo build --release --example epochflux -p emergent-encounters 2>&1 | grep -E "^error" && exit 1 || true
R=""
for c in target/release/examples/epochflux /home/glmlab/lab-target-*/release/examples/epochflux; do
  [ -x "$c" ] && R="$c" && break
done
[ -z "$R" ] && R=$(find / -name epochflux -type f -path "*release/examples*" 2>/dev/null | head -1)
O=$D/work/out; mkdir -p $O
timeout 120 $R book 20261018 1e-4   > $O/book.txt
timeout 120 $R smallh 20261018 1e-4 > $O/smallh.txt
timeout 500 $R stream 777 1e-4 23 2048 1500 4242     > $O/stream-777-q23.txt
timeout 500 $R stream 20261018 1e-4 23 2048 1500 4242 > $O/stream-s1-q23.txt
timeout 300 $R stream 20261018 1e-4 0 512 1500 4242   > $O/stream-dv0.txt
cd $D/work && python3 ledger.py | tee out/ledger.txt
echo REGEN-DONE
