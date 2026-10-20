Grade: gold

**Abstract.** Claim: the 26%-vs-84-87% compile-share contradiction dissolves into
denominator (from_state stages vs whole `Work::rebind` wall) × scene (population e),
and the term neither run measured — rebind scaffolding outside `from_state` — is the
largest measured term on both walls. Reproduced in a clean tree (patch applied by me,
fresh build): bench wall 0.366-0.430, stages 0.845-0.866 (a765's stored 0.894/0.882/0.876
verified from its branch: its "rebind mean" column is the from_state total); belt wall
0.254-0.266, stages 0.438-0.452; scaffolding 40-57%; bench counters and digests
bit-identical across author/runner/checker2. Four fresh adversarial arms (seed 1234,
seconds 30, rtf 300, belt 3×10⁴ burn) hold every cell; the burn belt keeps compile cheap
(8.8 µs/mint), so scene = population, not activity. Adoption: nothing in code
(print-only); re-scope both citations, re-aim the kick row at the scaffolding.

**Reasons.**

1. **Reproduction (clean tree, my own runs).** Applied `work/patch.diff` myself at base
   30860cea, rebuilt, reran regen.sh end to end. Every dossier number lands inside the
   stated spread: bench compile/wall 0.427/0.395/0.366 (repeat 0.430) vs dossier
   0.413/0.387/0.367 (0.427); stages 0.866/0.845/0.852 (0.865) vs 0.853/0.842/0.848
   (0.861); compile 53-65 µs/mint vs 55-74; fit_key 4.3-4.5 and tail 5.2-5.6 flat; belt
   wall 0.264/0.257, stages 0.451/0.442, scaffolding 41.4/41.8%. Bench counters
   (mints/rebinds/kicks/hist) bit-identical across the author's, the runner's and my
   runs; belt counter drift is the disclosed frame-clock binding. Digests bit-identical
   (e622722…, replay 58127f4c…): the census does not perturb the bench.
2. **The crux verified at the source.** a765's stored table (its branch): compile
   63.92/54.87/52.78 µs of fit+compile+tail 71.49/62.23/60.25 = 0.894/0.882/0.876 — its
   "rebind mean" column IS the from_state total (my fs_total: 62.8-75.3 µs), so a765's
   85-90% was compile/of-stages all along, exactly the re-scoping aa42 argues. 7fd3's
   stored belt 0.265/0.259 reproduced. The adjudication is not an interpretation: the
   same counters, two denominators, both reproduced. mints = a765's "calls" (1467/1737/
   1349) — counters deterministic across runs, days and instruments.
3. **Predictions.** predictions.md (17:33:21) predates the author's runs (out/ 17:38,
   dossier 17:39) and the runner's regen (17:42). The fork was pre-registered with all
   three exits; the mixed branch fired inside its band (0.366-0.430 ∈ (0.35, 0.55)),
   the stage band [0.80, 0.92] held on every seed, and P3/P4 held; P1/P2/P5 killed and
   reported as killed — honest kills of pre-registered criteria (the fork's two exits
   were the prior runs' supersession stories, not the author's mechanism, and the
   author's mechanism predictions held). This is the diagnosis discipline PRINCIPLES
   H0183 asks for, not a failed prediction papered over.
4. **Attack (4 arms, 2 outside the author's swept numbers).** Bench seed 1234, seed 1
   --seconds 30 (3× duration), seed 1 rtf 300 (next pace decade): wall 0.405-0.409,
   stage 0.844-0.846, compile 54-56 µs/mint, scaffolding 51.7-52.0% — the bench cell
   is robust in seed, duration and pace (checker1's rtf-30 edge at 0.55 is one-sided).
   Belt 3×10⁴ burn: wall 0.297, stage 0.494, compile 8.8 µs/mint, scaffolding 39.9% —
   a third scene stays in the belt's cell, refining "scene" to the population's e
   (the plane's strong-e tail), not the activity. Nothing broke; folded into the page.
5. **Novelty.** The live page named this "the named experiment to gold" with the
   contradiction unresolved (scene/era/instrument hypotheses — none of which is the
   answer). No prior run measured the outside-from_state term: a765 and d4f1's
   0.85-0.90 family all stop at from_state's edge; 7fd3 folded the term into "fit
   74%". First measurement, and it reverses the lever ranking: fit_key is 3-15% of
   walls, the scaffolding 35-57% — 7fd3's "the kick's next 10× is the fit" is wrong
   as stated, and a765's "compile-bound rebind" holds only in-stage. A premise shown
   wrong; adoptable within one step (nothing to merge).
6. **Goal fit.** Board kick row (75-160 µs vs 50 ns floor). "Measure before claiming";
   "a failed expectation is not automatically a failed method: diagnose which one
   broke (H0183)"; "the right question, then the representation" — the right question
   was "share of what, on which population". Print-only, digests untouched.

**Page.** Faithful to the evidence; I corrected one overstatement in place: the
scaffolding was called "second-largest on the belt" while the run's own numbers make
it larger than the compile there too (11.5-12.7 vs 7.3-8.2 µs) — now "largest measured
term on BOTH walls" — and folded my four arms into the domain sentence. Not a
three-gold closure: 7fd3 stands silver; this settles the gate its checker named.

**What the author missed.**

- The belt-wall ranking slip above (dossier understates: "bigger than the compile on
  the bench wall" — it is bigger on the belt wall too; conservative direction).
- mints (1467) > rebinds (1333): fs_ms sums over all mints, so fs/rebinds
  over-attributes from_state time into rebinds and *understates* the scaffolding —
  the 41-57% band is a floor, unremarked.
- The patch is not strictly print-only: it drops `machine_after` and `wall_seconds`
  from the bench JSON (non-identity metadata; refused/replay_digest/digest intact and
  bit-identical — not the ff42 sin, but "print-only" overclaims by two fields).
- The burn belt was listed unmeasured; it stays in the belt cell (scene = population
  e, not activity) — a free sharpening the run could have had.
- fit_key's flat band is 4.0-5.9, not 4.2-5.9 (the author's own belt rows read
  4.01/4.03 under regen load); trivial, the flatness claim is unaffected.
- The scaffolding internals remain unpriced (the author names this): decode/turn/
  residual vs word-retry vs τ-reads/retirement — one timer layer, the next run's
  first hour, and the natural gold follow-up on the re-aimed lever.
