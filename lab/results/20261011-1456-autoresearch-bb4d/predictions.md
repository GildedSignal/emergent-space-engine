# Held-out predictions (written before the decisive optimized run)

Baseline (instrumented build, KICK_REPS=9, seconds=20, seed 1): made-kick median 42-56 µs, leaver median 362-380 µs, kick_us_all median 44.4 µs; quad = 129 µs/kick (~140 quad calls/kick, ~200 ns/node); cut = 9 µs/kick; compile = 84% of a kick. Digests: plane `46d63fe0cb18daee…`, replay `f3e04738b88805ce…`.

Change under test: replace `fast_quad`'s four native u128/u128 divisions (`__udivti3` software division on this x86-64) with the exact word division `div_word`, guarded so any case outside its precondition falls back to the original division. Bit-identical by construction; verified by digest equality.

Held-out cases (not tuned on, run once at the end):
1. `--kick-bench --seconds 20 --seed 7` (never measured before this file): made-kick and leaver medians improve by the same factor as seed 1 (predicted 1.3-1.8x), `refused: 0`.
2. `--kick-bench --seconds 20 --seed 13`: same expectation.
3. `--bench --rtf 100 --seconds 20 --unpaced` (the whole plane): engine p50 frame CPU drops (engine share was 20%: ship 70 µs/item, player 344 µs/item), view_gather share rises, and the canonical-cut digest `6ce636fa…` is IDENTICAL (same bits, any budget).
4. `cargo test -p emergent-space` (the crate's own suites, including its exactness tests): all green, unchanged.

Falsifier: any digest change, any refusal increase, or a speedup that shows only on the tuned seed 1.
