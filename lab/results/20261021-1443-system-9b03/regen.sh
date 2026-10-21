# regen.sh — 20261021-1443-system-9b03
# Regenerates every number in dossier.md from shipped code + work/patch.diff.
# Total wall: about 4 minutes (build ~40 s once, three flights < 30 s together).
set -e
cd "$(dirname "$0")/../../.."   # repo root
git apply "$(dirname "$0")/work/patch.diff" 2>/dev/null || echo "(patch already applied)"
cargo build --release -p emergent-universe --example scannews
R=${CARGO_TARGET_DIR:-target}/release/examples/scannews
OUT="$(dirname "$0")"
for arm in "30000 coast" "30000 burn" "3000 coast"; do
  f="$OUT/regen_$(echo "$arm" | tr ' ' '_').log"
  SCAN_NEWS=1 "$R" $arm 10 100 12 >"$f" 2>&1
  grep -E '^scannews' "$f"
  python3 - "$f" <<'EOF'
import re, sys
rows = []
for l in open(sys.argv[1]):
    m = re.match(r'SCANNEWS t=(\d+) n=(\d+) ch=(\d+) me=(\w+) fb=(\w+)', l)
    if m: rows.append((int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4) == 'true', m.group(5) == 'true'))
n = sum(r[1] for r in rows); ch = sum(r[2] for r in rows)
dup = sum(1 for a, b in zip(rows, rows[1:]) if a[0] == b[0])
print(f"per-scan check: scans={len(rows)} walked={n} changed={ch} news_frac={ch/max(n,1):.5f} same_tick_pairs={dup} fallback={sum(r[4] for r in rows)}")
EOF
done
echo "regen done"
