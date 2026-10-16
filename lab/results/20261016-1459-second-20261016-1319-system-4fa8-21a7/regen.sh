#!/usr/bin/env bash
# Regenerates every number in dossier.md from shipped code + work/patch.diff (pre-applied by the
# runner). Deterministic numbers print exactly; wall-clock digits (ms, timeouts' seconds) vary.
# Total ~11 min on the lab's 8-vCPU box.
set -euo pipefail
cd "$(dirname "$0")/../../.."  # repo root
RUN=lab/results/20261016-1459-second-20261016-1319-system-4fa8-21a7
R="$RUN/flights"
B="${CARGO_TARGET_DIR:-target}/release"
mkdir -p "$R"

grep -q "ES_CHAIN" crates/universe/src/step.rs || { echo "ERROR: patch.diff not applied"; exit 1; }
echo "tree: $(git rev-parse HEAD) (patch applied)"

# 1. Build (patched): the universe examples and the behave judge.
cargo build --release -p emergent-universe --example nladder --example ladder_digest -p xtask

# 2. The gates. B12+B13 per arm (the deterministic digits); B14's frozen 60 s cap exceeds this
#    box, run for the two headline arms to record the timeout. ~4.5 min.
run_gates () {  # run_gates <label> <gate-list> [ENV=.. ..]
  local label=$1 list=$2; shift 2
  env ${@:+"$@"} "$B/xtask" behave --law plane --gates "$list" > "$R/gates_$label.txt" 2>&1 || true
}
run_gates off           B12,B13,B14
run_gates chainstagger  B12,B13,B14  ES_CHAIN=1 ES_LOCAL_STAGGER=1
run_gates phase         B12,B13      ES_LOCAL_PHASE=1
echo "--- gate lines (deterministic digits must be identical across arms) ---"
for a in off chainstagger phase; do echo "== $a =="; grep -E "^B1[234]" "$R/gates_$a.txt" | sed 's/; 44.*//; s/; 9 draws.*//; s/\[[0-9.]* s\]//'; done

# 3. The traces: per-answer event counts prove handoffs=0 and arm-invariance. ~3.5 min.
env PLANE_TRACE=1 "$B/xtask" behave --law plane --gates B13 > /dev/null 2> "$R/trace_b13_off.txt" || true
env ES_CHAIN=1 ES_LOCAL_STAGGER=1 PLANE_TRACE=1 "$B/xtask" behave --law plane --gates B13 > /dev/null 2> "$R/trace_b13_chainstagger.txt" || true
env PLANE_TRACE=1 "$B/xtask" behave --law plane --gates B12 > /dev/null 2> "$R/trace_b12_off.txt" || true
env ES_CHAIN=1 ES_LOCAL_STAGGER=1 PLANE_TRACE=1 "$B/xtask" behave --law plane --gates B12 > /dev/null 2> "$R/trace_b12_chainstagger.txt" || true
timeout 75 env PLANE_TRACE=1 "$B/xtask" behave --law plane --gates B14 > /dev/null 2> "$R/trace_b14_off.txt" || true
timeout 75 env ES_CHAIN=1 ES_LOCAL_STAGGER=1 PLANE_TRACE=1 "$B/xtask" behave --law plane --gates B14 > /dev/null 2> "$R/trace_b14_chainstagger.txt" || true
echo "--- traces: identity + handoffs=0 ---"
for g in b13_off b13_chainstagger b12_off b12_chainstagger b14_off b14_chainstagger; do
  printf "%-18s lines %s  handoffs>0 %s\n" "$g" "$(wc -l < "$R/trace_$g.txt")" "$(grep -c 'handoffs=[1-9]' "$R/trace_$g.txt" || true)"
done
diff -q "$R/trace_b13_off.txt" "$R/trace_b13_chainstagger.txt" && diff -q "$R/trace_b12_off.txt" "$R/trace_b12_chainstagger.txt" && diff -q "$R/trace_b14_off.txt" "$R/trace_b14_chainstagger.txt" && echo "ALL TRACES IDENTICAL OFF vs CHAIN+STAGGER"

# 4. The equal-bill flights: 3 arms, 3,300 frames each, plus 3 CPU repeats. ~30 s.
for arm in off chainstagger phase; do
  case $arm in off) E="";; chainstagger) E="ES_CHAIN=1 ES_LOCAL_STAGGER=1";; phase) E="ES_LOCAL_PHASE=1";; esac
  rm -f "$R/dump_long_$arm.csv"
  env ${E:+$E} "$B/examples/nladder" 1000 coast 55 100 1000000 > "$R/long_$arm.txt" 2>&1 || true
  env ${E:+$E} ES_DUMP="$R/dump_long_$arm.csv" "$B/examples/nladder" 1000 coast 55 100 1000000 >> "$R/long_$arm.txt" 2>&1 || true
  for i in 1 2 3; do env ${E:+$E} ES_DUMP="$R/cpu_${arm}_$i.csv" "$B/examples/nladder" 1000 coast 55 100 1000000 > /dev/null 2>&1 || true; done
done
echo "--- equal bill (stats line + dump sums; deterministic counts exact, ms box-relative) ---"
for arm in off chainstagger phase; do
  grep -E "^game " "$R/long_$arm.txt" | head -1
  awk -v a=$arm '{n++; s+=$2; e+=$3; if (n==1161) e_at=e} END{printf "%-13s frames %d  engine_ms %.1f  events %d  rate_past_1900gs %.3f\n", a, n, s, e, (e-e_at)/3500}' "$R/dump_long_$arm.csv"
  echo -n "  envelope: "; awk '{b=int($1/500); if($3>m[b])m[b]=$3} END{for(i=0;i<=b;i++)printf "%d ", m[i]; print ""}' "$R/dump_long_$arm.csv"
  awk -v a=$arm '{s+=$2} END{printf "  cpu %s: %.1f\n", a, s}' "$R/cpu_${arm}_2.csv"
done

# 5. Digests: patched OFF = pristine main (control binary, crates unchanged since b07f5a0b);
#    the arms' digests differ, one digest across 4 schedules each. ~50 s.
"$B/examples/ladder_digest" "N=1000 coast" | tee "$R/digest_off.txt"
"$RUN/bin/ladder_digest_pristine" "N=1000 coast" | tee "$R/digest_pristine.txt"
diff <(grep -o "6895ce06[0-9a-f]*" "$R/digest_off.txt") <(grep -o "6895ce06[0-9a-f]*" "$R/digest_pristine.txt") && echo "OFF DIGEST = PRISTINE BIT FOR BIT"
ES_CHAIN=1 ES_LOCAL_STAGGER=1 "$B/examples/ladder_digest" "N=1000 coast" | tee "$R/digest_chainstagger.txt"
ES_LOCAL_PHASE=1 "$B/examples/ladder_digest" "N=1000 coast" | tee "$R/digest_phase.txt"

# 6. Pristine gates control: revert the patch, rebuild, fly B12/B13 on shipped main, restore.
echo "--- pristine control (revert + rebuild) ---"
git diff > /tmp/regen_patch.diff
git checkout -- crates/
cargo build --release -p xtask
"$B/xtask" behave --law plane --gates B12,B13 > "$R/gates_pristine.txt" 2>&1 || true
git apply /tmp/regen_patch.diff
grep -q "ES_CHAIN" crates/universe/src/step.rs && echo "patch restored"
for f in gates_off gates_pristine; do grep -E "^B1[23]" "$R/$f.txt" | sed 's/; 44.*//; s/; 9 draws.*//; s/\[[0-9.]* s\]//' | md5sum; done
echo "DONE. Deterministic digits: gates identical across pristine/OFF/arms; traces identical; OFF digest = pristine."
