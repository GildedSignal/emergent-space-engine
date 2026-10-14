# regen.sh — regenerates every number in the dossier (≤ 15 min).
# The patch (work/patch.diff) is applied by the runner before this runs.
set -e
cd "$(dirname "$0")/../../.."   # repo root
W="lab/results/20261014-1511-quant-7226/work"   # logs live with the run, not in /dev/null
mkdir -p "$W"
# The lab sets CARGO_TARGET_DIR (shared per lab slot); honor it or the build
# "succeeds" into a dir the invocations never read.
T=${CARGO_TARGET_DIR:-target}
X=${X:-$T/release/xtask}
build() {
  if cargo build --release -p xtask > "$W/build.log" 2>&1; then tail -1 "$W/build.log";
  else tail -20 "$W/build.log"; echo "BUILD FAILED" >&2; exit 1; fi
}
run() { # label seed [ES_FP=1]
  local label=$1 seed=$2
  "$X" universe --kick-bench --seed "$seed" --rtf 100 --seconds 8 > "$W/$label.out" 2> "$W/$label.err" \
    || { echo "arm $label failed (exit $?), stderr tail:" >&2; tail -5 "$W/$label.err" >&2; exit 1; }
  python3 -c 'import sys,json; t=sys.stdin.read(); d=json.loads(t[t.index("{"):]); print(json.dumps({"digest":d["digest"],"replay":d["replay_digest"],"made_med":d["kick_us"]["median"],"leaver_med":d["kick_us_leavers"]["median"],"all_p99":d["kick_us_all"]["p99"],"refused":d["refused"],"impact":d["searches"]["impact"],"exit":d["searches"]["exit"]}))' < "$W/$label.out" \
    || { echo "no JSON parsed from $W/$label.out, stdout tail:" >&2; tail -5 "$W/$label.out" >&2; exit 1; }
}
echo "== build (patched tree; ES_FP off == shipped semantics) =="; build
[ -x "$X" ] || { echo "xtask binary missing at $X (CARGO_TARGET_DIR=$T)" >&2; exit 1; }
echo "== OFF s3 rtf100 (the census) ==";  run off_s3 3
echo "== ON  s3 rtf100 (the kill) ==";    ES_FP=1 run on_s3 3
echo "== OFF s7 rtf100 (held-out) ==";    run off_s7 7
echo "== ON  s7 rtf100 (held-out) ==";    ES_FP=1 run on_s7 7
echo "== equality test (fast vs slow on every dipping tube) =="
cargo test --release -p emergent-universe --lib the_false_positions -- --nocapture > "$W/test.log" 2>&1 \
  || { tail -20 "$W/test.log"; echo "TEST FAILED" >&2; exit 1; }
tail -3 "$W/test.log"
echo "== probe trace (first searches, ES_FP on) =="
ES_FP=1 ES_FP_TRACE=1 "$X" universe --kick-bench --seed 3 --rtf 100 --seconds 1 > "$W/trace.out" 2> "$W/trace.err" \
  || { echo "trace arm failed, stderr tail:" >&2; tail -5 "$W/trace.err" >&2; exit 1; }
grep TRACE "$W/trace.out" "$W/trace.err" | head -14 || true
