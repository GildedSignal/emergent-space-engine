# Dossier — 20261008-1058-fermi-8e6f

**Claim.** At 10⁹ bodies on the 8 GB M1, H_live (the board's unmeasured risk) is not the binder: for ship- and rock-mass bodies, encounter-driven element changes are sub-quantum at any cell-scaled element quantum (8 GB fill time ≥ 10²⁰ s), and memory binds only in the corner "one dense belt of planet-mass bodies" (~23 h to fill); the binding terms are the ones already on the board — kick cost (175 cores at today's 29 µs, the board's "~190" re-derived to 8%) and, in the dense-belt extreme, encounter work (15 cores at 1 µs/event with element-sort's measured 786 work/encounter) — while candidate pairs and total real encounters grow as N²·⁰⁹ (per-body rate measured ∝ N^1.09 at fixed distribution), so certificates must exploit hierarchy, exactly as designed.

**Bottleneck.** Board focus items "fitting 10⁹ in 8 GB, decided by distinctions per game-second" and the top scaling risk (candidate pairs O(N²)). Expected gain: retires or bounds the memory question for all plausible masses (infinite × on that axis), and converts "O(N²) risk" into a measured exponent with a fluid cap. Deletes: any need to design scar reabsorption for sub-rock masses.

**Evidence.** All anchors repo-measured, cited; two runs of my own.

*Probe A — true encounter rate at fixed distribution* (`probe-a.jsonl`, exact conservative-advancement truth from `crates/encounters`, σ_e = 10⁻², ρ = 10⁻⁴, a ∈ [1, 1.5], 20 orbits, seeds 20261008+i):

| N | candidate pairs | true encounters | per body / orbit |
|---|---|---|---|
| 10³ | 60,720 | 32 | 1.60×10⁻³ |
| 2×10³ | 244,920 | 169 | 4.23×10⁻³ |
| 4×10³ | 970,769 | 584 | 7.30×10⁻³ |

Fit: γ(N) = 8.9×10⁻⁷·N^1.09 per orbit; candidate pairs exponent 2.00. Extrapolated to 10⁹: 6.4×10³/orbit, capped by the 2D fluid sweep limit at 3.2×10³/orbit (mean spacing 8×10⁶ m < ρ = 1.5×10⁷ m there). The dilute-regime exponent is clean (cap is 17× above the N = 4×10³ point).

*Probe B + ledger* (`ledger-out.txt`, `ledger.py`): per-ρ-encounter impulse δv = 2Gm/(b·v_rel), b < ρ, v_rel ~ e·v_K (σ_e = 10⁻², 3 AU belt, T = 1.6×10⁸ s):

| mass | median \|Δa\|/a per encounter | 8 GB fill (dense single belt) | 8 GB fill (hierarchical, 10⁵×10⁴ belts) |
|---|---|---|---|
| ship 10⁶ kg | 4.9×10⁻¹⁸ | ≥ 10²⁰ s at ε = 2⁻³⁰ | never |
| rock 10¹² kg | 4.9×10⁻¹² | 7.3×10⁸ s at ε = 2⁻³⁰ | 10¹⁵ s |
| Ceres 9.4×10²⁰ kg | 4.6×10⁻³ | 8.2×10⁴ s ≈ 23 h | 1.2×10¹¹ s ≈ 4,000 yr |

Sub-quantum accumulation folded in as a crossing rate (ε/δ)² (principle 6). Static store: 0.126 bits/body programs = 15.8 MB at 10⁹; naive 16 B tubes = 16 GB > 8 GB (programs mandatory, as designed). Throughput: all-LEO mix = 6×10⁶ kicks/s × 29 µs = 175 cores (board's "~190" ✓); 114× averaging (H0190 K2) → 1.5 cores; 0.3 µs kicks → 1.8 cores. Dense-belt encounters: 1.95×10⁴/s total; at element-sort's 786 events each = 15.3 cores at 1 µs/event. Bandwidth: ≤ 0.15 GB/s, 400× under.

Reproduce: `cd lab/results/20261008-1058-fermi-8e6f && python3 ledger.py` (0.7 s); `cd probe && CARGO_TARGET_DIR=/tmp/fermi-target cargo build --release && /tmp/fermi-target/release/fermi-probe` (34 s run, < 200 MB).

**Predictions** (`predictions.md`, written before both runs). Held: exponent α = 1.09 ∈ [0.7, 1.3]; the 190-cores re-derivation (175, 8% off); ship/rock h = 0 at cell-scaled quanta, Ceres-class ≈ 40 bits; dense-belt fill ~days (23 h, same OoM); hierarchical ≥ years; LEO needs 60–170× (measured 117–175×). Partially held: the N = 10⁴ anchor — same-(σ_e, ρ) extrapolation gives 1.9×10⁻²/orbit vs r8 belt-0's 2.1×10⁻³ (factor 9), but r8's σ_e and ρ were log-uniform draws (rate ~ ρ²/σ_e), so the comparison is not at equal parameters; within the draw ranges it is consistent. Kill criterion not triggered (α ≥ 0.5, anchor not > 10× off after parameter accounting).

**What would make it wrong.** (1) Masses above ~10¹⁹ kg living dense in one belt (then H_live binds in days — but such a region is an aggregate source by principle 33 and the count-quantum rule, not 10⁹ tracked scars). (2) An element quantum finer than ~10⁻¹² of a for rock-mass bodies (then every encounter is a distinction; that is a certificate choice, and the ledger says it is the wrong one). (3) Distinction sources I did not model: births/deaths of ships (game content, not orbital mechanics), the player (one wildcard, c-bounded, negligible), and recompile churn (a bijection, no growth). (4) The 2D, circular-orbit, impulsive-encounter model; inclined or resonant belts have higher conjunction rates (resonance kills averaging — known). Adoption cost: none as code; it is a bound and a priority call. Fit with PRINCIPLES: "The memory floor is information-theoretic" (measured here where it actually bites); "Compute only surprises"; "influences below one quantum accumulate" (the crossing-rate model); "the cheapest compute is compute not done" (no scar machinery needed for sub-rock masses).

**The lens.** A Fermi run sees masses and quanta as free parameters; the game may not let me choose them. I measured the dilute exponent only to N = 4×10³ (60 s limit) and extrapolated 6 orders with a physical cap as a guard. The 40 bits/scar is an estimate (index + quantized deltas), not a measurement of shipmem's actual codec. And "which term breaks first" is a statement about the regime mix, which is a game-design decision the engine cannot make — the honest output is the table, not a single number.
