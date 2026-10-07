Working...
Check complete. Verdict written to `lab/results/20261007-1801-second-20261007-1646-autoresearch-a191-18df/check.md`; tree restored clean at `a838a28`; only `check.md` added.

**Grade: silver.**

What I did (45 min, clean tree, my own binaries):

- **Reproduced everything, exactly.** Applied `scope-free.patch` (clean, zero `prof` refs, `universe.rs` deletion byte-identical to the silver run's); my own interleaved A/B on their four scenes plus my adversarial m4 and rtf1000: made −18…−21 %, leavers −5.5…−8.5 %, both digests bit-identical everywhere, `refused` 0; 18 suites, 104/0/1 tests. Cadence ladder: kicks 949→507→287→173, per-kick flat 28.5→29.6 µs, work ×0.54/×0.30/×0.16, exponent 0.98–1.04. B13: 60/64→41/64→15/64, worst 2.12e-2→8.47e-2→3.39e-1 (×4.00/halving). Jacobi ×3.5 with kicks exactly halved. `predictions.md` (18:03:36) precedes all decisive data (18:06:39+).
- **Attacked.** Beyond-ladder cadence (l2=8 linear, l2=3 breaks flat per-kick, +11–18 %); stash-verified the jacobi step-7 panic is pre-existing at HEAD; digest-sensitivity check (equality is not vacuous); found their m24 "−34.3 %" pair was load-contaminated (base 43.3 µs vs 35.1 in a clean pair; my clean m24 = −19.4 %, in family) — disclosed by the author but misread as a super-gain.
- **Novelty.** The adoptable artifact and engine-side cadence pricing have no H entry; `q-cadence-7d0d` (5 Oct, silver) measured the complementary behaviour frontier offline and is never cited — the main miss, since per-body Hill-gated cadence is exactly where this table points.
- **Not gold:** the deletion is 1.1–1.2× per kick and the cadence table prices the integrator's `q-cadence` door without opening it — at l2=4 work falls only 6.3× while B13 collapses to 15/64, so no 10× exists at held behaviour. The one gold experiment: a per-body, Hill-gated cadence measured on the plane holding B13/B12-redesigned.
