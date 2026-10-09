Grade: gold

**Abstract.** Claim: the plunge-tube claim now holds on the shipped record — the honest bracket + Newton-in-ψ readout sits at the compiled table's own error floor in every case and across the winding sweep, at 25–28 µs pure Python / ~0.53–0.59 µs compiled, winding-flat; the 3 µs headline is retired as a 10⁻⁵-accuracy linear readout. All three commands reproduced: `plunge_record.py` byte-exact (including the θ-form adjudication), readout physics exact (timings 28–31 µs under load), C probes bit-identical at 587/589 ns. My independent mpmath oracle, spike-packed k=7 targets, τ extremes, off-sweep (E,L) and photon near-critical all sit at floor; the restated reference converges (60↔80 dps, θ-form = 23.841746). Adoptable as the `b-plunge-tubes` step; cost: one substitution + anchor in `crates/space`.

## Reproduction

Clean tree (`patch.diff` empty; `plunge_falsifier.py`/`plunge_cost.py`/`run-output.txt` verified byte-identical to the first run's commit ec4313f). All three dossier commands run:

1. `python3 plunge_record.py` — reproduces `record-output.txt` **byte-exact**: P3 pair-b column ≤1% (0.14–0.19% at k=2–3, exact k≥4), restated near-critical errors 5.8e-15…7.449e-3, slope −0.5001, Lcrit deviation 3.947e-8, adjudication table (θ-form = ψ-split = oracle at every k; tube 24.019348 the outlier).
2. `python3 plunge_readout.py` — every physics number identical (floors, linear-readout errors, Newton errors, conv35); timings 27.9–30.9 µs vs the author's 25.3–28.1 (shared-runner load; same verdicts: >20 µs, winding-flat 1.097 vs 1.014).
3. `cc -O2 … && ./plunge_readout_c` — probe abs diffs **0.0** vs Python (C is a faithful translation; real 513-entry tables; `chk` accumulator prevents dead-code elimination), 587.2/589.3 ns vs claimed 529.8/534.4 (same order, ~11% load).

Timeline: `predictions.md` (21:26:41) precedes every script and output of this run (earliest 21:33:52); pre-registered with a verdict rule that anticipated PR3 failing. `readout-output.json` was written 18 s after `dossier.md` — a dump of the same run, physics fields matching the txt exactly.

## Predictions

PR1 (floor) held everywhere; PR3 held (up to 10⁹× above floor, 390× growth); PR4 held on b-column/slope/checker agreement, wrong at k=4 in the interesting direction (shipped 1.665e-8 was reference artifact — true 1.5e-12, root-limited, cross-consistent with pair-b 9.65e-13); PR5 held. PR2's <20 µs missed 1.3× in pure Python and its k=6/7 convergence clause missed — both disclosed, and the compiled form passes by ~34×. This is the prediction system working: numbers falsified and reported, not tuned (H0183: diagnose which expectation broke).

## My attacks (independent of the author's oracle)

1. **Independent mpmath oracle** (cumulative mp.quad inversion in ψ; no DOP853, no GL4, no np.roots): case C readout 1.2e-13 = the table's own GL4-cumulative error (mechanism itself 1.1e-14 at an interior target); k=5 2.89e-7 and k=7 1.76e-3 sit exactly at the table's edge error — the reader adds ~nothing.
2. **Spike-packed targets at k=7** (the lens-admitted miss): 16 targets inside the five panels around ψ_s=π/4 — readout 2.04e-3/5.12e-4 vs nearest-edge floor 2.67e-3/3.99e-4. Within floor; no extra readout error inside spike panels.
3. **Off-sweep adversarial (E,L):** E=1.05, L=0.999L_c: 4.9e-14/9.4e-15. E=1.2, L=L_c(1−10⁻⁶): exactly at floor (1.75e-3/2.58e-4). Photon b=0.9999b_c: r 3.93e-11 vs floor 3.95e-11.
4. **τ extremes (case C):** finite and correct at τ=0, τ=Tau[-1], and beyond range (clamps to horizon values u→0.5, φ→4.152078, v→55.8635).
5. **Reference convergence:** split dφ at 60 vs 80 dps agree to ~1e-60; 512-panel errors vs 80 dps = 1.537e-12/4.159e-7/1.790e-4/7.449e-3 (k=4…7) — the restated column is the truth, and θ-form at 60 dps independently gives 23.841746. The k=7 adjudication is genuine and non-circular.

## Novelty and goal fit

`docs/HISTORY.md` still logs "plunge orbits have no tube"; `b-plunge-tubes` is queued (`lab/queue.txt`) and untouched. This run adds no new mechanism by design — it is the first checker's named gold-gap experiment, fully delivered. New content: the honest readout contract, the θ-form third reference, and finding 6 (per-sample panel sizing ∝ ln(1/δ) requirement). Fit: "Measure before claiming" (the 3 µs headline retired with measured numbers for both mechanisms); "Store the generator, not the generated" (one (E,L) compiles, readouts derived); the lab lesson "agreement is not independence" applied (the two agreeing schemes shared a flaw; the θ-form closed it). The ~10⁻¹⁰ non-critical accuracy and O(1) sub-µs readout delete the `NoBoundOrbit` refusal class in one compiled object — ≥10× on the queued bottleneck.

## What the author missed

- `plunge_readout.py` writes `readout-output.json` into the record dir — the same hygiene the first checker flagged for `plunge_main.json`; my reproduction overwrote it (physics fields deterministic and identical; the timing floats in it are now the checker's run — the authoritative record is `readout-output.txt`, untouched). The next author should write elsewhere.
- The compiled timing covers only case C and k=7; the L=0 and photon special forms are never compiled or timed (they are the cheap branches; minor).
- The "~13,000× under DOP853" compares one readout sample against a whole-plunge integration (7.3 ms, nfev 782) — a framing inherited from run 1; the per-sample oracle cost would be smaller, but the engine-facing conclusion (µs table readout vs ms re-integration) is robust.
- Per-sample panel sizing (finding 6) is measured as a requirement but not measured at the panel counts that would fix k=6/7 (their own lens note; that is the build step's work, alongside the integer B₈ re-derivation, u_stop absorption and mid-plunge kicks, all disclosed as open).
