Grade: silver

**Abstract.** The belt kick is decomposed in wall time on shipped main (46.3-52.9 µs;
`bind_surface` 45-59%, `secondaries` 13.5%, the quadrature only ~26% of the fit), and the
per-event sources rebuild is measured 2.66-8.2× redundant at its `(doll, tick)` key (63.9-89.9%
of calls shared): read-stream's direction 1 answered — ticks are already shared, the cache is
real but buys only ~8-10% of the kick. Reproduced: regen exit 0, parity bit-identical, census
84,254/31,652 exact, kick 44-53 µs, compile 4.4 µs, `div_word` 8×. My adversarial arms
strengthen it (24-28× sharing at N=10⁵ and rtf 100; zero stale cache keys in 292k calls).
Not gold: 5ade had already decomposed the wave kick and killed a source memo on the spread
belt (0.029) — a regime this run never flew; no 10× moved.

**Reasons.**
- **Reproduction complete.** The runner's regen exited 0 (parity bit-identical on
  `ladder_digest` N=3000); my own re-flights on a fresh apply of `work/patch.diff` match:
  main arm kick 44.0-45.2 µs, FIT 19.8-20.5 µs (45%), secondaries 6.2 µs, census 84,254 at
  31,651-31,652 keys (63.9% at ≥2, to the digit), bind bench 17.3-17.7 µs, kickfloor micro
  wide 22.3 / `div_word` 2.8 ns, compile medians 4.4 µs (belt) / 13.6 µs (strong). The FIT
  stage and the standalone bind bench agree (19.8-20.5 vs 17.3; 25.6-30.4 vs 28.0) — two
  independent measurements of one operation, the decomposition's best internal check.
  `secondaries` = 6.25 µs ≈ 3 hot planet-key readouts (~2 µs each, kick-jet's own 1.9-3.1 µs
  hot read) — consistent. Code claims verified: `weak_quad` uses `div_word` (orbit.rs:382);
  `fast_quad` pays four wide u128 divisions per node (orbit.rs:429-433) where `n >> 64 < d`
  holds outside absurdly deep field; `num.rs` states the same-bits contract.
- **Adversarial (mine), all strengthen, none break:** (1) N=10⁵, a decade-scale jump: census
  35,997 at 1,288 keys = 27.9× (98.6% shared); FIT/WH-kick = 47%; note the clock comb does
  not fire in 20 s wall there (WH kicks only) — the "kick (clock)" decomposition's domain is
  the lighter arms. (2) rtf 100, below the tested range: 24× sharing (99.2%). (3) The run's
  own named unknown — cache invalidation — probed directly with a content hash of the
  returned `Vec<Secondary>` per normalized `(doll, tick, except)` key: **0 of 292,864 calls
  across three arms had changed content at a repeated key.** The cache would have been
  bit-identical everywhere flown. (My probe is print-only, prof-gated, tree restored.)
- **Predictions:** honestly reported. P1 half-wrong (secondaries 13.5% not ≥35%; FIT largest
  but 45-59%), P2 half-wrong/half-overshot (steady-alone refuted at 63.9%; the ≥8 tail held
  at 62.6-88%), P3 wrong low (17.3-28.0 vs 8-15 µs), P4 held. `predictions.md` predates the
  dossier and the final patch export; the flights' own outputs were overwritten by regen, so
  log-order proof is partial — mtimes are consistent.
- **Novelty (the gold blocker).** The census with the drain answer is new and load-bearing
  (d959's direction 1 named it "unflown"). But the dossier's headline "priced from the inside
  on shipped main for the first time" overstates: 5ade (16 Oct, kick-jet) decomposed the wave
  kick — fit 41%, sources 23%, tau pair 15%; a765 measured the rebind at 84-87% of its arm;
  c4d3 (15 Oct) timed the compile at true belt keys at the same 4.4-4.5 µs p50. What is
  genuinely new here: the fit's internal split (quadrature ~26% of the fit — the compile is
  not the fit's mass, reframing b063/a765's "refit is the kick"), the `(doll,tick)` census,
  and `div_word`-in-`fast_quad` (micro, strong-field only — c914's divq 1.04× was the belt
  path, which already uses `div_word`).
- **Goal fit.** The board's kick row, directly. PRINCIPLES #1 ("the cheapest compute is
  compute not done") and #3 ("compute only surprises" — an unchanged field re-read is not a
  surprise). No 10× moved, nothing deleted, and the premise corrections (b063/a765's refit
  share; direction 1 as the kick's cure) are opened, not resolved on one named arm.
- **Page.** Faithful on the evidence; corrected in place where it overstated by omission:
  direction 1 now carries the regime qualifier and 5ade's kill; Contradictions gains 5ade's
  0.029 and a765's 84-87%; my staleness result is marked checker's, not the author's.

**The one experiment to gold.** Implement the `(doll, tick, except-normalized)` cache (~30
lines) and fly it digest-identically on both regimes — the plane's steady arm and the
wave/birth-crest belt (5ade's spread-belt harness) — measuring the wall gain in each. Either
it deletes 62-89% of `secondaries` in the wave too (5ade's memo was keyed wrong; direction 1
lives, ~8-10% of the kick plus the frame's read stream), or the lever is plane-steady-only
and direction 1 dies for the 10⁹ ledger. One flight decides it, and adjudicates the
b063/a765 84-89% tension on a shared arm.

**What the author missed.**
- 5ade's source-memo kill (0.029, spread belt) on the same lever in the wave regime — the
  census answers direction 1 only for the plane's steady/crest flight, which is not the
  regime the 10⁹ ledger's 23 µs is about. Unengaged in dossier and page (page now corrected).
- a765 and c4d3 as priors; "for the first time" does not survive them.
- The invalidation rate, named unmeasured, was measurable with the run's own instrument
  style (content hash per key): zero stale keys in 292k calls. This strengthens adoption and
  should have been in the dossier.
- The cache key needs `except` normalized (planet-self events pass `except = j`; step.rs:410,
  observe.rs:145) — trivial, but unstated, and a raw `(d, t)` key would serve a planet its
  own field.
- "Re-runs move the stage timings ≤ 5%" holds for the main arm but not the held-out arm's
  FIT/readout/secondaries (FIT 30.4 → 25.6 µs, −16%, in the runner's regen); the census and
  the kick clock are the stable numbers. Also 48.4 secondaries calls/frame is 0.94/event, not
  0.97 (89,923 events / 1,740 frames).
