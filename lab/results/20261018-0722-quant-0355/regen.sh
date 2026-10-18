# regen.sh — lab run 20261018-0722-quant-0355
# Regenerates every dossier number from shipped code + work/patch.diff (applied by the
# runner before this runs). ~4 min on an 8 vCPU box. Orders of magnitude only (Linux/x86).
set -euo pipefail
cd "$(dirname "$0")/../../.."   # repo root (lab/results/<run>/ -> root)

# Self-apply when the runner's apply did not land (the patch is text-only now:
# work/keys.bin is captured fresh below, never shipped in the diff). Idempotent.
grep -q 'PROBE_RELAXED' crates/space/src/orbit.rs || \
  git apply lab/results/20261018-0722-quant-0355/work/patch.diff

echo "== build (space + universe examples) =="
cargo build --release -p emergent-space --example compmemo 2>&1 | tail -1
cargo build --release -p emergent-universe --example ladder_digest 2>&1 | tail -1
DIGEST=/home/glmlab/lab-target-3/release/examples/ladder_digest
COMPMEMO=/home/glmlab/lab-target-3/release/examples/compmemo

echo "== control: pristine digest (the record: d2632de90255f5c10de9fd7372a3790d, kicks 34537) =="
"$DIGEST" "N=3000 coast through" | tee /tmp/ctl.txt

echo "== capture run (instrument must be digest-neutral: same digest line) =="
mkdir -p work && rm -f work/keys.bin
ES_KEYCAP="$PWD/work/keys.bin" "$DIGEST" "N=3000 coast through" | tee /tmp/cap.txt
nospan() { sed 's/ *\[[0-9.]* s\]$//'; }   # drop the trailing wall-clock field
diff <(grep '|' /tmp/ctl.txt | nospan) <(grep '|' /tmp/cap.txt | nospan) && echo "DIGEST_NEUTRAL=yes" || echo "DIGEST_NEUTRAL=NO (investigate)"
ls -l work/keys.bin

echo "== bench: split, exactness, hit prices =="
"$COMPMEMO" work/keys.bin 3
