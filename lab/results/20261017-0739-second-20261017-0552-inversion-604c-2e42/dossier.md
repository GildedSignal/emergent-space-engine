# Dossier — 20261017-0739-second-20261017-0552-inversion-604c-2e42 (second author on 0552)

**Claim.** The checker's named experiment, run: the K=1,000 formation frame's over-budget tail is
**comb-owned, not scan-owned** — 97.7-98.5% item pipeline (kicks/boundaries/fits), 0.6-1.0% scan
channel, on both seeds and both passes (68/540 frames over; the six p99 frames 98.0-98.7% comb;
the worst frames are the wave frames: `ev=1002`, comb 43.93 / scan 0.24 ms in the author pass,
65.44 / 0.33 in the regen pass — the whole formation's kick wave in one frame) — so **the fix
ranking inverts: the frame's first fix at fleet scale in-phase is the comb's cadence, not the
observer's phase axis**; the scan channel rides idle room (91-95% of its time inside under-budget
frames, ≈10% of mean frame wall at K ≤ 1,000) until 69f3's latch freezes it (zero answers in
flight at K=3,000-10,000, the pin growing to 51-93 MB), and 0552's P5 mechanism ("SCAN_BACKLOG
then forces it into a frame") never fires anywhere: held_max ≤ 71 against the backlog's 2,048.

**Bottleneck.** The board's top item (bodies: 28 vs 10⁹) and the promotion page's refutation ("the
near set is crowd-proportional, the observer alone ruins the frame at 13,028 bodies"). The checker
held 0552 at silver for exactly this gap: "Per-worst-frame decomposition at K=1,000 on ≥ 2 seeds,
splitting the 52-ms p99 between the scan channel and the comb channel … That split decides the fix
ranking the run proposes." Done: the split is measured per frame, both seeds, plus the ruin case
(3,000+10⁴) and the decade-up (10⁴) — and it decides the other way.

**Evidence** (all from `regen.sh` — the regen pass below is a clean re-run from the shipped tree
plus `work/patch.diff` — Linux/x86, 8 vCPU shared, load 1.0-2.4; each flight ≤ 40 s wall;
instrument = 0552's atomic counters plus per-frame `prof` stage deltas, channels = top-level stages
only — scan `ENCOUNTERS+SCANS`, comb `REKEY+APPLY+REQUEUE+PROCESS+TAKE_DUE+HANDOUT`; the channels
close against wall to 98.4-99.6% (unaccounted 0.4-1.6%), which is the instrument's own control;
census bit-identical ×3 on a quiet machine (one of the final pass's three stability reruns diverged under load — the flight ends at a different tick, 0552's checker's caveat); every digest reproduces, all three passes, seed-1 K=1,000 digest identical to 0552's
`4916c14e…0c793172`; wall ms differ between passes exactly as the lab expects on a shared machine —
the shares and the deterministic counts are the claim; raw in `raw/`, the author-pass values where
quoted are the first flights on the same binary):

*The decisive split (form=1000, extra=0, coast, 10 s, rtf 100).* Seed 1: 68/540 frames over the
12-ms budget; over frames = **0.6% scan / 98.5% comb** (author pass, mean 34.19 ms; regen pass
0.9%/97.7%, mean 38.47); the six worst (p99) frames 0.5% scan / 98.7% comb (regen 0.6%/98.0%), of
the comb ~80% kick items (fits ~38% nested inside them); author-pass worst frame f=135: `wall 44.57
| scan 0.24 / comb 43.93 / unaccounted 0.40 | kick 34.49, fit 16.27 | ans=0 cap=1 ev=1002`; the
regen pass's worst is the same animal (f=455, comb 65.44 / scan 0.33, ev=1002) — the wave frame:
every formation ship's kick lands in one frame. Seed 2: same class — over 68, 0.7% scan / 98.5%
comb (regen 1.0%/97.7%); p99 frames 0.6% scan / 98.3% comb (regen 0.7%/98.0%); candidates
1,031.9 = 32.1 + 1.00·K, 87/87 scans bailed (0552's crowd law and the checker's seed-2 numbers
reproduce). The mean late frame: 9.7-10.0% scan, 85.1-85.3% comb, both seeds — **the observer owns
a tenth of the mean frame and none of the tail**; `chan scan-placement`: 95%/94% author pass
(91%/92% regen) of all scan-channel ns falls inside frames that end under budget (answers drained
into idle room, one at a time; held_max ≤ 15 across passes).

*The mechanism correction.* 0552's P5 note said a 4.5-ms answer "does not fit idle time's 750-µs
margin and SCAN_BACKLOG then forces it into a frame." Measured: the answer is 3.93 ms/call at
K=1,000 and is answered in quiet frames' idle room (the drain's gate `room ≥ 2·max(scan_ns,
0.75 ms)` holds while answers are ≤ ~6 ms); SCAN_BACKLOG (2,048) never fires in any flight
(held_max 1-15 at K=1,000, 71 at 3,000+10⁴, 43 at 10⁴ and at 3,000 alone). Above the latch the
drain freezes exactly as 69f3 recorded (answers 0 ms in flight at K ≥ 3,000; the flight's scan
channel is then captures only, 1.3-1.5% of wall at 3,000+10⁴) and the held candidates pin memory:
71 × 3,338 × 216 B ≈ **51 MB** at 3,000+10⁴, 43 × 10,039 × 216 B ≈ **93 MB** at 10⁴, answered only
by the untimed final digest.

*The ruin case and the decade-up, decomposed.* form=3,000 + 10⁴ belt: 85 frames over, mean 85.16 ms
(author; 98.53 regen) = 1.3-1.5% scan / 91.9-92.9% comb; p99 frames 134.55-197.45 ms = 1.0% scan /
97.5-97.8% comb; author-pass worst frame 137.26 ms = 1.47 scan / 134.23 comb (kick 104.60,
`ev=3002`). form=3,000 alone: 43 over, 0.6% scan / 95.8% comb, answers 0 ms, held_max=43. form=10,000
alone (the checker's decade-up): p99 452.8-463.5 ms, over frames mean 310.9-322.4 ms = 0.7% scan /
95.0-95.5% comb, p99 frames 0.4% scan / 98.4% comb, hwm 471 MB. **At every K measured (200, 1,000,
3,000, 10,000) the over-budget frames are 91.7-99.7% comb** (K=200's single over frame: 99.7%
comb, seed 2's worst six 8.6-10% scan only because they end *under* budget at 10.9 ms). The belt
controls and the tier reproduce 0552 and the checker: 186.2/187.1 candidates, zero bails at
10⁴/10⁵; 81/87 bailed beside the 10⁴ belt; the tier off beside a 10⁵ belt (0 bails, 387.1
candidates — the "200 ships re-kill" crossing is population-pair-dependent, as the checker showed).

*What the split decides.* Both channels are crowd-proportional in their own bills (candidates and
answer cost ∝ K; wave events ∝ K), but they break different gates: the comb owns the frame's tail
(smoothness, the 12-ms budget, 23% of game time lost at K=1,000 — over frames ~98% comb), the
observer owns the mean's ~10% below the latch and the pin above it. Fix ranking at fleet scale
in-phase: **(1) the comb's cadence** (de-phase the formation's events — they are in-phase because
the births are; kick-cadence's page, nladder's comb), **(2) the observer's phase axis**
(taleb-09b5's rank-along-orbit: cuts the candidates, the answer bill and the pin), and the bail's
locality (0552's fix (a)) third — it changes which frames walk, not what the walks cost. 0552's 10⁹
arithmetic stands as written for the observer's own bill (~0.36 s capture + ~4.4 s answer a scan at
a 10⁶ fleet); what it missed is that the same fleet's comb is ~8× the scan in the mean frame and
~100× in the tail, so at 10⁹ the observer fix alone buys a smooth mean on a ruined frame.

**Predictions** (`predictions.md`, written before the decisive runs): P1 (over frames ≥ 80% comb,
both seeds; SCAN_BACKLOG never fires; answers drain into quiet frames) — **held with margin**
(97.7-98.5% comb; 91-95% placement). P2 (≥ 80% of scan ns under budget; mean split comb 80-90%,
scan 8-15%) — held (91-95%; 85.1-85.3% vs 9.7-10.0%). P3 (answers one at a time, 3-5 ms) — held
(3.93 ms/call; held_max ≤ 15). P4 (seed 2 same class) — held (0.7-1.0% scan in over frames; 87/87
bail; 32.1 + 1.00·K). P5 (at 3,000+10⁴ comb ≥ 60% of worst frames, scan share rises) — held on the
first (91.9-97.8% comb), and the scan share of *frame time* in fact falls (1.0-1.5%) because the
latch freezes the answers rather than admitting them — the failure mode moves from time to pin.
The kill criterion (unaccounted > 40% of any worst frame) did not fire (max 1.6%).

**What would make it wrong.** The channels are wall-clock shares of one thread (Linux/x86, shared
machine): shares, not the ms, are the claim, and they were stable across two passes and both seeds
(over-frame scan share 0.6-1.0%). Burn is still unflown (coast only, as in 0552 — the census's
70.0-at-burn half of the O(1) sentence stays untested); the formation is one-birth-tick in-phase by
construction, the comb's worst case — a spread-birth fleet would flatten the wave and raise the
scan's relative share, which is itself the cadence fix measured from the other side. The probe
times `frame_to` only; the final digest's drain is untimed (as in 0552), so the pin is measured as
held_max × candidates × 216 B, not as a frame cost. held_max at K=1,000 moved 1 → 15 between
passes (load): the answer "bill" is unchanged, only how many are left held at a frame boundary.

**Cost of adoption, and fit.** Nothing to build here: this re-ranks 0552's own fixes and hands each
half to its owner page (the comb to kick-cadence, the crowd law and the pin to promotion's phase
axis). Prior art, re-scoped as the checker asked: the plane-scale bail and the `bodies/4 + 64`
mechanism are scan-queue's (cdf0 20261016-1120: Home's doll trips the N-relative rule at the
plane's flown N, 95% of coast captures walk and clone; 3999 20261016-1740: the range-hull
registration, the belt-band every-N disease); the drain's one-way latch is 69f3 (20261016-0213).
0552's new content stands: the formation scene flown, the 1.00/ship crowd law, the always-bail
under concentration (cdf0's "small-N disease" scoping corrected by 0552's checker at 10⁴ in-band
bodies), the frame cost — and this run adds the decomposition that ranks the fixes. Fit: PRINCIPLES
19 (a fix signals the wrong representation — in-phase births are the comb's wrong representation,
and the bail's nonlocal threshold the observer's) and 12 (smoothness: p95/99 is the goal, and the
p99 is comb-owned).

**The lens.** The second author inherits inversion's blind spot from the other side: a channel
split prices what each frame spent, not what each fix would save — de-phasing the births may move
work into exactly the quiet frames where the answers now drain, so the two fixes interact (cheap
to measure next: the same probe on a spread-birth formation). And the split is coast-only; burn
changes both the window (0552's mechanism) and the drain's gate (1250's max-gate finding).
