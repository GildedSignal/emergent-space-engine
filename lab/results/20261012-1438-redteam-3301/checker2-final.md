Working...
Check complete. `check2.md` written to the run folder; nothing else touched; all scratch work in `/tmp/check2-repro`.

**Grade: silver.**

Summary of what the check established:

- **Reproduction: exact.** `python3 falsifier.py` regenerated every row of `metrics.json` bit-for-bit (14.4 s, empty patch); `predictions.md` predates the run; misses (P4, P6) honestly reported.
- **Headline claim false about the engine.** The dossier asserts the plane's gather has "no documented fallback" — but `crates/universe/src/view.rs::crossing` has maintained an integer bracket with step-clamping since H0211 (642e9e8b, 1 Oct) and the relativistic acceptance window since H0213 (b5c817d3) — precisely the fix the dossier proposes. The author's own "what would make it wrong" clause describes this exact counterexample; they never opened the file. My faithful port on the author's exact breaking scenes: **zero wrong sprites** (≤0.48°, pure tick quantization), readouts mean 1.1–2.0 — the 23.3° and p99 2→7 claims apply only to a solver nobody ships.
- **Real defect found — by the check, not the run.** The shipped solver's first-sight acquisition at relativistic lag ping-pongs between bracket edges (`hi` crawls −1 per 2 reads across a ~3,500-tick bracket), exhausts the 64-read cap, and drops the emitter for 9–18 consecutive frames at β ≥ 0.99, D0 = 10. No cascade, no poisoned seed; the dossier's "no self-healing" mechanism does not exist in the shipped code.
- **Novelty partial:** lab run `20261003-2306-redteam-4570` already red-teamed this gather's relativistic window (adopted in b5c817d3); the dossier claims the only prior measurement was H0213's steady 0.9c.
- **Secondary attacks verified:** representation.md:32 still names the killed Minsky/Binet mechanism "the primary in-cell solution" against law.md:20's kill record (the dossier's most useful line); r5/r6 confirmed absent from `lab/rungs/`.

The gold experiment is named in the check: rerun the worst-case ladder against the shipped algorithm with the one-line bracket-interior bisection fix, freeze r6 with a first-sight case, and patch the two doc contradictions.
