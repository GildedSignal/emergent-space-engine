# Dossier — H_live measured on the plane's own law: the lattice, not the rate, breaks 10⁹ in 8 GB

Run: `20261008-2113-components-a9d7` (components lens). 8 October 2026.

## Claim (one sentence)

On the plane's own law and scene, distinctions are so rare (3.5×10⁻⁵ fired kicks per body per game-second, invariant across belt, seed and N) that H_live as a *rate* is trivially affordable at a billion bodies (≈0.4 MB/s of stream), but each distinction costs ~86 bits because the velocity lattice sits at 2⁻⁷⁴ c — so the per-body deviation state (~104 bits after 139 days, growing ballistically at +2 bits per time-doubling) exceeds the entire 64-bit-per-body budget of 10⁹ bodies in 8 GB from the very first kick: the store's floor is set by the lattice exponent, not by the body count, and the fix the measurement points at is a deviation-native quantum (~2⁻³³ c, 25–30 bits per kick) with program re-anchoring.

## The component, its owner, its floor

The **storage** component (the body store behind `BodyStore`; `crates/shipmem` is its research form).
Requirement owners: PRINCIPLES 24 "The memory floor is information"; 6 "Store the generator, not the generated"; plane.md "Distinctions created per game-second … this, not the body count, decides whether a billion bodies fit" — the quantity HANDOFF lists as **not measured yet**.
The floor is information-theoretic: bits per body = program (measured 0.126 bits, gold `components-98bc`) + the exact deviation from the program that the law's own integers create (the kick stream) − what reabsorption removes. A population's store = program + scars; the program predicts each body's birth tube and the star's compiled drift conserves it, so **every departure enters through kicks**, whose integers the engine already carries (`Kick::dv`, and across a rebind the integer velocity jump between the retired and the new binding).

## What was measured (the instrument)

`crates/universe/examples/hlive.rs` (new, ~200 lines): the plane's star and its three planets (`scenario::PLANETS`), a belt of ships on the root doll, no fleet, no player, advanced headless by `settle()` at the population's minimum step, `prune()` run like the plane does. Per **fired** kick (the resolver only rebinds when the quantized dv ≠ 0 — sub-quantum kicks stay in the sigma-delta carry and write nothing) it records the exact integer velocity jump between the retired binding and the new one read at the same tick, both velocity exponents, and the carry; at 16 sample times it records the state tuple. Entropies are exact-integer moments (differential entropy on the lattice, log₂(2πe·σx·σy), controlled by a coarse exact histogram); **distinct-value entropies are saturated at log₂N and are not entropy** (the first version of this analysis made that mistake and was rewritten). Digests before/after are unchanged by the instrument (pilot `051deb2f…` identical across instrumented and uninstrumented builds).

## Evidence

Reproduce: `cargo build --release -p emergent-universe --example hlive`, then in `lab/results/<run>/data/`:
`/path/to/examples/hlive 512 2 1.2e7 spread 16 s2` (each run ≤ 35 s wall, < 0.5 GB), `python3 ../shrink.py s2`, `python3 ../analyze.py s2 s3 inner outer` (the outer kicks file is split `a`/`b` to keep each file under 5 MB; the loader rejoins it). Held-out runs (predictions written first): `s2` (seed 2, n 512, spread, 1.2×10⁷ s ≈ 139 days), `s3` (seed 3, same), `inner` (seed 7, n 384, a∈[0.5,3] AU), `outer` (seed 11, n 384, a∈[3,8] AU, Giant inside the belt). Tuning (plumbing only) on seed 1.

| quantity | s2 | s3 | inner | outer |
|---|---|---|---|---|
| fired kicks | 219,822 | 222,966 | 54,513 | 279,175 |
| kicks/body/game-s | 3.58e-5 | 3.63e-5 | 3.55e-5 | 3.64e-5 |
| bits per kick (lattice) | 85.9 | 87.3 | 79.3 | 88.7 |
| kick σ (c) | 1.0e-10 | 0.9e-10 | 2.7e-11 | 2.5e-10 |
| gross bits/body/s | 3.07e-3 | 3.17e-3 | 2.81e-3 | 3.22e-3 |
| net deviation bits at horizon | 103.7 | 106.3 | 93.1 | 109.7 |
| net growth, bits per log₂ t | 2.0 | 2.2 | 1.9 | 3.1 |
| carry bits (bounded, ±2¹⁶) | 34.2 | 34.3 | 34.5 | 34.0 |
| bodies back at D = 0 exactly | 0 | 0 | 0 | 0 |
| PlainBodies bytes/body | 1,497 | 1,483 | 1,506 | 1,491 |

Headline consequences:
- **Rate**: one fired kick per body per ~7.8 hours of game time, the same to 3% across both seeds, n = 256→512, and inner vs outer belts (the kick cadence is not per-orbit — prediction 1's inner/outer ratio of ≥20× was wrong; the fictitious clock sets it, nearly belt-independent). At 10⁹ bodies the fired-kick stream is ~36 kHz of events, ≈0.4 MB/s, ≈1.4 GB per game-hour if every kick were stored raw — affordable for hours, not for a persistent store.
- **Per-event cost**: ~86 bits per kick. Not because the physics is rich but because the lattice is: kick σ ≈ 10⁻¹⁰ c on a 2⁻⁷⁴ c lattice is ~2⁴¹ quanta per axis; `choose_units` spends the i64 (velocity 2×10⁻³ c = 2⁻⁹ needs 64 − 9 = 73 trailing bits) on resolution the dynamics at this scale does not consume. The magnitude-class entropy is 2.1–2.5 bits.
- **Net state**: the velocity deviation from the program reaches ~104 bits per body by day 139 and grows **ballistically** (+2 bits per doubling of time, vs the random walk's +1): kicks accumulate coherently — secular, not noise. No body ever returns to exactly D = 0 (reabsorption to the birth program never happens at this lattice), and the carry stays bounded exactly as documented (±65,515 ≈ ±2¹⁶, 34 bits).
- **The verdict**: 8 GB / 10⁹ bodies = 64 bits/body for *everything* (program, tube, scars). The measured velocity-deviation alone exceeds that from the first kick (86 bits). At 10⁹ bodies, a 10-game-year belt needs ~(113 + 34) bits ≈ 18 B/body for velocity scars alone ≈ 18 GB — **does not fit; the budget is broken by the lattice, not the count or the rate.**
- **Idiot index**: current store 1,497 B/body = 93× the 16-byte logical tube (prediction 7 ✓); and each distinction costs ~86 bits where a deviation-sized lattice (~2⁻³³ c, resolving the kick's σ to ~1%) would cost 25–30 — a ~3× that compounds per event, ~60 bits saved per kick forever.

## Predictions (`predictions.md`): what held, what did not

Held: rate order 10⁻⁵ (3.5e-5 ✓); magnitude-class entropy 2.1–2.5 within the 4–14 band; carry bounded ±2¹⁶ (34 bits ✓); store ≥ ~100× the tube (93× ✓); gross stream at 10⁹ ≈ GB-per-hour order (1.4 GB/h, at the top of the band, ✓ direction).
Missed, honestly: (1) inner vs outer rate ≥20× — measured equal (the cadence is clock-set, not orbit-set); (2) H(dv) 4–14 bits — measured 86: the prediction ignored the lattice exponent, which is the finding; (3) net 6–20 bits after 10 years — measured 104 at 139 days growing +2/doubling: I predicted a random walk from a small start; the kicks are coherent (secular) and the first kick alone carries 86 bits; (4) stray-item check <5% — measured ~97% in spread/outer (one engine item per fire that changes no binding: boundaries vs non-firing epochs cannot be separated post-hoc), 2.5% in inner. The entropy numbers are unaffected (rows are fires, verified by construction: the resolver rebinds only on dv ≠ 0).

## What would make it wrong

- The net-deviation bits are a **lower bound** on the scar (velocity deviation only; the tube's timing/angle deviations are not yet measured and plausibly double it — so the verdict is conservative in the direction of "worse").
- If the law's exactness (principle 13) can be kept with deviation quanta coarser than 2⁻³³ c — i.e. if the B5/B12 error floors permit a 2⁻³³ c velocity lattice for this regime — the per-kick cost drops to ~25–30 bits and the 10-year belt fits in ~6 GB; that boundary (error floor vs lattice) is the next experiment, and it is exactly gate territory (B5, B12).
- Re-anchoring the program (reset the deviation reference at √(floor/C), as the gold re-anchor rule does for memos) turns ballistic growth into a bounded quantity, but only if the anchor epoch is itself derivable — otherwise it adds a per-body clock.
- The scene has no encounters and no resonant kicks near a planet's shell (no body entered a changeover level: all kicks level 0); concentrated fleets (the 6 October gold) will have higher, correlated rates.

## Cost of adopting, fit with PRINCIPLES

Adopting the measurement: none (an example binary; `run.sh` saves it as a patch; no engine file touched — verified by unchanged digests). Adopting the *consequence* is a representation change in `shipmem`/bindings: store deviations relative to the program on a deviation-sized lattice. Fits: "The memory floor is information" (24); "Compute only surprises" (3) — the surprise is rare but written at 86 bits where ~27 would do; "we just need to have the right representation so that math is trivial" (18); "what's the biggest quantization that we can get away with?" (16, OC#38). It also feeds B18's floor: the gate should demand the *deviation* quantum, not the absolute one.

## The lens's blind spot

One component, one scene: the fleet (Fermi frames, contacts) and the player are absent; encounters and changeover levels never fired; the belt is born cold (Rayleigh-lite e ≤ 0.25). The neighbours (kick *compute* cost, the recompile churn measured at ~70 µs/kick here — consistent with the memo story) were not the target and could move if the lattice changes: a coarser lattice also shrinks the recompile rate's exactness burden, but that is a claim for another run.
