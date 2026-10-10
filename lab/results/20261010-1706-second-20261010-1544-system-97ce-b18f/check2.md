Grade: gold

**Abstract (for the integrator).** The re-anchor wired on the belt path (config-gated, integer threshold 48/2¹⁶ = √(floor/C)) hits its compute targets but refutes adoption as a memo, at the law's own threshold. Everything reproduces bit-for-bit: compiles 3,204 = 0.01598/kick (target 0.05), wall 9.29→5.18 s = 1.80×, determinism bit-identical; behaviour moves on every held-out Jupiter seed (|Δa|/a med 1.5×10⁻³, max 4.6×10⁻², seed 6 alive-diff 1 with one readout off the integer word; the existing lifecycle pin fails at 48 — verified). Error ∝ threshold while compiles ∝ 1/threshold (re-verified on fresh seeds), so no threshold reaches the 10⁻⁶ floor below one compile per kick: the derivative-less offset-carry is a law change, not a memo. Adopt in one step: keep the lever off, record the refutation, redirect to the jet's stored derivatives and H0190's averaging.

## Reproduction (clean tree, `git apply work/patch.diff`, from `crates/`)

Every command in the dossier's Evidence re-run; all counters bit-for-bit, walls within shared-box noise:

- `belt_reference` (16 s): REFERENCE 2⁷ events 406,220 (kicks 203,017, opens 385, boundaries 202,818), rekeys 203,017 = 1.0000/kick, 22.9 µs/event — the dossier's record exactly. ANCHORED 2⁷: compiles 3,204 = 0.01598/kick, re-anchors 197,340, wall 9.29→5.18 s = 1.795×, 12.9 µs/event. 2⁴: 2,859 compiles = 0.1093/kick; fired |dv| mean 7.68×10¹³ = 8× the 2⁷ row's 9.60×10¹². All match.
- `behaviour_vs_reference_many_seeds` (122 s): Jupiter seeds 2–6 compiles/kick 0.01498–0.02073; |Δa|/a med 1.51–1.65×10⁻³, max 8.08×10⁻³–4.63×10⁻²; |Δx|/r med 3.7–4.6×10⁻², max 0.51–0.99; seed 6 alive-diff 1 and max = inf (one readout outside the word). Saturn 2⁻¹² seeds 2–4: compiles/kick 0.0000, |Δa|/a med 5.6–5.8×10⁻⁵, |Δx|/r med ~9×10⁻⁴. Determinism seed 7 twice: kicks 204,495, readouts bit-identical. All match the dossier.
- `control_coorbital` (0.3 s): 11 compiles of 408 kicks (97% deferred), |Δx|/r med 8.97×10⁻⁴ max 9.88×10⁻⁴, alive-diff 0. Matches.
- `threshold_tightening` (17 s): num 1 → compiles/kick 0.520, |Δa|/a med 2.110×10⁻⁵ max 1.03×10⁻⁴. Matches.
- `belt_offset_headroom` (6 s): max |carried| 5.994×10¹⁴ vs smallest threshold 3.093×10¹⁴. Matches.
- Full suite, default off: 0 failed (62 passed here = the 54 pre-existing + the author's 5 hlive + my 3 throwaway probes). The dossier's "54 passed, 0 failed" is the pre-existing count; with hlive it is 59 — green either way.
- **The gate claim verified by edit**: `the_origin_takes_the_dolls_kicks_like_a_ship` with `reanchor_num: 48` fails (5% push-parity broken), passes at default 0. The refutation is indeed seen by an existing pin, not only by the new instrument.

## Held-out predictions

`predictions.md` mtime precedes the run outputs (`work/hlive-all.out`, `patch.diff`) by ~18 min; its tuned-seed record is the first run's seed, correctly declared not held out. Held: compiles/kick band 0.010–0.030 (all Jupiter seeds), wall 1.7–1.9×, element ordering, determinism, the 2⁴ cadence row. Failed honestly and reported: Saturn compiles 0.0000 vs band 0.002–0.020; |Δx|/r max ~1 vs ≤10⁻² (the author's in-file first-order analysis was right and their stated band wrong — disclosed); alive-diff 1 vs 0. The pre-registered kill line (|Δa|/a max ≥ 10⁻³ or any alive-diff ⇒ law change, 5 October precedent) tripped on every Jupiter seed, exactly as written. The kill criterion is falsifiable, not a control: at num 1 the median passes it (2.1×10⁻⁵).

## Attack (my three adversarial cases, fresh seeds, throwaway test file, removed after)

- **A, 4× the tide (Jupiter 2⁻⁸, seed 11)**: compiles/kick 0.066 — **above the 0.05 target** (same seed at 2⁻¹⁰: 0.0154), while |Δa|/a med stays 1.43×10⁻³ (baseline 1.40×10⁻³). The compute side of "targets hold" is field-strength dependent, which the dossier does not disclose (it discloses only cadence dependence). Direction: strengthens the kill — in stronger fields the memo buys even less; and error set by the threshold, not the tide, confirms the mechanism.
- **B, double horizon (4 planet periods ≈ 48 game-years, seed 2)**: compiles/kick stable 0.016; |Δa|/a med 2.15×10⁻³ (1.4× for 2× time) but **max 9.9×10⁻², 12× the 24-year max**; |Δx|/r med 0.127; alive-diff 0. Median drift is near-linear, the tail superlinear: the refutation deepens with time; nothing rescues adoption at longer horizons.
- **C, threshold scaling on a fresh seed 13**: num 48/6/1 → compiles/kick 0.0151/0.1266/0.5155, |Δa|/a med 1.46×10⁻³/2.83×10⁻⁴/1.99×10⁻⁵. Error ∝ threshold and compiles ∝ 1/threshold hold on held-out seeds; reaching the 10⁻⁶ floor needs ~10³× tighter, i.e. compile every kick. The dossier's scaling falsifier replicates off its chosen seed.

Mechanism verified in code, not just inferred: `readout` (crates/universe/src/bind.rs:138) is the compiled tube plus a **constant** residual — the carried velocity offset is never integrated into position — so between anchors position error is first order in elapsed time. The scaling (C) is that mechanism's signature. law.md's error = C·drift² belongs to the jet *with stored derivatives*; this residual has none.

## Novelty

docs/HISTORY.md and the docs hold no prior measurement of this. law.md:35 specifies re-anchoring **for the jet (exact offset plus stored derivatives)**, cost ~0.05 compiles/kick, error C·drift² (red-team 20261006-0346). The 5 October kill (quantized (E,L) memo, "re-rounds every kick") is a different mechanism (random walk, not first-order drift). H0207's "re-anchoring" is the battle frame's anchor policy, a different object. This run is the first to wire the re-anchor on the engine's belt kick path and measure that the derivative-less variant is a law change — measured on the design's own cheap path, which is exactly what the 29 September red-team lesson demands. It builds on (and cites) the first run 20261010-1544, whose record it reproduces bit-for-bit.

## Goal fit

Board line 1: kicks dominate, and each fired kick recompiles. The run prices the designed fix as wireable today (0.016 compiles/kick, 1.8× wall — the compute premise of law.md:35 confirmed) and kills its adoption at the law's own threshold on behaviour grounds, redirecting the lever to the jet's stored derivatives and H0190's averaging (Saturn row: even zero-compile carry drifts 5.8×10⁻⁵). PRINCIPLES: 9 — "a failed experiment kills that configuration, never the method" (the jet with derivatives is untouched and priced next); 13 — "we don't want errors that can compound"; 19 — "a fix signals the wrong representation": the residual without derivative terms is the wrong water for this fish. The kill is a premise correction the integrator can adopt in one step (keep `reanchor_num: 0`, record the refutation in law.md), in the shape of the components-4643 gold precedent (a measured kill, nothing to build).

## What the author missed

- The compute target's field-strength dependence (my A: 0.066 > 0.05 at 2⁻⁸): "compiles track accumulated drift" is true not only across cadence but across tide strength; the 0.05 figure is a weak-field number.
- The tail's superlinear growth at longer horizons (my B: max 12× at 2× time) — "first-order" describes the median; the tail is worse, which matters for principle 13.
- `belt_offset_headroom`'s "headroom 0.516×" compares one ship's max |carried| against the smallest threshold across all ships (different bodies); the printed ratio is not per-ship. The conclusion (ships cross; ~63-kick windows) is still right, confirmed by 197,340 re-anchors.
- "54 passed, 0 failed" is the pre-existing count; the patched tree runs 59 (its own 5 hlive tests pass too).
- Disclosed by the author: one belt shape, two perturbers, 24 game-years; B12/B13 scenes unrun; the resonant/encounter regimes touched only by the co-orbital control.

None of these touch the claim, the numbers, or the kill; the next run the refutation points at is the jet's stored derivatives on the same belt path.
