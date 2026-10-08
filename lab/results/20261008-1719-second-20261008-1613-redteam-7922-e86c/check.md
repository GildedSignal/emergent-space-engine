# Check — second checker, run 20261008-1719-second-20261008-1613-redteam-7922-e86c

Grade: gold

## Abstract (for the integrator)

The jet re-anchor horizon on the shipped integer law (`space-darwin16-scaled-v5`) follows (1−e²)^(2/3): ratio 0.088 vs 0.089, every grid point within 2% of 543·(1−e²)^(2/3), δ^(−2/3) verified (0.0465/4.69 vs 0.0464/4.64). The tide channel (fixed a, Kepler-blind) is 3–123× safer yet dies at the tail (512 kicks at e = 0.995). A scene-calibrated global-rate trigger fails from e = 0.9 (563× floor at 0.995); the per-cycle curvature trigger holds everywhere (≤ 0.6× floor, 0.050 compiles/kick at e = 0.995 at tide-scale kicks; ~7×10⁻⁶ at the law's quanta). No belt scene in the tree concentrates (B18b σ 0.07 cap 0.6; encounters σ 0.03 cap 0.5: share(e>0.9) = 0, p99 ≤ 2.1×); a σ = 0.3 tail concentrates 37.9% of compile crossings on 1.1% of bodies. All three commands reproduce bit-for-bit (3.1/17.5/3.5 s). Cost to adopt: one law.md sentence, one rung criterion, one scene decision (freeze or refuse hot tails before B18b certifies smoothness).

## Reasons

**Reproduction (clean tree, empty patch.diff).** `python3 falsifier-orig.py`: stdout and metrics.json byte-identical to the stored first-run record (3.1 s). `cargo run --release --bin jetbench` (17.5 s): every number in E1/E1b/E2/E3 identical to `falsifier2-out.txt`; metrics2.json identical except `wall_s`. `--bin cost`: 6.1/29.5/137.3 µs vs 6.3/30.5/138.8 (jitter). Scene constants verified in the tree: B18b `xtask/src/behave/belt.rs` SPEC (sigma_milli 70, e_cap 644245094/2³⁰ = 0.6, p ∈ [2048, 2560)); encounters `crates/encounters/src/belt.rs` cap 0.5, σ_e ≤ 3×10⁻²; LAW_ID, the 10⁻⁶ floor and the 0.05 compiles/kick budget all in `crates/space` / `docs/law.md` (line 35). No crate, gate, doc or `main` edit (`git status` shows only the run folder).

**Predictions.** `predictions.md` (17:26:55) predates `jetbench/` (17:29:46) and the decisive output (17:34:30). P1, P3, P5, P6 held (P5 stronger than predicted: fails from 0.9, not 0.95); P2 half-held outside its band on the safe side and is reported as such; P4's hot-tail p99.9 and share missed upward (148 vs [20, 80]; 37.9% vs [8, 20]%) with the measured cause (the compile builds the outbound half and mirrors — I confirm: knots = 22.91·ln((1+e)/(1−e))+2 within ~1 knot, exactly half of B9's full-cycle count); P7 missed informatively and is reported. Honest adjudication throughout.

**My seven adversarial cases** (independent crate in /tmp, same shipped law):
1. Seed sweep of the random channel: randE horizons spread ~2× (8811–19833 at e = 0.5) but stay ≥ 3.5× corrE everywhere — P3 is not a seed artifact.
2. p-sweep (512, 1024, 2304, 8192): ratio n\*(0.99)/n\*(0.5) = 0.088 at every p; absolute tail horizons p-independent (scale-free, as the Kepler mechanism requires).
3. Beyond the grid: corrE 25→18, corrL 512→266 from e 0.995→0.997; by e ≈ 0.999 fixed-a leaves the bound domain (`NoBoundOrbit`) — the tail meets the plunge, matching the lens note.
4. **The per-cycle trigger under random-sign kicks** (the belt's residual channel; the author tested correlated only): holds at ≤ 0.54× floor at all e, all three seeds, at ~5× lower recompile rates (0.0106/k at e = 0.995). The criterion is stronger than claimed.
5. Knots: half-cycle mirror confirmed against B9's full-cycle formula.
6. corrL walk: the walk moves a body's periapsis < 1% (1152→1144 M at e = 0.5) — see "missed".
7. Kepler-blindness: compiled T at fixed a deviates from Kepler by 1.3×10⁻³ growing to 1.46×10⁻³ at e = 0.995 — that e-variation is the corrL horizon's only driver, as claimed.

**Novelty.** Nothing in docs/HISTORY.md, docs/ or the taste log measures the horizon's e-dependence, the tide channel, or the trigger on the integer law. The nearest record is law.md's adopted drift-threshold re-anchor (from red-team 20261006-0346-redteam-df81: "about 0.05 compiles per kick", scene-independent) — this run shows that constant is (1−e²)^(2/3)-dependent and kick-size-conditional, and kills the cheap global-rate alternative by 563× with a planted negative control. The first run's Kepler-float result is confirmed; its belt arithmetic (σ 0.3 charged as "B18b", full-cycle knots) is corrected.

**Goal fit.** Board focus items 1 and 4 (kicks per orbit; smoothness, the p99) and gate B18b directly. It shows a premise is wrong (a scene-calibrated re-anchor interval is unsafe; no tree scene certifies the tail) and is adoptable in one step. PRINCIPLES 12 ("i care about the p95/99 results i want the game to be smooth"), 3 ("Compute only surprises" — the surprise rate is δE/|E|, which spikes at the separatrix), 33 ("a body resolves only the influences that are significant at its own scale").

## What the author missed

- **A wording defect in the dossier's mechanism sentence:** "the walk takes the periapsis from 1152 M to 11.5 M" — the measured walk moves periapsis < 1%; 1152 M and 11.5 M are periapses of the e = 0.5 and e = 0.995 grid bodies. The tail steepness is real; this causal sentence as written is wrong.
- The per-cycle trigger was validated only on correlated kicks; the residual channel (the belt's H0190 mode) also needed it — it holds, more cheaply (my case 4).
- The "every grid point within 2% of the Kepler closed form" holds at p = 2304 only; the near-circular ratio n\*(0+)/n\*(0.5) is p-dependent (0.96 at p = 512, 1.78 at p = 1024 vs Kepler 1.21) — the near-circular point is GR-sensitive. The tail ratio is the p-invariant part.
- Single-seed randE ratios quoted without the ~2× seed spread.
- Inside the harness itself, the corrL tail stops compiling before the plunge (FD anchor at e ≈ 0.9985 hits `NoBoundOrbit`): the horizon there is a bound on the jet only up to the domain edge — worth one sentence in the rung criterion.
- The corrL channel is a monotone worst-case pump, not a measured tide law; the "3–123×" is model-dependent (direction conservative). The static-e belt MC is flagged by the author; the time-evolved MC remains the named follow-up, and the rung criterion's frozen hot-tail scene would settle it.
