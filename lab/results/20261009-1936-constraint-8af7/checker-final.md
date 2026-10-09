Working...
Check written to `lab/results/20261009-1936-constraint-8af7/check.md`. Tree restored to clean main (no tracked modifications; run folder untouched except `check.md`).

**Grade: silver.**

What I did:
- **Reproduced bit-exact.** Clean-main bench (`--members 480 --rtf 100 --unpaced --seconds 10`): digest `aadaa1c8…` identical to the author's; gather 54.3%/3.08 ms p50, engine 32%. Applied `work/patch.diff`, rebuilt: same digest, counters match <2% off (435,865 cartesian calls at 4.54 µs; 2.47 calls/eval; 0.718 Newton evals per body per frame; state_rate 97% of the bodies loop; secondaries 5.6%). Purity control verified in both directions myself.
- **Claim 1 reproduced** (paced 30 s default: gather 73.6%, engine 4.4%, zero hitches, p50 3.33 ms). Kick-bench reproduces the 5 Oct anchor (exact 0%, quantized 95.5%). `behave` log confirms B14 consumes 60 s and B17 never runs.
- **Adversarial:** seed 7 and rtf 1000 — gather leads everywhere (52.4%/52.6% vs engine 34.1%/39.9%), but the dossier's "64–75% at every rtf" band fails at rtf 1000 on my rerun, and engine passes its stated 29% ceiling. Shared-machine noise can't be excluded; only one bench JSON was retained.
- **perf is blocked** on this host (`perf_event_paranoid=4`), so no independent profiler exists — all attribution shares one harness (the digest control and kick-bench anchor are the cross-checks).

Why silver, not gold: physics and reproduction are solid and the re-ranking (readout, not kicks, owns the frame) is real, but the record overstates in two places — P2's eval-count range (1.2–2.5 predicted, 0.72–1.0 measured) is reported "held" via a post-hoc one-sided reading, and "loadavg 0.3–1.4 recorded in every run's JSON" is unsupported (all machine fields read "unavailable" on Linux). The 10× gain is projected, not delivered. The named gold experiment: warm-start the decode from the previous frame's converged `psi` in the same knot bracket, show ≥5× cheaper gather at an unchanged digest. Bonus finding the author missed: at rtf 1 the per-body cost is ~6× higher (~46 µs), so the player's-regime cap is nearer 360 visible bodies per frame.
