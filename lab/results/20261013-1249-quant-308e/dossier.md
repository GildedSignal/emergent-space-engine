# Dossier — 20261013-1249-quant-308e (Quant)

**Claim.** The compile's `cos` lever is dead twice over on x86: the primitive already sits at its
single-chain ISA latency floor (41.6 ns, not 7d2b's 77 ns), and interleaving the panel's four
independent cos chains — the wiki's named, untested open direction — buys 1.51× per cos in
isolation but **0% at the compile**, because the core's out-of-order window already overlaps
those chains inside `fast_quad`; the compile's cos cost is port throughput, not chain latency.

**Bottleneck.** `kick-jet` open direction 1/1a: "interleaving the four nodes' independent chains
if the walk is latency-bound (untested)" and "the `cos` series (77 ns)". This run closes both
halves by measurement. Expected gain was compile −4–12%; the realized gain is 0%, which deletes
the direction (the next lever inside the node is panel count alone — a law change, as c914/9384
already narrowed).

**Evidence** (all from shipped code + `work/patch.diff`, Linux/x86 i7-4790-class shared, orders
of magnitude; arms compared only within one wall-clock epoch):

1. **Primitive (fuzz 2M operands lane-wise, bit-identity of `cos_tuned`/`cos4` vs `cos`):**
   `cos shipped 41.6 ns | tuned 41.2 ns | cos4 lane 27.6 ns | isqrt(u128) ref 56.0 ns`
   (cargo test, `num::bench::cos_variants`). The shipped loop is already at its dependency-chain
   floor: 13 nested factors × (mul 3c + extract ~2c + mul 3c + extract ~2c + sub 1c) ≈ 143–150
   cycles ≈ 40–42 ns at 3.6 GHz. 7d2b's 24%-of-a-320 ns-node ≈ 77 ns attribution was ~1.9×
   inflated. Codegen is not a lever (`cos_tuned`, fully unrolled straight line: 41.2 ns).
2. **Compile-level A/B (28-key plane-like grid, p = 2^20…2^32, e = 0…0.99, median of 3×40
   compiles per key, `COS4` env switch inside one binary, pinned core, epochs interleaved):**
   `B(cos) 25.2/25.1/24.9/25.4 µs` vs `I(cos4) 25.4/25.5/24.9/25.3 µs` — no difference at any
   percentile (min 4.4–4.7, max 115–117 both arms). The isolated 1.51× does not survive the node.
   (Naive back-to-back arms are worthless on this box — identical base code measured 18.9 µs
   and 24.7 µs in two epochs minutes apart; the naive pair, recorded: base 18.9/19.4 µs and
   patched 18.6–18.8 µs in the earlier fast epoch, an apparent −3–5% that was pure drift —
   hence the interleaved one-binary protocol above is the evidence).
4. **Mechanism, stated for the M1 check:** `fast_quad` evaluates four cos per panel at
   `mid ± dx₀, mid ± dx₁` — four independent 13-step chains. OoO execution fills the chains'
   latency bubbles with the panel's other independent work (4 divisions at their measured
   hardware floor, u64 isqrt, products), so total time is set by port pressure; `cos4` executes
   the *same* 26 floored multiplies per cos (no fewer ops), only reorders them — hence 0%. On any
   core with a deep OoO window the same holds; only an in-order target (some GPU lanes) could
   profit, and the plane is not compiled there.

**Predictions.** `predictions.md` was written before the patched A/B: band 1 (−4–12%) missed
low; prediction 5 (the registered risk — "the OoO window may already interleave the chains, then
the honest claim is the primitive's 1.51× does not survive the node") is what the measurement
returned. Prediction 2 (per-key gradient) is void — no aggregate movement to gradient. Bit-identity
(prediction 3) held exactly.

**What would make it wrong.** A compile workload whose panels are not the fast path (compact
near-separatrix keys use `node()` with a single cos per Gauss point, serially dependent on the
Scalar algebra around it) could still hide cos latency differently — but that path is rarer than
the plane's regime, and its cos calls sit inside longer Scalar chains, making interleave even less
plausible. The claim is x86 (Haswell-class, shared); the M1 re-measure would need the same
interleaved-epoch protocol. Cost of adopting: none — the patch is an A/B scaffold, not a proposal
to merge; the result retires the direction instead.

**Fit with PRINCIPLES.** "The cheapest compute is compute not done" — this run deletes a
planned optimization (the interleave build) by measuring it to zero, and corrects a wrong number
(77 ns) before anyone budgets against it; "Measure before claiming"; a falsifiable prediction was
registered before the decisive run and its low band missed honestly.

**Commands** (each ≤ 60 s unless noted): `regen.sh` runs all of the above end to end (≈ 3 min
including the 60 s suite).

**The lens (what Quant may have missed).** HFT instinct prices chain latency because books are
serial; here the node is a wide independent bundle and the hardware is the interleaver — the
profitable question becomes port pressure (fewer ops, e.g. panel count or a cheaper exact `cos`
with *fewer* floored products — impossible without changing bits), not scheduling. I did not
profile the divisions' port pressure on this box (c914 measured their latency floor), and I did
not touch the per-band serial `cut()` isqrt chain (9384's −9.5% lives there, unhidden by OoO —
consistent with this run's mechanism).
