#!/bin/sh
# Regenerates every number in the dossier from the shipped tree + work/patch.diff.
# The angular certificate carries its own control arm (ES_SCAN_CERT=0), so one binary
# produces both arms; the digest lines must be pairwise identical (the falsifiable claim).
set -e
cd "$(dirname "$0")/../../.." # the repo root
RUN=lab/results/20261016-1740-quant-1250
OUT=$RUN/work/out
mkdir -p "$OUT"
git apply --check "$RUN/work/patch.diff" 2>/dev/null && git apply "$RUN/work/patch.diff" || echo "patch already applied"
cargo build --release -p emergent-universe --example nladder --example frame_digest
B=${CARGO_TARGET_DIR:-target}/release/examples/nladder
FD=${CARGO_TARGET_DIR:-target}/release/examples/frame_digest
for N in 300 1000 10000 100000; do
  for fl in coast burn; do
    ES_SCAN_CERT=0 "$B" "$N" "$fl" 20 > "$OUT/n${N}_${fl}_off.txt" 2>&1
    ES_SCAN_CERT=1 "$B" "$N" "$fl" 20 > "$OUT/n${N}_${fl}_on.txt" 2>&1
    d0=$(grep -o "digest .*" "$OUT/n${N}_${fl}_off.txt")
    d1=$(grep -o "digest .*" "$OUT/n${N}_${fl}_on.txt")
    [ "$d0" = "$d1" ] && ok=DIGEST-IDENTICAL || ok="DIGEST-DIFFERS (kills the certificate)"
    echo "N=$N $fl: $ok"
    grep -h "scan census" "$OUT/n${N}_${fl}_off.txt" "$OUT/n${N}_${fl}_on.txt"
  done
done
echo "=== the scripted flights (frame_digest), finder with certificate vs without vs brute ==="
ES_SCAN_CERT=0 "$FD" 3 > "$OUT/fd_off.txt" 2>&1
ES_SCAN_CERT=1 "$FD" 3 > "$OUT/fd_on.txt" 2>&1
BRUTE=1 "$FD" 3 > "$OUT/fd_brute.txt" 2>&1
diff <(sed 's/\[[0-9.]* s\]//' "$OUT/fd_off.txt") <(sed 's/\[[0-9.]* s\]//' "$OUT/fd_on.txt") && echo "cert arm == off arm (12 flights x 4 schedules)"
diff <(sed 's/\[[0-9.]* s\]//' "$OUT/fd_off.txt") <(sed 's/\[[0-9.]* s\]//' "$OUT/fd_brute.txt") && echo "finder == brute reference"
grep -c "schedules agree" "$OUT/fd_on.txt"
