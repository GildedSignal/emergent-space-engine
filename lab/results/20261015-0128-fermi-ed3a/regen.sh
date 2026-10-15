#!/bin/sh
# Regenerates every number in dossier.md (lab run 20261015-0128-fermi-ed3a).
# The runner applies work/patch.diff (step.rs + examples/stagger.rs) before this runs;
# if it has not, this script applies it itself (idempotent either way).
# ~6 min on an 8-vCPU Linux box; the two 3e5 flights each exceed 60 s (noted in the dossier).
set -e
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)          # lab/results/<run>
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)               # repo root
W=$HERE/work

# The patch must be present (stagger.rs is new; step.rs gains the ES_STAGGER gate).
if [ ! -f "$ROOT/crates/universe/examples/stagger.rs" ]; then
  git -C "$ROOT" apply "$W/patch.diff"
elif git -C "$ROOT" diff --quiet -- crates/universe/src/step.rs; then
  # stagger.rs present but step.rs pristine: the split state this script itself leaves behind.
  git -C "$ROOT" apply --exclude=crates/universe/examples/stagger.rs "$W/patch.diff"
fi

cd "$ROOT/crates/universe"

echo "== build (patched tree) =="
cargo build --release --example stagger --example belt_first --example frame_digest 2>&1 | tail -1

echo; echo "== 1. the mechanism at birth: belt_first, gate off vs ES_STAGGER=1 (N=1e5) =="
echo "--- gate OFF (shipped) ---"
cargo run --release --example belt_first -- 100000 2>/dev/null
echo "--- ES_STAGGER=1 ---"
ES_STAGGER=1 cargo run --release --example belt_first -- 100000 2>/dev/null

echo; echo "== 2. default-neutrality: frame_digest (9 flights x 4 schedules), patched gate-off =="
cargo run --release --example frame_digest -- 2 > $W/fd_patched_off.txt 2>/dev/null
tail -1 $W/fd_patched_off.txt

echo "== pristine build (step.rs reverted; stagger.rs is a new file, frame_digest does not see it) =="
git -C "$ROOT" checkout -- crates/universe/src/step.rs
cargo build --release --example frame_digest 2>&1 | tail -1
cargo run --release --example frame_digest -- 2 > $W/fd_pristine.txt 2>/dev/null
git -C "$ROOT" apply --exclude=crates/universe/examples/stagger.rs "$W/patch.diff"
cargo build --release --example stagger 2>&1 | tail -1
if diff -q $W/fd_pristine.txt $W/fd_patched_off.txt > /dev/null; then
  echo "DEFAULT-NEUTRAL: byte-identical ($(wc -l < $W/fd_pristine.txt) digest lines)"
else
  # The trailing "[N.N s]" is wall time (nondeterministic); everything else must match.
  sed 's/ *\[[0-9.]* s\]$//' $W/fd_pristine.txt    > $W/fd_pristine.digests
  sed 's/ *\[[0-9.]* s\]$//' $W/fd_patched_off.txt > $W/fd_patched_off.digests
  if diff -q $W/fd_pristine.digests $W/fd_patched_off.digests > /dev/null; then
    echo "DEFAULT-NEUTRAL: identical modulo wall-time annotations ($(wc -l < $W/fd_pristine.digests) digest lines)"
  else
    echo "DEFAULT-NEUTRALITY BROKEN:"; diff $W/fd_pristine.digests $W/fd_patched_off.digests || true
  fi
fi
echo; echo "== 3. N=1e5 flights, coast, 220 s page (the 1e5 table) =="
cargo run --release --example stagger -- 100000 220 $W/a1.csv 2>/dev/null
ES_STAGGER=1 cargo run --release --example stagger -- 100000 220 $W/a2.csv 2>/dev/null

echo; echo "== 4. N=3e5 flights, coast, 460 s page (the 3e5 table; ~85 s each) =="
cargo run --release --example stagger -- 300000 460 $W/b1.csv 2>/dev/null
ES_STAGGER=1 cargo run --release --example stagger -- 300000 460 $W/b2.csv 2>/dev/null

echo; echo "== analysis (windows, flattening, lag location; dossier numbers 3-4) =="
python3 $W/analyze.py $W/a1.csv $W/a2.csv
python3 $W/analyze.py $W/b1.csv $W/b2.csv
W=$W python3 - <<'EOF'
import csv, os
W = os.environ['W']
def wins(p):
    ws = {}
    for r in csv.reader(open(p)):
        if r[0] == 'frame':
            continue
        g = float(r[1]); e = int(r[3])
        if g >= 0:
            ws[int(g // 250)] = ws.get(int(g // 250), 0) + e
    return ws
b1, b2 = wins(f'{W}/b1.csv'), wins(f'{W}/b2.csv')
print('14k window (first kicks): control', b1.get(55, 0), 'staggered', b2.get(55, 0),
      '(%.1fx)' % (b1.get(55, 0) / max(b2.get(55, 0), 1)))
print('28k window (first boundaries): control', b1.get(112, 0), 'staggered', b2.get(112, 0),
      '(%.1fx)' % (b1.get(112, 0) / max(b2.get(112, 0), 1)))
print('wave 2 sums 41-44k: control', sum(b1.get(w, 0) for w in range(164, 176)),
      'staggered', sum(b2.get(w, 0) for w in range(164, 176)))
EOF
echo; echo "regen done."
