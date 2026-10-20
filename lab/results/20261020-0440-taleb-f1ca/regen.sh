#!/bin/bash
# Regen 20261020-0440-taleb-f1ca (v4: the disarm channel as an exactly-safe publish floor).
# Applies work/patch.diff (541d's gate+v3+instrument, verbatim, plus this run's v4 change in
# finalize()) to the shipped tree, builds once, and flies every block the dossier cites:
# E1 reproducer (3 arms, sequential), the quiet paired protocol (8 seeds x shipped/v4),
# the 4-way and 12-way crush blocks. Fires are wall-clock draws: the fire COUNT may move
# between windows; the deterministic claims (v4 never fires, present ratios, the equality
# law) regenerate. ~5 min on 8 vCPU.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../../.." && pwd)
cd "$ROOT"
R=$HERE
D=$R/work/draws
mkdir -p "$D"
rm -f "$D"/*.err "$D"/*_rc.txt 2>/dev/null || true
B=${CARGO_TARGET_DIR:-target}/release/examples/exposure
git apply --check "$R/work/patch.diff" 2>/dev/null || git apply -R "$R/work/patch.diff" >/dev/null 2>&1 || true
git apply "$R/work/patch.diff"
cargo build -p emergent-allocator --release --offline --examples
run() { # arm seed block (one stderr file per draw)
  local arm=$1 s=$2 blk=$3; local g=0; [ "$arm" != shipped ] && g=1
  local extra=""; [ "$arm" = "v3" ] && extra="ESE_V3=1"
  env $extra "$B" battle "$s" 2400 32 8192 0.5 24 8704 4.5 "$g" 2>"$D/${blk}_${arm}_s$s.err" || echo "rc=$? ${blk}_${arm}_s$s" >> "$D/rc.txt"
}

echo "== E1 reproducer s19 (sequential, quiet)"
for arm in shipped v3 v4; do run $arm 19 e1; done
echo "== quiet paired protocol (sequential)"
for s in 11 13 15 17 19 21 23 25; do for arm in shipped v4; do run $arm $s quiet; done; done
echo "== 4-way and 12-way crush blocks (background, then wait)"
for s in 11 19 21 23; do for arm in shipped v4; do run $arm $s mid & done; done; wait
for s in 11 19 21 23; do for arm in shipped v3 v4; do run $arm $s crush & done; done; wait

echo "== summary"
for f in "$D"/*.err; do a=$(basename "$f" .err)
  done=$(grep -m1 "^done" "$f" | grep -oE "present [0-9]+|rollbacks [0-9]+" | tr '\n' ' ')
  fire=$(grep -c FIRE "$f" || true); echo "$a fire=$fire $done"
done | sort
echo "== equality law on gated draws (all m<=0, out empty):"
grep -h "^RB " "$D"/*v4*.err | grep -oE "m=-?[0-9]+" | sort -t= -k2 -g | tail -1
echo "out= nonempty: $(grep -h '^RB ' "$D"/*v4*.err | grep -vc 'out=\[\]')  |  fires on gated draws: $(grep -l FIRE "$D"/*v4*.err "$D"/*v3*.err 2>/dev/null | wc -l)"
grep -h FIRE "$D"/*.err || echo "no fires in this window (race)"
