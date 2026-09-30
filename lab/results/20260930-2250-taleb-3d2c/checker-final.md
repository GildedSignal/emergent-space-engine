Working...
Check complete. `check.md` written to `lab/results/20260930-2250-taleb-3d2c/`; nothing else in the folder touched (all artifact md5s and mtimes unchanged).

**Grade: silver** — real, fully reproduced, but two of three headline claims fail adversarial attack.

**What reproduced (bit-for-bit, clean tree):** controls, the full 4096-orbit sweep, sweep-fast, and both chatter runs — every physics field identical (only `wall` differs). Predictions were pre-registered (mtime 23:12:49 precedes sweep 23:15:49 and both chatters) and honestly scored. The post-decisive edit to `tau_selector.py` (23:18:45) was traced via the pre-edit pyc: only the `fast` reproduction path and horizon generalization; physics classes identical, and my bit-identical full rerun settles it. Benign, undisclosed.

**What broke:**
1. **The "100×" placement claim is a grid artifact.** The chatter grid (τ=0.35–0.65) contains no moon straddling 0.40. I ran the missing straddlers: vs τ\*=0.40 they flip up to **1455**/4096 orbits; vs the author's own recommended τ₀=0.28, up to **921**. Placement buys ≤1.6×, not 100× — only dwell/hysteresis removes chatter, inverting the dossier's principle-19 argument. The cost magnitude itself (~0.2–0.35 handoffs/orbit vs H0190's 0.3 kicks/orbit budget) survives.
2. **A retrograde seed bug guts the retro column.** The retro flip reflects velocity across the world x-axis instead of the apsidal line: at e0=0.05 four of eight "retro" seeds are prograde (two bit-identical to prograde seeds — their esc_orb values match the prograde row exactly), two are retro with e=0.149; at e0=0.3, seven of eight are wrong, with e_osc=0.749. The "retro onset 0.45, identical pattern, flat 4/8" is prograde trajectories echoing the prograde result; genuine retro survives past 0.90 — the author's scored "P2 miss" may be the bug masking a correct prediction.
3. **"Exactly the quadrature seeds" is 4-point aliasing.** Clean 16-M0 scans show escape *bands* (quadrature ±45° pro at 0.45; only ±22.5° around alignment survives at retro 0.70), and the discriminator is the moon's initial sun–moon elongation, not the "sun–apsis angle" the dossier names — its own seed 2 (apse aligned, moon at quadrature) ejects.

**What stands:** τ₀ from e-pump tolerance (0.25–0.30, bracketed, saturated not accumulating — confirmed exactly), the prograde escape onset 0.45 (horizon-stable at 8192 orbits), F-verdict transfer (≤2/8 mismatch, clustered 0.40–0.55, dE to 1.44), and the elongation split as a real geometric structure. Novel (no prior evection/chatter/placement work in HISTORY or law.md; B14 is open and FAILing).

**Gold path:** one-line seed fix (assert h<0, e_osc=e0), retro rerun, and a straddler-controlled placement-vs-hysteresis comparison.
