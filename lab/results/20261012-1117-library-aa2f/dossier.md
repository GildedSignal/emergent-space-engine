# Dossier — 20261012-1117-library-aa2f (library lens)

**Claim.** The slack skin's trigger must sit on accumulated element drift against a quantum (`W_SLACK ≤ R_ENC/2`, a provable 1-D triangle-inequality bound), never on kick arrival: measured 3.4× less work per real encounter at the plane's kick rate, 10.9× when kicks are sparse, zero trigger misses everywhere, flat under co-orbital concentration while the standing element tier is 106× quadratic — and the failure mode that remains is width, not trigger: an `|Δa|` window leaks 28% of eccentric-tail encounters.

**Bottleneck.** The board's top scaling risk (candidate work must track real encounters) via the named lever (the slack skin, 12.6×, "nothing to build" yet — build slots open in both the GLM and Codex lanes). This run derives the trigger rule the skin build should implement, its gain formula, and its honest failure mode.

**Evidence** (probe: `probe_skin.py`, deterministic, 38 s, < 300 MB, Linux x86 cloud — orders of magnitude only; machine: load 2.70/8 vCPU, 13 GB free):

    python3 probe_skin.py          # writes probe_out.json

Element-space model: analytic generators (no ticks), kicks are the only element changes, certs = a-windows + predicted conjunction deadlines, truth = independent physical x-sweep. A = pay per kick; B = pay per quantum crossing; identical seeded kick realizations.

| case | A work/enc | B work/enc | gain | width-miss |
|---|---|---|---|---|
| belt 10k/20k/40k, λ=32 (fixed density) | 127k / 104k / 114k | 37.7k / 30.8k / 33.7k | 3.4× flat in N | 0 / 0 / 0 |
| belt 20k, λ=0.5 | 6 326 | 579 | 10.9× | 0 |
| belt 20k + tail (10% at e 0.7–0.9) | 117k | 34.7k | 3.4× | 95/341 = 28% (identical for A and B) |
| formation 5k (concentrated) | 145k | 42.9k | 3.4×, flat vs belt | 0 |

- Gain mechanism: kicks-per-crossing ≈ `W_SLACK / (0.8·σ_kick)` — a dial, not a constant. At σ=5e-5, W=1e-4: 2.5 expected, measured 3.4× (window sizes at crossing vs kick times); at sparse λ the walk collapses and the gain is superlinear (10.9×).
- Standing wide element tier vs skin's live pairs (setup, arithmetic): belts 127–156×; formation **106×** (11.55M vs 108k pairs) — independently reproduces gold `20261006-0346-taleb-09b5`'s 135×.
- Smoothness: absolute per-checkpoint p99 is 3.4× (λ32) to 10.9× (λ0.5) lower for B, but B's own p99/median worsens at sparse λ (2.42 vs A's 1.27): quantum crossings burst; the least-slack allocator (bottleneck 4) still has a job — repairs need deadline budgets.

 
- Held-out parameter (not tuned on): σ_kick = 5e-6 (10× smaller) → measured kicks-per-crossing 27.6 against the formula's 25 (work/enc gain 37×; `probe_skin_smalkick.py`, `probe_out_smalkick.json`). The dial is real: kick-size reduction multiplies the skin's amortization exactly as `W_SLACK/(0.8σ_kick)` says. B's p99/median rises to 4.0–4.3 there (crossings rarer still): the allocator tie-in sharpens as kicks shrink.
**Predictions** (`predictions.md`, written before the run):
1. Zero misses for B — **held for every circular workload** (the trigger bound never failed); the tail leaked 28%, but through cert *width*, identical for A and B: a geometry failure, not a trigger failure. New finding, not predicted as such.
2. A grows with N, B constant — **half failed**: both are flat at fixed density (per-kick repair is local too); the real lever is the quantum ratio, constant 3.4× across all workloads at λ=32.
3. A's p99/med ≥ 10× B's — **failed as a ratio** (both smooth; B's ratio is worse when sparse); **held in absolute p99** (3.4–10.9× lower). Structure C (budget smoothing) not built — time; B's measured burstiness is now the motivation for it.
4. Submax vs max-safe skin — **not run** (time).
5. Held-out tail: A jumps ≥3× — **failed** (A flat). Held-out formation: E ≥ 100× B, B constant under concentration — **held** (106×; 42.9k vs 30.8k).

## The five lessons (the lens deliverable)

1. **Trigger on the accumulation, not the arrival.** *Fooled by Randomness*, Taleb: "By a law of probability called distribution of the maximum of random variables, the maximum of an average is necessarily less volatile than the average maximum." Paying per kick pays the arrival process's rate; paying per drift crossing pays an average-type statistic. Change: skin fires on `Σ|da| ≥ W_SLACK`. Test: probe, 3.4–10.9×, zero misses.
2. **The gain is amortization, so spend on kick size.** *The Personal MBA*, Kaufman: "Amortization is the process of spreading the cost of a resource investment over the estimated useful life of that investment." Cert life ≈ `W_SLACK/(0.8 σ_kick)` kicks. Change: `W_SLACK` and `σ_kick` are one budget — cap `W_SLACK` at the bound `R_ENC/2`, then every upstream kick-size cut (H0190 tide averaging: 114×) multiplies the skin's amortization for free. Test: 1-line param change, rerun.
3. **Size by the typical; carry the tail with a bound.** *Bruce Lee* (ed. John Little): "training with submaximal loads (as little as two-thirds of maximum strength) twice weekly, and maximal loads once weekly, would result in as much strength improvement as training maximally three times per week." Never size the skin by the worst-case kick (that is paying every kick); the triangle bound `W_SLACK ≤ R_ENC/2` is the guard. Test: zero width-misses on all circular workloads despite 5%-tail kicks.
4. **Dilution is Mediocristan; concentration is the regime switch.** *The Black Swan*, Taleb: "When your sample is large, no single instance will significantly change the aggregate or the total." Work/encounter is flat in N at fixed density (10k→40k); formations break the element tier (106×) but not the skin (flat). Change: no tier widening under concentration — switch regime by a dimensionless number (PRINCIPLES #4), as gold taleb-09b5 already ruled.
5. **The wide tier's memory has alternative uses — delete it standing.** *Basic Economics*, Sowell: "Economics is the study of the use of scarce resources which have alternative uses." The standing element tier holds 106–156× more pairs than the skin needs. Change: per-body skins only (~60-entry windows); re-derive broad pairs on demand — "store the generator, not the generated" (PRINCIPLES #6). Test: E-setup/B-live columns above.

**What would make it wrong.** Correlated kicks (drift then not a random walk; crossings clump and the gain formula breaks); real-plane λ and σ differ (formula given, so checkable in one run); conjunction-eval counts are an analytic estimate (small either way, equal for both); eccentric populations already break the `|Δa|` window (28%) — the skin needs radial-range windows `[a(1−e), a(1+e)]` there, which is the next experiment, not a patch.

**Cost of adoption.** Small: the skin build is in flight in both lanes; this is a trigger rule (accumulate-then-cross vs pay-per-kick) with a provable bound, no new structures. Failures stay machine-readable if the width leak is tested by the same sweep truth.

**Fit with PRINCIPLES.** "influences below one quantum accumulate" (#6 — the trigger is literally that rule); "No work for no reason, so no ticks… we only care about changes" (#14); "Compute only surprises" (#3); "error type over error size" (#2 — a bound, not a statistical sizing).

**The lens (blind spot).** Julien's Readwise library (770 books, 4,580 highlights, fetched and cached as `rw-0.json`/`library.json`) is Taleb-heavy; the practitioner books this lens most wants (Kelly's *More Than My Share of It All*, *Boyd*, *Ignition!*, *Structures*, *Reminiscences of a Stock Operator*, Jaynes) are on the to-read shelf with zero highlights — every quote above is verbatim and retrieved, but the lessons inherit Taleb's tail-obsession and underweight flight-test practice. The probe is an element-space toy (one orbit, circular-dominated, Gaussian independent kicks, single primary); numbers are orders of magnitude, and the checker should try σ_kick and λ variants — the gain formula is the falsifiable part.
