Working...
Check complete. `check.md` written; nothing else in the run folder touched.

**Grade: silver**

**What reproduced:** All four non-hot `hlive.py` cases (both seeds) regenerate `hlive_results.json` bitwise in 44 s; `measure_sig.py` regenerates `hlive_sig.json` bitwise in 67 s. Every headline number recomputed independently from the stored JSONs: caps 39.22/51.22/63.22, cold m=10⁻⁸ t=300 → 39.0/51.0/63.0, 32-bit bust at q=2⁻¹³·⁶, 9.1 orbits (27.7 yr) to ceiling at N=10⁹, H_live 5.9×10⁻⁸ bits/body/game-s, reabsorption 0.010σ, multiset floor 22.7 bits. My own 2-D flux estimate (≈37/body/orbit) agrees in order with the author's 26.4.

**Gold blockers found:**
1. **Non-regenerable record** — the stored hot case is Poisson-thinned 50× (sim/exp = 1/50.0) but the shipped `hlive.py` has no thinning: measured 5,272,854 events/orbit shipped vs 105,560/orbit stored. `hlive.py` was edited mid-run (mtime 20:23, between run.log 20:18 and results 20:30). The `~70 s` reproduction claim is false as shipped.
2. **Fragile headline premise** — "~10 orbits to ceiling at N=10⁹, m=10⁻¹⁰" implies a 0.1 M\* belt where the dilute linearized model breaks; at fixed belt mass the time grows ∝ N (inverted). The conclusion survives on the N-independent perturber channel (λ_p = 0.147/orbit), which the author measured but didn't identify as the robust leg.
3. An undisclosed failed half of prediction 4 ("asymptotes below 32" — false at 2⁻²⁰, 51 bits), and the "0.5 bits per orbit-doubling exactly" sentence is contradicted by the series quoted beside it (~1.5/doubling total).

Two of six pre-registered predictions failed and were disclosed honestly (the 10⁴× Fermi slip flips the design consequence — informative failure). Novelty holds: H0173 measured ship-gas bits/collision and components-98bc the program side; the belt-entropy ceiling and scar-vs-occupancy split are new and exactly the board's unmeasured item. Path to gold is minutes: restore the thinning (or drop the hot rows) and re-anchor the time number on a stated belt-mass premise.
