Grade: gold

**Abstract.** The named gold experiment is done and holds. 2df1's row-set deletion wired into
`Session::step` collapses the flyable frame at 10,071 ladder bodies from 264.6 to 1.20 ms p50
(220×; regen 217×), flat in N — my own clean-tree flights extend it a decade past the author's
range: 1.28 ms p50 at 100,071, engine p99 4.47/max 4.86 ms, wire 26.3 KB/frame, served 88 rows.
Engine digest bit-identical with/without `--rows` at 71/1,071/10,071 bodies (both regen sets).
Display exactness 0–0.98% of drawn rows across five runs, 0 violations on my held-out seed 3
(822 rows, panel 0); transient bounded, not periodic ([32,32,3] at both 360 and 720 frames).
Cost to adopt: the patches (~60-line session wiring + policy port) plus 2df1's view change; the
page's client half stays unbuilt. Gain: the board's #1 gap moves from ~800 to >10⁵ flyable
bodies in-frame.

**Reasons.**
1. **Reproduced from a clean tree.** I applied `work/extra.patch` + `gather-rows.patch` +
   `rowset-wiring.patch` to pristine HEAD (base 0c68c9df) myself, rebuilt (40.6 s), and re-flew.
   My numbers match the author's and the runner's regen within load noise (b10000 260.7–264.6 ms,
   view share 0.997; r10000 1.20 ms p50, 32 hitches; collapse 217–220×). The same-day baselines
   reproduce the first author's arms (261.8 ms at 10⁴).
2. **Digest identity, all three sizes.** extra 0/1000/10000: identical digests with and without
   `--rows` (03abdbc9… at 10⁴) — the engine is untouched by the view deletion, as claimed
   (PRINCIPLES #3: views are derived, never evolved).
3. **Adversarial, beyond the author's domain.** (a) Held-out decade 10⁵ (author stopped at
   3×10⁴): frame p50 1.28 ms — the flat-in-N claim extends; worst hitch 686.8 ms at frame 6 ≈
   one fill cohort (6.8 µs/body), exactly the transient scaling the dossier named; 32 hitches,
   all early, all gather. (b) Held-out seed 3 + audit: p50 1.07 ms, audit 0/822 violations,
   panel 0. (c) 2× duration at 10⁴ (720 frames): hitch counts unchanged ([32,32,3]) — the
   transient saturates; it is bounded, not periodic.
4. **Predictions.** `predictions.md` (24 m) predates the decisive matrix (author's log 20 m;
   runner's regen later still). All eight predictions held; the two misses (readout run-average,
   the transient's existence) were disclosed, not hidden.
5. **Novelty.** The published flyable-frame page's open direction #1 was exactly this wiring;
   2df1 built the deletion but flew it only in an example harness (view.md). This run is the
   first measurement inside the frame loop the player runs. Not a repetition; the collapse, the
   in-frame audit, the digest identity and the transient/fill findings are new.
6. **Goal fit.** Board #1 (28 vs 10⁹ bodies in the flyable engine), 220× at 10⁴, adoptable as
   measured. #1 "the cheapest compute is compute not done": ~99% of readouts deleted at the
   pixel quantum; #28 "the view is an instrument".
7. **Instrument error found (my one correction, in the letter only).** The audit is *not*
   "charged to no channel": in the rows path the audit's full `gather_cached` runs between `t3`
   and the `dash.parts` call, so it lands in the **wire channel** and inside the timed frame
   (audit arms only: a10000 wire max 245.3 ms, p99 234, worst frame 271.7 ms; my seed-3 audit
   arm 237/234/268 ms — vs ≤0.15 ms wire max in every non-audit arm). No dossier number comes
   from audit-arm tails (only audit arms' p50 1.19/1.21 ms, which is true and unaffected), and
   the exactness counts are read-only, so no result changes — but any future reader of audit-arm
   JSONs must take tails from non-audit arms only. Corrected on the page.

**What the author missed.**
- The audit-charging error above (the code comment "never charged to a channel" contradicts the
  placement of the audit between `t3` and `dash.parts`).
- The transient's cure (spreading the fill's first dues) is asserted by mechanism, never
  measured — at 10⁵ the worst frame is already 687 ms, so the next rung needs that one-liner
  flown, not argued.
- One display mode (map, fitted zoom) flown, as the lens admits: belt zoom and the sky's near
  field (both known Θ(N) residues) are the honest next probes before any "10⁶ flyable" claim;
  my 10⁵ flight does not touch them.
- Minor: the fit section's "98.9% of readouts deleted" mixes the transient-contaminated run
  average with the steady figure; the stated raw numbers (368 avg, ~40 steady) are the honest
  pair.

Gold stands: reproduced twice independently (runner regen, this check), held-out predictions
held, the board's top bottleneck moves 220×, and the adoption is one code step plus the
already-named client half.
