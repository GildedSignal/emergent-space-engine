# Predictions (written before the member sweep; only the 48-member shipped default was run, for calibration)

Question: where is the plane's single-thread capacity today — the member count at which the
smoothness contract (p99 frame ≤ 16.7 ms at rtf 100, 60 Hz) breaks — and which resource binds
there (engine advance, view gather, JSON, memory)?

Cases I have NOT run when writing this: members 10³, 10⁴, 10⁵, 10⁶, at rtf 100 and rtf 1.

1. **Capacity point.** The plane holds p99 frame < 16.7 ms and rtf median ≈ 100 up to 10⁴
   members; at 10⁵ members it breaks (p99 > 16.7 ms or overflow_frames > 1% of frames).
   Fermi: engine p99 ≈ 1.7 ms at 71 bodies with ~0.2 ms per resolved event and events/s
   scaling with bodies (410/s at 71 → ~6 per body per game-second; 1.67 s of game per frame
   at rtf 100).
2. **Shape.** Median frame CPU grows with exponent ≈ 1.0 (±0.15, fitted over 10³–10⁵) while
   the fleets are still separated. The p99.9 tail grows faster than the median once real
   contact batches appear (the fleets merge inside the horizon at larger member counts,
   because the crossing takes separation/relative-speed ticks and separation grows as √n).
3. **Tail control.** p99.9/p50 stays below 10 up to the capacity point (the causal-deadline
   order bounds the tail); if it exceeds 10 the allocator is the story, not the capacity.
4. **Readout.** view_gather + view_json share grows with members; at 10⁵ members the readout
   (gather+JSON), not the engine, holds the majority of the worst frame.
5. **Memory.** bytes_per_body falls as fixed scene costs amortise (5,189 B at 71 bodies),
   settling near a few hundred B; 10⁶ members stay under 1 GB resident.

Controls: same seed and input log run twice must give the same digest (determinism); rtf 1
at the breaking member count must still hold (else the break is the scene's contact rate,
not the plane's per-event capacity).
