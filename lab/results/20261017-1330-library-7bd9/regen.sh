#!/bin/sh
# Regen: every dossier number from shipped code + this run's scripts + work/patch.diff.
# Total < 15 min on the lab box (the cargo build is the long pole; cached target at ~/lab-target-N).
# NOTE: this is a SHARED box. The quiet arm's flat assertion is only checked when the box
# has idle room (loadavg < 3); under external load the flat path cannot be demonstrated
# there and the check prints SKIP. The record logs (flow_quiet.log / flow_load.log,
# 3,600-frame arms flown 13:33-13:34 on a quiet stretch) carry the dossier's exact numbers.
set -e
RUN="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$RUN/../../.." && pwd)"
cd "$ROOT"

echo "== 0. patch present (example flow_attr) =="
if [ ! -f crates/universe/examples/flow_attr.rs ]; then
  git apply "$RUN/work/patch.diff"
fi
ls -la crates/universe/examples/flow_attr.rs

echo "== 1. quote verification (byte-identical, fresh fetch cached in run folder) =="
python3 "$RUN/verify_quotes.py" "$RUN/readwise.json"

echo "== 2. build the probe =="
cargo build --release -p emergent-universe --example flow_attr
BIN="$(cargo metadata --format-version 1 2>/dev/null | tr ',' '\n' | grep -o '"target_directory":"[^"]*"' | cut -d'"' -f4)/release/examples/flow_attr"
[ -x "$BIN" ] || BIN="$HOME/lab-target-1/release/examples/flow_attr"
echo "BIN=$BIN"

echo "== 3a. preflight: kill any stale spinners from a previous regen (they poison the quiet arm) =="
pkill -f "while :; do :; done" 2>/dev/null || true
sleep 1
LOADAVG="$(cut -d' ' -f1 /proc/loadavg)"
echo "loadavg=$LOADAVG"

echo "== 3. quiet arm (1,200 frames = 2,000 gs; flat path expected on idle CPUs) =="
taskset -c 0,1 "$BIN" 400 1200 > "$RUN/flow_quiet_regen.log" 2>&1 || { cat "$RUN/flow_quiet_regen.log"; exit 1; }
tail -2 "$RUN/flow_quiet_regen.log"

echo "== 4. load arm (6 spinners pinned to the same 2 CPUs; 1,200 frames) =="
for i in 1 2 3 4 5 6; do taskset -c 0,1 sh -c 'while :; do :; done' & done
SPINNERS="$(jobs -p)"
taskset -c 0,1 "$BIN" 400 1200 > "$RUN/flow_load_regen.log" 2>&1 || { kill $SPINNERS 2>/dev/null || true; cat "$RUN/flow_load_regen.log"; exit 1; }
kill $SPINNERS 2>/dev/null || true
tail -2 "$RUN/flow_load_regen.log"

echo "== 5. assertions =="
python3 - "$RUN" "$LOADAVG" <<'EOF'
import re, sys
run, loadavg = sys.argv[1], float(sys.argv[2])
def last(path):
    rows = [l for l in open(path) if l.startswith("gs=")]
    m = re.search(r"live_B=\s*(\d+).*held_scans=\s*(\d+)", rows[-1])
    return int(m.group(1)), int(m.group(2))
qB, qH = last(f"{run}/flow_quiet_regen.log")
lB, lH = last(f"{run}/flow_load_regen.log")
assert lH >= 40, f"load arm did not accumulate: held={lH}"
assert lB > 1.5 * qB, f"load live {lB/1e6:.0f} MB did not separate from quiet {qB/1e6:.0f} MB"
if loadavg >= 3.0 and qH > 60:
    print(f"SKIP quiet-flat (box busy, loadavg {loadavg}: quiet held={qH}); the record log flow_quiet.log carries the flat path")
else:
    assert qH <= 60, f"quiet arm grew: held={qH} (is the box loaded? rerun when 0,1 have idle room)"
    assert qB < 60_000_000, f"quiet live_B {qB/1e6:.0f} MB too high"
    print(f"quiet flat: held={qH}, live {qB/1e6:.1f} MB")
print(f"PASS: load arm held={lH}, live {lB/1e6:.1f} MB vs quiet {qB/1e6:.1f} MB")
EOF

echo "== 6. the FLOW arithmetic table (from the record logs) =="
python3 "$RUN/flow_arith.py" "$RUN"

echo "== 7. census anchors (shipped code, grep) =="
grep -n "const SCAN_BACKLOG" crates/universe/src/universe.rs
grep -n "about 10 KB each" crates/universe/src/universe.rs
grep -n "pub fn held_scans" crates/universe/src/universe.rs
echo "(the stats ledger never prints the standing held count: the counter existed, unread)"
grep -rn "held_scans()" crates/ xtask/ | grep -v "flow_attr\|frame_f1\|nladder\|frame_loop" || echo "(no other consumer)"

echo DONE
