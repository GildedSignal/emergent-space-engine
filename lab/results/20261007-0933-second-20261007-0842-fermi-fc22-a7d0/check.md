Grade: gold

**Abstract.** The named experiment is done: on a live belt from the shipped machinery (far quantum 10⁻⁶·v_kep in force), the planar flux model reproduces the measured element-write rate with no fitted constants (ratios 1.05–1.47; N^1.07, m^1.13); the 32× closes as cross-section form plus width (6.0×) times a rate remembered from a different belt (5.3×); the ≤ 1 MB/game claim holds in 3-D (18 KB) but is refuted ~200× for the planar belts the engine ships (209 MB/game, 31 writes/s at 10⁹). All reproduced bit-identically (three sim rungs, verify a, ledger.py, kick, plane 2349 B/body). Adversarial: seed +6%; σ_e×3 −9% (v-independence); m÷10 ÷11.3; N=8000 exponent 1.13, conservative. Cost: none to build; two design consequences plus a falsifiable B18 rung number.

## Reproduction (clean tree, empty patch.diff)

- `ledger.py` → `ledger-out.json` **bit-identical**, and bit-identical to the original silver's committed `ledger-out.json` (script differs only in its output-path line). Arithmetic re-derived by hand: planar 3.1006×10⁻⁸ /body/s → 31.01 writes/s → 209.3 MB/game ✓; P6 gap = 6.016 × 5.291 = 31.8 ✓.
- `verify a` → every physics counter identical (truth_enc 35/68/189/248, matched 100%, sections/checks/queries/evals equal); only timing fields differ under load.
- `livebelt` all three rungs → **every counter bit-identical** (crossings 270/1133/15178, kicks 2198/9202/94422, events, scanned, `mean_vrel` to 5 digits; m=10¹⁹ rerun 424 s vs author's 352 s under my heavier load). Deterministic, same seed.
- `plane -- 100` → 28 bodies, `bytes/body 2349` exact. `kick` → structural counters identical (812.8 pairs/kick, scanned, changed/flipped fractions); only µs timings differ.
- Model code checked: `4σ_nμ/q·2π` with σ_n = N/(2π·ā·w) at the annulus' exact geometry (ā=1.25, w=0.5) — no fitted constants, v_rel genuinely cancels.
- Timestamps: `predictions.md` 09:45:45 → sim crate 09:48–09:51 → `verify-a.json` 09:59:45 → `sim-rungs.json` 10:00:09. Held out before both decisive runs. Tree clean outside `lab/results/`.

## Predictions

Held: PA2-strip (1.41–1.94× at every σ_e), PA3 (linear in σ_e), PB1 (1.416×10⁻² in band), PB2 (ratios 1.05–1.47, flat; m^1.13, N^1.07), PB3 (threshold-dominated: mean crossing kick ≈ 5q, 1.2–5.1 kicks/crossing), PB4 (209 MB/game and 31 writes/s against the predicted 100–300 MB, ~30/s; 3-D ≤ 1 MB ✓). Missed, both disclosed: PA1 (measured 1.89×10⁻³, 6% below the band edge) and PA2's tube band (4.3–123×, not 30–200× — the tube/strip ratio is ∝ σ_e). The misses are on auxiliary bands; every load-bearing number landed.

## Attack (five adversarial cases)

1. **Seed** 987654321 at (N=4000, 10¹⁸ kg): 1.5062×10⁻² vs 1.4162×10⁻² (+6%) — seed-robust.
2. **σ_e = 3×10⁻²** (3× dispersion): 6.175×10⁻³ vs 6.75×10⁻³ (−9%). The strongest physics claim — planar crossing rate is v_rel-independent (no Coulomb log, threshold-dominated) — survives tripling the dispersion.
3. **m = 10¹⁷ kg** (mass ÷10): rate ÷11.3 (m^1.05 downward), kicks/crossing 1.18 — single-kick dominated at the 10⁹ belt's mass scale, which is what licenses the threshold form in the extrapolation.
4. **N = 8000**: 3.1044×10⁻² vs model 2.5742×10⁻² (ratio 1.206); exponent 1.13 over the octave, 1.10 over the full 4× N range. Mildly super-linear — the planar break at 10⁹ is if anything *under*estimated (~5× if the drift persisted), so the refutation direction is robust.
5. **Far-walk truncation**: b_cap = 10·b_q omits kicks with δv < q/10; their random-walk contribution pushes measured up, again conservative for the refutation. The 3-D sheet-diffusivity term zeroed in `ledger.py` is 17× below the tube term — immaterial, though its comment ("beyond-H kicks < b90") states the wrong reason.

## Novelty

No H entry or doc measures element-word writes on a live belt; the handoff's risk list said H_live "not measured yet". The planar/3-D boundary is new and corrects the first checker's own attack #5, which applied the 32× correction to the 3-D form and concluded the ≤ 1 MB claim survives — the wrong geometry for every belt the engine ships. Distinct from components-98bc (births program, 0.126 bits/body) and from r8 v2 (encounter discovery, not write rates).

## Goal fit

Board: "fitting 10⁹ in 8 GB … decided by distinctions created per game-second"; B18 (a requirement from the goal) gets its first engine-side number and a falsifiable rung prediction (4σ_nμ/q with the 1.05–1.47 band). PRINCIPLES: "The memory floor is information" (#24) — the floor's dynamics term is now measured in the regime the engine runs; "Compute only surprises" (#3) — 1.2–5 kicks per crossing, sub-quantum kicks reabsorbed as designed; the 32× was the wrong cross-section for the geometry measured, not a wrong constant (#19's "a fix signals the wrong representation").

## Why gold

Reproduced bit-for-bit everywhere the code is deterministic; the decisive held-out predictions held; it shows a premise of a silver candidate is wrong by ~200× in the geometry the engine actually ships, converts the ledger from calibrated model to measured gate input, and is adoptable in one step (nothing to build; the design fork — coarse far quantum, 3-D store, or an accepted planar ledger line — plus the B18 number).

## What the author missed

- The dossier's "16.5–19.6 ms per recertification" is in no stored artifact: its own `kick.json` stores 7.2–7.5 ms (my clean repro matches the structure; 21–26 ms under load). A loaded-run timing quoted as if from the cited file. Direction unaffected (0.27–0.6 CPU-s/s either way).
- The sim's own `word_writes` counter runs 8–10× the crossing rate (element quanta are the sim's invention, not shipped) — a real element-word store would pay more than the crossings×50-bits line; worth folding into B18's rung when its quanta are fixed. Strengthens, not weakens, the planar refutation.
- The 3-D "holds" leg is anchored in direction only (Part A pins the cross-section's σ_e-dependence, not the ln Λ constant); honest, but it means the ~50× margin is still one 3-D belt measurement away from a gate number.
- Resonant/collective relaxation in nearly planar disks could raise the 10⁹ rate above the two-body estimate; untestable at N=4000–8000, disclosed in the lens section, and it only worsens the planar break.
