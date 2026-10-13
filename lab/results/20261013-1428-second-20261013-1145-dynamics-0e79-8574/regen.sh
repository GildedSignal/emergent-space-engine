#!/bin/sh
# Regenerates every number in dossier.md from the shipped tree + this folder.
# 1. builds second_probe.rs (the 20261013-1145 record made regenerable: D levels [0,2,4,5,6,8,15]
#    committed, plus the E/F/G flights) and runs the full 38-flight grid at horizon 2^35;
# 2. verifies all 22 record rows (grid.txt + grid-d.txt of 20261013-1145) bit-identical;
# 3. decomposes the refusal storms (reflog.txt).
# Wall ~5.5 min on the shared 8-vCPU runner. Physics columns are deterministic (settle-only
# inputs at fixed check cadence, seed 1); only the [..s wall] fields vary between runs.
set -e
cd "$(dirname "$0")/../../.."
R=lab/results/20261013-1428-second-20261013-1145-dynamics-0e79-8574
cp "$R/second_probe.rs" crates/universe/examples/second_probe.rs
cargo build --release -p emergent-universe --example second_probe
"${CARGO_TARGET_DIR:-target}/release/examples/second_probe" 35 > "$R/grid-regen.txt" 2> "$R/traces-regen.txt"
python3 - "$R" <<'EOF'
import re, sys
R = sys.argv[1]
def load(path):
    rows = {}
    for line in open(path):
        if line.startswith(('pump probe', 'flight ')):
            continue
        rows[line[:26].strip()] = re.sub(r' \[[0-9.]*s wall.*\]$', '', line.rstrip('\n'))
    return rows
ref = load(f"{R}/grid-ref.txt"); ref.update(load(f"{R}/grid-d-ref.txt"))
new = load(f"{R}/grid-regen.txt")
names = ["control: coast", "control: cut-brake L8 g30"] + [f"A: held L{n} g30" for n in (15,12,8,4,2)] \
      + [f"B: held L15 g{x}" for x in (10,3,1.5,1.1)] + [f"C: held L15 g3 off{x}" for x in (45,90,135,180)] \
      + [f"D: from orbit L{n}" for n in (0,2,4,5,6,8,15)]
bad = [n for n in names if n not in new or new[n] != ref.get(n)]
print(f"record rows: {len(names)-len(bad)}/{len(names)} bit-identical" + ("" if not bad else f" — DIFFERS: {bad}"))
EOF
python3 "$R/reflog.py" "$R/traces-regen.txt" | tee "$R/reflog.txt"
