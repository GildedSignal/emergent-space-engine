Grade: silver

**Abstract.** Both census arms do certify at 16/planet-period — but this run's own arms never flew them. `OrbitSpec.periapsis` is consumed as the semi-latus rectum (`OrbitKey::bound`: k = 1/(1+e), stored peri = p/(1+e)), so every e≠0 draw at `periapsis = a(1−e)` lands at actual a = a/(1+e): the "zone31" bodies orbited 2.2–2.45 AU (no 3:1), the "bridge" arm sat at 6.3–7.5 Hill (already certified), the "5:2" arm accidentally flew the true 3:1. Checker re-placement: actual 3:1 scan 1.3–2.2e-5 at step 4 **with real capture** (|mean e^{iφ}| = 0.905, Δe pump 0.072/100p, step-independent), interior bridge 5.9–6.4 Hill 1.2–1.5e-5, step-3 cliff 14/25 fail. The ≈550× headroom stands; "no island anywhere" is refuted, and with it the birth-frozen-safety argument. Adoption waits one rerun.

## Reasons

**Reproduction.** Every number regenerates (regen.log; my re-run of `4 100 6 zone31` bit-identical: kicks 19726, values equal). Controls on both sides hold (belte PASS, strong deaths, step-3 cliff 5/6 both arms). `predictions.md` predates the decisive runs (mtime order consistent). The instrument is cbe6's verbatim (diffed against cbe6's patch: same scene, rng, Jacobi closure, sampling, scaling).

**The premise break (checker's finding).** `universe.rs:345` passes `spec.periapsis` to `OrbitKey::bound` as `p`, whose contract (orbit.rs:109, and its math: apoapsis = p/(2k−1)) makes `p` the semi-latus rectum: the stored periapsis radius is p/(1+e). `OrbitSpec`'s doc says "periapsis radius". Verified three independent ways:
- osculating fit of the engine's own t=0 state: a_osc = 2.2804 AU vs nominal 2.5289; = p/(1−e²) to 5 digits; ϖ fixed, elements two-body-clean (probe on the engine, not a paper check);
- the φ-winding fingerprint: measured windings match 3 − (a_p/a_actual)^1.5 exactly (−0.442 vs −0.4445; ship 2 −1.043 vs −1.044) across 8 ships, 2 seeds, all steps — this is the "≈ −4.6·e offset" the dossier's own numbers carry but never explain;
- apoapsis identity apo_actual = a_nominal.

So: the "3:1 zone" arms drew actual a ∈ [2.06, 2.45] AU (the e=0.20 "whole-zone scan" actually covered 2.06–2.13 AU, and its "ridge at frac −0.2" sits at actual 2.080 AU = the 4:1 + 0.7%); the "bridge" arm's actual apoapsis gaps were 6.3–7.5 Hill — inside cbe6's certified circles; the "5:2" arms (nominal 2.75–2.92) actually covered 2.39–2.66 AU, crossing the true 3:1.

**What is refuted.** "No island anywhere": at true placement (ARESC = 1+e compensation), the e=0.20 scan shows |mean e^{iφ}| = 0.905 at exact resonance with stalled winding (+0.1 turns vs ±45 outside), island half-width ≈ 0.3 of the pendulum width — not "≫10× narrower". Belt-e-law draws capture within 100 periods (seed 2: |mean e^{iφ}| = 0.529, winding +0.1, Δe 7.2e-2/100p). "Zero deaths, refusals, captures" is true only of the displaced population. The re-derive-trigger reasoning ("a birth-frozen certificate is safe") loses its support: a captured body pumps Δe ≈ 0.07 per 100 planet periods, a real route into the e-domain on horizons a few× the flyable one.

**What survives, and is even strengthened.** The B12 certificate at 16 holds at the true placements with capture present: actual 3:1 scan step 4 worst 2.2e-5 (25/25 PASS), step-6/4 Δe pump identical to 2 digits (4.9e-2), step-3 cliff 14/25 fail; actual interior bridge 5.9–6.4 Hill at step 4: 1.2–1.5e-5; the composition arithmetic (115 → 16.2, headroom ≈ 550×) checks against ddeb's own formula and fractions, and the certificate premise is now actually flown — by the checker, one seed, one horizon. The engine-side Δe step-independence claim ("real dynamics, not aliasing") is confirmed at a real resonance.

**Scope notes (minor).** The e-domain fraction 1.1% exceeds the Rayleigh(0.07) tail P(e>0.23) ≈ 0.45% — conservative for the headroom (693× at 0.45%). P1's "held" overstates: the predicted step-5 worst ≈ 1.8e-5 did not occur (a death intervened; survivors 5.8e-6) — disclosed, but the ledger should say the letter failed. The engine's `ladder_ship` belt birth passes the same `a(1−e)`, so the shipped belt actually spans [1.43, 3) AU in semimajor axis (mean −8%) — ddeb's census membership is nominal-space, cbe6's checker2 e-draw inherits the same placement; all mutually consistent, all displaced from their labels.

## The one experiment for gold

Re-fly both arms placed at actual elements — `periapsis = a(1−e²)` (or ARESC = 1+e per fixed-e arm) — two seeds, 400 periods, bridge apoapsis at actual 4.1–6.3 Hill, 4:1 and 7:3 included; fold in the capture Δe-pump rate as the zones' re-derive trigger. One `beltzone` edit, ~5 min of runs; my probes predict it passes and the ≈550× sentence then stands on the author's own instrument.

## What the author missed

The `OrbitSpec.periapsis` semantics (doc says periapsis radius, `bound` takes the latus rectum) — it displaces every e≠0 body this run, cbe6's e-draw arm, ddeb's census membership and the shipped plane's belt birth itself; it is the run's real discovery, made by none of its instruments. Second, the author's own φ data carried the signature (winding ≈ 3 − (a_p/a)^1.5 only under the displaced a) — a one-line cross-check of winding against the drawn a would have caught it. Third: the capture/pump at the true 3:1 kills the "birth label" story the dossier leads with; the certificate claim never needed it.
