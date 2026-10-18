Grade: silver

**Abstract.** The fit-compile key census on flown inputs, reproduced: the exact `ShapeKey` memo is dead on the whole fit path (hit 0.0001 over ~155k–180k cycle fits at N=3000/10⁴ coast; boundaries add no `from_state` calls — cycles 154,992 ≈ kicks 154,043 while boundaries ≈ kicks in count), the 17-bit shape class hits 0.978–0.992 at 1.2–1.7k classes that saturate in N, MB-scale memory. Checker extended the domain: N=3×10⁴ coast hit 0.9926 at 1,656 classes (1.11× classes for 3× bodies); burn N=3000 hit 0.9913; digest-neutral on five further `ladder_digest` cases. Not yet adoptable: the 12.33 µs compile's quadrature-vs-glue split is unmeasured and the serving key is a law decision. Cost: zero (measurement only).

## Reproduction

Applied `work/patch.diff` myself to a pristine tree at `d28f9352` (= the run's `base`), built pristine and census binaries. The runner's `regen.sh` (exit 0) and my own arms:

- Digest controls: pristine vs census-off vs census-on identical (`d2632de90255f5c10de9fd7372a3790d`, kicks 34537, encounters 934, contacts 0; `OFF_IDENTICAL`/`ON_IDENTICAL`, no panic). I extended the neutrality control to cases the author did not use: `belt crossing L10` (N=1000/3000 — including `4995f384…`, the same digest d399 reported) and `key mashing` (N=100/1000/3000): all bit-identical pristine vs census-on.
- The four census arms reproduce the dossier's hit rates to the 3rd–4th digit (N=0: 0.0017/0.9921/0.9924 exact/quant/shape; N=3000: 0.0001/0.9707/0.9921; N=10⁴: 0.0001/0.9348/0.9916; rtf 600: 0.0002/0.9355/0.9784). Cycle totals −1.6% vs the author's pass, inside the disclosed ±3% wall truncation; game-s differ likewise (43.2k vs 45k at N=0). Hit rates and class counts are the invariants, as the dossier states, and they hold. `quant_err=0` everywhere, confirmed.
- The cross-schedule artifact is real in `ctrl/on.err`: exact distinct 32,756 @2¹⁵ calls → 34,203 @2¹⁶ (≈95.6% recurrence inside `ladder_digest`'s re-flight of one case on 4 schedules). The published arms are single flights; no such recurrence. The multiple-testing guard is sound and honestly recorded.

## Predictions

`predictions.md` predates the dossier (mtimes: predictions 27 min before dossier, 24 before the patch teardown), contains a pre-registered kill criterion and both interpretation branches of P1. P1 failed exactly as pre-registered (exact hit 0.0001, not >0.5) and the failure branch ("boundaries do not re-enter from_state") is confirmed by an independent count argument the author left implicit: cycles ≈ kicks (1.006×) while boundary events ≈ kicks in count — had boundaries re-fitted, cycles would be ~2×. P2, P3, P4, P5 held. A failed prediction with a pre-registered interpretation is evidence of genuine pre-registration, not a defect.

## Attack (three adversarial cases, one outside the tested range)

1. **N=30000 coast rtf 1800** (3× the author's maximum, the next decade): exact 0.0001 (224,091 distinct / 224,111), shape hit **0.9926 at 1,656 classes** — 1.11× classes for 3× bodies. Saturation and the class-level claim hold at the next decade. The quant cell hit falls to 0.861 (31,261 ≈ 1.04 cells/body) — consistent with per-body cells, but below the dossier's "0.934–0.9921" range; the claim never rests on the quant level, and I corrected the page to say the quant hit falls with N.
2. **Burn N=3000 rtf 1800** (a regime the author never censused; passages 3,442 vs 1,649 coast): exact 0.0002, shape hit 0.9913 at 1,324 classes. Holds under player thrust.
3. **Digest neutrality on five untested cases** (above): identical.

The domain still ends at the coast/burn birth-program belt; a stirred or driven belt (the author's own named limit) and the strong-branch shape key (this census's weak-branch 17-bit class is not what strong-field bodies would share) remain unmeasured — the page says so.

## Novelty

`lab/wiki/read-stream.md` open direction 2 (d399, current best) names exactly this gate: "sharing rate on flown fit keys unmeasured". Memo.rs's standing law (taste log, 5 October; H0213/H0216 era) killed the exact memo on kicks only, and warned the quantized cell changes orbits; 3570 measured boundary rebinds as no-ops at the kick site. New here: the three-level census at `from_state` over ALL fit entries, the class-level sharing rate (99.2%) with its saturating class count and byte price, and the cross-schedule instrument artifact. Not a repetition: it extends a known law to a new site and prices the previously unmeasured design space.

## The page

Faithful overall; two overstatements corrected in place: (i) "hits 0.9917–0.9924" omitted the pre-registered rtf-600 arm (0.9784) — now "0.978–0.978–0.992 across paces"; (ii) "3.04× bodies" is a typo for 3.3× (10,028/3,028). Added checker brackets: my domain extensions (N=3×10⁴, burn, five digest cases) and the cycles≈kicks boundary cross-check.

## Goal fit

Board's kick bottleneck (75–160 µs vs ~50 ns floor); read-stream direction 2's named gate. PRINCIPLES 3 ("Compute only surprises… Nothing is evolved that can be derived when looked at") — a 99.2%-repeated quadrature is derivable when looked at; and 19's warning is respected by killing the exact-level cache rather than caching harder. Measurement only; no gate touched, no law changed; the census is print-only and digest-neutral on six cases.

## Why silver, not gold
Faithful overall; two overstatements corrected in place: (i) "hits 0.9917–0.9924" omitted the pre-registered rtf-600 arm (0.9784) — now "0.978–0.992 across paces"; (ii) "3.04× bodies" is a typo for 3.3× (10,028/3,028). Added checker brackets: my domain extensions (N=3×10⁴, burn, five digest cases) and the cycles≈kicks boundary cross-check.
Everything reproduces and the predictions held where pre-registered, but nothing is adoptable within one step: the delete's size is unmeasured (the 12.33 µs compile could be mostly per-key glue, in which case the 99.2% hit deletes little — the dossier names this honestly), and serving the shape needs a law decision (quantized key = memo.rs's known 2⁻¹¹-period change; `from_shape(exact, quantized)` exactness unmeasured). The premise-is-wrong prong is weak here because memo.rs had already killed the exact memo on kicks; this run extends the kill, it does not overturn a live premise.

**The one experiment that would make it gold:** split the 12.33 µs `compile` on the flown-key corpus into `OrbitShape::bound` (shared quadrature, servable from the 99.2% class cache) vs per-key glue, paired with the cheapest exactness probe of `Orbit::from_shape(exact key, quantized shape)` on the belt corpus. If the quadrature owns most of the compile, the delete is priced, bit-identity or a measured law change is the certificate, and adoption is one step.

## What the author missed

- The patch's `Print` drop-guard is a const-initialized thread-local: its destructor never runs, so the `FITCENSUS end` / `top10` lines are dead code (no output in any log). Harmless — the totals come from `nladder`'s explicit call — but anyone reusing the census in a multi-threaded harness gets no per-thread totals.
- The quant-cell hit falls with N (0.971 @3k → 0.936 @10⁴ → 0.861 @3×10⁴); the dossier's range reads as if stable. Corrected on the page.
- The strongest evidence for "boundaries never re-enter" (cycles ≈ kicks, 1.006×, with boundaries ≈ kicks in count) was available in their own logs and left implicit; the page now carries it.
- The strong-branch shape key: the census only ever exercises the weak 17-bit class on the belt; a strong-field sharing census (one high-e or close-in arm) would close the representation question the class cache actually needs.
