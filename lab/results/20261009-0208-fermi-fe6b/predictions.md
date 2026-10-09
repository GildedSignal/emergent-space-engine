# Predictions (written before any measurement output was observed)

Written 09:5x UTC, before reading `cost.rs` output (job launched but not yet observed) and
before running the reabsorption micro-bench. No number below was tuned on any run.

The budget being tested: N = 10⁹ real bodies, one 8 GB M1 (4 P-cores + 4 E, ~68 GB/s unified,
~10¹⁰ simple ops/s CPU), belt-like diffuse population at fixed distribution, orbital period
P = 1.26e8 game-seconds (4 yr, AU scale), real-time factor rtf = 100 (the plane's current
speed). Held-out cases = the ones I have not fitted anything on:

1. **Shipped-code event costs** (`cargo run --release -p emergent-universe --example cost`,
   Linux x86 shared runner, orders of magnitude only):
   - `compile` (one cycle from (E,L)): **20–200 µs**.
   - `state` (signed state at a time): **1–10 µs**.
   - `cartesian`: **1–5 µs**. `from_state` (rebinding): **5–50 µs**.
   - None of these comes within a factor 10 of the measured 4.3 ms per-kick certificate
     cascade at n=10⁴ (r8, M1); i.e. the cascade, not the compiler, is the kick's cost.

2. **Reabsorption ceiling** (re-band 10⁷–10⁸ synthetic (E,L) scars, this machine):
   ≥ 5×10⁷ bodies/s on one core. So reabsorption exceeds scar creation at 10⁹ by ≥ 3 orders
   at rtf 100 (creation ≈ N·k/P·rtf with k ≈ 0.28 kicks/orbit ≈ 222 scars/s).

3. **Term ranking at 10⁹, rtf 100** (the claim of the run):
   - certificate cascade on kicks, fixed-density two-tier certs + slack skin (12.6×):
     **0.5–10 s of work per real second (10–250% of one core)** — the only term above 10%
     of a core;
   - kicks proper (incremental multiply-add, ~50 ns + 0.05 compiles/kick): < 1% of a core;
   - encounter handling (0.04 encounters/body/orbit at fixed density, ~1 µs each): < 2%;
   - program memory (0.126 bit/body, gold components-98bc): ~16 MB — free;
   - scars at live fraction 1%: ~2.4×10⁸ B — fits with ≥ 10× margin; at live fraction > 30%
     it breaks 8 GB;
   - per-body event keys (one (time, id) pair per body): 12–16 GB — **does not fit**; the
     queue must key programs/blocks, not bodies. Prediction: this is a structural rule the
     b-h-live build must adopt.

4. **Claim checks:**
   - The board's "10⁹ orbiting bodies at today's rates would need about 190 cores"
     re-derives as the no-averaging (k = 32/orbit), no-skin cascade at rtf ≈ 5–20: my table
     must reproduce 100–400 cores in that corner, i.e. agree within 2×.
   - representation.md §6's kick row ("~50 ns each, < 1% of a core") is right about the
     kick arithmetic and **wrong about the belt workload by ≥ 10³×** because it omits the
     certificate cascade; with k = 0.28, skin, and phase-neighbour certificates the row
     becomes true again (< 1 core in 4).

5. **What would kill the budget:** a corner where the cascade cannot be thinned —
   near-resonance belts (kicks keep conjunction phase, k per conjunction, not per orbit:
   representation.md:68) or concentrated fleets (taleb-09b5). If the resonant belt's k
   rises to per-conjunction (~n_conj/orbit ~ O(1–10)), the cascade term multiplies by
   3–30 and 10⁹ needs the dense order locally, not certificates.
