#!/usr/bin/env bash
# Regenerates every number in dossier.md from shipped code + work/patch.diff
# (patch = the single new example file finpol.rs, inherited verbatim from
#  20261017-1018-taleb-01e7; no engine edit).
# ~8 min on the shared lab box; every process < 2 GB, frames draws <= 6 s wall.
set -u
cd "$(git rev-parse --show-toplevel)"
O=lab/results/20261017-1149-second-20261017-1018-taleb-01e7-bc0f/out
mkdir -p "$O"
cargo build -p emergent-allocator --release --offline --example finpol 2>&1 | tail -1
B=${CARGO_TARGET_DIR:-target}/release/examples/finpol
pan() { grep -o "rollback of region [0-9]* from [0-9]* would revise its published tick [0-9]*" "$1" 2>/dev/null | head -1; }

# ---------- core arms (the standing record, re-run so every table row regenerates) ----------
for s in 11 12 13 14 15 16 17 18 19; do timeout 15 $B selfchurn frames 120 6 128 600 2 $s > $O/sc2-r600-s$s.out 2> $O/sc2-r600-s$s.err; echo "sc2-r600 s$s exit=$? $(pan $O/sc2-r600-s$s.err)"; done
for s in 11 12 13; do timeout 30 $B selfchurn chunks 120 1800 128 600 2 $s > $O/sc2-chunk128-s$s.out 2> $O/sc2-chunk128-s$s.err; echo "sc2-chunk128 s$s exit=$? $(pan $O/sc2-chunk128-s$s.err)"; done
for s in 11 12 13 14 15 16; do timeout 15 $B selfchurn frames 120 6 128 600 8 $s > $O/sc8-r600-s$s.out 2> $O/sc8-r600-s$s.err; echo "sc8-r600 s$s exit=$? $(pan $O/sc8-r600-s$s.err)"; done
for s in 11 12 13; do timeout 15 $B selfchurn frames 120 6 128 300 8 $s > $O/sc8-r300-s$s.out 2> $O/sc8-r300-s$s.err; echo "sc8-r300 s$s exit=$? $(pan $O/sc8-r300-s$s.err)"; done
for s in 11 12 13; do timeout 20 $B selfchurn frames 240 6 128 600 8 $s > $O/sc8-n480-s$s.out 2> $O/sc8-n480-s$s.err; echo "sc8-n480 s$s exit=$? $(pan $O/sc8-n480-s$s.err)"; done
for s in 12 13 14; do timeout 15 $B wave frames 120 6 128 600 8 $s > $O/wv-r600-s$s.out 2> $O/wv-r600-s$s.err; echo "wv-r600 s$s exit=$? $(pan $O/wv-r600-s$s.err)"; done
for s in 12 13; do timeout 15 $B wave frames 120 6 128 1200 8 $s > $O/wv-r1200-s$s.out 2> $O/wv-r1200-s$s.err; echo "wv-r1200 s$s exit=$? $(pan $O/wv-r1200-s$s.err)"; done
for s in 11 12 13 14; do timeout 15 $B crossing frames 120 6 128 600 8 $s > $O/xc-r600-s$s.out 2> $O/xc-r600-s$s.err; echo "xc-r600 s$s exit=$? $(pan $O/xc-r600-s$s.err)"; done
for s in 11 12 13; do FINPOL_MINREGION=32 timeout 15 $B selfchurn frames 120 6 128 600 2 $s > $O/sc2-mr32-s$s.out 2> $O/sc2-mr32-s$s.err; echo "sc2-mr32 s$s exit=$? $(pan $O/sc2-mr32-s$s.err)"; done
for s in 11 12 13; do FINPOL_WINDOW=32 timeout 15 $B selfchurn frames 120 6 128 600 2 $s > $O/sc2-w32-s$s.out 2> $O/sc2-w32-s$s.err; echo "sc2-w32 s$s exit=$? $(pan $O/sc2-w32-s$s.err)"; done

# ---------- arm A: single-call batch, on-grid vs off-grid horizon, seeds x replicates ----------
# 1792 = 112 x window 16 (on-grid); 1800 off-grid. Seeds {11,15,21} x 2 replicates each.
for h in 1792 1800; do for s in 11 15 21; do for r in 1 2; do
  timeout 60 $B selfchurn batch 120 $h 128 600 2 $s > $O/sc2-batch$h-s$s-r$r.out 2> $O/sc2-batch$h-s$s-r$r.err
  echo "sc2-batch$h s$s r$r exit=$? $(pan $O/sc2-batch$h-s$s-r$r.err)"
done; done; done

# ---------- arm B: vmax-16 incidence, fresh seeds {22,23,24} x 2 replicates ----------
for s in 22 23 24; do for r in 1 2; do
  timeout 15 $B selfchurn frames 120 6 128 600 16 $s > $O/sc16-r600-s$s-r$r.out 2> $O/sc16-r600-s$s-r$r.err
  echo "sc16-r600 s$s r$r exit=$? $(pan $O/sc16-r600-s$s-r$r.err)"
done; done

# ---------- arm C: n=480 bodies (arg 240) at vmax 2, seeds {11,12,13} x 2 replicates ----------
for s in 11 12 13; do for r in 1 2; do
  timeout 25 $B selfchurn frames 240 6 128 600 2 $s > $O/sc2-n480-s$s-r$r.out 2> $O/sc2-n480-s$s-r$r.err
  echo "sc2-n480 s$s r$r exit=$? $(pan $O/sc2-n480-s$s-r$r.err)"
done; done

echo "=== summary (rb/E from .out rows; crash from .err) ==="
for f in "$O"/*.out; do b=$(basename "$f" .out); rb=$(grep -o 'rb *[0-9]*' "$f" | head -1 | grep -o '[0-9]*'); c=$(grep -c 'would revise' "${f%.out}.err" 2>/dev/null || true); echo "$b rb=${rb:-NA} crash=$c"; done | sort
