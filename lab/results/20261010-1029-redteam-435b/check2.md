Grade: gold

**Abstract.** Claim: the design's view contract (representation.md §2 / law.md "Observation": one crossing per tube, lensing from the doll's memoized deflection(b)) fails structurally near a compact mass. Reproduced bit-for-bit (two reruns byte-identical, 15 s, 34 MB): at r_o = 10 M every source within 41.3° of the anti-hole direction vanishes while truth shows ≥ 2 images (μ-ratio ≥ 0.56, cut-independent); at r_o = 100 M memo directions are off by up to 26.5°, > 1° for 67%. Blind ⟺ b_line < 3√3 M (closed form, re-derived); weak-form negative control fails identically, so the failure is structural. Verified: no r6 rung exists, B3/B16 gate the forward ray only, view.rs is flat-only today. My probes extend it (r_o = 30 M: median 29° error where it sees). Adopt: freeze r6's completeness criterion and the branch-indexed memo before the gather is built; zero engine cost.

## Reproduction

- `python3 falsifier.py` (numpy 1.26.4): 16.3 s / 14.8 s wall, 34 MB RSS (dossier: 13.8 s, < 100 MB ✓). Two consecutive reruns produced byte-identical `falsifier-out.json` (md5 eaa136de…), 421 leaf fields — the author's "421/421 identical" verified. Every dossier number matches the JSON to the last digit: A 1 root at 5.94e-6 rad, Newton 1 iteration at β ≤ 0.999 (src −0.9c); B err/bend 5.15%, b_line 749.45; C r_o=10 blind 100%, multi 100% (all three r_s); r_o=100 blind 14.3% (exact alignment only), median 2.05°, max 26.49°, >1° 66.7%, >10° 16.7%, weak-control identical 16.7%; C4 gap 0.72 rad half-width (dossier's 1.44 full), truth_min_images 2, always visible; convergence 2 roots at n=700, 3 at n=1400.
- Disclosure: the script writes its JSON next to itself, so my rerun overwrote the author's `falsifier-out.json` in the untracked folder (no git copy existed). The on-disk file is the deterministic script's own output and matches every quoted number; nothing else in the folder was touched.
- `work/patch.diff` is empty — no tree edits to apply. Premise quotes verified verbatim: representation.md:57, law.md:53 ("Lensing takes deflection(b) from the doll's memo"), view.rs:14-15 ("Light is straight in the root frame (no lensing yet)"). `lab/rungs/` has no r5/r6; law.md:88 lists r6 as an open rung; representation.md §7's r6 line measures cost only. B3/B4/B7/B16 are forward-ray/clock gates. The "ungated inverse gather" claim is exact.
- predictions.md predates the decisive artifacts (mtimes 38 m vs 23 m / 19 m at listing). The pre-registered kill criteria all triggered as frozen (blind non-empty at r_o = 10 M; >1° for a double-digit fraction).

## My adversarial cases

1. **Independent truth.** scipy DOP853 with a terminal event on the same orbit equation: agrees with the author's RK4 table to 3e-4–8e-3 rad over b ∈ [5.5, 300] (0.06 rad at b = 5.5 near the divergence). The dossier's "two independent methods agree to 10⁻⁴ rad" holds only near b ≈ 300 (4.5e-5 abs); at b = 30–250 the table sits 4e-4–8e-4 rad off. Immaterial: every conclusion is degree-scale or closed-form (b_c alone decides the blind patch), and the negative control already rules bend accuracy out.
2. **Shadow edge at r_o = 10 M.** The tracer's capture boundary sits 2.7° inside the analytic asin(b_c√(1−2M/r_o)/r_o) = 152.31° (over-capture of marginally escaping rays near the photon sphere). Bias direction is conservative for the "truth never absent" claim. The exact-alignment pair reproduces at 136.30°/223.70°, equal magnification, outside both edges.
3. **Fresh standoff r_o = 30 M, r_s = 100 M (author never ran it).** Blind for 50% of the swept window; where the memo sees, median error 29.2°, max 94.8°, > 1° for 100% of sources. The failure persists and is relatively worse at an intermediate standoff — this kills any "10 M is extreme, 100 M is safe" middle ground.
4. **Magnification robustness.** The two true images behind the hole sit at μ-ratio 1.000/1.000 (alignment) and 0.56–0.59 (off): "≥ 2 images" survives a 50% cut; the 1% cut does no hidden work.
5. **Off-axis control r_o = 10 M, dφ = 2.0.** b_line = 7.7 M is already strong-field; memo off by 23.7° even off the anti-hole axis — consistent with C3, and the failure zone at close standoff is wider than "behind the hole".

## Novelty

No HISTORY entry or prior run attacks the inverse gather. H0211/H0212 built the flat (no-lensing) gather — exactly what this run's control A validates; B16 (1 Oct) gates the forward bend of moving lenses. The premise lines date from the 30 Sept pivot and law.md's 5 Oct freeze and were never tested. Not already known.

## Goal fit

P30 ("navigation, knowledge and dynamics those need to be perfect") — the gather is the knowledge instrument; P34 ("the oracles are guards, not shepherds") — B3/B16 shepherd the forward bend while the player-visible inverse walks unjudged; P10 — simplest falsifying test first (static scene, 15 s). It shows a written premise of the design is wrong, at zero engine cost, adoptable in one step (amend the Observation lines; freeze r6 with the completeness criterion and the branch-indexed memo before anything is built).

## Why gold and not silver

Reproduced bit-for-bit; the decisive, pre-registered kill criteria held; controls pass on both sides; the negative control proves the failure structural; the premise text, missing rung, flat-only view, and gate coverage all verified against the repo; my independent scenes extend the kill rather than weaken it. Two auxiliary held-out predictions missed (B1: 5.2% vs ≤ 1%; C1: wrapped images below the cut) — both reported honestly as misses in the dossier's Predictions section, neither load-bearing for what would be adopted (one of them strengthens the attack). This differs from the 1 October precedent, where a missed prediction was reported as held.

## What the author missed

- The moving gather (observer at β → 1 sweeping a lens: caustic crossings per frame, Newton seeding across aberration swings) remains unmeasured; disclosed, and structural in kind, but r6 should name it.
- The named cure for scene B's composition error ("a Newton that iterates through the bend") is asserted, never run — the 5.2% → ? after bend iteration is unmeasured.
- The deflection-table agreement claim is loose (1e-4 only near b ≈ 300; 4e-4–8e-4 across the used range).
- The truth tracer over-captures near b_c (edge ~2.7° inside analytic at r_o = 10 M); conservative here, but must be tightened before r6 freezes it as the oracle.
- The attack is Schwarzschild-only; the showcase is Kerr (B19), whose lopsided shadow and asymmetric caustics will move the numbers — the proposed r6 criterion must state the metric, and the 1%-direction tolerance is ill-defined at caustics until the branch index the author proposes is part of the criterion.
