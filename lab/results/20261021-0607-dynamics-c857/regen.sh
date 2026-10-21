#!/bin/sh
# Regenerates every number in the dossier: the two-seed engine census to g=145 on the shipped
# plane_extra (belt 2,700), the dump analysis and the step-ledger extraction. The runner applies
# work/patch.diff (adds crates/universe/examples/calendar_flight.rs) before this runs. Cold-cache
# wall: ~12 min (build + two parallel flights ~8.5 min + analysis ~3 min) on 8 vCPU.
set -e
ROOT=$(cd "$(dirname "$0")/../../.." && pwd)
RUN="$ROOT/lab/results/20261021-0607-dynamics-c857"
cd "$ROOT"
cargo build --release -p emergent-universe --example calendar_flight
mkdir -p "$RUN/work"
CENSUS_DUMP="$RUN/work/dues_s" cargo run --release -q -p emergent-universe --example calendar_flight -- 3000 145 1 > "$RUN/work/flight_s1.txt" &
P1=$!
CENSUS_DUMP="$RUN/work/dues_s" cargo run --release -q -p emergent-universe --example calendar_flight -- 3000 145 2 > "$RUN/work/flight_s2.txt" &
P2=$!
wait $P1 $P2
python3 "$RUN/analyze.py" "$RUN"
echo "--- seed 1 flight ---"
head -2 "$RUN/work/flight_s1.txt"
echo "--- seed 2 flight ---"
head -2 "$RUN/work/flight_s2.txt"
echo "--- endpoint rows (last 5 generation rows per seed; the table ends when n < 100) ---"
grep '^g=' "$RUN/work/flight_s1.txt" | tail -5
grep '^g=' "$RUN/work/flight_s2.txt" | tail -5
echo "--- step ledger (extract) + pooled analysis ---"
python3 "$RUN/extract.py" "$RUN" | tee "$RUN/work/extract.txt"
