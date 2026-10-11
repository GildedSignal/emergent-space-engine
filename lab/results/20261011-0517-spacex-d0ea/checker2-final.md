Working...
Check complete. **Grade: gold** — written to `check2.md` with the abstract for the integrator.

**Summary of the check:**

- **Reproduction:** bit-faithful. My small-config rerun matches the author's stored decisive run within 0.06 bit and their cadence control exactly; every dossier number regenerates from `analyse.py` on the stored CSV. Deterministic across reruns. The 6.1 GB RSS overrun of the decisive command is confirmed in `belt-hlive.time` and honestly reported; my reruns all stayed under 700 MB.
- **Adversarial probes (4, all confirmed the claim):**
  1. **μ→10⁻⁶/10⁻⁹ sweep** — scatter falls exactly 10 bits/field per 1000× planet mass, linear in μ with no floor: the scatter is planet-coupled synodic physics, not rounding (this settles the attribution the cadence control left open, and supplies the negative control `predictions.md` wanted).
  2. **M=512** — distribution is quasi-uniform (range/sd≈3), so log₂(1+range) is a fair cost and the headline slightly *understates*; entropy ≥9 bits/field.
  3. **e₀=0.2** — same one-time-scatter shape; single-scene worry doesn't bite.
  4. **Smoothness in orientation** (ρ≈0.998) — the author's named epicycle-generator fix is viable; the residual is a smooth function of synodic phase.
- **Predictions:** pre-registered (file times confirm), misses disclosed and correctly diagnosed — the 7× magnitude miss *is* the finding, the opposite of tuning.
- **Novelty/goal fit:** H_live was explicitly unmeasured (HANDOFF, plane.md); the prior belt gold covered births only. The run kills the shipmem premise (program + averaged generator, sparse scars) at the law's current quanta: 8.6–18.3 GB at 10⁹ against the 4 GiB budget — the "premise is wrong" gold prong, adoptable within one step as the belt-store requirement.

Tree left exactly as found (patch reverted, scratch test removed; only `check2.md` added to the run folder).
