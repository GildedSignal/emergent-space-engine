# Dossier — 20261019-0435-fermi-0659

## Claim
The 10⁹ ledger's open dial "what share of fired kicks promote" is measured on shipped code: **the share is 1.0** — every resolved kick item fires a velocity change (170,629 of 170,897 counted items across three independent flights; 59,425/59,425 belt clock-kicks across two cadence waves, 9,710/9,710 at the held-out K; |dvq| ≥ 16 quanta in every fired item; the sub-quantum sigma-delta carry fires 266 times in 170,897 = 0.16%, all split-path, one arm, and **never** on the belt's clock path) — so the ledger's pessimistic residency arm (τ = 43.6 game-s at 8 GB / dwell ≤ ~33 game-s at 6 GB) is the measured one, and no compact store sleeps through the doll's cadence.

## Bottleneck
budget-1e9 open direction 2 ("price the promotion fraction… every plan to 10⁹ gates on it") and the board's "smallest promotion between a compact body and a live one". The dial's two arms differed by ~10⁴ (τ = 43.6 game-s if every kick promotes vs orbit-scale if the belt sleeps); the measurement collapses them to one: the promotion rate equals the kick-item rate λ = 3.6–4.3×10⁻⁵/body/game-s (a9d7's rate re-derived as the cadence: one item per ~27.6k gs per belt body, confirmed: 59,425 items / 29,700 belt bodies = 2.00 per 46.7k gs).

## Evidence (all from the patched-but-behaviour-identical shipped `nladder`; probe = env-gated atomic counters inside `step::kick`/`step::kick_clock`, `ES_KICKCENSUS`; OFF runs bit-identical stats)
Machine: GitHub Actions Linux, 8 vCPU, load 0.4–0.8 during runs, single-threaded, each process < 300 MB.

| arm | game-s | path | items | fired | share | Σ|dvq|max | mean |dvq| |
|---|---|---|---|---|---|---|---|
| A1 K=3×10⁴ coast rtf 280 (wave 1) | 14,280 | clock (belt) | 29,710 | 29,710 | **1.0000** | 4.32e15 | 1.46e11 q |
| A1 |  | split (locals/planets) | 23,104 | 23,102 | 0.9999 | 2.19e16 | 9.5e11 q |
| A3 K=3×10⁴ rtf 1050 (waves 1+2) | 46,713 | clock | 59,425 | 59,425 | **1.0000** | 8.66e15 | 1.46e11 q |
| A3 |  | split | 74,987 | 74,721 | 0.9965 | 9.66e16 | 1.29e12 q |
| A2 K=10⁴ coast rtf 280 (wave 1) | 14,280 | clock | 9,710 | 9,710 | **1.0000** | 1.42e15 | 1.46e11 q |
| A6 K=3×10⁴ 20 s rtf 100 (pre-wave) | 1,899 | clock | 0 | — | (belt silent) | — | — |
| A6 |  | split | 3,671 | 3,671 | 1.0000 | 8.25e14 | 2.25e11 q |

Independent flights total 170,897 counted items (A3 + A2 + A6; A1 is a deterministic prefix of A3 and is not double-counted); 170,629 fired.

Key decompositions:
- **Wave 2 = wave 1** (steady cadence, not a birth transient): A3−A1 clock = 29,715 items, all fired, Σ|dvq| = 4.34e15 vs wave 1's 4.32e15 (0.5% apart). The birth-Δs reading of wave 1 is refuted; every 27.6k-gs step re-delivers the same distribution.
- **Every fired item ≥ 16 quanta**: m==1 = 0 in every arm; m≥16 = fired items everywhere; the shipped branch `if dvq == [0,0] { return }` ("a sub-quantum kick fires nothing") fires 266 times in 170,897 items (0.16%, all in A3's split arm) and **never on the belt's clock path** (0 in 69,135 belt items across A3+A2): on the plane it is dead code in practice.
- **K-flat**: p = 1.0000 at 10⁴ and 3×10⁴; mean |dvq| per belt kick 1.46e11 quanta at both. (No belt–belt channel exists in the plane, so K-flatness is expected and confirms nothing hidden scales with N.)
- **Control (P5)**: census OFF vs ON, same flight (K=3×10⁴, 20 s, rtf 100): kicks 3624 = 3624, events 11115 = 11115, opens 37, boundaries 3499, game 1898.5 both. Counters only.
- λ cross-check: belt clock items / belt bodies / game-s = 59,425/29,700/46,713 = 4.28e-5 ≈ a9d7's 3.55–3.64e-5 (window edge cuts wave 3); the ledger's λ is the item rate, and now also the promotion rate.
- F1 through wave 1 at 3×10⁴ rtf 280: 0 frames over 12 ms, p99 11.94 ms, lag 0 — the census adds no frame cost.

Commands (each ≤ 60 s; `cargo build --release -p emergent-universe --example nladder` first):
```
ES_KICKCENSUS=1 LADDER_CAP_S=54 <bin> 30000 coast 52 280   # A1 wave 1
ES_KICKCENSUS=1 LADDER_CAP_S=54 <bin> 30000 coast 46 1050  # A3 waves 1+2
ES_KICKCENSUS=1 LADDER_CAP_S=54 <bin> 10000 coast 52 280   # A2 held-out K
LADDER_CAP_S=54 <bin> 30000 coast 20 100                   # A5 OFF control
ES_KICKCENSUS=1 LADDER_CAP_S=54 <bin> 30000 coast 20 100   # A6 ON control
```
`<bin>` = `$CARGO_TARGET_DIR/release/examples/nladder` after applying `work/patch.diff` (census counters in step.rs; the census print and `LADDER_CAP_S` in the example; the macOS-only `proc_pid_rusage` replaced by a /proc reader — the shipped example does not link on Linux, dcf1's same disclosed replacement).

## Predictions (predictions.md, written before the flights)
- P1 **failed as written**: predicted clock fired-share ∈ [0.05, 0.8]; measured 1.0000. The Fermi estimate missed the kick's physical weight: one doll step is 27.6k gs of tide, and the sigma-delta carry has no margin to absorb it (fired kicks deliver ~1.5×10¹¹ quanta, never 1–2). This failure is the result: the "kicks sleep" hope is dead on shipped code.
- P2 held (K-flat), P3 failed (predicted 1–2 quanta per fire; measured ~1.5e11), P4 held (wave 2 = wave 1), P5 held (OFF = ON).
- The kill criterion pre-registered for the design ("if p > 0.5 the residency dial improves < 2× and the compact store's value must come from absorbing quantized kicks, a law change") **fired**.

## What would make it wrong
The census counts `kick`/`kick_clock` calls; fleet-origin kicks (lattice battles) ride a different path (`fleet.rs`, its own 2⁻¹⁶ carry) and are excluded — a belt wired through fleets could differ. The promotion share is inferred from "fired ⇒ rebind ⇒ a static compact certificate cannot absorb it": a certificate that *absorbs* quantized kicks (a secular generator, step 5 of the law's plan) would cut the share below 1.0 by design — that is exactly the named law change, not a measurement error. Different dolls (a stirred belt with belt–belt encounters, not wired in the plane) add promotions on top; p = 1.0 is the floor of the shipped cadence, not the ceiling of the game.

## Cost of adopting / fit with PRINCIPLES
Nothing to adopt in code: one number, `p = 1.0`, and one dead branch documented. It closes the ledger's open direction 2 at its pessimistic arm and re-points the work at the law (the cadence's kick must be absorbable by the compact row — "the simulation decides, not us", #22; "a fix signals the wrong representation", #19: a compact store that cannot sleep through its own cadence is the wrong certificate, not a tuning problem). Numbers are Linux/x86 orders of magnitude; the shares and counts are deterministic (bit-identical stats across ON/OFF).

## The lens (Fermi)
The estimate-before-build discipline is what the run delivered: P1's wrong band, pre-registered, is the finding (the per-step tide dwarfs the velocity quantum by ~10¹¹×). What the lens may have missed: I did not measure the belt-only |v| (the Σ|v| census is population-mixed — the player's items ride the clock path), so the *relative* kick size per belt body is bounded (≥16 quanta) but not pinned; and the register `p_t` moves every item too (`ext.add_pt` runs before the fired check), so even a zero-fire design would still touch body state — the compact row must carry or re-derive the register either way.
