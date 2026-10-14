Grade: silver

**Abstract.** Claim: a quantum gate (each candidate pair's strongest conjunction charged against one Q48 of E, `crates/space` `Key`) deletes 99.96% of exact-tier pair work on an asteroid-like 10⁹ belt, composing the 1.65–8.2×10³-core contiguous-averaged wall to 0.5–3.1 cores. Reproduced bit-for-bit; controls (all-50-m → 1.000000, all-10-km → 0.118) and the phase-vacuity result (1/K → 0) confirmed. Headline refuted: the conjunction model (miss uniform over v_rel·P_syn/2, min of N_c uniforms) overestimates the miss by 6×10²–9×10³× at Δa ∈ [0.005, 0.05] — my Kepler integration (random ω, 10³-orbit horizon) shows quasi-periodic misses revisiting near-zero. Corrected: deletable 0.955–0.978, survivors 2.2–4.5×10⁻², ledger 37–369 cores; budget 4 fails; ×52 mass → 0.64. Mechanism, vacuity and anchors stand.

## Reasons

**Reproduction (clean).** `regen.sh` exit 0; my rerun is identical to `gate-out.txt` on every line (seeded). `work/patch.diff` empty; no files outside the run folder touched. Provenance: `predictions.md` (12:28) predates `gate.py`'s final save (12:35) and the decisive output; all four predictions are registered and resolved in the dossier.

**Anchors verified.** `crates/space/src/lib.rs:171–178`: `Key { energy: Words }`, "E in Q48", `ENERGY_FRACTION_BITS = 48`; `events/handoff.rs:125`: a `Carry` accumulates sub-quantum increments — the gate's premise exists in shipped code. c7eb (0/1000, median 0.998/1091), 62f7 (0.87–1.04), 90fb (pairs/kick law), 1738 (1.65×10³–8.2×10³ contiguous-averaged) all match the published wiki. Note 1738 is itself awaiting grade — the composition is conditional on it.

**Attack 1 (outside the author's tested range): the conjunction model vs real Kepler orbits.** The author validated the *impulse formula* against RK4 but never the *miss-distance model*. Direct integration (two eccentric crossing orbits, random ω and phases, e = 0.05, H = 1000 orbits, 4×10⁶ samples, min |r₁−r₂|; 8 seeds per Δa):

| Δa | P_syn | true min-miss (med) | model b_min (med) | model / true |
|---|---|---|---|---|
| 0.005 | 843 | 1.0×10⁻³ | 9.5 | **9 300×** |
| 0.010 | 424 | 5.8×10⁻³ | 2.3 | **400×** |
| 0.020 | 215 | 2.7×10⁻⁴ | 0.62 | **2 300×** |
| 0.050 | 89 | 2.3×10⁻⁴ | 0.14 | **620×** |
| 0.100 | 47 | 3.0×10⁻² | 0.05 | 1.7× |

The true misses are quasi-periodic and revisit near-zero — exactly the r8-v2 lead's own structure ("a pair's miss distance at successive conjunctions is quasi-periodic"), which the uniform-in-synodic-tube model discards. The author named this risk but scoped it to "the resonant minority"; it is the generic Δa ≲ 0.05 majority of the candidate set. Sampled mins are upper bounds (time smear 1.6×10⁻³), so if anything the error is understated.

**Attack 1's consequence (corrected decisive run).** Re-running the author's decisive spectra with the measured miss distribution (b_min drawn from the pooled empirical true/Δa factors): deletable **0.967 / 0.955 / 0.978** (was 0.99962 / 0.99968 / 0.99990); surviving 2.2–4.5×10⁻² (was 3.8×10⁻⁴); ledger **37–369 cores** against budget 4. Even the most conservative correction (every pair at the pooled p90 factor, 0.93·Δa — still 5× below the model's median miss) pushes survivors to ~10⁻²–10⁻³ and the top anchor over budget: the budget conclusion fails under any Kepler-honest miss model. The all-10-km negative control flips to 0.000 (prediction 3 still "holds", but both mass controls shared the model's blind component — controls that share the model validate nothing, the page's own H0183 lesson).

**Attack 2 (the author's flagged risk, real-belt mass ×52):** deletable 0.64. **Attack 3 (finer quantum Q52):** 0.78 — and the "survivors as the square" heuristic understates. **Attack 4 (cold belt σ_e = 0.01):** 0.82.

**Second, unflagged gap: the gate's own amortized cost.** The ledger multiplies the wall by the surviving fraction, implicitly pricing the per-refresh gate comparison at zero. At "one comparison per candidate pair at certificate refresh" (the dossier's own wording), the deleted pairs still pay r × full-pair work; with the author's own 786 evals/encounter the top anchor alone adds ~10 cores. Either r must be measured (against f79a's ~4 µs/pair), or the dossier must argue the check runs only on key changes (the `Carry` route) — neither is done.

**Novelty.** First yield measurement of a quantum gate on the belt; the group-certificate vacuity (phase-free form) is new and stands (it is independent of the conjunction model). The refuted miss model is the r8-v2 lead's quasi-periodicity re-entering — a repetition neither in evidence nor credited. Not a repeat of c7eb (contact/tick anchor, not pair-work yield).

**Goal fit.** Board live question 2 ("what never needs a pair test at all"). PRINCIPLES #6 verbatim "influences below one quantum accumulate" — the gate is a fair reading, and the shipped `Carry` makes it adoptable. The corrected ceiling (37–369 cores) is itself decision-grade: the gate alone does not fit the budget; the flux/observation split (62f7) or islands topology stays required — which is what prediction 4 originally said before the run "missed in the lever's favor".

## The one experiment that would make it gold

Re-derive the decisive yield with Kepler-true miss distributions: measure min-miss vs (Δa, e, ω) by integration (my table is the skeleton), sample candidate pairs from that, and re-state the ledger **including the gate's own per-refresh cost r** (measured against the cascade's per-pair work on shipped code). If the corrected deletable clears ~99.8% the original claim returns; on my numbers it will not, and the honest result — gate ceiling ~20–45×, budget met only with the flux split — is the gold.

## What the author missed

1. The miss model was never tested against real orbits; the record's own r8-v2 lead contradicts it (quasi-periodic misses), and the risk was mis-scoped as a resonant minority.
2. The ledger's r-term: "cheaper than what it replaces" is asserted, never priced; the composition sets it to zero.
3. Belt mass "falls out" at 2.3×10⁻¹¹ M☉ via sample-mean × 10⁹, but the D^−3.5 mass integral diverges as √D_max: a true 10⁹ draw of the same construction reaches ~280 km and ~1.4×10⁻¹⁰ M☉ (the "~50× lighter than the real belt" note understates the gap and the sample under-represents the top). `predictions.md`'s "belt mass ~10⁻³ of the star" is 9 orders off the construction actually run.
4. The proposed page's Contradictions paragraph ends mid-sentence ("its own two m…"); completed in my correction.
5. Timing note: regen and my reruns stay ≤ ~105 s and well under the memory cap.
