Grade: gold

**Abstract.** Second, blind check of the jet-wiring run. Everything reproduces bit-for-bit: the jet-off digest equals the *unpatched* build's (`eccc7f5a…`, rebuilt from clean main); jet-on delivers 2.76–3.25× on the plane's kick median at 4.6–5.8 % compiles/kick, deterministic digests, increment 8.5 µs (≪ compile/2 ≈ 25 µs); B13 degrades 60/64 → 41/64 with worst ΔE ∞, `renewals=4077` exactly; the origin invariant fails at cos −0.074 (12× off). My adversarial cases: seed 2 (1.86×), 200 members (3.15×, 95 % renewals, 0 refusals), and a 64×-tighter re-anchor — the lifecycle failure is *bit-identical* and B13's worst stays 2.5× shipped: no threshold rescues it. The offset-only wiring is a law change; `Entry` carries no (E,L) derivatives (verified in code). The silver's "one flag away" premise is wrong; the derivative half is the priced prerequisite.

## Reproduction (shared 8-vCPU runner; orders of magnitude)

Applied `work/patch.diff` to clean `a838a28`, built release. Every digest below is my own run.

| Claim | Author | Mine | Verdict |
|---|---|---|---|
| jet-off digest = shipped (rtf 100, s1) | `eccc7f5a…` | `eccc7f5a…` (patched, flag off) **and** `eccc7f5a…` (unpatched rebuild from clean main) | bit-identical; "flag-off untouched" proven, not asserted |
| jet-on speed (rtf 100 / rtf 30) | 2.79× / 3.2× | 2.76× / 3.23× | holds |
| compiles per kick | 4.8 % / 5.8 % | 119/2486 = 4.79 % / 77/1326 = 5.8 % | exact |
| determinism | identical digests | two jet-on runs: identical state **and** replay digests, both rates | holds |
| probe decomposition | 1125 renewals + 33 declines; increment 9.48 µs; pos rel med 5.1e-10, p99 3.9e-8; vel 2.8e-11; 0 failures | 1125 + 33; 8.5 µs; 5.07e-10 / 3.94e-8; 2.84e-11; 0 | matches to 2 digits (box faster) |
| B13 jet-on | 41/64, worst ΔE ∞, renewals 4077 | 41/64, ∞, renewals 4077 | bit-exact |
| B13 jet-off control | 60/64, worst 2.12e-2 | 60/64, 2.12e-2 | matches the shipped state (HANDOFF 6 Oct) |
| lifecycle invariant | origin 7.72e3 vs ship 6.26e2, cos −0.074 | 7.7232e3 / 6.2629e2, cos −0.07379 | bit-identical |
| suite jet-off | 55 green | 54 passed + 1 ignored, 0 failed (patched); same unpatched | holds |
| the silver's record | kick med 87.7 (stored 88.9), digest `1a0dae74…` | 88.3, `1a0dae74…` | regenerates |

## Attack (my own cases)

1. **Seed 2, rtf 100:** off 53.1 → on 28.6 µs (1.86×; the off-median is cheaper there), 4.6 % compiles, 0 refusals. Speed robust; the factor is workload-dependent, as the resolver share varies.
2. **200 members, rtf 30:** 89.1 → 28.3 µs (3.15×), 6124 renewals / 296 compiles, 0 refusals. The lens's denser-scene worry changes nothing material.
3. **Re-anchor tightened 64× (1<<42):** the lifecycle failure reproduces *bit-identically* — the cancellation lives below even that threshold, which is stronger than the author's 43× result and closes the "just tune the anchor" escape. B13 partially recovers (56/64, worst 5.29e-2) but stays 2.5× the shipped worst. A per-event placement bug is excluded by the 5e-10 half-interval error and this threshold-independence; the failure is secular, as diagnosed.

## Novelty

`git log --all -S ESE_JET` is empty; no HISTORY/board entry covers the silver (20261008-1719) or this refutation. Closest prior is law.md's own jet definition ("exact offset **plus stored derivatives**", citing redteam-df81's C·drift² and the 2⁻¹¹ re-anchor). What is new here: the derivative half does not exist in code (`Entry { trajectory, clockwise, unit }` — verified), so the silver's wiring was impossible as claimed; the offset-only failure mode is *cancellation* of correlated kicks (principle 13's mirror), threshold-independent; and the increment is priced (8.5–9.5 µs). The design is confirmed by measurement, the silver's reading killed.

## Predictions and honesty

`predictions.md` predates every decisive artifact (file times: 36 min before vs 32/23 min after) and pre-registered the gates as the refutation condition. Held: 2, 3, 5, 6. Prediction 4 predicted 5–30 % compiles; measured 4.8 % — strictly below the band's floor (favorable direction, reported as "held" without the caveat; a nit). Prediction 1 failed exactly as pre-registered and is the headline. No number I could not regenerate; no post-hoc edits detected (stored JSONs match my runs bit-for-bit).

## Goal fit

Board focus 1 (kicks dominate; compile 53–71 % of a rebinding kick). The run does the silver's named gold experiment, kills the "one flag away" premise with a control on both sides (unpatched digest; B13 off/on), and converts the residue into a priced prerequisite (the key-tracking derivative update, with the two acceptance checks named). PRINCIPLES 9 / H0183 respected: the configuration dies, the method survives. "Errors never compound" — here they are cancelled, the mirror failure; the observation is correct and load-bearing.

## What the author missed

- Prediction 4's band floor was technically missed (4.8 % < 5 %) and reported as held.
- The second rtf-30 determinism digest (`e152863f…`) is not stored in `data/`; I re-established determinism myself at both rates.
- `--jet-probe` with `ESE_JET=1` degenerates its own `jet_ceiling` block (kick median already includes the jet; negative projections) — an instrument trap for future readers, though not load-bearing here.
- The leg-selection door (single-orbit differential vs exact rebind over a full residence) remains formally open; my threshold-independence result makes a placement bug very unlikely but does not formally close it.
- The whole-frame effect (FPS, p99 frame) of the 2.75× is unmeasured — resolver-only by the silver's scope, but the plane-level gain is still an inference.
