#!/bin/bash
# The plane judged by the frozen gates: verdict, detail line, kicks per orbit, wall time.
# One row per (gate, --plane-step). Positive controls (echo) and planted controls (the gates bite).
set -u
cd /home/runner/work/emergent-space-engine/lab-0
OUT=lab/results/20261005-1404-q-plane-judge-65fd
BIN=target/release/xtask
run() { # law gate step label
  local law=$1 gate=$2 step=$3 label=$4
  local t0=$(date +%s.%N)
  if [ "$step" = "-" ]; then
    PLANE_TRACE=1 $BIN behave --law "$law" --gates "$gate" > "$OUT/rows/$label.out" 2> "$OUT/rows/$label.err"
  else
    PLANE_TRACE=1 $BIN behave --law "$law" --gates "$gate" --plane-step "$step" > "$OUT/rows/$label.out" 2> "$OUT/rows/$label.err"
  fi
  local rc=$?
  local t1=$(date +%s.%N)
  echo "ROW $label rc=$rc wall=$(echo "$t1 $t0" | awk '{printf "%.1f", $1-$2}')"
  grep -E "^(B1[2347]|behave|machine_state end)" "$OUT/rows/$label.out" | sed 's/^/  out: /'
  grep "plane_trace" "$OUT/rows/$label.err" | awk -v k=0 '{for(i=1;i<=NF;i++){if($i~/^kicks=/){sub("kicks=","",$i);k+=$i} if($i~/^spans=/){sub("spans=","",$i);p+=$i}}; print "  trace: " $0} END{if(NR>0) printf "  sum: kicks=%d spans=%.2f planet-periods -> %.1f kicks per planet period per ship\n", k, p, k/p}'
}
mkdir -p "$OUT/rows"
echo "=== positive controls (echo: the judge itself) ==="
for g in B12 B13 B14 B17; do run echo "$g" - "echo-$g"; done
echo "=== planted controls (the gates bite) ==="
run planted-kick B12 - planted-kick-B12
run planted-kick B13 - planted-kick-B13
run planted-notide B14 - planted-notide-B14
run planted-apsides B14 - planted-apsides-B14
run planted-average B17 - planted-average-B17
echo "=== the plane ==="
for g in B13 B12 B17 B14; do
  for s in 3 4 5 7; do
    run plane "$g" "$s" "plane-$g-s$s"
  done
done
