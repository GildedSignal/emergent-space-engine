Grade: silver

**Abstract.** The usable-root census for the SEM step (solve whole-step α so K = 0), per the first checker's recipe: across 5 scenes × k ∈ {6,8} × {plain, zero, best}, usable roots (α ∈ [1/2,2]) cover 0–24% of steps against the 99% the memo's P8 line allows; two planets give 0/1600 plain and 0/9808 on the best trajectory. All six reproduction targets bit-identical (controls, noether, base/two k8 census, best base k8, flyby k6). My attacks only strengthen the kill: k=4 → 0.35, k=10 → 0.00; a 24/octave grid finds no extra or touching roots; co-rotating two planets still 0/1600. Gain: exact-constraint closure retired; B12-v2 freed for a bounded-offset certificate; adoption cost none. Silver on record defects, below.

## Reproduction (clean tree; `work/patch.diff` empty; p8.py verified byte-identical to the first run's commit `7796f5f`)

- `census.py controls` (~7 s): 147 roots, worst |K(α\*)| 3.61e-16 = 7.33× floor, 0/127 flip failures, Kepler-only negative flat (2.22e-16, 0 roots) — **bit-identical** to `controls.json`.
- `census.py noether` (~1 s): one-planet 8.68e-15, two-planet 1.24e-8 vs finite difference — **bit-identical**.
- `census base 8 plain 200` (31 s), `census two 8 plain 200`, `best base 8 2.0`, `census flyby 6 plain 300` (3 min) — all **bit-identical** to the stored JSONs, flyby including its nan=164 count.
- Every dossier table cell checked against the stored records: all match (plain 0.000–0.239; zero 0.009–0.103; best 0.000–0.041; two 0/1600 at both k, sens band 23/1600 at k=6 and 0/1600 at k=8; runaway median α 10.7–32.3; k=6 |K(64)| ~1.3e5–2.2e6; best after-root 0.0000 at base/ecc, 0.139/0.025 bursty at flyby; all records lost=0; best trajectories complete 2 periods, records = steps×8).
- Timing: `predictions.md` frozen 15:35:57, every decisive record 15:38:00+; the two disclosed crashes (two-planet shape bug, `run_best` scalar-t bug) match the runlog tracebacks; the final edit (15:48:06) precedes the flyby-k6 pair, `noether.json` and the disclosed base-k8 re-run (15:50:45). The regeneration story holds.

## Adversarial cases (mine)

1. **Step-size extremes.** base plain at k=4 → usable 0.3481; at k=10 → 0.0000. The kill holds over a 64× ds range and tightens at small steps. (0.348 at k=4 exceeds the dossier's "strongest cell" 24% — immaterial, still 65× below the kill line, but the fraction peaks between k=4 and k=6, not at ecc k=6.)
2. **Instrument attack (missed roots).** A 24/octave grid over [1/4,4] finds **zero** usable sign changes that the shipped 3/octave grid misses, and **zero** touching roots (|K| at the float floor without a crossing), on base k8 and on the strongest cell, two k8. The 0/1600 is not a grid artifact.
3. **Co-rotating two-planet control.** Second planet moved co-orbital (sep 5.2, phase 2.1, Δω/ω ~ 1e-6): rigid rotation restores the rotating symmetry and the J-exact kick form — yet usable is still **0/1600** and the residual stays first-order (1.74e-7 vs 1.20e-7 at generic Ω). The kill is more robust than claimed; the stated mechanism is not the discriminator.
4. **Null-second-planet control.** Mass 0 at 9.5 AU reproduces the base-k8 record exactly (median |K(1)| 7.6078e-12, usable 0.0425): the two-planet 1.2e-7 residual is genuinely the second body's.

## Novelty

No H entry or doc mentions SEM/KMO/P8 (H0215 leaves P8 unanswered and B12's rebuild pending; the 1058 constraint run is the view gather, unrelated). The first run (20261008-1419, silver) proposed exactly this census as the gold-making step; this run executes it: new instrument, three new scene families, the Z/best variants, the shipped Noether identity, the structural probe. Not a redo.

## Goal fit

Retires the exact-constraint closure question for the whole-step-scaling family across scenes, freeing B12-v2 to certify a bounded state-function offset (H0215's open item). PRINCIPLES #9: "A failed experiment kills that configuration, never the method" — the dossier is explicit about which solve is killed and which projections remain untested. Adoption cost: none.

## Why silver, not gold

The physics is gold-grade — every reproduction bit-identical, every attack strengthened the kill — but this lab's own rule (a headline the log contradicts costs the grade) bites:

1. **"nan audit 0 everywhere" is false.** flyby k6 has nan=164 (plain) / 165 (zero) of 2400 attempted records (~6.8%): non-finite α-families, cosh/sinh overflow at extreme α on hyperbolic ships (86 overflow warnings in the runlog; my re-run reproduces the count bit-identically). The runlog itself printed these counts before the dossier was written.
2. **A failed prediction is reported as held.** P8 ("nan fraction 0 everywhere") did not hold at flyby k6; the dossier's Predictions section says "P8 held: 0 nan". Counted as missing solutions the nan class *strengthens* the kill — but the verdict line contradicts the record.
3. Smaller slips, same class: the Z-collapse holds in **7/9** cells, not 8/9 (two k8 also inverts, 0.0000 → 0.0094; both ≪ 1%); "reproduces p8's one-planet 8.06e-12 exactly" — the regenerable number is 7.6078e-12, and 8.06e-12 is in no shipped record.

## The one step to gold

Not a physics experiment — an erratum plus one cheap classification: disclose the flyby non-finite α-families as a census class (are the overflows confined to runaway α ≥ 8, or do any sit in-band?), and correct the P4/P8 lines, the 8.06e-12 figure and the symmetry attribution (or fold in the co-rotation control, which sharpens the kill). Every line then regenerates from the folder and every prediction verdict matches the record.

## What the author missed

- The nan class is signal, not noise to audit away: overflow at extreme α is the runaway structure made visible; classified, it belongs in the census table.
- The symmetry control on their own mechanism claim: "no rotating-frame symmetry ⇒ ~1.3e-7 residual" is refuted by rigid co-rotation (residual persists, roots still 0); the operative cause of the two-planet residual is unproven.
- two k8's Z-inversion (their own P4 falsifier, undercounted).
- The usable fraction's peak over k (0.35 at base k=4) sits outside the k ∈ {6,8} sweep — harmless here, but a k-sweep is the honest boundary for "strongest cell" claims.
