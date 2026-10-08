Grade: silver

**Abstract (for the integrator).** Second blind check. All four dossier commands reproduce
bit-identically (30/9/10 s); my independent re-implementation matches every per-case number.
Rung r6 PASS stands: the doll-frame crossing solver survives γ to 2×10⁶ (0 fails, 0 wrong
roots, ~4 iters; extended: 0 fails to γ=2808 under acceleration), raw observer-frame
magnitudes silently mis-locate ~12 700 emission events at γ=2×10⁶, and one-sample-per-pixel
fails the exposure truth from ≈0.02–0.03 orbits/frame (γ≈3–4 at β_o=0.3). But the
candidate's PASS is convention-carried: under photon-count or energy readings of the same
exposure the pure phase sprite fails 0.1 at β_o=0.3 (p99 0.53/1.26) at every γ, and at
β_o=0.5 even under the author's own truth (0.131). The kills are robust; the spec line
needs one more experiment.

## Reproduction

- `gather_falsifier.py`, `r6_run.py`, `r6_check.py` and `verdict.py` all rerun from the dossier's commands; every JSON (md5) and log line is bit-identical to the stored ones. Timings as claimed. `work/patch.diff` is empty.
- Order audit: rung frozen 20:43:22 → `predictions.md` 20:43:33 → decisive `metrics.json` 20:43:45; tuned only on the pilot, exactly as declared. Held out: γ ∈ {2.24, 255} and the whole β_o = 0.05 ladder.
- My own code (bisection truth, closed-form and periodic-decomposed integrals) reproduces the author's per-case table to three decimals under their truth (instant: 0.076 / 0.728 / 1.324 / 1.005 at β_o = 0.3 for γ = 2.24 / 22.4 / 70.7 / 125; 0.098 / 0.31 at β_o = 0.05 for γ = 22.4 / 70.7; kavg worst 0.067 at γ = 70.7).
- Rung hygiene: positive control passes, negatives fail distinct frozen criteria (instant fails `bright` only, raw-obs fails `solve-fail`+`wrong-roots`), verdict PASS with no DISPUTED outcome. No trajectory identity demanded. Controls on both sides, per the r2 lessons.

## Predictions

7 of 8 held (P1, P2, P3, P4, P5, P7, P8). P6 honestly missed and correctly diagnosed: I confirm frozen = 1.0 at 0.995 orbits/frame and 0.0 at 1.99/2.03 in `r6_results.json`, and my dense ladder shows the sampling error dipping at integer ratios — the wagon wheel is a resonance, not a band. The miss sharpens the claim rather than weakening it.

## Attacks (independent code, my own)

1. **The truth convention decides the candidate's pass.** The author's exposure truth, ∫b·k dte/∫k dte, is the time-average of the retarded signal; the physical camera/detector records photon-count (∫b dte/∫k dte) or energy (∫b·k⁻³ dte/∫k⁻¹ dte, local Doppler k, DC dropped — first-order biases +1 and −2·β_o·s̄·b̄ respectively; my implementations check against that analysis). Under those two readings, kavg as implemented (pure sinc phase average, no local-k amplitude) fails the frozen `bright ≤ 0.1` at β_o = 0.3 at **every** γ (p99 0.53 photon, 1.26 energy; even at γ = 1), and the energy reading fails at β_o = 0.05 (0.139). Instant's and raw-obs's kills survive all three readings (instant ≥ 1.0 at high k everywhere). So the premise kill is robust; the pass margin (1.7×, as the dossier itself notes) exists because the author's num/den makes the local, first-order-in-β_o amplitude term cancel for any phase-correct render — not because the physics is nearly exact. The dossier discloses only the DC k⁴ cancellation ("a law that got k⁴ wrong would fail elsewhere"); the local, non-DC part is 0.3–1.3 in criterion units and is made invisible by construction.
2. **β_o = 0.5 breaks the frozen criterion even under the author's own truth.** Dense ladder (orbits/frame 0.01–3, 20 points each): kavg ≤ 0.071 at β_o ≤ 0.3 (no resonance spikes; onset of instant's failure at 0.02–0.03 orbits/frame, i.e. γ ≈ 3–4 at β_o = 0.3 — the dossier's onset claim is honest), but at β_o = 0.5 kavg reaches 0.114–0.131 for orbits/frame 0.17–0.5 > 0.1. The author's own P2 scaling law predicts it (0.067·0.5/0.3 ≈ 0.11); the frozen ladder stops one step short. Compact binaries live at β_o ~ 0.3–0.5, so this is in game scope.
3. **Acceleration** (Rindler observer, uniform proper-time frames, the dossier's own wrong-maker): clean 0 fails, 0 wrong roots to γ = 2808 at a = 2/s; at a = 4/s to γ ≈ 10⁹, 11 of 6368 solves fail (0 wrong roots) only once the record includes a flyby — outside the rung's coasting scope. The doc's Newton sentence is exonerated more strongly than the dossier claims.

## Novelty and fit

- `docs/HISTORY.md` ends at H0215 (6 October); no entry covers the view at γ, exposure truths, or the wagon wheel. The first run's folder is absent from this checkout, so "bit-identical to the first run" is unverifiable here — determinism from the shipped script is what stands. The queue's `b-high-gamma` item is the target; the attacked sentences are real (representation.md §2 lines 57–59), and the proposed fix is the doc's own line-58 vocabulary (type × log k sprite).
- Fit: a premise shown wrong (one sample per pixel as the temporal law) plus a solver exoneration and a number-form kill (raw magnitudes mis-locate roots silently — `wrong-roots` is the criterion that catches what the fluence criterion cannot). Principle 28 ("your dials are made up and hold no informations") and 34 (the rung judges the law, it does not size the view). On-goal.

## The one experiment that would make it gold

Freeze the physical exposure truth (energy ∫b·k⁻³/∫k⁻¹ or photon ∫b/∫k — the local Doppler amplitude inside the truth, k from the crossings the engine already solves), extend the ladder to β_o ∈ {0.05, 0.3, 0.5}, and give the candidate the design's full sprite: sinc phase × local-k⁴ amplitude, per the doc's own line 58. If that passes `bright ≤ 0.1` at every γ and β_o, the proposed representation.md §2 line is adoptable as written; if not, the line must be scoped to the phase part with the amplitude delegated (B16's territory).

## What the author missed

- The k-weight placement in the truth is a first-order convention, not a normalisation detail; it alone decides the candidate's pass, and the "DC beaming cancels" sentence understates it.
- The frozen tolerance breaks one β_o step beyond the ladder, predicted by the author's own P2 scaling — the ladder's upper end was chosen where the law passes.
- Under the physical readings the instant kill's onset story changes character (amplitude bias present from γ = 1, not sampling onset at γ ≈ 4); the γ-onset claim is meaningful only in the phase-normalised reading.
- The accelerating case was left as prose; it passes cleanly to γ = 2808, a free strengthening of P8 that went unmeasured.
- Record nit: `author-final.md` quotes 12 695 (checker metric set) where the dossier table says 12 702 (author set) for raw-obs wrong roots; both are in the record. The author's "independent" first check (`r6_check.py`) is algorithm-independent (contraction roots, three-way truth validation: 5.4×10⁻⁹ / 7.2×10⁻⁷ / 4.8×10⁻⁵, all reproduced) but same-session; this blind check is the actual second finder, and it confirms every outcome while adding the three findings above.
