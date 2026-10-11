Grade: gold

**Abstract.** Claim: at 10⁹ bodies on the 8 GB M1 the binding term is memory capacity, not compute or bandwidth. Reproduced bit-for-bit in a clean tree (steady: 414/1738/40 hits; budget.py output identical). My adversarial cases held: another seed gives 0.0184 truth-checked (method = truth, 921/921, missed 0), ρ=1e-2 gives exponent 1.03, n=10000 gives 0.1954 (linear predicts 0.207), σ_e=1e-3 gives 0.0024, confirming the P1 post-mortem's σ_e pre-factor. Compute at belt scale is 0.024 cores today (175× margin, no levers); the board's 190 cores re-derives as 175 (all-LEO worst case); capacity breaks today at 3.2× (tubes, linear queue); H_live is 2.65 bits/body/orbit → recompile each ~1.5 orbits. Gain: deletes the event-speed hunt, aims scale work at memory (B18b, sublinear queue). Cost to adopt: a re-rank, no code.

## Reproduction

`work/patch.diff` is empty — the run used shipped code, so I reproduced from the clean tree:

- `steady 1000 0.001 20`, `steady 3000 0.001 10`, `steady 1000 0.0001 20`: every deterministic counter identical (cone_pairs 44691/412502/41889, checks 549/2738/53, hits 414/1738/40, queries, qsteps, evals all bit-for-bit; only wall-time fields differ, as they must).
- `python3 budget.py` → output identical to `budget-out.txt` (diff empty).
- Derived numbers re-checked by hand: 0.0207 = 414/20000; n-ratio 2.799; ρ exponent log(0.002/0.0207)/log(0.1) = 1.01; 40 bits/body = 5 GB/10⁹; 3.2× over; 2.65 = 0.0207×128; 15.1 = 40/2.65; 764 ev/s; 1.07 s full pass; 1 B/body/frame. All correct.
- Constants traced to frozen evidence: 29 µs (H0210, HISTORY L3106), 32.5 kicks and 114× (H0190, L2809-2810), 0.126 bits/body (components-98bc, L3130), 16-byte tube (law.md L12).

## Held-out predictions

File times are consistent with pre-registration: predictions.md 19:22:32 → budget.py 19:24:54 → budget-out 19:24:56 → steady.jsonl last append 19:25:50. All steady evidence postdates the predictions. P1's band [0.3, 5] *missing* the measured 0.0207 by 15× is itself proof the band was not tuned on a prior run. P2 held (2.80× vs 3× ±30 %), P3 held (α = 1.01 in [0.7, 1.3]). P1's miss is reported prominently and diagnosed (σ_e sets the radial spread; rate ∝ σ_e) — my σ_e=1e-3 probe below confirms that mechanism quantitatively. P7's pre-committed failure protocol was followed exactly.

## Adversarial cases (mine)

1. **Same config, different seed, truth-checked** (`verify b`: r8like-s1e-2-r1e-3, seed 20261007, 50 orbits): truth_enc = 921, method_enc = 921, missed 0, false 0 → rate 0.0184/body/orbit, −11 % vs 0.0207. Three seeds now (0.0184, 0.0207, 0.0214 = board's belt-0 427/20000) agree within ±15 %; "truth-checked hits" is fair — the method equals truth on this config.
2. **ρ upward** (`steady 1000 0.01 20`): 0.2229/body/orbit → exponent 1.03. The near-linear ρ law holds on the high side too, not just the probed low side.
3. **n = 10000, fixed volume** (`steady 10000 0.001 10`): 0.19535 vs linear prediction 0.207 (−6 %); steady_work_per_encounter stays 1.57. Cone pairs scale as density × N (461.7/body at 10× density vs 44.7 at 1×), so at fixed game density pairs/body is N-independent — the 10⁹ extrapolation of the discovery cost is sound.
4. **σ_e = 1e-3** (`verify b` row 1, 100 orbits): truth 236 → 0.00236/body/orbit, ~8.8× below σ_e=1e-2. Rate ∝ σ_e^~1 — confirms the author's P1 post-mortem and scopes the scar numbers to belt temperature (flagged by the author in (b) and the lens section).
5. **Un-amortized discovery worst case** (arithmetic from the run's own measured constants): re-setting up every cone pair every orbit at 100× rtf costs 1e9 × 44.7 pairs/body ÷ 4×10⁵ s × 12.7 µs = **1.42 cores** — under the 4-core budget *without* any per-element-change amortization. The compute-clears verdict does not lean on the unmeasured amortized regime.

## Novelty

No H entry does the three-term 10⁹ decomposition. Closest priors: the board's own "about 190 cores" (item 3 — this run re-derives it as 175 and shows it is the all-LEO adversarial bound, not the belt case); H0158 (memory-derived capacity for the *old* engine at 2.7 KB/ship — obsolete representation); the early 1e9-ship compressed sweep (16 families, zero events — H0005-era, not the tube/scar design); components-98bc (the 0.126 bits constant, an input here). HANDOFF L70 says H_live "not measured yet" — this run is that first measurement (2.65 bits/body/orbit at belt-0 config, with exponents), which is the handoff's named open question, not a re-run of known work.

## Goal fit

It corrects the premise of ranked bottleneck 3 ("We need 10–100× less" compute): at belt scale compute is 175× under *today's* rates with no levers; the levers (12.6× slack skin × 114× averaging) matter only for the all-LEO bound and take it to 0.12 cores. It installs capacity as the binding term with numbers (3.2× over today; 40 bits/body; recompile ~1.5 orbits ≈ 2 game-years). PRINCIPLES #24 ("The memory floor is information-theoretic") becomes a number; #14 ("no ticks") becomes a measured bandwidth law (1 B/body/frame). Adoption is a bottleneck re-rank plus aiming B18b at recompile cost and the sublinear queue — one step, no code.

## Reasons for the grade (and the caveats that survive it)

Reproduced exactly; held-out predictions P2/P3 held; P1 missed 15× low but was pre-committed as reportable (P7), honestly reported, and its diagnosed mechanism is confirmed by my independent σ_e probe — nothing downstream cites the predicted value, only the measured one. The verdict survives every adversarial case above. Remaining caveats, none verdict-flipping: (a) the scar model (128 bits per encounter, near-constant reabsorption cost) is assumed — the *cadence* (1.5 orbits) inherits it, though the binding-term verdict does not (tubes and the linear queue break at 3.2× with no scars at all); (b) "LEO clears" composes two levers measured in other regimes (flagged by the author in (d)); (c) the 5×10⁻⁵-core discovery row assumes the amortized per-element-change design (q-candidate-degree silver) — but the un-amortized worst case still fits (1.42 cores, case 5); (d) 5 GB usable is an assumption (flagged in (a)); at the plan's open 20 GiB budget "breaks today" softens to "no room for anything else", same verdict.

## What the author missed

- The un-amortized discovery worst case (1.42 cores at 100× rtf, from the run's own 12.7 µs/pair and 44.7 pairs/body) is the number that makes the compute verdict amortization-independent; the dossier reports only the amortized 5×10⁻⁵. It strengthens the claim and should have been in the sensitivity block.
- The ρ exponent was probed only downward; one upward run (mine: 1.03 at ρ=1e-2) closes the range.
- Seed robustness is claimed via r8 v2's belt-0 but one `verify b` run (0.0184, truth-identical) would have grounded it in this run's own evidence.
- The scar-per-encounter size (128 b = one tube) is an upper bound presented as the value; a scar is a difference record and may be smaller, which relaxes the cadence linearly. The named next experiment (recompile cost under scatter, B18b) is the right one and decides this.
