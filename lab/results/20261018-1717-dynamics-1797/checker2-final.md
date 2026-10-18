Working...
Check complete. Summary of the second blind check:

**Grade: gold** (`check2.md` written; first line `Grade: gold`).

**Reproduction** — exact. Clean tree + `work/patch.diff`, full regen rerun: analysis tables identical, all 13,518 archived sample rows bit-identical to my fresh run (deterministic), 331,776 crossings / ~21 µs confirming the page's fixes of the dossier's bookkeeping slips. Independent full-series re-fit reproduces every constant: C = 2.603/2.536/2.606×10¹⁰, R² ≈ 0.99999, β = 0.50; anchors −13 and −1 exact on 4096/4096; w drifts, jump counts, radius and periapsis invariants all match; the page's minted-e correction (2.6×10⁻⁵ at 10⁹) recomputed independently.

**Predictions** — pre-registered (file times precede the run artifacts); P1/P2/P4/P5/P6/P7 held, P3 failed and is disclosed as the secondary finding (the one-signed w drift — verified: cum ≡ drift×n mod 1 turn).

**Adversarial** (five, two outside the author's range):
- 2¹⁸-deep circle: D² = 2Cn holds per window, direct rate 260.5 vs C/D = 257.
- Gap-interior seed e₀ = 10⁻⁵ (the dossier's named falsifier): −9.87 vs C/D = 9.25 — state feedback by ~50× against the same-n circle rate.
- **p-sweep 2¹⁸–2²⁹ (new finding)**: the arresting class hits p = 2²⁰, 2²², 2²⁴ — 2²⁴ freezes the whole column from crossing 6815 — while neighbours diffuse cleanly. This falsifies the dossier's "clean law at ≥ 2²¹ M" and the page's strong-field arrest framing; harmless direction (arrest mints less than diffusion, so the 4000× re-pricing stands as a lower bound). Page corrected in place.
- Pin at 16× depth: −1 on 262,144/262,144.
- Retrograde: C within 0.15% of prograde; w drift sign flips with orbit sense.

**Novelty** — the published page still carried this morning's linear pricing (~7×10⁸); the diffusion law, state feedback, w drift and composite price are new, and od 2's named gap is closed. Adoption cost zero: a frozen decision re-priced 4000× under PRINCIPLES 13.

Tree restored (probe files removed, `git status` as found); nothing in the run folder touched except `check2.md` and the two `wiki/order-boundary.md` corrections.
