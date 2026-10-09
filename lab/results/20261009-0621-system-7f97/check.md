Grade: silver

**Abstract.** Claim: the integer plane's kick-cadence frontier is regime-split — B17 (resonant bulk) passes at 16 kicks/period, B13 (deep passages) needs ≥128 and collapses below 64 — yet one doll-wide Δs tied to the fastest secondary (a tick, principle 14) pays the passage price everywhere; cutting the bulk 8× removes ~5× of kick events at flat per-kick price while distinctions stay cadence-independent. I reproduced every deterministic number exactly (B13 60/64→3/64 across S=7→4, B17 PASS@4/FAIL@3, digests, 630/126 kick samples, 611/108 rebinds, 45/45 memo shapes). My adversarial S=9/10 run closes the author's named open hole in their favor: B13 degrades (58/64, 53/64) — not cadence-limited. Gain: ~5× fewer kicks for the queued q-cadence build. Not gold: no build; the per-body Δs rule is unimplemented.

## Reproduction (clean tree, patch applied, offline build 38 s)

| Command | Author | Mine |
|---|---|---|
| B13 S=7 | 60/64, worst 2.12e-2 | identical |
| B13 S=4 | 3/64, worst 1.34e0 | identical |
| B17 S=4 | PASS pump [.9905, 1.0028], lib 0.981 | identical |
| B17 S=3 | FAIL pump [.9517, 1.3064], lib 0.023 | identical |
| bench no env | digest 21c73edc…, 170.1 ev/s | identical (default-path bit-identity holds with the patch) |
| bench LOG2=4 | 7d13a00c…, 80.9 ev/s | identical |
| kick-bench S=7/S=4 | 630/126 samples, 611/108 rebinds, 45/45 shapes, hit 0.9263/0.5833 | identical (µs medians drift with load, as expected) |

The same 9 replaced oracle-domain draws appear in every B13 run — columns compare like for like, confirmed.

## Held-out check

predictions.md (06:28) predates the dossier (06:41) and the saved data (06:42–43); run start 06:21. P1 was falsified (3/64 at S=4) and reported as falsified, first line of the Predictions section — honest. The disclosed no-op (`UNIVERSE_STEP_OUTER`) verified: PLANE_TRACE outputs byte-identical (times stripped) with and without it on B13 S=7; and `on_clock` (step.rs:535) confirms gate ships are clock bodies, so the patch cannot reach them. Correctly discarded as evidence.

## Attack (my three cases)

1. **B13 at S=9 and S=10** (the author's named open hole): 58/64 and 53/64, worst ΔE rising to 7.53 and 1.62e1. Saturation confirmed — B13's residual failure is not cadence-limited — and strengthened: past S=8 more kicks make B13 *worse*, so the passage regime has no passing cadence at all. This reframes the split's passage half: the payoff is bounded by the bulk's ~5×, and passages belong to the encounter/changeover representation (H0214), not to a finer Δs.
2. **`UNIVERSE_STEP_OUTER=4` on the bench**: digest changes (821e8cd5 ≠ 21c73edc) while events/s stays 170.1 — the no-op is gate-scoped, not bench-scoped; the bench scene does carry root-doll `plan_interval` bodies. Consistent with the dossier's narrower claim, worth stating exactly.
3. **B17's catastrophic mode at S=3** (libration crushed to 0.023, pump 1.31): reproduced; the regime break, not a walk.

## Novelty

H0214 (pre-v2) had the plane failing B13/B17 "at every cadence"; H0215 (v2) records B13 marginal-fail and B17 pass, no step sweep. The q-cadence lens holds float-replica numbers only (4–16/orbit, disagreeing runs). The post-v2 integer-law frontier, the 8× regime split, the doll-wide-Δs "tick" reading (verified in `ext.rs`: Δs = 2^−k·P_D/f'(c), P_D the doll's *shortest* secondary), and the 91%-cadence-driven cost split are new. The B17-passes-at-4–6 half is confirmatory of documented knowledge, which the author discloses.

## Goal fit

Board focus 1 verbatim: "fewer kicks per orbit at the same behaviour: kicks dominate the engine's cost." The dossier hands the queued q-cadence build its integer-law numbers and the knob's true location. Principle quotes check out (#14 tick, #4 dimensionless regimes, #33, #1). It also correctly separates work (events, compiles, re-setup) from distinctions (sigma-delta carry, 45 shapes) — the negative P4 is the run's most useful guard against over-claiming.

## Why silver, and the one experiment

No adoptable code: the per-body Δs rule (coupling U_P/c, re-derived on approach) is proposed, not built or validated, and its gold validation needs B12, currently being rebuilt (H0215). Gold experiment, as the author names it: implement the clock-path regime split and validate B12+B13+B17 together plus a belt-scene cost run — folding in my S=9/10 result so the split claims only the bulk saving.

## What the author missed

- The S=9/10 degradation (above): it closes their hole and materially sharpens the claim — "deep passages need ≥128" is really "no cadence passes B13; it peaks at S=8 and degrades", i.e. per-kick error compounds at high cadence too.
- The abstract's "deep passages need ≥128" could read as "128 suffices"; the table shows 60/64 (FAIL). The dossier body states this honestly; the one-liner should not.
- The pre-registered decision rule said a P1 failure at S=4 "collapses the question back into q-cadence's surface"; the dossier instead keeps the regime-split reading. The falsification is disclosed, but the pivot off the pre-registered rule is not named as a pivot.
- The inline "median 88 vs 71 µs" does not match the run's own saved cost.txt (90.24 vs 73.28); quote the saved data.
- P3's "total events fall by the same factor" was corrected in-flight (boundary/open floor ~70/s) — the correction is in the dossier, but it means the events/s headline (170→81, 2.1×) and the kicks headline (5×) must not be conflated when adopting.
