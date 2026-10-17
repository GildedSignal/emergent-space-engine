Working...
**Grade: gold** — written to `lab/results/20261017-0839-fermi-2b89/check.md`.

**What I verified:**

1. **Reproduction, clean tree.** Applied `work/patch.diff` myself; the probe reproduces `probe.out` **bit for bit**; `compose.out` matches regen exactly. Independently recomputed D* (2.47/5.33/0.77 m), b_flip, the 10⁹ event rates (6.45×10⁶/s → 25.8/322 cores), and the Dohnanyi mass/flux — all match. Read the shipped code the claim rests on: `word_for` (60-bit-relative, `v_max.exponent() − 60`), `quantize`'s carry floor and fire rule, `AU`, belt radius, Rayleigh-0.07.

2. **Predictions.** Pre-registered (mtime 08:53:48, before compose.py 08:59:22); outcome A held (ev −73.6±1.5 predicted, −73 measured; mint threshold predicted 2¹¹, measured 2¹¹–2¹²). The two disclosed failures — a c-vs-c² slip that *strengthened* the claim, and the control-caught first reading — are marks of genuine pre-registration.

3. **Adversarial, 4 cases (one outside range).** Full census at seeds 1/2/7 and N=10⁴: **9,700 belt bindings all in {−73, −72}, zero Passages, whole plane [−77, −71]** — no shipped binding near f0a2's −48 world. Mint ladder on 3 more bodies + transverse axis: threshold is **2¹¹–2¹²** (dossier's 2¹² is the k=300/axis-0 value), tube moves a tick from 2² transversely while the compiled entry holds. ±2⁴⁰-quanta orbit changes leave ev invariant. Slow-conjunction tail fires *harder* (Δv ∝ 1/v_rel), so 0% deletion is robust.

4. **Novelty.** First integer-path measurement of the live anchor; the published page's standing contradiction was between f0a2 (legacy E-key code reading, still "awaiting grade") and 277d (hypothetical binding-relative anchor) — neither measured the shipped binding.

5. **Page corrections (in place).** 2¹² → 2¹¹–2¹² (three places); "all below the 70-m floor" no longer sweeps in D*_key = 184 m at 10⁷ (the 0% deletion rests on D*_word 0.77–11.5 m); Domain line extended with the checker census. Accidentally ate the "Event itself" paragraph during editing — restored; structure re-verified (header, five sections, no conflict markers).

Tree restored to pristine (scratch example removed; only `lab/results/` untracked, as expected). No commits made.
