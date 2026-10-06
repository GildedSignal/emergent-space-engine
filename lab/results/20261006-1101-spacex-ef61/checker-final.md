Working...
Check complete. **Grade: gold**, written to `lab/results/20261006-1101-spacex-ef61/check.md`; tree restored clean (only untracked `lab/results/`).

What I did, and found:

**Reproduction** — clean tree at `f639094`, applied `work/patch.diff`, rebuilt, ran. Baseline and instrumented runs both give bit-identical digests (`2fd6e1ce…` state, `c5d2cd0c…` replay) to the author's; every stage within ~0.5 µs (made: compile 6.4 of 44.0 µs = 15%, forces 9.9, readout 3.9, bind_whole 28.8; leavers: compile 242.9 of 277.9 bind; tail panels 2.2/kick; memo 0/0).

**Predictions** — mtime order verified (baseline 11:05 → predictions 11:06:53 → staged 11:12). The two central predictions *failed* and the failures are the finding; the author reported them as failed.

**Adversarial** — seeds 3, 42 (no leavers), 11, 99, and the promised-but-unreported 55 s: structure identical everywhere. I also added my own timer slots around the two `orbit_state` calls in `rebind`: **3.40 + 3.46 = 6.9 µs of the ~11.3 µs overhead**, turning the dossier's subtraction split into a direct measurement. Code-verified the rest: `step.rs:304` re-reads the unchanged old tube twice per kick; the forces stage is `state_of` gather reads.

**Novelty/goal fit** — first stage-level decomposition of the kick path; it falsifies HANDOFF #3's "15 of 29 µs in fit and compile" (made-body kicks: readout family ~50%, fit+compile ~24%), which is a gold criterion (premise shown wrong, adoptable in one step — it redirects Sol's blocked kick-cost job from compile-side to readout-side).

Caveats noted in the check: Linux x86 only (M1 rebalance is the integrator's re-measure by lab rule), the passage "band/knot build" attribution stays inference, and `instrumentation.diff` omits the new `stages.rs` (doc nit; `patch.diff` is the operative patch).
