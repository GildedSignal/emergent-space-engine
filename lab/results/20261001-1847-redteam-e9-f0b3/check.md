Grade: silver

**Abstract.** Pre-freeze red-team of E9's Schwarzschild oracle. Reproduced cleanly: the truth dump rebuilds **bit-for-bit** from a harness whose physics functions are byte-identical to the judge's `schwarzschild.rs`; the Newtonian-tide miss at r/M=1e6 is 7.02e-6/5.03e-6, below the 1e-5 oracle tolerance, and my extension measures 7.03e-4 at r/M=1e4 — still inside the 1e-2 band, so the weak control certifies wiring, not GR (mutants code-verified to run only at 1e6). Strong-end margin 1.614e-6 (6.2×) and extent gap 4.88e-7 reproduced from the dump alone. But the headline "confirmed … to ~1e-9" is contradicted by the author's own final log: 1.02e-5 at r/M=10 e=0.6, 5.5e-7 at e=0. I ran their missing mirror-vs-dump check at e=0.6: **6.3e-12** — the oracle stands; the residual was their construction's. Premise notes stand; the confirmation claim does not.

**Reproduction (clean tree, no author code where it matters).**
- `rustc -O` of the folder's `rust-truth-harness.rs` regenerates `truth.jsonl.gz` **md5-identical** (`0d4f4360a5ae1701f67fcebd7291d020`), also confirming determinism of the release path. Normalized-text diff of the harness against wt/judge2 `xtask/src/engine_judge/schwarzschild.rs`: `metric`, `connection`, `rk4`, `inv_diff`, `displaced`, `initial`, `period`, `oracle`, `errors` all **identical** — the dump is the judge's oracle, unmodified.
- Weak-control premise (dossier §5): my own Newtonian trace vs the dump at r/M=1e6 gives position 7.024e-6 / shape 5.030e-6 — reproduces 7.0e-6/5.0e-6, below ORACLE_TOL=1e-5. `run()` sends both planted mutants through `--e9-weak-control` → `RADII[..1]`=[1e6] only (code, lines 385–435). Fail-closed confirmed: `E9_FROZEN=false` returns UNSUPPORTED before any engine call (371–377).
- Margin fragility (§6): dump-internal s32-vs-s16 at r=10 e=0.6 = 1.614e-6 vs 1e-5 (6.2×). The 1.61e-9-vs-1.61e-6 transcription story is confirmed by the author's own stderr (`/tmp/e9harness/errs.log`: `rust-errors ratio=10 e=0.6: position=0.000001614…`).
- Extent gap (§4): dump-internal s1-vs-s16 = 4.879e-7 / 6.54e-8 / 1.85e-8 — reproduced.
- Killing constants: my own turning-point derivation matches Darwin to dE/E ≤ 1.15e-16, dL/L ≤ 4.7e-16 at α=0.1 (their numbers exactly); the α=1e-6 3.7e-11 is cancellation in their closed form, as disclosed.
- dt: the harness's e=0.6 dt (0.6752134258890299, stderr) equals the author's Python quadrature to all digits, and the Rust `period()` is the same Simpson-4096 integrand — the dt-mismatch excuse for e=0.6 discrepancies is dead.
- `cargo test -p xtask schwarzschild` was **interrupted twice by my 300 s window** on this shared 2-vCPU box (build, not test failure); superseded by the byte-identical harness plus my recomputation of the quantities the tests assert. The "5/5" claim is unverified as stated.

**Held-out predictions: written before the runs (file order: predictions 48 m < dump 30 m < compare-run2 8 m), and the decisive ones did not hold.**
- Prediction 3 (core premise, <1e-9): measured 1.023e-5 (r=10, e=0.6 — **above their own pre-registered "a value >1e-5 would break the oracle"**), 5.50e-7 (r=10, e=0), 7.75e-7 (r=1e6, e=0). The dossier's Evidence §2 asserts "Held prediction: <1e-9" citing the very log that shows 1.02e-5; the claim "confirmed … to ~1e-9" cherry-picks the P2 simultaneity residual (3.3e-9), not the end-to-end P1.
- Prediction 2 (mirror fidelity ~30%): 15×–450× off — owned in the dossier.
- Prediction 6: the script crashed (TypeError); epicycle 2.59e-6 vs <1e-6; geodetic rate never printed. The dossier says only "pending".
- Mitigation, and why silver not lead: the P1 misses indict the *author's construction*, not the oracle — their axis transport was never validated (the validating section crashed) and their mirror disagrees 450× on second-order controls at e=0.6 while matching Rust to 8.5e-16 at e=0. The oracle's internal controls (refinement, separation, invariants) hold at every radius I tested. The dossier was written at 21 m, before compare-run2 landed at 8 m, and was never updated — explanation, not excuse.

**Adversarial cases of my own.**
1. r=30, e=0.6 (author-untested): separation 2.90e-8, extent 6.22e-6 — no new oracle-invalid case; the 6× margin is specific to r=10 e=0.6, not a cliff.
2. Newtonian discrimination radius: at r/M=1e4 the miss is 7.03e-4, **still inside BAND=1e-2** — discrimination against a Newtonian tide needs r/M ≲ 3×10³, so predictions.md's "≤1e4" is optimistic; this *strengthens* the wiring-only premise note.
3. Dump purity: bit-level rebuild above; plus r=1e4 e=0 controls (5.33e-9/1.79e-8) under tolerance.
4. The missing mirror-vs-dump check at e=0.6 (their folder's last value: order-unity): run at the exact harness dt it gives **6.3e-12/4.0e-12** — the mirror is faithful at e=0.6 too; the O(1) line was a bug artifact, and P1's 1.02e-5 is attributable to their absolute construction's axis transport, not the oracle.

**Novelty.** `docs/engine-judge.md` (wt/judge2) stages the E9 candidate "not yet frozen", admission blocked pending exactly this GLM red-team; no prior E9 red-team in HISTORY (the 1 Oct red-team was the law's). This is the required check, not a redo.

**Goal fit.** "Certificates need independent, adversarial checks" — this is that check, and its premise notes are real. Not gold: no 10× or deletion; the physics-confirmation claim did not survive its own held-out cases.

## The one experiment to gold

Close the independent confirmation at the claimed level, in one window: (a) fix section 6's crash and validate the geodetic rate to <1e-6 (the axis transport is the unattributed 5e-7 floor at e=0 and the likely source of the 1.02e-5 at e=0.6 — my mirror run at 6.3e-12 already clears the oracle itself); (b) measure the absolute construction's own error budget at e=0.6 (member + transport convergence) so the 1.02e-5 is attributed or the "~1e-9" claim is withdrawn to the measured level; (c) record the two premise notes (wiring-only weak control with the measured r/M ≲ 3×10³ Newtonian threshold; the 6× strong-end margin) in `docs/engine-judge.md` and freeze on measured ground.

## What the author missed

- The Newtonian-degeneracy is by design in the judge's own suite: the weak-field test's *positive* control is the Newtonian trace (asserted ≤ BAND at 1e6). The hole is real but should be named as "no near-field Newtonian mutant exists", with the r/M ≲ 3×10³ threshold measured, not "≤1e4" estimated.
- The margin map has two points (r=10, r=100); r=30 was one cheap run away.
- The dossier's Evidence §2 and the abstract-grade claim were left contradicting the folder's own final logs; a freeze decision reading only the dossier would over-trust the oracle's independent confirmation by 2–4 orders of magnitude.
- `cargo test`'s "5/5 on this box" is asserted but no captured output is in the folder (only the harness stderr survives); on a loaded 2-vCPU box the assertion is not reproducible within a checker's window without the build cache.
