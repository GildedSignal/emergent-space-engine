Grade: silver

**Abstract.** Claim: the proposed occlusion cure ("static occlusion is one interval test
per row", direction 5) is the wrong law at game velocities. Reproduced exactly and
independently (all 27 Jaccards digit-for-digit, W1 onsets to 4 decimals): the snapshot
wiring mis-times by −d/c (−2/−10/−100 s at 2/10/100R) and goes arc-disjoint once
β·d/R ≳ 2; the worldtube test prices at ~70–80 ns/row. But the headline sprite number is
an instrument artifact: the exact sprite's true onset error is bounded O(R/β)
(+0.24…+0.62 s over 2–100R), not "+125 s, unbounded in d"; its real parity break is the
arc, shrunk by exactly 1/γ. Cost to adopt: one exact quadratic per row per occluder.
Not gold: one load-bearing claim refuted by the check.

**Reasons.**

1. **Reproduction.** `regen.sh` exit 0, output byte-identical to the dossier's numbers, 7 s, deterministic. Static controls reproduce e59e (1667/319 at 2R/10R). My from-scratch implementation (simultaneous-distance worldtube test, bisection-solved sprite retarded time) reproduces the entire mid-transit Jaccard table exactly — W1 0.847/0.401/0.079, W2 0.974/0.855/0.420 … 0.875/0.452, W2p 0.9874/0.7840/0.5217/0.3065/0.0000 — and the W1/W3 onset columns to 4 decimals (−1.7634/−9.7637/−99.7659 …). The exact-instrument half of the run is solid, including the analytic correction term R(√(1+β²)−1)/β, which I re-derived.

2. **The instrument bug (my main attack, outside the tested domain).** The W2/W2p **onset** columns come from `min_dist_vs_t`, whose retarded-time quadratic uses the occluder's *current* distance `|occ(t)|` where the worldline's perpendicular offset `d` belongs — exact only at t_O = 0, which is precisely where the (correct) Jaccard table sits. Proof by bisection at t_O = 98, d = 100, β = 0.9: the author's closed form gives t_ret = −40.148; the true solution of |X(τ)| = t_O − τ is −2.016 (38 s of instrument error). Consequence: all four headline onsets are artifacts (true values, my corrected wirings: +0.472/+0.286/+0.241 s at 2/10/100R β0.5; +0.620/+0.434/+0.389 s at β0.9; W2p +0.236/+0.384 s at large d). The rim numbers +0.75/+1.82 s are the same artifact (true: +0.436/+0.275 s). The bug's signature grows as ~β²·d — exactly the "mechanism" the dossier claims for physics. The claim sentence, the abstract, three places in the wiki page and the proposed rung's negative-control expectation ("~β²d at 22d1's measured rates") all carry it. I corrected the page in place.

3. **What actually survives (and is adoptable).** (a) The snapshot kill: mis-timing unbounded in d, arc-disjoint at β·d/R ≳ 2 — exact, decisive against the letter of direction 5. (b) W2 is genuinely not parity, via a cleaner mechanism than claimed: the sprite sits at retarded distance γd, so its arc is the true arc shrunk by exactly 1/γ, centres coinciding (atan(βγ) = asin β) — predicting Jaccard → √(1−β²) = 0.866/0.436 at large d, matching the measured 0.865–0.875/0.436–0.452; at close approach an edge asymmetry (measured 0.855). (c) W2p worse than W2 at speed. (d) Price 69–81 ns/row (81 on this box; order of magnitude). (e) Arm B verified by hand: exact 8.5084 vs quadrature 1.79%; the limb differential 0.782 s = 4M ln((b−R_p)/(b+R_p)), independent of the source-distance nit; 19.55% of a 4 s transit. (f) Arm O cross-checks check2 (17.58°/49.77°) with the standard aberration formula.

4. **Predictions.** `predictions.md` pre-registered (file order consistent). P1 held, P4 held, P6 held, P7 held, P5's cross-check held. P3's refutation stands (exact instrument). **P2's refutation does not**: the bounded rim form the author "refuted" was right in form (bounded; the true rim error shrinks with d, 0.44 → 0.28 s); the run's evidence against it was the artifact. Reporting P2/P3 as "refuted and the misses are the result" is half wrong.

5. **Novelty.** No prior run measures occluder-motion eclipse parity (e59e measured static opacity yesterday; 5977 time transfer; 6eae multi-image; 8be2 moving lenses). The page's own direction 5 named this as unmeasured. Not a repetition.

6. **Goal fit.** Moves the view's correctness half and freezes a wiring decision before the lensing memo lands (principle 19: "a fix signals the wrong representation"; principle 23: the snapshot wiring places influence where the occluder is *now*). The corrected story is *stronger* for the thesis: every cheap wiring breaks parity by geometry (arc placement/width), which no cadence or budget fixes.

**The one experiment to gold.** Fix the two wirings in `min_dist_vs_t` (sprite retarded time by correct quadratic — perpendicular offset, not current distance — or bisection; W2p offset with constant d), rerun, and restate the W2 leg as the bounded O(R/β) timing plus the 1/γ arc-width deficit; re-grade P2 as held-in-form; freeze the rung's sprite-negative at the corrected rates (my numbers above can seed it). One session, the instrument already exists.

**What the author missed.**
- The tell was in their own log: at 100R β0.9 the two "different" wirings W2 and W2p report onset errors +125.1344 and +125.1206 — near-identical where their t_O = 0 behaviours differ materially. Convergent wrong numbers from different methods mean a shared broken instrument, not shared physics (the page's own 5 Oct lesson: agreement is not independence when the harness is shared).
- The true W2 mechanism (retarded distance γd → arc narrower by 1/γ, centres exactly aligned) is one line of algebra from quantities the run already computed, is d-independent, and gives the adoptable rung bar directly; the timing story was the wrong observable.
- Arm B's diff_limb is independent of the source-distance choice (the r_E, r_O factors cancel in the difference) — worth stating, it hardens the 0.782 s.
- Minor: dossier L58-59 has a dropped sentence fragment ("…worldtube test. / frame-consistent (2/10⁴ …)"); the static 100R control is 31 by exact β = 0 (32 at β = 10⁻⁴ motion) — the "reproduces e59e exactly" phrasing overstates by one row at one distance.
