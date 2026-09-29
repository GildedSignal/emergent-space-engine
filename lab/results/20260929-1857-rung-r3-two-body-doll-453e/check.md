Verdict: KILL (verdict.py on metrics-check.json + metrics.json: no dispute) — the `eob-doll` configuration is killed by `prec` (0.0625 < 0.99) and `nu` (0.981 < 0.99); both negatives fail exactly the gates they were built to fail.

## Abstract

The exact-Schwarzschild EOB doll is only 1PN-faithful above p ≈ 800 M: its periastron advance exceeds the 1PN Damour–Deruelle oracle by ≈ 8/p (e-enhanced), which kills the 1% precession gate at 6.25% pass (min passing p = 800.3). Every number reproduced exactly in a clean tree (binaries, 100-handoff chain, 64 flybys, picture byte-identical): period 1.0 (93/256 oracle-truncation exclusions), ν-effect 0.981, handoff exponent 0.036, assist 1.0 (worst 0.57% at b = 49 R_p), events 0. Independent checks: my own 1PN-EOM integration and invariant mapping confirm the +8/p excess is genuine 2PN content, not a bug. Finding for the board (docs/representation.md §"Two bodies are one doll"): the 1PN EOB map needs a 2PN map or p ≳ 800 M before it can be the engine's two-body parent. Cost of adoption of the finding: none (a kill, not a component).

## Reproduction

- Clean copy of the run folder, fresh `gcc -O2` build (patch.diff is empty — no tree edits). `binaries.py`, `ships.py`, `picture.py` reproduce every published number **bit-for-bit**, including the reference (103 crossings, t=26.001126663496), the tol 1e-9 vs 1e-11 convergence (1.39e-7 yr / 1.85e-7 AU/yr), both handoff exponents, both flyby pass fractions and worst errors.
- `metrics-check.json` = my reproduced values; verdict.py: KILL, author/checker agree on all 18 outcomes.
- predictions.md predates the outputs (mtimes: predictions 35 m, binaries_out 34 m, ships_out 2 m) and held: prec "~0.05" → 0.0625; period "~1.00" → 1.0; ν "[0.85,1.00]" → 0.981; assist "0.8–1.0, hardest at large b" → 1.0, worst at b=49.3 R_p; per-exit |dE/E| 1e-6..1e-4 confirmed.

## Oracle verification

- oracle.py is a verbatim port of xtask/src/gr_oracle_extended.rs (`eih_invariants`, `damour_deruelle`, `schwarzschild_from_invariants`, `bound_constants`, `bound_period_quad` integrands); the author's standalone Rust re-run (rscheck) matches out.txt.
- I ran `cargo xtask gr-oracle`: it prints "ORACLE DISAGREES" in main — a **pre-existing** condition (author touched nothing): 12 rows at e=0.5 fail their 2PN-residual bands (DD vs eih_ode period diff 1.7e-2 at p=100, 1.8e-4 at p=1000). My independent adaptive RK4 (tol 1e-13) of the same harmonic 1PN EOM reproduces eih_ode's values exactly, and an energy/angular-momentum probe shows eih_invariants' turning radii are only 1PN-consistent at high e (J_peri vs J_apo mismatch 2.6e-2 at p=100 e=0.5; orbit apoapsis falls 1.2% short of p/(1−e)). This oracle ambiguity is largest exactly where the doll fails by 8–69% and is ≤1e-3 in the passing region (p > 800) — it cannot flip `prec`. The ν=0 spot values also check against exact Schwarzschild (test_mass rows pass in xtask).
- DD values re-derived: advance 6π/J² and n=(−2E)^{3/2}[1+(−2E)(−15+ν)/8] match the cited DD/Iyer formulas; my ODE integration agrees with DD to 1.1e-2 at p=450 e=0.2 and 4.5e-3 at p=1000 (2PN-consistent scaling).

## Independent confirmation of the kill reason

My own invariant mapping + GL-800 quadrature (no author code): doll−DD advance = +0.79% at p=1000, +8.4% at p=100 (e=0.6), +68.7% at p=20; period +0.031% at p=100. The exact metric bakes in 2PN+ content; the rung's gate legitimately kills it. The 4 ν-failures are all p<170 with 14–16% deviations from the oracle's ν-term — 2PN contamination, not bugs.

## Spec deviations (all reproducible from the folder)

1. **No dossier.md** (the brief lists it; predictions.md's "see dossier" dangles). The deviations below are documented only in code docstrings.
2. **Transfer is not a figure-eight.** design.py's resonant figure-eight shooting failed to converge (residuals −3.7e-3 / +5.4e-2 after 59 iterations, kept in design.json) and was silently replaced by a retrograde co-orbital circular orbit (r=1.003 AU, ~4 crossings/yr, 100 kept). It still delivers 100 SOI handoffs with entry/exit alternation, but the inside/outside leg alternation of the frozen case is absent.
3. **Handoff metric re-initialises the doll from the reference state at every crossing**, so per-segment errors cannot compound by construction. Adversarial rerun (mine, autonomous chain, doll state fed forward): exponent 0.0246 (schw) / 0.0257 (kepler) — still ≤ 0.2, so the shortcut hid no failure; the metric would pass honestly. Errors grow ×36 across the chain from encounter-geometry drift, not compounding.
4. Flyby sampler interpretation: b drawn log-uniform after advancing Random(20261002) through the 256 binary triples; "impact parameter" read as pericentre (converted to true impact parameter). Defensible readings of an underspecified frozen text.

## What the author missed

- The ship cases carry **no GR signal**: schw and kepler agree to ~1e-6 in every ship metric (2GM/rc² ~ 1e-8 at 1 AU). Handoff/assist exercise the patched-conic handoff machinery only; they cannot discriminate the GR doll at solar-system scale — worth stating, since the rung's title pairs the EOB doll with handoffs.
- The repo oracle's own e≥0.5 tension (above) is unmentioned though it touches the same gate family.
- `events_per_orbit = 0` passes vacuously: the binary doll is a closed-form generator with no handoffs/crossings/kicks — honest, but the criterion tests nothing here.
- The assist gate's real margin is thin: worst 0.57% vs 1% gate at b=49.3 R_p, growing ∝ b (neglected planet pull outside SOI), as the author's own prediction anticipated.
