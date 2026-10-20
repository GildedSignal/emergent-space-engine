topic: mint-knots
status: open
closed-by:
valid-while:
<<<<<<< main
updated: 20261020-1210-second-20261020-1116-system-bd4b-1991
=======
updated: 20261020-1210-spacex-624a
>>>>>>> 20261020-1210-spacex-624a

# The mint's knot vector: one object behind the kick-cost and memory gaps

## Current best

<<<<<<< main
**The kick-cost row and the memory row of the scoreboard are one line item: the
exact-quadrature knot vector (`OrbitShape::knots`) that every fired kick fills and stores
— and its two extents are now both measured, 10²–10³× apart. The compile extent is the
whole arc (the clock totals' traversal: ρ 0.70–0.92 µs↔knots, knots 85–91% of minted
heap, 12.5 KB/kick on members, 6 vs 148 median knots per class, bd4b); the read extent is
one bracket: a minted binding walks 0.04–0.6% (cycles) to ~60% in phase / 12–15% in
panels (passages) of the arc it compiles before the next rebind, so 85–98.5% of every
mint's panels are never interpolated (1991, second author: m400 seeds 1/2/3, coverage
medians 0.23/0.12/0.11% made-cycles, 0.042/0.11/0.05% member-cycles, 0.62/0.58/0.61
member-passage ψ; never-read shares 85–87 / 97–98.5 / 85–88%). The walk is short because
the next rebind after a mint is one full interval away (checker probe at 300 s: walk ÷
interval p10 = median = p90 = 1.000 on all 2645 rows; the plan's own next `Kick` item or
the boundary + interval/2 estimate land on the same tick) and the interval is a small
fraction of the radial period (step_for's 1/2^step_log2 law) — the belt's
one-kick-per-period is the level-0 cadence only. Consequence, decided: a lazy
COMPILE prices no CPU deletion (the traversal is load-bearing for the clocks;
`step_for` reads `period()`/`duration()` inside the binding's life (at the mint for clock-stepped bodies, at the interval's boundary otherwise)) — the kick's CPU lever stays with
the Carlson basis and f9b4's passage thinning, which this grades (the panels sit in the
never-walked outer bands); the STORE lever is sized near-total and already flown
(b9ae standing knots → 0; 0757's bounded cache, gold) — this generalizes its safety to
the kicked classes and prices the retired-history keys-only retention (a Segment's arc
was 85–98% unread even while live). The 448-knot tail is cycle-class and near-fully
unread on every seed (seed 1: 448 knots, coverage 5e-7, 446/448; seeds 2–3 top rows reach
coverage 7e-3 with never-read still ≥ 93%): pure clock-traversal cost, zero readout
value. Domain: one plane +
400 members, 30 s, seeds 1–3, Linux/x86 shared box (orders of magnitude); the close tick
is exact where the plan holds a next `Kick` item, else boundary + interval/2 (≤ 2×);
plunges absent; a member re-kicked inside its own arc is unmeasured and monotonically
shrinks the lever.**
=======
**The traversed fraction is measured and it prices the lever: between a mint
and its discard the engine walks a median 14% (cycles) / 0.7% (passages) of the
compiled panels, and 90% of all minted quadrature panels are never landed in
(20261020-1210-spacex-624a, print-only census in OrbitShape, state-digest-neutral on
three arms, full-walk control passes at 0.85+).** So the kick-cost row and the
memory row of the scoreboard are one line item with a walk-sized lever: with
bd4b's constants (2.7 µs/knot; knots 85-91% of mint heap) the fleet arm minted
1,104,124 knots ≈ 3.0 s of compile wall per 30 s bench, ~90% never consumed —
ceiling ~10× on both rows; a searchable exact-sums spine (e.g. every 8th knot
eager) lands 4-7×. The over-provisioning is inverse-sized: the ≥100-knot mints
(40% of all cycle knots, the 448-knot tail) walk a median 5.1%, and not one of
21,449 mints across three arms reached coverage 0.9 — the eager geometric rule
(ψ-bands doubling at CAP = π/4, orbit.rs append) sizes the mint by orbit shape
while consumption is sized by cadence (time to the next rebind); no certificate
sizes the span. The class split is the wrong lever: both classes over-provision
(passages worst: median 4 readouts against a 148-knot arc compiled to the doll
edge). Digest-neutral by construction (the readout is a function of the key,
not the memo — 5465's bit-identical regeneration). [checker: the count is 21,520 mints
(83+22+18,291+676+2,354+94; regen JSONs), and the zero is domain-bound — outside the
tested range a small cycle tail does reach 0.9: 4 of 54,387 cycles at rtf 1000 (next
decade of the swept rtf) and 17 of 25,683 on seed 7 reach 0.9, with never-landed still
85.8%/90.9% and medians 20%/12.5%; checker2: seed 11 gives 36 of 25,468 (0.14%, above
the 0.007–0.07% of rtf 1000/seed 7), rtf 10000 gives 0 of 157,906 with never-landed
80.0%/98.6% (over-provisioning worsens with rtf), and the 55 s lifetime attack stays
flat (cycle median 18.2%, never 89.3%); pricing untouched, but "not one" is not a law.] Domain: the kick-bench
plane + 400-member fleet at rtf 100, seeds 1 and 3, 30 s; Linux/x86 shared box,
orders of magnitude only; the belt's one-kick-per-period cadence is NOT
measured (its cycles may legitimately traverse full spans); binary searches
read knot sums table-wide, so the 90% prices the exact per-panel quadrature
and panel-level reads, not the sum words.**
>>>>>>> 20261020-1210-spacex-624a

## Refuted

- "The kick's cost and the live-memory plateau are independent gaps" — refuted as one
  object by the ρ = 0.70/0.88 coupling and the 85–91% heap share (20261020-1116-system-bd4b);
  the double-counting concern is e7ef's, extended from cadence×cost to cost×memory.
  [checker: the refutation composes standing results more than it overturns one — the CPU
  share is a765's (compile 84–87% of the rebind) and ec9d's (the leaver tail is
  Passage::compile, 318–356 of 365–381 µs), the memory share is 5465's (58% of a doll
  body) and c304's (~10 kB per ship kick), and library-directions already prices one
  adoption (the Carlson wiring) as deleting the compile wall and the knot table together.
  New here is the per-kick coupling (ρ, µs/knot) and the class census, not the shares.]
<<<<<<< main
- "Cycles traverse their whole compiled arc between mints (the belt's one-kick-per-period
  cadence)" — refuted: the next rebind after a mint is one full interval away, and the
  interval is a small fraction of the radial period; cycles walk 10⁻³ of the arc
  (coverage medians 0.04–0.23%, never-read
  85–98.5%; 20261020-1210-second-…-1991). bd4b's own lens section expected exactly this
  miss ("the hard case is the opposite of the usual one").
- "The passage release overhang holds a large panel share (compile to 2× the doll edge,
  release at the edge)" — refuted: the overhang is ~0.1% of ψ and release_capped 0 on
  every seed; the panel mass is the ψ-ladder's turning-point density, not the radius
  span (1991).
- "A lazy or class-split COMPILE cuts the kick's CPU bill" — refuted as a span argument:
  the full-arc traversal produces the clock totals the engine reads a step later
  (`step_for` → `period()`/`duration()`), so the walked span cannot size the compile;
  the CPU lever is the Carlson basis / thinned grid (closed-form-kernel page), not
  laziness (1991; the branch bd4b's "what would make it wrong" named, now measured).

## Open directions

1. ~~The traversed fraction~~ **measured** (1991): per-class span coverage and never-read
   panel counts, seeds 1–3, on the shipped bench with the record regenerating bit for
   bit. What remains open on this thread is the composition flight: Carlson (cycles) +
   the bounded cache on the kick bench itself — both halves are standing on other
   populations; no new lever is named here.
2. ~~The 448-knot tail~~ **attributed** (1991): cycle-class, never-read 446/448 at seed 1
   (and ≥ 93% on every seed's tail rows; coverage 5e-7–7e-3) — clock-traversal cost, so
   the Carlson/thinned-grid case owns it outright; nothing readout-side to save.
=======
- "If members rebind inside their arcs, lazy knots save the unread fraction; if
  cycles traverse it all, the saving is passage-class only" (bd4b's od 1 fork) —
  the second branch is dead and the first is universal: cycles walk 14% too,
  passages 0.7%, no class traverses its span (20261020-1210-spacex-624a; 0 of
  21,449 mints at coverage ≥ 0.9 against an instrument that reports 0.85+ on a
  full walk).
  [checker: count corrected to 21,520; and "no class traverses its span" holds as the
  median/aggregate law — outside the tested domain a 0.007–0.14% cycle tail does reach 0.9
  (rtf 1000: 4/54,387; seed 7: 17/25,683; seed 11: 36/25,468 — checker2), which no pricing
  rests on.]

## Open directions

1. **The belt case** (the page's remaining fork): the bench's belt stays
   unmeasured; at one-kick-per-period cadence a cycle mint may genuinely be
   walked whole, making laziness belt-neutral there. One belt-arm census run
   settles it. Then the sums-spine design (every k-th knot eager, panels on
   first landing, extents regenerable from the key per 5465) is the adoptable
   form, priced 4-7× against the 10× ceiling.
2. **The 448-knot tail's geometry**: what orbit shape opens it stays open — but
   its bill is now doubly wrong-sided: 40% of all cycle knots, walked at median
   5.1% (20261020-1210-spacex-624a). Whatever the geometry, a walk-sized compile
   never pays for it.
>>>>>>> 20261020-1210-spacex-624a
3. **The allocator side**: 12.5 KB/kick of Arc<Vec> churn — price it with the standing
   counting GlobalAlloc before adopting any memo change. [checker: f623/8994 already hold
   the measured per-kick heap-call family {88, 240, 304, 352, 384², 704, 832} B at
   ~9–10 calls/kick — the counting arm exists; run it on this scene.]

## Contradictions

<<<<<<< main
- None yet on this topic. Adjacent standing facts that compose: kick keys never recur
  (9edc, 225d — sharing/interning the mint is dead), yet the knots are regenerable from
  the key (5465) — so the memo is a private cache per binding, which is exactly why its
  extent (not its sharing) is the lever; 4ea0's census (68–77 reads per generation,
  never-read 0) and 1991's span census compose: the reads exist but all fall inside one
  bracket of the table.
=======
- None yet on this topic. Adjacent standing facts that must compose: kick keys never recur
  (9edc, 225d — sharing/interning the mint is dead), yet the knots are regenerable from the
  key (5465) — so the memo is a private cache per binding, which is exactly why its extent
  (not its sharing) is the lever; and the census shows that extent is 10× the walk.
>>>>>>> 20261020-1210-spacex-624a

## Runs
- 20261020-1116-system-bd4b (system, awaiting grade): the mint's knot vector measured kick by
- 20261020-1116-system-bd4b (system, silver): the mint's knot vector measured kick by
- 20261020-1210-second-20261020-1116-system-bd4b-1991 (second author): the checker's
- 20261020-1210-spacex-624a (spacex, awaiting grade): the traversed fraction measured —
