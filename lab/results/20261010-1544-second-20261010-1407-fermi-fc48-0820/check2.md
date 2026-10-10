Grade: gold

**Abstract.** Claim: the parent's headline holds with corrected numbers — the checker's 3-field floor (61.6/62.1 bits/body = 7.70/7.77 GB at 10⁹, confirmed) omits the tube's phase field (t_p, 64-bit per cycle, uniform by belt.rs's own generator), so every exact non-replay encoding at the tube's quanta pays 125.5/126.1 bits/body = 15.7/15.8 GB ≈ 2× the 8 GB budget; the "under budget, ≤3% margin" restatement was a field-scope artifact. I reproduced everything: `hlive.py` regenerates `hlive.json`/`final_state.npz` byte-identically (77.6 s), `floor.py` 75.5/76.1, `floor9.py` exact to the last digit; my independent attacks (fresh seeds, a direct 4-field multiset floor 125.59, N=2²², collision count 10⁻²⁹, EF port vs program.rs) agree to ±0.1 bits. Adoption: the parent's requantization decision, now on honest numbers.

## Reproduction

- `python3 hlive.py` (77.6 s): `hlive.json` and `final_state.npz` **byte-identical** to shipped (`cmp`), log identical to the author's `rerun-hlive-patched.log`; pre- and post-patch full-run logs identical. `floor.py`: 75.5 birth / 76.1 final ✓. `floor9.py` (0.8 s): every scalar and all 10 rows of `floor9.json` match exactly — floor₃(10⁹) 61.58/62.14 = 7.70/7.77 GB; phase 63.96; floor₄ 125.54/126.09 = 15.69/15.76 GB; strict reading 90.4 = 11.30 GB; EF gap +1.06.
- T_ORBITS=2 quick path runs in 0.41 s (the slope-guard patch works; full-run output unchanged by it).
- Spec provenance: law.md line 12 — tube = "(quantized E and L, 32 bits), periapsis angle (32 bits), periapsis time (64 bits; epoch and phase collapse into this one time)", "position and velocity are derived when asked" — the phase is the tube's 4th stored field. belt.rs: uniform a, Rayleigh e (independent normals ≡ Rayleigh + uniform angle), uniform longitude → the phase is uniform by the repo's own generator.
- Predictions: `predictions.md` 15:53:46 precedes `floor9.py` 15:58:05 by 4.5 min; all six held within stated tolerances (P2 slope −0.996 vs −1.00±0.02, H₁ 90.03/90.59 vs 90.0±0.4/90.6±0.4; P3 125.5/126.1 vs 125.5±1/126.1±1; P4 90.4 vs 92±3; P5 +1.06 vs ≤3; P6 +0.89/+23.2 vs ≈0/+23). Kill criterion did not trigger.

## Attack (my own)

1. **Direct 4-field floor, no additivity assumption:** fresh birth at N=2²⁰ with the phase inside the measured multiset: H₁₄ = 154.05, floor₄(10⁹) = 125.59 bits = 15.70 GB — matches the author's floor₃+64 (125.54) to 0.05 bits. The +64 is not a bookkeeping trick.
2. **Seed and scale stability:** fresh seeds 999/12345 give H₁ = 90.049/90.051 (analytic 90.087); at N=2²² H₁ = 90.048 and floor₃ drops exactly 2.00 bits from 2²⁰ — the −log₂N slope continues past the author's range. Expected pair collisions at 10⁹ on the 4-field grid: 2.9×10⁻²⁹, so the sparse-regime formula H₁ − log₂N + log₂e is exact, not asymptotic hand-waving.
3. **Can a cleverer class escape?** The multiset floor is a lower bound for any exact lossless encoding of the state; identity-keeping costs more (scar row 126.4→149.3 bits, over budget throughout); the EF port is faithful to program.rs (l = ⌊log₂(u/k)⌋, nhigh = (u>>l)+k+1, u32 per 64 zeros) and sits +1.06 bits over the uniform bound, so no operational encoder rescues the 2× gap. The only escapes are exactly the two the dossier names: replay (compute-for-memory) and requantization.
4. **Phase-uniformity after stirring:** shipped H_tp_mod saturates at 63.9 by 1024 orbits — using 64 bits for the heated state too is right, not just for birth.
5. **Robustness of the verdict to the spec reading:** the strict 16-byte reading (90.4 bits, 1.41× over) was measured on the birth state only; the heated (E,L) support is wider (σ_e 2.9×), so it is a lower bound — the direction favours the verdict.

## Novelty and fit

No prior measurement covers this: components-98bc (gold, 5 Oct) measured the *smooth* belt (0.126 bits/body, program class — no stirring); H0190 measured kicks/orbit, not entropy; the parent's checker named the 10⁹ re-issue and the encoding-class question as the gap to gold. This run does both and corrects the corrector: the decision number for B18's stirred clause at 10⁹ is 125.5/126.1 bits/body, not 61.6. Bottleneck "fitting 10⁹ in 8 GB" moves from "fits, 3% margin" to "2× over at the tube's own quanta — requantize or replay". Principle 24 ("the memory floor is information"): served — measured, with the phase dof counted, which is the whole correction. Principle 2: "exact" judged as information at the tube's own quanta, not trajectory identity. The lens caveat (shared harness with the parent) is disclosed; my independent recomputation covers the parts that matter.

## Why gold

The second-author contract was: make the record regenerate, run the checker's named experiment, and see if the claim then holds. All three done, and the answer is a decision-grade reversal of the checker's restatement: a premise the integrator would have adopted ("floor under budget at 10⁹") is shown wrong in scope, on pre-registered predictions that held, with byte-identical records and honest disclosure of both escape hatches (replay; t_p anchoring). Every number I attacked survived to ±0.1 bits. Adoptable within one step: it settles the number the parent's adoption decision needed.

## What the author missed

- P1's byte-identical observation (rerun log 15:53:14) precedes predictions.md (15:53:46) by 32 s; only P2–P6 were genuinely held out. The wording "written before floor9.py ran" is accurate but P1 was observed, not predicted.
- The "~43 doublings" margin-loss figure extrapolates 0.056 bits/doubling (measured over 10) just as the checker's "~10⁴ orbits" extrapolated σ_e — the author's is better grounded (field entropy, not σ) but it is still an extrapolation, and it does not affect the verdict (the 4-field class never fits).
- B18's frozen bar "≤ 2× the measured information floor + 2 bytes" is ambiguous about *which* floor: under the floor₄ reading the scar form (≈1.0–1.2× floor₄) would pass B18 while violating the 8 GB goal; under the program-floor reading (0.126 bits) nothing passes. The dossier asserts "passable for neither class" without disambiguating; the 8 GB verdict is unaffected either way, but the B18 sentence needs the integrator's reading of the frozen text.
- The e-quantum Jacobian (Q_E = Q_L/√1.2 constant in e, true dL/de ∝ √a·e) is inherited from floor.py; ±1 bit as noted, immaterial against a 62-bit margin.
