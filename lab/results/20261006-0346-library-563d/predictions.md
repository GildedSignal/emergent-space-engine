# Predictions (re-frozen before the decisive run, 2026-10-06, author, library lens)

Disclosure: a first version of this file pre-filled result numbers by mistake; it was
rewritten to remove them before any full run (only a 300-item smoke test had run).
A 500-item pilot then showed two model defects, both fixed before freezing:
(a) uncapped heavy units made p99 measure the service tail, not scheduling (the engine
mandates bounded units: plane.md #7), so the cap became the positive config and the
uncapped variant the negative control; (b) a Horn-rule clairvoyant control had 69
max-lateness violations against EDF (my bug), so it was replaced by a trivially correct
control: EDF with all arrivals pre-rolled to t=0 = perfect prediction + legal
compute-ahead (the engine's idle-time speculation; it ignores discard cost, so it is an
UPPER bound on what any forecast machinery could ever buy for ordering).

Probe: `work/allocator_probe.py` — preemptive-resume single server; 70% cheap units +
30% heavy Pareto(alpha) units (capped at 40 mean-cheap-units, or uncapped as negative
control); Pareto(1,1.5) interarrival gaps (bursts); deadline = arrival + causal slack,
log-uniform over 3 decades; exact utilization rho by timeline rescaling; n=5000 items,
10 seeds per cell; lateness normalized by mean service. Policies: FIFO, SRPT, EDF,
LeastLaxity (the design, engine.md rule 5), Clairvoyant-as-compute-ahead.

## Held-out predictions (not tuned on; parameters fixed a priori)

- **P1 (discipline vs naive):** at rho=0.7, alpha=1.5, capped: LeastLaxity p99 ≤ 0.6 ×
  FIFO p99.
- **P2 (the slack formula is not the lever):** LeastLaxity within 1.25 × of EDF p99 in
  every capped cell.
- **P3 (bounded units are load-bearing):** uncapped p99 ≥ 3 × capped p99 for
  LeastLaxity at rho=0.7, alpha=1.2.
- **P4 (headroom is a lever):** LeastLaxity p99 at rho=0.95 ≥ 3 × its p99 at rho=0.7
  (capped, alpha=1.5).
- **P5 (forecast headroom exists):** Clairvoyant p99 ≤ 0.5 × EDF p99 at rho=0.9,
  alpha=1.5, capped.

## What happened (after the decisive run: `python3 work/allocator_probe.py 5000 10`,
20.5 s, clairvoyant-vs-EDF validity control violations: 0)

- **P1 HELD:** LeastLaxity p99 = 14.5 vs FIFO 32.5 (0.45× ≤ 0.6) at rho=0.7,
  alpha=1.5, capped. The advantage shrinks with load: 1.5× at rho=0.9, 1.07× at 0.95.
- **P2 HELD:** LeastLaxity/EDF p99 ratio ≤ 1.18 in all nine capped cells. The slack
  ordering formula is on the online frontier; nothing >~1.2× is hiding in ordering.
- **P3 FAILED at the named cell** (capped 3412 vs uncapped 411: wrong direction).
  Diagnosis: the timeline rescale makes slack-to-work tighter in the capped config at
  alpha=1.2, a confound between cap and deadline tightness. The control does blow up as
  expected in 7/9 cells (uncapped/capped = 2.8×-39× at rho ≥ 0.9); the cap comparison
  is a lead with a named confound, not a result.
- **P4 HELD:** LeastLaxity p99 14.5 (rho=0.7) → 158.4 (rho=0.95), 10.9× ≥ 3×.
- **P5 HELD, kill criterion did NOT fire:** Clairvoyant compute-ahead p99 = −3.6 vs
  EDF 56.9; deadline misses 0.9% vs 30.8% at rho=0.9, alpha=1.5 (and 3.7% vs 45.6%
  at 0.95). Upper bound (ignores speculation discard cost), disclosed as such.
- **Beyond predictions:** SRPT has the best mean flow and the worst max lateness
  (Lmax 643–2753 in capped cells vs 25–149 for EDF/LeastLaxity): ordering by unit
  size starves exactly the tail Julien's p99 rule exists to protect.
