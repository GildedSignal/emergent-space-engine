# Predictions (written before any arm of the decisive experiment ran)

Question: does the belt's boundary comb ride the step lever with the kick comb (the
kick-cadence page's open direction 1), i.e. is the boundary welded to the same `full` the
kick closes (`step.rs` `kick_clock`: boundary at `t + full/2`, kick at `t + full`, one `full`
from `ext.time(y, ds)`, `ds` set once from `cfg.step_log2` at `plan_clock`)?

No arm of this experiment has run when this is written. The anchors I lean on (14,072 and
28,141.5 game-s, 1.00 + 1.00 events/body/interval) are other runs' published numbers
(3294, 8ffc), not measurements of mine.

Arms: `belt_combs <N=10000> <rtf=2400> <wall=30> <step_log2>`, step_log2 ∈ {7 (shipped), 8}.
Held-out for the checker: another N (e.g. 3×10⁴), another rtf, and step_log2 = 6.

1. **The lever moves the step (control).** Genesis first-kick h p50 at step_log2 = 8 is
   2.00× ± 1% of the step_log2 = 7 value (≈ 28,14x against ≈ 14,07x game-s). If h does not
   double, `step_log2` is not a step lever and the whole design is VOID.
2. **The counters ride together.** boundaries/kicks over ≥ 1.5 intervals ∈ [0.97, 1.03] at
   BOTH arms (belt-dominated at N = 10⁴: the belt's 2/body/interval dwarfs the locals).
3. **Both rates halve.** kicks/gs and boundaries/gs at step_log2 = 8 are each 0.5× ± 5% of
   the step_log2 = 7 arm.
4. **The welding identities hold per body.** After ≥ 1.5 intervals, ≥ 99.5% of belt bodies
   hold exactly 1 Boundary + 1 Kick item in the standing plan; (K − B)/h p50 ∈ [0.99, 1.01];
   interval/(2h) p50 ∈ [0.98, 1.02] (the step recomputes from the kicked state: small drift
   allowed); (B mod interval)/interval p50 < 0.02 (the boundary comb at the interval's edge,
   the kick comb half an interval later — the two combs of 8ffc).
5. **The branch that would falsify welding:** if the boundary comb has a metronome of its
   own, arm 8 keeps boundaries/gs at the arm-7 value while kicks/gs halves, and
   (B mod interval)/interval spreads ~uniform. That branch would pin a ~16-core M1 floor at
   10⁹ that no split can remove (the ledger's negative branch).

Ledger arithmetic the answer decides (regenerates in `ledger.py`): with both combs riding
any step lever, the 10⁹ belt stream at split S is 233/S cores x86 at rtf 100 (65.6 µs per
body per interval: 52.7 kick + 12.9 boundary, 8ffc's costs), ≈ 79.6/S on the M1 anchor
(kick 29.3 µs, boundary 7.2 µs by the same ratio, survival 0.615) — closable at S ≈ 20
(4e2d's S* = 20.7); with the boundary pinned, ≥ ~16 M1 cores at every S (unclosable).
