#!/bin/bash
# Regenerates every number in the dossier from shipped code.
#
# Fix after the exit-124 run:
#  - TDIR was unbound (the stamps came out empty): the lab builds into
#    $CARGO_TARGET_DIR (~/lab-target-0), not ./target. It is now taken from
#    the environment, and the duplicate mtime-blind STAMP definition is gone
#    (the newest-rlib one is kept).
#  - The box pins jobs=2 in ~/.cargo/config.toml, which made every mutant arm
#    a 5m25s build; regen now runs 6 jobs and drops debug symbols via env
#    profile overrides (codegen/thin-LTO untouched, so no timing-gate
#    semantics move). Tests, flags and invocation are otherwise unchanged.
#  - The serial B10 control now runs inside the M-prune arm, sharing that
#    mutant's universe build instead of re-applying it after a restore, and
#    the trailing number-free clean xtask rebuild is gone.
# Every step logs to regen-logs/ and is timestamped; target ~8 min.
set -u
export CARGO_BUILD_JOBS=6
export CARGO_PROFILE_RELEASE_DEBUG=0
cd "$(git rev-parse --show-toplevel)"
TDIR=${CARGO_TARGET_DIR:-$PWD/target}
RUN=lab/results/20261014-0450-second-20261014-0059-inversion-8e84-7559
OUT=$RUN/regen-logs
mkdir -p "$OUT"
STAMP() { find "$TDIR/release/deps" -name 'libemergent_universe-*.rlib' -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2- | xargs -r sha256sum | cut -c1-16; }
SUM=$OUT/summary.txt
: > "$SUM"

counts() { awk -v tag="$1" '/^test result:/ {p+=$4; fl+=$6; ig+=$8} END {printf "[%s] passed=%d failed=%d ignored=%d\n", tag, p, fl, ig}'; }

apply() { python3 - "$1" <<'PY'
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
    edit("crates/universe/src/step.rs",  440,
         "len: self.rec.interval >> (2 * level as i64)",
         "len: self.rec.interval >> (2 * level as i64 + 1)")
elif mid == "M-prune":
    edit("crates/universe/src/universe.rs", 1105, "+ (1 << 26)", "+ (1 << 20)")
else:
    sys.exit(f"unknown mutant {mid}")
PY
}

echo "== 1. lattice lib, clean baseline (teeth available) == $(date +%T)"
git checkout -- crates/
cargo test --release --locked --offline -p emergent-lattice --lib 2>&1 | tee "$OUT/lattice-clean.txt" | counts lattice-clean | tee -a "$SUM"

echo "== 2. M-wrap control: the lattice suite must bite == $(date +%T)"
apply M-wrap; touch crates/lattice/src/law.rs
cargo test --release --locked --offline -p emergent-lattice --lib 2>&1 | tee "$OUT/lattice-M-wrap.txt" | counts lattice-M-wrap | tee -a "$SUM"
grep -E 'FAILED' "$OUT/lattice-M-wrap.txt" | head -2 | sed 's/^/   /' | tee -a "$SUM"
git checkout -- crates/lattice/src/law.rs; touch crates/lattice/src/law.rs

echo "== 3. liveness: clean universe rlib fingerprint == $(date +%T)"
cargo build --release -q --offline --locked -p emergent-universe 2>>"$OUT/build.txt"
echo "clean-rlib $(STAMP)" | tee -a "$SUM"

for m in M-kick:step.rs M-prune:universe.rs; do
  id=${m%%:*}
  echo "== $id: full universe+lattice suite == $(date +%T)"
  git checkout -- crates/universe/src; apply "$id"
  case $id in M-kick) touch crates/universe/src/step.rs;; M-prune) touch crates/universe/src/universe.rs;; esac
  cargo test --release --locked --offline -p emergent-universe -p emergent-lattice 2>&1 | tee "$OUT/suite-$id.txt" | counts "suite-$id" | tee -a "$SUM"
  echo "$id-rlib $(STAMP)" | tee -a "$SUM"
  if [ "$id" = M-prune ]; then
    echo "== 5. B10-flake control: behave::tests serial under M-prune (same build) == $(date +%T)"
    cargo build --release -q --offline --locked -p xtask 2>>"$OUT/build.txt"
    cargo test --release --locked --offline -p xtask --bin xtask behave::tests:: -- --test-threads=1 2>&1 | tee "$OUT/serial-M-prune.txt" | counts serial-M-prune | tee -a "$SUM"
  fi
  git checkout -- crates/universe/src
done
find crates/universe/src -name '*.rs' -exec touch {} +

echo "== 4. restore control: lattice lib equals the clean baseline == $(date +%T)"
cargo test --release --locked --offline -p emergent-lattice --lib 2>&1 | tee "$OUT/lattice-restore.txt" | counts lattice-restore | tee -a "$SUM"

echo "== done $(date +%T): compare $SUM against the dossier table; the clean and mutant rlib stamps must differ =="
cat "$SUM"
