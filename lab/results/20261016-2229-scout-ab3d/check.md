Grade: silver

**Abstract.** The two-stage angular certificate (mean-longitude window with exact per-body anomaly margins, then an equation-of-center series) is real, sound in its domain, and refutes 3999's "no pre-read cut on the tight axis": 26/26 scene rows reproduce bit-exact, series 48.7–49.4 ns, Newton 270 ns. But the run's "shipped radii" are wrong by 2¹⁸: the belt branch ships `Scalar::raw(34, -10)` = 49-m ships (near = 6.71×10⁻⁷ AU), not 12,850 km. Checker rerun at the true point: 0–1 truth hits per 10⁵ scan (3999's ZERO is then exact, not "the log"), 0 misses in 27 all-seed scenes, S(10⁵) = 1.79 ms < 6 ms bar; 10⁶ marginal (~6.4 ms with λ-index + 0.5-µs readout). The "0.53%·N truth wall" describes a counterfactual Earth-sized belt. Unsounded as coded for querents e > 0.4 (crafted hit missed). Adoption: one additive filter; ~230× at 10⁵.

## Reproduction

`rustc -O falsifier.rs -o falsifier && ./falsifier` (clean tree, empty patch): 13.7 s, 32 rows. All 26 scene rows identical to `run.jsonl` in every cell (keep fractions, truth hits, miss = 0). Timing cells only: c1 4.03 ns (stored 3.20), series 48.71 (49.05), Newton 269.5 (269.8) — the dossier's 2.8–2.9 ns stage-1 band excludes the regen's own 3.20; same order. `predictions.md` (22:37) predates the decisive run (falsifier 22:48, run.jsonl 22:50).

## The adjudication the author deferred (goes against the replica)

`scenario.rs::ladder_ship`, belt branch (line 344): `return Ok((spec, Scalar::raw(34, -10)?))` with `doll: 0` — 34·2⁻¹⁰ root units = **49 m**. The 34·2⁸ constant (line 346) is the *local* ships' radius in Home-doll units (Home unit = 2⁻¹⁸ root): the same 49 m. So near = 2¹⁰·2·49 m = 68 root units = 6.71×10⁻⁷ AU — 2⁶⁰ ≠ 0.176 AU, and within 2× of the author's own "rock point" (3.42×10⁻⁷). The author corrected one decimal slip (12.9 km → 12,850 km) and missed a 2¹⁸ branch error; the dossier's "The replica is code-derived" is true of the genesis, false of the radius. My rerun at near = 6.71×10⁻⁷: truth 0–1 hits per 10⁵ scan, 0 at 10⁶ — 3999's ZERO encounters reconciles exactly, and their "log froze" hypothesis is unnecessary. Their nearest-candidate 2.1×10⁶–5.7×10⁷ × reach also lands (typical spacing 0.0125 AU ≈ 1.9×10⁷ × 98 m).

## Adversarial cases (mine)

1. **True operating point, every seed checked** (the author checked seed 1 only — `check = seed == 1`; the dossier's "all 22 checked scenes (3 seeds × 3 querents × 2 horizons…)" overstates: 12 scenes had truth on): 27 truth-checked scenes incl. seeds 2–3 and fresh seed 7 at 10⁶ — **0 misses**. keep1 6.4–31%, keep2_series 0.12–0.41% (long h). Composed S(10⁵) = **1.79 ms** with the shipped 4.2-µs readout — the bar claim survives at the true point, on the author's own rock-row structure.
2. **Outside the tested range, the radii axis**: at 10⁶, S = 17.9 ms (O(N) pass), and (49.4·110,164 + 500·1,878)/10⁶ ≈ **6.4 ms** with the λ-index + 0.5-µs readout — *over* the 6-ms bar on regen/checker costs; the dossier's "≈4.8 ms, under" needs its low-band 34.7 ns. 10⁶ is marginal, not met.
3. **Outside the e-domain (querent)**: crafted querent a=2.2, e=0.6 with a belt body co-located at t (guaranteed truth hit): **miss = 1**. `margin_of` clamps at the e=0.4 bin (0.816 rad) while max|ν−M| at e=0.6 is 1.2615 rad, so stage 1's window is undersized. Belt bodies cap at e=0.4 by genesis, but the *player* can fly e > 0.4 and the scan is the player's instrument. Wiring must extend the margin/tail tables (or bound the querent exactly); as coded it is unsound for that querent.
4. Formation re-clustered at the true near scale (±3×10⁻⁷): keep 1.000 (no truth hits — at the true point hits are rare by construction; the author's 500/500 control at 0.176 AU remains the positive soundness evidence).

## Novelty

New on the scan-queue page: the tight-axis pre-read cut (EoC series + per-e tail at ~49 ns) refutes 3999's "no pre-read cut exists on it", and the two-stage λ-then-series composition with measured costs is unmeasured before (cdf0 priced 10–20 ns unmeasured; 1250 built a different mechanism — the knot-panel certificate for the plane's regime; 3999 priced the sound mean-longitude form only). No HISTORY entry covers it.

## Goal fit

Board bottleneck 1 ("bodies: 28 against 10⁹ … which term breaks first as the plane grows (per-frame walks…)"): the in-belt answer walk is that term, cut 418 ms → 1.79 ms at 10⁵ (~230×). PRINCIPLES #3 "compute only surprises" (stage 2 drops 99.6–99.9% of candidates), #30 "navigation, knowledge and dynamics those need to be perfect" — the certificate drops only provably-far candidates (the `radial.rs` pattern), outcomes unchanged by construction. Caveat the author states and I repeat: this is a float Kepler replica; the shipped integer window's residual widenings must be carried or the cut eats a hit.

## The experiment that would make it gold

Re-derive every constant from the branch that ships (near = 68 root units), rerun the falsifier at that point with truth checks on every seed, extend the margin/tail tables past e = 0.4 (querent side), and re-fold the page at the corrected operating point. I ran exactly this as checker and the mechanism holds (0 misses, 1.79 ms at 10⁵); the run's own regenerable code must carry it.

## What the author missed

- The belt branch's `-10` vs the local branch's `-10+18`: the "code-derived" radius was read off the wrong branch; every "shipped radii" number in the dossier and page describes a non-shipped belt, including the headline wall ("the operating point, not the finder") and the 3999 reconciliation they flagged for me.
- The evidence section claims truth checks on scenes that ran with `check = false` (12 of 22).
- The e > 0.4 querent clamp (their own lens section names the GR-precession renewal miss but not this one).
- The "≈4.8 ms at 10⁶" composes the low-band series cost; on the regen's own costs it is 6.3–6.4 ms — over.
