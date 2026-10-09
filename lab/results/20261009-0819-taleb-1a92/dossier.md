# Run 20261009-0819-taleb-1a92 — H_live is absorbing, and its rate is set by the worst cell

## Claim

Population programs cannot be the 10⁹-belt's memory: close-encounter scarring is absorbing and
universal (every body scarred, T50 = 55–71 orbits at r8 belt density; 0.9 orbits in a narrow
belt), the per-body rate λ scales linearly with local body count (×3.04 for ×3.33, measured), and
the rate varies 63× between a wide and a narrow belt — so H_live is Extremistan **across cells,
not across time** (Fano ≈ 1.0, inside the Poisson control): size compaction by the mean of the
worst cell, and size nothing by temporal bursts.

## Bottleneck

Board focus item 5 / risk 2: "fitting 10⁹ in 8 GB … decided by distinctions created per
game-second (H_live): not measured yet." This run measures it on shipped code: the exact
encounter truth (`crates/encounters/src/truth.rs`, conservative advancement, every local minimum
of pair distance below ρ) on shipped belts (`belt.rs`), and the memory semantics of
`crates/shipmem` (kicks are absorbing scars; a kicked orbit ship draws ~50 bits of fresh entropy:
11–17-bit deltas on t_p/E/L/ω, `pop.rs::kick`).

## Evidence

All runs ≤ 24 s, 4 threads, `dup_times: 0` (each event a distinct distance minimum); determinism
control: `long-s11` re-run gives the identical stream hash `728984ad277c321b` and counts.

| config (n, σ_e, ρ, span, orbits) | λ /body/orbit | T50 (q=1.0) | S_end q=1.0 / q=0.03 | Fano (1-orbit bins) |
|---|---|---|---|---|
| long-s11/12/13 (300, 1e-2, 1e-3, [1,1.5], 1000) | 0.0059–0.0062 | 55–71 orbits | 1.0 / 0.38 | 0.89–0.99 |
| ultra (100, …, 10000) | 0.0019 | 302 orbits | 1.0 / 0.65 | 1.02 |
| dense (3000, 1e-2, 3e-4, 20) | 0.0176 | — (S=0.50 @20) | — | 0.76 |
| storm = narrow-adversarial (400, 2.5e-2, 3e-3, [1,1.0025], 20) | **0.374** | **0.9 orbits** | 1.0 / 1.0 | 0.43 |
| scale300 → scale1000 (ρ=1e-3, 20 orbits) | 0.0065 → 0.0198 | ×3.04 for ×3.33 bodies | | |

- **Absorption (the premise-killer):** first-event times per body give S(t). At every-event-scars,
  S→1 on every config; the quantum sweep (only events closer than q·ρ count) pushes T50 out
  (long-s11: 57 → 195 → 359 orbits at q = 1 → 0.3 → 0.1; still S=0.38 at q=0.03 over 1000 orbits;
  ultra reaches S=0.65 at q=0.03 over 10⁴ orbits). A program that survives a 1000-orbit persisted
  belt must ignore ~99.7 % of encounter distances — i.e. leave sub-quantum kicks unmodelled
  (B12's bounded-vs-compounding question, now with a number attached).
- **Steady-state memory:** every ship scarred ⇒ per-ship storage ≈ 157 bits/body (the
  components-98bc endpoint) ⇒ 10⁹ bodies = 19.6 GB against the 8 GB budget (which allows 64
  bits/body). Fresh entropy in transit: ~50 bits per kick (shipped `pop.rs::kick`).
- **Across cells (the real tail):** λ = 0.374/orbit in the narrow belt vs 0.0059 wide — 63×. A
  10⁶-body cell at narrow-belt rate generates ≈ 2.3 GB of scar entropy per orbit; no idle-time
  compaction absorbs that. The budget is decided by the worst cell's λ·N, not the mean (Taleb:
  size for the worst cell).
- **Across time (no tail):** Fano 0.43–1.05, max/median bin within the Poisson control's p95
  (Poisson control run at 5000 draws per config). Encounter streams are clockwork-regular in
  aggregate, even in the storm belt (Fano 0.43). Nothing here needs burst absorption.
- **Trains:** 25–38 % of events are same-pair returns within 1.5 synodic periods (long runs);
  18–20 % of pairs are multi-event; max pair multiplicity 7–24. Pairs that meet once usually meet
  again within one synodic period: encounter certificates should survive one synodic period, not
  be dropped after the event (feeds r8 v4's pay-once-per-element-change).
- **The black-swan body does not make a black-swan second:** an e = 0.9 intruder crossing the
  whole belt took 4 events (tied for max) with Fano 1.39, inside the Poisson control. Fast
  transits spread; they do not storm.

Reproduce (each ≤ 60 s): in `crates/encounters`,
`cargo run --release --example hlive -- <name> <n> <sigma_e> <rho> <a_lo> <a_hi> <orbits> <seed> <out.csv> [intruder]`
— e.g. `cargo run --release --example hlive -- long-s11 300 0.01 1e-3 1.0 1.5 1000 11 long-s11.csv`;
then `python3 tails.py` in `work/` (exact port of the belt RNG for synodic periods and
eccentricities; prints one JSON per config, full table in `work/stats.jsonl`). Raw streams:
`work/*.csv`. New code: `crates/encounters/examples/hlive.rs` (patch captured by run.sh).

## Predictions (see predictions.md, written before these runs)

Held: P4 (T50 < 200 orbits: 55–71), P7 (narrow > 30× wide: 63×), P8 (λ linear in n: 3.04 vs
3.3 ± 30 %), P9 (bit-identical re-run). **Failed:** P1 (Gini 0.24–0.28 < 0.3; max/median 2.6–5.2,
not >10 — across-body concentration is mild once past the transient), P2 (Fano ≈ 1, not >1.5 —
no temporal burstiness), P6 (the intruder does not storm), P3 borderline (25–38 % vs >30 %: held
on one seed of three). My Taleb prior (bursts everywhere) was wrong; the tail lives in space
(cells), not time — reported as held-out failures, not smoothed over.

## What would make it wrong, cost of adoption, fit

- The truth holds orbits fixed (no scattering feedback), so measured train-clustering is a lower
  bound; absorption (first event) is unaffected by feedback — it only comes earlier.
- Events are distance minima below ρ; whether one scars is decided by the law's kick quantum
  (cell-relative, not in this crate). The q-sweep brackets it; the integrator must set q against
  B12's drift question. If the real quantum ignores ≳99.7 % of belt encounters, programs live and
  the claim weakens to "T50 is a quantum choice, not a property".
- Adoption: one step — wire the measured λ(S) into `shipmem`'s degradation ladder
  (`Rung::Rate(x)` with x = S(t)) and read bits/body; expected ≈ 0.126·(1−S) + ~50·S fresh
  entropy until repack. Belt design must then choose per cell: coherent groups (shared kicks stay
  programs — fleets, convoys), coarse quantum + drift budget, or fewer bodies.
- PRINCIPLES: "his direct influence is bounded"; "the memory floor is information-theoretic"
  (the floor of a mature belt is per-ship, not program); "Compute only surprises" (Fano ≈ 1 says
  surprises arrive at a flat mean rate per cell — the allocator can plan, but by the worst cell).

## The lens

Taleb's blind spot is speed: this run says nothing about making encounters cheaper, and its
"worst cell" instinct measured only two cell shapes (wide, narrow). Real belts have resonance
edges and collisional families (sharper than my narrow belt). The failed P2/P6 also warn: this
lens expects ruin in every tail; here the temporal tail is benign, and saying so loudly is the
run's second result.
