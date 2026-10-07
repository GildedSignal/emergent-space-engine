Working...
Check complete. `check.md` written; tree restored to clean at 70f27a9.

**Grade: gold.**

What I did and found:

**Reproduction** — Clean tree, `git apply work/patch.diff`, release build. All three stored JSONs (plane, formation 2000, belt 2000) reproduced **byte-identically** after dropping machine/wall fields — a cross-container determinism check stronger than the author's same-box md5. Clean-tree tests: 7 passed / 3 failed (step.rs overflows), matching the claimed pre-existing failures.

**Mechanism verified in source** — `Catalogue::insert` (bind.rs:44–52) only recycles freed slots, never compares content: 2,000 ships on one identical orbit really do hold 2,000 entries. `prune`'s `h.len() > 1` makes the mandatory 192 B segment structural. `bytes_of` is the engine's own accounting, as disclosed.

**Adversarial** — Seed 7 formation: 1,233 B/body, catalogue_live = n_bodies. Belt 10,000 (5× N): 1,261 B/body, catalogue_live = 10,076 — width flat in N, so the 1.28 TB / 160×-over-8 GB extrapolation rests on measured scaling. Arithmetic re-checked (159×, 685 GB shared, player 0.097 events/s / 16 segments).

**Predictions** — File times put predictions.md before all JSONs; failures reported honestly and all one-directional (engine fatter than guessed; no sharing where sharing was predicted).

**Novelty/goal** — HANDOFF said H_live "not measured yet"; this is the first measurement, and it kills two premises: the memo is designed-not-built, and a billion individual records miss 8 GB even at law-floor widths (14–18 GB) — population programs mandatory.

**Missed by the author** (recorded in check.md): the "9–15 GB at 10 AU" scar figure doesn't follow from the run's own numbers (my arithmetic gives 0.8–1.3 GB; the 10 AU kick rate was never measured); `run.log` is empty, so run-order evidence is mtimes only; the RSS-vs-`bytes_of` trace remains undone. None load-bearing for the claim.
