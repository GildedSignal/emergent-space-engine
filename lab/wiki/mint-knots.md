topic: mint-knots
status: open
closed-by:
valid-while:
updated: 20261020-1729-spacex-65b8

# The mint's knot vector: one object behind the kick-cost and memory gaps

## Current best

**The page's 100× conflict is adjudicated (20261020-1729-spacex-65b8, one binary, one
instrument, shipped digests regenerated bit for bit): 624a's 14% and 1991's 0.04–0.6%
are both real and both reproduced — they are different quantities.** 624a's number is
panel-landing share: at median table sizes one bracket panel per read IS 1/n (16.7% on
the default arm's 6-knot tables ≈ their 20%; fleet panels+probes 46%, quad-only 10.4%
brackets their 14.3%; passages 0.68% = their 0.7% exactly). 1991's number is the
binding's lifetime share, now measured on observed next kicks: every closed row
(8,710 seed 1 + 7,379 seed 3) rebinds at interval < period/64. The real per-mint law is
a third quantity: **post-mint quadrature is read traffic** — per-frame reads, reflection,
and the resolver's exit/periapsis time-bisections probe the binding at scattered phases —
touching 6.6–19.9% of the arc's phase (walk; the quad-panel share is 10.4% at rtf 100)
regardless of the < 1/64 lifetime; rtf is a mint-count dial, not a cadence dial
(mints 496→18,933, per-mint medians held within 2×). Decision, composed: the CPU lever stays blocked at the clock totals
(`from_shape` sinks period/proper/advance from the full-arc last-knot sums at mint —
lazy compilation cannot produce them; 1991's kill confirmed structurally), and is priced
by traffic once totals are O(1) (the Carlson basis): ~90% of cycle panels and ~99.3% of
passage panels never run quadrature post-mint, so traffic-priced lazy panels cut the
mint's quadrature wall ~10× behind Carlson. The store lever stands near-total (b9ae/0757
generalized). The 448-knot tail: 1.2% of its panels ever quadrature (reads 474–731).
Domain: the kick-bench plane, made + 400-member fleet, rtf 1 and 100, seeds 1 and 3,
10–30 s; Linux/x86 shared (orders of magnitude); belt cadence absent (no closed row
≥ 1/64 — ships only, the belt unwired); resolver-internal fit mints (~9.8k at rtf 100)
counted but excluded from class tables.
[checker: reproduced bit for bit, and the two invariance laws are rtf ≤ 100 laws — at
rtf 1000, outside this domain, 526 of 26,330 closes (2.0%, all member cycles) land in
[1/64, 1/16) with none at or above 1/16 (still no level-0 row), and member-cycle
medians move (walk 0.02%, reads 22, median knots 9, quad 16.7%): rtf is not a pure
mint-count dial past the conflict's decade, and the walk–cadence relation appears once
lifetimes pass 1/64 (bin walk 5.1% vs 0.01%) — P4's monotone form. Seed 11 and 55 s
hold every number (closes all < 1/64, passages 0.68% exact). The ~10× lazy ceiling
assumes per-panel caching: quad_calls run ~27× (cycles) / ~12× (passages) per landed
panel. checker2: independently rerun — rtf 1000 reproduces 526/26,330 and the moved
medians; seed 7 and 55 s hold every close < 1/64 and the 0.68% passage floor; aggregate
never-quad 90.2–92.5% (cycles) / 98.2–99.3% (passages) across all arms; quad_calls per
landed panel 27.6× / 12.1× at rtf 100.]

## Refuted

- **"The two headline numbers measure the same traversed fraction, so one run is
  wrong"** — refuted: both reproduce in one run; they are panel-landing share vs
  lifetime share (20261020-1729-spacex-65b8).
- **624a's "a lazy/streaming compile deletes most of the mint wall (4–7×)"** — refuted
  as stated: lazy compile needs the full-arc totals the engine reads one step later
  (`step_for` → `period()`/`duration()`; the totals are the mint's own last-knot sums),
  so laziness alone prices no CPU; the cut exists only behind Carlson O(1) totals, and
  is then sized by traffic (~10×), not by 1 − walk (20261020-1729-spacex-65b8;
  1991's kill argument, now structural).
- **1991's "cycles walk 10⁻³ of the arc, so the mint serves ~10⁻³ of the orbit"** —
  refuted as a consumption claim: the binding LIVES < 1/64 of a period but its
  quadrature traffic spans 6.6–19.9% of the arc's panels (planning bisections and
  reflection read outside the lifetime window); consumption is traffic-driven,
  cadence-decoupled below 1/64 (20261020-1729-spacex-65b8).
- "The kick's cost and the live-memory plateau are independent gaps" — refuted as one
  object by bd4b (ρ 0.70–0.92 µs↔knots, 85–91% of mint heap); the Carlson case
  (closed-form-kernel) composes as the totals-first half of the same lever.
- "If members rebind inside their arcs, lazy knots save the unread fraction; if cycles
  traverse it all, the saving is passage-class only" — both branches dead: no class
  traverses its span by lifetime (624a's census, 0 of 21,449 at coverage ≥ 0.9 with a
  full-walk control; 1991's span census composes), and the panel-level saving is
  traffic-priced, not class-priced (20261020-1729-spacex-65b8).

## Open directions

1. **The composed flight:** Carlson O(1) clock totals (cycles) + traffic-priced lazy
   panels, on the kick bench — the experiment neither earlier run priced correctly;
   ~10× ceiling on the mint's quadrature wall, store lever near-total behind it.
2. **The belt case, bounded:** no level-0 mint exists on shipped code (ships only, the
   belt unwired); at one-kick-per-period with per-frame reads a body traverses its
   table (laziness belt-neutral exactly there). Settles fully only when the belt is
   wired or a level-0 arm is forced.
3. **The allocator side:** 12.5 KB/kick of Arc<Vec> churn — price with the standing
   counting GlobalAlloc on this scene (f623/8994 hold the measured per-kick heap-call
   family).

## Contradictions

None open (the 1991-vs-624a conflict is resolved above). Adjacent standing facts that
compose: kick keys never recur (9edc, 225d — sharing/interning dead), knots regenerable
from the key (5465), the memo a private cache per binding — so its extent (not its
sharing) is the lever, and the extent's consumption is traffic, now measured.

## Runs
- 20261020-1116-system-bd4b (system, awaiting grade): the mint's knot vector measured kick by
- 20261020-1116-system-bd4b (system, silver): the mint's knot vector measured kick by
- 20261020-1210-second-20261020-1116-system-bd4b-1991 (second author): the checker's
- 20261020-1210-spacex-624a (spacex, awaiting grade): the traversed fraction measured —
- 20261020-1116-system-bd4b (system): the mint's knot vector measured kick by kick
- 20261020-1210-spacex-624a (spacex): the traversed fraction measured (landing share)
- 20261020-1210-second-20261020-1116-system-bd4b-1991 (second author): lifetime span
- 20261020-1729-spacex-65b8 (this run): conflict adjudicated — landing share vs lifetime
