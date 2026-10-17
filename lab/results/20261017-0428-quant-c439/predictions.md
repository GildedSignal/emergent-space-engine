# Predictions (written before the decisive runs)

The question: the burn read stream at 10⁹ (promotion page, open direction 1: "what are the
resolver's re-reads FOR"). Instrument: `prof::reads` census on shipped main (patch:
counters only, feature-gated), example `read_census` = the ladder's flight (plane_extra,
rtf 100, 12 ms budget, burn at L8 from 1 s, counters from 1 s).

Cases I have NOT tuned on (the smoke run was N=100 burn 5 s only):

- **P1 (the reader).** In every burn arm the player's neighbourhood scan (`scan: candidate`)
  owns ≥ 70% of all `binding_at` calls. Coast arms read ≥ 10× less in total (the scan items
  sit on the burn's cadence).
- **P2 (the scaling — decisive).** Scan reads per scan grow linearly with N: reads/scan ≈
  bodies within 1.5× at N = 100, 10⁴, 10⁵ (the radial apsidal filter returns "most of the
  doll" in the root doll, so capture reads every body). If reads/scan stays ~O(400) (the
  filter cuts the belt), the scan is NOT the 10⁹ read knee and this prediction fails.
- **P3 (the events).** Event-side reads (`state_of` + `ext::source` + `root_state_raw` +
  `rec: advance`) run ≈ 2–4 per kick plus one `rec` per kick; over a wave-free burn window
  that is ≥ 10× below the scan's rate, and at the wave (13–14.5k gs) it appears as one burst
  of ~3–5 reads per body.
- **P4 (the hits).** ≥ 95% of reads hit the current binding (the history walk is rare in
  flight); misses ≈ 0.
- **P5 (the price and the 10⁹ projection).** One `binding_at` ≈ 40–90 ns on this box (a
  192 B Binding clone). If P1+P2 hold, the scan alone demands ~1.75 scans/gs × N reads per
  game-second (≈1.75e11 reads/s at 10⁹, rtf 100) — no store can serve that: the deletion has
  to make the scan itself read-free (answer from an index/certificate), not make reads
  cheaper.
- **P6 (bits).** The census binary (feature `prof`) and the plain build print the same
  flight digest at identical args (the counters change nothing).

Kill criterion for my own claim: if P1 or P2 fails, the burn read stream is not the scan's,
and the dossier says so with the measured owner instead.

# What happened (after the runs)

- **P1 — held, magnitude wrong.** The scan owns 79% of burn `binding_at` calls (148,996 of
  188,181) and 52% at coast (33,875 of 64,935); coast totals are 2.9× below burn, not ≥10×
  (the coast scan is rarer — 184 scans vs 2,127 — but wider, 184 reads a scan).
- **P2 — REFUTED, by its own kill criterion.** Reads/scan is 70.0 at burn at BOTH N=1e4 and
  1e5 (absolute scan-read counts identical: 148,996 at both N; all readers' counts equal to
  0.03%). The radial apsidal filter cuts the belt; the scan reads a bounded near set. The
  read demand is O(1) in N, not N-linear.
- **P3 — held.** Reads/event 2.85 (burn window), 3.41 (coast), 4.28 (through the wave:
  state_of 1.57 + root_state_raw 1.81 + rec 0.89 per event); the wave is the burst.
- **P4 — held.** History hits 0.06–4.3% (2,794 of 64,935 worst, the coast scan's older
  ticks), misses 0 everywhere.
- **P5 — moot as feared (P2 failed); the honest projection:** observer reads at 10⁹ rtf 100
  ≈ 7.7e3/s (O(1)); event-riding reads = 1.7e-5 kicks/body/gs × 4.3 × 1e9 × 100 ≈ 7e6/s
  (~0.7 core at the measured ~96 ns) — the kick cadence's mint bill, not a separate knee.
- **P6 — held.** Plain and prof binaries print the same digest (d1822b88…) at identical
  args; repeated runs stable under wall jitter.
