#!/usr/bin/env bash
# Regenerates every number in dossier.md from shipped code + this run's patch.
# Applies work/patch.diff (if not already applied), builds, flies, and prints the tables.
# Total ~8 min (the full ladder_digest pass is the long part).
set -euo pipefail
cd "$(dirname "$0")/../../.."  # repo root

# 1. Apply the run's patch if the tree is clean of it.
if ! grep -q "ES_CHAIN" crates/universe/src/step.rs; then
  P=work/patch.diff
  [ -f "$P" ] || P="lab/results/20261016-1319-system-4fa8/work/patch.diff"
  git apply "$P" 2>/dev/null || patch -p1 --forward < "$P" || true
  grep -q "ES_CHAIN" crates/universe/src/step.rs || { echo "ERROR: patch did not apply"; exit 1; }
fi
echo "tree: $(git rev-parse HEAD) (patch applied)"

# 2. Build.
cargo build --release -p emergent-universe --example nladder --example ladder_digest
B="${CARGO_TARGET_DIR:-target}/release/examples"
R="lab/results/20261016-1319-system-4fa8/flights"
mkdir -p "$R"

run () {  # run <label> <env...> -- <nladder args...>
  local label=$1; shift
  local envs=()
  while [ "$1" != "--" ]; do envs+=("$1"); shift; done; shift
  echo "=== $label: nladder $* ==="
  # `${envs[@]+"${envs[@]}"}`: expands to nothing when envs is empty (a bare "${envs[@]:-}" would
  # pass one empty-string arg to env, which then dies with `env: '': No such file or directory`).
  env ${envs[@]+"${envs[@]}"} "$B/nladder" "$@" 2>&1 | tee "$R/$label.txt" | grep -E "frames after|game .* s after"
}

# 3. The four arms at N=1000, and the two arms at N=0/600/10^4 (1,900 game-s).
run n1000_off            -- 1000 coast 20 100 1000000
run n1000_chain          ES_CHAIN=1 -- 1000 coast 20 100 1000000
run n1000_stagger        ES_LOCAL_STAGGER=1 -- 1000 coast 20 100 1000000
run n1000_chainstagger   ES_CHAIN=1 ES_LOCAL_STAGGER=1 -- 1000 coast 20 100 1000000
run n0_off               -- 0 coast 20 100 1000000
run n0_chainstagger      ES_CHAIN=1 ES_LOCAL_STAGGER=1 -- 0 coast 20 100 1000000
run n600_off             -- 600 coast 20 100 1000000
run n600_chainstagger    ES_CHAIN=1 ES_LOCAL_STAGGER=1 -- 600 coast 20 100 1000000
run n10000_off           -- 10000 coast 20 100 1000000
run n10000_chainstagger  ES_CHAIN=1 ES_LOCAL_STAGGER=1 -- 10000 coast 20 100 1000000

# 4. The long runs (5,400 game-s) with per-frame dumps: envelope and total engine ms.
rm -f "$R/dump_long_off.csv" "$R/dump_long_chainstagger.csv"
echo "=== long off ==="
"$B/nladder" 1000 coast 55 100 1000000 > "$R/n1000_long_off.txt"
ES_DUMP="$R/dump_long_off.csv" "$B/nladder" 1000 coast 55 100 1000000 | tee -a "$R/n1000_long_off.txt" | grep -E "frames after|game .* s after"
echo "=== long chain+stagger ==="
"$B/nladder" 1000 coast 55 100 1000000 > /dev/null   # warm the dump file's arm-mate ordering
ES_CHAIN=1 ES_LOCAL_STAGGER=1 ES_DUMP="$R/dump_long_chainstagger.csv" "$B/nladder" 1000 coast 55 100 1000000 | tee "$R/n1000_long_chainstagger.txt" | grep -E "frames after|game .* s after"
echo "--- envelope (max events per 500-frame slice) ---"
for arm in off chainstagger; do
  echo -n "$arm: "; awk '{b=int($1/500); if($3>m[b])m[b]=$3} END{for(i=0;i<=b;i++)printf "%d ", m[i]; print ""}' "$R/dump_long_$arm.csv"
done
echo "--- total engine ms over the dump ---"
for arm in off chainstagger; do
  awk -v a=$arm '{n++; s+=$2} END{printf "%s: %d frames, %.1f ms total engine\n", a, n, s}' "$R/dump_long_$arm.csv"
done

# 5. Digests: OFF (= pristine main, control binary beside this script) and the arms.
echo "=== digest: patched OFF (all cases) ==="
"$B/ladder_digest" | tee "$R/digest_off.txt" | tail -2
echo "=== digest: pristine main, N=1000 coast (control) ==="
lab/results/20261016-1319-system-4fa8/bin/ladder_digest_pristine "N=1000 coast" | head -1 || true
for arm in chain stagger chainstagger; do
  case $arm in chain) E="ES_CHAIN=1";; stagger) E="ES_LOCAL_STAGGER=1";; chainstagger) E="ES_CHAIN=1 ES_LOCAL_STAGGER=1";; esac
  echo "=== digest: $arm (N=1000 coast + through the wave) ==="
  env $E "$B/ladder_digest" "N=1000 coast" | tee "$R/digest_$arm.txt"
  env $E "$B/ladder_digest" "N=1000 coast through the wave" | tail -2
done
echo "DONE. Compare against dossier.md's tables (flights/ holds every raw line)."
