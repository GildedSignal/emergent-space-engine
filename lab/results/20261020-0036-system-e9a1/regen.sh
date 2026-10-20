#!/bin/sh
# Regen for 20261020-0036-system-e9a1: the pair-cone census at the ladder's wall rungs.
# Applies work/patch.diff (print-only, env-gated ES_CONE_PROBE), builds, flies the four arms,
# prints the census. ~5 min.
set -e
cd "$(dirname "$0")/../../.." || exit 1
RUN=lab/results/20261020-0036-system-e9a1
git apply --check "$RUN/work/patch.diff" 2>/dev/null && git apply "$RUN/work/patch.diff" || echo "patch already applied or tree dirty (continuing)"
cargo build --release -p emergent-universe --example nladder
BIN="${CARGO_TARGET_DIR:-target}/release/examples/nladder"
cd "$RUN/work"
for spec in "100000 burn 20" "100000 coast 20" "200000 burn 20" "100000 burn 40"; do
  set -- $spec
  ES_CONE_PROBE=1 timeout 95 "$BIN" "$1" "$2" "$3" 1000 12 > "arm_$1_$2$3.log" 2> "arm_$1_$2$3.err" || true
done
echo "=== census (scans / candidates / skip frac / passers / hits / violations) ==="
for f in arm_100000_burn20 arm_100000_coast20 arm_200000_burn20 arm_100000_burn40; do
  awk -v name="$f" '/^cone_scan/{n++;for(i=1;i<=NF;i++){split($i,a,"=");v[a[1]]=a[2]+0}c+=v["cands"];s+=v["skip_cert"];h+=v["hits"]} END{printf "%s scans %d cands %d skip %.4f passers %d hits %d\n", name,n,c,(n?s/c:0),c-s,h}' "$f.err"
  printf "  violations: %s\n" "$(grep -c VIOLATION "$f.err" || true)"
done
echo "=== pulls ==="
for f in arm_100000_burn20 arm_100000_coast20 arm_200000_burn20 arm_100000_burn40; do
  awk -v name="$f" '/^pull_wave/{split($4,a,"=");p=a["pulled"]+0; if($3=="children_only=false"){f0++;fp+=p}else{t0++;tp+=p}} END{printf "%s root calls %d pulled %d | child calls %d pulled %d\n",name,f0,fp,t0,tp}' "$f.err"
done
echo "=== ladder lines (frames/memory class) ==="
grep -h ladder: arm_*.log | sed 's/.*ladder:/ladder:/'
