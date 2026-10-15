#!/bin/sh
# Regenerates every number in the dossier from shipped code + work/patch.diff (applied before this runs).
# Binaries are built once; each arm is bounded by `timeout`. Total under 15 minutes on a quiet box.
set -e
cd "$(dirname "$0")/../../.."   # the repo root (the runner applies work/patch.diff first)
OUT=lab/results/20261014-2336-system-c592/out
mkdir -p "$OUT"
cargo build --release -p emergent-universe --example scan_ruin
BIN=$(cargo metadata --no-deps --format-version 1 | python3 -c "import json,sys; print(json.load(sys.stdin)['target_directory'])")/release/examples/scan_ruin

# P1 certificate, N=10^3, full 16,000 game-s cut: digest must be identical between the arms.
timeout 300 "$BIN" 1000 burn 280 100 12 16000    > "$OUT/n1000-pristine.txt" 2>&1
timeout 300 env ES_TABLE_SHARED=1 "$BIN" 1000 burn 280 100 12 16000 > "$OUT/n1000-shared.txt" 2>&1

# The decisive arms, N=5x10^4 (the box must allow ~8 GB for the pristine arm to finish un-killed;
# a kill (exit 137 / timeout) is the ruin reproducing, not a failure of the regeneration).
timeout 500 "$BIN" 50000 burn 480 100 12 16000    > "$OUT/n50000-pristine.txt" 2>&1 || echo "pristine 5x10^4 arm ended $? (a kill is the expected ruin on a capped box)"
timeout 500 env ES_TABLE_SHARED=1 "$BIN" 50000 burn 480 100 12 16000 > "$OUT/n50000-shared.txt" 2>&1

# P5 controls: coast in-band (no burn), both arms, N=5x10^4.
timeout 300 "$BIN" 50000 coast 280 100 12 16000    > "$OUT/n50000-coast-pristine.txt" 2>&1 || true
timeout 300 env ES_TABLE_SHARED=1 "$BIN" 50000 coast 280 100 12 16000 > "$OUT/n50000-coast-shared.txt" 2>&1 || true

cd - >/dev/null
python3 - <<'EOF'
import re, glob, os
os.chdir(os.path.dirname(os.path.abspath('regen.sh')) if os.path.exists('regen.sh') else '.')
try:
    os.chdir('lab/results/20261014-2336-system-c592')
except FileNotFoundError:
    pass
print("== summary ==")
for f in sorted(glob.glob('out/*.txt')):
    txt = open(f).read()
    m = re.search(r'scanruin: (.*)', txt)
    print(f, '->', m.group(1) if m else ('KILLED/TRUNCATED: ' + txt.strip().splitlines()[-1][:120] if txt.strip() else 'empty'))
pr = open('out/n50000-pristine.txt').read(); sh = open('out/n50000-shared.txt').read()
d = lambda t: re.search(r'digest: (\w+)', t).group(1)
print('digest equal at 5x10^4:', d(pr) == d(sh), d(pr), d(sh))
a = open('out/n1000-pristine.txt').read(); b = open('out/n1000-shared.txt').read()
print('digest equal at 10^3:', d(a) == d(b))
EOF
