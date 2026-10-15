# Predictions (written before the probe runs)

Probe: `nladder_lin` (this run's Linux port of the shipped `nladder.rs`, read-only + one gather per
wall second — the view the player actually has), N = 10^4 and 3x10^4, coast, rtf 6000, 12 ms budget,
flown ~40 s wall (~240,000 game-s ≈ 8-9 wave periods; b30b's protocol, view on). Census at the end:
RSS, store bytes/body (`bytes_of` sum), retired-history bodies, catalogue, warm gather ms,
`seen`, ViewCache readouts, digest.

Priors: b30b (headless plateau 4.85-5.06 kB/body at 10^5, 5.58 at 10^4), 0e37 (store held 1,806
B/body at 10^5, 74.3% knots; retired belt tables read 0 times in flight — headless), cf45 (wave
spacing ~27.5 k game-s).

1. **Plateau**: RSS/body at 10^4 lands 5.3-5.9 kB (b30b's 5.58 ± platform offset); flat over the
   last 3 waves (slope < 200 B/body/wave).
2. **Store share**: sum(bytes_of)/N lands 1.7-2.0 kB/body; more than half the bodies hold >= 1
   retired segment at steady state (the wave retires every belt body once per wave).
3. **The view sees everything**: `seen` >= 0.99 N at both N — on this scene there are no invisible
   bodies to delete records for; the Asimov cut cannot come from unobserved bodies, only from
   serving the same reader with keys instead of knots.
4. **Knots' steady reader with the view on**: warm gather <= 3 ms at 10^4 and readouts/body/gather
   ~ 1-3; the crossing reads the record, not the knot tables — so a 1 Hz view adds ~0 steady knot
   reads (0e37's headless 0-reads survives the view being on, except through the ramp completion).
5. **Digest**: view-on flight settles to a digest equal to the same cut flown view-off (gathers
   mutate nothing) — checked by flying 10^4 once with the gather disabled (ES_NO_GATHER=1).

If 3 fails (seen << N), the deletion target is the unseen fraction and lesson 2 changes shape. If 4
fails (warm gather >> 3 ms or readouts/body >> 3), the view is a steady mass reader of knots and
0e37's two-word completion becomes load-bearing for the frame, not just memory.
