Working...
Check complete — `check2.md` written at `lab/results/20261009-1858-inversion-9d6d/check2.md`.

**Grade: gold.**

What I did as the blind second checker:

1. **Reproduced exactly.** Applied `work/patch.diff` (adds only `rank.rs` + bin entry), rebuilt, ran the dossier's commands: anchor (p99=3, miss(4)=0.05%), m1200 (p99=28, miss(4)=50.8%), bunched 600-ship fleet (p99=98, miss(4)=80.4%) — every number bit-identical to `evidence.jsonl`, each run ≤ 25 s.
2. **Verified the method against the crate.** The fleet generator matches `make_belt` draw-for-draw with the same `Rng`, so the anchor is the gold's `coorbital` scene bit-for-bit; truth is the pre-existing rigorous conservative-advancement solver, independent of any tier; the E|Δn| = 0.5·band derivation checks out.
3. **Held-out discipline held.** predictions.md (19:11:34) predates evidence.jsonl (19:13:25); P1–P8 held, P9's partial miss honestly disclosed.
4. **Five adversarial cases, all confirming:** e-spread 7.5× band (the lens's named blind spot) leaves the κ law unchanged; m1200 at the gold's own band 1e-4 gives κ-collapse (p99 9, miss 14.4%); H=100 collapses onto m1200/H50 almost exactly (5/28/51.4% vs 5/28/50.8%); H=1 confirms the disclosed cadence escape hatch (miss(4)=0, but the pairwise tier then costs 1242 pairs/encounter); seed 31337 robust.
5. **Novel:** nothing in HISTORY.md or the docs sizes the certificate's k; the gold's record sizes the trigger only.

The finding shows a premise of an adopted gold (rank-4 as scale-free) is wrong — a certificate that silently drops 14–80% of encounters at 10³–10⁶ ships is exactly the wrong error type — and supplies the one-step fix (κ sets k and the re-derivation cadence). Flagged gaps: the re-sort cadence cost at 10⁶ ships is unmeasured, and correlated (string-of-pearls) formations untested.
