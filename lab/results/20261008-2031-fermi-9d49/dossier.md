# Dossier — H_live: distinctions per game-second decide 10⁹ in 8 GB, and they are a census, not a rate

## Claim

H_live per body **saturates** (measured on the shipped store: program member 17.3–29.6 bits, first scar +70.7–76.7 bits, individual 149.7–196.6 bits, re-kicks ≈ 0), so whether 10⁹ bodies fit 8 GB is decided by the **promotion census** — the fraction of bodies ever promoted past a first quantum crossing — not by the event rate (representation.md's ~6×10⁴ kicks/game-second create ≈ 0 bits); at 4 GiB the ceiling is 9.5–12.9% individuals (24% scarred), and at B18b belt geometry the promoters are **contacts** (belt turnover in ~10² yr for 1-km rocks) and **embedded masses** (M ≥ 8×10¹⁷ kg turns the belt over per Myr; v_rel cancels), never mutual gravity between rocks (b_cross < contact radius at every rock size) — so the engine needs contact-driven recycling (fragment programs) and retirement as a designed counterweight, and the dashboard should count promotions/retirements, not kicks.

## Bottleneck

Board item "fitting 10⁹ in 8 GB (crates/shipmem), decided by distinctions created per game-second"; HANDOFF risk "not measured yet". Expected gain: converts the H_live risk into a budget identity with measured constants (orders of magnitude, not 10× compute), deletes the misreading "distinctions per second ≈ event rate", and gives `b-h-live` its exact counters. It also kills one number in representation.md §4 (see below).

## Evidence

Machine: Linux x86 cloud runner (8 vCPU), orders of magnitude only. All commands ≤ 60 s, run from the repo root; every measurement round-trips bit for bit (`roundtrip_mismatches: 0`).

```
cargo build --release -p emergent-shipmem --example measure          # 6.7 s
R=lab/results/20261008-2031-fermi-9d49
cargo run --release -p emergent-shipmem --example measure -- convoy    1e6 200000 128 $R/measure.jsonl
cargo run --release -p emergent-shipmem --example measure -- formation 1e6 200000 128 $R/measure.jsonl
cargo run --release -p emergent-shipmem --example measure -- convoy    1e6 0       128 $R/measure.jsonl
cargo run --release -p emergent-shipmem --example measure -- formation 1e6 0       128 $R/measure.jsonl
cargo run --release -p emergent-shipmem --example measure -- random    1e6 0       128 $R/measure.jsonl
cargo run --release -p emergent-shipmem --example measure -- traders   1e6 0       128 $R/measure.jsonl
python3 $R/fermi_hlive.py                                            # output in $R/fermi_hlive.out
```

Measured (`measure.jsonl`, n ≈ 1.0×10⁶ per run; kicks are ±2¹⁰–2¹⁶-quantum events on (t_p, E, L, ω); kicked members keep their slot, compaction re-groups, oracle-checked):

| form | bits/body | floor |
|---|---|---|
| convoy (perfect launch program) | 17.29 | 13.73 |
| formation (grid + jitter) | 29.60 | 19.92 |
| + one kick per ~20% of members | +14.1 / +15.3 bits per member (70.7 / 76.7 bits per kicked member) | — |
| individual, shared doll key (traders) | 149.73 | 145.51 |
| individual, no structure (random) | 196.62 | 189.51 |

Budget identity: 4 GiB ÷ 10⁹ = 34.4 bits/body. All-convoy 2.01 GiB ✓; all-formation 3.45 GiB (edge); all-individual 17.4–22.9 GiB ✗ (2–3× the entire 8 GB). Ceilings at 4 GiB: f_indiv ≤ 12.9% (trader-like), ≤ 9.5% (random); f_scarred ≤ 24.2%.

Rates (analytic, units checked in `fermi_hlive.py`, belt = B18b geometry 8.4×10⁶ bodies in a 2.2–3.2 AU 2D annulus, q_rel = 10⁻⁶):
- Mutual gravity between rocks **never** promotes: b_cross = 2Gm/(q_v v_rel) = 16 m for 1-km rocks vs 2 km contact radius; ratio ∝ R². All mutual kicks are sub-quantum, sum exactly on the grid (r2).
- Contacts: rate per body = S_n·4R·v_rel → 1-km rocks: one per 72 yr game time (whole belt individual in ~centuries); 1-m rocks: 7.2×10⁴ yr.
- Embedded masses: others promoted at S_n·4GM/q_v (v_rel cancels); turnover in T needs M ≥ N q_v/(4GS_n T): 8×10¹⁴ kg/Gyr, 8×10¹⁷ kg/Myr. One Ceres: 26 promotions/game-day, belt individual in ~870 yr. A 10¹⁵ kg fleet alone: 0.01 promotions/yr (dead; alive only as an aggregate, principle 6).
- Resonance chaos: first-order widths 2.5μ^(2/3) ≈ 0.024a vs spacing 0.027a → 91% axis coverage; f_chaos × N promotions once each, in ~orbits (separatrix) to 6×10³–6×10⁵ yr (weak chaos). A 10⁹-body universe of such belts at f_chaos = 0.3 → 5.2 GiB: over budget without retirement.
- Births: program births ≈ 0 bits/member; individual births are player-rate: dead terms.

## Predictions (`predictions.md`, written before the runs)

Held: convoy 17.29 ∈ [14, 24] (floor 13.73 vs analytic 13.4); random 196.62 ∈ [130, 200]; per-kick 70.7/76.7 ∈ [40, 100] with Δ 14.1/15.3 ∈ [8, 20]; fleet sweeps dead (P7); f_indiv_max 9.5–12.9% < 15% (P9); event-rate ≠ distinction-rate (P10, with the refinement that the ratio is ~1 only for a body's first kick inside a zone).
**Missed (held as missed):** P5 — formation is +12.3 bits over convoy, I predicted ≤ +8 (the jitter columns cost more than guessed). P6 — **wrong, and it matters**: I predicted mutual belt encounters promote < 10⁻⁶/body/Myr (the 3D real-belt picture); in the game's 2D geometry contacts promote every ~72 yr per 1-km rock. The miss flips the dominant promoter from gravity to contacts. P4 (re-kick boundedness) was not run — the CLI has no knob; collisions inside the run imply ~78 bits/distinct member at 1.1 kicks each; boundedness remains an inference from the store's design (kicked members keep slots), not a measurement.

## What would make it wrong

- The 10⁻⁶ relative quantum: promotion rates scale as 1/q_v (embedded masses) and 1/q_e (resonances); if behaviour gates freeze q at 10⁻⁵–10⁻⁴, ceilings relax ×10–100 and the whole census question softens.
- If contact outcomes are exact elastic bounces that stay within the family program (no promotion), the contact term dies and only embedded masses and resonance chaos remain.
- If the store's individual width can come down to the law's 16-byte Tube (128 bits) with key sharing and a behaviour-width t_p (r2 widths not yet frozen), f_indiv ceiling rises to ~16%; representation.md §4's "12–16 bytes for an individual" is **not reachable at today's widths** (measured 18.7–24.6 bytes, = 1.04× the crate's own entropy floor, so B18's ≤2×floor+2 rule holds — the doc's floor is a width claim, not a store defect).
- The B18b belt geometry (8.4×10⁶ in 17 AU²) sets the contact rate; sparser scenes scale linearly.

## Cost of adoption, fit with PRINCIPLES

Adoption cost: `b-h-live` counts promotions (first crossings), retirements, program births instead of kick events; belt scenes declare rock radius and embedded masses as first-class design inputs (they set H_live, not flavour). No code change in this run (analysis + measurement only). Fit: "The memory floor is information" (P24) — measured, the floor of an individual is 145–190 bits at today's widths; "Compute only surprises" (P3) — events that mutate in place are not surprises; "influences below one quantum accumulate" (P6 of the register) — confirmed dead term until crossing; "every body real, never averaged" (P: no Elite style) — held: nothing here averages, promotion is per-body exact state.

## The lens (what Fermi may have missed)

The estimate lens buys orders of magnitude, not constants: the 91% resonance-coverage number is a linear width ratio, not an overlap calculation (Wisdom's e_c ≈ 0.21μ^(1/7) ≈ 0.08 suggests most of a σ_e = 0.1 belt is mildly chaotic — bracketed, not resolved). The contact-recycling gain (fragments emitted as programs) is asserted from the shipmem design, not measured — a rung could measure fragment-family emission cost. Everything is Newtonian-scene framed; GR corrections (retarded moments) do not change promotion census at these densities.
