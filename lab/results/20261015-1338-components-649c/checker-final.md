Working...
Check complete. Verdict written to `lab/results/20261015-1338-components-649c/check.md`, page corrected in place.

**Grade: gold**

**Reproduced** — clean tree at base 0233abef, regen exit 0; every floor number to the digit (8.540e-18 ×3 at 10⁴, 3.084e-17 ×2 at 10⁵, 6.102e-8/6.021e-8 at 10³, near counts 308/309/322, readouts/emitter 1.67–2.00). Timing-only diffs (23→25.85 µs/body, 196.6→194.5 s); one real dossier mismatch: the 10⁴-coast table cell "max 1.6e-9" vs regen's 4.156e-7.

**Predictions** — pre-dated by file times (21 min vs 10–16 min artifacts); all six held, no kill criterion fired.

**Adversarial (3, one outside range)** — (a) rtf 10⁴: drift 1.103e-5 ≈ the disclosed 1.06e-5, boundary verifies; (b) L15 in the *live* post-first-light regime at 10³ — far rows exact (p99 1e-17) where coast drifts 6.1e-8: the observer-side burn claim survives its hardest case, strengthened; (c) N=3×10⁵: 299,685 far rows exact, near set 338, price linear, 786 MB.

**The correction I folded into the page:** the 10⁴/10⁵ "bit-exact" windows end at game 433/133 s — *before the belt's first light* (first steps 356–543 game-s; view.rs returns the tick-0 state pre-light, constant by construction). The permanent regime is the run's own 10³ 899-frame arm: horizon 8.3e3 frames, far demand ~12/frame at 10⁵ — the ~300× deletion and O(near) read set survive unchanged, so this corrects the headline numbers, not the claim. Also fixed: "9,714/10,028 never step" is contradicted by the arm's own max (≥1 stepper; honest is ≥99%), and the 6e-8 rad/frame motion is emission-point orbital advance, not observer parallax.

**Gold because:** it answers the board's "which term breaks first" on shipped code (the gather, 97–99.8% of the flown frame), refutes view open 3's O(visible) burn premise measured on shipped crossings, and hands 2df1's existing row-set build its missing exact due rule — adoptable in one step, ≥10³× ceiling path.
