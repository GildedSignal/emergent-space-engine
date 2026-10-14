#!/bin/bash
# Regenerates every number in dossier.md (lab 20261014-2130-second-...-eb2d).
# The runner applies work/patch.diff before this runs; we revert to pristine for the
# baseline phase, then re-apply, then measure. ~9 min on the lab box.
set -e
R="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(git -C "$R" rev-parse --show-toplevel)"
B="$CARGO_TARGET_DIR/release/examples"
BUILD="cargo build --release -p emergent-universe --example ladder_digest --example frame_digest --example jacobi"
flt() { grep -v '\[.*s\]$' "$1"; }

echo "== phase 1: pristine baseline =="
git -C "$ROOT" checkout -- crates/
rm -f "$ROOT/crates/universe/examples/key_dial.rs"
(cd "$ROOT/crates/universe" && $BUILD --example key_dial >/dev/null 2>&1 || true; $BUILD >/dev/null)
"$B/ladder_digest" wave      > "$R/work/pristine_ladder_wave.txt"
"$B/ladder_digest" crossing  > "$R/work/pristine_ladder_crossing.txt"
"$B/frame_digest" 5          > "$R/work/pristine_frame5.txt"
"$B/jacobi" 6 100 6          > "$R/work/pristine_jacobi.txt"

echo "== phase 2: patch, default-neutrality =="
git -C "$ROOT" apply "$R/work/patch.diff"
[ -f "$ROOT/crates/universe/examples/key_dial.rs" ] || cp "$R/key_dial.rs" "$ROOT/crates/universe/examples/"
(cd "$ROOT/crates/universe" && $BUILD --example key_dial >/dev/null)
"$B/ladder_digest" wave      > "$R/work/default_ladder_wave.txt"
"$B/ladder_digest" crossing  > "$R/work/default_ladder_crossing.txt"
"$B/frame_digest" 5          > "$R/work/default_frame5.txt"
ok=1
for f in ladder_wave ladder_crossing frame5; do
  flt "$R/work/pristine_$f.txt" | diff - <(flt "$R/work/default_$f.txt") > /dev/null || ok=0
done
echo "neutrality (default digests == pristine, timing lines aside): $([ $ok = 1 ] && echo IDENTICAL || echo BROKEN)"

echo "== phase 3: the dial =="
"$B/key_dial" 3000 1000 20 > "$R/work/dial_default.txt"
for d in 48,16 33,16 24,16 12,12 12,24 12,28 12,32 16,28 16,32; do
  ES_KEY_BITS=$d "$B/key_dial" 3000 1000 20 > "$R/work/dial_${d//,/_}.txt"
done
for d in 12,24 16,28 16,32 20,36; do
  ES_KEY_BITS=$d "$B/jacobi" 6 100 6 > "$R/work/jacobi_${d//,/_}.txt" 2>&1 || true
done
grep -h . "$R/work/dial_default.txt" "$R/work"/dial_{48,33,24,12,16}_*.txt | sed 's/ | refused.*flight/ | flight/'
echo "jacobi baseline: $(tail -1 "$R/work/pristine_jacobi.txt" | head -c 120)"
for d in 12,24 16,28 16,32 20,36; do echo "jacobi $d: $(tail -1 "$R/work/jacobi_${d//,/_}.txt" | head -c 120)"; done

echo "== leave the tree pristine =="
git -C "$ROOT" checkout -- crates/
rm -f "$ROOT/crates/universe/examples/key_dial.rs"
echo REGEN_DONE
