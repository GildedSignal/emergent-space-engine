# Dossier — 20261010-1152-second-20261010-1029-library-6cfc-fd0f (second author, library lens)

**Claim.** The checker's named experiment (the metric-vs-phase skin comparison on the engine's
real encounter path, on the taleb-09b5 formation, station-kept, with churn and e-dispersion,
counting setups and pair-evals end-to-end) splits the library run's claim: its **cost story
holds and strengthens** (the metric skin's set is saturated by the a-clump alone — 2516 pairs
and 60 ms per kick at every eps ≤ 1e-5, permanent, no phase packing needed — while the k=5
mean-longitude train holds 5 pairs and 0.42 ms, 146×), but its **correctness story is
refuted as stated**: in the concentrated regime (a 200-ship phalanx, σ_λ = 0.01, station-kept,
churned) the mean-longitude phase skin **misses 70–75% of real encounters** (partner λ-rank
max 80, p99 64, because the epicyclic amplitude 2e ≈ 0.02 rad dwarfs the bunch width), the
true-longitude ranking restores the ranks (max 5, p99 4, distance-rank ≤ 4 under churn —
taleb-09b5's evidence extends) but its **sound event-driven schedule degenerates to
watch-everyone** exactly there; and on the real multi-a belt the sound phase skin rebuilds
7.3×10⁴ times per body per orbit (the synthetic probe's belt row was an artifact of its
one-ring model). The slack lever itself survives concentration (fleet-fleet budgets ~60× the
belt's), and the adoptable form is a regime-conditional switch with a new dimensionless
trigger: clump mean-longitude spacing vs epicyclic amplitude.

**Bottleneck.** Board focus #1 and the top scaling risk; the 6 Oct gold named the slack skin
12.6× the lever and taleb-09b5 the phase-neighbour certificate. This run measures the skin
layer under concentration on the real path: it keeps the 12.6×'s base cheap where the train
applies, kills the mean-phase implementation before it is built (`q-skin`, `b-encounter-skin`),
and sizes the trigger for the switch.

**Evidence** (all in this folder; Linux x86, 8 vCPU shared, < 300 MB; `skin/` is a standalone
crate path-depending on `crates/encounters`' public API — no crate, gate or doc touched).
Reproduce (each ≤ 60 s except truth ≤ 200 s):
`cd skin && CARGO_TARGET_DIR=/tmp/st cargo build --release`, then
`/tmp/st/release/skin-probe cost fleet|belt|phalanx`, `… truth phalanx-low|uniform-low|belt`,
`… slack belt|fleet` (one JSON line per row, saved as the `*.jsonl` files here);
`cargo run --release -p emergent-encounters --bin encounters -- kick` for the anchor;
`python3 probe_skin_regen.py` for the synthetic chain of custody:

1. **Cost, end-to-end per kick** (`skin-probe cost fleet|belt|phalanx`, ≤ 60 s each;
   cert horizon 20 orbits, 100 kicks on fleet bodies, station-keep each orbit, eps grid;
   ρ = 1e-4):

   | workload | skin | pairs/kick | evals/kick | µs/kick | rebuilds/body/orbit |
   |---|---|---|---|---|---|
   | belt n=4000 | metric (cone) | 344 | 6.1k | 3075 | — |
   | belt | phase, sound rule | 5 | — | — | **7.3e4** (analytic; dead) |
   | fleet 400+3600 sea | metric | **2516** (399 clump + ~2100 sea) | 183k | 60,518 | — |
   | fleet clump | phase mean-λ k=5 | **5.0** | 12k | **417** | 1.0 |
   | phalanx 200 | metric | 199 | 78k | 22,764 | — |
   | phalanx | phase mean-λ | 5.5 | 20k | 403 | 4.2 |
   | phalanx | phase true-λ (sound bound) | **199** (degenerate) | — | 39 | 1.0 |

   Saturation is *permanent* (element-based: identical at eps = 1e-9; eps = 1e-3 shows the
   kicked body leaving the clump, 2264). The clump-internal term falls 399→5 pairs,
   ~180k→~600 evals per kick (~300×); the ~2100 sea-candidate term is radial overlap from the
   sea's own e-spread, paid identically by both skins in the full design.
2. **Correctness under churn + station-keeping** (`skin-probe truth phalanx-low|uniform-low`,
   200 ships, a=1±1e-5, e~Rayleigh(0.001), ϖ±0.1, 30 kicks at eps=1e-5, λ re-packed every
   orbit, 3 orbits, brute force dt = 5e-5, bins on true position angle ≈ 2ρ — sound for
   sub-ρ pairs; ranks computed inline at the closest step, per-pair best as in taleb-09b5):
   - phalanx (σ_λ = 0.01): **1105 encounter pairs**; distance-rank max 4, p99 3;
     **mean-λ rank max 80, p99 64**; true-λ rank max 5, p99 4. Misses: mean-λ k=4/5/8 →
     825/770/656 (75/70/59%); true-λ → 0/0/0, but only because the sound rate bound
     (dθ/dt ≤ n(1+e)/(1−e)²) makes the drift allowance (~4 rad) swallow the ring: the
     cost run shows its set = all 199. With the tight epicyclic bound (|Δn| + 2n(e_i+e_j) ≈
     0.04 rad here) the allowance still exceeds the bunch width (0.02 rad): **in the jam,
     no k-nearest watch in any orbital coordinate stays O(k) under a sound schedule** —
     bodies oscillate across the whole bunch each orbit. Not implemented for the dilute
     case (arithmetic only: spacing 0.0157 vs amplitude 0.04 → set ~k·3, still O(k)).
   - belt control (static, method-as-truth on 154 sampled bodies): λ-rank max 73, p50 38 —
     mean-λ fails on belts for the same reason (e-offset ≫ λ-spacing).
   - uniform λ (dilute clump): 2 encounters (dormant, as taleb measured 0.008/body/orbit);
     all ranks 0; zero misses for every skin. The train's cheap regime.
   - Instrument notes: three harness bugs were found and fixed before these numbers stood
     (post-hoc ranks on final elements; tighten() fed a validity where it expected an
     allowance; true-λ skins unbuilt before the first station-keep). The 51-miss and
     rank-177 intermediates were artifacts of those, not physics.
3. **The slack lever under concentration** (`skin-probe slack belt|fleet`, kick()-style
   budget bisection, horizon 100 orbits): belt pairs silent 100%, median budget 3.5e-5;
   **fleet fleet-fleet pairs silent 99%, median budget 2.1e-3 (~60× the belt's)** —
   skippable 99/99/98/62% at eps 1e-9/1e-7/1e-5/1e-3 (belt: 100/99.5/71/14%,
   fleet-sea: 100/98/57/0%, phase partners: 90/90/58/28%). The lever survives; it cannot
   fix the store (the metric skin still holds n_c² sections — taleb's 40 TB at 10⁶) or the
   scan. Anchor from shipped code, regenerated: `anchor-crate-kick.jsonl`
   (`cargo run --release -p emergent-encounters --bin encounters -- kick`, n = 10⁴, horizon
   1000 orbits): skippable 94.6/57.5/3.0/0.25% — the 12.6× regime; budgets scale ∝ 1/horizon,
   so the 100-orbit probe and the 1000-orbit anchor agree in kind.
4. **Chain of custody**: the original synthetic probe reproduces bit-for-bit
   (`python3 probe_skin_regen.py` → `probe_skin_regen_out.json`: metric belt 2.5–16 vs
   formation 300–809 pair-evals, phase 3.0/3.0 — identical to the silver dossier's table).

**Predictions** (`predictions.md`, written before any decisive run). P1 held (saturation
permanent; the "≥50× belt evals" letter reached 30× at this sea density — order held, factor
not). P2 held and was exceeded (phase 0.42 ms vs belt metric 3.1 ms). P3 split: distance
half held (max 4); **λ half refuted** (max 80, and mean-λ k=8 misses 59%) — the headline.
P4 held (7.3e4 rebuilds/body/orbit on the real belt). P5 split: belt and phase-partner halves
held; **the fleet kill-line refuted in the lever's favour** (99% skippable, not < 30%).
P6 **refuted** (`truth-belt.jsonl`, 154 sampled bodies, 49 encounters over 20 orbits):
belt partners' mean-λ rank max 73, p50 38 — the same epicyclic mechanism (2e ≈ 0.02 rad vs
belt λ-spacing 1.6e-3), so mean-longitude ranking is invalid on the real belt too, not only
in the jam. The regime map closes: mean-λ rank is sound only where clump λ-spacing ≳ 2e·r
(the dilute fleet: rank 0 measured).

**What would make this wrong.** The phalanx is one seed family (27) at one a and one σ_λ; the
regime trigger (spacing vs 2e·r) is stated, not swept. The true-λ degeneration under the
*wight* bound is measured, under the *tight* epicyclic bound it is arithmetic. The cost runs
kick fleet bodies only (sea bodies' kicks are the belt row). Truth ranks are per-pair best,
not per-event. Cloud numbers are Linux/x86 orders of magnitude.

**Cost of adoption.** Small and representation-local: `b-encounter-skin`/`q-skin` build the
train as k-nearest in mean longitude **only when the clump's λ-spacing ≳ 2·e_max·r** (the new
trigger; otherwise keep the cone/sections tier — in the jam nothing O(k) is sound), rank by
true longitude if in doubt between the two, and keep the slack skip (it holds everywhere,
strongest exactly under concentration). No crate edited; the probe is a path-depend.

**Fit with PRINCIPLES.** "A test that cannot fail is a control": the synthetic ring could not
fail on coordinate choice — the real path did. "A fix signals the wrong representation"
(P19): mean longitude was the wrong water for the fish. "Measure before claiming" (P10):
the library run's "immune" was a model artifact; the corrected certificate keeps taleb-09b5's
rank evidence and adds its boundary. "Regimes are chosen by dimensionless numbers" (P4): the
spacing/amplitude trigger.

**The lens.** Second-author lens: I took the checker's one experiment literally and ran it;
what it made me miss is the store-vs-cadence decomposition (the slack lever and the train fix
different halves — the library run's "shape not size" framing conflated them), and I nearly
shipped two broken instruments myself (the post-hoc rank computation, the tighten units) —
caught only because the first numbers were impossible (rank 177 of 199), the same lesson as
taleb-09b5's λ-binned brute.
