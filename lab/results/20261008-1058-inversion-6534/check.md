Grade: silver

**Abstract.** Claim: two concentrated crossing lanes force tier 2's full n_A·n_B product while every per-encounter metric calls the scene healthy. Reproduced bit-identically (`work/crossing/run.sh`, clean tree, empty patch): zero-miss 124/124; hits 189→49 574 (exponent 2.016), evals exponent 2.003, 0.5 evals/pair, ~0.8–1.2 µs/pair (4-thread wall); cone and radial both return exactly m² pairs; corridor d_max 0.029–0.030 rad, 0 beyond 0.15, m-independent (my m=2000 rerun: 0.0323, still 0 beyond); belt contrast 14 951 vs 39 evals/hit. My attacks: zero-miss holds on fresh seeds (129/129), near-tangent (304/304) and steep (100/100) scenes; cone = m² there too. Gain: identifies the last O(N²) block (board's top scaling risk) and the metric blind spot. Cost to adopt: one routing clause plus a crossing-time-rank window, not built here. Two record flaws (below) hold it at silver.

**Reasons.**

1. **Reproduction: exact.** Every deterministic number regenerates (counts, evals, exponents, quantiles); only wall times drift on the shared runner, as disclosed. The exponents re-fit to 2.016/2.003 from the raw lines. The gold's regime reproduces flat (394.0/394.4/395.9 setup evals/pair within-lane).
2. **Predictions.** `predictions.md` (11:07) predates the outputs (11:14) and the log order is consistent. Predictions 1, 2, 4, 5, 6, 7 held; 3 failed and is honestly reported as strengthening the claim. Kill criteria were pre-written; none fired.
3. **Adversarial cases (mine).** (a) Fresh seeds: 129/129 matched, 0 missed/false/dup — soundness is not a seed artifact. (b) Steep incidence (e=0.35, γ≈19.8°): zero-miss, all-Cross sections, 0.5 evals/pair, cone still exactly m² — the product structure is incidence-independent. (c) Near-tangent (γ≈0.6°): zero-miss 304/304, but all sections go Wide, 518.6 evals/pair (72× per pair, 15 497 evals/hit — 1000× per encounter), and the corridor bound breaks (d_max 0.249, 292/8363 beyond 0.15). The author's disclosed failure mode is real and far larger than the run implies.
4. **Novelty.** No crossing-lane measurement exists on the adopted stack (board through 6 Oct, HISTORY.md, `git log`); q-candidate-degree answered dilution at fixed density, taleb-09b5 answered same-orbit concentration. Ancestor: H0156 (25 Sept) found all-pairs search under relative motion in the pre-pivot population sweep — same symptom, different machine; new here are the routing gap between two adopted certificates, the metric inversion, and the corridor invariant.
5. **Goal fit.** Top board bottleneck (q-candidate-degree, the O(N²) scaling risk). It shows a premise wrong: "work per real encounter constant ⇒ healthy" is blind to absolute cost under concentration. PRINCIPLES §10: "We need also to map how things break, think in extremes"; §3 "Compute only surprises".

**Why silver, not gold.** Two dossier numbers its own log contradicts, and the exit is unbuilt:

- The extrapolation divides by 4 twice: 0.79 µs/pair is already 4-thread wall, so 10¹⁰ pairs ≈ 2.2 h (not 30 min) and 10¹² ≈ 9 days (not 2 days). The conclusion (unpayable, and unpayable even at 1 ns/pair) survives — the error understates the cost — but the printed headline is wrong.
- The corridor mechanism is misattributed: my steep control (ρ/sin γ = 0.0030, 4× smaller than the original's 0.0127) leaves d50 unchanged (0.0106 vs 0.0104). The width is set by the lane's crossing-longitude dispersion (ϖ spread ±0.02 rad) until γ gets small (tangent: d50 ≈ ρ/sin γ indeed). "d50 ≈ ρ/sin γ" was scene-coincidence numerology; window sizing and the near-tangent trigger both depend on getting this right.

**The one experiment to gold.** Build the exit on the frozen scene: sort each lane's crossing times per crossing longitude, sliding-window merge with half-width from the measured corridor (dispersion ∨ ρ/sin γ) + margin; verify zero-miss vs truth at m ≥ 500 and measure work per real encounter (the selectivity side of O((n_A+n_B)·log n)). That converts the corridor from a necessary condition (recall, measured here over 15 391 encounters) into the claimed mechanism, and re-does the two flawed numbers.

**What the author missed.**

- The two record errors above; both are in adoptable text, not just prose.
- The measured scene is the benign end of the crossing family: near-tangency costs 72× more per pair and 1000× per encounter (measured by this check), so the product block's constant varies by ~100× across incidence — the routing trigger needs γ, not just "cones intersect".
- Zero-miss vs truth only at m=100; the corridor at m ≥ 500 is measured over method events, sound by extension of the control, not directly.
- Within-lane blocks were never truth-checked (minor; the claim's focus is A×B).
- H0156 should have been cited as the ancestor of the symptom.
