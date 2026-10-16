#!/usr/bin/env bash
# H1/H2/H3 (the checker's named experiment), on copies of the REAL wiki:
#   - v1 heal contrast: the original patch leaves orphan marker lines on nladder
#   - v2 heal: truly zero marker lines (all three kinds) on every page and the index,
#     content preserved in order
#   - two further patched publishes on healed nladder (a clean one, then a
#     conflicting one): zero markers before and after, runs union intact
# Usage: heal-real.sh <repo-root> <v2-wiki.py> <v1-wiki.py>
set -uo pipefail
ROOT=$(readlink -f "$1"); V2=$(readlink -f "$2"); V1=$(readlink -f "$3")
R=$(cd "$(dirname "$0")" && pwd)
PY=python3; export PYTHONDONTWRITEBYTECODE=1
INST="$PY $R/inst.py"
S=$R/scratch-heal; rm -rf "$S"; mkdir -p "$S/lab/wiki"; cd "$S"
git init -q .; git config user.email t@t; git config user.name t
cp "$ROOT"/lab/wiki/*.md lab/wiki/
git add -A; git commit -qm C0; C0=$(git rev-parse HEAD)
for p in nladder scan-queue encounters; do cp lab/wiki/$p.md $S/$p.orig.md; done

echo "== H0 (regenerate the checker's finding): v1 heal on a copy leaves orphan markers =="
mkdir -p v1/lab/wiki && cp "$ROOT"/lab/wiki/*.md v1/lab/wiki/
(cd v1 && LAB_WIKI=lab/wiki $PY "$V1" heal >/dev/null)
for p in nladder scan-queue encounters; do
  echo "  v1-healed $p.md: $($INST count v1/lab/wiki/$p.md)"
done

echo "== H1: v2 heal on the real pages (copy): zero markers, all three kinds =="
$PY "$V2" heal | sed 's/^/  /'
FAIL=0
for f in lab/wiki/*.md; do
  c=$($INST count "$f"); echo "  $f: $c"
  case "$c" in starts=0" "mids=0" "ends=0*) ;; *) FAIL=1; echo "  ** MARKERS REMAIN in $f";; esac
done
echo "  index marker-leak lines: $(grep -cE '<<<<<<<|>>>>>>>' lab/wiki/index.md || true)"

echo "== H2: content preservation (subsequence, independent instrument) =="
for p in nladder scan-queue encounters; do
  echo "  $p: $($INST subseq $S/$p.orig.md lab/wiki/$p.md)  runlines orig=$($INST count $S/$p.orig.md | sed 's/.*runlines=//') healed=$($INST count lab/wiki/$p.md | sed 's/.*runlines=//')"
done

echo "== H3: two further patched publishes on healed nladder =="
git add -A; git commit -qm healed; CH=$(git rev-parse HEAD)
cp lab/wiki/nladder.md healed-nladder.md
BEST=$(grep -m1 '^\*\*The ' healed-nladder.md)
echo "  standing best line both proposals rewrite: ${BEST:0:70}..."
mkrun() { # id newbest runline -> proposal edited from the healed page at CH
  local id=$1 best=$2 line=$3
  mkdir -p results/$id/wiki
  $PY - "$id" "$best" "$line" "$BEST" <<'PY'
import sys, pathlib
run, best, line, old = sys.argv[1:5]
t = pathlib.Path("healed-nladder.md").read_text()
t = t.replace(old, best, 1)          # rewrite the standing best line (conflict region)
t = t.replace("\n## Runs\n", f"\n## Runs\n{line}\n", 1)  # append-only runs list
pathlib.Path(f"results/{run}/wiki/nladder.md").write_text(t)
PY
  printf 'Grade: gold' > results/$id/DONE; echo "$CH" > results/$id/base
}
echo "  before publish 1: $($INST count lab/wiki/nladder.md)"
mkrun runX "**Best runX: the ladder flies.**" "- 20261016-2100-runX (gold): runx"
$PY "$V2" apply results "$CH" >/dev/null
echo "  after publish 1 (runX, clean):   $($INST count lab/wiki/nladder.md)  runX present: $(grep -c 'Best runX' lab/wiki/nladder.md)"
mkrun runY "**Best runY: the ladder flies faster.**" "- 20261016-2110-runY (gold): runy"
$PY "$V2" apply results "$CH" >/dev/null
echo "  after publish 2 (runY, conflict): $($INST count lab/wiki/nladder.md)  runX present: $(grep -c 'Best runX' lab/wiki/nladder.md)  runY present: $(grep -c 'Best runY' lab/wiki/nladder.md)"
echo "  runs union: $($INST count lab/wiki/nladder.md | sed 's/.*runlines=//') run lines (original + 2)"
echo "  summary(): $($PY -c "import importlib.util as u; s=u.spec_from_file_location('w','$V2'); w=u.module_from_spec(s); s.loader.exec_module(w); print(repr(w.summary(open('lab/wiki/nladder.md').read())))")"
$PY "$V2" index
echo "  index row: $(grep '| \[nladder\]' lab/wiki/index.md | cut -c1-170)"
echo "  content still whole: $($INST subseq $S/nladder.orig.md lab/wiki/nladder.md)"
[ "$FAIL" = 0 ]
