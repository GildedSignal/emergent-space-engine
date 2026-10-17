# Dossier — 20261016-2327-second-20261016-2229-scout-ab3d-1d54

## Claim

At the true shipped operating point — the belt branch's 49-m ships, `near` = 68 root units =
6.713×10⁻⁷ AU (`scenario.rs:344` ships `Scalar::raw(34, -10)` in doll-0 units; the silver run's
12,850-km radii were a 2¹⁸ misread) — the two-stage angular certificate is sound and cheap on a
fully regenerable record: **zero missed true hits in all 32 truth-checked scenes, every seed,
every horizon**; the answer walk closes at **S(10⁵) = 2.1–2.2 ms** with the shipped 4.2-µs
readout (~190× under the 418-ms latch, under the 6-ms bar); the e > 0.4 querent unsoundness the
checker found is **fixed by an exact closed-form margin** (max|ν−M| at its stationary point,
valid for every e < 1), which the old clamped table provably misses on crafted co-located hits
at e = 0.6/0.8/0.95 (miss_old = 1 each, miss_new = 0); the truth at the shipped point is
**ZERO encounters per scan** — 3999's ZERO is exact, not a frozen log — the bar holds for
querents up to e ≈ 0.6 (5.9 ms) and dies by e = 0.95 (27.7 ms), and 10⁶ is marginal:
6.9 ms with the λ-index and a 0.5-µs readout, 15% over the bar.

## Bottleneck

The board's furthest gap (bodies 28 → 10⁹), the scan-queue page's latch term: the in-belt
answer walk (S = (N−314)×4.2 µs = 418 ms at 10⁵). This run converts the silver's
checker-measured correction into the run's own regenerable record (`falsifier2.rs`,
`sh regen.sh`, 14 s) — the named gold experiment, done.

## Evidence

All numbers from `./falsifier2` (`run.jsonl`, 38 rows; x86 shared box, orders of magnitude;
scene rows bit-deterministic across two runs — verified; only timing cells vary).

- **Constants, code-derived:** root unit = AU/101_300_000 = 1,476.9 m (`scenario.rs::AU`; the
  Moon's 260,000-root periapsis = 383,990 m confirms the scale), ship radius 34·2⁻¹⁰ root
  = 49.06 m, `near` = 2¹⁰·(r_a+r_b) = 68 root = 6.7127×10⁻⁷ AU (row 1).
- **The closed-form margin (the fix):** cos ν* = ((1−e²)^{3/4}−1)/e, margin = ν*−M*, exact
  for any e < 1; margin(0.07)=0.1401, (0.4)=0.8160, (0.6)=**1.2615** (the checker's value,
  4 digits), (0.8)=1.7861, (0.95)=2.3774. Cross-check against a dense same-e grid on
  (0, 0.99]: closed − grid ∈ [+1.0×10⁻⁹, +5.4×10⁻⁷] — the closed form dominates everywhere
  (K0 holds; the grid only ever undershoots the true sup).
- **Soundness (K1, all 32 scenes checked — the silver checked seed 1 only):** miss = 0
  everywhere. Natural scenes (22 at 10⁵ over seeds 1, 2, 3 + held-out 5, 7, three querents,
  two horizons; 2 at 10⁶ seeds 1 + 7): **truth_hits = 0 in every one** — 3999's ZERO
  encounters is exact at the shipped point, and their nearest-candidate distances
  (2.1×10⁶–5.7×10⁷ × reach ≈ 0.02–0.6 AU vs a 100-km near) now reconcile in order too.
  Controls: the true-scale formation (500 bodies within near/2 of the querent, constructed
  exactly) keeps 500/500; the counterfactual 0.176-AU belt holds 550 hits (0.55%·N — where
  the silver's "0.53%·N truth wall" lived, one labeled row, not the shipped point).
- **The e > 0.4 fix is load-bearing, not decorative:** co-located adversarial rows (a belt
  body at periapsis placed exactly on a max-margin-phase querent, d0 = 0, a guaranteed truth
  hit): e = 0.6/0.8/0.95 → truth 1, miss 0 (exact margin), **miss_old_margin 1** (the
  silver's clamped table drops each one). Querent-e cost scenes: keep1 46.6% (e=0.6) /
  86.7% (e=0.95), keep2_series 0.80% / 5.5%.
- **Keep fractions at the true point:** stage 1: 6.1–6.5% (player-like e=0.01), 9.9–17.0%
  (belt querent), 30.7–31.3% (belt e=0.39); stage 2 series: 0.27–0.42% (long h),
  0.12–0.16% (short h); Newton: 0.15–0.29% / 0.005–0.012%. At 10⁶ (seeds 1, 7): keep1
  10.88/10.87%, keep2_series 0.319/0.314% — held-out within 0.2%.
- **Costs (hot loops, 10⁶ bodies):** stage 1 = 2.8–3.5 ns a candidate; stage 2 = 48.6–48.8 ns
  (series), 189–192 ns (Newton, now early-exit); K3 holds.
- **Composed S (this run's own cells):** 10⁵ wired (O(N) pass + series + 4.2-µs exact
  readout on survivors) **2.15 ms < 6 ms bar**; with a 0.5-µs readout 0.97 ms. 10⁶: wired
  21.5 ms, cheap-readout 9.7 ms, **λ-index + cheap readout 6.89 ms — 15% over the bar,
  marginal** (the silver's 4.8 ms composed its low-band series cost; the checker's 6.4 ms
  is confirmed). Querent-e at 10⁵ wired: e=0.6 → **5.89 ms (bar survives, barely)**;
  e=0.95 → 27.7 ms (dead).

Reproduce: `cd lab/results/20261016-2327-second-20261016-2229-scout-ab3d-1d54 && sh regen.sh`
(14 s; recompiles, reruns, and machine-checks the invariants: 38 rows, 0 misses, the three
adversarial miss_old ≥ 1, K0 ≥ −10⁻⁶, 500/500 formation, margin(0.6) = 1.2615).

## Predictions

`predictions.md` was written before any run. Held: truth ≈ 0 (exactly 0 everywhere — and the
silver's "0–1 per scan" was a self-pair artifact, the querent reading itself at d0 = 0; now
excluded as the shipped scan does); keep1 bands (6.1–6.5 in 5–15; 30.7–31.3 in 25–38);
S(10⁵) 2.15 in 1.4–2.6; 10⁶ index 6.89 in 6–7 (marginal over, as predicted); costs within
bands (Newton below, early-exit); soundness and the adversarial miss_old ≥ 1 exactly; e=0.6
5.89 in 4.5–6.5; held-out seeds inside ±30% (belt keep1 seed 5 vs 1: −31%, at the edge).
Failed, honestly: **short-h series keep was 6–30× above my band (0.12% vs 0.005–0.02%)** —
I priced the window as |w|h-dominated, which the Newton keep (0.005–0.012%) confirms; the
series adds its per-e tail slack, and mid-e belt bodies carry it. Cost-only, soundness
untouched; the composed S at short h is 0.35 ms, irrelevant to any verdict.

Disclosure: the record is from the complete program after two replica bugs found and fixed in
a smoke run (the formation's radius inversion `a(1−e²)/(1+e·cosν)`; the self-pair exclusion)
and after adding two composed querent-e rows; no scene construction changed after the
decisive run, and scene rows are bit-deterministic across runs. The counterfactual row's 550
vs the silver's 551 is the self-pair removal, and its keep1 0.1824 vs 0.1838 is the exact
margin replacing the bin-top table.

## What would make it wrong

- The replica is planar, unperturbed float Kepler between epochs (λ linear; true under the
  shipped key between events, since every kick re-anchors); the shipped integer window's
  residual/rounding widenings are still idealized — wiring must carry them or the cut eats a
  hit (unchanged from the silver; a wiring question, not a measurement one).
- The 10⁶ "marginal" verdict rides on the unbuilt λ-index being free and the 0.5-µs
  closed-form readout (3999's named price, kick-jet-cd6e-corroborated); if the index's
  maintenance costs ~1 ms a scan, 10⁶ stays over. The bar's honest 10⁶ status: open, one
  experiment away.
- Querents above e ≈ 0.7 at 10⁵ are outside the bar on this mechanism alone (stage-1 margin
  1.3–2.4 rad keeps 47–87%); the domain boundary is measured, not hidden.
- The capture half (0.046–0.111 µs/body) and the reuse walk (7343) are untouched; they bind
  after the answer half closes.

## Cost of adopting, and fit

One additive filter in front of `Scan::compute`'s readout loop, the margins computed exactly
at registration (10 flops, cheaper than a table lookup), the per-e tail table beside
`radial.rs`'s hulls — no law change, outcomes unchanged by construction (the certificate only
drops provably-far candidates; floats widened, the exact integer predicate decides). The
e > 0.4 fix costs nothing: the closed form replaces the table entirely. PRINCIPLES #3
"compute only surprises" (the wired cut reads 0.3% of the belt at 10⁵), #19 "the right
representation always just feels right" (the anomaly margin is a stationary point in closed
form — the table was the banda­id), #30 "navigation, knowledge and dynamics those need to be
perfect" (sound for every querent the player can fly, e < 1).

## The lens

The second-author lens sees a record that regenerates and a claim whose numbers all moved
one way (toward the silver's checker, as they should); what it may miss is everything outside
the replica's frame: the integer widenings, the index's maintenance cost, and the GR doll's
apsidal advance (a precessing ω breaks a static ω registration — the margin must renew with
the doll's own precession; the silver's lens named it, still unpriced). The deeper risk is
shared-frame agreement: my record and the checker's reruns use the same replica, so they are
not independent on the replica's fidelity to the shipped integer scan — the wiring step (the
only place that risk dies) is not taken here.
