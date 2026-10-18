#!/bin/sh
# Regenerates every number in dossier.md from a restored tree: applies work/patch.diff
# (604c's formation harness + f134's composed-law arms + this run's comb/ledger
# instrument), builds, and flies the same arms. Wall-clock times are load-dependent
# (shared runner); every events/ledger/digest number is deterministic.
set -e
cd "$(dirname "$0")/../../.."   # repo root
P="$(dirname "$0")/work/patch.diff"
# Idempotent apply: a re-run must not fail because the patch is already on the
# tree (the recorded failure: "scanprobe.rs already exists", hunks then miss).
if git apply --check --reverse "$P" 2>/dev/null; then
  echo "patch already applied; skipping"
elif git apply --check "$P" 2>/dev/null; then
  git apply "$P"
else
  git apply --3way "$P" || { echo "patch does not apply to this tree" >&2; exit 1; }
fi
B=${CARGO_TARGET_DIR:-/home/glmlab/lab-target-3}/release/examples/scanprobe
OUT="$(dirname "$0")/regen"; mkdir -p "$OUT"; cd "$OUT"
for arm in "off:" "chain:ES_CHAIN=1 ES_LOCAL_STAGGER=1" "secular:ES_SECULAR=1" "composed:ES_SECULAR=1 ES_CHAIN=1 ES_LOCAL_STAGGER=1"; do
  name=${arm%%:*}
  for k in 1000 10000; do
    rm -f dump-$name-$k.txt
    env ${arm#*:} ES_DUMP=dump-$name-$k.txt $B $k 0 10 100 2>&1 | grep -vE "^  " > $name-f$k.log
    echo "== $name f$k"; grep -E "^(comb|ledger|probe):" $name-f$k.log
  done
done
for arm in "off:" "composed:ES_SECULAR=1 ES_CHAIN=1 ES_LOCAL_STAGGER=1"; do
  name=${arm%%:*}; env ${arm#*:} $B 200 10000 10 100 2>&1 | grep -vE "^  " > $name-pair.log
  echo "== $name pair"; grep -E "^(comb|probe):" $name-pair.log
done
python3 - <<'EOF'
for name in ["off","chain","secular","composed"]:
    rows=[tuple(map(float,l.split())) for l in open(f"dump-{name}-1000.txt")]
    big=[(int(f),int(e)) for f,ms,e in rows if e>500]
    gaps=[big[i+1][0]-big[i][0] for i in range(len(big)-1)]
    print(f"{name:9s} beats>500ev n={len(big)} mean={sum(e for _,e in big)/max(1,len(big)):.0f} gap(set)={sorted(set(gaps))}")
EOF
echo "regen done: compare against dossier tables 1-3 (digests and event counts must match exactly)"
