# Predictions — 20261021-0312-fermi-614b

Written before any census arm ran. The question: name the past-cap allocation chains on the player
path (budget-1e9 od 7) and measure their size law against K, so the at-10⁹ chain cost is an
extrapolation of a measured law instead of an assumption. Prior numbers I have not tuned on:
6e76's coast seed-2 past-cap chains (16 player reallocs, mean 114,688 B), 8994's burn chains
(3,670,016 B at 10⁴, 7,340,032 B at 3×10⁴), the 95.7% filter die-off.

Held-out cases (I will run them only after this file is written):

1. **Coast, seed 2, N=10⁴, 30 s at rtf 100.** Prediction: allocations ≥ 61,440 B occur during the
   flight; their backtraces land in `PlayerNeighbourhood::capture` (crates/universe/src/encounter.rs,
   the `candidates: Vec<(usize, Binding, Scalar)>` build), sizes sit on doubling rungs (448 B × 2^k),
   and every one coincides with a `Radial::candidates` fallback (`None`). The counter
   `capture.loop ≈ fallback × bodies + indexed × ids` (≥ 90% of iterations from the fallback).
2. **Burn, seed 1, N=10⁴ and 3×10⁴, 10 s.** Prediction: the chains reproduce (3.7 MB / 7.3 MB rungs
   ± a rung), same site, and `capture.max` (exact content, first time measured) is between 4,097 and
   16,384 entries at 10⁴. The die-off (loop−tuples)/loop ≈ 95%+.
3. **The size law, N = 10⁵ and 3×10⁵.** Prediction: `capture.max` grows with K with exponent below 1
   (point estimate 0.5–0.9): the pulled set is window-limited (a fixed-metre reach meeting a denser
   belt), not a fixed fraction of the universe. If instead the exponent is ~1, the 0.25–0.37 TB/chain
   figure at 10⁹ stands; if it is ~0.5, the honest 10⁹ chain is ~10–40 GB (a frame-scaled stall, not
   seconds of bus).
4. **Rate.** On coast at N=10⁴ the fallback is rare (chains = isolated events, ≲ 1/s of game time);
   under the level-8 burn it fires on most frames while the burn lasts, so chain bytes per game-second
   of burn at 10⁹ ≈ 448 B × max × fallback/game-s. I expect this to be the row that decides whether
   the fix is mandatory (≥ 60 GB/s equivalents during a burn) or merely good (≪ bus).

What would make me wrong: chains whose backtraces land outside `capture` (then the site is elsewhere
and the od-7 letter is wrong); `capture.loop` not explained by fallback × N (then the fallback is not
the read set); exponent ≈ 1 with content tracking K exactly (linear pull — the 10⁹ figure stands).
