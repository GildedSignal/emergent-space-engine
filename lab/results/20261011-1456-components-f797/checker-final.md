Working...
Check complete. `check.md` written to the run folder; tree restored (probe and patch removed; only untracked `lab/results/` remains, as before).

**Grade: silver.**

What I did and found, in brief:

**Reproduction** — Applied `work/patch.diff`, built, ran `kickbench` twice. Every cell of `bench.txt` regenerates within ~2% (three runs total: author's saved + two of mine, load 0.74). All key%/shape% columns identical; the exact-circle probe prints `Ok` as claimed. The arithmetic in the dossier (idiot indices, design-inclusive 8.8×, conservative 4.7×, ~5 KB memory via 16-byte `Scalar`) all checks out.

**Predictions** — `predictions.md` (15:05) predates `bench.txt` (15:16). P1 and P4 held; P2 held on the harness and is structurally true regardless (the rebind path has no memo — every fired kick compiles, step.rs:618→`bind`→`from_state`→`Orbit::compile`). P3 strictly failed on the circular belt scene (39% < 50%) yet is reported as "all four held" — disclosed number, overstated verdict.

**Three adversarial cases** —
1. **Headroom scan**: the bench's `bind_hd` goes *finer* (units−2), i.e. anti-headroom — "with or without 4× word headroom" was never tested as stated. My scan (units +0…+6) repairs it: bind drops from 2.0× to **0.99×** `from_state` at 2³ coarser (e 0.6), confirming the word-transition cause the dossier attributes.
2. **Kick streams**: the bench's loop never advances position; at phase 7/32 fixed-position, 1-quantum monotone kicks change the `OrbitKey` only **72%** of the time — "any velocity change moves the periapsis" is false at quantum scale. On plane-realistic advancing streams: 99–100%, so the conclusion survives.
3. **Floor model**: `(5·knots+3)` verified against `Integral([Scalar;5])` + `increments:[Scalar;3]`; `Scalar` is `{i64,i16}`, constant-time — the floor model is fair, ~20% conservative (omits ψ-grid updates).

**Novelty** — the "nobody had the price on the record" line is overstated (H0210: 29 µs/kick; `cost_split.rs`/`cost.rs` exist). New and verified: the jet floor, the design-within-2×-of-floor quantification, the `word_for` double-compile mechanism, and the ShapeKey memo extension.

**Why silver, not gold**: the jet was already the adopted design (law.md:35), nothing was built or deleted here, and the engine-level gain today is the author's own 2–3× bound. One experiment to gold: build the jet's (E, L)-derivative compile at anchor and instrument a real plane run's kick breakdown. Evidence-hygiene flaws noted: `bench.txt` is not the shipped code's output (missing probe and machine-state lines).
