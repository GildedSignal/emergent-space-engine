# Dossier — 20261020-1210-second-20261020-1116-system-bd4b-1991 (second author on bd4b)

## Claim

The checker's named gold experiment is done — per-class SPAN coverage is measured, it
splits the unification's lever in half, and it kills one half: **a minted binding walks
0.04–0.6% (cycles) to ~60% (passages, in phase; 12–15% in panels) of the arc it compiles
before the next rebind, so 85–98.5% of every mint's panels are never interpolated — but
the walk cannot price a lazy COMPILE, because the traversal is load-bearing for the clock
totals, not the readout; the span lever is a store/readout lever (already flown as
b9ae/0757, now sized near-total on the kicked classes), and the kick's CPU lever stays
with the Carlson basis and the passage thinning.**

## Bottleneck

The board's two worst rows (kick 75–160 µs vs ~50 ns floor; memory per body vs ~6 B) were
unified by bd4b as one object, the knot vector. The checker held gold back on one missing
measurement: the traversed fraction (phase at next rebind ÷ compiled span) per class. It
decides whether a class-split/lazy compile rule prices a real deletion on both rows that
the composed Carlson case does not already own. This run is that measurement; it either
sizes the lever or kills its practical content — it does both, one half each.

## Evidence (Linux/x86, shared box — orders of magnitude only)

Instrument: bd4b's print-only census (`work/patch.diff` of bd4b, kept bit-for-bit in
`work/base-patch.diff` and extended): per fired kick that mints, the census holds the new
`Binding` and closes the row at the body's **next planned kick** — the plan's own next
`Kick` item (exact), or the next `Boundary` plus half its interval (estimate) — reading the
walk with the shipped readout (`Binding::orbit_state`), capping passages at the release
radius (a tube is compiled to 2× the doll edge; the ship is handed back at the edge), and
counting never-read panels exactly from the knots' own `psi` values, bracket-aware (a read
touches the panel containing it). No engine code touched; the original census fields
regenerate identically.

Commands (each ≤ 60 s, from the repo root with `work/patch.diff` applied), or `regen.sh`
for all of it in ~2 min:

```
cargo build --release -p xtask -p emergent-universe --example nladder
$CARGO_TARGET_DIR/release/xtask universe --kick-bench --seconds 10
$CARGO_TARGET_DIR/release/xtask universe --kick-bench --members 400 --seconds 30 --seed 1|2|3
```

- **Controls.** Seed 1 digests regenerate the shipped record bit for bit: default
  `b42da477294f7619` / replay `a693ac68cbc7fb46`; m400 `8c242b023e8b79e4` / replay
  `0de3a82c1926a83d`; `refused == 0` on every arm; mints 23/137, kinds [23,0,0] and
  [55,82,0], 12.5 KB/mint — the span census is print-only. Seeds 2–3 held the structure
  (below).
- **The walk (m400, seeds 1/2/3).** Coverage = phase walked to the next rebind ÷ compiled
  span; never-read = panels outside the walked arc's bracket:
  - **made cycles**: coverage median 0.23%/0.12%/0.11% (max 0.7%); never-read **85–87%**
    of minted panels (seed 1: 152 of 175).
  - **member cycles**: coverage median 0.042%/0.11%/0.05% (max 3.4%); never-read
    **97–98.5%** (seed 1: 5,388 of 5,480 knots).
  - **member passages**: coverage median 0.62/0.58/0.61 of the ψ span — but never-read
    **85–88% of panels**: the ψ-band ladder concentrates panels toward the outer turning
    point, exactly where the walk stops. Release overhang ≈ 0.1% of ψ (release_capped 0
    on every seed): compiling to 2× the doll edge adds almost no panels — the panel mass
    is the turning-point ladder's density, not the radius span.
    Reading note: ψ is a fast coordinate near the turning point — the member passages
    mint deep in the slow zone (ψ₀ ≈ 0.8–0.9 of the span) and the next kick catches them
    at ψ₁ ≈ 0.95, so the ψ-coverage overstates the time walked (a few percent of the
    remaining duration); the never-read panel count is exact and unaffected.

- **The tail correction, folded (checker's point 4).** The biggest mints are cycles at
  coverage ≤ 1e-4: seed 1's 448-knot mint walks 5e-7 of its arc (446/448 panels never
  read), 257→256, 196→194; seeds 2–3 same shape (185→174, 346→345). The tail is
  clock-traversal cost with zero readout value.
- **Why the walk is so short (the cadence fact).** The next planned kick after a mint is
  a sub-kick of the nested split, ~interval/8 away (12/23 made rows close on an exact
  `Kick` item; members' next kick is planned at the following boundary, estimated as
  boundary + interval/2). The belt's one-kick-per-period is the level-0 cadence only; the
  levels underneath rebind 8–64× per period, so a fresh mint serves ~10⁻³ of the orbit.
  This refutes bd4b's own expectation (and my P1) that cycles traverse their whole arc.

## Predictions

See `predictions.md` (written before the decisive run). P2 held (passages ≥ 30% never
read: measured 85–88%). P4 held (the tail is cycle-class) and sharpened (it is 99.6%
never-read). **P1 failed informatively**: cycles were predicted to walk ≥ 90% of the arc
(belt cadence); they walk ~10⁻³ — the plan's nested levels, not the period, set the
rebind cadence. **P3 failed**: the release overhang is ~0.1% of ψ, not ≥ 20% — the 2×
compile-out is nearly free in panels. The pre-registered kill criterion (P1 and P2 both
≈ 0 never-read) did not trigger.

## What would make it wrong, adoption cost, fit

Wrong if: the member rows' estimated close tick (boundary + interval/2, all 137 member
rows) is off by orders of magnitude — it cannot be (the estimate is within one step of
the plan's own boundary, and a step change at a boundary moves the next kick by ≤ 2×);
or if a reader between mints walks beyond the mint→next-kick span — impossible on this
law: every read (view, replay, drift) is at a tick inside the binding's life, and the
walk is monotone in elapsed time, so every read's ψ lies inside the measured arc. The
plan-prediction control (observed next mint vs planned tick) never exercised: no body was
minted twice inside a 30 s window.

**The decision the experiment makes.** The unification (two rows, one object) stands,
now with the object's two extents measured and 10²–10³× apart:
- **The CPU half of the span lever is killed.** The compile's full-arc traversal produces
  the clock totals (advance/period/duration from the last knot's running sums;
  `step_for` reads `period()`/`duration()` inside the binding's life (at the mint for clock-stepped bodies, at the interval's boundary otherwise) to set the interval), so
  compiling only the walked span cannot produce the clocks the engine needs a step
  later. Lazy compilation does not cut the kick's CPU bill — the branch bd4b's own "what
  would make it wrong" named, now measured. The CPU lever remains the Carlson basis
  (cycles, standing) and f9b4's static thinning (passages) — and this run grades that
  thinning: the panels sit in the never-walked outer bands, so thinning there first
  captures most of the passage compile.
- **The store/readout half is sized near-total.** 85–98.5% of minted panels are never
  interpolated before the next mint; the readout's working set per binding is one
  bracket (~2 knots). This generalizes b9ae (standing knots → 0, digest-identical) and
  0757 (bounded cache, gold, 962 B/body) from the nladder population to the kick bench's
  minted classes, and prices the retired-history ratchet (bd4b's keys-only retention):
  the arc a Segment retains was 85–98% unread even while live.

Cost of adoption: none new — the memory-side change is already flown (0757 gold); this
run supplies its per-class sizing on the kicked classes and the reason it is safe. Fit
(PRINCIPLES): "Compute only surprises" (3) — 85–98% of the mint is pre-computed reading
that never happens; "Store the generator, not the generated" (6); "the right question,
then the representation" (18) — the question "who reads the arc before the next mint" is
answered: the clocks write it, nobody reads it.

## The lens (what this lens may have made me miss)

A second author inherits the scene: one plane, 30 s, ≤ 400 members. A member re-kicked
inside its own passage arc (longer windows, the cadence ladder's territory) is
unmeasured — but it could only raise coverage above the measured 0.6 cap, shrinking the
lever further, so the conclusion is monotone-safe in that direction. The census prices
panels, not allocator churn (f623/8994 own that), and plunge mints are absent (0 on this
scene). The deepest miss risk is structural: "span coverage" is measured against the
next KICK because the bench sees kicks; a non-kick rebind (capture) ends a walk earlier,
which this census would overcount as read — conservative for a deletion claim.
