# Predictions — 20261008-1859-second (second author on 20261008-1757-system-72ef)

Written before the decisive experiments. Reproduction (control, main) has run;
it is bit-identical and tells nothing about the level. Tuned on nothing of
mine: the instrument below has never seen the scar arrays. The checker's
histogram estimates (level ≈ 91 bits at q = 1e-6) are on the record, so my
intervals around 91 are consistency checks, not held-out claims; the held-out
items are P3, P4, P5, P6, P7.

Instrument: two-part population code — coarse k-bin histogram table (shared by
all bodies) + exact fractional bits log₂(Δ/q) for the within-bin offset at
quantum q. The plug-in wall log₂(N)/channel is removed because the q-resolution
never becomes distinct symbols. Angles use the wrapped circle.

1. **Instrument controls (positive and negative).** Synthetic wrapped-uniform
   (N = 10⁴) reads 22.58 ± 0.10 bits at q = 1e-6 (exact log₂(2π/q) = 22.577);
   synthetic Gaussian σ = 1e-2 reads 15.34 ± 0.15 (analytic h + log₂(1/q) =
   15.337). Negative control: the old plug-in estimator on the same data reads
   ≤ 13.29 (the wall), i.e. it cannot see either answer.
2. **Level (consistency with the checker's estimate).** Model-coded total at
   45 000 kicks, q = 1e-6: 88–94 bits/body. Per channel: dlambda 22.0–22.58
   (near the uniform bound), dvarpi 20.5–22.5, (dh, dk) joint 33–36, da_rel
   11–13. If it reads ≤ 70, the checker's attack itself was wrong and the
   original dossier's 64 revives.
3. **Held-out generalisation (decisive for the instrument).** With N = 3×10⁵
   same-seed bodies (first 10⁴ identical to main by construction — asserted in
   code), the table fitted on 10⁴ bodies codes the 2.9×10⁵ held-out bodies
   within +0.15 bits/channel of its in-sample level. Excess > 1 bit anywhere
   kills the instrument (then only in-sample upper bounds stand).
4. **The N-sweep is not an independent instrument.** Plug-in at N = 3×10⁵ and
   4 500 kicks reads 79–84 bits total — still pinched (per-channel wall 18.21
   caps the two angle channels, both above 20 truly), while its wall-sum
   5·log₂(3×10⁵) = 91.1 sits within ~2 bits of the true level: a "plateau"
   there is the wall again, agreement with the model would be harness-shared,
   not independent. If plug-in(3×10⁵) matches the model-coded level to 1 bit,
   I am wrong and the N-sweep is decisive on its own.
5. **Time growth with the wall removed (decisive for "saturation").** From
   4 500 → 45 000 kicks the model-coded level grows +1.5 to +3 bits (dh/dk
   only, ~1 bit/channel/decade; angles bounded; da flat). So "saturation" is
   only approximate — logarithmic, not flat — while no channel is linear in
   kicks (the rate-form kill stands). If the growth is ≥ +8 bits/decade, even
   the level framing is wrong and H_live's rate form returns through the tail.
6. **8 GiB pricing (decisive for the budget verdict).** Level(q) falls at
   16.6 bits/decade of q (5 channels × 3.32); the 8 GiB ÷ 10⁹ budget = 68.7
   bits/body incl. genesis is met at a common q* ≈ 2–5×10⁻⁵ on raw channels;
   at q = 1e-6 the store needs 10.5–11.5 GiB (overflows, not brushes). Joint
   (h, k) coding with measured mutual information buys a finer q* (≤ half),
   i.e. more exactness for the same memory.
7. **The secular program re-answered (the original #4, wall-free).** The
   per-body linear-rate program (fitted on the first 30%, as shipped) cuts the
   model-coded level by ≤ 2 bits total, not ≥ 3×: Δϖ wanders non-monotonically
   (author's inspection). If it cuts ≥ 3×, the author's claim #4 revives.

Kill criteria for my run: any control outside tolerance (P1) voids the level
numbers; held-out excess > 1 bit (P3) demotes everything to upper bounds; a
runtime step > 900 s beyond plan.
