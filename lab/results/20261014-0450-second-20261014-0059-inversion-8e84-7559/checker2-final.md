Working...
**Grade: gold** — written to `check2.md`, with one correction to the author's wiki page.

**What I verified independently:**

- **Arm 1 (regen, runner):** suite-M-kick and suite-M-prune 91/0/3, M-wrap control dies in `hit_is_exact_past_the_i128_products`, restore = baseline, three distinct rlib fingerprints. Mutant sites (step.rs:440, universe.rs:1105, law.rs:337) match the tree; crates are byte-identical to the parent's 33c83f1a.
- **Arm 2 (my own run):** applied M-kick myself, ran `cargo test -p xtask` → 206/7/14, failure set identical to baseline. Reverse-dep check confirms only xtask and lattice link the universe crate — the two arms exhaust `cargo test`'s reach.
- **Arm 3 (my own run):** clean-tree `behave --law plane` exits 1 (96 s, B14 60 s over) — cannot adjudicate here, as claimed.
- **Adversarial beyond the author:** the dossier's liveness evidence was only an rlib fingerprint (compile-in, not behaviour). I ran the `flyby` example clean vs M-kick: dL/L +1.70e-3 → +1.27e-3 (r_p 1.3), dE/E −3.69e-4 → −3.90e-4 — and since line-440 kicks carry `clock: false`, that difference flows through the `credit` ramp itself. The mutant is behaviour-live and guarded nowhere; the passes are meaningful.
- **Predictions:** file times put predictions.md (04:54) before the first decisive run (05:08); P1–P3 held, P4 vacuous but substantiated.
- **Page:** faithful fold-in; I corrected the Refuted line's "identically to baseline" (not bit-true for M-prune's parallel xtask arm — B10 load flakes, serial 7/7).

**Missed by the author:** no behaviour-level liveness proof (I supplied it); panel.sh's ignored-count parse bug (`$10` vs `$8`); the behave summary's dead `PASS|FAIL$` regex.

Tree restored clean; nothing outside the run folder touched.
