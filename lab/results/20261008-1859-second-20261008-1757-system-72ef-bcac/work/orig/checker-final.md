Working...
Check complete. `check.md` written to the run folder; grade **silver**.

**Verdict in brief.** The work reproduces exactly (control bit-identical, main content-identical in 31.7 s, predictions pre-registered at 18:06 vs the 18:11 run, empty patch), is the first measurement of the H_live risk, and its structural result survives attack: no scar channel grows linearly in kicks, so "distinctions per game-second" is the wrong quantity.

But the headline number is an instrument artifact. The entropy estimator is plug-in over N=10⁴ bodies, capping each channel at log₂N=13.288 bits (66.44 total) — and the measured "saturation level" 64.3 sits against that wall (dlambda 13.278/13.288, 9 996 of 10 000 codes distinct). Three adversarial cases:

- **N×10, same physics:** level reads 73.85 (+10.2 bits), every channel above the old cap, still climbing toward the new 83.05 wall — a width-set level would not move with N.
- **μ×10, same N:** reads 66.38 at q=1e-7, 0.06 bits under the wall; ten times stronger physics moves the "level" by 2.3 bits.
- **Distribution estimate from the stored arrays:** true level ≈ 91 bits/body at q=1e-6 (dlambda cross-checks at 22.5 vs the 22.58 uniform bound) → **11.4 GB at 10⁹ bodies: the 8 GB verdict flips from "brushes" to "overflows"**, and the quantum becomes the budget-derived lever — the inverse of the dossier's "not set by the quantum".

Silver, not lead: the rate-form premise kill is real and adoptable now; the level/pricing half needs the one named experiment (ceiling-free re-measurement, whose cheap version I already ran). One disclosure in check.md: my `main` reproduction ran with cwd in the run folder and rewrote `scars-main.json`/`.npz` — content verified identical to the stored values extracted beforehand (seeded, deterministic).
