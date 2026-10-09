Working...
Check complete. `check.md` written: **Grade: silver**.

**What I did:**

1. **Reproduced** — `verify_mech.py` exact (227 encounters, Δλ = Δeqc at 46.4 vs 46.6ρ, median 12.2ρ); S0 and all four S2 rows of `invert_train.py` regenerate **bit-identically** from the shipped script; S1's clean rows in `ev3.log`. The three-log contamination story (sort-seam fix) is internally consistent and disclosed, and no headline number rests on the contaminated code.

2. **Attacked** — four probes of my own:
   - **Instrument bias found (the significant one):** the S2 jam truth detector checks only θ-adjacent (+1) pairs; dense unbiased sampling shows **47.4% of sub-ρ contacts have ≥2 bodies between** — invisible to it. So S2's "θ-train catches 100%" is circular (instrument and certificate share the same shape), and "misses stay rare" is biased low — the memo-artifact class the dossier itself preaches. S0/S1 are unaffected.
   - λ-catch 33% is seed-robust (3 fresh seeds) and survives e-cap 1.5e-3 → the core S0 finding is real and not the truncation tail; circular control passes.
   - θ-order churn measured at 23.75 vs λ's 2.29 swaps/body/orbit — the author's asserted θ-rebuild cost is real.

3. **Novelty (why silver, not gold)** — the headline divergence is already on the record from **four uncited successor runs on the same gold**: the gold's own lesson 6 (same scene, same mechanism, 83% miss), d1b0's λ∝σ_e law, a937 (**gold-graded**, instrument-vs-adoption divergence measured at 244–363 rank, 9 Oct 02:08), b1c0's crowding law, 2360 (**gold-graded**, two hours before this run). And the built `train.rs` already watches λ̄ with the sound eqc-bounded window δ + φ(e_i) + φ(e_j), so the fixed-k=4 target was already superseded. Genuinely new: the k=4 λ-rank in the gold's exact scene, the pinwheel battle-debris scene (λ-order frozen, Binet 33×, the trigger's other horn), and the θ-vs-λ churn ratio — real sharpening, not a 10× move.

4. **Gold experiment named:** run the *built* sound-window train (not the dead k=4 sentence) on the phalanx/jam/pinwheel and measure ζ, watch degree, misses — that corrects what actually ships.
