#!/bin/bash
# Regenerates every dossier number from shipped code + this run's scripts.
# work/patch.diff (the c914 patch + this run's div_floor_arm example) is applied
# by the runner before this runs; if the tree is clean we apply it ourselves.
# Total wall: ~6-10 min on the 8-vCPU shared runner (dominated by QEMU TCG runs).
set -euo pipefail
R="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$R/../../.." && pwd)"
cd $REPO

echo "== [0] tree =="
if ! git diff --quiet -- crates/space/examples/div_bench.rs 2>/dev/null || [ ! -f crates/space/examples/div_bench.rs ]; then
  git apply $R/work/patch.diff && echo "applied work/patch.diff"
else
  echo "the tree already carries this run's patch"
fi
git rev-parse HEAD

echo "== [1] toolchain =="
export RUSTUP_TOOLCHAIN=${RUSTUP_TOOLCHAIN:-1.90.0}
rustup target add aarch64-unknown-linux-musl 2>/dev/null | tail -1 || true
L=$(rustc --print sysroot)/lib/rustlib/x86_64-unknown-linux-gnu/bin/rust-lld
QEMU=${QEMU:-/tmp/qemu-aarch64-static}
QEMU_SHA=dce64b2dc6b005485c7aa735a7ea39cb0006bf7e5badc28b324b2cd0c73d883f
if [ ! -x $QEMU ] || [ "$(sha256sum $QEMU | cut -d' ' -f1)" != "$QEMU_SHA" ]; then
  curl -sL --max-time 300 -o $QEMU https://github.com/multiarch/qemu-user-static/releases/download/v7.2.0-1/qemu-aarch64-static
  chmod +x $QEMU
  echo "qemu sha256 $(sha256sum $QEMU | cut -d' ' -f1) (pinned $QEMU_SHA)"
fi
python3 -c "import capstone" 2>/dev/null || pip install --user -q capstone

echo "== [2] build (both targets, same kernels) =="
bash $R/mk_arm_bench.sh
cargo build --release -p emergent-space --example div_floor_arm
cargo build --release -p emergent-space --example div_bench
CARGO_TARGET_AARCH64_UNKNOWN_LINUX_MUSL_LINKER=$L RUSTFLAGS='-C linker-flavor=ld.lld' \
  cargo build --release -p emergent-space --example div_floor_arm --target aarch64-unknown-linux-musl

echo "== [3] measure (TCG wall + insn census + x86 controls + c914 record) =="
bash $R/measure.sh
echo "== regen done =="
