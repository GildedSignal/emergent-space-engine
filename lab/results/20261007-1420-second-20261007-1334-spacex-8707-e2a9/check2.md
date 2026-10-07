# Check 2 (blind to check 1) — 20261007-1420-second-20261007-1334-spacex-8707-e2a9

Grade: gold

## Abstract (for the integrator)

The silver run's named experiment is done and holds. The port (`hlive2.py --sampler orig`) regenerates the silver's stored `conv_dt10.json` bit for bit; `orig/` is md5-identical to the `claude/lab-20261007-1334-spacex-8707` branch, so the shipped record was not touched. I reran both decisive scenes: **bit-identical** JSONs; null reproduced exactly (4.05e-12 / 1.6e-13). Held-out seed 10 (b17) reproduces every headline: rate 1.0e-3 (q=1e-3) and 9.91e-4 (q=3e-3, 1.22x the original's 8.15e-4, far inside the 5x pure-2:1 bound), exponent 0.612, T* = 5 yr. A 3x-heavier Giant leaves the long-run rate unchanged and only shortens T* to 2 yr; my b16 dt=0.05 probe confirms the plateau (1.49e-3 vs 1.48e-3) and T* = 20 yr. Cost to adopt: one number for B18's reported-at-1e9 line, one refit cadence (5/20 sim-yr), and the 2^17 placement recommendation for Sol's wiring.

## Reproduction

- **Port fidelity.** `python3 hlive2.py --scene belt --sampler orig --N 4000 --years 300 --dt 0.1 --seed 7 --out port_conv_dt10.json` (6 s): deep compare against `orig/conv_dt10.json` differs only in the disclosed new key `frac_crossed_vs_t`; every original key is bit-equal (NaN-aware). Cross-check against the repo: `orig/{hlive.py, aggregate.py, predictions.md, belt_s7.json, null_1000.json, conv_dt10.json}` are md5-identical to `origin/claude/lab-20261007-1334-spacex-8707:lab/results/20261007-1334-spacex-8707/…`, so the author did not doctor the record the relabels are read from. The hlive2.py diff vs orig/hlive.py is exactly the disclosed delta (sampler switch, per-scene Kepler iters, scene-parameterized analysis constants, new output key); the physics loop is unchanged.
- **Decisive reruns.** `--sampler b17 --seed 7` and `--sampler b16 --seed 7` (N 30000, 1000 yr, dt 0.1, keep-sub 6000, ~250 s each): both outputs **bit-identical** to the stored `b17_s7.json` / `b16_s7.json`. `--scene null --sampler b17`: identical numbers to the author's `null_b17.json`.
- **Sampler and scale against the repo.** `xtask/src/behave/belt.rs` `SPEC` = {p_lo 2048≪16, p_bits 27, sigma_milli 70, e_bits 30, e_cap 644245094, w 32, t 44} — exactly the dossier's "Darwin p over [2048,2560) at 2^16, e Rayleigh 0.07 capped 0.6, angles uniform". `crates/universe/src/scenario.rs`: AU = 101,300,000 root, STAR_RADIUS = 471,000 — the author's 1 AU = 99.3e6·1.02 = 1.01286e8 agrees to 0.014%, and 471,000 = R_sun/(GM_sun/c²) checks. Darwin is Q16 doll-relative (`galaxy/scene.rs` passes p·65536 in its own GM=c=M=1 units; `Key::darwin` caps p at 8192), so SPEC alone fixes no physical placement — the "wiring unfrozen, k∈{16,17} bracket it" reading is right, and HANDOFF still lists "the belt wired to B18b" as Sol's queued build. At k=17 the Giant (5.2 AU) is 4020 darwin < 8192, the claimed 2x margin. b16 = [1.325, 1.656] AU overlaps no planet and only ≥5:1 resonances ("quiet" is fair); b17 = [2.650, 3.313] brackets 5:2/7:3/2:1.

## Predictions

`predictions.md` mtime 14:32:42; smokes 14:31 (≤ 200 yr snaps); null 14:34:08; decisive outputs 14:38:56–14:39:09 — written before the decisive runs. 6/7 held as the dossier says; the miss (b16 exponent 0.013 vs [0.4, 0.8]) is in the cheaper direction and honestly reported. The pre-registered kill criterion (rate > 5e-3 **and** T* < 0.5 yr) is nowhere near triggered.

## Attack

1. **Held-out seed 10, b17, full scale:** rate q=1e-3 1.0e-3 (saturated), q=3e-3 9.91e-4, exponent 0.612, T*25 = 5 yr, median first-cross 20 yr, fit-noise 1.000 — every headline holds out of sample.
2. **3x Giant (m_p = 3e-3), b17 seed 7:** long-run rates unchanged (1.0e-3 / 1.0e-3); exponent 0.534; T*25 drops 5→2 yr, frac@2yr 34.6%. The "second giant raises the floor" caveat costs cadence, not the ceiling — the claim's direction survives a perturber 3x the plane's.
3. **Map convergence where the author didn't check it:** the silver's dt runs covered only [2.0, 3.3]; b16's inner edge (1.33 AU, P ≈ 1.5 yr) gets ~15 kicks/orbit at dt = 0.1. My b16 seed 7 at dt = 0.05 (500 yr): plateau RMS 1.49e-3 vs 1.48e-3, exponent −0.039 vs −0.042, T* = 20 both, q=3e-3 final 0.03% vs 0.0%. The b16 saturation is physics, not slab error.
4. **Record relabels:** `orig/belt_s{7,8,9}.json` give median first-cross 10/10/20 (q=1e-3) and 50/50/50 (q=3e-3); the silver's 6.2/21.7 were indeed the aggregate's `T_cross` RMS-reaches-q; raw crossed fractions 1.0/1.0/0.999 (q=1e-5…1e-3) confirm q-insensitivity; the 24.29x |dv| multiple and 6.76 game-yr fill time recompute from `orig/aggregate.json`.

## Novelty

B18b was frozen at H0214 with "no wired belt yet"; HANDOFF queues the wiring with Sol. The silver (branch tip: "Grade: silver") measured an invented uniform belt; nothing in docs/HISTORY.md or the docs measures the frozen sampler's secular scar rate at either placement. This is the designated second-author closing experiment, not a repeat.

## Goal fit

Board focus: "fitting 1e9 in 8 GB … decided by distinctions created per game-second". The run makes the silver's rate sampler-independent (1.22x vs the checker's 5x worst case at the loaded placement, strictly cheaper at the quiet one), fixes the refit cadence T* = 5/20 sim-yr, and hands Sol a placement recommendation. PRINCIPLES #6 "Store the generator, not the generated" — the two-field-plus-clock program still suffices between refits on the plane's own sampler; #21 — the refit is the refinement, T* when it must fire. It resolves the one premise that could still have forced the 8 GB ceiling at session scale, and adoption is one step.

## What the author missed

- The **session-lag median hides a ~40x seed spread**: at 2 yr seed 7 has 3.1% crossed (b17) vs the reported 0.23% median. The load-bearing numbers (peak rate 5e-2, T*) are unaffected, but a worst-case session number should quote the max seed.
- "Nobody crosses q = 3e-3 in 1000 yr" is seed-7-true; seed 8 crosses 0.1% (rate 1e-6/body/yr). Immaterial, but the word overstates.
- The dv-profile minimum bin is the band's **inner edge** (2.65–2.70), not the "band-centre bin" the dossier names (the prediction said 2.70–2.75); the 16.6x multiple itself is correct.
- b16's dt-convergence was never run by the author (the silver's conv runs cover only [2.0, 3.3]); it passes (my probe above), but the author shipped the number untested.
- Post-refit regrowth is assumed ≤ the first-pass early rate; a refit-and-continue run would measure it directly (fit-noise 1.000 and the t^0.637 growth law make it plausible). Not gating adoption.
- The one-planet, 2-D harness inherits the silver's assumptions; the lens section says so. The genuinely open question it names — the encounter side of the e ≤ 0.6 tail — is where the 8 GB question should be re-asked, and that is a new experiment, not a defect of this one.
