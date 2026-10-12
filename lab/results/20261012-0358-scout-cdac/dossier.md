# Dossier — 20261012-0358-scout-cdac (scout lens)

## Claim (one sentence)

Live distinguishing memory (H_live) follows the **surprise rate, not the light cone's volume**: at star-system scale the cone saturates within ~12 game-seconds (rtf 100), belt self-encounters cost ~0.4–18 MB per play-hour at 10⁹ bodies and player-visible floors (≈1 byte per surviving scar at the floor, ~4,000× under today's 88 B/body), a periodic **repack/rebase** restores the generator floor at unchanged entropy, and the surviving fraction obeys s(ε) ∝ ε^−0.8 — so the 10⁹-in-8-GB risk lives in contacts/battles and the player's own news, not in belt dynamics.

## Bottleneck

Board: "fitting 10⁹ in 8 GB … decided by distinctions created per game-second"; HANDOFF risks: "the light cone keeps growing" and "H_live: not measured yet". Expected gain: sets the denominator for B18/shipmem and the b-h-live dashboard (both queued), and kills or keeps the light-cone memory risk. One named number replaces "not measured yet".

## Evidence (reproduce: `python3 lab/results/20261012-0358-scout-cdac/work/hlive_scout.py`, ~50 s, <0.5 GB; machine state load1≈1.1/8 vCPU, shared)

Event-driven belt toy (N up to 2×10⁵, Γ=1.1 encounters/body/orbit = r8 belt-0's measured rate, impulse kicks Δv=2Gm/(b·v_rel), b uniform [synodic sweep], quantum ε on relative (a,e); distinguished = current cell ≠ generator cell). All in `work/metrics.json`.

- **Cone (S4):** cumulative arrived distinctions grow with exponent **2.57** while the cone sweeps an active region, then RAM inflow = **1.048×** total inflow after T_x = 4,990 game-seconds for R=1000 AU (1.4 play-hours at rtf 100). Belt scale (2.4 AU): T_x ≈ **12 game-seconds**. H_vol ("the light cone keeps growing" as a memory law) is falsified at system scale; it binds only at galaxy scale (T_x ~ centuries of play at rtf 100).
- **Rate (S1, S5):** D(t) inflow exponent **0.88–0.94** (sub-linear: sub-quantum kicks accumulate before escaping — PRINCIPLES 6's "influences below one quantum accumulate", measured). D/events constant across N=5×10⁴–2×10⁵ (0.0071–0.0072).
- **Floor accounting (S1):** 664k encounters, 4,828 scarred bodies: 88 B/body naive 17.6 MB; 16 B/tube 77 KB; id+delta entropy **5.7 KB**; shared references 4.5 KB → **≈1.2 bytes per live scar**.
- **Quantum lever (S2):** survival s(ε): m=10⁻¹⁰ M_sun → 5×10⁻⁴ (ε=10⁻²) … 2.1×10⁻² (ε=10⁻⁴), **α≈0.8**; m=10⁻⁶ M_sun → saturated (96% scarred) at every ε ≥ 10⁻⁶: planetary-mass scatterers leave the floor no lever.
- **Repack (S1/S3b):** joint cell entropy of the whole belt **unchanged** by scarring at belt masses (14.384 → 14.384 bits/body): a rebase restores generator-grade compressibility; at m=10⁻⁴ it rises only to 15.5.
- **10⁹ extrapolation (S7):** 1,068 encounters/game-second (Γ=1.1, 2.2 AU, rtf 100) → **0.44 MB/play-hour** (m=10⁻¹⁰, ε=10⁻³, 16 B upper bound), 10.1 MB/h (m=10⁻⁸), ≤17.8 MB/h even at saturation — against 4 GiB live budget.
- **Controls:** Γ=0 → exactly 0 live bits (positive, passes); 88 B/body baseline and H_vol are the negatives (both lose by 10²–10⁴×).

## Predictions (predictions.md, written before the decisive run)

- P1 held on N-invariance; **failed its exponent band** (measured 0.88–0.94 vs 1.00±0.06): the miss IS the sub-quantum accumulation channel — reported as a finding, not tuned away.
- P2 held: quadratic-phase then flat; H_vol fails after T_x.
- P3 held: α=0.8 ∈ [0.5, 1.5].
- P4 held: shared-reference fraction 13% ≪ 50% early — the lever is the quantum, not reference sharing.
- P5 **failed**: no stirring runaway below planetary mass (Jupiter-class = wholesale scarification, 96%). My Γ(e) coupling is crude and fragmentation is unmodeled — the negative is honest but weak.

## What would make it wrong

The kick/conjunction model is rate-structure, not trajectory truth: real eccentric conjunctors, resonant phase locking (concentrated kicks) and three-body chains could fatten the escape tail; Γ=1.1/orbit is r8's dense belt-0 (MB/hour scales with it); dense-order contacts (battles) and the player's news-gravity channel are absent and are the plausible true dominators; rebase cost when structure (bijectivity, not histogram entropy) breaks under planetary scattering is unmeasured — the toy cannot see it. Held-out check for the next run: s(ε) and MB/hour against the engine's real encounter+kick path (b-h-live's dashboard is the ready instrument).

## Cost of adoption, fit with PRINCIPLES

Adoption is a definition + an accounting model + expected magnitudes for b-h-live/B18/shipmem (no engine change). Mechanism: **CRAM-style reference+delta** (verified: ~40–50% over BAM, bioinformatics-core-shared-training), **git-pack repack with bounded delta depth** (verified: git-pack-objects(1), `--depth`) as the reabsorption/rebase in idle time — already half-adopted in representation.md §3; this run supplies its rate and when to fire it. Fits PRINCIPLES 6 ("store the generator, not the generated"; sub-quantum accumulation now *measured*, exponent 0.9), 3 (memory follows surprises), 5 (light cones partition compute — and stop growing at system scale), 24 (the floor is information: 4–10³× under naive storage). UNVERIFIED at source: CRAM's exact 40–50% figure beyond the training-site page; all cross-field numbers are orders of magnitude only.

## The lens

Scout optimizes prior-art fit; the literature's ratios (CRAM, packfiles) come from data unlike ours and transfer as mechanism, not magnitude. This lens underweights adversarial gameplay: a player or AI farming encounters on purpose can pump Γ far above belt-0; the law survives (linear in Γ) but the MB/hour line does not, and the toy has no answer for deliberate contact storms.
