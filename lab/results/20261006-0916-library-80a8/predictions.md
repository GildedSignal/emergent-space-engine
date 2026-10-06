# Predictions (written before the probe run)

Probe: `probe_slack.py` — a 2-D belt (N=400, a∈[0.9,1.1] AU, Rayleigh e, σ=0.05), 60 orbits,
120 sub-steps/orbit. Kicks are the only surprise source: each body receives Poisson(λ=2/orbit)
kicks, each ±1 quantum on (a, e, ϖ) (q_a=1e-5 AU, q_e=1e-4, q_ϖ=1e-3 rad), so n and phase drift
only through quantized element changes. Certificates: per body, its k=4 phase neighbours with a
predicted next-conjunction time and closeness (the 6 Oct gold structure). Truth: all pairs with
|Δa| ≤ 0.02 AU, exact phase-crossing detection; a conjunction is CLOSE if |Δr| < τ = 0.01 AU.
A MISS is a close conjunction whose certificate was stale (predicted time off by more than its
window) or whose pair was not currently certified.

Policies:
- A `per-change` (positive control, max cost): rebuild a pair's certificate on any quantum to either member.
- B `slack` : rebuild only when the pair's accumulated quanta since last rebuild exceed m (integer m).
- C `cadence`: every certificate rebuilt every R orbits, R tuned to spend the same rebuilds as B.

Not tuned before the run (held-out cases):
1. A has ZERO misses. If A misses, the instrument is broken → VOID, no conclusions.
2. The no-kick control (λ=0) needs 0 rebuilds beyond the initial build and has 0 misses.
3. B reaches ZERO misses at some m ≤ 64 with ≥ 10× fewer rebuilds per pair-orbit than A
   (predicted m* in 8–32; rebuilds per pair-orbit ~0.1–0.5 vs A's ~2–4).
4. C, spending the same rebuild budget as B, misses (> 0 per 10⁴ pair-orbits): uniform cadence
   puts slack where nothing drifts and starves the drifted pairs (the tail), so cadence is the
   wrong trigger.
5. The dominant failure mode as m grows past m* is PARTNER drift, not timing drift: pairs whose
   phase-neighbour rank changed since the last rebuild (the skin must cover re-ranking, so the
   certificate's slack is element-quantum-wide, not time-wide).
6. The sizing rule holds: m* found in (3) is within a factor 3 of the p99 of accumulated quanta
   per pair per rebuild interval implied by τ (i.e. slack sized by the tail works, an average-sized
   slack misses).

If 3 or 4 fails, the lesson "slack sized by the tail beats cadence" is dead for certificate
maintenance, and I report it as killed (a failed configuration, not a failed method).
