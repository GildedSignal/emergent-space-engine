# Dossier — run 20261020-2306-m2-macro-structure-1bcc (lens: mathematical representations, structure/composition/scale; second deep pass)

## Claim (one sentence)

The belt's family base is measured for the first time: at the law's own 11+11-bit memo grid the
shipped belt is **key-saturated (72–93% of bodies alone in their cell at 10⁶)**, but a dyadic
coarsening of the same key reaches **F = 8,749 cells (114×) at 7+7 bits and F = 659 (1,517×) at
5+5 bits**, the base is **stable under real flight** (F flat at every width across 205,154 belt
events), and the schedule census kills the timing-wheel form (**99.7% of belt bodies hold a
distinct pending tick and a distinct (step, anchor) pair from genesis** — the stagger, not the
comb, is the schedule's entropy), so the family must be a **per-cell tape consumed at each
member's own tick**, not a synchronised firing.

## Bottleneck

Board rows **"Macro, kicks per body (~10³)"** and **"Macro, families and formations"**, with the
memory row through the shared tables. a877 (this window) measured *when* one kick stream is
shareable (the certificate Ξ, the w11 velocity word) but not *how many streams the belt needs*:
the gain is N/F and F was unmeasured — if the belt fills the key space, families are
formations-only and row 1 must come from cadence and kick cost alone. This run measures F and
its dial, prices the composition, and kills the wheel form of the schedule. What it deletes, at
the widths measured: N−F kick evaluations, refits and mints per epoch (a877's F−1 per family,
now with F measured), and the per-body compiled tables (each of the ~3.8 KB tables is today
private: my control census counts 99,700 distinct exact keys among 99,700 belt bodies).

## Evidence (each command ≤ 60 s; `regen.sh` reproduces all from a clean tree)

One probe, `crates/universe/examples/fibers.rs` (work/patch.diff, print-only; the law's own
`OrbitKey::bound` + `MemoCode::encode` on `ladder_ship`'s exact draws, and the shipped plane
flown by `frame_to`):

```
cargo run --release -p emergent-universe --example fibers -- draw 1000000 1   # the base census
cargo run --release -p emergent-universe --example fibers -- draw 1000000 2   # held-out seed
cargo run --release -p emergent-universe --example fibers -- flight 100000 20 100000
```

- **P1 held — the shipped memo width cannot be the family key.** At N = 10⁶ belt births
  (999,700 bodies), the law's own `MemoCode` cell (11+11 fraction bits) holds **72.3% as many
  cells as bodies** (F = 722,797; occupancy median 1, p90 2): the [2,3) AU × Rayleigh-e band
  spans far more than 2²² cells at that width. Sharing at the shipped grid is **1.4×**. The
  20 October formation-family page's construction ("same-key members share step size and tick
  anchoring") therefore has no keys to share at belt scale as shipped — its measured 0-fork
  horizons are about tight clusters (formations, the ring fleet), and the belt needs its own
  width dial.
- **P2 held — the dial is steep and saturates at the band's own support.** Coarsening both
  fraction fields of the same key by b bits (a dyadic coarsening: relative cell width
  2^(−11+b) per axis, exponents kept):

  | b (bits dropped) | grid | F at N = 10⁶, seed 1 | sharing N/F | seed 2 | N = 3×10⁵, seed 7 |
  |---|---|---|---|---|---|
  | 0 (shipped) | 11+11 | 722,797 | 1.4× | 722,798 | 270,188 (1.1×) |
  | 2 | 9+9 | 114,300 | 8.7× | 114,174 | 94,870 (3.2×) |
  | 4 | 7+7 | 8,749 | **114×** | 8,720 | 8,144 (37×) |
  | 5 | 6+6 | 2,380 | **420×** | 2,373 | 2,255 (133×) |
  | 6 | 5+5 | 659 | **1,517×** | 659 | 628 (477×) |

  F saturates at the band's intrinsic support (659 cells at 5+5, **identical across seeds**),
  so at N = 10⁹ the sharing at 6+6 is ~10⁶× by occupancy alone. The occupancy at 7+7 is
  heavy-tailed but sane (median 111, p90 229, max 426 bodies/cell at 10⁶).
- **P3 held — the base is stable in flight.** The flown plane (N = 10⁵, 20 s wall at rtf 10⁵,
  341,586 events of which 205,154 belt events, 2.06 per body): F(11+11) moves 96,359 → 96,358,
  **F(7+7) = 7,518 and F(6+6) = 588 bit-flat at every census** (t0, three mid-flight, end). The
  structural reason: a fired kick moves a key by far less than one cell (the velocity quantum is
  ~2⁻¹¹·v, so δE/E ~ 2⁻¹⁰, crossing an 11-bit cell needs ~10⁵ fires ≈ thousands of orbits at the
  shipped cadence). The exact keys stay 99,700 distinct throughout — the w61 scatter a877
  derived happens *inside* the cells.
- **P4 refuted — the wheel is dead; the stagger is the schedule's entropy.** At t0 (genesis,
  before any event): **99,670 distinct pending ticks among 99,700 belt bodies** (median 1
  body/tick, max 2), the tick divisibility histogram halves per power of two (99,670 / 49,806 /
  25,082 / …) — the signature of *uniform* ticks, not comb clustering — and **distinct steps =
  99,670, distinct (step, anchor) pairs = 99,670**: every body carries its own stride and
  anchor. The plane's staggered genesis (f82a's flat train) makes the calendar's content
  per-body by design; a hierarchical timing wheel would degenerate to one entry per body, and
  the calendar row's escape is the id-derived form (25ce's cursors; the schedule is a
  deterministic function of the birth draws), not a wheel.

**The composed pricing** (constants from the record: 43–52.8 µs per kick step, law-dominated,
zero reuse (kick-cadence, c01c/0c44); the fit that remains 58 µs a rebind (cell-rebind);
mature store 20.7–22.1 bits/ship (2b8e); fork rates at w11 measured by a877: 0 at δx ≤ 10³
root, 0.17%/kick at 10³–10⁶, the ⅛-orbit ring 0.94%/kick at the belt; w8 → 0; w16 → 20%):

- *Kicks:* today the belt costs N × 128 kick steps/orbit ≈ **50 core-s per game-second at
  N = 10⁶**. Under the fibration at 6+6 (F = 659 at 10⁶): per epoch, F stream evaluations
  plus the fork term (members whose own carry straddles: a877's measured rate, ring-dominated
  ~1–4%/member/kick at w11): F + 0.01–0.04·N evaluations ⇒ **24–85× at w11; ~300× at w8**
  (fork → ~0.1%). At 10⁹ the same arithmetic gives ~10–80× (the fork term, not F, is the
  ceiling — each fork is one body's own sigma-delta straddle, irreducible per-body work).
- *Memory:* today every belt body holds a private compiled table (my control: 99,700 distinct
  exact keys; the tables are ~3.8 KB each before GPT's cache). Under the fibration the table
  is per cell: F × 3.8 KB shared, members hold their 16 B tube + carries + the 22-bit store —
  the live-record floor drops from ~2.5–5.1 KB/body to **~O(10²) B shared + ~90 B live
  content**, the memory row's ~10².

**What the stagger finding forces (the tape form):** same-cell members do *not* fire together
(measured: distinct (step, anchor) = N), so a877's engine-side premise ("same-key members fire
at the same tick") does not hold on the shipped plane. The sharing must be a **per-cell tape**:
the cell's kick-delta sequence extended lazily (one evaluation per epoch per cell), each member
consuming it at its own tick with its own sigma-delta carry, forks writing member-local side
events. This also dissolves the apparent smoothness conflict: the stagger moves from bodies to
cells (F cells' evaluations spread across the epoch by the compute-ahead metronome — the due
times are known stride-ahead), so the allocator loses nothing.

## Predictions (predictions.md, written first)

- **P1 (belt saturation at the shipped grid) held**: 72.3% single-cell occupancy measured
  against a predicted 50–80% (I wrote 0.2–0.5·N occupied *cells*; the measured sharing 0.72 is
  at the pessimistic end — the belt is *more* saturated than my estimate).
- **P2 (a width b ≤ 6 with F ≤ 0.01·N) held**: b = 4 gives 0.88%, b = 5 gives 0.24%, b = 6
  gives 0.07% — and F saturates at the band's support (seed-independent at 5+5).
- **P3 (cells stable under kicks) held**: bit-flat at every flown census; the structural bound
  (a fire moves a key ~2⁻¹⁰ relative, a cell is 2⁻⁵…2⁻⁷) says stability holds for ~10³+
  orbits, far past the flight.
- **P4 (few distinct pending ticks — a wheel) REFUTED**: 99.7% distinct ticks, uniform
  divisibility histogram, N distinct (step, anchor) pairs. The prediction's kill branch fired:
  the stagger, not the comb, owns the schedule.

## What would make it wrong, cost of adoption, PRINCIPLES fit

- **Wrong if** the family word fails the behaviour gates — the same named experiment as a877's
  od 1 (a w11/b-variant plane against B12/B13/B17/B18), now with *two* dials (the velocity
  word w and the cell width b: the cell puts a bounded 2^(−11+b) relative element offset on
  every member, an error of the same bounded type a877 priced, but the gates must fly both).
  Also wrong if the fork rate at belt ring spreads exceeds the a877-derived 1–4%/kick once
  measured at the chosen width (my fork numbers are their measured rates plus their census's
  exact linearity |δa|/δx = 2μ/d³, not a new measurement), or if the rebind does not ride the
  sharing (the 58 µs fit is per fired member unless the kick is applied in element space —
  the engine-side census on a w/b-plane, a877's od 2 extended, is the named decisive
  experiment; the evaluation-only sharing bound is unmeasured below the 24× floor).
- **Cost:** the cell key (a coarsened MemoCode: two masks, no new arithmetic), the per-cell
  tape with fork side events, and the demotion of members back to (cell, phase) between
  events. No new physics; the law's own quantized arithmetic is unchanged — the cell is a
  sharing decision the certificate Ξ already bounds.
- **PRINCIPLES:** "Store the generator, not the generated" (#6: the cell's tape is the
  generator; the per-body tables are the generated); "the cheapest compute is compute not
  done" (#1); "same mechanics at all scales while not doing the work" (#19: the memo already
  shares tables by exact key — the fibration is the same mechanics one scale up, at the width
  the scale needs); "every body real" (the member's tube, carries and phase stay its own
  integers; the cell shares evaluation, never identity).

## The lens (what it may have made me miss)

The structure lens reached for the quotient (the fibration) and the order (the wheel) and
priced both; what it did not do is open the kick's own arithmetic (the fit/refit split inside
the 43–53 µs) — that is the micro lens's ground and GPT's live job, and my pricing leans on
the record's numbers rather than a fresh split. It also takes the belt's birth distribution
(the plane's [2,3) AU band) as the population; a game-born belt with tighter structure (the
birth program's bands) would change F at every width by the same census, and the encounter /
view terms of the composed 10⁹ budget are outside this run. The p90 occupancy's heavy tail
(426 bodies in one 7+7 cell) hints the band's edges matter to a real scheduler; I did not fly
a loaded machine, so no smoothness claim here is measured.
