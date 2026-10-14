Working...
Check complete. Summary of the verdict:

**Grade: silver** — written to `lab/results/20261014-1221-scout-0b81/check.md`, with the author's proposed `wiki/encounters.md` corrected in place where it overstated.

**What reproduced cleanly**
- `regen.sh` rerun identical to `gate-out.txt` on every line; empty patch, no files outside the run folder; `predictions.md` (12:28) predates the decisive run (12:35).
- Anchors verified against shipped code and the record: `Key.energy` is Q48 (`crates/space/src/lib.rs:171–178`), a `Carry` accumulates sub-quantum increments (`handoff.rs:125`); c7eb/62f7/90fb/1738 citations all match the published wiki.
- Both mass controls and the phase-vacuity result (1/K → 0) confirmed.

**What fell (my adversarial case, outside the author's tested range)**
- The author validated the impulse formula against RK4 but never the miss-distance model against real orbits. Direct Kepler integration (random ω, 10³-orbit horizon, 4×10⁶ samples): the model's `b_min` is **6×10²–9×10³× too large at Δa ∈ [0.005, 0.05]** — real conjunction misses are quasi-periodic and revisit near-zero (the r8-v2 lead's own structure; generic, not the "resonant minority" the dossier scoped).
- Corrected decisive run: deletable **0.955–0.978** (not 0.9996), survivors 2.2–4.5×10⁻², ledger **37–369 cores** against the 4-core budget; the all-10-km negative control flips to 0.000; ×52 real-belt mass → 0.64; Q52 → 0.78; cold belt → 0.82.
- Second unflagged gap: the ledger prices the gate's own per-refresh comparison at zero; with the author's own 786 evals/encounter the top anchor alone adds ~10 cores.

**Why silver, not lead:** the mechanism, controls, vacuity proof and content-dial direction stand, and the corrected ceiling (gate alone ≈ 20–45×, budget needs the flux split on top) is itself decision-grade — it vindicates the author's original prediction 4 over the run's outcome. The one gold experiment: re-derive the yield with Kepler-true per-Δa miss distributions and price the gate's per-refresh cost against the cascade (f79a's ~4 µs/pair).
