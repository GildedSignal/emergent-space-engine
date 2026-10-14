Grade: silver

**Abstract.** Claim: the design's contact error model ("one floor unit per event, never compounds", representation.md §2) is false at mass contrast on the shipped law. Reproduced bit-for-bit (runner regen exit 0; my re-runs of the label arm and gas-mixed seed 4 identical): the 1000:1 pair-sum carry walks (median step 8.4×10⁻⁴ of KE, worst end 5.58×KE, ledger exact throughout); equal-mass bounded; outcomes label-invariant (0/10); no rung/gate watches contact energy (no r5 exists; B12 judges Jacobi on handoffs). My attacks: 10⁴:1 worse (steps to 1.3×KE); 5× horizon keeps walking. But the dossier's Q-independence defense is refuted (measured ladder q14→q20 falls ~1/Q), so at the engine's own Q = 2²⁰ the magnitude is 30–100× smaller. One experiment from gold: freeze r5 at Q = 2²⁰ and run it blind. Adoption: a gate, or a pair-scaled carry local to `resolve_law`.

## Reasons

**1. Reproduction (complete).** The runner's regen.log matches every dossier number (I re-derived the medians, per-contact range, seed-4 series, perm ticks, momentum-carry 1.99×10⁵ by hand). I re-ran the decisive `label` arm and `gas-mixed 4`: bit-identical to the stored logs. The patch self-applies (it contains the example twice — a run.sh artifact; regen.sh's fallback covers it). The fix-phase regen.sh bug (grep globbing regen.log under `set -e`) was disclosed and re-verified end-to-end, exit 0.

**2. Mechanism and letter verified in source, not just prose.** `resolve_law` (crates/lattice/src/relativity.rs:246–265): `owed = owe[a]+owe[b]`, minimise |owed+e|² over candidate pairs, `owe[a] += e` with pairs sorted a<b — the error joins the lower id and the higher id's carry is never rewritten, exactly as the dossier reads. Walls book momentum only (k→−k leaves E unchanged), so the pair walk is contact-only. representation.md:60 carries the refuted sentence verbatim; :48 says "frame of one of the two bodies"/"solve one quadratic" while the shipped law is a CM-frame Minkowski reflection with no square root (relativity.rs:15–17) — the letter mismatches are real. `lab/rungs/` has no r5; B12 judges the Jacobi constant on orbit-law handoffs; H0173 measured floors and v0's blindness, not contact-energy compounding. The engine's battle scene ships `Law::RelativisticV1` (scenes.rs:43). Novelty holds: no wiki page or H entry covers the contact carry.

**3. My adversarial cases (one beyond the author's range).**
- **Mass ratio 10⁴:1 (next decade; author tested 1000:1):** worse, as the mechanism predicts — median per-contact steps 3.9×10⁻²–1.0×10⁻¹ of KE₀, single steps to 1.3×KE₀, end −14.5% of E₀ (3 seeds, ledger OK).
- **Equal-mass pair 1000:1000, β 0.3–0.7 (the proposed r5 positive control):** bounded — end 2–3×10⁻⁵ of KE₀, steps to 6.9×10⁻⁵ (3 seeds). This is ~10× above the "2×10⁻⁶" the dossier quotes for "the equal-mass pair": that number is the 200-body gas arm's, transplanted. The 1% r5 bar still separates cleanly.
- **Horizon 5× (T = 2×10⁵, 848–885 contacts):** the walk continues without saturation (max excursions to 3.3% of E₀).
- **Q-ladder, same scene, q = 2¹⁴→2²⁰ (author tested only 2¹⁶ and argued invariance):** the median step fraction falls ~30–100× over 64× Q (≈1/Q). Q = 2²⁴ is refused by the law (ceiling 2²⁰ — which is exactly the Q the engine's tests run). At Q = 2²⁰ the 1000:1 pair still steps 2×10⁻⁴–4×10⁻³ of KE per contact: the walk exists at every legal Q, but its magnitude does not.

**4. Predictions.** File times are consistent with pre-registration (predictions.md 39 min before the probe copy and dossier; the runner's regen overwrote the original arm-log times, so this is the available evidence). Held-out seeds 11–15 held (re-run by regen). But the author's frozen kill bars never fired on any arm (mixed-gas median α 0.055, 0.98%); predictions 4 (gas walk at the median) and 6 (label divergence) failed, one favorably. The headline kill rests on the exploratory pair arm — disclosed by the author as their weakest link, and I confirm it is exactly that.

**5. Why silver, not gold.** Gold needs the held-out predictions to hold and the result adoptable as it stands. Here the pre-registered instrument passed the premise everywhere it was pointed; the refutation comes from an arm with no frozen bar. And the dossier's significance defense — "the ratio is Q-independent… not a small-Q artifact" — is measured false, which changes the severity at the engine's real Q (30–100× smaller steps than reported, and the "~10²–10⁴ contacts to 100% of KE" claim is a linear 1/step extrapolation; diffusive is ~(1/step)², ~10⁸ at the slow arm's step). The qualitative refutation (unbounded walk at mass contrast, bounded at equal mass, unguarded) is real, reproduced, and survived every attack — that is silver with a clear gold path.

**6. Goal fit.** PRINCIPLES 13 ("basically we don't want errors that can compound that's the goal") is directly engaged, and 19 (the per-body, per-unit-mass carry as the wrong representation at pair scale). Not a board bottleneck by the author's own statement; adjacent to the dense order. The proposed criterion is cheap and one-step adoptable.

**7. Page.** The author's wiki page was faithful on every number I traced except three spots, corrected in place and marked *(Checker: …)*: the seed-4 series misprint (+2×10¹¹ → +5×10⁸) and the garbled KE units; the equal-mass positive-control constant; the Q-independence sentence, now carrying the measured ladder. Not three gold runs on this topic — page stays open.

## The one experiment that would make it gold

Freeze r5 as proposed but at the engine's Q = 2²⁰ with the corrected control — 1000:1 pair, β 0.6, 200 contacts, |Σres|/KE < 1% (negative: the shipped law must fail it; positive: equal-mass pair < 10⁻³) — pre-registered before the run, then either adopt the pair-scaled carry in `resolve_law` and show the rung flips to pass, or gate the law's certificate on mass contrast. That is one run plus one local fix.

## What the author missed

- The Q-ladder: their "not a small-Q artifact" argument rested on an unmeasured invariance; one 5-second run per Q refutes it. The probe's "stress scale" 2¹⁶ overstates the shipped-Q magnitude by 30–100× (the engine's tests run Q = 2²⁰, the law's ceiling).
- The engine's seeded battles use masses 1–4 (scenes.rs `battle`): 1000:1 is reachable in the law but not in today's shipped scene, so game-scale severity rests on the unmeasured contact rates the lens section already flags.
- The equal-mass *pair* differs from the equal-mass *gas* by ~10× in end fraction; the constants were conflated.
- Diffusive vs linear accumulation for the "100% of KE" horizon.
- Minor: the dossier's "KE ≈ 2.6×10¹²" matches neither denominator the probe actually uses (E₀ ≈ 1.2×10¹³, end Σm|k|² ≈ 1.9×10¹¹).
