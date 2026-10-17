#!/usr/bin/env bash
# Regenerates every number in dossier.md from shipped code + this run's patch
# (work/patch.diff = the single new example file, no engine edit).
# ~7 min on the shared lab box; every process < 2 GB, draws ≤ 6 s.
set -u
cd "$(git rev-parse --show-toplevel)"
O=lab/results/20261017-1018-taleb-01e7/out
mkdir -p "$O"
cargo build -p emergent-allocator --release --offline --example finpol 2>&1 | tail -1
B=${CARGO_TARGET_DIR:-target}/release/examples/finpol
pan() { grep -o "rollback of region [0-9]* from [0-9]* would revise its published tick [0-9]*" "$1" 2>/dev/null | head -1; }

# frames, selfchurn vmax 2 (the crashing regime), 9 draws
for s in 11 12 13 14 15 16 17 18 19; do timeout 15 $B selfchurn frames 120 6 128 600 2 $s > $O/sc2-r600-s$s.out 2> $O/sc2-r600-s$s.err; echo "sc2-r600 s$s exit=$? $(pan $O/sc2-r600-s$s.err)"; done
# on-grid chunked batch (128 = 8 x window 16), vmax 2 — the driver-rule test
for s in 11 12 13; do timeout 30 $B selfchurn chunks 120 1800 128 600 2 $s > $O/sc2-chunk128-s$s.out 2> $O/sc2-chunk128-s$s.err; echo "sc2-chunk128 s$s exit=$? $(pan $O/sc2-chunk128-s$s.err)"; done
# frames, selfchurn vmax 8 / vmax 16 (dispersion axis), r300, n480
for s in 11 12 13 14 15 16; do timeout 15 $B selfchurn frames 120 6 128 600 8 $s > $O/sc8-r600-s$s.out 2> $O/sc8-r600-s$s.err; echo "sc8-r600 s$s exit=$? $(pan $O/sc8-r600-s$s.err)"; done
for s in 11 12 13 14 15; do timeout 15 $B selfchurn frames 120 6 128 600 16 $s > $O/sc16-r600-s$s.out 2> $O/sc16-r600-s$s.err; echo "sc16-r600 s$s exit=$? $(pan $O/sc16-r600-s$s.err)"; done
for s in 11 12 13; do timeout 15 $B selfchurn frames 120 6 128 300 8 $s > $O/sc8-r300-s$s.out 2> $O/sc8-r300-s$s.err; echo "sc8-r300 s$s exit=$? $(pan $O/sc8-r300-s$s.err)"; done
for s in 11 12 13; do timeout 15 $B selfchurn frames 240 6 128 600 8 $s > $O/sc8n240-r600-s$s.out 2> $O/sc8n240-r600-s$s.err; echo "sc8n240 s$s exit=$? $(pan $O/sc8n240-r600-s$s.err)"; done
# no-churn controls: wave (planned merge) and crossing
for s in 12 13 14; do timeout 15 $B wave frames 120 6 128 600 8 $s > $O/wv-r600-s$s.out 2> $O/wv-r600-s$s.err; echo "wv-r600 s$s exit=$? $(pan $O/wv-r600-s$s.err)"; done
for s in 12 13; do timeout 15 $B wave frames 120 6 128 1200 8 $s > $O/wv-r1200-s$s.out 2> $O/wv-r1200-s$s.err; echo "wv-r1200 s$s exit=$? $(pan $O/wv-r1200-s$s.err)"; done
for s in 11 12 13 14; do timeout 15 $B crossing frames 120 6 128 600 8 $s > $O/xc-r600-s$s.out 2> $O/xc-r600-s$s.err; echo "xc-r600 s$s exit=$? $(pan $O/xc-r600-s$s.err)"; done
# guards, in the crashing regime (vmax 2)
for s in 11 12 13; do FINPOL_MINREGION=32 timeout 15 $B selfchurn frames 120 6 128 600 2 $s > $O/sc2-mr32-s$s.out 2> $O/sc2-mr32-s$s.err; echo "sc2-mr32 s$s exit=$? $(pan $O/sc2-mr32-s$s.err)"; done
for s in 11 12 13; do FINPOL_WINDOW=32 timeout 15 $B selfchurn frames 120 6 128 600 2 $s > $O/sc2-w32-s$s.out 2> $O/sc2-w32-s$s.err; echo "sc2-w32 s$s exit=$? $(pan $O/sc2-w32-s$s.err)"; done
# batch single call
timeout 60 $B selfchurn batch 120 1800 128 600 2 11 > $O/sc2-batch-s11.out 2> $O/sc2-batch-s11.err; echo "sc2-batch exit=$? $(pan $O/sc2-batch-s11.err)"
timeout 60 $B selfchurn batch 120 1800 128 600 8 11 > $O/sc8-batch-s11.out 2> $O/sc8-batch-s11.err; echo "sc8-batch exit=$? $(pan $O/sc8-batch-s11.err)"

echo "=== summary (rb from .out, panic from .err) ==="
for f in "$O"/*.out; do b=$(basename "$f" .out); rb=$(grep -o 'rb *[0-9]*' "$f" | head -1 | grep -o '[0-9]*'); c=$(grep -c 'would revise' "${f%.out}.err" 2>/dev/null || true); echo "$b rb=${rb:-NA} crash=$c"; done | sort
