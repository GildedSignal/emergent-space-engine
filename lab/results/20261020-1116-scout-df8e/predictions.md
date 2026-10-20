# Predictions (written before the decisive flights)

Question: the standing comb (0a46) is mint-synchrony on the belt's shared fictitious-clock
period (ext constants are per-doll, f' near-flat across the belt; every Ext is born with
`dt_carry: 0` at step.rs:632, so every belt clock starts at s=0 together). If so, a
deterministic golden-ratio phase rule injected at Ext creation (zero stored bits, one
u128 multiply; the "deterministic jitter" of the thundering-herd literature, legal under
exact determinism) should flatten the arrival stream and delete the freeze channel.

Arms: shipped tree, `nladder 100000 burn <s> 2000 12`, seed 1 (the record's scene).
Arm OFF = shipped bits (dt_carry 0). Arm ON = ES_CLOCK_SPREAD=1 (golden dt_carry at
Ext creation). Per-frame CSV (frame, ms, events, gs, lag) is print-only, env-gated.

- P1 (anchor): OFF reproduces the record family on this box: a wave onset at gs
  12.5k-14.5k, worst frame 400-1,300 ms at 1e5 (record family ~718-820 ms on quieter
  boxes), arrivals ~1 event/body in the crest window.
- P2 (the claim): ON deletes the freeze channel: worst frame < 50 ms at 1e5 over >= 2
  comb eras (>= 15x on the record's worst frame). If the crest still combs (peak/mean
  of arrivals in 1,500-gs bins > 2, or any frame > 100 ms inside a crest era), the
  golden phase rule is KILLED as the comb's cure.
- P3 (law conservation): total events and events/body/era equal across arms within
  +-2% (a phase move, not a rate move).
- P4: ON's p99 <= 12.5 ms at 1e5.
- P5 (held-out risk, the finding either way): if ON's era-to-era worst frames still
  alternate (clean-era cost << crest-era cost for identical arrivals), then the
  47-vs-12 us/event served-path split (0a46) is NOT arrival-shape-dependent and
  survives flattening - the comb was only the freeze's trigger, not its cost.
- P6 (determinism): ON rerun gives a bit-identical per-frame CSV.

Kill bars: K1 - if OFF shows no comb at all (no onset, flat arrivals, max < 100 ms),
the premise (mint-synchrony comb at these rungs) is wrong on this box and nothing is
gradeable. K3 = P2's failure bar. A control that cannot pass is a broken instrument.
