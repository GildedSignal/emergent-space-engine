#!/bin/sh
# The digests of the scripted flights now, against a recorded file: digests.sh [recorded file] -- prints IDENTICAL or the diff.
cd "$(dirname "$0")/../../.." || exit 1
REC="${1:-artifacts/runs/frame/digests_main.txt}"
cargo build --release -p emergent-universe --example frame_digest 2>&1 | grep -E "^error" -A8
./target/release/examples/frame_digest 20 2>&1 | grep seed | sed 's/ *\[[0-9.]* s\]//; s/[0-9] schedules agree/schedules agree/' > /tmp/frame_digests_now.txt
grep seed "$REC" | sed 's/ *\[[0-9.]* s\]//; s/[0-9] schedules agree/schedules agree/' > /tmp/frame_digests_rec.txt
if diff /tmp/frame_digests_rec.txt /tmp/frame_digests_now.txt; then echo "IDENTICAL: $(wc -l < /tmp/frame_digests_now.txt) flights, bit for bit"; fi
grep -c "DISAGREE" /tmp/frame_digests_now.txt | sed 's/^/schedule disagreements: /'
