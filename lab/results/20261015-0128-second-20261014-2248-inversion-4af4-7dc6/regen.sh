#!/usr/bin/env bash
# Regenerates every number in dossier.md from shipped code + this run's probe.
# work/patch.diff = 4af4's examples/wavetrain.rs (unchanged probe; the wiki part of 4af4's
# patch is superseded by this run's wiki/nladder.md). ~10 min on the lab box with a warm
# target dir (~14 cold): one build, the long train (700k game-s at 2e5), the N-ceiling arm
# (2 waves at 4.2e5), then analyze.py over every log. No `|| true`: an analyzer crash or a
# digest mismatch fails the regen (4af4's defect — its script could not regenerate its tables).
set -e
cd "$(dirname "$0")/../../.."
cargo build --release -p emergent-universe --example wavetrain
W="${CARGO_TARGET_DIR:-/home/glmlab/lab-target-2}/release/examples/wavetrain"
R=lab/results/20261015-0128-second-20261014-2248-inversion-4af4-7dc6
OUT=$R/out
mkdir -p "$OUT"

# Arm D — the checker's named in-box complement: 20+ waves at 2e5 (canonical absolute-tick cut).
$W 200000 700000 > "$OUT/armD_2e5_cut700k.txt"
# Arm E — N at this box's 2 GB ceiling (4.2e5; steady ~4,763 B/body -> ~1.9 GB), two waves.
$W 420000 60000 > "$OUT/armE_42e5_cut60k.txt"

# Determinism (prediction 7): the canonical digests must reproduce bit-for-bit.
grep -q "digest: 90348a698294dd47ccfca67a70dc890b8ea8835030bdd1a22eb2a74ee8293004" "$OUT/armD_2e5_cut700k.txt" \
  && echo "arm D digest bit-identical on rerun"
grep -q "digest: 0dec42f3c4416fec8e11b31e55edc456197d6c78ea9d1e0e649a00354a1e42f5" "$OUT/armE_42e5_cut60k.txt" \
  && echo "arm E digest bit-identical on rerun"

# The fixed analyzer (4af4's crashed: '%'-format TypeError, masked by `|| true`).
python3 "$R/analyze.py" "$OUT/armD_2e5_cut700k.txt" > "$OUT/reportD.txt"
python3 "$R/analyze.py" "$OUT/armE_42e5_cut60k.txt" > "$OUT/reportE.txt"
# It also regenerates 4af4's own wave tables from that run's shipped logs (the record fix):
python3 "$R/analyze.py" "$OUT/armA_3e5_cut150k.txt" > "$OUT/reportA_fixed.txt"
python3 "$R/analyze.py" "$OUT/armC_2e5_cut250k.txt" > "$OUT/reportC_fixed.txt"

# The floor-rise table (dossier's dissolution numbers) from arm D:
python3 - "$OUT" <<'EOF'
import sys
rows = []
for line in open(sys.argv[1] + "/armD_2e5_cut700k.txt"):
    if line.startswith("w:"):
        d = dict(kv.split("=") for kv in line[2:].split())
        rows.append((float(d["game_s"]), float(d["kicks"]), float(d["rss"]), float(d["lag"]), float(d["max_ms"]), float(d["over"])))
print("game_s-window  floor  peak  ratio  rss  over  max_ms")
for t0 in range(10000, 700000, 25000):
    win = [r for r in rows if t0 <= r[0] < t0 + 25000]
    if not win:
        continue
    fl = min(r[1] for r in win); pk = max(r[1] for r in win)
    print(f"{t0//1000:>4}k-{(t0+25000)//1000:<3}k  {fl:5.0f} {pk:6.0f} {pk/max(fl,1):5.1f}x {min(r[2] for r in win):4.0f} {sum(r[5] for r in win):4.0f} {max(r[4] for r in win):5.2f}")
EOF

grep -hE "^(end|digest|train):" "$OUT/armD_2e5_cut700k.txt" "$OUT/armE_42e5_cut60k.txt" > "$OUT/regen_summary.txt"
echo done
