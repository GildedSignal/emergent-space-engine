# The locals' storm is a standing comb phase-locked to `aligned`; the belt's cure cannot transpose, a permanent per-body phase collapses it

## Claim

The 334-event locals' storm (the frame's standing term at every N flown) is a **phase-locked comb**:
every planet-doll body anchors its intervals to `aligned`'s absolute power-of-two grid, so the ~300
ladder locals born at one tick boundary and kick at identical ticks forever — a standing,
non-decaying train (the belt wave decays ×0.72 per period). The page's open direction 1 — "the same
one-step first-kick spread flattens them" — is **refuted**: that spread is re-absorbed by `aligned`
within one period (comb re-forms at ~93% of its envelope, p99 unchanged). A **permanent per-body
phase** (each body's grid offset by a constant id-derived fraction of its own step) collapses the
storm to the no-locals plane — max events/frame 334→53, p99 136→25 — at the price of +19–41% total
events and the pair-shared-boundary property (a law change; digests differ; legality gates unflown).

## Bottleneck

The board's first gap (bodies in the flyable engine: the checker's 12-ms letter extrapolates to
≈ 6×10⁵, "locals-driven"). The locals' comb is ~334 events ≈ 9.8 ms M1-rate in the worst recurring
frames — by itself most of the letter. De-phased, the letter is set by the belt stream alone
(≈ 4.6×10⁶ at 917c's own stream rate), **past the memory break (1.3–1.6×10⁶)**: after ed3a's wave
cure and a locals de-phase, memory binds the flyable N, not the frame. No component is deleted by
this run (the phase arm is a measurement, not an adoption); what it deletes is a wrong lever
(direction 1) and the mystery of the storm's persistence.

## Evidence

All numbers: budget-free coast (`budget 100000 ms`), rtf 100, seed 1, one thread, N in {0, 600,
10³, 10⁴}, 2,000 and 6,000 game-s (20/60 s wall), this Linux box (8 vCPU, load 1.3, 13 GB free —
quiet). Raw per-frame rows + per-doll attribution: `data/*.txt` (one file a flight); the generator
is `scripts/run_batch.sh`, the analysis `scripts/analyze.py`, `scripts/summarize.py`. Cloud timings
are order-of-magnitude; event counts are exact and deterministic (the 20-s baselines at N=600,
10³ and 10⁴ share identical event statistics — 240/136/5.82, envelope 157/159/154/152 — the same
locals population, as the comb reading predicts).

**Structure (baseline, N=10³, 60 s = 5,900 game-s):**
- max events/frame **334** (= 917c's number at 10⁵ and 3×10⁵ — reproduced at 10³: the storm is
  N-independent for N ≥ 600, where the locals cap at 300: max 240, p99 136 at 2,000 game-s at
  N = 600, 10³, 10⁴ identically); **N=0 (no locals) max 51** (= 917c's).
- **Standing**: mean of the top 5 frames per quarter of the flight: **198 / 192 / 178 / 210** — the
  envelope does not decay (the belt wave decays ×0.72 per period; the comb's biggest beats land at
  the end: 334 near 5,900 game-s).
- Period: the storm frames beat at ~10–12 game-s spacing inside a ~331-game-s envelope (the
  power-of-two step hierarchy: same-step locals share every boundary tick).
- Composition (attribution of the worst frames, e.g. frame 396, 212 events): **Home's doll (d2)
  k=27 kicks + b=143 boundaries**, Giant's doll 3; the remaining ~146 of the worst-12 frames' 217
  events carry no doll attribution and **scale with the locals** (35.8 at N=0 → 145.7 at N≥600) —
  the same comb's members delivered through the player's pull lane, not an independent fleet storm.

**The one-shot spread is absorbed (`ES_LOCAL_STAGGER`, direction 1's lever transposed: a planet-doll
ship's first interval offset by a uniform id-derived fraction of its own step):**

| arm (N=10³, 60 s) | max ev/frame | p99 | top envelope (4 quarters) | events/game-s |
|---|---|---|---|---|
| baseline | 334 | 136 | 198/192/178/210 | 4.02 |
| one-shot stagger | 260 | **136** | 180/188/178/195 | **4.02** |
| permanent phase | **53** | **25** | 36/24/13/12 | 4.78 (+19%) |

The stagger's first quarter is already at 91% of baseline (180 vs 198): the comb re-forms within one
step of each body. The tail is untouched (p99 136 = 136) and the work is unchanged — the lever moves
nothing that matters. **Why (the mechanism, from the code):** the clock law's kick times chain from
the previous kick (`plan_clock` inserts at `t + half` at the kick's own tick — an offset persists
forever, which is why ed3a's stagger cured the belt), but the interval law re-anchors every interval
to the absolute grid (`aligned(step, t)`); any one-time offset is snapped back at the next boundary.

**The permanent phase (`ES_LOCAL_PHASE`: the offset is a constant fraction of the body's *current*
step, so it survives step changes):** max 53 = the N=0 floor (51); worst-frame lane split 32.1 total
(planet dolls 5.5, pull lane 26.6) = the N=0 plane's shape (40.6 / 4.8 / 35.8); the ~331-game-s beat
gone (storm spacings jitter 7–18 game-s). At 10⁴ the same: max 53, p99 26. Frame walls: ms p99
5.97→1.90 (3.1×), mean of the 10 worst frames 10.17→3.58 ms (2.8×). Price: events/game-s +19% at
60 s (4.02→4.78; +41% over the first 2,000 game-s: 5.82→8.19) — the phase grid mints stubs at step
changes — and the law's invariant "every pair shares boundaries" (docs/law.md, `aligned`'s doc) is
given up: all three arms' `ladder_digest` rows differ (off = the record bit-for-bit: N=100
`4b822570…`, N=1000 `6895ce06…`, N=3000 `ddd5b1cc…`, kicks identical; stagger N=1000 `e5e9bea5…`
kicks 3750; phase `708f7d82…` kicks 3932).

Reproduce (each ≤ 60 s except the 60-s flights' wall, all ≈ 9 min total): `bash
lab/results/20261016-0504-dynamics-4c22/regen.sh` (applies `work/patch.diff`, rebuilds, reflies
everything above, prints the table and digests).

## Predictions

`predictions.md` was written before the arms ran (the baseline instrument at 20 s existed by then).
P1 structure: **held** (standing ✓, N-independent ✓, N=0 ≈ 51 ✓ — one miss in the letter: my
"no decay >10% per period" holds for the top envelope but the mid-level peaks do decay slowly
(median storm height ×0.992/period), so the comb concentrates rather than fades). P2 absorption:
**held** (re-formed to ~93%, p99 and totals unchanged). P3 collapse: **held** on the collapse (max
53, floor-shaped, periodicity gone) and on the digest difference; **missed** on the overhead — I
predicted totals within ~2%, measured +19–41% (the phase grid's stubs at step changes). P4 (the
fleet lane stays unchanged): **wrong in letter** — the lane scales with the locals and collapses
with them; it is the locals pulled by the player's item, which strengthens the mechanism reading
(one population, two delivery lanes). P5 identity: **held** bit-for-bit.

## What would make it wrong

The phase arm's legality is unflown: B13/B14-class behaviour under shifted phases could refuse or
degrade (the pair-engagement certificate and the changeover interlacing assume shared boundaries in
places I have not audited). The absorption claim is mechanical (code + measurement agree), but a
per-interval birth de-phase that keeps pair boundaries *within a group* while breaking them across
groups would make my "must change the property" conclusion too strong. The +19–41% event overhead is
measured on this scenario's locals only; a population with different step-change rates pays
differently. Cloud timings are this box's; event counts are exact.

**Cost of adopting:** the de-phase is a law change (digests move; the record's anchors re-fly; the
pair-boundary property is documented as load-bearing for SyMBA engagement) — adoption needs the
gates, and the cheaper alternative already named in the docs is step 5 (secular kicks for stable
planet-doll bodies), which *deletes* the comb's events rather than spreading them.

**Fit with PRINCIPLES:** "No work for no reason, so no ticks" — `aligned`'s absolute grid is a
hidden global tick, and the comb is its bill; "a fix signals the wrong representation" — spreading
one birth tick (a fix) failed exactly because the representation (an absolute grid) re-imposes the
tick; "Compute only surprises" — a standing comb is the opposite of surprise: the same coincidence,
every period, forever. "Errors never compound" cuts the other way for the phase arm: it is
untested on energy behaviour, hence not adoptable from this run alone.

## The lens

The dynamics lens (attractors, phase locking) is what made the mechanism visible — but it also
biased me toward the phase-lock story before measuring; the lane-attribution surprise (the "fleet"
residue being the same population) was found only because the instrument counted what I did not
expect. Missed by construction: the legality/energy behaviour of the de-phased law (a gates
question, not a dynamics one), and the M1's absolute timings.
