#!/usr/bin/env bash
# Resume: skip runs whose JSON already exists. E1 remainder, E2, E3, then E4 (4 seeds/point).
set -u
XT=/home/glmlab/lab-target-3/release/xtask
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
sum() {
python3 - "$1" <<'EOF'
import json, sys
n = sys.argv[1]
try:
    d = json.load(open(f"data/{n}.json"))
    f, c, w = d["frame_ms"], d["frame_cpu_ms"], d["where_the_time_goes_ms"]
    lb = d["uptime_before"].rsplit("load average:",1)[1].split(",")[0].strip()
    print(f"{n:14s} N={d['bodies']:3d} load {lb} cpu_p50={c['p50']:5.2f} cpu_worst={c['worst']:6.2f} "
          f"cpu_h={c['hitch_counts']} wall_worst={d['worst_hitch_ms']:6.2f} gather_p99={w['view_gather']['p99']:5.2f} "
          f"gather_max={w['view_gather']['max']:6.2f} share={w['view_gather']['share']:.2f} eng_p99={w['engine']['p99']:4.1f} "
          f"ovfl={d['rtf']['overflow_frames']}", flush=True)
except Exception as e:
    print(f"{n}: BAD {e}", flush=True)
EOF
}
run() { # name seconds extra...
  local name=$1 secs=$2; shift 2
  [ -s "data/$name.json" ] && { echo "skip $name"; return; }
  taskset -c 6 "$XT" universe --bench --seconds "$secs" "$@" > "data/$name.json" 2> "data/$name.err"
  sum "$name"
}

echo "== E1 remainder (paced, rtf 100, 30 s, pinned core 6) =="
for M in 256 320 384 400; do
  for S in 1 2 3 4 5 6 7 8; do
    run "q_M${M}_s${S}" 30 --rtf 100 --seed "$S" --members "$M"
  done
done
echo "== E2 unpaced CPU cross-check (20 s, seeds 1,4,8) =="
for M in 256 320 384 400; do
  for S in 1 4 8; do
    run "u_M${M}_s${S}" 20 --rtf 100 --seed "$S" --members "$M" --unpaced
  done
done
echo "== E3 controlled contention (same-core spinner, members 400) =="
for S in 1 2; do
  [ -s "data/c_M400_s${S}.json" ] && { echo "skip c_M400_s${S}"; continue; }
  taskset -c 6 timeout 34 python3 -c "while True: pass" &
  SPIN=$!
  run "c_M400_s${S}" 30 --rtf 100 --seed "$S" --members 400
  kill $SPIN 2>/dev/null
done
echo "== E4 inversion check (members 96 vs 192, seeds 1-4) =="
for M in 96 192; do
  for S in 1 2 3 4; do
    run "q_M${M}_s${S}" 30 --rtf 100 --seed "$S" --members "$M"
  done
done
echo "== ALL DONE =="
