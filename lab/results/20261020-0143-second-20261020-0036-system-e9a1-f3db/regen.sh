#!/bin/sh
# Regenenerates every number in dossier.md from the shipped code + work/patch.diff (print-only
# ES_ITEM_PROBE probe + ee4d's env-gated ES_ROOT_STREAM cure/control, carried verbatim).
# ~5 min: one build + seven flights (each 20 s of wall flight on the nladder scene).
set -e
cd "$(dirname "$0")/../../.."   # the repo root
out="lab/results/20261020-0143-second-20261020-0036-system-e9a1-f3db/work/out"
mkdir -p "$out"

# The patch is applied by the runner before this runs; apply it ourselves if run standalone.
if ! grep -q "fn item_probe" crates/universe/src/universe.rs; then
  git apply "lab/results/20261020-0143-second-20261020-0036-system-e9a1-f3db/work/patch.diff"
fi

cargo build --release -p emergent-universe --example nladder
B="${CARGO_TARGET_DIR:-target}/release/examples/nladder"

# The seven arms: disease (d), ee4d's cure (c, ES_ROOT_STREAM=1), its naive control (n),
# and the coast control. Shipped scene, seed 1, rtf 1000, 12 ms budget, 20 s wall.
run() { tag=$1; shift; echo "=== $tag: $*"; env "$@" timeout 180 "$B" 100000 burn 20 1000 12 > "$out/$tag.log" 2> "$out/$tag.err" || true; grep -E "^worst frames|^ladder:|^game " "$out/$tag.log"; }
run2() { tag=$1; shift; echo "=== $tag (2e5): $*"; env "$@" timeout 240 "$B" 200000 burn 20 1000 12 > "$out/$tag.log" 2> "$out/$tag.err" || true; grep -E "^worst frames|^ladder:|^game " "$out/$tag.log"; }
run  d1e5 ES_ITEM_PROBE=1
run  c1e5 ES_ITEM_PROBE=1 ES_ROOT_STREAM=1
run  n1e5 ES_ITEM_PROBE=1 ES_ROOT_STREAM=naive
run2 d2e5 ES_ITEM_PROBE=1
run2 c2e5 ES_ITEM_PROBE=1 ES_ROOT_STREAM=1
run2 n2e5 ES_ITEM_PROBE=1 ES_ROOT_STREAM=naive
echo "=== d1e5c (coast control)"
ES_ITEM_PROBE=1 timeout 180 "$B" 100000 coast 20 1000 12 > "$out/d1e5c.log" 2> "$out/d1e5c.err" || true
grep -E "^worst frames|^ladder:|^game " "$out/d1e5c.log"

# The census: worst player item, pull census, worst frame, ships frame — per arm.
echo; echo "===== census (awk -f work/sum.awk <arm>.err) ====="
cd "lab/results/20261020-0143-second-20261020-0036-system-e9a1-f3db/work"
for a in d1e5 c1e5 n1e5 d2e5 c2e5 n2e5 d1e5c; do echo "--- $a"; awk -f sum.awk "out/$a.err"; done

# The premise check on e9a1's own committed record (read-only, from the branch):
echo; echo "===== e9a1's own .err files on its branch (root pulls) ====="
for f in arm_1e5_burn arm_2e5_burn arm_100000_coast20; do
  git show "origin/claude/lab-20261020-0036-system-e9a1:lab/results/20261020-0036-system-e9a1/work/$f.err" 2>/dev/null \
    | awk -v f="$f" '/^pull_wave/ && /children_only=false/ {n++; split($NF,k,"="); p=k[2]+0; tot+=p; if(p>0)pos++; if(p>m)m=p} END{printf "%s: root calls=%d (>0: %d) pulled_total=%d max=%d\n", f, n+0, pos+0, tot+0, m+0}'
done
