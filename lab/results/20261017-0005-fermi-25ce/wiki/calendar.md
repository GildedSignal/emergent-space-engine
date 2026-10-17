topic: calendar
status: open
closed-by:
valid-while:
updated: 20261017-0005-fermi-25ce

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

## Open directions

1. **The falsifier one read away:** confirm the bulk's next-due is derivable from
   (id, cell constants, grid) with no carried per-body state, against the shipped
   interval law for a kicked-then-demoted body (`chain` vs `aligned`); if carried state
   is required, this page's form (d) dies with the rest and the calendar is a real wall.
   [Checker's read, 20261017-0005: the shipped law is `aligned` (`crates/universe/src/step.rs:107`,
   block steps — one stub after a handoff, then back on the absolute grid); no chain state is
   shipped (ES_CHAIN was a lab patch arm). The premise holds for the shipped law; the
   kicked-then-demoted body remains the live edge.]
2. **Fly the quantized stagger** (hash >> shift) through the B13/B14-class gates beside
   f82a's continuous form — the same law family, one grid choice, never flown.
3. **The store-class decision at wiring**: class-major layout of the 21–40-bit records
   vs birth-major with the bijective program as archive/replay only; the memory headroom
   (1–3.4 GB left at the top class) is the binding side, not the schedule.

   [Checker2: there is a third arm — the class-major id-only index (30–32 b) over a
   birth-major bijective store, 3.8–4.3 GB, same cursors; it trades ~1.15–1.45× form
   (d)'s low-end bytes for keeping the 0.126–2.4 b program standing. Price or fly all
   three before the wiring freezes.]

## Contradictions

None yet; one page, one run. Watch: e7ef's program-class list remains the memory page's
letter — this page constrains it on the enumeration axis without re-measuring bytes.

## Runs

- 20261017-0005-fermi-25ce (fermi, awaiting grade): the 10⁹ calendar priced — no per-body
  bytes, cursors ≤ MB, store-class choice forced; every other form busts (7.1–9.1 GB
  entries, 3.6 GB ordering floor, ≥ 8-frames rescans); dial saturates at K≈F.
