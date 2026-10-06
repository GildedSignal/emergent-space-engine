Working...
Check complete. `lab/results/20261006-0437-constraint-ec9d/check.md` written; tree restored to clean main; nothing committed or pushed.

**Grade: silver.**

What I did:
- **Reproduced** all five evidence items on clean main (8e28af2) and under the author's patch: kick-bench digests identical (`2fd6e1ce…`, seed 7 `1452eba7…`, whole-plane `b411cce8…`); leaver kick median 365–381 µs with compile 318–356 µs (89–97% of the rebind; fit_key flat 4–9 µs); force gathering ≤ 9 µs; exact-memo hit rate 0.
- **Pre-registration verified by file times**: predictions.md (04:43) precedes every decomposition run (04:45–04:49); the author's honest reporting of its wrong sub-mechanism (fit iterations, not compile) checked out.
- **Attacked**: re-derived the phase table the saved patch can't regenerate (it agrees — a reproducibility hole in the dossier); counted trajectory kinds directly across 5 seeds — every passage rebind is a leaver kick (0 among made), stronger than the author's arithmetic; adversarial seeds: seed 3 has no leavers at all (tail intermittent), seed 11 hits 500 µs, seed 5 only 78 µs — cost tracks geometry, exactly the claimed log(edge/periapsis) mechanism, which I verified in `orbit.rs` (panels shrink x by 15/16; `passage_edge` = 2× doll edge).
- **Novelty**: HANDOFF/dbd4add knew leaver medians and "15 µs fit and compile" for made bodies; the decomposition and mechanism are new.

Why not gold: the fix (bounded `Passage::compile_bounded`) was never built — the ~10× p99 gain and the digest-identity of the fix are projected, and the author says so itself. One experiment away: build it, show bit-identical digests plus the p99 drop, and count whether deferred tail panels are ever read.
