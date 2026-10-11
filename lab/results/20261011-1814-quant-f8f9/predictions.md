# Predictions (written before any run; only `cargo build` has happened)

Question: on the shipped plane (`xtask universe --bench`, the player's frame loop), which stage
owns the presented frame's tail, what is ns/event, where does the engine budget saturate in rtf,
and does the digest stay schedule-independent under a squeezed budget?

Cases (none tuned on — first runs of the shipped binary on this machine):

- P1 (stage shares). At rtf 100, members 48: the readout (gather + JSON + wire) owns > 50% of the
  summed frame time; the engine advance < 40%. Basis: 48 members is tiny, the view+serialisation
  walks everything every frame whatever the rtf.
- P2 (tail). At rtf 100: worst frame CPU ≥ 5× its p50 CPU; hitch count above 16.7 ms is nonzero
  over 900 frames but < 5% of frames. Basis: compile/rebind bursts; budget is 5 ms so bursts
  beyond it must defer, but the view is unbudgeted.
- P3 (capacity). Overflow fraction and delivered rtf degrade monotonically in rtf; at rtf 1000 the
  engine misses the cut (presented_tick_at_end < cut_tick) or overflow frames exceed ~30%.
- P4 (per-event cost). Engine CPU ns/event at rtf 100 stays within 2× from members 48 to 400
  (work per event independent of N at plane scale; events per member roughly constant).
- P5 (schedule independence). Same seed, rtf, seconds and cut with engine budgets 1 ms vs 15 ms,
  and paced vs unpaced: identical digest. Basis: the budget changes when work is done, never what
  (plane.md foundation 7).
- P6 (the arithmetic to the goal). Delivered events/s at saturation is 10^4–10^5 per core-second;
  at the goal's kick rates (≤ 32 kicks/orbit, target 10^9 bodies at rtf ≥ 100) the gap between
  measured events/s and required events/s is ≥ 10^3×, so cadence (events per body), not ns per
  event, must close it — ns/event would have to reach ~0.01–0.1 ns, below one cycle.

Kill criteria for my own claim: if P1–P5 all hold, the frame ledger stands as measured; if P5
fails (digests differ), that is a severe premise break to report, not a tuning issue.
