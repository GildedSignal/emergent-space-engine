Grade: silver

**Abstract.** Claim: the lopsided Kerr shadow is real, player-visible and ungated; a χ-blind/|b|-keyed view misplaces it by degrees. Reproduced bit for bit (~12 s): shipped `kerr::deflection` sense-exact (capture exactly at Bardeen's b_c±; bends = oracle modulo the oracle's disclosed 2b/r_max tail, next correction ~1e−10); no gate maps b± to the sky; L57's one-sided deflection(b) wrong by type. Gain: one premise correction plus one gate. But the run's edge map is Schwarzschild's static formula with Kerr b_c: the exact static tetrad (validated 6e−15) moves edges up to 16°, kills the wrap-at-3.2M claim (tangential only at r_o = r_ph⁻ = 3.3–4.0M, never past), cuts the centre headline 33°→20° — r15's reference table is wrong as written.

## Reasons

1. **Reproduction: exact.** Applied `work/patch.diff` to the clean tree (base 2a2afff2), ran `regen.sh`: `instrument-out.txt` and `shipped-defl.txt` byte-identical to the author's, `max |residual − tail| = 1.00e−9`, exit 0, ~12 s. Bend spot checks (`bend(0.9,10)`, `bend(0.998,−20)`) match the stored 9 digits.

2. **The shipped-law half is sound.** Capture thresholds match Bardeen's b_c± exactly (retro −6.138/−6.832/−6.997, pro +4.096/+2.844/+2.111 for χ 0.5/0.9/0.998); the DEFL-vs-oracle residual is exactly |b|·1e−5 = 2b/r_max at every one of the 47 escaping points. I independently expanded the oracle's tail: next correction 2aM/r_max² + b³/(3r_max³) ≈ 5e−11 at b=100 — below the 1e−9 match, so the author's reading (shipped exact, oracle biased by its own cutoff) is right, and P5 holds. The rim-wall numbers (A = 1.000/2.583/0.784; δb/b = 1.86e−3/8.8e−2/3.3e−4) reproduce from the author's own printed bends and are bend-based, untouched by my correction below.

3. **Predictions: held out properly, 2 of 5 held.** `predictions.md` predates the instrument (mtime order; held-out cases named). P1 and P5 held; P2/P3 failed on sign and magnitude (centre measured retrograde, predicted prograde); P4 half. Honestly reported, but by house precedent (1 October red-team) a failed held-out prediction bars gold.

4. **Main attack — the shadow-edge map is not the exact static observer.** The instrument maps edges with α = asin(b·√(1−2M/r_o)/r_o): Schwarzschild's static formula with Kerr's b_c substituted. In Kerr equatorial BL, g_tφ ≠ 0, so a static observer's orthonormal φ-leg is √(g_φφ − g_tφ²/g_tt)·∂_φ-direction, giving
   sin α = √(g_φφ − g_tφ²/g_tt)·Q/(r_o²·E)·√(1−2M/r_o), Q = (b−a) + aP/Δ,
   validated two independent ways (tetrad projection vs the radial-only null identity p₀² = pᵣ² + p₃²: max 6e−15; the b-form (b + 2aM/(r_o(1−2M/r_o)))·√(1−2M/r_o)/√G agrees to 1e−16; reduces to the author's formula at a=0). Consequences, at the edges themselves: the author's map is biased −0.15…−0.35° at 20M, −3.7°(χ=0.5)/−9.7°(0.9)/−12.2°(0.998) at 6M retrograde, −14.5…−16.2° at 3.2M prograde. Against χ-blind (exact-static reading; the χ-blind comparator ±asin(3√3·f/r_o) is correct at a=0 either way):
   - edge errors become ≈ 2.5°–43.9° on the author's grid (was "2.7°–28.3°"): prograde at 3.2M is *worse* than reported (−17.8°/−34.9°/−43.9°), retrograde at 6M better (−7.9°/−13.7°/−15.1°), retrograde at 3.2M flips sign (+4.3°/+15.9°/+18.5°; the author's constant −6.08° there was the forced −π/2);
   - the centre displacement max is −19.8° at (0.998, 6M) — not −33.1°; at 3.2M it is only −6.8°…−13.2°. The retrograde direction survives everywhere;
   - **the wrap claim dies**: for a static observer |sin α_retro| reaches 1 exactly at r_o = r_ph⁻ (3.33M at χ=0.3 → 4.00M at χ≈1) and never exceeds it — I scanned r_o ∈ (2.001, 20] at five spins. At 3.2M the exact retrograde edges are −79.6°/−68.0°/−65.4° (χ=0.5/0.9/0.998), not tangential. The author's "wraps past tangential at r_o ≤ 3.2M", the "≥7-point error the symmetric law cannot represent at all", and r15's criterion (2) are artifacts of the wrong map (its threshold even points the wrong way: tangentiality is *above* 3.2M for every spin tested);
   - arc fractions at 3.2M become 29.0–40.5% (author 31.6–39.3%) vs χ-blind 46.6%; at weak χ the arc error is small (χ=0.3: 44.3 vs 46.6).
   The kill itself survives — and strengthens on the prograde side: multi-degree, monotone in χ and depth, centre displaced retrograde-side, unrepresentable by any |b|-symmetric law at the strong-field rim.

5. **Outside the author's range** (checker cases): χ = 0.3 and χ = 0.9999 at r_o ∈ {20, 10, 6, 3.2}: continuous with the table; at χ=0.3/20M the χ-blind edge error is only −1.5°/−1.7° — below the proposed r15 negative bar "≥ 2.7°", which is a strong-χ number, not a law of the effect (the error → 0 continuously as χ → 0, as law.md L32's "χ = 0 is the Schwarzschild law, bit for bit" demands).

6. **Novelty: real for the record.** wiki/view.md names only "Kerr timing" as unmeasured; docs/HISTORY.md has no Kerr-shadow entry; 039d (the same page's standing half) was Schwarzschild. The physics is Bardeen's (used as controls — properly); what is new is the measurement on the lab's instrument, the sense-split rim wall priced for the memo key, the shipped-law verification, and the gate gap. B19 item (2) *does* gate photon capture at b± of each sense — the physics that makes the edge — so the claim should be scoped to "no gate maps b± to the observer's sky", which is what the dossier means and what I verified (law.md L81; r6 Schwarzschild; r13 the γ channel).

7. **Small faults.** Dossier typo "b_c−=−5.93" for χ=0.5 (the instrument says −6.138 — the page's own numbers are right). The author's "What would make it wrong" flags the observer choice but asserts the static map as settled; it was the one thing that was wrong.

## The one experiment for gold

Replace the edge map with the exact static tetrad (one line: sin α = √(g_φφ − g_tφ²/g_tt)·Q/r_o²·√(1−2M/r_o); my /tmp/check_kerr.py is the reference implementation), re-derive the table and the r15 reference values, replace the wrap clause with the tangentiality-at-r_ph⁻ clause, scope the negative bar to the frozen χ grid, and rerun the predictions. The oracle, the shipped comparison and the rim wall need no change.

## What the author missed

The frame-drag term in the static observer's own tetrad (g_tφ enters e₃ and G) — the exotic case was measured with the boring half's formula. Also: the weak-χ floor of the effect (the "at every spinning hole" refuted-entry headline needs the χ→0 caveat), B19 item (2)'s existing coverage of photon b±, and that the retrograde χ-blind error *flips sign* at the 3.2M rim (under-cover, not over-cover).
