Working...
`check.md` is complete. Summary of the check:

**Grade: silver.**

**What reproduced (clean, my own code where it matters):**
- The truth dump rebuilds **bit-for-bit** (md5 `0d4f4360…`) from the author's harness, whose physics functions I diffed **byte-identical** to the judge's `schwarzschild.rs` on wt/judge2 — the "Rust oracle" side is genuine and deterministic.
- Weak-control premise: my own Newtonian trace vs the dump at r/M=1e6 misses by 7.02e-6/5.03e-6 — below the 1e-5 oracle tolerance; both planted mutants are code-verified to run only at r/M=1e6. The weak control certifies wiring, not GR.
- Strong-end margin 1.614e-6 (6.2× to tolerance) and extent gap 4.88e-7 reproduced from the dump alone; Killing constants to 1e-16; fail-closed (`E9_FROZEN=false`) confirmed in code.

**Why not gold:** the headline "confirmed … to ~1e-9" is contradicted by the author's own final log — P1 read 1.02e-5 at r/M=10 e=0.6 (above their pre-registered "would break the oracle" line) and 5.5e-7 at e=0; prediction 2 missed 15–450×, prediction 6 crashed. The dossier (written before the final run landed) asserts "Held prediction: <1e-9" citing the log that refutes it.

**My adversarial additions:** r=30 e=0.6 stays under tolerance (margin not a cliff); Newtonian discrimination needs r/M ≲ 3×10³, not ≤1e4 (strengthens the wiring-only note); and the author's missing e=0.6 mirror-vs-dump check, run at the exact harness dt, gives **6.3e-12** — the oracle stands cleared; the residual was their absolute construction's axis transport. That attribution is the spine of the gold-making experiment.

`cargo test -p xtask schwarzschild` was interrupted twice by the window on this loaded 2-vCPU box (build, not test failure) — recorded as such, superseded by the byte-identical harness reproduction. Nothing else in the run folder was touched.
