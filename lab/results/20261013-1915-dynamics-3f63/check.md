Grade: silver

**Abstract.** Claim: the held-brake crash boundary on circular starts is the tangent family Λ\* = κ(r)·R/√(r²−R²) — κ = 2.85 ± 0.07 within 13% of the surface, drifting as κ ≈ 2.72 + 1.71·(r/R − 1); Λ spans ×8.2 across the same sweep and is dead as the ruler. Reproduced bit-identically (runner's regen plus my own flights on the applied patch). My 8 adversarial arms all confirm: L7 (a level never swept) brackets its boundary inside (1.002, 1.004)R with (1.004R, L7) ALIVE where constant-κ said DEAD; mid-gap (2.6R, L0) DEAD where plateau-only κ said LIVE — the drift is real; 2³⁷ horizon keeps both borderline ALIVE arms alive. Gain: the HUD's one-line brake-margin certificate (open direction 1's number); cost: one HUD line, no engine change. Not gold: no 10× board move (author concedes), and the ruler is untested on the plane's own world.

## Reasons

**Reproduction.** regen.sh (runner, exit 0) matches every dossier number: the seven r\* brackets, the κ table (5.90/4.61/3.74/3.16/2.89/2.76/2.91), plateau 2.852 ± 0.071, slope median +0.77, margin fit 2.72 + 1.71·(r/R−1) rms 0.081, Λ span 2.23 → 18.20 (×8.2), held-out verdicts, the three 8574 cross-checks, and the Λ(1.099R, L5) = 10.70–10.71 check against the page's twice-corrected ladder (grounded in shipped `thrust.rs`: burn = 2^level × base, α = 2^(thrust_log2+level)). I applied work/patch.diff myself on the clean tree at 4503420: the pilot and the (2.30R, L0) arm reproduce bit-identically across three invocations (determinism holds beyond the author's one repeat).

**Predictions.** predictions.md predates the decisive runs (file order consistent; and its central κ = 3.5 was then falsified — a post-hoc fabrication would not fail). P1 held exactly (anchors: crash L0–L4, alive L5–L15, matching the page's D-row bracket). P2: central r\* within 0.1–5.5% at L2–L5, 18% off at L0 (the drift). The registered kill criterion (|d ln κ/d ln r| > 0.2) fired at +0.77 and the author reports the constant-κ tangent dead, keeping the tangent *form* with measured drift — an honest reframing, and my arms below show the drifting curve has real content.

**Attack (my arms, all on the same tree, all matching the fitted curve).**
1. **Level extrapolation, outside the swept grid** (L7 never swept; radii below the L6 boundary): (1.004R, L7) ALIVE as the fit predicts (Λ/Λ\* = 1.17; plateau 1.12; constant-κ 0.91 — falsified again), (1.002R, L7) DEAD (0.83). The L7 boundary lies inside (1.002, 1.004)R: the near-surface plateau extrapolates to a new level at 0.2% r-resolution.
2. **Mid-gap radius the sweep jumped over** (L0 bisect flew 2.36 → 3.03): (2.6R, L0) DEAD as the drift-fit says (0.82) while plateau-only κ (1.58) and constant-κ (1.28) both say LIVE — the drift is a measurement, not noise. (3.2R, L0) ALIVE (1.33).
3. **Fresh radius column** at 1.45R: L2 DEAD / L3 LIVE, both as predicted.
4. **Horizon 2³⁷** (4× the page's horizon, 676,954 game-s): (1.70R, L2) and (1.099R, L5) stay ALIVE with unchanged anatomy — the dossier's admitted late-crash risk is closed for the borderline arms.
5. **Coast control** clean at all five new radii (1.002–3.2R).

**Novelty.** The page's open direction 2 named the r-only sweep as the missing flight and carried no dimensionless ruler; docs/HISTORY.md has no prior tangent/κ crash-basin claim (its κ hits are the hybrid's kinetic prior). The Λ-kill across r was the page's inference from raised-apo brackets; this run measures it (×8.2) on circular starts and adds the curve. Not a repetition.

**The page.** Faithful: every new line traces to the log or analysis.py, and the residues (v₀ degeneracy, sub-1% cleanliness, 2³⁷ horizon, minimal-world vs plane) are carried into open direction 2. No correction needed.

**Goal fit.** "Regimes are chosen by dimensionless numbers" (P4) — the number and its domain are now named and measured; every arm is an exact integer settle (P2). It closes a named hole on a 16-run page and supplies open direction 1's HUD number. It moves no board bottleneck by 10× — the author says so himself — and the Λ premise was already refuted by the page, so this is a tightening, not a premise kill.

**Why silver, not gold.** (a) No 10×/deletion/premise-kill leg on a board bottleneck. (b) The ruler's domain has two untested legs the author names but cannot claim: circular starts make Ψ = 1/Λ identically, so the sweep cannot say *what* the thrust races; and the minimal world is validated against the plane only through the D-row bracket. (c) The held-out set's discriminating power rested on one arm ((2.50R, L0)); the other three agreed with the already-dead constant-κ too. My arms repair (c) but not (a) or (b).

**The one experiment for gold:** the plane-world transfer — re-fly a handful of boundary arms on the plane's own scene (moon, fleet, Home's real orbit): the L0 boundary near 2.83R, L2 near 1.62R, the 1.099R anchors. If the κ curve holds there, the certificate is adoptable as the HUD number in one step.

**What the author missed.**
- Only 1 of the 4 held-out arms discriminated the fitted curve from constant-κ; "the drifting curve gets 4/4" is true but oversells the registered evidence.
- The sweep ran L6 beyond the pre-registered levels 0–5, undisclosed — and L6 is the noisiest point (12% bracket) and one of the three plateau members.
- L1's central miss (8.9%) is unreported; the dossier gives 0.1–5.5% for L2–L5 and 18% at L0 only.
- My (1.002R, L7) death anatomy is unread: r_last = 1.0058R ≥ surface with a garbage min_r, death before the first checkpoint — classification unambiguous, but the "die in-doll with r_at_death < 1" reading does not hold at checkpoint granularity near the surface at L7.
- min_r is sampled at 2²⁶-tick checkpoints, so graze depths are upper bounds; the page's "reproduce the D row exactly" is the crash/live bracket (correctly scoped in the dossier), while this world's L5 graze reads 1.1273R against the page's 1.014R specimen — different start phase, same side of the boundary; worth a line on the page if adopted.
