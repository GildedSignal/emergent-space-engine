# Predictions (written after the 3e5 anatomy draw a1, before the unfenced 1e5 draws)

The 3e5 draw (a1) flew before these were written (time pressure; disclosed). What it showed,
and what the remaining draws must decide:

a1 (3e5, fence TTL=16): max frame 2,647 ms = the unstaggered kick comb (52,079 events,
~51 µs/ev — the off-arm of 9ed1, no stagger in my patch); 126 captures walked ALL 300,076
bodies (radial filter bailed) at 74-91 ms each, on the player's item (critical path); the
largest ANSWER was 11 ms / 2,612 candidates, read_ns = 97.3% of answer ns, skip_dom 2607/2612
= 99.8%; scans with cand=299,715 were captured and NEVER answered (aged out at TTL) — the
guard (room ≥ 2·max(scan_ns, 750µs) ≤ 24 ms) can never admit a ~1.2 s answer into a 12 ms
budget; it opens only after the running max decays 1/64 per cheap answer.

## Held-out predictions for the unfenced 1e5 draws (no TTL; the answer must run somewhere)

- P1: at least one draw shows a worst frame ≥ 300 ms whose anatomy is ONE answer line with
  cand ≈ 1e5 (the belt-wide scan answered to completion, unguarded — at drain(None) in
  flush/settle or after guard decay), ns ≈ 3-6e8 (3-6 µs/body), read_ns ≥ 90% of ns.
- P2: that answer's skip_dom ≥ 99% of cand (the bound's ceiling in the belt).
- P3: unfenced peak RSS at 1e5 lands near 1.9 GB (9ed1's 1,887 MB) — the fence is what kept
  a1's held queue small, and with it the big scans die unanswered: the fence deletes the
  answer channel's work (the encounter log differs — a law change, now measured as total).
- P4: the capture channel is fence-independent: every draw shows radial=ALL captures of
  ~0.25-0.3 µs/body whether or not any big answer runs (it is the player's item, not idle
  work; "the scans are already off the critical path" is false twice — capture is ON it).

Kill bar: if no unfenced draw produces a ≥300 ms single-answer frame at 1e5 after 3 seeds,
the "one uninterruptible belt-wide answer" reading of 9ed1's bite is wrong and the freeze
must live elsewhere (then: find the frame's anatomy by matching frame index to CAP/ANS lines).
