#!/bin/bash
# The gate-bite mutant panel: six one-line law mutants, two corpora (stale, fresh).
# Usage: bash panel.sh   (from the repo root; ~10 min: one rebuild per mutant)
set -u
RUN=lab/results/20261014-0059-inversion-8e84
STALE=artifacts/flights
FRESH=$RUN/corpus-fresh
OUT=$RUN/panel-logs
mkdir -p "$OUT"

gate() { # $1 corpus dir, $2 tag
  local out rc
  out=$(cargo run --release -q -p xtask -- universe --replay-all --flights "$1" 2>&1); rc=$?
  echo "$out" | tail -1 | sed "s/^/[$2] exit=$rc /" | tee -a "$OUT/summary.txt"
  echo "$out" > "$OUT/$2.txt"
}

apply() { # $1 id — python edits, line-exact
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
elif mid == "M-sign":
    edit("crates/universe/src/force.rs", 89,
         "Ok((scale2(d, k)?, r))", "Ok((scale2(d, k.negate())?, r))")
elif mid == "M-thrust":
    edit("crates/universe/src/ctx.rs", 44, "thrust_log2: -44", "thrust_log2: -45")
elif mid == "M-kick":
    edit("crates/universe/src/step.rs", 440,
         "len: self.rec.interval >> (2 * level as i64)",
         "len: self.rec.interval >> (2 * level as i64 + 1)")
elif mid == "M-bind":
    edit("crates/universe/src/bind.rs", 233,
         "if len <= cur_len && vel <= cur_vel {", "if len <= cur_len + 1 && vel <= cur_vel + 1 {")
elif mid == "M-prune":
    edit("crates/universe/src/universe.rs", 1105, "+ (1 << 26)", "+ (1 << 20)")
else:
    sys.exit(f"unknown mutant {mid}")
PY
}

for m in M-wrap M-sign M-thrust M-kick M-bind M-prune; do
  case $m in
    M-wrap)   f=crates/lattice/src/law.rs;;
    M-sign)   f=crates/universe/src/force.rs;;
    M-thrust) f=crates/universe/src/ctx.rs;;
    M-kick)   f=crates/universe/src/step.rs;;
    M-bind)   f=crates/universe/src/bind.rs;;
    M-prune)  f=crates/universe/src/universe.rs;;
  esac
  cp "$f" "$f.orig"
  if ! apply "$m"; then echo "[$m] EDIT FAILED" | tee -a "$OUT/summary.txt"; rm -f "$f.orig"; continue; fi
  if ! cargo build --release -q -p xtask 2>"$OUT/$m-build.txt"; then
    echo "[$m] BUILD FAILED" | tee -a "$OUT/summary.txt"; tail -5 "$OUT/$m-build.txt"; mv "$f.orig" "$f"; continue
  fi
  gate "$STALE" "$m-stale"
  gate "$FRESH" "$m-fresh"
  mv "$f.orig" "$f"
done
cargo build --release -q -p xtask && gate "$STALE" "restore-stale" && gate "$FRESH" "restore-fresh"
