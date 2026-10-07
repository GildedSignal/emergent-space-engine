Grade: silver

**Abstract.** Fermi run on H_live (HANDOFF: "not measured yet"): at 10⁹ bodies the 8 GB promise is gated by the individualized fraction (f_ind ≤ 0.375 at 6 GB, 16 B tubes), not the encounter stream — ship/rock mutual encounters carry ~0 bits (δv/v ≤ 10⁻¹⁰ even after my ×57 conjunction-speed correction). Reproduced bit-identically in 0.4 s; P2–P4 held. But the headline creation rate (3.8×10² bits/s) assumes every body is a 10²² kg embryo: the stated 10³-embryos-among-10⁹ scenario gives 3.8×10⁻⁴ bits/s; the inclination systematic is ~540× at tight ρ, not ×2–3; the r8 claim check floated N (frozen at 10⁴). The priority call — build nothing for encounter memory, instrument f_ind — survives every attack. Gold needs the queued b-h-live engine measurement.

## Reproduction

- `python3 hlive.py` → bit-identical to `hlive-out.json`, 0.35 s, seeded. `work/patch.diff` is empty (no tree edits). `predictions.md` mtime precedes the script and its output by ~5 min; log order consistent.
- Independent recomputation from `belt.rs`/r8-v2 rung sources: geometry claims check out (coplanar, Rayleigh e capped 0.5, a∈[1,1.5], 20 orbits).

## Adversarial cases (mine)

1. **Embryo fraction kills the headline.** `creation_bits_per_game_s = 1e9·r_bits·3/yr_s` counts every within-b_bits passer as an embryo (f_emb = 1). The dossier's own scenario (10³ embryos among 10⁹, f_emb = 10⁻⁶) gives **3.8×10⁻⁴ bits/s**, 10⁶ below the 3.8×10² headline; even f_emb = 10⁻³ gives 0.38 bits/s. Same factor in materialization (0.39/s → 3.9×10⁻⁷/s) and the "80 game-years" horizon (→ ~10⁸ yr). So "every measured H_live term is 3–8 orders below the floor" is not established: the margin for the largest term spans ~6 orders on an unmeasured game-design parameter. P5's self-grade flips: it missed low, not "just missed high". (Conservative direction — the claim survives a fortiori.)
2. **Impulse speeds understated ~57×.** The table uses v = v_K = 1, but the script's own `conj_sample` measures median conjunction v_rel = 0.0175 v_K (it is computed and dropped). Δv/v_K = 2μm/(b·v_rel): embryo@10⁻⁴ AU is ~6×10⁻³, not 10⁻⁴; b_bits widens ~×50 to ~0.5 AU (wider than a doll's annulus). Ship/rock conclusions still hold (rock 10¹⁵ kg at 15 km: ~6×10⁻⁷, marginal only for near-contact events).
3. **Inclination systematic understated by ~2–3 orders at tight ρ.** MC with σ_i = σ_e = 0.01: P3D/P2D = 1.9×10⁻³ at ρ = 10⁻⁵, 5×10⁻³ at 10⁻⁴, 0.47 at 10⁻². The stated "×2–3" holds only at b ~ 10⁻² AU (the embryo-bit scale), not at the tight thresholds that decide the r8 claim check and strong-scatter rates. Belt 0 is genuinely coplanar, so the claim check itself is at correct geometry; the extrapolation statement is wrong.
4. **r8 claim check floats a frozen parameter.** The rung pins N = 10⁴ and draws σ_e log-uniform in [10⁻³, 3×10⁻²]; the dossier asserts σ_e = 0.01 as "belt-0's own generator shape" (unsupported — in-tree `verify_set` has no belt 0) and fits N = 4250, ρ = 10⁻⁵. At frozen N = 10⁴: σ_e = 0.01 misses candidates ×3.7 and encounters ×5.8–150 over the ρ band; an in-band (σ_e = 3×10⁻³, ρ = 10⁻⁵) matches both within ×1.2–1.8. So the model is consistent with r8 v2 at factor-2 level, but "reproduced within a factor 2" is earned by parameter freedom the author only half-discloses (N yes, σ_e no).
5. Minor: b_bits = 1.5×10⁶ km, not the dossier's "1.5×10⁵ km" (10× prose slip; JSON AU value is right). Cadence arithmetic verified: 1.6×10⁶ step-events/s at rtf 100, 950 events/s averaged, ratio 1700×.

## Predictions

P1 held only with N free (disclosed); P2 held strongly (survives the ×57 correction); P3 held; P4 held (10²–10³ vs ≥0.1); P5 did not hold and its self-grade is wrong once f_emb is applied. Timing consistent with pre-registration.

## Novelty

HANDOFF's H_live was explicitly "not measured yet"; H0173's ~4 bits/collision is collision-refinement floors, a different question; the 190-core and 0.126 bits/body figures are pre-existing (board/taste log) and used as claim checks, properly attributed. The f_ind gate formulation and the encounter-bits quantification are new on the record. Not the queued `b-h-live` build: that brief asks for a digest-safe definition and measurement in `xtask universe --bench` — no engine code here, so "not measured yet" stays true in the engine sense.

## Goal fit

Board: "fitting 10⁹ in 8 GB … decided by distinctions created per game-second"; PRINCIPLES #24 "the memory floor is information-theoretic" and #10 "run the simplest falsifying test first". The priority call — encounter memory is a non-problem at ship/rock mass; gate f_ind; do not spend on encounter-memory — is the run's real product and it survived all four attacks (each error conservative or gated by f_emb).

## Why silver, not gold

The central claim is real, reproduced and robust, but the quantitative dossier is not: the largest H_live term is 10⁶ inconsistent with its own scenario, the impulse table is ~57× off, the stated inclination systematic is ~540× off at decision thresholds, and the claim check's "factor 2" rests on floating frozen parameters. Nothing here can be adopted as numbers; only the direction is adoptable.

**The one experiment for gold:** the queued b-h-live build itself — define H_live from engine state and measure f_ind/bits-per-scar in the plane's belt scene — which simultaneously pins f_emb and the impulse accounting on a real population and turns this Fermi gate into a measured one.

## What the author missed

The embryo-fraction accounting (the load-bearing number), the v_rel already computed in their own script, the true magnitude of 3D geometry at tight ρ, that belt-0's N and σ_e are frozen/unknown rather than fitted, that P5's self-grade inverts, and the b-h-live brief's actual deliverable (engine instrumentation, not estimates).
