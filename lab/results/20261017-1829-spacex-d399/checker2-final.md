Working...
Done. **`Grade: gold`** — written to `lab/results/20261017-1829-spacex-d399/check2.md`, blind to the first check.

**What I verified independently:**

- **Reproduction from a clean tree** (applied `work/patch.diff` myself): the delete arm (`FIT_NODECODED=1`) is bit-identical on **all 13 `ladder_digest` corpus cases** × 4 schedules — the author showed 5; the diff shows only wall-time annotations differ. Stage table matches (compile 12.04 µs = 49%, `at_radius` 1.13 µs = 4.6%, `decoded_event` 3.59 µs = 15%). Fit cost: −14.5% replay mean, −17.1% flight ns/call; two extra interleaved `nladder` passes give −14.0%/−15.7% — the cut equals `decoded_event`+`residual_between` exactly, internally consistent.
- **Structural proof in code, not the author's grep**: `bind_in` (bind.rs:260-288) reads only `trajectory`/`periapsis_angle`/`periapsis_time`/`clockwise` and builds its own residual from its own `decode`; `Rebinding.residual`'s only production consumer is `TubeEvent::bind→reconstruct()` (space crate's handoff path, not imported by universe). The digest hashes the *bound's* residual — identity is exact by construction.
- **Predictions** written before the decisive artifacts; P1/P3/P4 held, P2 held in its own 3–8% band.
- **Adversarial**: the 8 untested N=100/N=1000 cases (identical); the error-corner can't fire in the corpus, is disclosed, and the proposed API split dissolves it; `behave --law plane` is broken identically on both arms here (no signal, noted as such).
- **Novelty**: no HISTORY entry; the run answers the page's open direction 2, refutes the `at_radius` hypothesis, and corrects compile 26%→49%.

**One correction made to the page**: the dossier's headline "engine p50 −18.3%" is single-pass noise (my three A/B passes: −6.8%, 0%, +5.1%); the reproducible engine-level gain is `process(whole)` −3 to −8%. Fixed in the Runs appendix; the gold rests on the fit-stage numbers, which reproduce on every pass.

Tree restored to its pre-check state (patch reverted, only `lab/results/` untracked); no commits or pushes.
