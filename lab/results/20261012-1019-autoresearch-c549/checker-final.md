Working...
Check complete. Summary of the verification:

**Grade: silver** (`lab/results/20261012-1019-autoresearch-c549/check.md`)

- **Reproduced from the dossier's commands in a clean tree**: patch applies; pure kick 33.5→26.3 µs (−21.7%, author claimed −18.9%), whole 49.3→43.4 µs/item (−12%, author −13%); all four digests equal the author's recorded values bit for bit; 54/54 tests (count is exact); `cost_split` piece costs reproduce (3.30/3.29/3.29/6.87 µs).
- **Premise verified in source**: baseline `step.rs` really decodes the same binding three times per kick (`readout` l.355 + `orbit_state`×2 in `rebind` l.312).
- **Adversarial cases of my own** (seeds 9/3/12, dense/sparse orders, step_log2 5 — never tuned on): universes bit-identical, and — the lock the author lacked — the scheduler's private `pos` cache bit-identical baseline↔patched, via a temporary accessor. This matters because the universe digest hashes `r.proper` (witnessing H1) but not `pos`, so the dossier's "digest proves it" was structurally insufficient for H2. The claim is true; the recorded evidence wasn't.
- **Predictions**: written before the decisive runs (mtimes and content order consistent, B absent from loop logs); held at the top edge, with the one wrong call (bytes/body +8%) honestly disclosed and priced.
- **Novelty**: H0210 queued "kick cost" as open work; no prior entry does decode-dedup or position hand-forward.
- **Not gold**: 1.2×, no 10×, no component deleted, no premise killed — the author self-grades identically. Gold path: the named law-level lever (skip the tube refit on a sub-quantum kick), which needs a behaviour gate, not a digest.
- One number (`Rebinding::from_state 11.1 µs`) has no regenerable command — flagged as the lab's known record failure mode.

Working tree restored to pristine (only untracked `lab/results/`); nothing else in the run folder touched.
