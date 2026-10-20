#!/usr/bin/env bash
# Regenerates every dossier number from shipped code + work/patch.diff (applied by the runner
# before this runs). Two flights (~40-60 s wall each) + build; the analysis is awk over the
# stderr anatomy lines. No stagger in this patch: the combs dominate the worst frames (disclosed).
set -eu   # no pipefail: analysis pipelines end in head/awk-exit and would die on SIGPIPE (141)
RUN_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$RUN_DIR/../.." && pwd)"
cd "$REPO"
cargo build --release -p emergent-universe --example nladder
BIN=${CARGO_TARGET_DIR:-target}/release/examples/nladder
mkdir -p "$RUN_DIR/work"   # absent when the runner restores the tree; patch.diff is applied by the runner
cd "$RUN_DIR/work"

# a1: 3e5, TTL-fenced (the memory gate; discloses the fence as a law change)
ES_SCAN_TTL_S=16 ES_ANSWER_ANATOMY=1 timeout 100 "$BIN" 300000 burn 45 1300 12 1 > a1_3e5_s1.out 2> a1_3e5_s1.err || true
# b1: 1e5, unfenced (the held-out draw)
ES_ANSWER_ANATOMY=1 timeout 100 "$BIN" 100000 burn 45 1300 12 1 > b1_1e5_s1.out 2> b1_1e5_s1.err || true

for A in a1_3e5_s1 b1_1e5_s1; do
  echo "== $A =="
  grep -E "^frames|^ladder:" $A.out | cut -c1-200
  echo "-- captures: ALL walks (count, top ns, total ms) and idx walks"
  awk -F'ns=' '/^CAP.*ALL:/ {split($2,a," "); n++; s+=a[1]; if (a[1]>m) m=a[1]} END {print "ALL: n=" n, "top_ns=" m, "total_ms=" s/1e6}' $A.err
  awk -F'ns=' '/^CAP.*idx:/ {split($2,a," "); n++; s+=a[1]} END {print "idx: n=" n, "total_ms=" s/1e6}' $A.err
  awk -F'cand=' '/^CAP.*ALL:/ {split($2,a," "); print "ALL cand=" a[1]; exit}' $A.err
  echo "-- answers: top by ns (t ns read_ns cand tests skip_dom enc), per-body µs, read share, skip share"
  grep '^ANS' $A.err | sed 's/ANS t=//; s/ ns=/ /; s/ read_ns=/ /; s/ cand=/ /; s/ tests=/ /; s/ skip_dom=/ /; s/ enc=/ /' | sort -k2 -rn | head -3
  grep '^ANS' $A.err | sed 's/ANS t=//; s/ ns=/ /; s/ read_ns=/ /; s/ cand=/ /; s/ tests=/ /; s/ skip_dom=/ /; s/ enc=/ /' | sort -k2 -rn | head -1 | awk '{printf "top answer: %.2f us/body, read %.1f%%, skip %.1f%% (%d/%d), enc %d\n", $2/$4/1000, 100*$3/$2, 100*$6/$4, $6, $4, $7}'
  echo "-- biggest scan ever answered (cand) vs biggest captured:"
  grep '^ANS' $A.err | sed 's/.* cand=//; s/ .*//' | sort -rn | head -1
  grep '^CAP' $A.err | sed 's/.* cand=//; s/ .*//' | sort -rn | head -1
done
echo "regen done"
