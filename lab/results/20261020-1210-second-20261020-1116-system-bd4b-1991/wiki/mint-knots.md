topic: mint-knots
status: open
closed-by:
valid-while:
updated: 20261020-1210-second-20261020-1116-system-bd4b-1991

# The mint's knot vector: one object behind the kick-cost and memory gaps

## Current best

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
3. **The allocator side**: 12.5 KB/kick of Arc<Vec> churn — price it with the standing
   counting GlobalAlloc before adopting any memo change. [checker: f623/8994 already hold
   the measured per-kick heap-call family {88, 240, 304, 352, 384², 704, 832} B at
   ~9–10 calls/kick — the counting arm exists; run it on this scene.]

## Contradictions

- None yet on this topic. Adjacent standing facts that compose: kick keys never recur
  (9edc, 225d — sharing/interning the mint is dead), yet the knots are regenerable from
  the key (5465) — so the memo is a private cache per binding, which is exactly why its
  extent (not its sharing) is the lever; 4ea0's census (68–77 reads per generation,
  never-read 0) and 1991's span census compose: the reads exist but all fall inside one
  bracket of the table.

## Runs

- 20261020-1116-system-bd4b (system, silver): the mint's knot vector measured kick by
  kick — ρ 0.70/0.88 µs↔knots, knots 85–91% of minted heap, 12.5 KB/kick on members, 6 vs
  148 median knots per class in one scene.
- 20261020-1210-second-20261020-1116-system-bd4b-1991 (second author): the checker's
  named experiment flown — span coverage 0.04–0.6% (cycles) / ~60% ψ but 12–15% panels
  (passages), never-read 85–98.5% per class; lazy-compile CPU killed (the clocks own the
  traversal), store lever sized near-total on the kicked classes. [checker2: reproduced
  bit-for-bit (digests equal bd4b's stored record); held-out seeds 4–5 and a 50 s arm
  (147 re-mints, close-tick estimate off by ≤ 18% of the walk) hold the structure;
  `--members` is clamped to 400 (xtask/src/universe/mod.rs:40), so the ≤ 400-member domain
  is the bench's cap, not a choice.]
