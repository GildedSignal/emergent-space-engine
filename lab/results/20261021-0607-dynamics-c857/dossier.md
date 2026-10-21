# 20261021-0607-dynamics-c857 — the genesis train does not mix to the Poisson floor: the profile is a frozen attractor

## Claim

On the shipped engine (`plane_extra`, belt 2,700, seeds 1–2), the belt's worst-window event excess over the Poisson floor does **not** decay to the floor by fire 145 — the frozen-step model's "floor by fire 100–120" endpoint (a97f, calendar od 4) is refuted — because the excess is not a mixing transient: it is the **frozen density profile of the clock's own step distribution** (shape correlation r = 0.974, stationary from g ≈ 2), plus thousands of permanently phase-locked co-firing pairs at both seeds, and the only homogenising mechanism (step diffusion, 6.9×10⁻⁵ per change-fire, unbiased, flat in g) needs ~3×10⁶ fires to smooth it.

## Bottleneck

The calendar row (per-body state, ~10×) and the 10⁹ worst-frame line: the ledger currently quotes Poisson windows "outside the epoch" (a97f's endpoint). Measured here: the allocator's worst window stays at max/μ ≈ 1.6–1.75 against the Poisson floor 1.36–1.37 at g ≥ 49 (excess +0.25 to +0.38, ≥ 2.5× the floor's p90 band) with no decisive decay. This deletes the "wait ~10² fires" option and leaves two: the stagger from birth (45c0: exact in the stationary measure) or carrying the profile contrast (~1.25–1.4× worst-frame headroom) in the 10⁹ composition.

## Evidence

Instrument (all from `crates/universe/examples/calendar_flight.rs`, pure observation: `settle` + `key_of` polling, Δ = 0.8·p10(step) epochs, at most one fire a body an epoch, multi = 0 both flights; the view's own retention `Universe::prune()` called every epoch — the flight's per-frame retention at census granularity, which keeps the process at ~0.2 GB; a never-retaining configuration is not flyable and its dues diverge from this one from g = 37):

- **Floor anchor.** Monte-Carlo uniform floor at n = 2,700, W = 64: **1.375 [p10 1.280, p90 1.470]** — digit-for-digit a97f's floor; the instrument is in the page's family.
- **Per-generation profile** (64 windows over each generation's dues; matched n = 2,700): max/μ = **4.08 at g = 1 and 3.94 at g = 129** (seed 1; excess +2.70 → +2.56); seed 2: 3.39 → 3.65 (g = 60). The median-window contrast c50 is **frozen at 0.52–0.57 from g = 2 to 129**. `work/flight_s{1,2}.txt` hold every generation.
- **Pooled worst window** (fixed L = step/32, sliding, all generations mixed — the allocator's number; `work/analysis.txt`): seed 1 excess **+20.6 (g≤16) → +0.90 (17–48) → +0.38 (49–96) → +0.25 (97–139)**; seed 2 **+19.1 → +0.84 → +0.25 → +0.28** (flat from g = 49). Floors 1.335–1.374 at μ = 72–87.
- **The profile is the step distribution.** Per-body modal steps span **11.4% / 10.9% of their mean** (seeds 1/2; the step law is near-constant across a belt whose periods span 84% — it is not ∝ T), are continuous (268,433 / 267,917 distinct values over 357,941 / 357,195 intervals — no power-of-two comb), and the g = 129 due profile correlates with the step profile at **r = 0.998 / 0.997** (64-bin shapes).
- **The drift ledger.** Per change-fire |Δstep|/step = **6.5–7.0×10⁻⁵ at both seeds, flat in g** (g = 3 → 129), signed mean −2.8×10⁻⁶ to −6.3×10⁻⁷ (seed 1) and +7.3×10⁻⁷ to +1.3×10⁻⁶ (seed 2) — unbiased within a seed and smaller than |drift| by 25–100×: no ratchet. Fires alternate change/no-change: the kick/boundary comb parity. a97f's pilot read 6×10⁻⁵ (agrees); its deep census read 5×10⁻⁴ → 2.5×10⁻³ by g = 40, which does not reproduce here at any depth.
- **Spread law.** Var(due)/step² = **2.4×10⁻⁴·g²** (fit β = 2.018 / 2.020 over g = 8 → 129, seeds 1/2): pure frozen-step shear.
- **Locked pairs.** Pairs within one window L for ≥ 8 consecutive generations: **6,654 (seed 1), 6,547 (seed 2); uniform-redraw control 0 at both seeds** — the pairwise part is structural at every seed, refuting the seed-1-only split.
- **Cost.** 352 s (seed 1) and 500 s (seed 2) on 1 core each (8 vCPU shared, Linux/x86 — orders of magnitude only); ~0.2 GB per process under per-epoch `prune()` (against 3.0–3.6 GB without it: the history ratchet, unflown past g ≈ 50 before this).

Reproduce (the runner applies `work/patch.diff` first; cold cache ~9 min, the two flights in parallel):

```
sh lab/results/20261021-0607-dynamics-c857/regen.sh
# = cargo build --release -p emergent-universe --example calendar_flight
#   + two parallel flights: calendar_flight 3000 145 1 / 2   (CENSUS_DUMP=.../work/dues_s)
#   + python3 analyze.py <run>   → work/flight_s{1,2}.txt, work/analysis.txt, work/dues_s{1,2}.bin
```

Every number above is a verbatim line of those three artifacts.

## Predictions

`predictions.md` was written before the decisive flight (tuning seen: seed 1, n = 600, g ≤ 8). Outcome:

- **P1 (floor by g ≤ 145): FAILED at both seeds** — the pre-registered kill criterion fired; this dossier's claim is that branch. The crossing did not occur; seed 2 shows no pooled decay at all after g = 49.
- P2 (β ∈ [1.0, 1.6]): **wrong in magnitude** — β = 2 exactly (pure shear; the drift is 7–10× too small to bend it by g = 96). Direction (super-linear, no clean diffusion) held.
- P3 (drift < 10⁻², signed < 10% of |drift|): **passed** (6.9×10⁻⁵ flat; −2×10⁻⁶ signed).
- P4 (seed 2 endpoint ≤ seed 1): **passed** on the pooled excess (0.28 vs 0.25, both ≫ floor); failed in its premise — seed 2 has locked pairs too (6,547).
- P5 (c50 → 0.93 ± 0.04): **failed** — c50 is frozen at 0.55 (the same finding as P1, seen by the second statistic).
- P6 (span ∝ g): **passed** (0.105·g exactly, g = 1 → 96).

## What would make it wrong

The floor claim is anchored to a97f's own 1.375 floor, so an instrument mismatch with the page's fixed-window definition cannot break the refutation: the refutation needs only that the engine's own uniform control (MC floor, and the uniform-redraw pair control) sits at 1.36–1.37 / 0 while the engine sits at 1.6–1.75 / 6,547+ at g ≥ 97 — all internal. What would break it: a mechanism that mixes the *step distribution itself* on a horizon ≪ 10⁶ fires that my census cannot see (e.g. a rare regime the belt enters later — encounters are off in this plane; stirring/burns are the unflown arm), or a97f's deep-census drift (2.5×10⁻³ by g = 40) being real on a population mine excludes (my ledger covers every belt body, both seeds, to g = 96 at n = 2,700 — it does not reproduce there). Adoption cost: none for code — this is a ledger/endpoint correction plus one design decision (stagger-from-birth vs carry-the-contrast); the stagger's B-gate flight (kick-cadence od 8) becomes the blocking item. Fit with PRINCIPLES: #22 ("the simulation tells us what's next not us") — the worst window is readable from the frozen profile at genesis, for free; #2/#21 — the error is one of model endpoint, and the falsifying test was the cheapest one (fly the engine past the extrapolation).

## The lens

The attractor got delivered, but the lens nearly cost the run: I first read the flat per-generation table as "no mixing at all" and nearly missed that 45c0's and a97f's "mixing" (C50 → 1.2 by g ≈ 25) is the *within-profile* scrambling, real but invisible in the worst-window statistic that the ledger actually quotes — two different coordinates on the same flow. The blind spot that remains: long-run behaviour past g = 145 (a 3×10⁶-fire flight is ~50 core-minutes per seed — cheap for a checker to extend by 10×, and the locked pairs' |Δstep| tail decides whether they unlock before the profile diffuses).
