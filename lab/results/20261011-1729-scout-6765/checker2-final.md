Working...
`check2.md` written. Verdict: **silver**.

**What was done (30-min budget, all processes <50 MB):**

1. **Reproduction** — clean copy, empty patch, `python3 galaxy_doll.py full`: every physics number in `galaxy-out.json` identical to the author's at 1e-12 tolerance; 0.54 s wall. Timeline verified: `predictions.md` (17:46) predates the final script (17:48) and both runs; the post-freeze script edits match the disclosed bug fixes exactly.

2. **Independent instruments (attacking the admitted same-harness oracle risk)** — QUADPACK adaptive quadrature validates the 512-panel reference to ≤5e-12 on B/D/E; a leapfrog on case E (the hardest rosette, which the author only checked same-family) converges with exact 2nd-order behavior onto the compiled phase; P7's GR-seam arithmetic re-derived by hand (r_SOI/rs = c²/2v₀² = 9.29e5, seam 492→1.24e5 rs, ∝M^-0.4 as claimed).

3. **Adversarial cases** — nucleus scatter at β=0.9 passes at 4.3e-10 rad (author ran mbh=0 only, so this *strengthens* the claim). But the **deep-span disc orbit (rp 0.001, ra 20, no nucleus) needs 512 panels to 1e-6 and never reaches 1e-9 ≤512** — directly falsifying the headline's "≤16 panels on every case". Near-separatrix (128/256 panels) and cuspier-nucleus (512) cases confirm the author's own disclosure but extend it inside the claimed scope.

4. **Novelty/goal fit** — no prior galaxy-doll run in HISTORY (prior galaxy entries are pre-pivot GEM sums and lattice cluster tracks); HANDOFF #5 confirms it as the unowned item. Textbook integrability is openly cited; the contribution is the mapping onto the engine's cycle compiler plus the two design rules.

**Silver, not gold:** headline universality falsified by one in-scope case; the disc-deletion claim leans on unmeasured resonance widths; "adoption cost none" overstates (float Python vs the integer/banded Rust compiler); one dossier number (132.8 µs compile) not regenerable by the shipped code (80.9 µs). The gold experiment: rerun with per-band cuts on the adversarial orbit set — then "the smooth disc needs no fallback" becomes a measured invariant.
