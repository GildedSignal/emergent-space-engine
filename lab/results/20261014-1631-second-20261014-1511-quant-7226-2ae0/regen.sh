#!/bin/sh
# regen.sh — regenerates every number in the dossier (≤ 15 min; measured ~2.5 min).
# work/patch.diff (the counters + the policy ladder + the warm start) is applied by the
# runner before this runs. Every arm is the kick bench on the patched tree; digests are
# compared within the run (off vs policy vs warm), and the off arm's digest is the one the
# prior run's checker verified against a pristine HEAD build (code identical f1322a79..db0f3e74).
set -e
cd "$(dirname "$0")/../../.."   # repo root
W="lab/results/20261014-1631-second-20261014-1511-quant-7226-2ae0/work"
mkdir -p "$W"
T=${CARGO_TARGET_DIR:-target}
X=$T/release/xtask
if ! cargo build --release -p xtask > "$W/build.log" 2>&1; then tail -20 "$W/build.log"; echo "BUILD FAILED" >&2; exit 1; fi
[ -x "$X" ] || { echo "xtask binary missing at $X" >&2; exit 1; }

j() { python3 -c 'import sys,json; t=sys.stdin.read(); d=json.loads(t[t.index("{"):]); print(json.dumps({"digest":d["digest"][:8],"replay":d["replay_digest"][:8],"leaver_med":d["kick_us_leavers"]["median"],"all_p99":d["kick_us_all"]["p99"],"refused":d["refused"],"impact":d["searches"]["impact"]}))'; }
fly() { $X universe --kick-bench --seed "$1" --rtf 100 --seconds 8 2>/dev/null | j; }
bat() { ES_MEMBERS=20000 $X universe --kick-bench --seed "$1" --rtf 1 --seconds 8 --members 4000 2>/dev/null | j; }

echo "== the kill table regenerates (s3 flying; policy ladder) =="
echo "OFF (shipped):";                                  fly 3 | tee "$W/r_off_s3.json"
for p in 1 2 3 4; do echo "ES_FP=$p:"; ES_FP=$p fly 3 | tee "$W/r_p${p}_s3.json"; done

echo "== the frozen rule's matrix: OFF vs policy 3 at 3 seeds x both paces =="
for s in 3 7 11; do
  echo "s$s flying OFF:"; fly $s | tee "$W/r_off_s${s}f.json"
  echo "s$s flying P3:";  ES_FP=3 fly $s | tee "$W/r_p3_s${s}f.json"
  echo "s$s battle OFF:"; bat $s | tee "$W/r_off_s${s}b.json"
  echo "s$s battle P3:";  ES_MEMBERS=20000 ES_FP=3 $X universe --kick-bench --seed $s --rtf 1 --seconds 8 --members 4000 2>/dev/null | j | tee "$W/r_p3_s${s}b.json"
done

echo "== the composition, layered (identity chain; s3, both paces) =="
echo "s3 fly WARM only:";  ES_IMP_WARM=1 fly 3 | tee "$W/r_warm_s3.json"
echo "s3 fly WARM+P3:";    ES_IMP_WARM=1 ES_FP=3 fly 3 | tee "$W/r_both_s3.json"
echo "s3 bat WARM only:";  ES_MEMBERS=20000 ES_IMP_WARM=1 $X universe --kick-bench --seed 3 --rtf 1 --seconds 8 --members 4000 2>/dev/null | j | tee "$W/r_warm_s3b.json"
echo "s3 bat WARM+P3:";    ES_MEMBERS=20000 ES_IMP_WARM=1 ES_FP=3 $X universe --kick-bench --seed 3 --rtf 1 --seconds 8 --members 4000 2>/dev/null | j | tee "$W/r_both_s3b.json"
echo "== composition at the held-out seeds =="
for s in 7 11; do
  echo "s$s fly WARM+P3:"; ES_IMP_WARM=1 ES_FP=3 fly $s | tee "$W/r_both_s${s}.json"
  echo "s$s bat WARM+P3:"; ES_MEMBERS=20000 ES_IMP_WARM=1 ES_FP=3 $X universe --kick-bench --seed $s --rtf 1 --seconds 8 --members 4000 2>/dev/null | j | tee "$W/r_both_s${s}b.json"
done

echo "== identity: every policy equals the bisection on every dipping tube of a settled plane =="
cargo test --release -p emergent-universe --lib 2>&1 | tail -2 | tee "$W/r_test.log"

echo "== off semantics are the shipped ones even with the env vars set to their off values =="
ES_FP=0 ES_IMP_WARM=0 $X universe --kick-bench --seed 3 --rtf 100 --seconds 8 2>/dev/null | j
