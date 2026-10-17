# Predictions (written before the decisive runs)

The question the checker named for gold: the 0552 dossier prices the K=1,000 frame (p99 ≈ 45-52 ms,
68/600 frames over the 12-ms budget) only in aggregate (stage means + ns/call). Which channel owns
the worst frames — the scan (capture + held answers, the observer half) or the comb (the item
pipeline: kicks, boundaries, fits — 1,000 ships born on one tick at one period)? That split decides
the fix ranking the dossier proposes (a phase axis for the observer vs cadence for the comb).

Instrument: per-frame top-level prof stages (channels: scan = ENCOUNTERS+SCANS; comb =
REKEY+APPLY+REQUEUE+PROCESS+TAKE_DUE+HANDOUT; nested FIT/ROOT/H_*/P_* mirrors are detail only),
decomposed for every late frame, aggregated over all / over-budget / worst-1% frames, plus the 12
worst frames individually. Smoke (form=200, untuned): channels close to 98.4% of wall (unaccounted
1.6%); over frames there 99.7% comb, 0.3% scan; the scan channel 100% inside under-budget frames.

Cases I have NOT tuned on (form=1000 extra=0 and form=3000 extra=10⁴, seeds 1 and 2, not yet run
with this instrument):

1. **The over-budget frames at K=1,000 are comb-owned, not scan-owned.** Prediction: in the
   over-budget frames the comb channel carries ≥ 80% of wall and the scan channel ≤ 10%, on both
   seeds; the single worst frame is ≥ 80% comb (a wave of in-phase kick items resolved inside one
   frame, the first item always running and pull_ships bursts being outside the budget's control —
   universe.rs's own comment). The dossier's P5 mechanism ("a 4.5-ms answer does not fit idle time's
   margin and SCAN_BACKLOG then forces it into a frame") is wrong at K=1,000: SCAN_BACKLOG (2048)
   never fires (held_max ≈ 1); instead the answers are drained inside quiet frames' idle room and
   inflate those frames (0.3 → ~5 ms), which stay under budget.
2. **The scan channel lands in under-budget frames.** ≥ 80% of total scan-channel ns (capture +
   answers) occurs in frames that end ≤ 12 ms, at both seeds; the mean late-frame split is comb
   ≈ 80-90%, scan ≈ 8-15%.
3. **The answers ride the quiet frames, one at a time** (ans ≤ 1 in ≥ 90% of frames that carry any
   answer; each answer 3-5 ms at K=1,000), so the observer half lifts the mean and the crowd law
   (candidates 1.00/ship) but not the p99.
4. **Seed 2 holds the class**: 87/87 scans bail, candidates ≈ 32 + 1.00·K, over frames ≥ 80% comb.
5. **At form=3,000 beside the 10⁴ belt (the ruin case, p99 ≈ 140-160 ms)** the comb still owns the
   worst frames (≥ 60% of wall), but the scan channel's share rises above its K=1,000 share
   (answers grow with the walk: ~9.5k binding_at a scan there) — lower confidence (the two channels
   may interleave in the same long frame; the per-frame table will show it).

Consequence if 1-4 hold: the fix ranking inverts at fleet scale in-phase — the frame's first fix is
the comb's cadence (de-phasing the births/events, kick-cadence's page), and the observer's phase
axis is the crowd-law fix (candidates ∝ K, capture ∝ K) but not this p99's owner. If instead the
over frames are scan-heavy (≥ 50% scan), the dossier's ranking stands and the observer fix is first.

Kill criterion for the instrument itself: if the channels do not close (unaccounted > 40% of any
worst frame's wall), the decomposition cannot decide and I report that instead of a split.
