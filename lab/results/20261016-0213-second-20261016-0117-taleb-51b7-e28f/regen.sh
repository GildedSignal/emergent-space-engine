#!/bin/sh
# Regenerates every number in dossier.md for run 20261016-0213-second-20261016-0117-taleb-51b7-e28f.
# The runner applies work/patch.diff (the belt scenario + this example + the snapshot-sharing cure in
# encounter.rs) before this runs. Total ~9 min; the two long items are the 1e5 flush arm (~140 s,
# the answer bill) and ladder_digest (~115 s). SCAN_SHARE=0 is the shipped mint inside the same binary.
cd "$(dirname "$0")/../../.."
RUN=lab/results/20261016-0213-second-20261016-0117-taleb-51b7-e28f
RAW=$RUN/raw
mkdir -p "$RAW"
if [ ! -f crates/universe/examples/belt_ladder.rs ]; then
  cp "$RUN/belt_ladder.rs" crates/universe/examples/belt_ladder.rs
fi
E="cargo run --release -p emergent-universe --example belt_ladder --"
# Quiet controls: the cure leaves the quiet plane bit-for-bit (digests 612c1388 / c459ac4b), and the
# mint counters read zero (the record's held-based "quiet mints zero", now seen directly).
$E 10000 belt 8                      | tee "$RAW/quiet_1e4_8s.txt" | tail -1
SCAN_SHARE=0 $E 100000 belt 3            | tee "$RAW/quiet_1e5_3s_ship.txt" | tail -1
# Identity A/B, budget-free (the trusted digest class), one word: ship vs cure digests must be equal.
SCAN_SHARE=0 $E 1000 beltburn 3 100 10000   | tee "$RAW/burnfree_1e3_ship.txt" | tail -1
SCAN_SHARE=1 $E 1000 beltburn 3 100 10000   | tee "$RAW/burnfree_1e3_cure.txt" | tail -1
SCAN_SHARE=0 $E 10000 beltburn 8 100 10000  | tee "$RAW/burnfree_1e4_ship.txt" | tail -1
SCAN_SHARE=1 $E 10000 beltburn 8 100 10000  | tee "$RAW/burnfree_1e4_cure.txt" | tail -1
# The 1e5 burn pair truncates at the wall cap (~2.3 s/frame: the answer bill paid inline); the two
# sides can truncate at different frames under load (first run matched at 64/64; a regen rerun split
# 63/59), so this pair is the mint-law witness (21 vs 1 mints), NOT an identity claim -- the robust
# 1e5 identity is the quiet pair above. Disclosed in the dossier.
SCAN_SHARE=0 $E 100000 beltburn 2 100 10000 | tee "$RAW/burnfree_1e5_ship.txt" | tail -1
SCAN_SHARE=1 $E 100000 beltburn 2 100 10000 | tee "$RAW/burnfree_1e5_cure.txt" | tail -1
# Identity A/B, sustained burn (word re-issued every 30 frames; args: x = flush anyway, 30 = hold_every).
SCAN_SHARE=0 $E 10000 beltburnhold 20 100 10000 x 30 | tee "$RAW/holdfree_1e4_ship.txt" | tail -1
SCAN_SHARE=1 $E 10000 beltburnhold 20 100 10000 x 30 | tee "$RAW/holdfree_1e4_cure.txt" | tail -1
# The fence-killer arms (budget on, 12 ms):
#   1e4 word: the record's shipped arm (730 MB, held 633) completes at 44 MB cured.
SCAN_SHARE=1 $E 10000 beltburn 8            | tee "$RAW/burn_1e4_8s_cure.txt" | tail -1
#   1e5 word (the record's fenced arm: dead at 148 scans / 1.9 GB in 2.5 s): completes all 720 frames,
#   ONE snapshot; the end-of-run flush measures the answer bill (~118 s for 606 held / 304 distinct).
SCAN_SHARE=1 $E 100000 beltburn 12          | tee "$RAW/burn_1e5_12s_cure.txt" | tail -1
# Sustained (hold_every=1, noflush): the count arms. Ship side fences (~1.9 GB at ~430 changes);
# cure sides complete with mints=1 (10^4: 840-971 consecutive changes; 10^5: 606).
SCAN_SHARE=0 $E 10000 beltburnhold 45 100 12 noflush 1  | tee "$RAW/hold_1e4_45s_ship.txt" | tail -1
SCAN_SHARE=1 $E 10000 beltburnhold 45 100 12 noflush 1  | tee "$RAW/hold_1e4_45s_cure.txt" | tail -1
SCAN_SHARE=1 $E 10000 beltburnhold 90 100 12 noflush 1  | tee "$RAW/hold_1e4_90s_cure.txt" | tail -1
SCAN_SHARE=1 $E 100000 beltburnhold 12 100 12 noflush 1 | tee "$RAW/hold_1e5_12s_cure.txt" | tail -1
# The shipped plane, bit for bit, cure compiled in: all 10 rows must equal the record's ladder_digest
# (4b822570 / 9e46f10f / bab8d6f5 / 6895ce06 / 8eb769bd / 484ccce0 / ddd5b1cc / 69d7abbb / 253d8aed / df0e87cd).
timeout 220 cargo run --release -p emergent-universe --example ladder_digest 2>&1 | grep -E "^N=" | tee "$RAW/ladder_digest.txt"
echo REGEN-DONE
