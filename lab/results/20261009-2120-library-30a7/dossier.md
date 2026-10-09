# dossier.md — run 20261009-2120-library-30a7 (library lens)

**Claim.** Five of Julien's own practitioners answer the board's top scaling
risk (candidate pairs grow O(N²); work must track real encounters), and the
cheapest of their tests kills a live sub-claim of the r8 "next" note: naive
continued-fraction/beat prediction of a pair's next close conjunction misses
~90% of them (recall 0.067 at e ≥ 0.25) because the conjunction-phase drift is
~2.5–12× the close-set window — "pay once per element change" is falsified in
the cleanest non-circular case; the predictor must be drift-corrected or
carry a ≥3× skin.

**Bottleneck.** Encounters at N (board, 5 Oct: q-candidate-degree + the 6 Oct
co-orbital gold). Expected gain: deletes the pair list as an object (1.7M
candidate pairs vs 427 real encounters on belt 0, board 30 Sep) and prevents
a wrong predictor from being built into the encounters design.

**Evidence.** Readwise export cached (9 pages, `readwise-pages/`, 4.3 MB;
770 books, 4,580 highlights indexed to `highlights.tsv`). Reproduce, each
< 60 s: `bash fetch_readwise.sh` (needs READWISE_TOKEN); `python3 cf_probe.py`
(2.6 s; writes `cf_probe_out.json`); quote check:
`grep -c -F "skewed bets" highlights.tsv` → 1 (all 7 quote anchors hit, P5).

## The five lessons (each changes a decision)

1. **Question the requirement, then delete — never accelerate it.**
   "Step one should be to question the requirements… Make them less wrong and
   dumb, because all requirements are somewhat wrong and dumb. And then
   delete, delete, delete." — Walter Isaacson, *Elon Musk* (with: "Always wait
   until the end of designing a process… before you introduce automation.").
   Tesla's algorithm puts deletion before speed. Change: "enumerate candidate
   pairs cheaply" is the dumb requirement — the pair list (4,000× the real
   events) never exists; envelopes + phase rank only. Test: belt rung counts
   materialized pairs/orbit → 0 outside windows.
2. **Invert: prove absence, don't search presence.** "Problems frequently get
   easier… to solve if you turn around in reverse" / "Invert, always invert."
   — Munger, via Farnam Street highlights. Disjointness proofs compose per
   group and amortize; searches re-pay per pair per orbit. Change: tier-1 is a
   certificate of no-event, paid once while envelopes are disjoint. Test:
   cold-belt tier-1 work/orbit decays to ~0 with misses 0 (scan stays flat).
3. **Skewed bets: rent is constant, misses are ruin.** "…“skewed bets,”… I try
   to benefit from rare events… the rarer the event, the more undervalued it
   will be." — Taleb, *Fooled by Randomness*. Crisis hunters pay frequent
   small losses for rare large payoffs; sizing by average rate is the ruin.
   Change: tier-1 is rent, a constant per body per orbit; no miss-for-rent
   trade (the "Wide" tightening that missed 23% at e 0.7–0.9 is forbidden).
   Test: adversarial belt with planted deep flybys — rent flat in N, misses 0.
4. **Barbell: two extreme tiers, no adaptive middle.** "…so is the barbell a
   domestication, not an elimination, of uncertainty." — Taleb, *Antifragile*.
   Fragility hides in the middle (medium cost, medium fidelity, both failure
   modes). Already adopted for GPU/CPU regions (H0162). Change: exactly two
   tiers (ultra-cheap everywhere + ultra-exact once); dimensionless numbers
   pick regimes, sliders refused at review. Test: mechanism count on the 6 Oct
   formation case == 2.
5. **Firemen: events have call times — but my probe corrects the fantasy.**
   "We are made to live like firemen, with downtime… between calls." — Taleb,
   *Fooled by Randomness*. Idle capacity converts to bursts; conjunction times
   are computable ahead (idle-time compute, principle 17). Change: the
   next-conjunction predictor is a slack-skin artifact — drift-corrected or
   widened ≥3×, else recall 0.067 (probe). Test: `cf_probe.py` (3 s), then the
   same probe on the repo's belt (J2 adds frequencies; expect worse).

**Predictions.** `predictions.md`, written before the probe. P1 FAIL (median
f_close 0.067 vs ≥ 0.8), P2 FAIL (best-index CF hit 7.5% vs ≥ 65%), P3 FAIL in
direction (near-commensurable seeds scored higher, 0.133 vs 0.033; n = 3, no
claim either way), P4 PASS trivially (0.034 < 0.1; both sides tiny), P5 PASS
(7/7 quote anchors verbatim in the cache). The kills are the result: the naive
CF claim and the pure beat-arithmetic predictor both die; low-e belts are
phase-degenerate (miss ≈ |a2−1| for every conjunction), so "close" is only
phase-selected where e is high — exactly where the drift is worst.

**What would make it wrong.** The probe is a 2-body coplanar model with zero
apsidal precession and K = 600 conjunctions; a real belt's J2 precession adds
frequencies, which can only make linear/CF prediction worse, but a
drift-corrected two-frequency generator could restore "pay once per element
change" — then lessons 1–4 stand, lesson 5's correction is withdrawn. The
lessons are analogies until their cheapest tests run on the rung's own data.

**Cost of adopting.** Nothing to build: three review rules (no pair list; no
middle tier; no miss-for-rent trades) for the encounters design, plus one
correction to the r8 v3/v4 plan (predictor needs drift correction or a ≥3×
skin). All tests reuse the existing belt rung harness.

**Fit with PRINCIPLES.** Lesson 1 is "the cheapest compute is compute not
done" (P1); lesson 2 is "no work for no reason, so no ticks" (P14) —
certificates amortize to zero when nothing changes; lesson 3 is "errors never
compound" (P13) with misses as the compounding side; lesson 5 is "use idle
time to compute ahead" (P17), now with its measured boundary.

**The lens.** Taleb dominates (3 of 5): his library over-weights him, so
Kelly/Skunk-Works-style engineering discipline is under-represented; the
allocator already mined barbell/inversion for scheduling (H0158-era
`work-allocation-principles.md`), so novelty here is the *application* to
encounters, not the patterns; and an earlier wave logged Musk's algorithm as
absent from the library — the Isaacson highlights arrived since, which is why
lesson 1 could finally be quoted verbatim.

**Grade suggested:** silver — one reproduced negative result (the CF
predictor kill) plus five decision rules, each one belt-rung test from gold.
