Working...
Check complete. Verdict: **lead**.

**What I did**

1. **Reproduced bit-exact** — reran `falsifier.py` clean: every A/B/C number matches the stored JSON (float identity, seeded RNG included, 1.7 s). Verified the closed forms independently (x = 2√(1+e)δv/(1−e), the separatrix conditions, the Binet cubic). `patch.diff` empty, nothing outside the run folder touched.

2. **Ran five adversarial cases**, one class outside the author's range: second GR energies (E = 0.97/0.99 — log form and the (δL/d)² law hold, prefactor b/2T collapses as E → 1, and the family exists only for E ≥ √(8/9), so the 4.9% headline is the worst point of a narrow band); one decade deeper d; a *non-crossing* 0.9× boundary kick (still 9.9% wrong); the belt e* boundary at e = 0.999995 (0.87%, confirmed); apoapsis-site control (10⁴–10⁶× safer — the e* table is a periapsis boundary). The physics survives everything.

3. **Found the kill is not new.** `docs/law.md` retired this exact update on **12 October** (commit 49d59704, six golds): "The jet is retired… **a kick recompiles its cycle exactly, as the plane does**." `lab/wiki/kick-jet.md` (70 runs, titled with this run's premise) already holds the same constant — 9a04 (gold): (15/8)(δE/(1−E))² — the same plunge-fabricated-as-bound type error (4978, gold) — and the same root-distance fix (ee08, gold). The attacked sentence lives only in representation.md §3, a DRAFT untouched since 6 October. By the lab's own rule ("a repetition is not gold, however well done"), this is a lead; no experiment could make it gold because the stricter fix is already the law.

4. **Named four dossier defects**: the φ control "1.2e−5" is not regenerable (7.3e−5 measured); "half of r1's sampler" overstates (top ~28% of e ≤ 0.9); "unbinds after 18 kicks" (17 complete); the "27–55% at eps 0.03–0.10" churn citation unfindable.

5. **Corrected the author's wiki page** (prior-record citations on the Current-best paragraph and Refuted bullet, "half" fixed, grade context in the Runs entry) and flagged a process finding: two red-teams in one day missed kick-jet's page on the same premise — the wiki's discovery path failed, not just one author. The one adoptable residue is a doc sync: representation.md §3 should carry law.md's retirement.
