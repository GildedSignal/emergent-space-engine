#!/bin/bash
# The totality arm: `xtask behave --law plane` judges the shipped engine (the
# plane through its public API — gates B12-B14, B17). cargo test never runs it
# (behave_cli tests use echo/planted-* laws), so it is the last shipped
# instrument that could kill M-kick or M-prune. Baseline, both mutants, restore.
set -u
cd "$(git rev-parse --show-toplevel)"
RUN=lab/results/20261014-0450-second-20261014-0059-inversion-8e84-7559
OUT=$RUN/behave-logs
mkdir -p "$OUT"

behave() { # $1 tag
  local out rc
  out=$(timeout 600 cargo run --release --locked --offline -q -p xtask -- behave --law plane 2>&1); rc=$?
  { echo "$out"; echo "exit=$rc"; } > "$OUT/$1.txt"
  echo "== [$1] exit=$rc: $(grep -cE ' (PASS|FAIL)$' "$OUT/$1.txt") gate lines; $(grep -cE ' FAIL$' "$OUT/$1.txt") FAIL" | tee -a "$OUT/summary.txt"
  grep -E ' FAIL$' "$OUT/$1.txt" | sed 's/^/   /' | tee -a "$OUT/summary.txt"
  tail -1 "$OUT/$1.txt" | sed 's/^/   last: /' | tee -a "$OUT/summary.txt"
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

echo "== behave baseline (clean tree) ==" | tee "$OUT/summary.txt"
git checkout -- crates/universe/src/step.rs crates/universe/src/universe.rs
find crates/universe/src -name '*.rs' -exec touch {} +
cargo build --release -q -p xtask 2>>"$OUT/build.txt"
behave baseline

for m in M-kick M-prune; do
  case $m in
    M-kick) f=crates/universe/src/step.rs;;
    M-prune) f=crates/universe/src/universe.rs;;
  esac
  echo "== $m ==" | tee -a "$OUT/summary.txt"
  git checkout -- "$f"; apply "$m"; touch "$f"
  cargo build --release -q -p xtask 2>>"$OUT/build.txt"
  behave "$m"
  git checkout -- "$f"; touch "$f"
done

echo "== restore control ==" | tee -a "$OUT/summary.txt"
cargo build --release -q -p xtask 2>>"$OUT/build.txt"
behave restore
