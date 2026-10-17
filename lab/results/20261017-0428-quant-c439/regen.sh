#!/bin/bash
# Regenerates every number in the dossier from shipped code + this run's patch
# (prof::reads counters, feature-gated; example read_census). ~4 min on 8 vCPU.
set -e
cd "$(dirname "$0")/../../.."   # the repo root
T=${CARGO_TARGET_DIR:-target}/release/examples
OUT=lab/results/20261017-0428-quant-c439/raw
mkdir -p "$OUT"

echo "== build (plain, then prof) =="
cargo build --release -p emergent-universe --example read_census 2>&1 | tail -1
cp "$T/read_census" /tmp/rc_plain
cargo build --release -p emergent-universe --example read_census --features prof 2>&1 | tail -1
cp "$T/read_census" /tmp/rc_prof

echo "== machine state =="
uname -r; nproc; uptime; free -m | head -2

echo "== bit identity: plain vs prof, same args (digest must match) =="
/tmp/rc_plain 10000 burn 20 | tee "$OUT/identity_plain.txt" | grep -E "^flight"
/tmp/rc_prof  10000 burn 20 | tee "$OUT/a1_burn_1e4_20s.txt" | grep -E "^flight"

echo "== arms =="
/tmp/rc_prof 10000 coast 20 | tee "$OUT/a2_coast_1e4_20s.txt" | grep -E "^flight|total"
/tmp/rc_prof 100000 burn 20 | tee "$OUT/a4_burn_1e5_20s.txt" | grep -E "^flight|total"
/tmp/rc_prof 100000 coast 20 | tee "$OUT/a5_coast_1e5_20s.txt" | grep -E "^flight|total"
/tmp/rc_prof 10000 burn 150 | tee "$OUT/a3_burn_1e4_150s_wave.txt" | grep -E "^flight|total"

echo "== reads/scan and reads/event (from the raw logs) =="
python3 - <<'EOF'
import re
def row(path, name):
    for ln in open(path):
        if name in ln and "binding_at" in ln:
            return int(re.search(r"binding_at\s+(\d+)", ln).group(1))
    return 0
O = "lab/results/20261017-0428-quant-c439/raw/"
for tag, f in [("burn 1e4", "a1_burn_1e4_20s.txt"), ("coast 1e4", "a2_coast_1e4_20s.txt"),
               ("burn 1e5", "a4_burn_1e5_20s.txt"), ("coast 1e5", "a5_coast_1e5_20s.txt"),
               ("wave 1e4", "a3_burn_1e4_150s_wave.txt")]:
    cand, me = row(O+f, "scan: candidate"), row(O+f, "scan: the player")
    st, raw, rec = row(O+f, "state_of"), row(O+f, "root_state_raw"), 0
    m = re.search(r"rec: advance.*rec\s+(\d+)", open(O+f).read())
    if m: rec = int(m.group(1))
    ev = re.search(r"events (\d+)", open(O+f).read())
    ev = int(ev.group(1)) if ev else 0
    print(f"{tag:10s} scans {me:6d}  reads/scan {cand/max(me,1):6.1f}  events {ev:7d}  reads/event {(st+raw+rec)/max(ev,1):5.2f} (state_of {st/max(ev,1):.2f} raw {raw/max(ev,1):.2f} rec {rec/max(ev,1):.2f})")
EOF
echo "== done =="
