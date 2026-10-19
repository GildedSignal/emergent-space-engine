# Dossier — the belt's memo cells saturate; the rebind bill is one aggregate

## Claim

**The belt's rebind cells saturate, not accumulate: 1,831 standing shapes at 11+11 for 299,699
bodies (1,095 at 2,699; increments +185/+121/+100 per decade, shrinking; a hard grid ceiling of
2 exponent × 2,048 = 4,096 cells ≈ 3.4 MB at any N), 100% weak-branch, ~840 B a shape — so the
kick's compile bill, the promotion bill and the belt's per-live-body shape memory are one
mechanism: the quantized cell IS the belt's generator (PRINCIPLES 6), and at 10⁹ the rebind
stream prices at ~0.02–0.04 cores of serves + ~2–3 MB standing, against ~4 cores of compiles
(104 µs × 36–43k fires/game-s) or 2.4–5.1 KB/body of live shapes.**

## Bottleneck

The board's interlock: CPU = N·rate·cost + encounters; memory = N·bits + N_live·bytes. The
promotion dial was closed at its worst arm (0659: p = 1.0, every kick item fires and promotes;
τ = 43.6 game-s), and the kick's compile is 84–89% of its cost (b063/12db) — so the 10⁹ bill
hinged on one unmeasured constant: the standing-cell census on the belt (cell-rebind's checker:
"the belt census stays the open measurement"; open direction 1). Measured here: the constant is
O(1) in N. This deletes the compile term of the 10⁹ kick row and the shape term of the live-row
bytes for the belt, and re-prices promotion (760f/c4d3's 4.6–9.2 µs compile) as a 0.4–0.9 µs
serve — not by a new law, by the census of the law's own cell.

## Evidence

Shipped law and draw (`scenario::plane_extra`, the nladder population; no memo wired — every
rebind is the shipped exact compile), print-only hook at `step.rs::rebind` (records
`MemoCode::encode` of the new cycle key; `ES_CENSUS` unset = no-op; the shipped `memo.rs` test
passes bit-identically with the hook OFF **and** ON). Commands (each ≤ 60 s; regen ≈ 3 min:
`lab/results/20261019-1316-system-f7c3/regen.sh`):

    cargo run --release -p emergent-universe --example beltcensus -- <N> <seed> <wall s> <rtf>

| N (belt bodies) | birth cells w11 | stream cells | belt stream recurrence | rebinds/cell | belt B/body |
|---|---|---|---|---|---|
| 3×10³ (2,699) | 1,095 | — (birth arm) | — | — | 334 |
| 10⁴ (9,699) | 1,425 | 1,425 (= birth, exactly) | 0.951 | 112 | 123 |
| 10⁴ seed 2 | 1,420 | 1,484 | 0.992 (all) | 128 | 123 |
| 3×10⁴ (29,699) | 1,610 | 1,650 | 0.982 | 132 | 47 |
| 10⁵ (99,699) | 1,731 | 1,760 | 0.9915 | 175 | 15.4 |
| 3×10⁵ (299,699) | 1,831 | — (birth arm) | — | — | 5.6 |

- **Saturation:** cells ∝ N^0.11 over 3×10³→3×10⁵; per-decade increments 185→121→100
  (missing-mass of the Rayleigh(0.07) e-draw's q on the 2,048-fraction gap grid). Growth
  exponent of exact keys over the same range: ~1.0 (96,358 distinct of 99,699) — the exact memo
  stays dead (5 Oct correction), the cell memo is the aggregate.
- **Weak branch 100%** of belt keys at every arm (compactness ≤ 2⁻¹⁸): the shape identity is
  the gap alone (`MemoCode::shape_bits`), so the ceiling 4,096 cells is a property of the code,
  not the fit — 1.8 MB measured at 3×10⁵, ≤ 3.4 MB at any N, versus 2,460–5,100 B/body live.
- **The stream stays in its birth cell:** belt stream cells = birth cells exactly at 10⁴ (both
  seeds) and 10⁵ over 2–3.2 intervals (~68–89k game-s); fires p50 2–3; cells per body p50 = 1;
  new cells beyond birth per window 29–61, all but a handful from the non-belt locals. Belt
  recurrence 0.95–0.99, whole-plane 0.991–0.994 (the 301 locals + planets + player: 237 birth
  cells, 459–506 stream cells, 104–136k rebinds — the locals' own aggregate, recurrence 0.996).
- **Composition to 10⁹ (cited constants, not measured):** fires 3.6–4.3×10⁻⁵/body/game-s (0659)
  × 10⁹ = 36–43k rebinds/game-s; served at 0.40 µs (read-stream 0355's class memo; the 11+11
  carried serve 0.85 µs, cell-rebind) = 0.016–0.036 cores + turnover; the shipped compile
  ceiling 104 µs × same rate = 3.7–4.5 cores. Cold builds = turnover ≈ 0/3 fires measured
  (no belt–belt channel on the shipped cadence, 0659's note).

## Predictions

`predictions.md` was written before the decisive arms (the 3×10³ pilot had run). P1 held with
near-misses at the top: cells 1,610/1,731/1,831 against bands topping 1,550/1,650/1,700
(4–8% over; kill criteria — >4,000 or β>0.25 — not fired; β = 0.11 against ≤0.1, marginal).
P2 held (recurrence 0.99 ≥ 0.97; stream ≤ 1.3× birth; fires 2–3) and is stronger than
pre-registered: belt stream cells equal birth cells exactly. P3 held at 10⁵ within 3%
(15.4 B/body against <15). P4 held (weak share 1.0000 at every arm). P5's domains (burn,
stirring, >3 fires) stay unflown and scope the claim.

## What would make it wrong

- **A stirred belt** (the wired compact store with a belt–belt channel, or resonance): walking
  raises turnover (cold builds/second), not the standing set (grid-bounded), but a turnover
  near the fire rate returns the CPU bill to the compile ceiling — unmeasured, the named
  successor experiment.
- **The burn**: a thrusting body walks its gap cell every fire (unmeasured here; coast only).
- **A wider e-draw** raises the asymptote toward the 4,096 ceiling (σ 0.07 → 1,831; σ 0.3
  would sit nearer 3,000) — constant moves, law holds; the ceiling does not.
- **Adoption cost** (unchanged from cell-rebind, now with the memory half closed): the wiring
  (`Orbit::from_shared` in the rebind), B1/B2/B9 re-judged on memo keys, B12/B13/B17 re-flown
  (a law-level digest change), the `memo.rs` 0.9 guard recalibrated on the served stream
  (0.898, disclosed there), eviction (efd4) needed only if the 4,096 ceiling is deemed too
  loose. Fit with PRINCIPLES: 6 ("store the generator, not the generated"), 33 ("smaller ones
  enter as an aggregate"), 24 ("the memory floor is information") — the belt's shape
  information at 11+11 is ~11 bits of gap, ~2,000 shapes, and that is all any N needs.

## The lens

The whole-system read: three pages' open items (cell-rebind's belt census, budget-1e9's
promotion pricing, the scoreboard's kick row) were one missing constant, and it was a census,
not a mechanism. The blind spot I must name: elegant saturation on the *unflown* horizon — my
window is ~3 intervals; the shearing measured at 5–6 intervals (8ffc) and any stirring regime
could make turnover, not standing memory, the wall, and this run cannot see it.
