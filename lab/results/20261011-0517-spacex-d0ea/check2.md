Grade: gold

**Abstract (for the integrator).** Claim: the belt's live distinguishing information on the plane's own path is a one-time ~146 bits/body at exact quanta (~69 at the memo cell), flat after orbit 1, dominated by orientation-coupled synodic scatter — so the program+scars store at the law's current quanta cannot hold 10⁹ bodies in 4 GiB (8.6–18.3 GB, cold alone). Reproduced bit-faithfully: the small config matches the stored decisive run within 0.06 bit and the author's cadence control exactly; deterministic across reruns. My probes confirm the attribution: scatter drops exactly 10 bits/field per 1000× planet mass (μ-linear to μ=10⁻⁹ — physical, no rounding floor), the M=512 distribution is quasi-uniform (log₂(1+range) is a fair cost, headline slightly understates), and deviations are smooth in birth orientation (ρ≈0.998), so the named epicycle-generator fix is viable. Nothing to adopt as code; it sets the belt-store requirement.

## Reproduction (clean tree, `work/patch.diff` applied)

- Small config (`HL_RADII=8 HL_M=32 HL_ORBITS=5 HL_SNAPS=5`): 9.3 s, 444 MB RSS. At orbit 5, shared radii: bits_exact 149.53 / 158.36 / 162.74 vs the big run's 149.59 / 158.38 / 162.78 (≤0.06 bit); identical to the author's `ctrl-step7.csv`. Deterministic across my two runs.
- `analyse.py belt-hlive.csv` regenerates every dossier number: cold 27/33 groups, exact 146.14→148.19, cell 68.16→69.64; field means p 43.6 / k 39.6 / ang 25.3 / t_p 37.75→39.24 (+0.078/orbit, the only growing cold field); hot 6/33 = 18.2%, hot-weighted 81.4 bits → 10.18 GB; cold exact 18.83 GB. `belt-hlive.time` confirms 2:16 wall, 6.09 GB max RSS — the decisive config exceeds the lab's 2 GB cap (honestly reported; I did not rerun it; the small repro carries the result).
- Arithmetic checks: 146×10⁹/8 = 18.3 GB, 69→8.6 GB, both > 4 GiB; hot cap 128 bits matches law.md's 16-byte tube; scene geometry (μ-linear 5.2 AU planet, 88 yr ≈ 2.8×10⁹ s) checks.

## Adversarial cases (mine, all under 700 MB)

1. **μ → 10⁻⁶ and 10⁻⁹** (the negative control predictions.md wanted and couldn't run): bits_exact 150.5 → 110.6 → 70.8 at r=2.70 — **exactly 10 bits/field per 1000× mass drop, linear in μ, no floor down to a Ceres-mass planet**. This establishes what the cadence control could not: the scatter is planet-coupled physics (synodic), not kick sampling, not rounding, not an artifact. It confirms the dossier's attribution with a cleaner instrument.
2. **M=512 vs M=32** (cold radius, 2 orbits): 156.6 vs 150.9 bits_exact. The distribution is quasi-uniform (range/sd ≈ 3.0, largest gap ≪ range), so log₂(1+range) is a fair fixed-width cost, not outlier-inflated; entropy at these quanta ≥ 9 bits/field (all 512 distinct). The M=64 headline *understates* by ~5 bits — the verdict is safe in the conservative direction.
3. **e₀ = 0.2**: same shape — one-time ~148 bits, flat (149.5→148.2 over 5 orbits at a cold radius); resonance still grows. The single-scene limitation does not change the answer's form.
4. **Smoothness in birth orientation** (from per-ship dumps): lag-1 ρ = 0.998 (p), 0.997 (k), 1.00 (t), sign-change rate 0.01 — the scatter is a smooth function of synodic phase. The author's "what would make it wrong" (first-order epicyclic generator absorbing it, residual → O(μ²)) is confirmed viable; that experiment is well-posed.

## Predictions

`predictions.md` (26 min before the decisive CSV) existed pre-run; the dossier discloses every miss prominently and correctly: saturation held, magnitude missed 7× (the transient is the full kick scatter); resonant slope held, the 5× level missed; the verdict flipped the author's own way (predicted 14 bits fits; measured 69–146, fails). The pre-registration worked as designed — it caught the author's optimism, and the miss *is* the finding. Not tuning: the measurement contradicted the author's stated hope (SpaceX-lens builder's optimism, named in "The lens").

## Novelty and goal fit

- HANDOFF L70 / plane.md L36: H_live "not measured yet" — this run is the queued measurement, on the board's named shipmem bottleneck ("fitting 10⁹ in 8 GB … decided by distinctions created per game-second").
- Prior belt gold (components-98bc, PRINCIPLES L99) measured the *birth* program (0.126 bits/body); law.md's store (program + sparse scars) is exactly the premise tested. No prior H entry measures live scar growth.
- PRINCIPLES 24 ("the memory floor is information") now has its belt number; Principle 6 survives only with the richer generator, as the dossier says. The finding kills a premise (bare averaged generator + sparse scars at current quanta), the gold prong "shows that a premise is wrong", and is adoptable within one step as the belt-store requirement (Sol's belt/B18b lane).

## What the author missed

- The μ-sweep control (my case 1) was available, cheap (3–10 s each) and decisive for the attribution; the cadence control left the rounding hypothesis open.
- The M=512 probe (fairness of log₂(1+range), and the +5.6-bit M-growth showing the headline understates) — the author flagged the bound but the probe was in reach.
- The smoothness-in-α probe (5 lines) would have confirmed the epicycle escape's viability now rather than naming it.
- Total cold growth is 0.108 bit/orbit (146.14→148.19 over 19), not just t_p's 0.078 — between prediction 1's own 0.1 threshold and the 0.3 kill line; whether clock decoherence saturates needs a longer run (≥50 orbits), which the 6.1 GB RSS made impossible here. The one-time-floor verdict does not depend on it.
- The decisive command itself breaks the lab's 2 GB memory rule (6.1 GB, reported); future H_live runs need smaller HL_SNAPS or a streaming measure. The 2.9 MB/ship live-RSS side-flag is a real second idiot index, correctly flagged, unmeasured.
