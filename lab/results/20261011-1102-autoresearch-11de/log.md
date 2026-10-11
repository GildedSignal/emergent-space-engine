# Autoresearch log — 20261011-1102 (lens: autoresearch on something that works)

Artifact: the shipped per-kick path, `crates/space` (`readout -> parent_tide -> handoff::bind`).
Metric: ns/kick (best of 5 × 64 kicks) on 4 tuned scenes; behaviour held by the blake3 digest
of the TubeEvent stream + `cargo test -p emergent-space` (50 tests).
Machine: shared 8-vCPU Linux, load 0.9–1.5 recorded per run; orders of magnitude only.

| # | Hypothesis | Change | Metric (tuned scenes, µs/kick) | Kept? |
|---|---|---|---|---|
| 0 | — | baseline | 18.6 / 36.1 / 49.8 / 49.4; bind = 86–94% of kick; compile-only 3.5/19.2/30.5/31.0 µs | — |
| 1 | fast_quad's four u128/u128 divisions have u64 divisors satisfying div_word's precondition → identical floor, native width | `num::div_word` for g, g1, ratio, rt (orbit.rs fast_quad) | 18.7 / 36.7 / 47.0 / 46.0 (−0–6%); digests identical | KEPT (bit-identical, never slower; below the 10% bar) |
| — | profile (perf blocked, paranoid=4; temporary in-crate timers, reverted) | — | quads are ~30/compile at 0.4–1.0 µs each; cuts 27/compile at ~0.2 µs; node = cos 44 ns + shape 44 ns + 3 div_word 51 ns | — |
| 2 | `TubeEvent::bind`'s `fit.reconstruct()` recomputes a state+cartesian to recover the caller's input (residuals are exact i128, so reconstruct ≡ input by construction) | pass `exact` into `TubeEvent::bind`, drop the reconstruct | 15.7–17.1 / 32.8–33.4 / 42.3–45.4 / 42.0–42.6 (−6–17%); digests identical on all 8 scenes; 50 space tests green | KEPT |
| 3 | candidates: cos micro-restructure (25% of node, <10% of kick), cut() memo (<10%), H2-style decode fusion in fit.decoded_event vs tube.state (NOT bit-identical by construction: mod-2π applied at different points) | none executed | analysis only | STOPPED (<10% each; three consecutive sub-10% rounds by round 1 + round 3 analysis; round 2 was the last ≥10%) |

Held-out run (`kickbench heldout`, after the final state, run once):
17.7 / 19.5 / 21.3 / 42.3 µs/kick vs baseline 20.3 / 23.6 / 23.5 / 47.3 → −13 / −17 / −9 / −11%;
digests 96496d6dfa0bb069, 564218447bbc3383, d2de595a7b2f6c66, 72e90661e4615503 — all identical to baseline.

The one idea that carried most of the gain: delete the recompute that recovers a value the caller
already holds (the exact event state), rather than making the arithmetic cheaper.
