#!/bin/bash
# The named experiment (check2 of 8e84): do the shipped test suites kill the two
# gate-dark mutants? Runs the suites the shipped way (xtask test's own command:
# cargo test --workspace --release --locked --offline) under M-kick and M-prune,
# with M-wrap as the positive control (the suites must bite where the gate is
# dark) and a restore control (must equal the baseline).
# Usage: bash panel.sh   (from the repo root)
set -u
cd "$(git rev-parse --show-toplevel)"
RUN=lab/results/20261014-0450-second-20261014-0059-inversion-8e84-7559
OUT=$RUN/panel-logs
mkdir -p "$OUT"

SUITE() { # $1 scope (e.g. "-p emergent-lattice" or "--workspace"), $2 tag
  local out rc
  out=$(cargo test --release --locked --offline $1 2>&1); rc=$?
  { echo "$out"; echo "exit=$rc"; } > "$OUT/$2.txt"
  # the one-line verdict: pass/fail counts + every failing test name
  echo "== [$2] exit=$rc" | tee -a "$OUT/summary.txt"
  grep -E '^test result:' "$OUT/$2.txt" | awk '{p+=$4+0; f+=$6+0; i+=$10+0} END {printf "   passed=%d failed=%d ignored=%d\n", p, f, i}' | tee -a "$OUT/summary.txt"
  grep -E '^[a-z_]+ .* FAILED|^failures:$' -A0 "$OUT/$2.txt" >/dev/null
  grep -E '^    [a-z_0-9]+$' "$OUT/$2.txt" | sort -u | sed 's/^/   FAILED: /' | tee -a "$OUT/summary.txt"
}

apply() { # $1 id — same line-exact edits as the parent run's panel.sh
python3 - "$1" <<'PY'
import sys
mid = sys.argv[1]
def edit(path, lineno, old, new):
    ls = open(path).read().split("\n")
    assert old in ls[lineno-1], f"{path}:{lineno} does not contain {old!r}"
    ls[lineno-1] = ls[lineno-1].replace(old, new)
    open(path, "w").write("\n".join(ls))
if mid == "M-wrap":
    edit("crates/lattice/src/law.rs", 337,
         "hit_narrow(d, w, reach).unwrap_or_else(|| hit_in(d.map(Wide::of), w.map(Wide::of), Wide::of(reach)))",
         "hit_in(d, w, reach)")
elif mid == "M-kick":
    edit("crates/universe/src/step.rs", 440,
         "len: self.rec.interval >> (2 * level as i64)",
         "len: self.rec.interval >> (2 * level as i64 + 1)")
elif mid == "M-prune":
    edit("crates/universe/src/universe.rs", 1105, "+ (1 << 26)", "+ (1 << 20)")
else:
    sys.exit(f"unknown mutant {mid}")
PY
}

run_mutant() { # $1 id, $2 file — apply, rebuild, suite, restore
  local m=$1 f=$2
  git checkout -- "$f"; apply "$m" || { echo "[$m] EDIT FAILED" | tee -a "$OUT/summary.txt"; return; }
  touch "$f"
  if ! cargo build --release -q -p xtask 2>"$OUT/$m-build.txt"; then
    echo "[$m] BUILD FAILED" | tee -a "$OUT/summary.txt"; git checkout -- "$f"; touch "$f"; return
  fi
  SUITE "-p emergent-universe -p emergent-lattice" "$m"
  git checkout -- "$f"; touch "$f"
}

echo "== baseline (clean tree) ==" | tee "$OUT/summary.txt"
SUITE "-p emergent-universe -p emergent-lattice" "baseline"

run_mutant M-wrap  crates/lattice/src/law.rs
run_mutant M-kick  crates/universe/src/step.rs
run_mutant M-prune crates/universe/src/universe.rs

echo "== restore control ==" | tee -a "$OUT/summary.txt"
cargo build --release -q -p xtask
SUITE "-p emergent-universe -p emergent-lattice" "restore"
