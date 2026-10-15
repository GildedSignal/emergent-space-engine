Working...
Second check complete. `check2.md` written with `Grade: gold`; the author's page needed no further correction (its one mislabel — the 2.7×-vs-promotion-path phrasing — was already fixed on the page and I verified the corrected arithmetic). Tree restored pristine; nothing else touched.

**Verdict: gold.** Basis:

- **Reproduced from a clean tree**: applied `work/patch.diff` myself; decisive run p50 4.43 µs / p99 7.85 (dossier 4.44/7.85), held-out seeds 4.54–4.55 at load 1.3, e-bands and strong-field grid identical, deterministic content bit-stable.
- **The harness prices the flight's true path**: `ladder_ship → add_body → spec_binding → OrbitKey::bound(to_tube(periapsis), e_q48)` is verbatim the shipped flight (scenario.rs:260-262, universe.rs:343-346); doll 0 is `Unit::ONE`, `to_tube` identity (world.rs:86,98-100).
- **Adversarial cases held**: N=10⁶ keys with a fresh seed (5× the author's range) → p50 4.58, still e-monotone; RSS 2.10 kB/body as claimed; and I independently re-derived the in-flight corroboration from b172's published branch — promote p50 4.44/4.60 µs, 940,718 promotions at cap 16,384, 4.72 s — which sits exactly on this run's number and being *below* `add_body` makes the batched-form regression worse (~2.8×), not better.
- **Novelty and fit**: fills open direction 4's explicitly-missing number; kills 262f's belt adoption ("cuts ~3–8×" was priced on a669's ~30 µs anchor, whose domain was not the belt) — a prevented adoption at zero cost, per "the cheapest compute is compute not done".

Defects noted but immaterial: the dossier's "2.7× the shipped promotion path" factor (true only against the compile/in-flight promote; 1.4× against `add_body`), a b172 divisor transcription (132,061 vs 132,278/130,187), and shared-box timing wobble of +2–3%.
