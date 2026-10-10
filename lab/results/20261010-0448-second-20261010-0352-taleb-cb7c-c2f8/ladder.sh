#!/usr/bin/env bash
# Contention-controlled load ladder (checker's named experiment).
# Bench pinned to core 6; E3 adds a same-core spinner (controlled descheduling).
set -u
XT=/home/glmlab/lab-target-3/release/xtask
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
run() { # name seconds extra...
  local name=$1 secs=$2; shift 2
  local t0=$(date +%s)
  taskset -c 6 "$XT" universe --bench --seconds "$secs" "$@" > "data/$name.json" 2> "data/$name.err"
  local rc=$?
  python3 - "$name" "$rc" "$(( $(date +%s) - t0 ))" <<'EOF'
import json, sys
n, rc, wall = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
try:
    d = json.load(open(f"data/{n}.json"))
    f, c, w = d["frame_ms"], d["frame_cpu_ms"], d["where_the_time_goes_ms"]
    lb = d["uptime_before"].rsplit("load average:",1)[1].split(",")[0].strip()
    la = d["uptime_after"].rsplit("load average:",1)[1].split(",")[0].strip()
    print(f"{n:16s} rc={rc} wall={wall:3d}s N={d['bodies']:3d} load {lb}->{la} "
          f"wallp50={f['p50']:5.2f} wallworst={d['worst_hitch_ms']:6.2f} "
          f"cpu_p99={c['p99']:5.2f} cpu_worst={c['worst']:6.2f} cpu_h={c['hitch_counts']} "
          f"gather_p99={w['view_gather']['p99']:5.2f} gather_max={w['view_gather']['max']:6.2f} "
          f"eng_p99={w['engine']['p99']:4.1f} ovfl={d['rtf']['overflow_frames']:4d} "
          f"digest={d['digest'][:12]}", flush=True)
except Exception as e:
    print(f"{n}: rc={rc} BAD {e}", flush=True)
EOF
}

echo "== E0 provenance: author's det_repeat, pinned =="
run det_repeat 5 --rtf 10 --seed 1 --members 48

echo "== E1 quiet ladder: paced, rtf 100, 30 s, pinned core 6, seeds 1..8 =="
for M in 256 320 384 400; do
  for S in 1 2 3 4 5 6 7 8; do
    run "q_M${M}_s${S}" 30 --rtf 100 --seed "$S" --members "$M"
  done
done

echo "== E2 unpaced CPU cross-check: 20 s, seeds 1,4,8 =="
for M in 256 320 384 400; do
  for S in 1 4 8; do
    run "u_M${M}_s${S}" 20 --rtf 100 --seed "$S" --members "$M" --unpaced
  done
done

echo "== E3 controlled contention: same-core spinner + bench on core 6, members 400 =="
for S in 1 2; do
  taskset -c 6 timeout 34 python3 -c "while True: pass" &
  SPIN=$!
  run "c_M400_s${S}" 30 --rtf 100 --seed "$S" --members 400
  kill $SPIN 2>/dev/null
done
echo "== ladder done =="
