# Dossier — 20261016-1120-scout-79ed (scout lens, topic: binet-cells)

## Claim

The per-band u_k refit is priced on the frozen r1 sampler: the **one-law form** (every
visited band's constant = the geometric mean of the u-extremes the orbit itself attains
inside that band, a self-consistent fixed point — *identical to the frozen centre for
every band the orbit merely crosses*) lifts the frozen 256-seed sampler to **256/256
precession at every m ∈ {8, 16, 32}** — including **m=8, which the frozen law fails on 6
seeds (250/256)** — at **−25% median advance error** (1.45e-4 vs 1.83e-4 at m=16; 5.52e-4
vs 7.68e-4 at m=8), with unchanged crossing counts and exact cycle-2 repeat (16/16). The
measured price: the refit moves the two turning bands' constants of essentially every
bound orbit (256/256 seeds' advances change by >1e-6 relative at m=16; 242/256 at m=32),
so it is a **canon change, not an overlay**; the letter's contained-only form (fe85's open
direction 2 as written) never fired on this draw (0 seeds changed at m=16) and carries no
measured win here.

## Bottleneck

Bottleneck 0 (the representation; board: "the representation, from scratch … fixed-bit
cells in a dyadic tree"). docs/representation.md names Binet cells "the primary in-cell
solution" and freezes m=16 as the default; fe85 measured the near-circular first-order
family and concluded "m=32 or a per-orbit u_k refit is the measured minimum". This run
prices the refit: if the refit holds, the cell width for the near-circular family is set
by the second-order term, not the first — one m-doubling of headroom (half the crossings,
half the constant-count per orbit at equal behaviour), and the frozen sampler's one-seed
margin at m=16 disappears. Order of magnitude: behaviour-qua-lifting, not a 10× cost cut;
its value is deleting fe85's "m=32 minimum" constraint on the primary in-cell law.

## Evidence

All numbers regenerate: `regen.sh` (≈10 s) → `report.json` + the console table below.

```
m=8  FROZEN: prec 250/256 per 252/256 cr_med 18 adv_changed   0 med_err 7.68e-04
m=8  CONT:   prec 252/256 per 253/256 cr_med 18 adv_changed   3 med_err 7.63e-04
m=8  GEO:    prec 256/256 per 253/256 cr_med 18 adv_changed 256 med_err 5.52e-04
m=16 FROZEN: prec 255/256 per 256/256 cr_med 34 adv_changed   0 med_err 1.83e-04
m=16 CONT:   prec 255/256 per 256/256 cr_med 34 adv_changed   0 med_err 1.83e-04
m=16 GEO:    prec 256/256 per 256/256 cr_med 34 adv_changed 256 med_err 1.45e-04
m=32 FROZEN: prec 256/256 per 256/256 cr_med 68 adv_changed   0 med_err 4.41e-05
m=32 CONT:   prec 256/256 per 256/256 cr_med 68 adv_changed   0 med_err 4.41e-05
m=32 GEO:    prec 256/256 per 256/256 cr_med 68 adv_changed 242 med_err 3.81e-05
repeat (cycle 2 == cycle 1 to 1e-12, 16 seeds): 16/16 every arm
crossings median: identical across arms at every m (18/34/68)
```

- **Instrument:** float64 re-implementation of the r1 Binet band map as frozen (bands
  r_k = 2^{k/m}, u_k at the band's geometric centre, exact per-band sinusoid segments,
  u and u′ continuous, dt/dφ = E/(L·u²(1−2u) integrated per segment by GL16). Oracle:
  ports of the shipped `xtask/src/gr_oracle.rs` `periapsis_elliptic` (including the
  m<0.25 series form of K−π/2) and `gr_oracle_extended.rs` `bound_constants` +
  `bound_period_quad` (same doubling rule), verified in form against the sources.
- **Calibration on the record:** FROZEN m=16 median advance error **1.83e-4 — exactly
  fe85's number** — and the frozen pass-count pattern (255/256 at m=16, failures
  concentrating at m=8) reproduces theirs (252/256 at m=8; my draw reads 250 — the
  sampler's redraw detail differs; both instruments agree the m=8 failures are the
  near-circular family plus its tail).
- **Arms:** FROZEN (the r1 letter); CONT (fe85's letter: refit only an orbit contained in
  one band, from one frozen pass); GEO (the one law: u_k = √(min·max) of the attained
  extremes per visited band, iterated to a fixed point, ≤12 rounds, |Δu_k|<1e-15 —
  crossing bands give the frozen value *exactly* by construction, so the law has no
  regime branch).
- **Instrument limits, stated (these rows are NOT claimed):** the deterministic e=0
  circle family (GEO arm reads a residual walker defect, 2.0e+01 worst; CONT never fires
  there — containment test defect), the strong-field held-out rows (8.5/0.9 etc., NaN —
  the hyperbolic-band turning-at-entry path), capture classification (5/10 misclassified
  in **every arm including FROZEN**, i.e. an instrument defect at the E=1/L=4 threshold
  band, not an arm effect), and the ISCO rows (probe wrong: 'plunge' in both cases).
  Consequence: predictions P2, P4, P5 and the pre-registered kill bar are **undecided by
  this instrument**, not passed.

## Predictions

`predictions.md` was written before the decisive run. What happened: P3 held (GEO 256/256
precession at m=16; m=8 period 253/256 = 0.988 < 0.99, exactly the "uncertain, may stay
below" call); P6 held (256/256 advances change at m=16, 90–100% band); P1 partially held
(frozen m=8 250/256 vs fe85's 252 — draw detail); P2, P4, P5 and the kill bar are
undecided — the instrument rows that would test them are the broken ones listed above.

## What would make it wrong

- The sampler draw: my redraw rule ("reject and redraw" both p and e) may differ from the
  frozen sampler's; the frozen-side anchor (1.83e-4 median, 255/256) matches fe85, which
  bounds the drift, but a checker should re-derive the draw order before freezing any
  rung on it.
- The win is measured on precession and repeat only; the period channel shows no GEO gain
  (253/256 at m=8 for both), so the refit does **not** yet license m=8 — only removes the
  precession constraint. The m=8 period failures are the open second-order tail.
- The refit is a canon change (every orbit's turning bands move). If the integrator wants
  bit-compatibility with the frozen law outside the near-circular family, the one-law
  form is disqualified by construction and only a contained-only form remains — which
  this draw could not exercise (0 firings). The next run must fix the circle-family
  instrument to decide between them.
- The fixed point's integer form (exact per-band rationals) is argued, not measured; the
  compile-time cost of ≤12 extra walks per orbit is unpriced in the engine's units.

## Cost of adopting, fit with PRINCIPLES

Adoption is a law-constant change inside `docs/representation.md`'s Binet cells: no new
state (u_k derives from the orbit's own attained extremes — a function of state the walk
already computes), no per-crossing cost (constants resolve at band entry), canon reset
required (advances move). Fit: "A fix signals the wrong representation" (19) — the
first-order family was the band-centre *representative point*, not the law; the refit
chooses the point from the fish's own attained range ("we know we have a fish, we need to
find its water"). Prior art with the same structure: WKB's Langer correction (the
half-index shift that cancels the next order — a representative-point choice), Hsu's cell
mapping, exponential integrators (freeze the linear part per cell, solve exactly).
Against: "regimes are chosen by dimensionless numbers" (4) — the one-law form needs no
regime branch, which is its elegance; the contained-only form would need one.

## The lens (what the scout lens may have missed)

The scout lens searched for the mechanism in other fields (WKB/Langer, cell mapping,
exponential integrators) and priced it on the frozen instrument — but it built its own
walker, and four of its seven channels (circles, strong-field, capture, ISCO) are
instrument-broken; a components-lens run with the shipped-law harness (or fe85's own
code, on its branch) should re-measure the circle family and the strong-field rows before
any freeze. The run also spent its budget on instrument debugging rather than a second
held-out family (e.g. Rayleigh-e belts, the engine's actual population).
