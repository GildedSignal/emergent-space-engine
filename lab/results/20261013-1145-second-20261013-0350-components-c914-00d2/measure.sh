#!/bin/bash
# Decisive measurements for the second-author run on 20261013-0350-components-c914:
# the division floor on aarch64 (checker's named experiment), via QEMU-user TCG
# wall time (per-insn pricing is NOT uniform — measured ~1.6 ns/insn for the
# multiply-heavy Newton vs ~0.8 for the branchy soft routine, so the wall axis
# is reported with that distortion) + an unbiased dynamic guest instruction
# census (singlestep exec trace, difference method between ROUNDS=N and
# ROUNDS=2N) + the executed-mnemonic histogram from capstone.
set -uo pipefail
R="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$R/../../.." && pwd)"
TDIR=${CARGO_TARGET_DIR:-/home/glmlab/lab-target-0}
ARM=$TDIR/aarch64-unknown-linux-musl/release/examples/div_floor_arm
QEMU=${QEMU:-/tmp/qemu-aarch64-static}
OUT=$R/probe-arm.txt
exec > >(tee $OUT) 2>&1

echo "== env =="
uname -a; cat /proc/loadavg
readelf -sW $ARM | awk '$8=="__udivti3"||$8=="__udivmodti4"{print "  sym", $8, "size", $3}'

echo "== [1] TCG wall time (ns/div, 3 runs each, ROUNDS=2000 => 8.19M divs/run) =="
for m in soft i128 asm newton none; do
  for i in 1 2 3; do ROUNDS=2000 $QEMU $ARM $m | grep 'arm-div'; done
done

echo "== [2] dynamic guest instructions per division (singlestep exec, N vs 2N) =="
count_mode () { # $1=mode $2=rounds -> total trace lines
  ROUNDS=$2 $QEMU -singlestep -d exec -D /dev/stdout $ARM $1 2>/dev/null | wc -l
}
for m in none soft i128 asm newton; do
  c1=$(count_mode $m 12); c2=$(count_mode $m 24)
  # per-division = (c2 - c1) / (12 * 4096)
  python3 -c "print(f'  insn/div[$m] = {($c2-$c1)/(12*4096):.1f}   (c12=$c1 c24=$c2)')"
done

echo "== [3] executed-mnemonic census (difference-based, N vs 2N, capstone) =="
for m in soft asm newton; do
  python3 $R/census2.py $ARM $m $QEMU
done

echo "== [4] native x86 harness, same kernels (control; ROUNDS=2000 x3) =="
X86=$TDIR/release/examples/div_floor_arm
for m in soft i128 asm newton; do
  for i in 1 2 3; do ROUNDS=2000 $X86 $m | grep 'arm-div'; done
done

echo "== [5] shipped div_bench x86 (the c914 record, same box today) =="
(cd $REPO && cargo run --release -p emergent-space --example div_bench -- div 2>/dev/null | grep -E 'div |sinks')
echo "== done =="
