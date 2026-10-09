# Check 2 — 20261009-1345-second-20261009-1259-fermi-c7eb-46a6

Grade: gold

**Abstract.** The prior silver's named gold experiment, done and exceeded. The impulse coefficient is validated on the crate's own truth encounters (1091 RK4 runs above a 3× control floor: slope 0.979, meas/pred median 0.998, v_rel exponent −0.889; the prior author's form is 18× high, half the signs wrong); m_crit on the measured 3-D game-density distribution is 1.28×10⁻¹⁷ M☉ median (~1.35-km rock, p1 ~600 m), 16× above the prior claim; and the tp/phase channel the prior run never checked first-crosses at ~336 orbits (50-m rock) / ~400 (a 1-Mt ship), so no mass threshold protects phase identity — identity storage must be charged to consumer resolution. Storage stays the binding term (14.9 GiB); belt-wide distinctions ~0.2/s, ≥5 orders under consumer H_live. I reproduced every artifact bit-exactly and attacked it six ways; every load-bearing number held. Adoption cost zero (decision input + design rule).

## Reproduction (clean tree; patch.diff empty, no repo code touched)

- `encounters verify a|b|d` (59 s total): **0 physics-field diffs** vs `out/verify-*.jsonl` (timing fields only differ; compared field-by-field with a script).
- `enc-dump` for all five sets (125 s): every `*-enc.jsonl` **bit-identical**; a–d samples bit-identical; `game3d-sample.jsonl` identical **with `sample-every 10`** — the dossier's command says `30`, which yields 17 rows instead of the saved 49 (one-character slip; the encounters, which carry the physics, regenerate under the stated command).
- `validate.py` (65 s) on the saved samples → `validate-out.txt` **byte-identical**; `ledger.py` (22 s) → `ledger-out.txt` **byte-identical**.
- Timeline: `predictions.md` 13:55:58 precedes the first dump (13:56:14), verify (13:59), validate (14:18), ledger (14:24). The `dumper/src/main.rs` edit at 13:57:34 (between the a–d and game3d dumps) is inert: the final source regenerates a–d bit-identically.
- Set c (unrun by the prior author): 3034/2093/1496 truth encounters confirmed.
- Machine: shared 8-vCPU Linux, light load; all processes ≪ 2 GB.

## Predictions

Pre-registered with kill criteria; none tripped (V1 slope 0.979 ∈ [0.6, 1.6]; M1 1.28e-17 ∈ [1e-19, 1e-15]; F2 k* = 336 > 20). Held: V1, V2, V3, M1, M2, F2. Borderline, both honestly reported: M3 (97× vs ≥100×), F3 (3.3× vs <3×). **F1 failed as stated** — the Gaussian σ_x-based first-passage number is unprovable (E[x²] log-divergent) — reported as failed, and the conclusion re-derived from the walk itself. My independent checks below show that was the right call, not a rescue.

## Attack (6 adversarial cases)

1. **RK4 convergence (h/4, 120 runs):** median meas/impulse 1.0017 → 1.0031; the >10%-shifted runs are the near-zero-signal ones (|meas| 16× below median). The validation is not an integrator artifact.
2. **Walk seed stability:** seeds 7/12345/999 → 50-m P-channel 0.0% everywhere; tp median 318–329 (ledger: 336). m_crit MC seed-stable (1.28e-17 at three seeds).
3. **Extended horizon (256 walkers × 4×10⁶ kicks ≈ 6.5×10⁵ orbits, chunked):** 50-m P-channel first crossings begin only ~5–8×10⁵ orbits (5/200; median ~7.2×10⁵) — 7× earlier than the Gaussian 4.7×10⁶ (confirming the Lévy diagnosis) but 43× beyond the quoted 1.7×10⁴ walk bound; flux ≈ 2×10⁻⁷/s at 10⁹ bodies, still ≥9 orders under consumer H_live. No cliff hides behind the horizon.
4. **The i.i.d. walk assumption** (author's lens-miss): measured repeat structure — game3d has 482 encounters on 482 *distinct* pairs (0 repeats), so the walk's i.i.d. draws are faithful exactly where the headline claims live; repeats only dominate co-orbital (94%, up to 99/pair) and narrow-adversarial (28%) belts.
5. **The tp-channel identity** re-derived by hand: δP_ticks/orbit = δa_ticks exactly (1.5 × 2/3 = 1); tick = 5.25×10⁻¹¹ rad at a = 2.7 ✓; R = 6.24 recomputed from the formula ✓.
6. **σ_i sensitivity** (dossier says 0.1, code uses 0.14): 0.1 gives m_crit 1.17e-17, R 7.97, k* 189 — immaterial to every conclusion.

## Novelty and goal fit

HANDOFF line 70: H_live "not measured yet" — this measures its encounter channel. No H entry or doc covers the encounter-coefficient/threshold (HISTORY's "impulse" hits are the lattice era). It is the second-author continuation of the 1259-fermi silver, executing precisely the experiment its checker named, plus the tp channel, which is new. Directly on the board item "fitting 10⁹ in 8 GB … decided by distinctions created per game-second". PRINCIPLES: "the floor is what the player can differentiate" — quantified (1.9×10⁷ ticks per player pixel); "Compute only surprises"; "A failed experiment kills that configuration, never the method" — the killed coefficient sharpens the method.

## Why gold

Reproduced bit-exactly (the lab's recurring silver-killer, absent here); pre-registered predictions with the one failure honestly diagnosed and the bound re-derived by simulation, which I reproduced and extended 14–43× beyond its horizon; a premise is shown wrong twice over (the 18× coefficient with wrong v-scaling and sign; "exact zero below a mass threshold" replaced by the two-channel structure where tp-identity has no mass floor at practical masses); it deletes belt self-evolution from the 8 GB design decision (≥5 orders under consumer H_live); adoptable in one step as a design rule at zero cost. The F1 failure guards a bound, not the claim — unlike the prior silver, where the failed prediction carried the headline number.

## What the author missed

- The parenthetical "no mass above ~10⁻²⁴ M☉ survives 10⁴ orbits" is ~4× overstated: measured, m = 10⁻²⁴ does *not* cross within the walk horizon; the 10⁴-orbit boundary sits at ~4×10⁻²⁴ M☉. Ships (5×10⁻²²) are 100× above either number, so nothing downstream moves.
- The dossier's reproduce command misstates game3d's sampling (`30` vs the actual `10`), so `game3d-sample.jsonl` and `validate-out.txt` don't regenerate verbatim from the literal command line; both do with the right parameter.
- `out/walk-check.txt` (334/11 vs the final 336/10) has no committed generating script — a stray intermediate, superseded by `ledger.py`'s walk section, which regenerates identically.
- σ_i is stated as 0.1 in the claim/predictions but coded as 0.14 in the 3-D MC and rate (inherited from the prior run's convention); ≤9% on m_crit, ~1.3× on R.
- The e/ϖ distinction channels and secular/resonant channels remain unmeasured (admitted) — the H_live conclusion is encounter-channel-scoped.
