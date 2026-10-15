#!/bin/bash
# Regenerates every number in dossier.md from shipped code + work/patch.diff.
# Total wall on an 8-vCPU shared Linux box: ~5 minutes.
set -e
cd "$(dirname "$0")/../../.."   # the repo root
OUT="$(dirname "$0")/flights"
mkdir -p "$OUT"

# The seam + instrument (the runner applies work/patch.diff before this runs).
cargo build --release -p emergent-universe --example lazy_flight 2>&1 | grep -E "^error" && exit 1 || true

run () {  # run <lazy 0|1> <N> <flight> <cut> <seed> <file>
  if [ "$1" = "1" ]; then export ES_LAZY_ENTRY=1; else unset ES_LAZY_ENTRY; fi
  cargo run --release -p emergent-universe --example lazy_flight -- "$2" "$3" "$4" "$5" > "$OUT/$6" 2>/dev/null
  echo "== $6"; cat "$OUT/$6"
}

# The certificate arms (dossier table 1): digest identity control vs seam.
run 0 10000 coast 20000 1 ctl_10000_coast_20000_1.txt
run 1 10000 coast 20000 1 lazy_10000_coast_20000_1.txt
run 0 10000 burn  20000 1 ctl_10000_burn_20000_1.txt
run 1 10000 burn  20000 1 lazy_10000_burn_20000_1.txt
run 0 100000 coast 20000 1 ctl_100000_coast_20000_1.txt
run 1 100000 coast 20000 1 lazy_100000_coast_20000_1.txt
run 0 10000 coast 20000 7 ctl_10000_coast_20000_7.txt   # held-out seed
run 1 10000 coast 20000 7 lazy_10000_coast_20000_7.txt
# The deep arm (three waves, the scout's 48,000 game-s cut).
run 0 100000 coast 48000 1 ctl_100000_coast_48000_1.txt
run 1 100000 coast 48000 1 lazy_100000_coast_48000_1.txt

# The digest check: every arm's digest must be identical control vs seam.
python3 - "$OUT" <<'EOF'
import sys, pathlib
out = pathlib.Path(sys.argv[1])
bad = 0
for ctl in sorted(out.glob("ctl_*.txt")):
    lazy = out / ctl.name.replace("ctl_", "lazy_")
    d1 = [l for l in ctl.read_text().splitlines() if l.startswith("digest ")][0]
    d2 = [l for l in lazy.read_text().splitlines() if l.startswith("digest ")][0]
    same = d1 == d2
    bad += not same
    print(f"{ctl.name[4:-4]:<28} {'IDENTICAL' if same else 'MISMATCH'} {d1[7:23]}…")
print("ALL ARMS IDENTICAL" if bad == 0 else f"{bad} ARMS MISMATCH")
EOF

# The crate suite on the patched tree (the seam is off by default; the shipped
# path must pass unchanged).
cargo test --release -p emergent-universe 2>&1 | grep -E "test result" || true
