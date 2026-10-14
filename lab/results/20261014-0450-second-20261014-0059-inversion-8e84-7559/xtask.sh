#!/bin/bash
# The crate-coverage completion: xtask's unit tests (behave::plane's adapter
# tests — one reads across kicks — and universe/flight_tests.rs) are the third
# and last crate whose tests reach step.rs/universe.rs (only universe, lattice
# and xtask reference emergent_universe). behave --law plane itself cannot
# adjudicate on this box: the clean tree fails B12/B13/B14 (M1-calibrated,
# budget/load-sensitive) — see behave-logs/. cargo test -p xtask under both
# mutants, with baseline and restore controls.
set -u
cd "$(git rev-parse --show-toplevel)"
RUN=lab/results/20261014-0450-second-20261014-0059-inversion-8e84-7559
OUT=$RUN/xtask-logs
mkdir -p "$OUT"

SUITE() { # $1 tag
  local out rc
  out=$(cargo test --release --locked --offline -p xtask 2>&1); rc=$?
  { echo "$out"; echo "exit=$rc"; } > "$OUT/$1.txt"
  awk -v tag="$1" '/^test result:/ {p+=$4; fl+=$6; ig+=$8} END {printf "== [%s] exit=%d passed=%d failed=%d ignored=%d\n", tag, '"$rc"', p, fl, ig}' "$OUT/$1.txt" | tee -a "$OUT/summary.txt"
  grep -E '^    [a-z_0-9:]+$' "$OUT/$1.txt" | sort -u | sed 's/^/   FAILED: /' | tee -a "$OUT/summary.txt"
}

apply() { python3 - "$1" <<'PY'
import sys
mid = sys.argv[1]
def edit(path, lineno, old, new):
    ls = open(path).read().split("\n")
    assert old in ls[lineno-1], f"{path}:{lineno} does not contain {old!r}"
    ls[lineno-1] = ls[lineno-1].replace(old, new)
    open(path, "w").write("\n".join(ls))
if mid == "M-kick":
    edit("crates/universe/src/step.rs", 440,
         "len: self.rec.interval >> (2 * level as i64)",
         "len: self.rec.interval >> (2 * level as i64 + 1)")
elif mid == "M-prune":
    edit("crates/universe/src/universe.rs", 1105, "+ (1 << 26)", "+ (1 << 20)")
else:
    sys.exit(f"unknown mutant {mid}")
PY
}

echo "== xtask baseline (clean tree) ==" | tee "$OUT/summary.txt"
git checkout -- crates/universe/src/step.rs crates/universe/src/universe.rs
find crates/universe/src -name '*.rs' -exec touch {} +
cargo build --release -q -p xtask 2>>"$OUT/build.txt"
SUITE baseline

for m in M-kick M-prune; do
  case $m in
    M-kick) f=crates/universe/src/step.rs;;
    M-prune) f=crates/universe/src/universe.rs;;
  esac
  echo "== $m ==" | tee -a "$OUT/summary.txt"
  git checkout -- "$f"; apply "$m"; touch "$f"
  cargo build --release -q -p xtask 2>>"$OUT/build.txt"
  SUITE "$m"
  git checkout -- "$f"; touch "$f"
done

echo "== restore control ==" | tee -a "$OUT/summary.txt"
cargo build --release -q -p xtask 2>>"$OUT/build.txt"
SUITE restore
