# Dossier — 20261007-0800-fermi-a91f (Fermi lens)

**Claim.** H_live is bounded and reabsorbable — a kicked body costs ~50 bits once and ~2 bits per
doubling of further exposure, not 44 bits per kick — so at 10⁹ bodies the first wall is memory,
not compute: a fully-mixed population (7.9 GB at 63 bits/body) busts the 8 GB machine, while all
kick compute (hot update + compaction) runs at ~8% of one core.

**Bottleneck.** HANDOFF's named risk "Distinctions created per game-second (H_live): they, not
the body count, decide whether 10⁹ fit in 8 GB; **not measured yet**", and board item "fitting
10⁹ in 8 GB decided by distinctions created per game-second". Expected gain: no new component;
it sizes the B18 gate (add a repeated-kick scene), fixes the affordable-population number for
the billion-ship design, and deletes the fear that H_live compounds (it does not).

**Evidence** (agonbox, i7-4790, load 1.2, 14 GB free; all runs ≤ 30 s, < 1 GB; machine.txt).
Driver `hlive.rs` (copy in this folder; added as `crates/shipmem/examples/hlive.rs` in the
patch) uses only shipped code: the frozen ladder's `Rung::Rate(0.0)` convoy, `Pop::Convoy.kick`
(the law's integer kick model: Δt ±2¹⁶, ΔE/ΔL/Δω ±2¹⁰), `Shelf::{add_group,get,update,compact}`.

- Commands (each ≤ 60 s):
  - `HLIVE_OUT=state.jsonl  cargo run --release -p emergent-shipmem --example hlive -- state 1048576`
  - `HLIVE_OUT=shelf-a.jsonl cargo run --release -p emergent-shipmem --example hlive -- shelf 1048576 8 0.25`
  - `HLIVE_OUT=shelf-b.jsonl cargo run --release -p emergent-shipmem --example hlive -- shelf 1048576 16 0.5`
  - `cargo run --release -p emergent-encounters -- verify a`
- **State floor vs kick count K** (every ship kicked K times; `state.jsonl`): 49.9 bits/ship at
  K=1 (the frozen ladder's 50.0 reproduced), 58.4 at 16, 65.2 at 256, 68.3 at 1024 — ≈ 4×(11 +
  ½log₂K) + 6, i.e. ~2 bits per doubling. The draw account (what a naive store or a logged
  history pays) is 44·K: at K=256 it is 173× the floor.
- **Shipped store under repeated kicks** (`shelf-*.jsonl`, bit-exact round trip every epoch,
  mismatches=0, including repacks): store stays 0.8–7 bits above the state floor; a repack fires
  near K̄≈4.5 and *drops* stored bits 66.6→62.5 while the floor rises — the store re-fits by exact
  cost, as law.md §Populations promises. At K̄=8 (essentially every ship ever-kicked, mean 8
  kicks): 7.94 bytes/ship vs floor 7.06. No compounding: the gap stabilises ≈ 7 bits.
- **Compute per kick**: hot update 30 ns median (p99 1.2 µs on first-touch blocks); compaction
  650 ms per 524 288 kicks = 1.23 µs/kick, flat across epochs. Total ≈ 1.26 µs/kick → the board's
  6×10⁴ kicks/game-second cost ≈ 76 ms/s ≈ 8% of one core.
- **Encounter-rate anchors** (shipped `verify a`, rho 1e-4): 1.75×10⁻⁴–5×10⁻³ encounters per body
  per orbit. Ever-kicked fraction f hits 0.5 after 139–3 960 orbits (r8 v2's belt 0, at ~1.1×10⁻²,
  would do it in ~65); at target scale (≈5×10³ game-s/orbit, from representation.md's 6×10⁴
  kicks/s ÷ 10⁹×0.3 kicks/orbit; rtf 100 → 50 s of play per orbit) that is ~1–55 play-hours —
  the wall is in-play, not hypothetical.

**Fermi budget at 10⁹** (8 GB total; ≈4–6 GB for bodies after OS, engine, view): affordable
32–48 bits/body → f_wall ≈ 0.5–0.75 of bodies ever-kicked at 63 bits each. Equivalently a
fully-mixed population tops out at N_max ≈ 5–7×10⁸ bodies. Compute terms: kicks 0.3% of a core,
recompression 8%, encounter discovery (cone, constant per encounter at fixed density) — memory
binds first, by 2–3×, and it is the only term that grows with play time.

**Predictions** (`predictions.md`, written before the runs): P1 (floor 44–70 bits, log growth) —
held (49.9→68.3, slope 1.6–2.8 bits/doubling). P2 (draw account >100× floor at K=256) — held
(173×). P3 (store within 2× floor + 2 B through K̄≈8, no compounding, bit-exact) — held. P4
(reabsorption < 5 µs/kick, < 30% of a core) — held (1.26 µs, 8%). P5 (all-kicked ≈ 6.25 GB,
does not fit beside the engine) — held and sharpened: measured 7.9 GB at K̄=8 with store overhead.

**What would make it wrong.** The kick model is shipmem's frozen `Pop::kick` (uniform integer
deltas on fixed widths); real tidal kicks have heavy-tailed magnitudes — a tail wider than the
column grid would push the floor toward the 208-bit random rung faster than log growth. Victims
were drawn independently; real encounters are spatially correlated, which *helps* compression
(neighbours share the event), so my f-growth is pessimistic. Machine is x86 cloud: orders of
magnitude only; the integrator re-measures on the M1. Costs measured at n=2²⁰; per-kick
compaction cost could grow with group count at 10⁹ (not tested above 16 groups).

**Cost of adopting.** None as code (measurements on shipped code only). Design consequences:
(1) B18 should add a repeated-kick saturation scene — the single-pass ladder cannot see the
equilibrium this run measures, and a store could pass B18 while compounding at K̄>1. (2) The
billion-ship design should treat f (ever-kicked fraction) as its memory dial: re-programming
diffused cohorts in idle time (repack already does this by cost) is what holds 10⁹ inside 8 GB.
(3) The "190 cores for 10⁹" board number belongs to the pre-H0190 configuration; at today's
measured kick costs the 10⁹ kick load is ~0.3% of one core — compute is not the wall.

**Fit with PRINCIPLES.** "The memory floor is information" (24): measured, the floor moves with
exposure (50→68 bits), so the budget is a rate equation, not a fixed bytes×count. "Compute only
surprises" (3): the first kick is the surprise (44 bits); later kicks add almost nothing (~2
bits/doubling). "Store the generator, not the generated" (6): confirmed quantitatively — 63 bits
of scars against 88 bytes of `Body`, and the store re-fits by exact cost.

**The lens.** Fermi estimates before building, but I nearly shipped a wrong shelf measurement
(group-offset bug in handle mapping: 983 041 false mismatches) — caught only because the byte
count landed *below* the information floor, which is impossible for a lossless store. The lens
should say: an estimate that violates its own floor is a broken instrument, not a good result.

**Grade suggested:** silver-to-gold. It moves a named, unmeasured bottleneck with shipped-code
measurements and held predictions; gold if the integrator accepts that sizing B18 and the f-dial
is adoptable within one step (no new code, one gate scene).
