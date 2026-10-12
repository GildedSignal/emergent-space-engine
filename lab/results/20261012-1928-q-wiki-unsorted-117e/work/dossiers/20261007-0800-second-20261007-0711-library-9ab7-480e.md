# dossier.md — run 20261007-0800-second-20261007-0711-library-9ab7-480e (second author)

**Claim.** The named experiment is done and the original claim **holds on the shipped
plane's own record**: the per-event work stream at the shipped default (rtf = 1,
members = 48) is fat-tailed with Hill α̂ ≈ 1.27 (jackknife over 15 seeds: 1.24–1.40)
and no construction bound (per-seed worst item 0.84–6.65 ms, an 8× spread), a median
55-s bench's p99.9 underestimates the worst frame of an hour of play by 4.5–6.8×, and
Gaussian moment extrapolation by 11–26× — so the smoothness gate needs the event-tail
exponent line, exactly as the silver run proposed. Two corrections travel with it:
the magnitudes are milder than the synthetic probe's (4.5–6.8× vs 11.5×; though the
Gaussian failure, 25.8×, and the bench-window lottery, 44×, match or exceed it), and
the hazard concentrates at 1:1 play — fast-forward (rtf = 16) *thins* the relative
tail (α̂ ≈ 4.5 at the top 1%), the opposite of the probe's framing and of my own P4.

Regeneration precision: a rerun of seed 5 reproduces the identical digest and
stats, and every demand/counter field of the record byte-for-byte; the timing
fields (µs, ms) and the top item's `kind` annotation (1 frame in 60 000) are
wall-clock and differ by run, as they must.

**Bottleneck.** Board #4 (smoothness and the allocator): what the smoothness gate
should measure, and where the hitch lever is. The gate currently reports percentiles
of a ≤ 55-s bench (`universe --bench` clamps seconds to [1, 55]); the run shows those
percentiles do not size the once-per-hour frame even on today's tiny plane. Gain:
deciding the measurement (one tail line), not speed. The tail is *made of* known
compile-class items — fleet contact epochs (158 of the 174 items ≥ 3 ms) and
player/ship kick recompiles (0.4–3.6 ms; the board already knows kicks dominate and
the plane recompiles on ~99% of kicks) — so the tail line points at the existing
cadence/memo lever, not a new component.

**Evidence** (this folder; Linux/x86 shared runner, 8 vCPU, load ≈ 1.8, 12 GB
available — orders of magnitude only; per-item µs carry CI descheduling noise, the
demand stream does not):

- `cd probe && cargo build --release` (17 s; `CARGO_TARGET_DIR` is preset) — the
  harness drives `emergent_universe::scenario::plane` through its public API only
  (no crate edited; the shipped `tail` example's method: `Budget::events(1)` per
  item, so the digest is budget-independent — control below).
- `bash sweep.sh` (124 s) → `sweep.log`: 15 seeds × 60 000 frames at rtf 1, m 48
  (config A = the shipped default); 1 seed × 216 000 frames (config H = one hour of
  play, digest 7feb0864…); 4 × 60 000 at rtf 16 (B); 4 × 60 000 at m 400 (C, the
  bench clamp). Records: 48 B/frame in `data/`, every file ≤ 3.5 MB.
- Digest control (in sweep.log): seed 1, 60 000 frames, per-item budget vs
  `Budget::unlimited` → identical digest `2f5383af…` and identical stats: the
  instrument changes when work is done, never what.
- `python3 analysis.py` (1.3 s) → `analysis.json`; `python3 addendum.py` (1.6 s) →
  `addendum.json`. The decision numbers:
  - Demand (items/frame, deterministic): A p50 = 1, p99 = 1, p99.9 = 13, max = 48
    (per-seed maxima 26–48); H p99.9 = 8, max = 34; the heaviest frames are
    coincidences (mean 9.4 slices + 7.8 boundaries + 5.6 kicks), not one class.
  - Cost (per-item µs): A p50 = 22, p99 = 42, p99.9 = 438, max = 6 650; Hill α̂
    plateau ≈ 1.0–1.5 for k ∈ [≈200, ≈2 500] (top 0.3–1% of 851 376 items), rising
    through 3 only inside the top ~3% (lighter body); per-seed maxima 0.84–6.65 ms.
  - Bench vs hour (3 300-frame windows = the bench's own 55 s): A window p99.9
    min/median/max = 1/11/44 items against an hour max of 48 (H: 5/…/28 vs 34): a
    median bench misses the hour by 4.5× (A) to 6.8× (H); the *worst* bench window
    captures it (1.08–1.49×) — several benches and taking the max is a partial fix.
  - Gaussian rule on the real hour run: μ, σ of the stream give 3.1 items (demand)
    and 195 µs (frame work) as the once-per-hour value against truths of 34 and
    5 019 µs → truth/Gauss = 11.1× and 25.8× (the probe's 27×).
  - Config B (rtf 16): demand max/p99.9 = 2.6, cost α̂(1%) = 4.5, frame max/p99 =
    12–28 — thinner *relatively*; the wide 3 383→54 128-tick window averages bursts
    in. Config C (m 400): item ceiling stabilises (per-seed max 2.3–2.75 ms) but the
    frame burst grows (p99.9 = 100, max = 328 items; worst frames 37–109 ms of item
    time) — at fleet scale the demand tail, not the item tail, carries the risk.
  - The estimator the silver run recommended (Hill on the event stream) is now
    measured on the engine itself: stable at k = 1% (jackknife 1.24–1.40).

**Predictions** (`predictions.md`, written after pilots only, before the sweep):
P1 killed (max/p99.9 = 3.7 > 3; bench→hour 4.5–6.8 > 3 — I predicted a thin stream);
P2 half-killed (max/p99.9 = 15.2 inside my [3, 30], but seed maxima spread 8× > 3×,
and the plateau is α̂ ≈ 1.3, not a bound); P3 killed (ratio > 3); P4 **inverted**
(rtf 16 thins the relative tail — reported as a held-out miss with the mechanism);
P5 partially held (m 400 fattens absolute frame work; the item ceiling stabilises).
My prior was refutation at 1:1; the experiment killed my prior and the original
claim survived — the held-out result points against me, which is the direction that
counts.

**What would make it wrong.** The per-item µs (and per-frame ms) on a shared runner
carry descheduling and `advance`-re-entry overhead (one `rekey` per budget-1 call);
the α̂ ≈ 1.3 could shift on the M1 and the absolute ceilings with it — but the
demand stream (integer, digest-pinned) and its bench-vs-hour ratios are timing-free,
and they alone carry P1/P3. The plane is small (one battle, 48 members): the tail at
true game scale could fatten (C says the frame burst does) or thin if compiles get
memoised (the tail *is* the compile class). The 25 ms worst frame in A is
engine-advance only (no view, no serialisation) — the shipped bench's 14.5 ms
(sonnet-plane2) is a different mix; ratios, not absolutes, are the transferable
part. The Hill plateau covers the top 0.3–1%: beyond once-per-hour extrapolation
(1 in 216 000) no data exists in 4.2 h of play; the extreme tip (k < 150) reads
lighter (α̂ 4–17), so a far-tail cap cannot be ruled out — the seed-max 8× spread
is the evidence against a tight one.

**Cost of adoption.** One line in plane.md's measured list (the event-size tail
exponent, Hill at the top 1% of the per-event stream, plus the bench-window max),
one measurement hook in the bench (log per-item work — this harness is the
template, `probe/src/main.rs`, 48 B/frame). No engine change. The ρ ≤ 0.7
utilisation policy remains the silver run's probe-level recommendation; this run
adds that its premise (fat event tail) is now measured, not assumed.

**Fit with PRINCIPLES.** "i care about the p95/99 results i want the game to be
smooth" (CL 09-25 14:06) — the run shows p99 of a short bench is not the quantity
that governs the player's worst moment even today. "Compute only surprises. Cost
follows change and entropy" — the tail *is* the entropy of the surprise stream,
now measured on the engine. "Measure before claiming" — the strongest lesson in
the silver run (the estimator was asserted) is now probed, and its P4-shaped
assumption (fast-forward fattens the tail) is corrected: the hazard lives at 1:1.

**The lens.** As the second author I came to bury, expecting a thin 1:1 stream; the
demand stream killed that within the first analysis. What the lens may still miss:
the plane's *player-facing* frame cost includes the view (B15's domain) — the
hitch the player feels is the sum of this tail and the view's, and only the first
is measured here; and the hour is one seed for H (16 seeds cover 16.7 min each),
so the hour-scale ratio rests on A's pooled windows plus one full hour, not many.
