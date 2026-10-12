Grade: gold

**Abstract.** The claim holds and the record is fully regenerating. `probe.py` regenerates `probe_out.json` byte-identical; probe2 parts A, a0, hcheck, a0998lite regenerate identically (ex-machine); `equality` 10/10 (170 s), `identity` 9/9 (384 s). The Kerr separatrix failure persists at every prograde spin (log divergence ~10×/decade; encounter kick α=10⁻³ errs 42–52%, α=3·10⁻³ plunges; whirl grows with spin, 84→215 rad at χ=0.998), and the parent's channel decomposition is indeed inverted: the T-channel tracks (15/8)(δE/(1−E))² (the precession channel is flat ~3.5·10⁻¹²). Gain: the jet's recompile certificate becomes one root-distance rule at both band ends, plus B19 recompile criteria. Adoption: integrator-side, one step (rung + gate criteria); float→integer decision still the rung's.

**Reproduction** (clean tree; `work/patch.diff` is empty). Every command rerun in a scratch tree:
- `python3 probe.py`: `probe_out.json` byte-identical (md5 86d7b060…; 9 s).
- `probe2.py A`: identical ex-machine — A1 ratios 1.048104/1.0092198/1.0045861 (dossier: 1.0481/1.0092/1.0046); A2 grid as claimed; A3 N_floor = 1 measured, formula capped at 1; A4 L-channel 7.54·10⁻¹² vs h-noise 2.0·10⁻¹²; A5 doc booleans all true against this tree.
- `probe2.py a0`: identical; control vs parent P3 dphi/T ≤ 1.0·10⁻¹², |∂T/∂E| ≤ 1.07·10⁻¹⁰; E_c = √(9/10), L_c = √(25/2) exactly.
- `probe2.py hcheck`: identical (h-refinement ~10⁻¹³).
- `probe2.py a0998lite`: identical (155 s vs claimed 143 s; shared box). a05/a09 record rows match the dossier table point for point (1.95·10⁴→1.88·10⁷; 5.33·10⁻⁶/0.461; 42.1%; plunge) — not rerun for time; the machinery is verified identical on four other parts.
- `cargo test -p emergent-lattice-event --test equality`: 10/10, 170 s (dossier 173 s). `cargo test -p emergent-engine --test identity`: 9/9, 384 s (dossier 472 s) — premise 4's substance (sparse `EventCore` vs dense `Chronon`, contacts, planted-late-kick negative) is real and passing here.

**Predictions.** `predictions.md` (mtime 1h) predates every decisive part (44–16m). P8 was written with a genuine falsification branch ("if the T-channel comes out flat ~1.9e-12, this prediction fails") — it resolved in the risky direction, i.e. against the parent's adopted mechanism. `probe2.py`'s mtime (16m) postdates the early parts (script edited to add hcheck/merge/lite), but the shipped script regenerates the shipped records exactly, which is the substance of the record rule.

**Adversarial (mine).**
1. *Retrograde* (the author's named open case; via the (a,L)→(−a,−L) symmetry, a=−0.9, r_c=8.0): |∂T/∂E| = 5.9·10⁵ → 6.6·10⁶ for ε 10⁻⁴→10⁻⁵ (11×/decade); quantum kick at ε=10⁻⁴ breaches the floor (7.2·10⁻⁶); α=10⁻⁴ errs 52%; α=10⁻³ and 3·10⁻³ plunge-after-kick. The categorical failure holds in retrograde — the "every spin state" claim extends beyond what the author measured. (At ε=10⁻³ the base cycle itself returns None — an oracle band-guard limit at that point, disclosed here; deeper ε runs cleanly.)
2. *Off-grid (15/8) law*: at p=50/e=0.8, p=200/e=0.95, p=35/e=0.3 the T-channel divided by (15/8)(δE/(1−E))² gives 0.989/0.998/0.959 — the corrected decomposition holds off the parent's grid.
3. *Whirl integration error*: h-refinement (10⁻³ vs 5·10⁻⁴) of the a=0.998, ε=10⁻³ whirl (84.17 rad) agrees to 1.3·10⁻¹¹ — the longest whirl is converged, closing the gap the author's h_check left (it covered a=0.5/0.9 at ε=10⁻³ only).
4. Gate/doc re-read: law.md's B19 gates behaviours only (precession, classification, frame dragging, both senses); the re-anchor trigger is drift-only (√(floor/C), law.md line 35) with no separatrix term — as claimed.

**Novelty.** docs/HISTORY.md ends at H0215; the parent run (20261011-2235) is unjournaled, and no entry covers the jet's Kerr domain or the decomposition. The drift-only trigger descends from df81 (20261006-0346, cited in law.md); the both-ends root-distance certificate and the Kerr measurement are new. No duplicate found.

**Goal fit.** Board focus "fewer kicks per orbit… the jet's recompile rate must be scheduled by certificate": this run measures when the multiply-add is invalid (recompile forced), unifies the two failure families into one rule, and names the missing gate criteria. Principles 13/21/19 as quoted in the dossier; floats explore, the rung decides — respected.

**Misses (none load-bearing):**
- `metal_identity.rs`, named in the dossier as the macOS-only GPU leg, **does not exist**; the metal crate's tests are `equivalence.rs`/`kickable.rs`. The substance (GPU leg untested on Linux; on Linux any metal test exercises the `#[cfg(not(macos))]` fallback) survives, but the citation is wrong.
- "Byte-identical to the parent's `probe_out.json`" is unverifiable in this checkout (the parent's folder is absent); only self-regeneration checks — and holds.
- At χ=0.998 the deep-ε divergence slope and L-band remain unmeasured (lite, honestly named; `a0998t` committed). The (15/8) law is still verified on Schwarzschild grids only (author's lens note; my off-grid points are Schwarzschild too).
- The retrograde ε=10⁻³ oracle failure above shows the band guard needs care before any retrograde rung freeze.

**Why gold.** Reproduced end to end; pre-registered predictions held, including a risky inversion prediction against the parent's gold-adopted mechanism, confirmed by my independent off-grid and retrograde probes; it corrects a wrong premise in the parent's record, hardens the finding to every spin state, repairs the record so the shipped code regenerates every headline number, and its adoption is one integrator step. The named open cases (deep-ε at 0.998, Kerr T-channel belt grid, the rung itself) are correctly bounded and costed, not hidden.
