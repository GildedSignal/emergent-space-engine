# Dossier — H_live: distinctions per game-second decide the billion-body fit, and they decide it against identity scars

## Claim

For a dense belt, live distinguishing information saturates at the belt's own element entropy — 39/51/63 bits per body at relative scar widths 2⁻¹⁶/2⁻²⁰/2⁻²⁴ — regardless of encounter rate; a 10⁹-body belt reaches that ceiling in ~10 orbits (Ceres-class masses, ~30 game-years, ≈ 6×10⁻⁸ bits/body/game-second), so the identity-scar representation busts 8 GB at any width finer than ~2⁻¹²–2⁻¹³. The rate is not the lever; the representation is: anonymous (exchangeable) bodies have a multiset floor ≤ 23 bits/body at 2⁻²⁰ and the seeded-program residual below that.

## Bottleneck

Board risk "Distinctions created per game-second (H_live): they, not the body count, decide whether 10⁹ fit in 8 GB; not measured yet" (HANDOFF, Risks; plane.md "Measured on the whole"). This run supplies the measurement the `b-h-live` build will instrument, and it moves the decision from "measure the rate" to "choose the representation": belts must not store per-body identity scars.

## Evidence

Impulse Monte Carlo of a Keplerian belt (G = 4π², M\* = 1, a ∈ [2.05, 2.15], Rayleigh σ_e, equal masses), conjunctions Poisson from the analytic crossing flux, deflection δv = 2Gm/(b·v_rel) with random in-plane geometry, exact two-body response of (E, L, eccentricity vector), scars = quantized (ΔE, ΔL, Δϖ) against the population program. 2 seeds × 300 orbits × N = 2000, five cases. Reproduce: `python3 hlive.py` (~70 s, prints the table and the flux validation) and `python3 measure_sig.py` (~70 s, per-field spreads). Data: `hlive_results.json`, `hlive_sig.json`.

- **Flux validated:** simulated conjunctions match the analytic expectation to 0.004% (15,833,023 vs 15,833,626). Cold belt (σ_e = 10⁻²): 26.4 conjunctions/body/orbit; hot (σ_e = 0.1): 2639 (Poisson-thinned 50×, kicks scaled √50, variance-preserving).
- **Scar ceiling (saturated, the load-bearing number):** cold m = 10⁻⁸ at t = 300 measures 39.0 bits/body at q = 2⁻¹⁶ against the uniform cap 39.2 (51.2 at 2⁻²⁰, 63.2 at 2⁻²⁴); the embedded-perturber case (one 10⁻⁷ M\* body) saturates by t = 30. Pre-saturation the walk diffuses: measured histogram entropy rises 0.5 bits per orbit-doubling exactly (19.6→21.9→24.3→26.2→28.1→29.4 bits at 2⁻²⁰, m = 10⁻¹⁰).
- **Time to ceiling at game scale:** σ_E grows ∝ √(N·t·m²); at N = 10⁹ (flux ×5×10⁵) the walk spans the belt's own width in ~9 orbits ≈ 30 game-years for m = 10⁻¹⁰; ~2×10⁵ years for m = 10⁻¹²; ~immediate with a 10⁻⁷ perturber. H_live ≈ 6×10⁻⁸ bits/body/game-second (m = 10⁻¹⁰, 2⁻²⁰).
- **Reabsorption is nil for strangers:** coherent mean drift vs spread = 0.01 σ (all cases) → a program refit removes < 0.2% of the scar bits. Reabsorption is real only where members re-anchor (families, convoys — pop.rs's ladder rung 1), not for a belt of strangers.
- **Instrumentation note for `b-h-live`:** plug-in histogram entropy saturates at log₂(samples) once the walk exceeds ~N/4 bins (my first pass read "32.8 bits" ceilings that were pure sample bias). Field entropies must come from σ (Gaussian fields) with the uniform cap, or from ≥ 10⁴-sample histograms.
- **Multiset floor (computation, flagged as such):** 10⁹ anonymous bodies in M = (W/q)²·(1/q) ≈ 2.5×10¹⁵ element cells at 2⁻²⁰ have an occupancy floor ≈ log₂(e·M/n) ≈ 23 bits/body — fits the 32-bit budget where identity scars (51) do not; the seeded-program residual (components-98bc: 0.126 bits/body) bounds it from below if the walked multiset stays derivable.

## Predictions

`predictions.md` was written before the run. Held: perturber ≥ 100× (saturated by t = 30 vs never at N = 2000 for the base case); bits/scar 25–45 pre-saturation (measured 21–29 histograms, 24–37 σ-based); saturation not growth (σ pins at the belt width); reabsorption < 1%. Wrong, and disclosed: prediction 1 (scar rate < 10⁻⁴/orbit) — my pre-registered Fermi slipped 10⁴× (divided by v_K²b instead of v_rel·b); a typical conjunction kick is ~1 quantum at 2⁻²⁰, so every body scars within 1–3 orbits. Prediction 6's cold-belt half flipped with it: m = 10⁻¹⁰ exceeds budget in decades, not > 10⁵ years; the m = 10⁻¹² half held.

## What would make it wrong

The MC's kick geometry is max-entropy (random direction, uniform anomaly), not correlated conjunction geometry; resonant locking (r4's regime) would slow the walk and is unmodelled; per-orbit linear superposition of kicks; the N-scaling (∝ n) is analytic, not simulated; the multiset floor is computed, not implemented; single belt width (w/a ≈ 5%). None of these plausibly moves the ceiling, which is set by the belt's own element entropy, not by the rate — but the time-to-ceiling numbers carry the rate's model error.

## Cost of adoption, fit with PRINCIPLES

The design consequence: `shipmem`/`b-h-live` must split H_live by identity class — identity scars only where identity is law (named ships, families, the player's consequences, small N), occupancy/program representations for anonymous multitudes. That is "The memory floor is information-theoretic (entropy given shared structure)" and principle 6 ("Store the generator, not the generated"), and it keeps "every body real, never averaged": an occupancy multiset stores every body exactly, it averages nothing. Adoption cost: the scar store's width policy (behaviour width, never law width Q48: a 2.2× idiot index) and an occupancy-coder path in shipmem; the replay question (taleb-c271) needs the event log or re-derivation, untested here.

## The lens

SpaceX's delete-first framing found the idiot index (112-bit law-width scars vs 51 needed vs ≤ 23 floor), but its blind spot bit exactly where warned: deleting per-body identity discards the per-body history that exact replays and rare-divergence certificates lean on; whether the occupancy representation can carry the replay contract is the open follow-up, and this run did not test it.
