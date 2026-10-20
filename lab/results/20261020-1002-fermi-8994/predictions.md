# Predictions — 20261020-1002-fermi-8994

Question (budget-1e9 od 6, the checker's named deciding instrument): are the allocation wave's
bytes **marginal** (inside the fired item's own scope) or **base** (the flight's frame-scope
work)? f623's window OLS said 1.4–3.3 KB/kick marginal of 12.3–12.7 KB/kick naive, but its own
checker showed the OLS is budget-coupled (slope sign flips) and asked for attribution *inside the
fired item's own scope* plus a >2 KiB per-call size census. Instrument: `alloc_scope` (env-gated
engine marker around the top-level item of class c, outermost wins; counting `GlobalAlloc` in
`examples/alloc_scope.rs`, shipped flight otherwise), on the shipped `nladder` scene, seed 1,
rtf 2000, 12 ms.

Two calibration runs (5 s and 3 s coast, K = 10⁴, gs ≤ 7.9k, pre-wave) were flown BEFORE this
file was written; the decisive arms below are the first to cross the belt's arrival wave
(gs ~13k). Calibration facts folded into the bands: realloc traffic must be counted (a player
item's Vec growths are ~5/6 of its bytes; without them item-scope reads 2.5 KB/kick and the
naive number is silently under-attributed), and the >2 KiB census must split by scope.

## Arms (decisive)
- D1 coast K=10⁴, 30 s, rtf 2000 (≈48k gs: wave 1 at gs ~13k and wave 2 beyond it; f623's own arm).
- D2 burn K=10⁴, 30 s, rtf 2000 (onset ~gs 13k + wave + tail; the checker's burn doubling).
- D3 coast K=3×10⁴, 30 s (the second f623 arm).

## Predictions (written before D1–D3)
- **P1 (the fork).** Item-scope bytes (alloc + realloc) per fired kick on D1 ∈ [8, 20] KB: the
  naive 12.3–12.7 KB is ≥ 60% marginal. Kill of the OLS reading: item-scope ≥ 8 KB. If instead
  item-scope ≤ 4 KB, f623's "the rest is a flight base" stands and pooling is not mandated.
- **P2 (anatomy).** The player's item scope carries ≥ 50% of item-scope bytes, and ≥ 60% of its
  bytes are realloc (growth chains), with the >2 KiB census mean 4–64 KiB per call; the base's
  >2 KiB tail (single calls up to megabytes) is ≤ 25% of total bytes.
- **P3 (the wave is marginal).** At D1's peak item-bytes frames the item-scope bytes/frame rise
  ≥ 3× over the ebb median while base bytes/frame stay < 2× (the wave rides the items, so
  pooling the item scratch is the smoothness lever; if the wave rode the base, the lever is the
  frame's own scratch instead).
- **P4 (burn).** D2's item-scope KB/kick ∈ [1, 2]× D1's (the naive burn doubling 21.5 vs 12.6 is
  item-carried, not base-carried).
- **P5 (composition).** With P1's marginal, the 10⁹ bandwidth row (rtf 100, λ = 4×10⁻⁵ →
  4×10⁶ events/wall-s) reads 32–80 GB/s = 53–133% of 60 GB/s **without** split8 — the row stops
  closing "3–6% after split8" and the pooling lever becomes machine-mandated at the shipped
  cadence (split8 × survival 4.92 still brings it under budget). If item-scope ≤ 4 KB, the row
  closes at ≤ 16 GB/s and no pooling subsystem is mandated (f623's sentence stands).
- **P6 (held-out rung).** D3's item-scope KB/kick within [0.7, 1.5]× D1's (the attribution is a
  law across rungs, not a K = 10⁴ artifact).

Kill criteria: any arm whose allocation counters move while `ES_ALLOC_SCOPE` is unset (the
instrument must be print-only when off) voids that arm; a base scope that never frees (freed ≪
bytes over 48k gs) means I am counting retained state, not traffic, and the traffic numbers get
re-derived from alloc+realloc only, disclosed.
