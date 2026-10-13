#!/usr/bin/env bash
# Regen: every number in dossier.md, from shipped code + this run's patch (work/patch.diff).
# Linux/x86 shared runner; orders of magnitude only. Total: ~2 min warm, ~6 min cold.
set -euo pipefail
cd "$(dirname "$0")/../.."
RUN=lab/results/20261012-2257-quant-32ab
W=$RUN/work
mkdir -p "$W"
cargo build --release -p emergent-universe --example frame_split -p emergent-universe --example player_items >/dev/null 2>&1
T="${CARGO_TARGET_DIR:-target}"
B=$T/release/examples/frame_split
P=$T/release/examples/player_items

# Machine state (the lab records it; timings are orders of magnitude on a shared box)
cat /proc/loadavg > "$W/machine.txt"; free -m | head -2 >> "$W/machine.txt"; nproc >> "$W/machine.txt"

# 1. The decisive passes: demand (unlimited budget) and paced (the page's 12 ms cap),
#    the sweep's flights, seed 1, 20 s, members 48.
$B demand 100 20 48             > "$W/demand_m48_r100_v2.csv"
$B paced  100 20 48             > "$W/paced_m48_r100.csv"

# 2. Knobs: rtf 25/400 (throughput vs prologue) and members 400 (the player scan's N).
$B demand 25  10 48 0 8 12 15   > "$W/demand_m48_r25.csv"
$B demand 400 10 48 0 8 12 15   > "$W/demand_m48_r400.csv"
$B demand 100 10 400            > "$W/demand_m400_r100_v2.csv"

# 3. The burst trace (stderr): which frames the player-item waterfall lands in.
$B demand 100 20 48 2> "$W/burst_m48.err" >/dev/null

# 4. The per-item micro-probe: pure resolve cost along the flight (player record, chained).
$P 15  100 20 48 40             > "$W/items_L15.csv"
$P 8   100 20 48 40             > "$W/items_L8.csv"
$P 255 100 10 48 40             > "$W/items_coast.csv"

# Summary table for the dossier's headline numbers.
python3 - "$W" <<'EOF'
import csv, sys, glob, os
W = sys.argv[1]
print("== demand m48 rtf100 20s (per level): p50/p99/max us, ev_fr_p99, burst max items, burst max ms, us_player share")
for r in csv.DictReader(open(f"{W}/demand_m48_r100_v2.csv")):
    tot = float(r["cpu_ms_total"]); pl = float(r["us_player"]) / 1e3
    print(f"  L{r['level']:>2} alive={r['alive']:5} p50={float(r['cpu_us_p50']):7.1f} p99={float(r['cpu_us_p99']):8.1f} max={float(r['cpu_us_max']):9.1f} evfr_p99={r['ev_fr_p99']:>3} it3_max={r['it3_fr_max']:>4} us3_max_ms={float(r['us3_fr_max']):9.1f} player_share={pl/max(tot,0.01):.2f}")
print("== paced m48 rtf100 20s: lag and overflows (the sweep's stutter)")
for r in csv.DictReader(open(f"{W}/paced_m48_r100.csv")):
    print(f"  L{r['level']:>2} lag_max={float(r['lag_s_max']):.3f}s overflows={r['overflows']}")
print("== members 400, demand, rtf100 10s: per-item player cost and the burst")
for r in csv.DictReader(open(f"{W}/demand_m400_r100_v2.csv")):
    per = float(r["us_player"])/max(int(r["it_player"]),1)
    print(f"  L{r['level']:>2} max_ms={float(r['cpu_us_max'])/1e3:9.1f} us/item={per:8.1f} it3_max={r['it3_fr_max']:>4}")
EOF
