# Dossier — 20261017-2330-quant-588d (quant lens)

## Claim

The fit-compile memo's sharing is measured on flown inputs: the exact `ShapeMemo`
is dead on the whole fit path (hit 0.0001, not just on kicks), while the shape
*class* the quantized memo actually shares hits 99.2% from ~1.2–1.5k classes that
saturate in N — a population-level cache of MB-scale, priced and ready for the
one law decision (quantized key vs exact-key/quantized-shape) that memo.rs
already owns.

## Bottleneck

Board: "the kick: 75–160 µs against a ~50 ns floor" — the fit's compile is 49%
of the fit stage (d399: 12.33 µs/call on flown keys), and read-stream's open
direction 2 named the unmeasured gate: "measure shape-key sharing on flown fit
inputs before designing anything". This run is that measurement. Expected gain
(order): up to the compile's share on 99.2% of calls if the shape can be served
without a re-quadrature; the exact split (shared quadrature vs per-key glue) is
the next measurement, not claimed here.

## Evidence

Instrument: print-only, env-gated (`FIT_CENSUS=1`) census at `from_state`
(`space/src/binding.rs`, the one fit entry the kick/scan paths own), counting
three levels per cycle fit: exact `ShapeKey`, the 44-bit `MemoCode`, and
`MemoCode::shape_bits` — the key `QuantizedMemo` actually shares `Arc<OrbitShape>`
by (17 bits on the weak branch). Patch = work/patch.diff (binding.rs, orbit.rs
`shape_bits` made `pub(crate)`, nladder's `proc_pid_rusage` cfg-gated to macOS
with a /proc stand-in so the ladder links on Linux). Linux/x86, 8 vCPU, load
ambient, single-threaded flights, each ≤ 55 s.

Controls, both sides:
- **Digest identity:** `ladder_digest "N=3000 coast through"` — pristine vs
  patched-census-off vs patched-census-on: digest `d2632de90255f5c10de9fd7372a3790d`,
  kicks 34537, encounters 934, contacts 0 identical in all three (wall seconds
  differ: 27.5/27.6/27.3 s); no panic/abort in the census-on run.
Regeneration: `regen.sh` was run end to end by the author (207 s): both digest
controls IDENTICAL again, all four arms reproduced with hit rates equal to the
third digit (exact 0.0001-0.0002, quant 0.9340-0.9921, shape 0.9784-0.9924);
the cycle totals move ±3% with the 55-s wall truncation (the flights are
wall-cut, not frame-cut) — the hit rates and class counts are the invariants.
- **Positive control (N=0 plane, 28 bodies, 1500 frames):** quantized hit 0.9921
  > 0.9 and exact hit 0.0017 < 0.05 — memo.rs's standing law reproduced by this
  census at a different call site (all fit entries, not kicks only).

Census (regen: `regen.sh`; totals from the flights' own `FITCENSUS totals` line):

| arm (coast) | cycle fits | passages | exact distinct (hit) | quant distinct (hit) | shape distinct (hit) |
|---|---|---|---|---|---|
| N=0, rtf 1800, 45,000 game-s | 8,692 | 1,348 | 8,677 (0.0017) | 69 (0.9921) | 66 (0.9924) |
| N=3000, rtf 1800, 99,000 gs | 157,474 | 1,650 | 157,454 (0.0001) | 4,562 (0.9710) | 1,223 (0.9922) |
| N=10000, rtf 1800, 99,000 gs | 179,992 | 1,650 | 179,972 (0.0001) | 11,575 (0.9357) | 1,491 (0.9917) |
| N=3000, rtf 600 (held-out pace) | 53,866 | 1,014 | 53,853 (0.0002) | 3,468 (0.9356) | 1,161 (0.9784) |

`quant_err=0` everywhere (every cycle key encodes). Saturation trail (classes
vs calls): N=3000 1,160 @32k → 1,223 @157k; N=10⁴ 1,427 @32k → 1,491 @180k —
log-shaped, not per-body. Quant cells ARE per-body-scale: 4,562 ≈ 1.5/body at
3,028 bodies, 11,575 ≈ 1.15/body at 10,028. Shape bytes: `OrbitShape` header
224 B + knots 88 B each (envelope example; flown tables 6–10.9 KB per d399) —
1,491 classes ≈ 1.5–16 MB at N=10⁴, three orders under any budget.

Instrument artifact worth recording: in the multi-schedule digest control the
per-thread census's exact distinct count collapsed 32,756 → 34,203 between 2¹⁵
and 2¹⁶ calls (≈96% exact recurrence in that stretch) — the exact keys recur
only because the digest re-flies the identical case on its 4 schedules inside
one process. Any census taken inside `ladder_digest` inherits that recurrence;
the arms above are single flights. (New instance of the memo-artifact lesson:
agreement across schedules is not independence.)

## Predictions

`predictions.md`, written before any run. P1 (exact hit > 0.5 on the belt,
boundaries re-fitting unchanged orbits) **failed** — hit 0.0001: boundaries
never re-enter `from_state`; their identical plans are carried state, which
confirms 3570's no-op reading at a new site and kills the exact memo on the
bind path too. P2 (shape hit ≥ 0.95) held (0.9922). P3 (classes sub-linear,
≤2× for 3.3× bodies) held (1,223 → 1,491 = 1.22×). P4 (N=10⁴ within 0.02;
rtf-600 shape hit within 0.05) held (0.9917; 0.9784 — the quant hit moved
0.035, the shape hit 0.014). P5 (N=0 negative/positive controls) held.

## What would make it wrong

The census counts fits, not the compile's internals: if `OrbitShape::bound`
turns out to be a small share of the 12.33 µs compile (the rest per-key glue),
the 99.2% hit deletes little — the split is unmeasured and is the run's named
next measurement. The hit rate is scoped to the ladder's coast belt
(2–3 AU, Rayleigh e births, ~1–6 kicks/body in window); a stirred belt
(04d7's 11–12-orbit re-key) or a driven belt can mint classes faster — the
saturation trail here never left the birth program's coverage. Adoption needs
one law decision: serving the shape needs either the quantized key (memo.rs's
known 2⁻¹¹-period law change) or `Orbit::from_shape(exact key, quantized
shape)`, whose exactness is unmeasured. Fit with PRINCIPLES: "Compute only
surprises" (3) — a 99.2%-repeated quadrature is the definition of derivable
when looked at; and "a fix signals the wrong representation" (19) — the wrong
turn would be caching harder at the exact level, measured dead twice now.

## The lens

The quant lens priced a cache like a trading system prices a memo table: hit
rate, key count, bytes, and the multiple-testing trap — the digest's
cross-schedule exact recurrence is exactly the "agreement is not independence"
failure mode, caught because the control was three-way. What the lens may have
missed: the exactness question (from_shape(exact, quantized shape)) is a
physics question, not a cost question, and belongs to the law's owners.
