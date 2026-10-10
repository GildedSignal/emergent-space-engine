# Predictions — written before the decisive runs

Run 20261010-0656-quant-d540 (Quant lens). Question: **what does one presented frame of the
shipped plane cost as the universe's body count N grows, when the events themselves are held at
belt-like cadence (≈0 per frame)?** This is the bet the queued belt build (`b-belt-wire`, B18b)
is about to make, measured before it is placed.

Code reading that motivates each prediction (all in `crates/universe/src/universe.rs` unless
said): `advance` calls `rekey` first, which calls `requeue` for every body — one Calendar set
per body per advance; the advance loop defers every entity whose next item is beyond the frame
target (remove + requeue = two more Calendar sets per body per frame); and
`encounter.rs`'s `PlayerNeighbourhood::find` does `binding_at` + `cartesian` for every body of
the doll per player item.

- **P1 (the frame is Ω(N) with zero events).** Per-frame p50 at rtf 100 grows at least 50×
  from N = 10³ to N = 10⁵ while the events column stays 0. If it stays flat (less than 3×),
  there is no wall in the frame loop and the run says so.
- **P2 (attribution).** The scheduling-only advance (`Budget::events(0)`) plus `rekey` alone
  account for ≥ 80% of the whole frame at N = 10⁵: the frame's cost is Calendar traffic, not
  resolution.
- **P3 (the break).** p50 frame time crosses the 16.67 ms budget somewhere between
  3×10⁴ and 3×10⁵ bodies on this Linux/x86 box (orders of magnitude only; the integrator
  re-measures on the M1).
- **P4 (the player scan).** `PlayerNeighbourhood::find` is linear in the doll's body count at
  roughly 1–5 µs per body (a binding plus a cartesian per body), crossing 16.67 ms per player
  item at N ≈ 3×10³–2×10⁴.
- **P5 (controls).** The digest control (settle straight to a horizon vs frames at two budgets,
  then settle) gives EQUAL, and the deep settle reports a nonzero event count (else the control
  is vacuous and I say so). A second alpha layout (stride 40503 instead of 2654435761)
  reproduces the frame-cost curve within 2×.

Kill rule, frozen: if P1 fails (frame flat in N), the wall claim is dropped — the dossier then
reports "no frame-loop wall to N" plus whatever P4 alone shows; if P4's find is under 1 ms at
N = 10⁵, the neighbourhood is not a wall either and both are reported as leads. Machine state
(load) is printed by the bench before and after each run.
