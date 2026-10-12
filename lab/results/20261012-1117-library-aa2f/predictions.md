# Predictions (written before the probe runs)

Probe: `probe_skin.py` — synthetic belt on analytic circular orbits (the generator philosophy: positions re-derived, never integrated), close approaches = coincidences within R_enc at checkpoints. Truth = exact x-sorted sweep per checkpoint. Structures compared (only their own work counted; per-checkpoint position derivation is free — it is the generator's job, already paid):

- **A** (global skin): per-body lists, radius R_enc + w, but ALL bodies rebuild when ANY body's displacement > w/2 (the naive shared Verlet trigger).
- **B** (per-pair/per-body trigger, the rLIN rule): a body refreshes only its own list when its own displacement > w/2. Zero-miss guarantee by triangle inequality (list radius R_enc + w covers any pair while both owners' displacements ≤ w/2).
- **C** (submax skin + earliest-deadline smoothing): trigger at w/3, refreshes capped per checkpoint (deferred), hard barrier at w/2 (guard). The Bruce-Lesson: carry the tail with a guard, don't size the whole skin by it.
- **E** (element-window tier, r8 v2's killed tier, arithmetic only): setup = all pairs with overlapping a-windows.

Work = pair-evals + structural ops (grid insert/remove/query, rebuild), each distinct event counted once (the memo-artifact lesson). Cases tuned on: belt N=20k, fixed density. Held-out cases (not tuned): eccentric tail (10% at e 0.7–0.9), formation (5k bodies on one orbit, concentrated), dilution (N=10k/20k/40k at fixed density).

## Predictions

1. **Zero misses for B and C** on every workload (the trigger is a proven bound, not a heuristic). A is also zero-miss but pays for it globally.
2. **A's work per real encounter grows with N at fixed density; B's stays constant** (within 2×). Mechanism: A's rebuild rate is set by the *fastest* body among N — the distribution of the maximum — so the whole belt pays for one mover. This is the library lesson made literal (Taleb: "the maximum of an average is necessarily less volatile than the average maximum").
3. **p99/median of per-checkpoint work: A ≥ 10× B's** on the mixed belt (rebuild storms = the tail Julien's p99 rule targets); C's p99/median < B's (smoothing works) at zero misses.
4. **Submax vs max-safe skin:** B with w sized to typical relative motion (p50 × 4) vs w sized to worst-case closing over 20 checkpoints: zero misses both, work per encounter within 1.5×, but max-safe list memory ≥ 2× (fewer bodies per list refresh amortize worse... direction uncertain — this one I am not sure of; recorded as uncertain).
5. **Held-out eccentric tail:** A's rebuild rate jumps ≥ 3× vs plain belt (the few disproportionate movers); B's work per encounter unchanged (< 1.5×).
6. **Held-out formation:** E's setup work per real encounter is ≥ 100× B's (quadratic in the fleet — confirms the gold taleb-09b5 kill at the tier); B's work per real encounter stays ~constant under concentration because physical per-pair lists never see the co-orbital pile-up.

## Kill criteria for the lesson (not the method)

- If B misses any true coincidence → the per-pair trigger lesson is wrong as stated (the guarantee failed in practice).
- If B's work per encounter grows with N at fixed density → the claim "triggers make work track encounters" dies; only the tier result survives.
- If A ≈ B on p99/median (within 3×) → the trigger-granularity lesson is a nothing-burger for smoothness; say so.

If predictions 2/3 hold and 1 holds, the design change is adoptable within one step: the slack-skin build (in flight in both GLM and Codex lanes) uses per-body triggers with local repair and deadline deferral, never a global rebuild or periodic polling.
