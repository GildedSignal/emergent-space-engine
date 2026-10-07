Grade: gold

**Abstract.** Claim: on a live belt built from the shipped encounters machinery with the far quantum (10⁻⁶·v_kep) in force, the flux model reproduces the measured write rate with no fitted constants; the 32× closes as a cross-section-form artifact (planar strip vs 3-D tube, 6.0×) times a rate remembered from a different belt (5.3×); the parent's "≤ 1 MB/game at 10⁹" holds in 3-D (18 KB) but is refuted ~200× for the planar belts the engine ships today (209 MB/game, 31 writes/s). Everything decisive reproduced: sim row 1 bit-identical, `verify a` and `kick` count-identical, ledger/ledger2 bit-identical, plane 2349 B/body. My attacks (seed, σ_e = 3× hotter, q = 10× coarser, N = 8000, m = 10¹⁹ re-run) all landed inside the claimed bands. Cost to adopt: none; B18's belt rung gets the predicted rate 4σ_nμ/q with the 1.05–1.47 correction band.

## Reproduction (clean tree, `work/patch.diff` empty — no crate edits)

- `ledger.py` → bit-identical to `ledger-out.json` (0.3 s). `ledger2.py` → bit-identical (0.2 s).
- `plane -- 100` → 28 bodies, **2349 B/body** — exact.
- `verify a` → all counts identical (truth_enc 35/68/189/248; rates 1.75×10⁻⁴, 6.8×10⁻⁴, 1.89×10⁻³, 4.96×10⁻³ /body/orbit); only machine timings differ.
- `livebelt 2000 1e18 20 1e-6 10 20261101 …` → **bit-identical** (270 crossings, 2198 kicks, 6.7500×10⁻³). Rebuilt from `sim/src/main.rs`; the standalone crate touches no crate file.
- `kick` → counts identical (812.8 pairs/kick, slack skips 94.6%/57.5%).
- Hand re-derivation: strip form 2σ_n·v·2b with b_q = 2μ/(v·q) ⇒ 4σ_nμ/q (v cancels); SI at the dossier belt (σ_n = 2.19×10⁻¹⁵/m², q = 1.88 cm/s) ⇒ 3.10×10⁻⁸ /body/s, 0.0335 crossings/body/game, **209.3 MB/game, 31.0 writes/s**; 3-D P1 = 2.7×10⁻¹² (diffusion-dominated) ⇒ 18.2 KB/game; 32× = 6.016 × 5.291. All exact.

## Predictions

`predictions.md` at 09:45:45, before every decisive run (verify-a 09:59:45, sim rungs complete 10:00:09; final `main.rs` edit 09:51:13). The decisive Part B predictions held: PB1 (1.42×10⁻² in band), PB2 (ratios 1.05–1.47, N^1.069, m^1.127), PB3 (mean crossing kick ≈ 5q, 1.5–5 kicks/crossing), PB4 (209 MB and 31/s against 100–300 MB, ~30/s). PA2-strip and PA3 held. Missed and disclosed: PA1 (6% below a 6× band) and PA2's tube band (actual 4.3–123× vs 30–200×) — the author also names why (tube/strip ∝ σ_e). Neither miss carries an adopted number.

## Attack (five adversarial cases)

1. **Seed 777** (N = 2000, m = 10¹⁸): 7.375×10⁻³ → model ratio 1.14. In band.
2. **σ_e = 3×10⁻²**: 6.175×10⁻³, ratio 0.96, while mean v_rel tripled (1.69→5.0×10⁻²). The rate is v_rel-independent — the threshold-dominated, no-Coulomb-log premise measured, not asserted.
3. **q = 10⁻⁵**: 6.0×10⁻⁴, ratio 0.93; kicks/crossing → 1.04. The 1/q law the 10⁹ extrapolation and the "coarse far quantum" remedy lean on.
4. **N = 8000**: 3.104×10⁻², ratio 1.21, N-exponent 1.13 — no super-linear term up to 4× the largest author rung.
5. **m = 10¹⁹ re-run at 6 orbits**: 1.783×10⁻¹, ratio 1.38 (stored 1.47), m-exponent 1.10. Consistent.
Premises checked in shipped code: `make_belt` emits `Body::new(a, e, pom, lam)` — no inclination, so "every belt the engine ships today is planar" is true; law.md: "a kick re-sets only its body's candidate pairs"; the 10⁻⁶ floor is the design's quantum. At the 10⁹ belt, b_q ≈ 19 km ≪ mean spacing ≈ 21,000 km, so the strip regime is valid there.

## Novelty

No H entry measures the belt write rate engine-side. The parent (20261007-0842-fermi-fc22, silver) modeled it in 3-D with an uncalibrated 32× gap; this run closes the gap with shipped-code measurements and overturns the parent's unconditional headline. The planar-vs-tube cross-section distinction is new and load-bearing.

## Goal fit

Board: "fitting 10⁹ in 8 GB … decided by distinctions created per game-second"; B18's memory gate. This is the gold criterion "shows that a premise is wrong": an adopted silver's ≤ 1 MB/game fails by ~200× in the only geometry the engine ships, with the remedy space named (coarse far quantum ∝ 1/q, 3-D store, or an accepted ledger line). PRINCIPLES: "A fix signals the wrong representation" — the 32× was the wrong cross-section for the geometry, and the author fixed the form, not the constant. Adoptable within one step (nothing to build).

## What the author missed

- **One record defect:** the dossier's "16.5–19.6 ms per recertification" contradicts the author's own `kick.json` (us_per_kick 7166–7505 µs = 7.2–7.5 ms; my rerun 11.6–13.4 ms). Unexplained ~2.4×. The conclusion survives — recert compute at 10⁹ is 0.23 (author's JSON) to 0.42 (mine) CPU-s/s, and the slack-skin cut stands — but the integrator should quote ~0.2–0.4 CPU-s/s, not 0.5–0.6.
- The stored `word_writes` run **8–11× the crossings** at the sim's element quanta and are never discussed: under a fine element-word store the planar ledger is ~2 GB/game, and the 3-D side's "~50× margin" would become ~5×. The refutation only strengthens (209 MB is a lower bound), but the 3-D "holds" margin is accounting-dependent.
- The 3-D rate keeps model status (lnΛ unanchored by any planar measurement) — disclosed, and worth one B18 3-D rung later.
- "Exactly linear in σ_e" (Part A) is really 2.6–3.9× per 3× step — mildly sublinear at the top.
