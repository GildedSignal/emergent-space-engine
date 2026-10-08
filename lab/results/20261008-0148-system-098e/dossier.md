# Dossier — the news cursor is a repair; the cell's version ring is the thing

Run: 20261008-0148-system-098e, lens: the whole system. Linux x86 cloud box;
orders of magnitude only.

## Claim

The queued news-gravity build's **cursor per (body, source)** is a component
that exists only to repair the absence of the cell layer: one structure — the
doll's ring cells holding **per-source version rings read at an integer lag
table** (lag = max-distance between the cell pair / c: the ring lattice's own
light cone) — carries gravity-at-c, the never-built multipole store (H0196)
and the causality certificate (engine.md rule 11) in one object, deletes the
cursor's per-pair state and per-pair tests, is never early, and its
quantization error is bounded at **≤ 3.4 source-cell light-crossings** with
orbital behaviour held to 1e-9 in the falsifying toy.

## Bottleneck

Not a cost rung: an architecture decision that is about to be taken wrongly.
`lab/lenses/b-news-gravity.md` (queued) prescribes "a cursor per (body,
source) and a version ring"; `docs/HANDOFF.md` risk list and H0196 record that
the multipole cell layer Julien asked for ~10 times was never built. Building
per-pair cursors now builds the repair a second time. Numbers at belt scale
(0.7–50 AU doll = 99 rings × 128 spokes = 12,672 cells, S = 10 sources, ring
depth 4):

| N bodies | cursor state | cell rings | state ÷ | tests/kick ÷ |
|---|---|---|---|---|
| 2^20 | 10.5 M words (84 MB) | 0.51 M words (4 MB) | 21× | 83× |
| 2^23 | 83.9 M words (672 MB) | same 4 MB | 165× | 662× |

Tests: cursor does N·S per kick; cells do cells·S per epoch, bodies read their
cell's merged version (the kick already visits the body). The lag table is one
static per-doll integer table (ring, ring, Δspoke) → lag, built once, read
per kick — no per-pair sqrt, no per-pair bookkeeping.

## Evidence (each command ≤ 60 s)

Toy (`toy_news.py`): star + one thrusting planet (μ=1e-3) + test receiver
(a=1.9, e=0.05, 16 phases); the source's tube changes by impulsive dv; the
receiver is pulled toward the seen tube extrapolated to now (law.md's "gravity
is news"). Laws: instant (the plane today), exact (per-pair light cone), cell
(lag = max cell-pair distance / c), laplace (retarded position — control).
Kepler propagator exact (ΔE ≤ 8e-14, RK4 cross-checked).

- `python3 toy_news.py c30` — impulsive dv=0.03 at t=5, c=30 AU/yr
  (β_p=0.033), 16 seeds, 12 yr:
  - exact vs cell: max |Δa|/a = **9.4e-9**, max |Δe| = 9.3e-9
  - instant vs exact (the delay the plane ignores today): 2.4e-6 (250× larger)
  - laplace control: 2.0e-4 (separates by 2×10⁴; it fails as it must)
  - arrival delta (exact − cell): −1.8e-3…−4.1e-3 yr, **never early** ✓
- `python3 toy_news.py c300` — c=300: exact vs cell = **5.0e-10** (scales ~1/c)
- `python3 toy_news.py per` — 201 alternating dv=5e-4 every 0.01 yr (period ≈
  the smear), 9 yr: exact vs cell = **2.6e-10**; laplace 1.9e-4 (still fails)
- `python3 smear.py` — 31,680 cell pairs (rings m=16, 128 spokes, 0.7–50 AU):
  **absolute lateness (max−min distance)/c = med 2.74, max 3.36 source-cell
  light-crossings at every separation** (bins 0–1 to 20–60 widths all ≈ 2.3–3.0).
  Relative smear ≈ 2/s (s = separation in cell widths): 63% at 4–6 widths,
  14% at 20–60.

## Predictions

`predictions.md` was written after tuning on one case only (c=30, 3 seeds,
8 yr); everything above was held out. **7 of 8 held.** Prediction 7
(relative smear < 10% beyond 3–4 cell widths, < 2% beyond 10) is **falsified**:
relative smear stays ≈ 2/s at all scales. The corrected invariant is stronger
and is the useful law: the never-early cell lag is *late* by at most ~3
source-cell light-crossings, independent of distance — the lattice's own time
unit ("a cell's time unit is its light-crossing time", representation.md §1).
Error type: bounded, one-sided, zero in the steady state (undisturbed sources
give identical fields under all three laws — no news, no work).

## What would make it wrong

- The toy is Newtonian with exaggerated c (β_p ≤ 0.033) and one changing
  source; real delays are ~2000× smaller (c = 63,241 AU/yr), so absolute
  errors shrink correspondingly — but so does the signal the plane currently
  ignores, in the same proportion.
- **Fast sources** (the lens blind spot): the seen tube extrapolates exactly in
  free fall, so error enters only through changes; during a change of
  acceleration Δa lasting T, the response error is ≤ lateness × β_source ×
  the field change. At β → 1 this is the same family as B16's static-memo lens
  error; it must be regime-gated (β_source above a dimensionless threshold →
  exact per-pair lags).
- **Near encounters**: at 1–2 cell widths the relative smear is O(1); the
  exact pair layer must own separations below ~4 cell widths — the design
  already routes close encounters to exact pair events (m-meso-motion).
- Comparable-mass binaries: q-gravity-at-c found news itself fails there at
  high e; inherited, not retested.
- The lag table is per-doll static and integer in the design; the toy sampled
  it in float. Same-ring pairs across the disc (Δspoke large) make the table
  wide but it stays O(rings² × spokes) built once.

## Cost of adoption

`b-news-gravity` builds per-cell version rings + the static lag table instead
of per-pair cursors: strictly less state (21–165× at belt scale), fewer
integer tests (83–662×), and the same structure is the multipole moment store
and the cells' certificate expiry (a cell's news validity = the next lag at
which a reader may need a newer version) — H0196's layer and engine.md rule
11's causality regions arrive with it, for free. The exact per-pair light cone
survives only inside the encounter layer.

## Fit with PRINCIPLES

- 7: "Multipoles are the mechanism, for gravity and for causality regions
  alike" — this is that one mechanism, one structure for both.
- 23: "beyond c=1 means paradoxes" — max-distance lags are never early by
  construction, machine-checkable (never_early=True in every run).
- 3: "Compute only surprises" — undisturbed sources cost nothing: identical
  fields, no cursor traffic.
- 33: "a body resolves only the influences that are significant at its own
  scale" — lateness is bounded by the source cell's own light-crossing.
- H0196: build the asked-for thing, not its repair.

## The lens

The unification is argued at design level with a float toy; the measured
per-pair cost it deletes is small today (one integer test per kick,
q-gravity-cursor), so the near-term win is state at scale and one structure
where three were planned — not engine milliseconds. A cost-driven checker
could fairly call that silver until the multipole layer needs the rings
anyway. Also: I judge behaviour of a toy, not of `crates/universe`; and the
receiver's cell was taken at event time (arrival-time cell is the engine's
choice; smear dominates either way).
