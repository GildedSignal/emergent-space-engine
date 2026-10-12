# Predictions (written before the decisive compile, 2026-10-12 ~16:4x)

The decisive step is the compile itself: classifying the 68 clustered runs and writing
`wiki/frame-cost.md`. Predictions on cases I have not yet checked in the dossiers:

1. **Classification counts.** Of the 68, I predict ~28–31 belong to `frame-cost`
   (engine-side frame loop + kick resolver), ~33–36 to `view` (gather/readout/JSON/wire),
   ~3 to `memory-h-live`, ~1–2 to `kick-cadence`/other, and 1 missing (no check.md).
2. **Gold density.** At most 9 golds in the cluster; I predict ≥ 6 of them touch
   frame-cost mechanics (2517, d540, 2439, b063, 115e, b29b, 762d-119f) or the frame
   loop's contract (40c0).
3. **The zero-event tax will not have one number.** I predict the per-body per-frame
   fixed cost spans ~40–90 ns (rekey only, hot cache) to ~0.4–0.8 µs (rekey + drain +
   defer/requeue, whole `advance`), and that no run reconciled these into one law; the
   page must state the range and its scopes, not one number.
4. **Digest-safety of the fix is unresolved.** I predict at least two runs (6766, 1537)
   show a naive peek/tick-calendar fix breaks cross-schedule digest identity, so the
   open direction stays open.
5. **The kick floor claim will be from exactly one gold** (b063: 75.6 µs vs 42–56 ns,
   ~1,400–1,800×, refit ~84%), corroborated in shares (not absolutes) by 2300 and 115e.
6. **No run in this cluster closes the topic**: three golds agreeing on one adoptable
   representation change do not exist here; the page stays `status: open`.
7. **At least one abstract number will be refuted by a later run in the same cluster**
   (my candidates: the 428-body "saturation" — an xtask clamp; the "4.6× frame p50 cut"
   in 7a39; the 0.95 s fleet slice in ba35; the paced-vs-unpaused gather inflation).
8. **The missing run** (`20261008-0743-second-...-a342`) will have a branch with at
   most a dossier and no `check.md`; it cannot be graded, so it is recorded as missing,
   not as a grade.

## Addendum — the contradiction probe (registered before its last runs)

After the compile, one contradiction qualified for the lens's cheap probe: the fleet exodus
(3cfc: one indivisible 0.6–1.5 s item at ≥~1,600 members vs ba35: hand-out events already
split by the budget). Registered 12 October, after the 1,600/3,200/4,000 results (39/100/98 ms
worst hitch) and **before** running 6,400 and 12,800:

9. **The worst hitch grows roughly linearly in members with no cliff**: I expect ~120–180 ms
   at 6,400 and no ≥600 ms stall anywhere below ~12,800 — i.e. ba35's "already split" holds
   through 6,400 and 3cfc's ≥0.6 s form, if real, binds only at ≳12,800 members.
   Outcome: **held at 6,400 (146 ms)**; 12,800 exceeded the probe's 110 s window on this box —
   unmeasured, disclosed in the dossier.
