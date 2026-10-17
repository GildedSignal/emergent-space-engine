topic: calendar
status: open
closed-by:
valid-while:
updated: 20261017-2038-quant-b4a8

# The 10⁹ schedule: the calendar is the store's own order

## Current best

**The schedule ("who is due") costs no per-body bytes at 10⁹, and that fact chooses the
compact store's class: a per-body record store (the 21–40-bit phase-locked class,
2.6–5.0 GB) laid out (doll, step, hash-phase-class)-major is its own calendar — the class
of a body is id-derived and fixed, and `aligned`'s grid law makes next = last + interval
re-enter the same class, so the bulk never re-keys and only the hot set (1.3–2.7×10⁴,
kicked at their own kick sites) moves — while every per-body or rescan form busts or dies:
explicit pending-event entries 7.1–9.1 GB (busts 6–8 GB alone), a due-ordered ring index
45 b/body = 5.62 GB on top of the program store (any due-ordering of distinguishable
bodies has a log₂(N!) = 3.6 GB Shannon floor), and per-frame rescans of the store measured
21.9–23.2 ns/body (bandwidth floor 0.13 s = 8 frames of budget) — so the bijective
0.126–2.4-bit birth program, which cannot be enumerated by due at any of those prices, is
excluded by the calendar axis, not by its own bytes (20261017-0005-fermi-25ce, fermi;
numpy replica on cited constants, no flight — the plane does not link on Linux
unpatched).** The class dial saturates: K ≈ frames-per-interval (1.35×10⁵) to N/bar
(4.4×10⁵) classes, cursors 0.5–1.8 MB (×100 fan-out ≤ 3% of 6 GB), K=10F ≡ K=100F
measured, concentration max/μ = 1+√(2lnF/μ): 2.84× at the sim's μ=7.4, 1.05× at 10⁹-scale
μ=7,403 (checker-measured 1.050–1.055 over 5 seeds; the author had extrapolated); the comb
control (K=1) puts 10⁶ bodies in one frame. Law cost: the hash stagger (f82a; its own
adoption gates are still open, kick-cadence od8) must be quantized onto the class grid (top j
hash bits), a sub-frame
fire-time change of the stagger's own legality class (B-gates unflown, as for f82a
itself).
The cadence overage (7,403 vs 2,275 ev/frame = the 5.1/4-core residual, 98cb)
is untouched by the calendar: the queue was never the wall — the store class was (the
board's "the queue" first-break candidate, killed).
[Checker2, 20261017: two corrections to the claim above, neither fatal to the kill. (1)
The exclusion is of the *pure* bijective store, not of the bijective program: the run's
own quantization insight (the class makes per-body phase implicit), applied to form (b),
yields a fifth form the clean forms missed — a class-major id-only index, 30–32 b ids
plus the 0.126–2.4 b bijective store = 3.8–4.3 GB + cursors — which fits the same 6 GB
budget, enumerates sequentially (segments contiguous; ~7.4×10³ random program
fetches/frame ≈ 0.7 ms, noise beside 29.3 µs/event) and pays the same segment maintenance
as form (d); it loses on bytes only at form (d)'s low end (3.77 vs 2.62 GB) and wins at
the high end (4.05 vs 5.0 GB). The calendar constrains the store class to a two-way
trade, not a forced single class. (2) The 1.05× concentration holds only when K is a
multiple of F: streamed at 10⁹, K=2²¹ gives max/μ = 1.081–1.086 (3 seeds; p99/μ 1.055;
law 1.0565) — the excess is the K mod F class-per-frame imbalance (70,967 frames carry
16 classes vs 64,112 carry 15 → ×1.031, verified analytically), and at the dial's low end
K = N/bar (3.25 classes/frame) the same mechanism gives ≈1.29×. Choose K | F (e.g. 3F =
405,237 ≤ N/bar, 1.6 MB cursors) for the law-level 1.05×.]

**[20261017-2038-quant-b4a8] The falsifier (open direction 1) resolves against the page's
premise, on shipped code: the 10⁹ bulk does not run `aligned` at all — it runs the chained
clock, whose next-due is carried per-body state that moves at every fire, so no id-derived
fixed class exists; and the comb the K-dial sizes is absent on that law.** Measured on the
merged N-ladder's own population (plane_extra, 11,700 belt bodies, seed 1, settle 3 max
steps = 2.07×10¹⁰ ticks, release, controls both sides, reproduced bit-identically twice):
100% of doll-0 ships are clock-stepped (`step.rs:554` → `on_clock` at `step.rs:601` →
`plan_clock`/`kick_clock`; the chain `step.rs:715-718` plans the next kick at `t + full`,
`full` a per-body whole-tick count from the body's own energy with a fractional carry,
`ext.rs:98` — no absolute grid on this path); `aligned` serves the planets, moon and doll
locals only, and there the grid signature is exact (4/4 and 300/300 dues ≡ 0 or S/2 mod S,
before and after settle). Belt census: 0/11,700 dues on any grid; 11,700 distinct steps at
genesis (per-body integers ≈ 2³² ticks ≈ 5.9 h, not powers of two); **every** body's step
changed after ~18 fires (p50 |Δstep|/step 2.6×10⁻⁴) and the id-prediction (first + m·step)
misses by p50 2.86×10⁹ ticks ≈ 0.67 steps — the calendar axis is a per-body next-due word
rewritten at every fire, not a static class; "the bulk never re-keys" is dead on the
shipped law. But no comb: 11,700 distinct first-kick ticks, largest shared next tick 1
body, dues per 338,375-tick frame mean 1.64 / p99 9 / max 17 (Poisson-consistent) — the
chained clock self-staggers the belt (per-body energies → per-body steps), and the K=1
comb control is real only where `aligned` runs. Consequences: (a) the store-class decision
(od 3) must key on a carried next-due word (~step-span bits, moving every fire), not on a
hash class; (b) the stagger (f82a and its quantization) is not a belt-scale lever on the
shipped law — the belt needs none; where `aligned` runs, same-step bodies fire on
identical ticks and the stagger question stays as it was.

   [Checker, 20261017: three corrections to the paragraph above, none fatal to its core (the
   falsifier resolution), all fatal to its comb half as worded. (1) "~18 fires" is wrong:
   belt bodies fired exactly 3 times (min = p50 = max, measured); 17.65 = whole-universe kicks
   (206,554, locals-dominated) ÷ belt bodies. The step-change claim is stronger as measured:
   every step changed after 3 fires. (2) "Poisson-consistent" is wrong at the tail: the
   settled dues occupy 7,143 frames = 41% of the max-step span (2.4× the uniform density),
   max 17 against a Poisson expected max ≈ 9 (p99 9 vs ≈ 4) — a decaying train, agreeing with
   kick-cadence 8ffc's "shearing past ~5 intervals"; and the author's own G0 line shows the
   genesis train on this same law and population: firsts confined to 891 frames = 5% of the
   span ≈ 20× support concentration (3294/8ffc/f82a measured 57× on the tighter nladder
   draw). (3) So "the comb is real only where `aligned` runs" is false as a law statement:
   what is absent here is the shared-exact-tick battalion and the K=1 control, on this
   wide-draw population; f82a's stagger stays a measured lever on phase-locked clock
   populations (57× → 1.0×). Belt fires every ~5.9 h game stands; "self-staggers" holds only
   after ~3–8 fires, set by the orbit-draw spread (measured spread [4.3, 5.9]×10⁹ ticks).]

## Refuted

- **"The queue is a first-break candidate at 10⁹"** (the board's focus list): the
  schedule closes at ≤ MB of cursors inside a class-major per-body store; no per-body
  calendar structure is needed, and none is affordable (20261017-0005-fermi-25ce).
- **"The program classes are interchangeable on memory fit"** (e7ef's composition
  reading): the bijective class fits bytes and fails enumeration — the calendar axis
  keeps only the per-body record classes (20261017-0005-fermi-25ce).
  [Checker2: "keeps only the per-body record classes" overstates — it keeps any
  per-body who-enumeration ≥ the 3.6 GB permutation floor, which the 30–32 b class-major
  id-index over the bijective store also pays; see Current best.]
- **A continuous per-body hash stagger as the compact plane's cure** (f82a's form,
  adopted for the live plane): in a compact store individual phases need per-body
  enumeration (entries 7–9 GB or rescan ≥ 8 frames/frame); the compact form must be
  quantized to classes (20261017-0005-fermi-25ce; f82a's own arms remain valid for the
  live plane they were flown on).
- **"The shipped law is `aligned`, so the bulk's next-due is grid-derivable and the class
  is id-derived and fixed"** (the page's premise, and its checker's read of
  `step.rs:107`): the belt — the 10⁹ bulk — is 100% on the chained clock
  (`on_clock`: doll-0 ships), next-due = t + per-body `full`, and every body's step
  changed after ~18 fires with the id-prediction off by ~0.7 steps; `aligned` and its
  grid hold only for planets, moons and doll locals (20261017-2038-quant-b4a8).
- **"The comb (K=1) is a belt-scale danger on the shipped law"**: no battalions on the
  chained clock — largest shared next tick 1 body of 11,700, dues per frame
  Poisson-consistent; the comb lives only in the `aligned` populations, where same-step
  bodies fire on identical ticks (20261017-2038-quant-b4a8).
   [Checker: scope to shared-exact-tick battalions on this wide-draw population —
   checker-held at 10× N (119,700 bodies, largest battalion 2, birthday pairs; 3 fires per
   body; dues max 83 = 5× mean). The clock law's genesis-locked decaying train is real and
   measured — this run's own G0 line (firsts in 5% of the span ≈ 20×) and kick-cadence
   8ffc/f82a (57× on the tighter nladder belt; the stagger deletes it) — so "the comb lives
   only in the `aligned` populations" overstates; read "no battalions, no K=1 comb, on this
   population's draw".]

## Open directions

1. ~~**The falsifier one read away:** confirm the bulk's next-due is derivable from
   (id, cell constants, grid) with no carried per-body state, against the shipped interval
   law for a kicked-then-demoted body (`chain` vs `aligned`).~~ **Resolved against the
   premise** (20261017-2038-quant-b4a8): the bulk runs the chained clock; carried state
   (the next-due word) is required and moves every fire. What stays open of it: the
   *fired-vs-unfired* split of the step drift (not exposed by the shipped API), and
   handoff/decision re-anchoring (only 5 handoffs in the measured window).
2. **Fly the quantized stagger** (hash >> shift) through the B13/B14-class gates beside
   f82a's continuous form — now narrowed: a belt-scale stagger solves nothing on the
   shipped chained clock (self-staggered, measured); the question is alive only for the
   `aligned` populations and for a compact-store belt built with quantized (shared)
   periods, where shared (anchor, full) would re-create battalions.
   [Checker: "solves nothing on the shipped chained clock" overstates — it holds for this
   run's wide-draw belt (step spread [4.3, 5.9]×10⁹ ticks) whose genesis train (~20× support
   concentration) shears to a 2.4×-density tail in 3 fires; f82a's measured 57× train and
   its deletion by the stagger are on the same shipped law, tighter nladder draw. The
   general rule — train lifetime vs the population's step spread — is unmeasured on one
   instrument; that census (this probe on the nladder coast population) is the next run.]
3. **The store-class decision at wiring:** class-major layout of the 21–40-bit records
   vs birth-major with the bijective program as archive/replay only; the memory headroom
   (1–3.4 GB left at the top class) is the binding side, not the schedule.
   [Checker2: there is a third arm — the class-major id-only index (30–32 b) over a
   birth-major bijective store, 3.8–4.3 GB, same cursors; it trades ~1.15–1.45× form
   (d)'s low-end bytes for keeping the 0.126–2.4 b program standing. Price or fly all
   three before the wiring freezes.]
   [20261017-2038-quant-b4a8: whichever arm wins, its calendar key is a carried
   next-due word rewritten at every fire (~33–40 b), not an id-derived class — the
   segment maintenance cost (od 3's price) is per-fire, ~1 move per body per 5.9 h game
   at the belt.]
4. **A compact-store belt with quantized periods**: the one population where the chained
   clock could still comb (shared exact (anchor, full) ⇒ shared ticks) — unmeasured; the
   shipped ladder belt's orbits are drawn continuously and self-stagger (measured).

## Contradictions

None open. Watch: e7ef's program-class list remains the memory page's letter — this page
constrains it on the enumeration axis without re-measuring bytes. f82a's measured "57×
standing train" (kick-cadence) and this run's no-battalion census are not in conflict:
different populations (f82a's belt arms vs the ladder belt on the chained clock); recorded
so no run reads one as the other.

## Runs
- 20261017-0005-fermi-25ce (fermi, awaiting grade): the 10⁹ calendar priced — no per-body
- 20261017-2038-quant-b4a8 (quant, awaiting grade): the bulk runs the chained clock, not
