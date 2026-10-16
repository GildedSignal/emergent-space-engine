#!/bin/sh
# Regenenerates every number in dossier.md for run 20261016-0117-taleb-51b7.
# The runner applies work/patch.diff (scenario.rs belt_player + this example) before this runs.
# Belt arms <= 20 s each; the two wave arms are 140-145 s by design (the wave is at 130-145 s wall
# at rtf 100); ladder_digest is cut at 110 s (its last row completes). Total ~11 min.
cd "$(dirname "$0")/../../.."
RUN=lab/results/20261016-0117-taleb-51b7
RAW=$RUN/raw
mkdir -p "$RAW"
# The patch's example file, in case the runner's patch missed the untracked file:
if [ ! -f crates/universe/examples/belt_ladder.rs ]; then
  cp "$RUN/belt_ladder.rs" crates/universe/examples/belt_ladder.rs
fi
E="cargo run --release -p emergent-universe --example belt_ladder --"
$E 10000 home 8        | tee "$RAW/home_1e4_8s.txt" | tail -1
$E 1000 belt 8         | tee "$RAW/belt_1e3_8s.txt" | tail -1
$E 10000 belt 8        | tee "$RAW/belt_1e4_8s.txt" | tail -1
$E 10000 belt 8        | tee "$RAW/belt_1e4_8s_again.txt" | tail -1   # digest identity (quiet)
$E 100000 belt 20      | tee "$RAW/belt_1e5_20s.txt" | tail -1
$E 1000 beltburn 8     | tee "$RAW/beltburn_1e3_8s.txt" | tail -1
$E 10000 beltburn 8    | tee "$RAW/beltburn_1e4_8s.txt" | tail -1
$E 100000 beltburn 12  | tee "$RAW/beltburn_1e5_12s.txt" | tail -1   # self-fences at 1.9 GB
$E 10000 beltburn 8 100 10000 | tee "$RAW/beltburn_1e4_8s_nobudget.txt" | tail -1
$E 10000 beltburn 8 100 10000 | tee "$RAW/beltburn_1e4_8s_nobudget_again.txt" | tail -1  # digest identity
$E 10000 belt 145      | tee "$RAW/belt_1e4_wave.txt" | tail -1      # through the first-kick wave
$E 100000 belt 140     | tee "$RAW/belt_1e5_wave.txt" | tail -1      # through the first-kick wave
# Bits held: the shipped plane's digests on the patched tree vs the pristine tree (dossier names
# the three pristine values; 4 schedules agree inside each run).
timeout 110 cargo run --release -p emergent-universe --example ladder_digest 2>&1 | grep -E "^N=" | tee "$RAW/ladder_digest.txt"
echo REGEN-DONE
