#!/bin/sh
# Regenerates every dossier number: applies the instrument patch to the clean tree, builds,
# flies the three decisive arms plus the neutrality control, and prints the analysis.
# ~75 s warm on this box (8 vCPU; ~21 s builds, ~45 s flights + control, analysis; each flight < 2 GB).
#
# Linux link fix (fix session): the shipped nladder.rs declares the macOS-only `proc_pid_rusage`
# extern unconditionally, so the shipped example never links on Linux (the author's control ran
# a binary left in the shared target dir by an earlier window). We link a stub that returns -1:
# footprint() already maps a nonzero return to (0,0), so the flight, its kicks and stats are the
# shipped ones verbatim — only the (unused) memory printout is dead. The stub rides a scoped
# `-C link-arg` via `cargo rustc`, so the shared target's dependency cache stays valid.
set -e
D=$(dirname "$0")
while [ "$D" != / ] && [ ! -f "$D/Cargo.toml" ]; do D=$D/..; done
cd "$D" || exit 1
[ -f Cargo.toml ] || { echo "FATAL: repo root (Cargo.toml) not found upward of the run folder" >&2; exit 1; }
R=lab/results/20261020-1002-fermi-8994
if git apply --check "$R/work/patch.diff" 2>/dev/null; then
  git apply "$R/work/patch.diff"
elif [ -f crates/universe/examples/alloc_scope.rs ]; then
  echo "patch already applied; continuing"
else
  echo "FATAL: patch neither applies nor is already applied (clean-tree apply failed; see git apply above)" >&2
  git apply "$R/work/patch.diff"
  exit 1
fi

mkdir -p /tmp/fermi8994
printf '%s\n' \
  '/* macOS libproc symbol, absent on Linux; nladder treats != 0 as "no footprint". */' \
  'int proc_pid_rusage(int pid, int flavor, unsigned long long *buffer) {' \
  '    (void)pid; (void)flavor; (void)buffer; return -1;' \
  '}' > /tmp/fermi8994/ppr_shim.c
cc -c -o /tmp/fermi8994/ppr_shim.o /tmp/fermi8994/ppr_shim.c

cargo build --release -p emergent-universe --example alloc_scope
cargo rustc --release -p emergent-universe --example nladder -- -C link-arg=/tmp/fermi8994/ppr_shim.o
B=$(cargo metadata --format-version 1 --no-deps 2>/dev/null | tr ',' '\n' | grep -o '"target_directory":"[^"]*"' | cut -d'"' -f4)
B=${B:-target}/release/examples

# the three decisive arms (each ~31 s wall; RSS < 100 MB)
ES_ALLOC_SCOPE=1 ES_ALLOC_CSV=/tmp/fermi8994/D1.csv "$B/alloc_scope" 10000 coast 30 2000 12 > /tmp/fermi8994/D1.log
ES_ALLOC_SCOPE=1 ES_ALLOC_CSV=/tmp/fermi8994/D2.csv "$B/alloc_scope" 10000 burn 30 2000 12 > /tmp/fermi8994/D2.log
ES_ALLOC_SCOPE=1 ES_ALLOC_CSV=/tmp/fermi8994/D3.csv "$B/alloc_scope" 30000 coast 30 2000 12 > /tmp/fermi8994/D3.log
# neutrality control: shipped vs instrumented, 3 runs each, fixed 5 s arm
echo "shipped kicks: $(for i in 1 2 3; do "$B/nladder" 10000 coast 5 2000 12 2>&1 | grep -o 'kicks [0-9]*' | head -1; done | tr '\n' ' ')"
echo "instrumented:  $(for i in 1 2 3; do ES_ALLOC_SCOPE=1 ES_ALLOC_CSV=/tmp/fermi8994/c$i.csv "$B/alloc_scope" 10000 coast 5 2000 12 2>&1 | grep -o 'kicks=[0-9]*'; done | tr '\n' ' ')"

python3 "$R/analysis.py" /tmp/fermi8994
echo "size censuses (chain means) live in the arm logs; copies checked in $R/data/"
