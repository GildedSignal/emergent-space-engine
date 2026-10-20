# Predictions — 20261020-1503-library-b57f (library lens)

Question: 9ed1 named two exits for the answer channel (one held-scan answer walks
the belt, 4.2–4.4 µs/BODY, TTL-proof) — incremental answering vs the unwired
encounter tier — and left the choice open. This run composes which exit the
measured laws leave standing, held by five verbatim library lessons.

Written BEFORE verify_quotes.py and compose.py run (calibration greps only, no
byte-checks, no arithmetic yet). Kill bars per prediction.

- **P1 (quotes, the held-out property).** All five lesson quotes — Holmes'
  brain-attic (A Study in Scarlet/"Sherlock Holmes", Conan Doyle), the frogs
  ("The Third Door", Banayan), Waitzkin's chunking definition ("The Art of
  Learning"), the Caves-of-Steel efficiency-at-eight-billion passage (Asimov),
  Benoit's "unrecognized simplicities" (via "The Great Mental Models",
  Parrish/Beaubien) — exist in the export byte-identically (exact
  case-sensitive substring, book title matching). Kill bar: any quote that
  fails byte-identity is dropped or marked UNVERIFIED in lessons.md, never
  silently paraphrased.

- **P2 (the walk at 1e9).** 1e9 × (4.2–4.4 µs)/BODY = 4.2–4.4 ks per answer
  against the 69.75 s era budget (a31c): ratio 60–63×. Kill bar: composed ratio
  outside [50, 75] → re-derive before publishing any number.

- **P3 (discard asymmetry).** Across the pages' flown scenes the walked count
  is population-proportional (72.7 → ~3e5, four decades) while the kept/answered
  content is scene-local (32.5–534 kept candidates; en = 178 at 3e5): the
  discard ratio (walked/kept) spans ≥ 10³ across the flown scenes and passes
  10⁶ at 1e9 with kept O(10²). Kill bar: if the kept count tracks the walked
  count across scenes (same exponent), the asymmetry dies and L2/L3 with it.

- **P4 (code anchors, verbatim in-tree today).** (a) encounter.rs's fallback
  iterator `0..ctx.bodies.len()`; (b) universe.rs "Replace the encounter finder
  (the seam): the Binet cone later."; (c) tier.rs "Two orbits meet only if
  their Binet separation"; (d) radial.rs "the caller reads every body as
  before: the filter costs nothing it does not save"; (e) encounter.rs
  `same_inputs` taking the full `candidates: &[(usize, Binding, Scalar)]` (the
  memo is exactly as coarse as the candidate set). Kill bar: any anchor missing
  → the lesson anchored on it is rewritten against what is there.

- **P5 (no cheaper maintenance signal).** No memo or change-signal exists in
  encounter.rs/radial.rs coarser than the candidate list: incremental
  answering has NO shipped maintenance signal below the candidate set (f102's
  measured emptiness holds in-tree). Kill bar: finding one (a version counter,
  an epoch, a doll-level dirty bit that gates answers) inverts L5's exit (a)
  and the dossier says so.

- **P6 (the chunk gate is genuinely absent).** radial.rs registers per-body
  bins; its hull is a BODY's bindings, not a DOLL's bodies. No per-doll
  interval/aggregate fronts the scan, so the O(1) opening test ("can anything
  in this doll be near") is unwired — a real addition, not an existing check
  misread. Kill bar: a per-doll aggregate gate found in-tree → L3 becomes a
  citation of it, not a change.
