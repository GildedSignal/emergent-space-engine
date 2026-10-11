Grade: silver

**Abstract (for the integrator).** Claim: the re-anchored jet (law.md, unowned) can amortize the per-kick rebind — carrying kicks against a frozen tube holds 10⁻⁶ for a median 30–900 kicks across real plane bodies — cutting the kick ≈1.5–1.9×. Reproduced bit for bit, robust across seeds 1/2/7 and 10000 kicks, both kick paths covered. But all three evidence rows are mislabeled (raw body ids where `ships[]` indices were meant): "Orbiter 3" is Hauler 11, "Hauler 1" is Home the planet, "Hauler 6" is Hauler 3; the reported prediction miss and the "inversion" are artifacts — on the intended bodies (ids 18/5/10: medians 72/314/705) the predictions held. Adopt: implement the jet with a cheap drift trigger, re-face B5/B12/B13/B17.

## Reproduction

Clean tree, `git apply work/patch.diff` (adds only `examples/jet_probe.rs`; `cost`/`cost_split` are shipped). Linux x86, 8 vCPU.

- `jet_probe`: **reproduces bit for bit** — all 27 numbers of `jet-probe-out.txt`, including medians 790/34/134 and the 10⁻⁵/10⁻⁴ rows.
- `cost_split`: kick resolve **34.4 µs** (author 35.6), readout 3.43, secondaries 3.43, tide 3.54, root_state 7.21 — matches.
- `cost`: `from_state` **11.3–13.8 µs** over four runs (author 17.5), compile 3.5 (author 4.8). The rebind is **~35% of a kick here, not 49%**; the speedup is ~1.5× under my load vs the author's 1.9×. Same order, but the dossier's "halves" and "49%" are load-sensitive and did not reproduce.

## The central finding: the bodies are mislabeled

The probe passes raw body ids (14, 1, 6) where the predictions name `ships[14]`, `ships[1]`, `ships[6]`. Bodies 0–3 are Cinder/Home/Giant/Moon; `ships[i]` is id i+4. Verified by listing kinds/dolls/names (`scenario.rs` id order):

| dossier row | actually measured | kick path |
|---|---|---|
| "Orbiter 3" (id 14) | **Hauler 11**, root doll, 2.4 AU | v2 clock (`kick_clock`) |
| "Hauler 1" (id 1) | **Home, a planet**, root doll | WH split (`kick`) |
| "Hauler 6" (id 6) | **Hauler 3**, root doll | v2 clock |

Consequences. (a) The row labels, the "tide+moon" description and "0.5–8 AU" for id 1 are false as written. (b) The prediction audit is wrong: the reported miss ("Hauler 1: 34") is Home the planet, and the celebrated "inversion" is an artifact. On the **intended** bodies (my runs, seed 1): Orbiter 3 (id 18, WH path in Home's doll) median **72**, Hauler 2 (id 5) **314**, Hauler 7 (id 10) **705** — so the original predictions (interval ≥ 50 on quiet bodies; orbiter shorter by 3–30×) **held as written**, and the dossier's "variation not strength" diagnosis, built on the inversion, is unsupported. (c) Both kick paths are covered only by accident (Home, a planet, rides the split path; no ship in a child doll was probed). Ironically the truth is stronger than the reported miss — but a checker cannot grade a table whose rows are not what they claim.

## Attack (my cases)

1. **Intended bodies, seeds 1/2/7**: medians Orbiter 3 = 72/67/68, Hauler 2 = 314/146/377, Hauler 7 = 705/609/903 — stable across seeds (behaviour, not a tuned seed; principle 20). Home = 34/34/34 (planets have fixed specs — seed-invariant by construction, so it is one case, not three).
2. **Stationarity**: 10000 kicks, seed 1: Orbiter 3 median 60 (156 intervals, min 44), Home 34 (299 intervals), Hauler 11 655 (15 intervals). No leak across recompiles, no decay — the recompile rate is stationary.
3. **Interval floor**: minima reach 6 (Orbiter 3, seed 7) and 9–12 (Home): a fixed-cadence trigger at the median would overshoot the bound on the short tail; the real trigger must be state-based (as law.md specifies) — unmeasured here.
4. **Probe validity**: tighter bounds give strictly more intervals (4→3→2 inverted with bound loosening), so the error check genuinely fires; no silent `cartesian` failure inflated intervals (exact-path `.unwrap()`s would have panicked).

## Novelty

The mechanism is prior art by design: law.md "Not adopted: a quantized (E, L) memo…; strong-field reuse is the jet…, **re-anchored**", with the red-team 20261006-0346's ~730 correlated quantum kicks at ~0.05 compiles/kick. What is new: the rebind's measured share of the shipped plane's kick (`cost`/`cost_split`) and the interval on the plane's actual bodies and both real kick paths (my corrected numbers: 34–903 at 10⁻⁶). Queue check holds: none of the directed builds touches the rebind (b-readout-cost is readouts). Not a re-run: the red-team measured quantum-kick drift in its own harness; this measures the plane.

## Goal fit

Board focus #1, the kick's cost — yes, the other lever after six runs killed correctors/deferral. PRINCIPLES 1 ("the cheapest compute is compute not done"), 14 ("we only care about changes"), 13 (bounded error type). The gain is ≈1.5–1.9× per kick, not 10×, and no component is deleted — so not gold by the bar even before the labeling flaw.

## Why silver, not lead

The measurements are real, exactly reproducible, and my independent runs (corrected identities, extra seeds, 10000 kicks) make the underlying claim *stronger* than the dossier reports: intervals 28–903 kicks at 10⁻⁶ on six bodies, both kick paths. This is genuine, adoptable input for the jet builder — it bounds the recompile rate. Not gold: the evidence table as written misstates what was measured (the "headline the log contradicts" failure), the cost split did not reproduce at 49%, the gain is sub-10×, and the mechanism is documented prior art now measured, not new.

**The one experiment for gold:** implement the re-anchored jet in `Work::kick`/`kick_clock` with a **cheap drift-bound trigger** (no access to the exact state — the probe cheats by reading the shipped exact path; a Σ|Δv|·Δt-style bound must be shown to fire at the measured rate 1/30–1/900), then re-face B5/B12/B13/B17 and show the behaviour digests hold.

## What the author missed

- The `ships[]`-vs-raw-id confusion itself; every downstream story (the inversion, the "coherent tide+moon" diagnosis, "Hauler 1 at 0.5–8 AU") is built on it. The intended bodies confirm the original predictions — the honest dossier was better than the one written.
- The rebind fraction is load-sensitive (49% → 35% here); a single-load number should not anchor "1.9×".
- The probe's trigger uses the exact path — the one thing an implementation cannot have. Named by the author as "carry the offset; recompile at the bound" without noting the bound is unmeasurable without the exact state.
- The printed growth exponents (18–760) are meaningless; the sound argument is the bound scaling (×1.6–3.8 per decade), which the dossier does use.
- The flyby and resonant cases were named, not run (the flyby example exists in the tree).
- 3000 kicks gives only 4 intervals for the 790-median body — order-of-magnitude only, as the board requires, but the censoring (last interval cut) is unflagged.
