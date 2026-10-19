Working...
Check complete. Summary of the verdict:

**Grade: silver** (`lab/results/20261019-1551-dynamics-e3b7/check.md`).

**Reproduced fully** — regen digest-identical on every arm; my own clean-tree rebuild from `work/patch.diff` and a variant binary validated bit-for-bit against C0 (`e8a69ff7…`); the dossier's slim-pair digest `37cfa9f0…` reproduces exactly. Most dossier numbers check out to the digit (C0 maxk ladder, rms growth, esc timing, contact totals, wall rates).

**But the central mechanism claim is refuted by adversarial control.** The dossier attributes the cold belt's self-destruction to "the tide representation, not contact noise" — "a contact-free cold belt self-heats". Four flights of mine:
1. **Isolated orbits** (outside the author's range): exact and +1-quantum circular single bodies at 36q and 70q are bounded for 7–19 orbits (maxk drift ≤ 0.25%) — and since belt bodies interact *only* via contacts, any C0 body that never contacted must follow this bounded dynamics.
2. **The decisive control**: same 800-body cold belt with `Response::Pass` (contacts recorded, velocities untouched) is **flat for 32 768 ch** — maxk +0.04%, rms constant, esc 0 (digest `b73b06dc…`). The instability is **contact-triggered, tide-fed**, not a pure tide pump. The energy half of the author's sentence survives (elastic bounces can't raise max speed).
3. **Cadence ruled out** (the author's own lens-note check): every-4th-chronon kicks at 4× leave onset unchanged (12 236 vs 13 022) — prediction held, cadence is a dead fix.
4. **Seed 2 thermal-0**: kill reproduces (onset 12 422, maxk→755k).

Also corrected on the page: "season peak 183 685" is the late *grinder's* peak (at t≈47.7k the cold control's own window is 184 250 — ratio 1.0; the real season peak is 102 874 = 174× cold); "esc 0 always" is false at genesis (301 bodies born beyond 250q); "1376" appears in no artifact (esc_max 1379 / esc_last 1371); the shell holds 77 bodies at t=4096; the discriminator's "≈20k contacts by 12k" is actually 1 352.

**Silver, not gold**: real, novel (open direction 2's named leftover, first flight), honestly pre-registered (P1's kill branch fired as written), but as submitted it would teach the integrator a wrong mechanism. The one gold experiment — the `Response::Pass` control plus corrected numbers — is flown and recorded in check.md; adopting the corrected page redirects the fix (pericenter pump on contact-eccentricized orbits, or Pass bodies for gravitating-only scenes — not cadence, not gravity wholesale). The operational verdict stands: today's wiring cannot hold a belt, and the missing gate is real. Tree left clean; nothing outside the run folder touched.
