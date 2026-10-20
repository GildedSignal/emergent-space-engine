Working...
Check complete. **Grade: silver** — written to `lab/results/20261020-1503-redteam-039d/check.md`, with the author's wiki page corrected in place where its Channel-2 constants overstated.

**What I did:**
- **Reproduced exactly**: `regen.sh` in a clean tree, exit 0, 39.4 s, `results.json` bit-identical (only `elapsed_s` differs). All controls assert; the deflection control's 2.95e-4 is exactly the second-order term.
- **Independent validation**: wrote a separate RK4 Binet integrator — reproduces the shadow edge to 3e-5 rad at r_o = 20/6/3.05M against the closed form; confirms the 25.00%-at-6M shadow and e59e's cross-run number.
- **Found a real instrument bug**: Channel 2's "backward ray" `u = (cos α, sin α)` is mirrored for the turning branch (true image bearing is π−α; my RK4 ray at π−α hits the emitter at φ = 2.6001 vs target 2.6, at α it lands at 1.28). The measured chord headed *away* from the hole, so "0.0% chord-blocked / 100% of eclipses missed / never fabricated / 9.3M separation" were forced artifacts, not physics. Re-measured on the author's validated path machinery: the chord misclassifies 7.6–12.0% of near-hole occluders **by both signs** (misses 5.0pp at Φ 2.6, *fabricates* 3.3pp at Φ 2.9) — the by-type kill survives, bidirectionally, and the "never fabricated" claim dies inside their own grid.
- **Adversarial beyond their range** (r_o = 3.05M): instrument holds, shadow = 49.1% of the sky, naive fabrication 100% (analytic for *every* r_o < b_c), all lensed images within 0.0021M of b_c — the rim wall is worse, not better. Their disclosed near-side under-count checks out (my 10.2% vs their ≈9%).
- **Novelty confirmed**: no prior run or rung measures occlusion correctness near a hole (e59e = fraction only; 22d1 = weak-field cost; r1–r10 in `lab/rungs/`, none names occlusion).

**Silver, not gold**: predictions held 2/5 (honestly reported), and one channel's headline constants were artifacts until corrected here. The one experiment to gold: refreeze r14 with the corrected bearing and a mismatch-based negative bar — numbers supplied in check.md.
