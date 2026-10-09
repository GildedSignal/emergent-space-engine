Grade: silver

**Abstract.** Claim: a kicked belt's live distinctions saturate at ≈61 bits/scarred body, so 10⁹ bodies cost 7.6 GB (1.8× the 4 GiB budget); the lever is the residual quantum. Reproduced bit-identically (all four commands; only timing fields differ). Controls pass (f=0 flat at 0.03; random 211.78 vs floor 208.00). Predictions pre-registered; P3 failed honestly. Novel: HANDOFF said H_live "not measured yet". My attacks confirm the k̄-law and the quantum lever (heavy kicks ×2⁶: 84.35 bits/scar vs law's 84.1) but **falsify "saturates"**: at scar_frac=1 the cost walks ~2 bits per doubling of k̄ (61.8 @ k̄=3 → 66.9 @ k̄=24), the exact slope the author thought he had refuted; his main window ended inside the fraction phase. Adoption is a corrected law, not code.

## Reasons

1. **Reproduction: exact.** Applied `work/patch.diff` in the restored tree, built, ran all four commands. Every storage field bit-identical (`main` r24: 58.66 bits/body, 124,411 scars; `heldout` r40: 56.13 @ k̄=2.5; `f0` 0.03 flat; `random` 211.78). Only `*_ns_per_kick` differ (shared loaded machine; same orders: update ~0.2 µs, seal/compact ~2–4 µs). Round trips: `bad_p=0` over all 131,072 ordinals at r8/16/24; `bad_b=0` on all decoded rows. The `mismatches` counter is confirmed as the disclosed artifact (`decoded=65536` — group split; the `k != n` term fires once per verify round).
2. **Predictions.** File times order `predictions.md` (−5 m) before f0/random (−3 m), main (−1 m), heldout (last); `run.log` empty, so nothing contradicts. P1, P4, P5 held; P2 partial and P3 failed — both reported honestly, with P3's failure informative (form B never crosses P; B = P + 1.92 at every fraction).
3. **Adversarial cases (mine).**
   - **Deep diffusion (f=1, 24 rounds):** per-scarred-body 60.1 @ k̄=1, 61.8 @ 3, 63.7 @ 8, 66.4 @ 16, 66.9 @ 24. Beyond scar_frac→1 the walk is ~2 bits per doubling of k̄ — logarithmic, unbounded. The dossier's "saturates", "re-kicks are ~free" and "the asymptote" are wrong; the author's own P2 slope (+2/doubling) was right and the "measured +0.3" was the fraction phase masking it. The walk is slow in game time (k̄=1000 ≈ decades of play → ~78 bits), so the *verdict* (over budget; quantum is the lever) survives, but the law is per-scar ≈ 58 + 2·log₂k̄, not 61 flat.
   - **Path independence at depth:** f=1/8 for 120 rounds → 66.26 @ k̄=15 vs 66.25 via f=1: the law depends on k̄, not the path (confirms the author's held-out point at 5× depth).
   - **Scale:** m=2²⁰ matches m=2¹⁷ within 0.03 bits at every k̄.
   - **Quantum lever:** kicks widened ×2⁶ → 84.35 bits/scarred @ k̄=1 vs Σlog₂(δ/q)+10 = 84.1: the rescaling law the "cost of adoption" section rides on is real.
4. **Novelty.** HANDOFF (6 Oct) line 70: H_live "not measured yet". `measure.rs` (shipped) does 2 update rounds on a shelf, no program-form trajectory, no saturation question; gold `components-98bc` measured the *static* program floor (0.126 bits/body). This measures the dynamic stock under iterated kicks with controls. No HISTORY entry covers it.
5. **Goal fit.** Closes board risk #2 for the belt arm of B18; "The memory floor is information-theoretic" — measured 61 sits ~20% over the 50-bit residual entropy of one kick (17+11+11+11), and no re-sorting recovers it (re-family also fails under heavy kicks: sorted-by-t shelf 70.7 vs 55.2 unsorted). "Nothing is evolved that can be derived when looked at": the 61 bits are precisely what cannot. Arithmetic checks: 4 GiB/61 bits = 5.6×10⁸; 10⁹ × 61 bits = 7.6 GB = 1.77× budget; k̄=3 at 0.3 kicks/orbit = 10 orbits ≈ the author's game-time anchor.

## The one experiment for gold

Run the author's own instrument at f=1 to k̄=24 (10 s), restate the law as per-scarred ≈ 58 + 2·log₂(k̄) bits (fraction × width phases), and re-derive the budget verdict at the design's play horizon (e.g. k̄=30 → ~68 bits → 8.5 GB per 10⁹). If the walk holds to k̄≥100, gold as a corrected law; if it bends, say where and why.

## What the author missed

- The headline mechanism is wrong in two ways: `Pop::Convoy.kick` **adds** deltas (a random walk), it does not overwrite; scars overwrite only the *stored total*, and the block width rides the walked residual max — which is exactly why +2 bits/doubling returns once every body is scarred. Stopping at k̄=3 read the fraction phase as the asymptote.
- "Averaged out by block-width quantisation" is the wrong explanation for the flat 60–62 window: it is the fraction phase, not quantisation absorbing width.
- The lens section flags heavy tails and the player-wildcard but does not test either; the ×2⁶ probe is one line in the author's own instrument and confirms the lever — it should have been in the dossier rather than in "what would make it wrong".
- The flow verdict (~4 µs/kick → noise for the allocator) is measured only at m=2¹⁷; seal/compact grow with scars, but even ×8 at 10⁹ stays percent-level — worth one line at scale.
