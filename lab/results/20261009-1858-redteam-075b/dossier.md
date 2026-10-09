# Dossier — 20261009-1858-redteam-075b (lens: premise red-team)

## Claim

The design's kick-absorption sentence — *"a cycle's derivatives are stored with it, so a kick updates the cycle by a multiply-add"* (representation.md §3), which §6's cost row *"undisturbed orbits ≈ 0 / a cycle's first computation: new invariants only"* rests on — carries a **systematic, compounding per-kick bias** (the second-order curvature of the exact cycle map) that is harmless in the cold mid-field but reaches **radian-level apsidal phase error within 1000 kicks near the separatrix** (p ≈ 6 + 2e, where slingshot-grade orbits live), at any memo bucket that does not recompile per kick; per-kick recompiles at H0190's 32 kicks/orbit cost ≈ 1200 crossing-evals/orbit, **above the 350–700 fixed-step control**, so on hot orbits the compiled memo loses to plain stepping.

## Bottleneck

Board focus line 1 ("fewer kicks per orbit at the same behaviour: kicks dominate the engine's cost") and bottleneck 6 (cost ≈ 0 for undisturbed bodies). Expected gain of adopting the fix: not a speedup — it **deletes a wrong premise** and redirects hot orbits to the dense order that already exists (the design's own regime for "many necessary interactions"), instead of paying recompiles inside a dead memo. Order of magnitude of the error killed: 14–96 rad of navigation phase.

## Evidence (float64, Linux x86, 8 vCPU shared, loadavg 0.2→3.8, all commands ≤ 60 s)

Law: 1PN Binet u″ = C + 3u² − u, M = c = 1, elements (C = 1/L², K) with exact turning points (1±e)/p. Truth: RK4 h = 1e-3 (h/2 changes nothing above 6 digits; weak-field F0 matches 6π/p + the known higher-order terms, e.g. p = 1000: +0.46%, p = 200: +2.3%), kicks applied at each periapsis as exact element jumps with (u, u′) continuous. Design paths carry only the cycle map F(C, K) (apsidal advance per cycle): **ignore** (negative control), **stale** (one compile + derivatives forever, representation.md literal), **bucketed q** (the live mechanism: memo keyed by quantized (C, K), fresh exact F + exact FD derivatives per bucket, linear inside), **recompile** (positive control: matches truth to 7.3e-12–9.1e-9 rad everywhere, including every catastrophic row below — the failures are the mechanism's, not the harness's).

```
gcc -O2 -o kick_absorb kick_absorb.c -lm
./kick_absorb 20 0.5 1e-4 0 2000 -2 -1 -3 1e-2 3e-3 1e-3 3e-4   # cold orbit, all paths
./kick_absorb 8.0 0.8 1e-4 0 1000 -1 -3 1e-2 1e-3 3e-4          # hot (near-separatrix)
./kick_absorb 8.5 0.9 1e-4 1 600  -1 -3 1e-2 3e-3 1e-3 3e-4     # hot + systematic drift
./kick_absorb 8.0 0.7 1e-6 0 1000 -1 -3 3e-3 1e-3               # bucket-phase luck
```
Full logs: `sweep_main.log`, `sweep_sep.log`. Numbers (max |Φ − φ_periapsis| in rad):

| orbit and kick train | stale | q=1e-2 | q=1e-3 | q=3e-4 | recompile |
| (20, 0.5) cold, ε=1e-6 rnd, N=2000 | 8.2e-7 | 8.2e-7 | 8.2e-7 | 6.1e-5 | 7.3e-12 |
| (20, 0.5) cold, ε=1e-4 rnd, N=2000 | 8.2e-3 | 1.6e-2 | 3.5e-4 | 3.3e-5 | 8.4e-11 |
| (20, 0.95) cold, ε=1e-4 rnd, N=2000 | 8.5e-4 | 2.0e-3 | 4.1e-4 | 3.0e-5 | — |
| (20, 0.5) ε=1e-5 **systematic**, N=2000 | 0.32 | — | 3.7e-4 | 3.4e-5 | 1.4e-10 |
| (8.5, 0.9) ε=1e-4 rnd, N=1000 | 0.033 | 6.8 | 1.7 | 0.14 | 5.1e-10 |
| (8.0, 0.8) ε=1e-4 rnd, N=1000 | 0.071 | 81 | 21 | **1.35** | 3.1e-9 |
| (8.0, 0.7) ε=1e-4 rnd, N=1000 | 0.37 | 458 | 4.6 | 0.36 | 9.1e-9 |
| (8.5, 0.9) ε=1e-4 **systematic**, N=600 | **96** | 63 | 3.6 | 0.26 | 2.3e-9 |

- **Driver is distance to the separatrix, not e.** Cycle-map curvature |∂²F/∂C²| ≈ 1e7–1e8 at p = 20 for every e ≤ 0.95 (non-monotone in e), ≈ 1.6e7 at (8, 0.7) base but **growing to 4e10 along the kick walk** as the orbit drifts toward p = 6 + 2e. The per-kick bias is ½|F″|·(offset from bucket centre)², systematically signed, accumulating ~linearly in cycles.
- **Bucket-phase luck.** Same orbit, same kicks: q = 1e-3 lands seed-aligned → 3e-7 rad; q = 3e-3 lands offset by ⅓ bucket → **14.3 rad** (single bucket, ε = 1e-6). A one-seed gate can pass by grid alignment.
- **Cost translation.** Holding even 1e-3 rad at (8.0, 0.8) needs q ≪ 3e-4, i.e. a recompile per kick at ε = 1e-4. At 32 kicks/orbit (H0190) × 38 crossings per compile (r1 anchor) ≈ **1216 crossing-evals/orbit vs probe 2's 350–700 fixed steps** — parity or worse, on exactly the orbits navigation must serve (principle 30).
- **Premise 5 (view gather) survives in flat space:** 40,000 gathers under a 0→0.9c burn with jinking: 0 wrong roots, max 6 Newton iterations, 1 non-single crossing (scan-grid scale). f(τ) = t − τ − |x_o − x_e(τ)| is strictly decreasing (df/dτ = −(1 − n̂·v_e) < 0), so one crossing per tube is structural, acceleration included. Untested: lensing multiplicity (r6 was never frozen) — and the gather's *cost* is the live issue (83% of a light frame, H0210).

## Predictions

`predictions.md` was written before the run. Controls (P1) held exactly. P4 (systematic drift crosses 1% of F early) held (0.32–3.8 rad). P5's cost-parity consequence held at p = 20 (q ≈ 3e-4 needed, not the predicted 3e-3; recompile every ~3 kicks at ε = 1e-4 → ≈ 380–500 evals/orbit ≈ parity). **P2 was wrong in its variable:** curvature does not grow with e at fixed p; it grows with proximity to the separatrix and along the drift (2500×). P3's ε = 1e-6 numbers were right for the wrong reason. Held-out cases: (8.0, 0.8) behaved "like (8.5, 0.9) or worse" ✓ (3–12× worse than my point predictions); systematic ε = 1e-5 gave 0.32 rad against my 8e-5 (missed by 4000×: the curvature *along* the systematic drift dominates, not walk statistics — the same lesson as P2).

## Ranked attacks (the lens deliverable)

1. **Kick absorption by cycle derivatives (premises 3+6) — lands, numbers above.** Rung that should have caught it: **none exists.** r2 judges carry widths, r4 judged resonance phasors, r9 judged Hill-regime kick values, H0190 counted kicks. Propose **r-kick-absorb**: kick train at declared ε on orbits at varying (p − p_sep); positive control recompile-per-kick (must match truth), negative ignore-kicks (must fail); criteria: max phase drift ≤ 1e-3 rad and crossing-evals/orbit ≤ 512, **with the seed swept across bucket phase** (see 2).
2. **Bucket-phase luck — measurement-gate flaw, found while running 1.** Error depends on where the seed lands inside its quantization bucket (3e-7 vs 14.3 rad at the same orbit and kicks). Any single-seed criterion (r1-style) can pass by alignment. Same class as the r8 v3 truth artifact and B12's oracle domain: gates must sample the quantization phase.
3. **View gather (premise 5) — survives in flat space** (measured + monotonicity proof). None does lensing multiplicity; r6 was never frozen. Cost, not correctness, is its live risk.
4. **Binet cells (premise 2) — already half-superseded:** law.md replaced the in-band linearised map (first-order slope error at turning points) with exact Darwin-phase compiles at ~1e-6 per cycle; representation.md §1 still carries the stale "Minsky map" text as "the primary in-cell solution". r1's envelope (e ≤ 0.7, b ≥ 10) never tested the Darwin compile at high e / near-critical light; my curvature results say the interesting difficulty is the same separatrix regime. Doc drift, not a new kill.
5. **Two-body doll (premise 1) — survives:** 1PN EOB with ν only in the energy map is a theorem; r3 v3 confirmed (1024/1024, 632/632, assists 64/64); the handoff kill was the criterion's noise floor (H0206).
6. **Dense ≡ sparse bits (premise 4) — survives where measured:** H0209/H0210's battle frame, bit-identical. Open risk is ordering across dolls (root-clock event keys), already on the risk list.

## What would make it wrong

My float model applies exactly if the live memo carries a within-bucket linear correction (law.md's quantized (E, L) key with stored ∂/∂E, ∂/∂L is that mechanism). If instead every key change forces a full recompile and no linear carry exists, the accuracy rows vanish — but then the 5 October plane measurement (recompile on ~99% of kicks; distinct-kick memo hits 0%) says the **cost** premise fails instead: one of the two rows of §6 breaks for hot orbits either way. If real tidal kick trains are ≪ 1e-4 relative (only H_live on the plane can tell), the cold-regime numbers (≤ 1e-6 rad) apply and the kill shrinks to within ≈ 0.5 of the separatrix. Unmodelled: mid-orbit (partial-arc) kick bookkeeping adds first-order phase terms (r4's resonant case already kills averaging there); Δt/Δτ derivatives inherit the same curvature a fortiori; integer quantization (r2's domain) is invisible to float.

## Cost of adopting, and fit with PRINCIPLES

Adoption is a policy, not a component: make distance-to-separatrix (e.g. (p − 6 − 2e)/p, a dimensionless number — principle 4, "regimes are chosen by dimensionless numbers") a trigger that routes hot orbits to the existing dense order and keeps the memo for the cold bulk, plus freeze r-kick-absorb. The finding enforces principle 13 ("basically we don't want errors that can compound that's the goal"): the multiply-add's error is a compounding bias, not the design's promised "at most one floor unit per event, carried forward so that it never compounds" (§2's error model). Principle 9: this kills the configuration (the absorption sentence as written), not the method — both escape hatches (recompile, dense order) already exist in the design.

## The lens

A red-team overweights exotic regimes, and mine is no exception: the median belt body (p ≫ p_sep, tidal kicks ~1e-6) is *safe* by my own numbers (≤ 1e-6 rad over 2000 kicks) — the premise mostly survives, and the kill is localised to the separatrix skin the player actively visits. I did not measure the light/clock side of the cycle derivatives, could not test integer quantization in float, and treated kicks as exact element jumps (the law's own idealization) rather than derived tides; a builder integrating real tidal kicks on the plane could find the effective ε smaller — or, near conjunction chains, larger — than my sweep.
